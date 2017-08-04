# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyDate(c):
    FailFlag = False
    tolog("<b>Verify date </b>")
    result = SendCmd(c, 'date')
    if 'Error (' in result or 'SystemDate:' not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: date </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify date </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyDateList(c):
    FailFlag = False
    tolog("<b>Verify date -a list </b>")
    result = SendCmd(c, 'date -a list')
    if 'Error (' in result or 'SystemDate:' not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: date -a list </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify date -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyDateMod(c):
    FailFlag = False
    tolog("<b>Verify date -a mod </b>")
    # yyyy/mm/dd where month's range is 1-12 and day's range is 1-31.
    # hh:mm:ss where hour's range is 0-23, minute's and seconds'range are 0-59
    SendCmd(c, 'date -a mod -d 2018/01/01 -t 08:08:08')
    c, ssh = ssh_conn()
    time.sleep(10)
    checkResult = SendCmd(c, 'date')
    if '2018-01-01' not in checkResult or '08:08:' not in checkResult:
        FailFlag = True
        tolog('\n<font color="red">Fail: date -a mod -d 2018/01/01 -t 08:08:08 </font>')

    d = time.strftime('%Y/%m/%d', time.localtime(time.time()))
    t = time.strftime('%H:%M:%S', time.localtime(time.time()))
    SendCmd(c, 'date -a mod -d ' + d + ' -t ' + t)
    # c, ssh = ssh_conn()
    # time.sleep(10)
    checkResult = SendCmd(c, 'date')
    if d.split('/')[0] + '-' + d.split('/')[1] + '-' + d.split('/')[2] not in checkResult or t not in checkResult:
        FailFlag = True
        tolog('\n<font color="red">Fail: date -a mod -d ' + d + ' -t ' + t + ' </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify date -a mod </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyDateHelp(c):
    FailFlag = False
    tolog("<b>Verify date -h </b>")
    c, ssh = ssh_conn()
    result = SendCmd(c, 'date -h')
    if 'Error (' in result or 'date' not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: date -h </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify date -h </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyDateInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify date invalid option</b>")
    c, ssh = ssh_conn()
    command = ['date -x', 'date -a list -x', 'date -a mod -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify date invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyDateInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify date invalid parameters</b>")
    c, ssh = ssh_conn()
    command = ['date test', 'date -a test', 'date -a mod -d 2017/13/30', 'date -a mod -d 2017/05/33',
               'date -a mod -t 24:00:00', 'date -a mod -t 00:61:00', 'date -a mod -t 00:00:61']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify date invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyDateMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify date missing parameters</b>")
    c, ssh = ssh_conn()
    command = ['date -a mod -d', 'date -a mod -t']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify date missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def bvt_verifyDate(c):
    FailFlag = False
    tolog("Verify date ")
    c, ssh = ssh_conn()
    result = SendCmd(c, 'date')
    if 'Error (' in result or 'SystemDate:' not in result:
        FailFlag = True
        tolog('Fail: date ')

    return FailFlag

def bvt_verifyDateList(c):
    FailFlag = False
    tolog("Verify date -a list ")
    c, ssh = ssh_conn()
    result = SendCmd(c, 'date -a list')
    if 'Error (' in result or 'SystemDate:' not in result:
        FailFlag = True
        tolog('Fail: date -a list ')

    return FailFlag

def bvt_verifyDateMod(c):
    FailFlag = False
    tolog("Verify date -a mod ")
    # yyyy/mm/dd where month's range is 1-12 and day's range is 1-31.
    # hh:mm:ss where hour's range is 0-23, minute's and seconds'range are 0-59
    SendCmd(c, 'date -a mod -d 2018/01/01 -t 08:08:08')
    c, ssh = ssh_conn()
    time.sleep(10)
    checkResult = SendCmd(c, 'date')
    if '2018-01-01' not in checkResult or '08:08:' not in checkResult:
        FailFlag = True
        tolog('Fail: date -a mod -d 2018/01/01 -t 08:08:08 ')

    d = time.strftime('%Y/%m/%d', time.localtime(time.time()))
    t = time.strftime('%H:%M:%S', time.localtime(time.time()))
    SendCmd(c, 'date -a mod -d ' + d + ' -t ' + t)
    # c, ssh = ssh_conn()
    # time.sleep(10)
    checkResult = SendCmd(c, 'date')
    if d.split('/')[0] + '-' + d.split('/')[1] + '-' + d.split('/')[2] not in checkResult or t not in checkResult:
        FailFlag = True
        tolog('Fail: date -a mod -d ' + d + ' -t ' + t + ' ')

    return FailFlag

def bvt_verifyDateHelp(c):
    FailFlag = False
    tolog("Verify date -h ")
    c, ssh = ssh_conn()
    result = SendCmd(c, 'date -h')
    if 'Error (' in result or 'date' not in result:
        FailFlag = True
        tolog('Fail: date -h ')

    return FailFlag

def bvt_verifyDateInvalidOption(c):
    FailFlag = False
    tolog("Verify date invalid option")
    c, ssh = ssh_conn()
    command = ['date -x', 'date -a list -x', 'date -a mod -x']
    for com in command:
        tolog(' Verify ' + com + '')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    return FailFlag

def bvt_verifyDateInvalidParameters(c):
    FailFlag = False
    tolog("Verify date invalid parameters")

    command = ['date test', 'date -a test', 'date -a mod -d 2017/13/30', 'date -a mod -d 2017/05/33',
               'date -a mod -t 24:00:00', 'date -a mod -t 00:61:00', 'date -a mod -t 00:00:61']

    for com in command:
        tolog(' Verify ' + com + '')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    return FailFlag

def bvt_verifyDateMissingParameters(c):
    FailFlag = False
    tolog("Verify date missing parameters")
    command = ['date -a mod -d', 'date -a mod -t']

    for com in command:
        tolog(' Verify: ' + com + '')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    return FailFlag



if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    bvt_verifyDate(c)
    bvt_verifyDateList(c)
    bvt_verifyDateMod(c)
    bvt_verifyDateHelp(c)
    bvt_verifyDateInvalidOption(c)
    verifyDateInvalidParameters(c)
    bvt_verifyDateMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped