# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyPhydrv(c):
    FailFlag = False
    tolog("<b>Verify phydrv </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify phydrv </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPhydrvList(c):
    FailFlag = False
    tolog("<b>Verify phydrv -a list </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify phydrv -a list</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPhydrvMod(c):
    FailFlag = False
    tolog("<b>Verify phydrv -a mod </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify phydrv -a mod </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPhydrvLocate(c):
    FailFlag = False
    tolog("<b>Verify phydrv -a locate</b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify phydrv -a locate </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPhydrvOnline(c):
    FailFlag = False
    tolog("<b>Verify phydrv -a online</b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify phydrv -a online </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPhydrvOffline(c):
    FailFlag = False
    tolog("<b>Verify phydrv -a offline</b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify phydrv -a offline </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPhydrvClear(c):
    FailFlag = False
    tolog("<b>Verify phydrv -a clear</b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify phydrv -a clear </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPhydrvSpecifyInexistentId(c):
    FailFlag = False
    tolog("<b> Verify phydrv specify inexistent Id </b>")
    # -p <PD ID> (1,512)

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify phydrv specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def verifyPhydrvInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify phydrv invalid option</b>")
    command = ['phydrv -x', 'phydrv -a list -x', 'phydrv -a mod -x', 'phydrv -a locate -x',
               'phydrv -a online -x', 'phydrv -a offline -x', 'phydrv -a clear -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify phydrv invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyPhydrvInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify phydrv invalid parameters</b>")
    command = ['phydrv test', 'phydrv -a list test', 'phydrv -a mod test', 'phydrv -a locate test',
               'phydrv -a online test', 'phydrv -a offline test', 'phydrv -a clear test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify phydrv invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyPhydrvMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify phydrv missing parameters</b>")
    command = ['phydrv -p', 'phydrv -a list -p', 'phydrv -a mod -s', 'phydrv -a locate -p', 'phydrv -a online -p', 'phydrv -a offline -p']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify phydrv missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyPhydrv(c)
    verifyPhydrvList(c)
    verifyPhydrvMod(c)
    verifyPhydrvLocate(c)
    verifyPhydrvOnline(c)
    verifyPhydrvOffline(c)
    verifyPhydrvClear(c)
    verifyPhydrvSpecifyInexistentId(c)
    verifyPhydrvInvalidOption(c)
    verifyPhydrvInvalidParameters(c)
    verifyPhydrvMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped