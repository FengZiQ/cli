# -*- coding = utf-8 -*-
# 2018.02.05

from ssh_connect import ssh_conn
from cli_test import *
from remote import server
import json


data = 'data/subscription.xlsx'


def precondition():
    clean_up_environment()

    privilege = ['power', 'maintenance', 'view']
    for i in range(3):
        server.webapi('post', 'user', {
            'id': 'test_user_'+str(i),
            'passwd': '000000',
            'email': 't@1.cn',
            'privilege': privilege[i]
        })

    server.webapi('post', 'user', {'id': 'test_user_3', 'passwd': '000000', 'privilege': privilege[2]})

    return


def clean_up_environment():
    # clean up environment: delete user
    try:
        users_request = server.webapi('get', 'user')
        users_info = json.loads(users_request["text"])
        for user in users_info:
            if user["id"] != 'administrator':
                server.webapi('delete', 'user/' + user["id"])
    except:
        tolog("to clean up environment is failed\r\n")

    return


def list_subscription(c):
    # precondition
    precondition()

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_subscription')

    return cli_list.FailFlag


def list_subscription_by_v_mode(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_subscription_by_v_mode')

    return cli_list.FailFlag


def mod_subscription(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'mod_subscription', 3)

    return cli_setting.FailFlag


def enable_disable_subscription(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'enable_disable_subscription', 3)

    return cli_setting.FailFlag


def test_subscription(c):
    # precondition
    server.webapi('put', 'user/administrator', {'email': 'zach.feng@cn.promise.com'})

    cli_setting = cli_test_other_action()

    cli_setting.other(c, data, 'test_subscription')

    return cli_setting.FailFlag


def invalid_parameter_subscription(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_parameter_subscription')

    return cli_failed_test.FailFlag


def invalid_option_for_subscription(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_subscription')

    return cli_failed_test.FailFlag


def missing_parameter_subscription(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_subscription')

    # clean up environment
    clean_up_environment()

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    list_subscription(c)
    list_subscription_by_v_mode(c)
    mod_subscription(c)
    enable_disable_subscription(c)
    test_subscription(c)
    invalid_parameter_subscription(c)
    invalid_option_for_subscription(c)
    missing_parameter_subscription(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped