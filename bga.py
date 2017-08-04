# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
import random
import  re
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyBga(c):
    FailFlag = False
    tolog("<b>Verify bga</b>")
    result = SendCmd(c, 'bga')
    checkPoint = ['NumberOfRebuild:', 'RebuildRate:', 'NumberOfRC:', 'RCRate:', 'NumberOfSC:', 'NumberOfSync:']
    for cp in checkPoint:
        if cp not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: bga </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify bga</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBgaList(c):
    FailFlag = False
    tolog("<b>Verify bga -a list</b>")
    result = SendCmd(c, 'bga -a list')
    checkPoint = ['NumberOfRebuild:', 'RebuildRate:', 'NumberOfRC:', 'RCRate:', 'NumberOfSC:', 'NumberOfSync:']
    for cp in checkPoint:
        if cp not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: bga -a list</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify bga -a list</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBgaMod(c):
    FailFlag = False
    tolog("<b>Verify bga -a mod </b>")
    option = ['RebuildRate', 'RCRate']
    values = ['Low', 'High', 'Medium']
    for op in option:
        for v in values:
            setting = '"' + op + ' = ' + v + '"'
            result = SendCmd(c, 'bga -a mod -s ' + setting)
            checkResult = SendCmd(c, 'bga')
            if "Error (" in result or op + ': ' + v not in checkResult:
                FailFlag = True
                tolog('\n<font color="red">Fail: bga -a mod -s ' + setting + '</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify bga -a mod</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBgaHelp(c):
    FailFlag = False
    tolog("<b>Verify bga -h </b>")
    result = SendCmd(c, 'bga -h')
    if "Error (" in result or 'bga' not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: bga -h </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify bga -h </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBgaInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify bga invalid option</b>")
    command = ['bga -x', 'bga -a list -x', 'bga -a mod -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify bga invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBgaInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify bga invalid parameters</b>")
    command = ['bga test', 'bga -a test', 'bga -a mod -s test', 'bga -a mod -s "rebuildRate=test"', 'bga -a mod -s "RCRate=test"']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify bga invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBgaMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify bga missing parameters</b>")
    command = ['bga -a ', 'bga -a mod -s']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify bga missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def bvt_verifyBga(c):
    FailFlag = False
    tolog("Verify bga")
    result = SendCmd(c, 'bga')
    checkPoint = ['NumberOfRebuild:', 'RebuildRate:', 'NumberOfRC:', 'RCRate:', 'NumberOfSC:', 'NumberOfSync:']
    for cp in checkPoint:
        if cp not in result:
            FailFlag = True
            tolog('Fail: bga ')

    return FailFlag

def bvt_verifyBgaList(c):
    FailFlag = False
    tolog("Verify bga -a list")
    result = SendCmd(c, 'bga -a list')
    checkPoint = ['NumberOfRebuild:', 'RebuildRate:', 'NumberOfRC:', 'RCRate:', 'NumberOfSC:', 'NumberOfSync:']
    for cp in checkPoint:
        if cp not in result:
            FailFlag = True
            tolog('Fail: bga -a list')

    return FailFlag

def bvt_verifyBgaMod(c):
    FailFlag = False
    tolog("Verify bga -a mod ")
    option = ['RebuildRate', 'RCRate']
    values = ['Low', 'High', 'Medium']
    for op in option:
        for v in values:
            setting = '"' + op + ' = ' + v + '"'
            result = SendCmd(c, 'bga -a mod -s ' + setting)
            checkResult = SendCmd(c, 'bga')
            if "Error (" in result or op + ': ' + v not in checkResult:
                FailFlag = True
                tolog('Fail: bga -a mod -s ' + setting + '')

    return FailFlag

def bvt_verifyBgaHelp(c):
    FailFlag = False
    tolog("Verify bga -h ")
    result = SendCmd(c, 'bga -h')
    if "Error (" in result or 'bga' not in result:
        FailFlag = True
        tolog('Fail: bga -h ')

    return FailFlag

def bvt_verifyBgaInvalidOption(c):
    FailFlag = False
    tolog("Verify bga invalid option")
    command = ['bga -x', 'bga -a list -x', 'bga -a mod -x']
    for com in command:
        tolog(' Verify ' + com + '')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    return FailFlag

def bvt_verifyBgaInvalidParameters(c):
    FailFlag = False
    tolog("Verify bga invalid parameters")
    command = ['bga test', 'bga -a test', 'bga -a mod -s test', 'bga -a mod -s "rebuildRate=test"', 'bga -a mod -s "RCRate=test"']
    for com in command:
        tolog(' Verify ' + com + '')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    return FailFlag

def bvt_verifyBgaMissingParameters(c):
    FailFlag = False
    tolog("Verify bga missing parameters")
    command = ['bga -a ', 'bga -a mod -s']
    for com in command:
        tolog(' Verify ' + com + '')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    return FailFlag



if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    bvt_verifyBga(c)
    bvt_verifyBgaList(c)
    bvt_verifyBgaMod(c)
    bvt_verifyBgaHelp(c)
    bvt_verifyBgaInvalidOption(c)
    bvt_verifyBgaInvalidParameters(c)
    bvt_verifyBgaMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped