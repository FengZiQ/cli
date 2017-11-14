# coding = utf-8
# 2017.11.14

from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
from remote import *
import json
import random

Pass = "'result': 'p'"
Fail = "'result': 'f'"


def list_tz(c):

    FailFlag = False

    tolog('timezone should be listed\r\n')
    result = SendCmd(c, 'tz')

    checkpoint = ['Time Offset', 'Zone', 'Support DST']

    if 'Error (' in result:

        FailFlag = True
        tolog('\r\nFail: tz\r\n')

    else:

        for check in checkpoint:
            if check not in result:
                FailFlag = True
                tolog('Fail: please check out ' + check + '\r\n')

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)

    return FailFlag


def list_tz_detail(c):
    FailFlag = False

    tolog('detail of timezone should be listed\r\n')
    result = SendCmd(c, 'tz -d')

    checkpoint = ['Time Offset', 'Zone', 'Support DST']

    if 'Error (' in result:

        FailFlag = True
        tolog('\r\nFail: tz\r\n')

    else:

        for check in checkpoint:
            if check not in result:
                FailFlag = True
                tolog('Fail: please check out ' + check + '\r\n')

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)

    return FailFlag


def mod_tz(c):

    FailFlag = False

    # precondition
    tz_request = server.webapi('get', 'alltz')
    tz_response = json.loads(tz_request["text"])

    # test data
    tz_dist = {}

    for tz in tz_response:
        tz_dist.update({tz["zone"].split('/')[1]: tz["dst"]})

    test_tz = [random.choice(tz_dist.keys()) for i in range(10)]

    for t in range(len(test_tz)):

        tolog('modify timezone to ' + test_tz[t] + '\r\n')
        result = SendCmd(c, 'tz -a mod -s "zone=' + test_tz[t] + '"')

        if 'Error (' in result:

            FailFlag = True
            tolog('Fail: tz -a mod -s "zone=' + test_tz[t] + '"\r\n')

        else:

            check_result = SendCmd(c, 'tz')

            if test_tz[t] not in check_result:

                FailFlag = True
                tolog('\r\nFail: please check out ' + test_tz[t] + '\r\n')

            elif tz_dist[test_tz[t]] not in check_result:

                FailFlag = True
                tolog('\r\nFail: please check out ' + tz_dist[test_tz[t]] + '\r\n')

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)

    return FailFlag


def invalid_parameter_for_tz(c):

    FailFlag = False

    # test data
    send_command = [
        'tz test',
        'tz -d test',
        'tz -a test',
        'tz -a mod -s ""',
        'tz -a mod -s "zone=1"'
    ]

    for command in send_command:

        result = SendCmd(c, command)

        if 'Error (' not in result:

            FailFlag = True
            tolog('Fail: ' + command + '\r\n')

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)

    return FailFlag


def invalid_option_for_tz(c):

    FailFlag = False

    # test data
    send_command = [
        'tz -test',
        'tz -d -test',
        'tz -a test',
        'tz -a mod -test ""',
        'tz -a mod -s "test=Beijing"'
    ]

    for command in send_command:

        result = SendCmd(c, command)

        if 'Error (' not in result:

            FailFlag = True
            tolog('Fail: ' + command + '\r\n')

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)

    return FailFlag


def missing_parameter_for_tz(c):

    FailFlag = False

    # test data
    send_command = [
        'tz -a',
        'tz -a mod -s '
    ]

    for command in send_command:

        result = SendCmd(c, command)

        if 'Error (' not in result:

            FailFlag = True
            tolog('Fail: ' + command + '\r\n')

    if FailFlag:
        tolog(Fail)
    else:
        tolog(Pass)

    return FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    list_tz(c)
    list_tz_detail(c)
    mod_tz(c)
    invalid_parameter_for_tz(c)
    invalid_option_for_tz(c)
    missing_parameter_for_tz(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped