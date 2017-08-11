# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def findPlId(c):
    plInfo = SendCmd(c, 'pool')
    plId = []
    row = plInfo.split('\r\n')

    for i in range(4, len(row) - 2):
        if len(row[i].split()) >= 9:
            plId.append(row[i].split()[0])

    return plId

def findPdId(c):
    plId = findPlId(c)
    pdId = []
    if len(plId) != 0:
        for i in plId:
            SendCmdconfirm(c, 'pool -a del -f -i ' + i)
        pdInfo = SendCmd(c, 'phydrv')
        pdRow = pdInfo.split('\r\n')

        for i in range(4, (len(pdRow) - 2)):
            if "Unconfigured" in pdRow[i] and 'HDD' in pdRow[i]:
                pdId.append(pdRow[i].split()[0])

        return pdId

    else:
        pdInfo = SendCmd(c, 'phydrv')
        pdRow = pdInfo.split('\r\n')

        for i in range(4, (len(pdRow) - 2)):
            if "Unconfigured" in pdRow[i] and 'HDD' in pdRow[i]:
                pdId.append(pdRow[i].split()[0])
        return pdId

def bvt_verifyRbStartAndStopAndList(c):
    FailFlag = False
    tolog("verify rb start")

    # precondition
    # delete spare driver
    spareInfo = SendCmd(c, 'spare')
    if 'No spare drive exists' not in spareInfo:
        spareId = []
        spareRow = spareInfo.split('\r\n')
        for i in range(4, len(spareInfo) - 2):
            if len(spareRow[i]) >= 8 :
                spareId.append(spareRow[i].split()[0])

        for i in spareId:
            SendCmd(c, 'spare -a del -i ' + i)

    raid = ['1', '5', '6', '10', '50', '60']
    pdId = findPdId(c)
    if len(pdId) >= 9:
        for rd in raid:
            tolog('verify raid' + rd + ' rebuild start')
            # create pool
            if rd == '1':
                createPool = SendCmd(c, 'pool -a add -s "name=testRb, axle=2, raid=' + rd + '" -p ' + pdId[0]
                                     + ',' + pdId[1])

                if 'Error (' in createPool:
                    tolog("To create pool is failed")
                    break
            elif rd == '50' or rd == '60':
                createPool = SendCmd(c, 'pool -a add -s "name=testRb, axle=2, raid=' + rd + '" -p ' + pdId[0]
                                     + ',' + pdId[1] + ',' + pdId[2] + ',' + pdId[3] + ',' + pdId[4] + ','
                                     + pdId[5] + ',' + pdId[6] + ',' + pdId[7])

                if 'Error (' in createPool:
                    tolog("To create pool is failed")
                    break
                time.sleep(10)
            else:
                createPool = SendCmd(c, 'pool -a add -s "name=testRb, axle=2, raid=' + rd + '" -p ' + pdId[0]
                                     + ',' + pdId[1] + ',' + pdId[2] + ',' + pdId[3] + ',' + pdId[4] + ','
                                     + pdId[5] + ',' + pdId[6] + ',' + pdId[7])
                if 'Error (' in createPool:
                    tolog("To create pool is failed")
                    break

            # offline pd
            if int(rd) >= 10:
                offlinePd = SendCmd(c, 'phydrv -a offline -p ' + pdId[0])
                if 'Error (' in offlinePd:
                    tolog('To offline is failed')
                    break
                time.sleep(10)
            else:
                offlinePd = SendCmd(c, 'phydrv -a offline -p ' + pdId[0])
                if 'Error (' in offlinePd:
                    tolog('To offline is failed')
                    break

            result = SendCmd(c, 'rb -a start -l 0 -s 0 -p ' + pdId[8])
            checkResult = SendCmd(c, 'rb')
            if 'Error (' in result or 'This background activity is not running' in checkResult:
                FailFlag = True
                tolog('Fail: ' + 'rb -a start -l 0 -s ' + pdId[0] + ' -p ' + pdId[8])

            tolog('verify rb list when rb starting')
            rbList = SendCmd(c, 'rb')
            if 'Error (' in rbList or 'This background activity is not running' in rbList:
                FailFlag = True
                tolog('Fail: rb')

            tolog('verify raid' + rd + ' rebuild stop')
            result = SendCmd(c, 'rb -a stop -l 0 -s 0')
            checkResult = SendCmd(c, 'rb')
            if 'Error (' in result or 'This background activity is not running' not in checkResult:
                FailFlag = True
                tolog('Fail: ' + 'rb -a stop -l 0 -s 0')

            tolog('verify rb list when rb stopped')
            rbList = SendCmd(c, 'rb')
            if 'Error (' in rbList or 'This background activity is not running' not in rbList:
                FailFlag = True
                tolog('Fail: rb')

            # delete pool
            deletePool = SendCmdconfirm(c, 'pool -a del -f -i 0')
            if 'Error (' in deletePool:
                tolog('To delete pool is failed')
                break

    else:
        tolog('\n\n The lack of pd')
        exit()

    if FailFlag:
        tolog('\n<font color="red">Fail: rb start and stop</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def bvt_verifyRbInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify rb invalid option</b>")
    command = ['rb -x',
               'rb -a list -x',
               'rb -a start -x',
               'rb -a stop -x'
               ]
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rb invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def bvt_verifyRbInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify rb invalid parameters</b>")
    command = ['rb -a list x',
               'rb -a start x',
               'rb -a stop x',
               # the pool id range is 0-31
               'rb -a start -l 32 -s 0 -p 12',
               'rb -a start -l -1 -s 0 -p 12',
               # the sequence number range is 0-511
               'rb -a start -l 0 -s -1 -p 12',
               'rb -a start -l 0 -s 512 -p 12',
               # the pd id range is 1-512
               'rb -a start -l 0 -s 0 -p -1',
               'rb -a start -l 0 -s 0 -p 513',
               ]
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rb invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def bvt_verifyRbMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify rb missing parameters</b>")
    command = ['rb -a start -l ',
               'rb -a start -l 0 -s ',
               'rb -a start -l 0 -s 0 -p ',
               'rb -a stop -l',
               'rb -a stop -l 0 -s'
               ]
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify rb missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    bvt_verifyRbStartAndStopAndList(c)
    bvt_verifyRbInvalidOption(c)
    bvt_verifyRbInvalidParameters(c)
    bvt_verifyRbMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped