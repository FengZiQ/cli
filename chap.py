# coding=utf-8

from send_cmd import *
from ssh_connect import ssh_conn
from to_log import tolog
import time

Pass = "'result': 'p'"
Fail = "'result': 'f'"

def findChapId(c):
    ChapInfo = SendCmd(c, "chap")
    ChapId = []
    row = ChapInfo.split('ChapId: ')
    for i in range(1, len(row)):
        print "wait to complete"

    return ChapId

def verifyChapAdd(c):
    FailFlag = False
    tolog("<b>Verify chap -a add</b>")
    tolog("<b>Verify CHAP legal name and type </b>")

    result = SendCmdpassword(c, 'chap -a add -s "name=a+-/(.)b,type=peer"', '111122221111')

    if 'Error (' in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: chap -a add -s "name=a+-/(.)b,type=peer" </font>')

    result = SendCmdpassword(c, 'chap -a add -s "name=testType,type=local,targetid=0"', '1111222211112222')

    if 'Error (' in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: chap -a add -s "name=a+-/(.)b,type=peer" </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify chap -a add</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyChap(c):
    FailFlag = False
    tolog("<b>Verify chap </b>")

    chapId = findChapId(c)

    if len(chapId) != 0:
        result = SendCmd(c, 'chap')

        if "Error (" in result or 'ChapId:' not in result or 'Name:' not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: chap </font>')

        tolog('<b>Verify chap -i chap id</b>')

        for i in chapId:
            result = SendCmd(c, 'chap -i ' + i)

            if 'ChapId:' not in result or 'Name:' not in result or i not in result:
                FailFlag = True
                tolog('\n<font color="red">Fail: chap -i ' + i + '</font>')
    else:
        result = SendCmd(c, 'chap')
        if 'CHAP record not found' not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: chap </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify chap </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyChapList(c):
    FailFlag = False
    tolog("<b>Verify chap -a list</b>")

    chapId = findChapId(c)

    if len(chapId) != 0:
        result = SendCmd(c, 'chap -a list')

        if "Error (" in result or 'ChapId:' not in result or 'Name:' not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: chap -a list</font>')

        tolog('<b>Verify chap -a list -i chap id</b>')

        for i in chapId:
            result = SendCmd(c, 'chap -a list -i ' + i)

            if 'ChapId:' not in result or 'Name:' not in result or i not in result:
                FailFlag = True
                tolog('\n<font color="red">Fail: chap -a list -i ' + i + '</font>')
    else:
        result = SendCmd(c, 'chap -a list')

        if 'CHAP record not found' not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: chap -a list</font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify chap -a list</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyChapMod(c):
    FailFlag = False
    tolog("<b>Verify chap -a mod</b>")

    chapId = findChapId(c)

    if len(chapId) != 0:
        result = SendCmdpassword(c, 'chap -a mod -s "name=testModifyName" -i 0', '111122221111')
        c.close()
        c,ssh = ssh_conn()
        checkResult = SendCmd(c, 'chap')

        if "Error (" in result or 'testModifyName' not in checkResult:
            FailFlag = True
            tolog('\n<font color="red">Fail: chap -a mod -s "name=testModifyName" -i 0</font>')
    else:
        tolog('\n<font color="red">Fail: CHAP record not found </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify chap -a mod</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyChapDel(c):
    FailFlag = False
    tolog("<b>Verify chap -a del</b>")

    ChapId = findChapId(c)
    for i in ChapId:
        result = SendCmd(c, 'chap -a del -i ' + i)
        if 'Error (' in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: chap -a del -i ' + i + '</font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify chap -a del</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyChapHelp(c):
    FailFlag = False
    tolog("<b> Verify chap -h </b>")

    result = SendCmd(c, 'chap -h')

    if "Error (" in result or 'chap' not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: chap -h </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify chap -h </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyChapSpecifyErrorId(c):
    FailFlag = False
    tolog("<b> Verify chap specify error Id </b>")

    result = SendCmd(c, 'chap -a del -i 4')

    if 'Error (' not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: chap -a del -i 4 </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify chap specify error Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyChapInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify chap invalid option</b>")

    command = [
        'chap -x',
        'chap -a list -x',
        'chap -a add -x',
        'chap -a mod -x',
        'chap -a del -x'
    ]

    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)

        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify chap invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyChapInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify chap invalid parameters</b>")

    command = [
        'chap test',
        'chap -a test',
        'chap -a add -s test',
        'chap -a mod -i test',
        'chap -a del -i test'
    ]

    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)

        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify chap invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyChapMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify chap missing parameters</b>")

    command = [
        'chap -i',
        'chap -a list -i ',
        'chap -a add -s ',
        'chap -a mod -i',
        'chap -a del -i'
    ]

    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)

        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify chap missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyChapAdd(c)
    verifyChap(c)
    verifyChapList(c)
    verifyChapMod(c)
    verifyChapDel(c)
    verifyChapHelp(c)
    verifyChapSpecifyErrorId(c)
    verifyChapInvalidOption(c)
    verifyChapInvalidParameters(c)
    verifyChapMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped