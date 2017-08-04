# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyHelp(c):
    FailFlag = False
    tolog("<b>Verify help </b>")
    result = SendCmd(c, 'help')
    command = ["about", "battery", "bbm", "bga", "buzz",  "chap", "clone", "ctrl", "date", "encldiag",
                "enclosure", "event", "export", "factorydefaul", "fc", "import", "initiator", "iscsi",
                "isns", "logout", "lunmap", "maintenance", "net", "ntp", "password", "pcie", "perfstats",
                "phydrv", "ping", "pool", "ptiflash", "rb", "rc", "rcache", "sc", "session", "shutdown",
                "smart", "snapshot", "spare", "stats", "subscription", "subsys", "swmgt", "sync",
                "topology", "trunk", "ups", "user", "volume", "wcache"]
    if 'Error (' in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: help </font>')
    for com in command:
        if com not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: help </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify help </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def bvt_verifyHelp(c):
    FailFlag = False
    tolog("Verify help")
    result = SendCmd(c, 'help')
    command = ["about", "battery", "bbm", "bga", "buzz",  "chap", "clone", "ctrl", "date", "encldiag",
                "enclosure", "event", "export", "factorydefaul", "fc", "import", "initiator", "iscsi",
                "isns", "logout", "lunmap", "maintenance", "net", "ntp", "password", "pcie", "perfstats",
                "phydrv", "ping", "pool", "ptiflash", "rb", "rc", "rcache", "sc", "session", "shutdown",
                "smart", "snapshot", "spare", "stats", "subscription", "subsys", "swmgt", "sync",
                "topology", "trunk", "ups", "user", "volume", "wcache"]
    if 'Error (' in result:
        FailFlag = True
        tolog('Fail: help ')
    for com in command:
        if com not in result:
            FailFlag = True
            tolog('Fail: help')

    return FailFlag

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyHelp(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped