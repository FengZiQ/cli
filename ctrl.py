# coding = utf-8
# 2017.12.18

from ssh_connect import ssh_conn
from cli_test import *

data = 'data/ctrl.xlsx'


def list_ctrl(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_ctrl')

    return cli_list.FailFlag


def list_ctrl_by_verbose_mode(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_ctrl_by_verbose_mode')

    return cli_list.FailFlag


def mod_ctrl(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'mod_ctrl', 1)

    return cli_setting.FailFlag


def clear_ctrl(c):

    cli_other_action = cli_test_other_action()

    cli_other_action.other(c, data, 'clear_ctrl')

    return cli_other_action.FailFlag


def invalid_setting_for_ctrl(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_ctrl')

    return cli_failed_test.FailFlag


def invalid_option_for_ctrl(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_ctrl')

    return cli_failed_test.FailFlag


def missing_parameter_for_ctrl(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_for_ctrl')

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    list_ctrl(c)
    list_ctrl_by_verbose_mode(c)
    mod_ctrl(c)
    clear_ctrl(c)
    invalid_setting_for_ctrl(c)
    invalid_option_for_ctrl(c)
    missing_parameter_for_ctrl(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped
