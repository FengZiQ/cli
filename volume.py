# coding = utf-8
# 2017.9.17

from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
import time
import xlrd
import random

Pass = "'result': 'p'"
Fail = "'result': 'f'"


def findPoolId(c):
    pdinfo = SendCmd(c, 'phydrv')

    poolId = []

    if 'Pool' in pdinfo:
        poolInfo = SendCmd(c, 'pool')
        row = poolInfo.split('\r\n')

        for i in range(4, len(row)-2):
            if len(row[i].split()) >= 8:
                poolId.append(row[i].split()[0])

        for i in poolId:
            SendCmd(c, 'pool -a del -y -f -i ' + i)

        SendCmd(c, 'pool -a add -s "name=test_volume,raid=5" -p 4,9,8')
        poolId = ['0']

    else:
        SendCmd(c, 'pool -a add -s "name=test_volume,raid=5" -p 4,9,8')
        poolId = ['0']

    return poolId


def addVolume(c):
    FailFlag = False
    tolog('Verify: add volume\r\n')

    findPoolId(c)

    data = xlrd.open_workbook("data/volume.xlsx")

    table = data.sheet_by_name('addVolume')

    for i in range(1, table.nrows):

        command = 'volume -a add -p 0 -s "' + \
               str(table.cell(0, 0).value) + '=' + str(table.cell(i, 0).value) + ',' + \
               str(table.cell(0, 1).value) + '=' + str(table.cell(i, 1).value) + ',' + \
               str(table.cell(0, 2).value) + '=' + str(table.cell(i, 2).value) + ',' + \
               str(table.cell(0, 3).value) + '=' + str(table.cell(i, 3).value) + ',' + \
               str(table.cell(0, 4).value) + '=' + str(table.cell(i, 4).value) + ',' + \
               str(table.cell(0, 5).value) + '=' + str(table.cell(i, 5).value) + '"'

        tolog('\r\nExpect: Add volume by name ' + table.cell(i, 0).value + '\r\n')
        result = SendCmd(c, command)

        if 'Error (' in result:
            FailFlag = True
            tolog('Fail: ' + command + '\r\n')
        else:
            time.sleep(1)
            checkResult = SendCmd(c, 'volume -v -i ' + str(i - 1))

            if table.cell(i, 0).value not in checkResult:
                FailFlag = True
                tolog('\r\nFail: please check out volume name\r\n')
            elif table.cell(i, 4).value not in checkResult:
                FailFlag = True
                tolog('\r\nFail: please check out volume sync\r\n')
            elif table.cell(i, 5).value not in checkResult:
                FailFlag = True
                tolog('\r\nFail: please check out volume thinprov\r\n')
            else:
                tolog('\r\nActual: volume ' + table.cell(i, 0).value + ' is added \r\n')

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)

    return FailFlag


def listVolume(c):
    FailFlag = False
    tolog('\r\nVerify: List volume \r\n')

    # List all of volume
    tolog('Expect: List all of volume \r\n')

    allResult = SendCmd(c, 'volume')

    if 'Error (' in allResult:
        FailFlag = True
        tolog('Fail: volume \r\n')
    else:
        tolog('\r\nActual: all of volume are listed')

    # List all of volume by verbose mode
    tolog('\r\nExpect: List all of volume by verbose mode\r\n')

    allVResult = SendCmd(c, 'volume -v')

    if 'Error (' in allVResult:
        FailFlag = True

        tolog('\r\nFail: volume -v \r\n')
    else:
        tolog('\r\nActual: All of volume are listed by verbose mode\r\n')

    # List specific volume
    tolog('Verify: List specific volume\r\n')
    volumeId = []

    volumeInfo = SendCmd(c, 'volume')
    row = volumeInfo.split('\r\n')

    for i in range(4, len(row) - 2):
        if len(row[i].split()) >= 9:
            volumeId.append(row[i].split()[0])

    i = random.choice(volumeId)

    tolog('\r\nExpect: list volume ' + i + '\r\n')

    listResult = SendCmd(c, 'volume -i ' + i)

    if 'Error (' in listResult:
        FailFlag = True
        tolog('\r\nFail: volume -i ' + i + '\r\n')
    else:
        tolog('\r\nActual: volume ' + i + ' is listed\r\n')

    # List volume by verbose mode
    ii = random.choice(volumeId)

    tolog('\r\nExpect: list volume ' + ii + ' by verbose mode \r\n')

    listVResult = SendCmd(c, 'volume -v -i ' + ii)

    if 'Error (' in listVResult:
        FailFlag = True
        tolog('\r\nFail: volume -v -i ' + ii + '\r\n')
    else:
        tolog('\r\nActual: volume ' + ii + ' is listed by verbose mode\r\n')

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)

    return FailFlag


def modVolume(c):
    FailFlag = False
    tolog('\r\nVerify: modify volume\r\n')

    data = xlrd.open_workbook("data/volume.xlsx")

    table = data.sheet_by_name('modVolume')

    for i in range(1, table.nrows):
        tolog('Expect: To modify name is ' + table.cell(i, 0).value + '\r\n')

        result = SendCmd(c, 'volume -a mod -i 0 -s "name=' + table.cell(i, 0).value + '"')

        if 'Error (' in result:
            FailFlag = True
            tolog('Fail: volume -a mod -i 0 -s "name=' + table.cell(i, 0).value + '"')
        else:
            checkResult = SendCmd(c, 'volume -v -i 0')
            if table.cell(i, 0).value not in checkResult:
                FailFlag = True
                tolog('\r\nFail: please check out volume name\r\n')
            else:
                tolog('\r\nActual: volume name is modified\r\n')

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)

    return FailFlag


def exportVolume(c):
    FailFlag = False
    tolog('\r\nVerify: export volume\r\n')

    volumeInfo = SendCmd(c, 'volume -i 1')

    if 'Exported' in volumeInfo:

        # precondition
        SendCmd(c, 'volume -a unexport -i 1')

        tolog('\r\nExpect: export volume 1 \r\n')

        result = SendCmd(c, 'volume -a export -i 1')

        if 'Error (' in result:
            FailFlag = True
            tolog('\r\nFail: volume -a export -i 1\r\n')
        else:
            checkResult = SendCmd(c, 'volume -i 1')

            if 'Exported' not in checkResult:
                FailFlag = True
                tolog('\r\nFail: please check out volume status\r\n')
            else:
                tolog('\r\nActual: volume 1 is exported \r\n')
    else:
        tolog('\r\nExpect: export volume 1 \r\n')

        result = SendCmd(c, 'volume -a export -i 1')

        if 'Error (' in result:
            FailFlag = True
            tolog('\r\nFail: volume -a export -i 1\r\n')
        else:
            checkResult = SendCmd(c, 'volume -i 1')

            if 'Exported' not in checkResult:
                FailFlag = True
                tolog('\r\nFail: please check out volume status\r\n')
            else:
                tolog('\r\nActual: volume 1 is exported \r\n')

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)

    return FailFlag


def unexportVolume(c):
    FailFlag = False
    tolog('\r\nVerify: un-export volume\r\n')

    volumeInfo = SendCmd(c, 'volume -i 1')

    if 'Un-Exported' in volumeInfo:

        # precondition
        SendCmd(c, 'volume -a export -i 1')

        tolog('\r\nExpect: un-export volume 1 \r\n')

        result = SendCmd(c, 'volume -a unexport -i 1')

        if 'Error (' in result:
            FailFlag = True
            tolog('\r\nFail: volume -a unexport -i 1\r\n')
        else:
            checkResult = SendCmd(c, 'volume -i 1')

            if 'Un-Exported' not in checkResult:
                FailFlag = True
                tolog('\r\nFail: please check out volume status\r\n')

            else:
                tolog('\r\nActual: volume 1 is un-exported \r\n')
    else:
        tolog('\r\nExpect: un-export volume 1 \r\n')

        result = SendCmd(c, 'volume -a unexport -i 1')

        if 'Error (' in result:
            FailFlag = True
            tolog('\r\nFail: volume -a unexport -i 1\r\n')
        else:
            checkResult = SendCmd(c, 'volume -i 1')

            if 'Un-Exported' not in checkResult:
                FailFlag = True
                tolog('\r\nFail: please check out volume status\r\n')

            else:
                tolog('\r\nActual: volume 1 is un-exported \r\n')

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)

    return FailFlag


def invaildName(c):
    FailFlag = False
    tolog('\r\nVerify: invalid setting name\r\n')

    data = xlrd.open_workbook("data/volume.xlsx")

    table = data.sheet_by_name('invalidName')

    for i in range(1, table.nrows):
        tolog('Expect: hint error and information contains: ' + table.cell(i, 1).value + '\r\n')

        result = SendCmd(c, 'volume -a mod -i 0 -s "name=' + table.cell(i, 0).value + '"')

        if 'Error (' not in result or table.cell(i, 0).value not in result:
            FailFlag = True
            tolog('\r\nFail: volume -a mod -i 0 -s "name=' + table.cell(i, 0).value + '"\r\n')
        else:
            tolog('\r\nActual: return error and information contains: ' + table.cell(i, 1).value + '\r\n')

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)

    return FailFlag


def invalidParameter(c):
    FailFlag = False
    tolog('\r\nVerify: invalid setting parameter')

    data = xlrd.open_workbook("data/volume.xlsx")

    table = data.sheet_by_name('invalidParameter')

    for i in range(1, table.nrows):

        tolog('\r\nExpect: hint ' + table.cell(0, i).value + ' is ' + table.cell(i, 6).value + '\r\n')

        command = 'volume -a add -p 0 -s "' + \
               str(table.cell(0, 0).value) + '=' + str(table.cell(i, 0).value) + ',' + \
               str(table.cell(0, 1).value) + '=' + str(table.cell(i, 1).value) + ',' + \
               str(table.cell(0, 2).value) + '=' + str(table.cell(i, 2).value) + ',' + \
               str(table.cell(0, 3).value) + '=' + str(table.cell(i, 3).value) + ',' + \
               str(table.cell(0, 4).value) + '=' + str(table.cell(i, 4).value) + ',' + \
               str(table.cell(0, 5).value) + '=' + str(table.cell(i, 5).value) + '"'

        result = SendCmd(c, command)

        if 'Error (' not in result or table.cell(i, 6).value not in result:
            FailFlag = True
            tolog('\r\nFail: ' + command + '\r\n')
        else:
            tolog('\r\nActual: ' + result.split('\r\n')[-3] + '\r\n')

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)

    return FailFlag


def invalidOption(c):
    FailFlag = False
    tolog('\r\nVerify: invalid setting option')

    data = xlrd.open_workbook("data/volume.xlsx")

    table = data.sheet_by_name('invalidOption')

    for i in range(1, table.nrows):

        tolog('\r\nExpect: hint error and information contains invalid option\r\n')

        command = table.cell(i, 0).value

        result = SendCmd(c, command)

        if 'Error (' not in result or table.cell(i, 1).value not in result:
            FailFlag = True
            tolog('\r\nFail: ' + command + '\r\n')

        else:
            tolog('\r\nActual: ' + result.split('\r\n')[1] + ' && ' + result.split('\r\n')[2])

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)

    return FailFlag


def missingParameter(c):
    FailFlag = False
    tolog('\r\nVerify: invalid setting option')

    data = xlrd.open_workbook("data/volume.xlsx")

    table = data.sheet_by_name('missingParameter')

    for i in range(1, table.nrows):

        tolog('\r\nExpect: hint error and information contains missing parameter\r\n')

        command = table.cell(i, 0).value

        result = SendCmd(c, command)

        if 'Error (' not in result or table.cell(i, 1).value not in result:
            FailFlag = True
            tolog('\r\nFail: ' + command + '\r\n')

        else:
            tolog('\r\nActual: ' + result.split('\r\n')[1] + ' && ' + result.split('\r\n')[2])

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)

    return FailFlag


def deleteVolume(c):
    FailFlag = False
    tolog('Verify to del volume \r\n')

    volumeId = []

    volumeInfo = SendCmd(c, 'volume')
    row = volumeInfo.split('\r\n')

    for i in range(4, len(row) - 2):
        if len(row[i].split()) >= 9:
            volumeId.append(row[i].split()[0])

    for i in volumeId:
        tolog('\r\nExpect: delete volume ' + i + '\r\n')

        result = SendCmd(c, 'volume -a del -y -f -i ' + i)

        if 'Error (' in result:
            FailFlag = True
            tolog('Fail: volume -a del -y -f -i ' + i + '\r\n')
        else:
            tolog('\r\nActual: volume ' + i + ' is deleted \r\n')

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)

    # clean up environment
    SendCmd(c, 'pool -a del -y -f -i 0')

    return FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    addVolume(c)
    listVolume(c)
    modVolume(c)
    exportVolume(c)
    unexportVolume(c)
    invaildName(c)
    invalidParameter(c)
    invalidOption(c)
    missingParameter(c)
    deleteVolume(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped