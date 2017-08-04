# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyPtiflash(c):
    FailFlag = False
    tolog("<b>Verify ptiflash </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ptiflash </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPtiflashStart(c):
    FailFlag = False
    tolog("<b>Verify ptiflash -a start </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ptiflash -a start </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPtiflashVersioninfo(c):
    FailFlag = False
    tolog("<b>Verify ptiflash -a versioninfo </b>")
    # result = SendCmd(c, 'ptiflash -a versioninfo')
    # checkPoint = ['Firmware', 'Ctrl', 'Partition', 'Version', 'BuildDate', 'FlashDate', 'Firmware', '', '', '', '', '', '', '', ]


    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ptiflash -a versioninfo </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPtiflashSpecifyInexistentId(c):
    FailFlag = False
    tolog("<b> Verify ptiflash specify inexistent Id </b>")
    # -i <CtrlId> (1,2)
    # -e <encl id>
    # -d <device id> (1,512)

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ptiflash specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def verifyPtiflashInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify ptiflash invalid option</b>")
    command = ['ptiflash -x', 'ptiflash -a start -x', 'ptiflash -a versioninfo -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ptiflash invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyPtiflashInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify ptiflash invalid parameters</b>")
    command = ['ptiflash test', 'ptiflash -a start test', 'ptiflash -a versioninfo test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ptiflash invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyPtiflashMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify ptiflash missing parameters</b>")
    command = [ 'ptiflash -t ', 'ptiflash -t -s ', 'ptiflash -t -s 000.000.000.000 -f', 'ptiflash -a']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ptiflash missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyPtiflash(c)
    verifyPtiflashStart(c)
    verifyPtiflashVersioninfo(c)
    verifyPtiflashSpecifyInexistentId(c)
    verifyPtiflashInvalidOption(c)
    verifyPtiflashInvalidParameters(c)
    verifyPtiflashMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped