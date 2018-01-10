# coding = utf-8
# 2018.01.10

from ssh_connect import ssh_conn
from cli_test import *

data = 'data/fc.xlsx'


def list_fc(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_fc')

    return cli_list.FailFlag


def list_fc_by_verbose_mode(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_fc_by_verbose_mode')

    return cli_list.FailFlag


def mod_fc(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'mod_fc', 1)

    return cli_setting.FailFlag


def reset_fc(c):

    cli_other_action = cli_test_other_action()

    cli_other_action.other(c, data, 'reset_fc')

    return cli_other_action.FailFlag


def clear_fc(c):

    cli_other_action = cli_test_other_action()

    cli_other_action.other(c, data, 'clear_fc')

    return cli_other_action.FailFlag


def invalid_setting_for_fc(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_fc')

    return cli_failed_test.FailFlag


def invalid_option_for_fc(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_fc')

    return cli_failed_test.FailFlag


def missing_parameter_for_fc(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_for_fc')

    return cli_failed_test.FailFlag

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    list_fc(c)
    list_fc_by_verbose_mode(c)
    mod_fc(c)
    reset_fc(c)
    clear_fc(c)
    invalid_setting_for_fc(c)
    invalid_option_for_fc(c)
    missing_parameter_for_fc(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped
