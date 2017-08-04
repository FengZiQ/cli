# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifySubscription(c):
    FailFlag = False
    tolog("<b>Verify subscription </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify subscription </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySubscriptionList(c):
    FailFlag = False
    tolog("<b>Verify subscription -a list </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify subscription -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySubscriptionMod(c):
    FailFlag = False
    tolog("<b>Verify subscription -a mod </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify subscription -a mod </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySubscriptionEnable(c):
    FailFlag = False
    tolog("<b>Verify subscription -a enable</b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify subscription -a enable </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySubscriptionDisable(c):
    FailFlag = False
    tolog("<b>Verify subscription -a disable </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify subscription -a disable </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifySubscriptionTest(c):
    FailFlag = False
    tolog("<b>Verify subscription -a test</b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify subscription -a test </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def verifySubscriptionInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify subscription invalid option</b>")
    command = ['subscription -x', 'subscription -a list -x', 'subscription -a mod -x',
               'subscription -a enable -x ', 'subscription -a disable -x', 'subscription -a test -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify subscription invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifySubscriptionInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify subscription invalid parameters</b>")
    command = ['subscription test', 'subscription -a list test', 'subscription -a mod test',
               'subscription -a enable test ', 'subscription -a disable test', 'subscription -a test test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify subscription invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifySubscriptionMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify subscription missing parameters</b>")
    command = ['subscription -a', 'subscription -a mod -u',
               'subscription -a mod -s', 'subscription -a list -v -t ', 'subscription -a test -u']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify subscription missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifySubscription(c)
    verifySubscriptionList(c)
    verifySubscriptionMod(c)
    verifySubscriptionEnable(c)
    verifySubscriptionDisable(c)
    verifySubscriptionTest(c)
    verifySubscriptionInvalidOption(c)
    verifySubscriptionInvalidParameters(c)
    verifySubscriptionMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped