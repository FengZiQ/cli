# coding=utf-8
# work on 2017.8.7

from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn

Pass = "'result': 'p'"
Fail = "'result': 'f'"

def findBgaSId(c):
    bgaSInfo = SendCmd(c, 'bgasched')
    bgaSId = []
    if 'Type' and 'ID' in bgaSInfo:
        row = bgaSInfo.split('\r\n')
        for i in range(4, len(row)-2):
            if len(row[i].split()) >= 6:
                bgaSId.append(row[i].split()[1] + ':' + row[i].split()[0])
    else:
        tolog('There is no bgasched')
    return bgaSId

def verifyBgaschedAdd(c):
    FailFlag = False

    # precondition
    def delOldBgasched(c):
        bgaSInfo = SendCmd(c, 'bgasched')
        if 'Type' and 'ID' in bgaSInfo:
            bgaSId = findBgaSId(c)
            for typeId in bgaSId:
                if 'BatteryRecondition' in typeId:
                    SendCmd(c, 'bgasched -a del -t br -i ' + typeId[0])
                elif 'SpareCheck' in typeId:
                    SendCmd(c, 'bgasched -a del -t sc -i ' + typeId[0])
                elif 'RedundancyCheck' in typeId:
                    SendCmd(c, 'bgasched -a del -t rc -i ' + typeId[0])

    # delete old bgasched
    delOldBgasched(c)

    # create pool
    def findPoolId(c):
        plInfo = SendCmd(c, 'pool')
        PoolId = []

        if 'No pool in the subsystem' in plInfo:
            pdInfo = SendCmd(c, 'phydrv')
            pdId = []
            pdRow = pdInfo.split('\r\n')
            for i in range(4, (len(pdRow)-2)):
                if "Unconfigured" in pdRow[i]:
                    pdId.append(pdRow[i].split()[0])
            if len(pdId) >= 5:
                SendCmd(c, 'pool -a add -s "name=testBgasched1, raid=1" -p ' + pdId[0] + ',' + pdId[1])
                SendCmd(c, 'pool -a add -s "name=testBgasched2, raid=0" -p ' + pdId[2] + ',' + pdId[3])
                SendCmd(c, 'pool -a add -s "name=testBgasched3, raid=0" -p ' + pdId[4])
            else:
                tolog('\n\n The lack of pd')
                exit()
        else:
            row1 = plInfo.split('\r\n')
            for i in range(4, len(row1) - 2):
                if 'OK' in row1[i]:
                    PoolId.append(row1[i].split()[0])

            for i in PoolId:
                SendCmdconfirm(c, 'pool -a del -f -i ' + i)

            pdInfo = SendCmd(c, 'phydrv')
            pdId = []
            pdRow = pdInfo.split('\r\n')
            for i in range(4, (len(pdRow)-2)):
                if "Unconfigured" in pdRow[i]:
                    pdId.append(pdRow[i].split()[0])
            if len(pdId) >= 5:
                SendCmd(c, 'pool -a add -s "name=testBgasched1, raid=1" -p ' + pdId[0] + ',' + pdId[1])
                SendCmd(c, 'pool -a add -s "name=testBgasched2, raid=0" -p ' + pdId[2] + ',' + pdId[3])
                SendCmd(c, 'pool -a add -s "name=testBgasched3, raid=0" -p ' + pdId[4])
            else:
                tolog('\n\n The lack of pd')
                exit()

        plInfo2 = SendCmd(c, 'pool')
        row2 = plInfo2.split('\r\n')
        for i in range(4, len(row2)-2):
            if 'OK' in row2[i]:
                PoolId.append(row2[i].split()[0])

        return PoolId

    poolId = findPoolId(c)
    type = ['rc', 'br', 'sc']
    listType = ['RedundancyCheck', 'BatteryRecondition', 'SpareCheck']
    defaultStatus = ['OperationalStatus: Disabled']
    defaultStartTime = ['StartTime: 22:00', 'StartTime: 02:00', 'StartTime: 22:00']
    # recurtype = ['daily', 'weekly', 'monthly']

    # add bgasched of daily type
    tolog('add bgasched of daily type')
    for i in range(0, 3):
        if type[i] == 'rc':
            result = SendCmd(c, 'bgasched -a add -t ' + type[i] + ' -s "recurtype=daily,poolid=' + poolId[0] + '"'),\
                     SendCmd(c, 'bgasched -a add -t ' + type[i] + ' -s "recurtype=daily,poolid=' + poolId[1] + '"')
        else:
            result = SendCmd(c, 'bgasched -a add -t ' + type[i] + ' -s "recurtype=daily"')
        checkResult = SendCmd(c, 'bgasched -v -t ' + type[i])
        if 'Error (' in result or listType[i] not in checkResult or defaultStatus[0] not in checkResult or defaultStartTime[i] not in checkResult:
            tolog('Fail: ' + 'bgasched -a add -t ' + type[i])
            FailFlag = True

    # pool of raid0 can not create rc bgasched
    result = SendCmd(c, 'bgasched -a add -t rc -s "recurtype=daily,poolid=2"')
    if 'Error (' not in result:
        FailFlag = True
        tolog('Fail: bgasched -a add -t rc -s "recurtype=daily,poolid=2"')

    delOldBgasched(c)


    if FailFlag:
        tolog('\n<font color="red">Fail: To verify add bgasched </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)





if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyBgaschedAdd(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped