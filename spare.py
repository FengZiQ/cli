# coding=utf-8
# 2017.9.19

from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
import xlrd

Pass = "'result': 'p'"
Fail = "'result': 'f'"

def findPdId(c):

    pdInfo = SendCmd(c, 'phydrv')

    if 'Pool' in pdInfo:

        poolId = []

        poolInfo = SendCmd(c, 'pool')
        row = poolInfo.split('\r\n')

        for i in range(4, len(row) - 2):
            if len(row[i].split()) >= 8:
                poolId.append(row[i].split()[0])

        for i in poolId:
            SendCmd(c, 'pool -a del -y -f -i ' + i)

    pdInfo = SendCmd(c, 'phydrv')

    if 'Spare' in pdInfo:
        spareId = []

        spareInfo = SendCmd(c, 'spare')
        row = spareInfo.split('\r\n')

        for i in range(4, len(row) - 2):
            spareId.append(row[i].split()[0])

        for i in spareId:
            SendCmd(c, 'spare -a del -i ' + i)

    pdInfo = SendCmd(c, 'phydrv')
    line = pdInfo.split('\r\n')

    pdId2 = []
    pdId4 = []

    for i in range(4, len(line)):

        if len(line[i]) >= 10 and 'Unconfigured' in line[i] and 'HDD' in line[i] and line[i].split()[4] == '2':
            pdId2.append(line[i].split()[0])

        elif len(line[i]) >= 10 and 'Unconfigured' in line[i] and 'HDD' in line[i] and line[i].split()[4] == '4':
            pdId4.append(line[i].split()[0])

    return pdId2, pdId4

def addGlobalSpare(c):
    FailFlag = False

    # precondition(need 4 2TB and 4TB HDD physical drive)
    tolog('=======================================precondition========================================\r\n')

    pdId2, pdId4 = findPdId(c)

    if len(pdId2) >= 4 or len(pdId4) >= 4:
        tolog('\r\n\r\nNeed 4 block 2TB and 4TB HDD physical drive\r\n\r\n')

    SendCmd(c, 'pool -a add -s "name=testSpare1,raid=1" -p ' + pdId2[0] + ',' + pdId2[1])

    tolog('\r\n=======================================precondition========================================')

    # Add global and not revertible spare
    tolog('\r\nAdd global and not revertible spare\r\n')

    result = SendCmd(c, 'spare -a add -t g -r n -p ' + pdId2[2])

    if 'Error (' in result:
        FailFlag = True
        tolog('\r\nFail: spare -a add -t g -r n -p ' + pdId2[2] + '\r\n')

    else:
        checkResult = SendCmd(c, 'spare')

        if 'OK' not in checkResult or 'Global' not in checkResult:
            FailFlag = True
            tolog('Fail: please check out spare status and type')

        else:
            SendCmd(c, 'phydrv -a offline -p ' + pdId2[0])

            time.sleep(10)

            checkRB = SendCmd(c, 'rb')

            if 'Running' not in checkRB:
                FailFlag = True
                tolog('Fail: please check out rb progress')

            else:
                SendCmd(c, 'pool -a del -f -y -i 0')

                pdInfo = SendCmd(c, 'phydrv -p ' + pdId2[2])

                if 'Unconfigured' not in pdInfo:
                    FailFlag = True
                    tolog('Fail: please check out parameter -r(revertible) n')

    # Add global and revertible spare
    tolog('\r\nAdd global and revertible spare\r\n')

    # precondition
    SendCmd(c, 'pool -a add -s "name=testSpare2,raid=1" -p ' + pdId4[0] + ',' + pdId4[1])

    result = SendCmd(c, 'spare -a add -t g -r y -p ' + pdId4[2])

    if 'Error (' in result:
        FailFlag = True
        tolog('\r\nFail: spare -a add -t g -r y -p ' + pdId4[2] + '\r\n')

    else:
        checkResult = SendCmd(c, 'spare')

        if 'OK' not in checkResult or 'Global' not in checkResult:
            FailFlag = True
            tolog('Fail: please check out spare status and type')

        else:
            SendCmd(c, 'phydrv -a offline -p ' + pdId4[0])

            time.sleep(10)

            checkRB = SendCmd(c, 'rb')

            if 'Running' not in checkRB:
                FailFlag = True
                tolog('Fail: please check out rb progress')

            else:
                SendCmd(c, 'pool -a del -f -y -i 0')

                pdInfo = SendCmd(c, 'phydrv -p ' + pdId4[2])

                if 'Revert' not in pdInfo:
                    FailFlag = True
                    tolog('Fail: please check out parameter -r(revertible) y')


    if FailFlag:
        tolog('\n<font color="red">Fail: Verify spare -a add </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def addDedicatedSpare(c):
    FailFlag = False

    # precondition
    tolog('=======================================precondition========================================\r\n')

    pdId2, pdId4 = findPdId(c)

    SendCmd(c, 'pool -a add -s "name=testSpare1,raid=1" -p ' + pdId2[0] + ',' + pdId2[1])

    SendCmd(c, 'pool -a add -s "name=testSpare2,raid=1" -p ' + pdId4[0] + ',' + pdId4[1])

    tolog('\r\n=======================================precondition========================================')

    tolog('\r\nAdd dedicated and not revertible spare\r\n')

    result = SendCmd(c, 'spare -a add -t d -r n -d 0,1 -p ' + pdId4[2])

    if 'Error (' in result:
        FailFlag = True
        tolog('Fail: spare -a add -t d -r n -d 0,1 -p ' + pdId4[2])

    else:
        checkResult = SendCmd(c, 'spare')

        if 'OK' not in checkResult or 'Dedicated' not in checkResult:
            FailFlag = True
            tolog('Fail: please check out spare status and type')

        else:
            SendCmd(c, 'phydrv -a offline -p ' + pdId2[0])

            time.sleep(20)

            checkRB = SendCmd(c, 'rb')

            if 'Running' not in checkRB:
                FailFlag = True
                tolog('Fail: please check out rb progress')

            else:
                SendCmd(c, 'pool -a del -y -f -i 0')
                SendCmd(c, 'pool -a del -y -f -i 1')

                pdInfo = SendCmd(c, 'phydrv -p ' + pdId4[2])

                if 'Spare' in pdInfo:
                    FailFlag = True
                    tolog('Fail: please check out parameter -r(revertible) n')

    tolog('\r\nAdd dedicated and revertible spare\r\n')

    # precondition
    SendCmd(c, 'pool -a add -s "name=testSpare3,raid=1" -p ' + pdId2[0] + ',' + pdId2[1])

    result = SendCmd(c, 'spare -a add -t d -r y -d 0 -p ' + pdId2[2])

    if 'Error (' in result:
        FailFlag = True
        tolog('Fail: spare -a add -t d -r y -d 0 -p ' + pdId2[2])

    else:
        checkResult = SendCmd(c, 'spare')

        if 'OK' not in checkResult or 'Dedicated' not in checkResult:
            FailFlag = True
            tolog('Fail: please check out spare status and type')

        else:
            SendCmd(c, 'phydrv -a offline -p ' + pdId2[0])

            time.sleep(10)

            checkRB = SendCmd(c, 'rb')

            if 'Running' not in checkRB:
                FailFlag = True
                tolog('Fail: please check out rb progress')

            else:
                SendCmd(c, 'pool -a del -y -f -i 0')

                pdInfo = SendCmd(c, 'phydrv -p ' + pdId2[2])

                if 'Spare' not in pdInfo:
                    FailFlag = True
                    tolog('Fail: please check out parameter -r(revertible) y')

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)

    return FailFlag

def verifySpareList(c):
    FailFlag = False

    # precondition
    tolog('=======================================precondition========================================\r\n')

    pdId2, pdId4 = findPdId(c)

    SendCmd(c, 'pool -a add -s "name=testSpare1,raid=1" -p ' + pdId2[0] + ',' + pdId2[1])

    SendCmd(c, 'pool -a add -s "name=testSpare2,raid=1" -p ' + pdId4[0] + ',' + pdId4[1])

    SendCmd(c, 'spare -a add -t g -r n -p ' + pdId2[2])

    SendCmd(c, 'spare -a add -t g -r y -p ' + pdId2[3])

    SendCmd(c, 'spare -a add -t d -r n -d 0 -p ' + pdId4[2])

    SendCmd(c, 'spare -a add -t d -r y -d 0,1 -p ' + pdId4[3])

    tolog('\r\n=======================================precondition========================================')

    # List all of spare
    tolog('\r\nList all of spare \r\n')

    result = SendCmd(c, 'spare')
    row = result.split('\r\n')

    if 'Error (' in result:
        FailFlag = True
        tolog('\r\nFail: spare\r\n')

    # List specific spare
    tolog('\r\nList specific spare\r\n')

    spareId = []

    for i in range(4, len(row) - 2):
        spareId.append(row[i].split()[0])

    if len(spareId) >= 1:

        for i in spareId:
            listResult = SendCmd(c, 'spare -i ' + i)

            if 'Error (' in listResult:
                FailFlag = True
                tolog('\r\nFail: spare -i ' + i + '\r\n')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify spare </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifySpareVList(c):
    FailFlag = False

    # precondition
    tolog('=======================================precondition========================================\r\n')

    pdId2, pdId4 = findPdId(c)

    SendCmd(c, 'pool -a add -s "name=testSpare1,raid=1" -p ' + pdId2[0] + ',' + pdId2[1])

    SendCmd(c, 'pool -a add -s "name=testSpare2,raid=1" -p ' + pdId4[0] + ',' + pdId4[1])

    SendCmd(c, 'spare -a add -t g -r n -p ' + pdId2[2])

    SendCmd(c, 'spare -a add -t g -r y -p ' + pdId2[3])

    SendCmd(c, 'spare -a add -t d -r n -d 0 -p ' + pdId4[2])

    SendCmd(c, 'spare -a add -t d -r y -d 0,1 -p ' + pdId4[3])

    tolog('\r\n=======================================precondition========================================')

    # List all of spare
    tolog('\r\nList all of spare by verbose mode\r\n')

    result = SendCmd(c, 'spare -v')
    row = result.split('\r\nId: ')

    if 'Error (' in result:
        FailFlag = True
        tolog('\r\nFail: spare -v\r\n')

    # List specific spare
    tolog('\r\nList specific spare by verbose mode\r\n')

    spareId = []

    for i in range(1, len(row)):
        spareId.append(row[i][0])

    if len(spareId) >= 1:

        for i in spareId:
            listResult = SendCmd(c, 'spare -v -i ' + i)

            if 'Error (' in listResult:
                FailFlag = True
                tolog('\r\nFail: spare -v -i ' + i + '\r\n')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify spare -v </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifySpareSpecifyInexistentId(c):
    FailFlag = False
    tolog("\r\n<b> Verify spare specify inexistent Id </b>\r\n")

    date = xlrd.open_workbook('data/spare.xlsx')

    talbe = date.sheet_by_name('inexistentID')

    for i in range(1, talbe.nrows):

        result = SendCmd(c, talbe.cell(i, 0).value)

        # if 'Error (' not in result:
        #     FailFlag = True
        #     tolog('\r\nFail: ' + talbe.cell(i, 0).value + '\r\n')

        if talbe.cell(i, 1).value not in result:
            FailFlag = True

            tolog('\r\nFail: ' + talbe.cell(i, 0).value)

            tolog('\r\nPlease check out checkpoint')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify spare specify inexistent Id </font>')
        tolog(Fail)

    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifySpareInvalidOption(c):
    FailFlag = False
    tolog("\r\n<b>Verify spare invalid option</b>\r\n")

    date = xlrd.open_workbook('data/spare.xlsx')

    talbe = date.sheet_by_name('invalidOption')

    for i in range(1, talbe.nrows):

        result = SendCmd(c, talbe.cell(i, 0).value)

        if 'Error (' not in result or talbe.cell(i, 1).value not in result:
            FailFlag = True
            tolog('\r\nFail: ' + talbe.cell(i, 0).value + '\r\n')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify spare invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifySpareInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify spare invalid parameters</b>")

    date = xlrd.open_workbook('data/spare.xlsx')

    talbe = date.sheet_by_name('invalidParameter')

    for i in range(1, talbe.nrows):

        result = SendCmd(c, talbe.cell(i, 0).value)

        if 'Error (' not in result or talbe.cell(i, 1).value not in result:
            FailFlag = True
            tolog('\r\nFail: ' + talbe.cell(i, 0).value + '\r\n')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify spare invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifySpareMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify spare missing parameters</b>")

    date = xlrd.open_workbook('data/spare.xlsx')

    talbe = date.sheet_by_name('missingParameter')

    for i in range(1, talbe.nrows):

        result = SendCmd(c, talbe.cell(i, 0).value)

        if 'Error (' not in result or talbe.cell(i, 1).value not in result:
            FailFlag = True
            tolog('\r\nFail: ' + talbe.cell(i, 0).value + '\r\n')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify spare missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifySpareDel(c):
    FailFlag = False
    tolog("\r\n<b>Verify spare -a del </b>\r\n")

    spareId = []

    spareInfo = SendCmd(c, 'spare')
    row = spareInfo.split('\r\n')

    for i in range(4, len(row) - 2):
        spareId.append(row[i].split()[0])

    for i in spareId:

        tolog('\r\n delete spare ' + i + '\r\n')

        result = SendCmd(c, 'spare -a del -i ' + i)

        if 'Error (' in result:
            FailFlag = True
            tolog('Fail: spare -a del -i ' + i + '\r\n')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify spare -a del </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    SendCmd(c, 'pool -a del -f -y -i 0')
    SendCmd(c, 'pool -a del -f -y -i 1')

    return FailFlag

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    addGlobalSpare(c)
    addDedicatedSpare(c)
    verifySpareList(c)
    verifySpareVList(c)
    verifySpareSpecifyInexistentId(c)
    verifySpareInvalidOption(c)
    verifySpareInvalidParameters(c)
    verifySpareMissingParameters(c)
    verifySpareDel(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped