# coding = utf-8
# 2018.01.10

from ssh_connect import ssh_conn
from cli_test import *
from remote import server
import json

data = 'data/target.xlsx'


def precondition():

    tar_request = server.webapi('get', 'target')

    try:
        tar_info = json.loads(tar_request["text"])

        for i in range(len(tar_info)):

            server.webapi('delete', 'target/1')

    except:

        tolog('\r\n precondition is failed\r\n')


def add_target(c):
    # precondition
    precondition()

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'add_target', 1)

    return cli_setting.FailFlag


def list_target(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_target')

    return cli_list.FailFlag


def del_target(c):

    cli_del = cli_test_delete()

    cli_del.delete(c, data, 'del_target', 3)

    return cli_del.FailFlag


def invalid_setting_for_target(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_target')

    return cli_failed_test.FailFlag


def invalid_option_for_target(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_target')

    return cli_failed_test.FailFlag


def missing_parameter_for_target(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_for_target')

    return cli_failed_test.FailFlag

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    # add_target(c)
    # list_target(c)
    # del_target(c)
    invalid_setting_for_target(c)
    invalid_option_for_target(c)
    missing_parameter_for_target(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped
