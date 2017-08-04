# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
from to_log import tolog
import paramiko
import time
import paramiko
import time
import random
import string
Pass = "'result': 'p'"
Fail = "'result': 'f'"
def chapSend_cmd(c, cmdstr,password):
    data = ''
    if cmdstr.endswith('\n'):
        c.send(cmdstr)
    else:
        c.send(cmdstr + '\n')
    while not c.exit_status_ready():
        if c.recv_ready():
            data += c.recv(2000)
            # add code for password in chap
            # data=data.replace("[32D[32C[0m[?12l[?25h","").replace("[?1l[6n[?2004h[?25l[?7l[0m[0m[J[0m","")
        while data.endswith('?25h'):

            c.send(password + "\n")
            data += c.recv(2000)
            if data.endswith('@cli> '):
                break
        if data.endswith('@cli> '):
            break
    # removig the following chars to avoid
    # <Fault -32700: 'parse error. not well formed'> when
    # updating to testlink
    while c.recv_ready():
        data += c.recv(2000)
        # print data
        if data.endswith('@cli> '):
            break
            # if data.endswith('?25h'):
            #     c.send("Local#123"+"\n")
    # data += c.recv(9999)
    data = data.replace("\x1b[D \x1b[D", "")
    data = data.replace("[?1l[6n[?2004h[?25l[?7l[0m[0m[J[0m", "").replace("[32D[32C[0m[?12l[?25h",
                                                                                   "").replace(
        "[?7h[0m[?12l[?25h[?2004l[?1l[6n[?2004h[?25l[?7l[0m[0m[J[0m", "")
    tolog(data)

    return data

def findChapId(c):
    result = SendCmd(c, 'chap')
    num = 2
    ChapId = []
    if 'CHAP record not found' not in result:
        while result.split("\r\n")[num] != 'administrator@cli> ':
            row = result.split("\r\n")[num]
            if 'ChapId' in row:
                ChapId.append(row.split()[1])
            num = num + 1
    return ChapId

def precondition(c):
    tolog("<b>Verify precondition</b>")
    ChapId = findChapId(c)
    for i in ChapId:
        result = SendCmd(c, 'chap -a del -i ' + i)
        if 'Error (' in result:
            tolog('\n<font color="red">Fail: precondition </font>')

def verifyChapAdd(c):
    precondition(c)
    FailFlag = False
    tolog("<b>Verify chap -a add</b>")
    tolog("<b>Verify CHAP legal name and type </b>")
    result = chapSend_cmd(c, 'chap -a add -s "name=a+-/(.)b,type=peer"', '111122221111')
    c.close()
    time.sleep(3)
    c, ssh = ssh_conn()
    if 'Error (' in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: chap -a add -s "name=a+-/(.)b,type=peer" </font>')

    result = chapSend_cmd(c, 'chap -a add -s "name=testType,type=local,targetid=0"', '1111222211112222')
    c.close()
    ssh.close()
    time.sleep(3)
    c, ssh = ssh_conn()
    if 'Error (' in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: chap -a add -s "name=a+-/(.)b,type=peer" </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify chap -a add</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
    c.close()
    ssh.close()
    time.sleep(3)

def verifyChap(c):
    FailFlag = False
    tolog("<b>Verify chap </b>")
    c, ssh = ssh_conn()
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
    c.close()
    ssh.close()
    time.sleep(3)

def verifyChapList(c):
    FailFlag = False
    tolog("<b>Verify chap -a list</b>")
    c, ssh = ssh_conn()
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
    c.close()
    ssh.close()
    time.sleep(3)

def verifyChapMod(c):
    FailFlag = False
    tolog("<b>Verify chap -a mod</b>")
    c, ssh = ssh_conn()
    chapId = findChapId(c)
    if len(chapId) != 0:
        result = chapSend_cmd(c, 'chap -a mod -s "name=testModifyName" -i 0', '111122221111')
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
    c.close()
    ssh.close()
    time.sleep(3)

def verifyChapDel(c):
    FailFlag = False
    tolog("<b>Verify chap -a del</b>")
    c, ssh = ssh_conn()
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
    c.close()
    ssh.close()
    time.sleep(3)

def verifyChapHelp(c):
    FailFlag = False
    tolog("<b> Verify chap -h </b>")
    c, ssh = ssh_conn()
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
    c.close()
    ssh.close()
    time.sleep(3)

def verifyChapSpecifyErrorId(c):
    FailFlag = False
    tolog("<b> Verify chap specify error Id </b>")
    c, ssh = ssh_conn()
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
    c.close()
    ssh.close()
    time.sleep(3)

def verifyChapInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify chap invalid option</b>")
    c, ssh = ssh_conn()
    command = ['chap -x', 'chap -a list -x', 'chap -a add -x', 'chap -a mod -x', 'chap -a del -x']
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
    c.close()
    ssh.close()
    time.sleep(3)

def verifyChapInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify chap invalid parameters</b>")
    c, ssh = ssh_conn()
    command = ['chap test', 'chap -a test', 'chap -a add -s test', 'chap -a mod -i test', 'chap -a del -i test']
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
    c.close()
    ssh.close()
    time.sleep(3)

def verifyChapMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify chap missing parameters</b>")
    c, ssh = ssh_conn()
    command = ['chap -i', 'chap -a list -i ', 'chap -a add -s ', 'chap -a mod -i', 'chap -a del -i']
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


def bvt_verifyChapAdd(c):
    precondition(c)
    FailFlag = False
    tolog("<b>Verify chap -a add</b>")
    tolog("<b>Verify CHAP legal name and type </b>")
    result = chapSend_cmd(c, 'chap -a add -s "name=a+-/(.)b,type=peer"', '111122221111')
    c.close()
    ssh.close()
    time.sleep(3)
    c, ssh = ssh_conn()
    if 'Error (' in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: chap -a add -s "name=a+-/(.)b,type=peer" </font>')

    result = chapSend_cmd(c, 'chap -a add -s "name=testType,type=local,targetid=0"', '1111222211112222')
    c.close()
    ssh.close()
    time.sleep(3)
    c, ssh = ssh_conn()
    if 'Error (' in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: chap -a add -s "name=a+-/(.)b,type=peer" </font>')

    c.close()
    ssh.close()
    time.sleep(3)

    return FailFlag

def bvt_verifyChap(c):
    FailFlag = False
    tolog("<b>Verify chap </b>")
    c, ssh = ssh_conn()
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

    c.close()
    ssh.close()
    time.sleep(3)

    return FailFlag

def bvt_verifyChapList(c):
    FailFlag = False
    tolog("<b>Verify chap -a list</b>")
    c, ssh = ssh_conn()
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

    # c.close()
    # ssh.close()
    time.sleep(3)

    return FailFlag

def bvt_verifyChapMod(c):
    FailFlag = False
    tolog("<b>Verify chap -a mod</b>")
    c, ssh = ssh_conn()
    chapId = findChapId(c)
    if len(chapId) != 0:
        result = chapSend_cmd(c, 'chap -a mod -s "name=testModifyName" -i 0', '111122221111')
        c.close()
        c,ssh = ssh_conn()
        checkResult = SendCmd(c, 'chap')
        if "Error (" in result or 'testModifyName' not in checkResult:
            FailFlag = True
            tolog('\n<font color="red">Fail: chap -a mod -s "name=testModifyName" -i 0</font>')
    else:
        tolog('\n<font color="red">Fail: CHAP record not found </font>')

    c.close()
    ssh.close()
    time.sleep(3)

    return FailFlag

def bvt_verifyChapDel(c):
    FailFlag = False
    tolog("<b>Verify chap -a del</b>")
    c, ssh = ssh_conn()
    ChapId = findChapId(c)
    for i in ChapId:
        result = SendCmd(c, 'chap -a del -i ' + i)
        if 'Error (' in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: chap -a del -i ' + i + '</font>')

    c.close()
    ssh.close()
    time.sleep(3)

    return FailFlag

def bvt_verifyChapHelp(c):
    FailFlag = False
    tolog("<b> Verify chap -h </b>")
    c, ssh = ssh_conn()
    result = SendCmd(c, 'chap -h')
    if "Error (" in result or 'chap' not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: chap -h </font>')

    c.close()
    ssh.close()
    time.sleep(3)

    return FailFlag

def bvt_verifyChapSpecifyErrorId(c):
    FailFlag = False
    tolog("<b> Verify chap specify error Id </b>")
    c, ssh = ssh_conn()
    result = SendCmd(c, 'chap -a del -i 4')
    if 'Error (' not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: chap -a del -i 4 </font>')

    c.close()
    ssh.close()
    time.sleep(3)

    return FailFlag

def bvt_verifyChapInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify chap invalid option</b>")
    c, ssh = ssh_conn()
    command = ['chap -x', 'chap -a list -x', 'chap -a add -x', 'chap -a mod -x', 'chap -a del -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')

    c.close()
    ssh.close()
    time.sleep(3)

    return FailFlag

def bvt_verifyChapInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify chap invalid parameters</b>")
    c, ssh = ssh_conn()
    command = ['chap test', 'chap -a test', 'chap -a add -s test', 'chap -a mod -i test', 'chap -a del -i test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')

    c.close()
    ssh.close()
    time.sleep(3)

    return FailFlag

def bvt_verifyChapMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify chap missing parameters</b>")
    c, ssh = ssh_conn()
    command = ['chap -i', 'chap -a list -i ', 'chap -a add -s ', 'chap -a mod -i', 'chap -a del -i']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')

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