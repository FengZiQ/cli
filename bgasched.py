# coding=utf-8

from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
from find_unconfigured_pd_id import find_pd_id
from remote import server
import json

Pass = "'result': 'p'"
Fail = "'result': 'f'"


def precondition():
    # create pool
    pdId = find_pd_id()
    if len(pdId) >= 6:
        server.webapi('post', 'pool', {"name": "testBgasched1", "pds": pdId[:3], "raid_level": "raid5"})
        server.webapi('post', 'pool', {"name": "testBgasched2", "pds": pdId[3:5], "raid_level": "raid1"})
        server.webapi('post', 'pool', {"name": "testBgasched3", "pds": [pdId[5:6]], "raid_level": "raid0"})


def clean_up_environment():

    bgaS_request = server.webapi('get', 'bgaschedule')

    bgaS_info = json.loads(bgaS_request['text'])

    for info in bgaS_info:

        server.webapi('delete', 'bgaschedule/' + str(info['id']))


def verifyBgaschedAdd(c):
    FailFlag = False

    # precondition
    precondition()

    poolId = ['0', '1', '2']
    type = ['rc', 'br', 'sc']
    # confirm information
    listType = ['Type: RedundancyCheck', 'Type: BatteryRecondition', 'Type: SpareCheck']
    defaultStatus = ['OperationalStatus: Disabled']
    defaultStartTime = ['StartTime: 22:00', 'StartTime: 02:00', 'StartTime: 22:00']
    startDay = SendCmd(c, 'date').split('\r\n')[-3].split()[-2]
    # recurtype = ['daily', 'weekly', 'monthly']

    # add bgasched of daily type
    tolog('add bgasched of daily type')
    for i in range(0, 3):
        if type[i] == 'rc':
            result = SendCmd(c, 'bgasched -a add -t ' + type[i] + ' -s "recurtype=daily,poolid=' + poolId[0] + '"'),\
                     SendCmd(c, 'bgasched -a add -t ' + type[i] + ' -s "recurtype=daily,poolid=' + poolId[1] + '"')
        else:
            result = SendCmd(c, 'bgasched -a add -t ' + type[i] + ' -s "recurtype=daily"')

        checkResult = SendCmd(c, 'bgasched -v -t ' + type[i])
        if 'Error (' in result or listType[i] not in checkResult or defaultStatus[0] not in checkResult or \
                        defaultStartTime[i] not in checkResult or 'Daily' not in checkResult or startDay not in checkResult:
            tolog('Fail: ' + 'bgasched -a add -t ' + type[i] + ' -s "recurtype=daily')
            FailFlag = True

    clean_up_environment()

    # pool of raid0 can not create rc bgasched
    result = SendCmd(c, 'bgasched -a add -t rc -s "recurtype=daily,poolid=2"')
    if 'Error (' not in result:
        FailFlag = True
        tolog('Fail: bgasched -a add -t rc -s "recurtype=daily,poolid=2"')

    clean_up_environment()

    # add bgasched of weekly type
    tolog('add bgasched of weekly type')
    for i in range(0, 3):
        if type[i] == 'rc':
            result = SendCmd(c, 'bgasched -a add -t ' + type[i] + ' -s "poolid=' + poolId[0] + '"'),\
                     SendCmd(c, 'bgasched -a add -t ' + type[i] + ' -s "poolid=' + poolId[1] + '"')
        else:
            result = SendCmd(c, 'bgasched -a add -t ' + type[i])

        checkResult = SendCmd(c, 'bgasched -v -t ' + type[i])
        if type[i] == 'br':
            if 'Error (' in result or listType[i] not in checkResult or defaultStatus[0] not in checkResult or \
                            defaultStartTime[i] not in checkResult or 'Monthly' not in checkResult or startDay not in checkResult:
                tolog('Fail: ' + 'bgasched -a add -t ' + type[i])
                FailFlag = True
        else:
            if 'Error (' in result or listType[i] not in checkResult or defaultStatus[0] not in checkResult or \
                            defaultStartTime[i] not in checkResult or 'Weekly' not in checkResult or startDay not in checkResult:
                tolog('Fail: ' + 'bgasched -a add -t ' + type[i])
                FailFlag = True

    clean_up_environment()

    # add bgasched of monthly type
    tolog('add bgasched of monthly type')
    for i in range(0, 3):
        if type[i] == 'rc':
            result = SendCmd(c, 'bgasched -a add -t ' + type[i] + ' -s "recurtype=monthly,poolid=' + poolId[0] + '"'), \
                     SendCmd(c, 'bgasched -a add -t ' + type[i] + ' -s "recurtype=monthly,poolid=' + poolId[1] + '"')
        else:
            result = SendCmd(c, 'bgasched -a add -t ' + type[i] + ' -s "recurtype=monthly"')

        checkResult = SendCmd(c, 'bgasched -v -t ' + type[i])
        if 'Error (' in result or listType[i] not in checkResult or defaultStatus[0] not in checkResult or \
                        defaultStartTime[i] not in checkResult or 'Monthly' not in checkResult or startDay not in checkResult:
            tolog('Fail: ' + 'bgasched -a add -t ' + type[i] + ' -s "recurtype=monthly')
            FailFlag = True

    clean_up_environment()

    if FailFlag:
        tolog('\n<font color="red">Fail: To verify add bgasched </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag


def verifyBgaschedMod(c):
    FailFlag = False
    type = ['rc', 'br', 'sc']
    recurtype = ['daily', 'weekly', 'monthly']
    # precondition
    for i in range(0, 3):
        if 'Error (' in SendCmd(c, 'bgasched -a add -t ' + type[i] + ' -s "recurtype=' + recurtype[i] + '"'):
            tolog('to create precondition is failed')
            exit()

    # setting by type of type
    globalSettings = [
        # status
        ['Disable', 'Disable', 'Enable', 'Enable'],
        # startTime
        ['00:00', '06:10', '12:20', '23:59'],
        # startFrom : year value range 1970~2037
        ['1970-01-01', '2037-12-31', '2000-01-01', '2000-01-01'],
        # endOn
        ['1', '255', '1970-01-01', '2037-12-31'],
        # autoFix
        ['Enable', 'Enable', 'Disable', 'Disable'],
        # pause
        ['Enable', 'Enable', 'Disable', 'Disable']
    ]
    for t in type:
        tolog('verify: bgasched -a mod -t ' + t)

        for i in range(0, 4):
            # setting autoFix and pause for rc
            result = SendCmd(c, 'bgasched -a mod -t rc -s "autofix='
                             + globalSettings[4][i] + ',pause='
                             + globalSettings[5][i] + '"')
            checkResult = SendCmd(c, 'bgasched -v -t rc')
            if 'Error (' in result or ('AutoFix: '
                             + globalSettings[4][i]) not in checkResult or ('PauseOnError: '
                             + globalSettings[5][i]) not in checkResult:
                FailFlag = True
                tolog('Fail: ' + 'bgasched -a mod -t rc -s "autofix='
                             + globalSettings[4][i] + ',pause='
                             + globalSettings[5][i] + '"')

            # setting status/startTime/startDay/endOn for all type
            result = SendCmd(c, 'bgasched -a mod -t ' + t + ' -s "status='
                             + globalSettings[0][i] + ',starttime='
                             + globalSettings[1][i] + ',startfrom='
                             + globalSettings[2][i] + ',endon='
                             + globalSettings[3][i] + '"')
            checkResult = SendCmd(c, 'bgasched -v -t ' + t)
            if 'Error (' in result or ('OperationalStatus: '
                        + globalSettings[0][i]) not in checkResult or ('StartTime: '
                        + globalSettings[1][i]) not in checkResult or ('StartDay: '
                        + globalSettings[2][i]) not in checkResult or (''
                        + globalSettings[3][i][:4]) not in checkResult:
                FailFlag = True
                tolog('Fail: ' + 'bgasched -a mod -t ' + t + ' -s "status='
                             + globalSettings[0][i] + ',starttime='
                             + globalSettings[1][i] + ',startfrom='
                             + globalSettings[2][i] + ',endon='
                             + globalSettings[3][i] + '"')

    # Setting the parameters associated with recurType of daily
    tolog('Setting the parameters associated with recurType of daily')
    dailySettings = ['1', '2', '254', '255']

    for ds in dailySettings:
        result = SendCmd(c, 'bgasched -a mod -t rc -s "recurInterval=' + ds + '"')
        checkResult = SendCmd(c, 'bgasched -v -t rc')
        if "Error (" in result or ('RecurrenceInterval: ' + ds) not in checkResult:
            FailFlag = True
            tolog('Fail: ' + 'bgasched -a mod -t rc -s "recurInterval=' + ds + '"')

    # Setting the parameters associated with recurType of weekly
    tolog('Setting the parameters associated with recurType of weekly')
    weeklySettings = [
        # recurInterval
        ['1', '2', '51', '52', '52', '52', '52'],
        # dow
        ['Sun', 'Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat']
    ]

    for i in range(0, 7):
        result = SendCmd(c, 'bgasched -a mod -t br -s "recurInterval='
                         + weeklySettings[0][i] + ',dow='
                         + weeklySettings[1][i] + '"')
        checkResult = SendCmd(c, 'bgasched -v -t br')
        if 'Error (' in result or ('RecurrenceInterval: '
                         + weeklySettings[0][i]) not in checkResult or ('DayOfWeek: '
                         + weeklySettings[1][i]) not in checkResult:
            FailFlag = True
            tolog('Fail: '
                         + 'bgasched -a mod -t br -s "recurInterval='
                         + weeklySettings[0][i] + ',dow='
                         + weeklySettings[1][i] + '"')

    # Setting the parameters associated with recurType of monthly
    tolog('Setting the parameters associated with recurType of monthly')
    monthlySettings = [
        # dom
        ['1', '2', '30', '31'],
        # dow
        ['Sun', 'Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat'],
        # wom
        ['1st', '2nd', '3rd', '4th', 'Last', 'Last', 'Last']
    ]

    for i in range(0, len(monthlySettings[0])):
        result = SendCmd(c, 'bgasched -a mod -t sc -s "daypattern=dom,dom=' + monthlySettings[0][i] + '"')
        checkResult = SendCmd(c, 'bgasched -v -t sc')
        if "Error (" in result or ('DayOfMonth: ' + monthlySettings[0][i]) not in checkResult:
            FailFlag = True
            tolog('Fail: ' + 'bgasched -a mod -t sc -s "daypattern=dom,dom=' + monthlySettings[0][i] + '"')

    for i in range(0, len(monthlySettings[1])):
        result = SendCmd(c, 'bgasched -a mod -t sc -s "daypattern=dow,dow='
                         + monthlySettings[1][i] + ',wom='
                         + monthlySettings[2][i] + '"')
        checkResult = SendCmd(c, 'bgasched -v -t sc')
        if 'Error (' in result or ('DayOfMonth: ' + monthlySettings[2][i] + ' ' + monthlySettings[1][i]) not in checkResult:
            FailFlag = True
            tolog('Fail: ' + 'bgasched -a mod -t sc -s "daypattern=dow,dow='
                         + monthlySettings[1][i] + ',wom='
                         + monthlySettings[2][i] + '"')

    if FailFlag:
        tolog('\n<font color="red">Fail: To verify modify bgasched </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag


def verifyBgaschedList(c):
    FailFlag = False
    command = ['bgasched',
               'bgasched -v',
               'bgasched -v -t br',
               'bgasched -v -t rc',
               'bgasched -v -t sc'
               ]

    for com in command:
        tolog('verify: ' + com)
        result = SendCmd(c, com)
        if 'Error (' in result:
            FailFlag = True
            tolog("Fail: " + com)

    if FailFlag:
        tolog('\n<font color="red">Fail: To verify list bgasched </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag


def verifyBgaschedDel(c):
    FailFlag = False

    result = SendCmd(c, 'bgasched -a del -t br -i 1')
    if 'Error (' in result:
        FailFlag = True
        tolog('Fail: ' + 'bgasched -a del -t br -i 1')

    result = SendCmd(c, 'bgasched -a del -t sc -i 1')
    if 'Error (' in result:
        FailFlag = True
        tolog('Fail: ' + 'bgasched -a del -t sc -i 1')

    result = SendCmd(c, 'bgasched -a del -t rc -i 1')
    if 'Error (' in result:
        FailFlag = True
        tolog('Fail: ' + 'bgasched -a del -t rc -i 1')

    if FailFlag:
        tolog('\n<font color="red">Fail: To verify delete bgasched </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag


def verifyBgaschedHelp(c):
    FailFlag = False
    result = SendCmd(c, 'bgasched -h')
    if 'Error (' in result or '<action>' not in result:
        FailFlag = True
        tolog('Fail: bgasched -h')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify Bgasched help </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag


def verifyBgaschedInvalidOption(c):
    FailFlag = False
    command = ['bgasched -x',
               'bgasched -a list -x',
               'bgasched -a mod -x',
               'bgasched -a del -x'
               ]
    for com in command:
        result = SendCmd(c, com)
        if 'Error (' not in result or 'Invalid option' not in result:
            FailFlag = True
            tolog('Fail: ' + com)

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify Bgasched invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag


def verifyBgaschedInvalidParameters(c):
    FailFlag = False
    command = ['bgasched -t x',
               'bgasched -a mod -t x',
               'bgasched -a add -t sc -s "status=x"',
               'bgasched -a add -t sc -s "recurtype=x"',
               # startTime range is 0-23
               'bgasched -a add -t sc -s "starttime=-1"',
               'bgasched -a add -t sc -s "starttime=24"',
               # recurInterval For Daily type, the range is 1-255
               'bgasched -a add -t sc -s "recurtype=daily,recurInterval=0"',
               'bgasched -a add -t sc -s "recurtype=daily,recurInterval=256"',
               # recurInterval For weekly type, the range is 1-52
               'bgasched -a add -t sc -s "recurtype=weekly,recurInterval=0"',
               'bgasched -a add -t sc -s "recurtype=weekly,recurInterval=53"',
               # dom The range is 1~31
               'bgasched -a add -t sc -s "daypattern=dom,dom=0"',
               'bgasched -a add -t sc -s "daypattern=dom,dom=32"',
               'bgasched -a add -t sc -s "daypattern=dow,wom=x"',
               # mm/dd/yyyy where month's range is 1-12, day's range is 1-31, year value range 1970~2037
               'bgasched -a add -t sc -s "startfrom=2017-0-1"',
               'bgasched -a add -t sc -s "startfrom=2017-13-1"',
               'bgasched -a add -t sc -s "startfrom=2017-1-0"',
               'bgasched -a add -t sc -s "startfrom=2017-1-32"',
               'bgasched -a add -t sc -s "startfrom=3038-1-1"',
               # endOn range is 0-255,month's range is 1-12 and day's range is 1-31
               'bgasched -a add -t sc -s "endon=-1"',
               'bgasched -a add -t sc -s "endon=256"',
               'bgasched -a add -t sc -s "endon=2017-0-1"',
               'bgasched -a add -t sc -s "endon=2017-13-1"',
               'bgasched -a add -t sc -s "endon=2017-1-0"',
               'bgasched -a add -t sc -s "endon=2017-32-1"',
               'bgasched -a add -t rc -s "autofix=x"',
               'bgasched -a add -t rc -s "pause=x"',
               'bgasched -a del -t x'
               ]
    for com in command:
        result = SendCmd(c,com)
        if "Error (" not in result or 'Invalid setting parameters' not in result:
            FailFlag = True
            tolog('Fail: ' + com)

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify Bgasched invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag


def verifyBgaschedMissingParameters(c):
    FailFlag = False
    command = ['bgasched -t ',
               'bgasched -a mod -t rc -s',
               'bgasched -a del -t'
               ]
    for com in command:
        result = SendCmd(c, com)
        if 'Error (' not in result or 'Missing parameter' not in result:
            FailFlag = True
            tolog("Fail: " + com)

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify Bgasched missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    # clean up environment
    clean_up_environment()
    find_pd_id()

    return FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    verifyBgaschedAdd(c)
    verifyBgaschedMod(c)
    verifyBgaschedList(c)
    verifyBgaschedDel(c)
    verifyBgaschedHelp(c)
    verifyBgaschedInvalidOption(c)
    verifyBgaschedInvalidParameters(c)
    verifyBgaschedMissingParameters(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped