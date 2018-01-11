# coding = utf-8
# 2018.01.10

from ssh_connect import ssh_conn
from cli_test import *
from remote import server

data = 'data/domain.xlsx'


def list_domain(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_domain')

    return cli_list.FailFlag


def list_domain_by_verbose_mode(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_domain_by_verbose_mode')

    return cli_list.FailFlag


def enable_domain(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'enable_domain', 1)

    return cli_setting.FailFlag


def reset_domain(c):

    cli_other_action = cli_test_other_action()

    cli_other_action.other(c, data, 'reset_domain')

    return cli_other_action.FailFlag


def clear_domain(c):

    cli_other_action = cli_test_other_action()

    cli_other_action.other(c, data, 'clear_domain')

    return cli_other_action.FailFlag


def invalid_setting_for_domain(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_domain')

    return cli_failed_test.FailFlag


def invalid_option_for_domain(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_domain')

    return cli_failed_test.FailFlag


def missing_parameter_for_domain(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_for_domain')

    return cli_failed_test.FailFlag

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    list_domain(c)
    list_domain_by_verbose_mode(c)
    enable_domain(c)
    reset_domain(c)
    clear_domain(c)
    invalid_setting_for_domain(c)
    invalid_option_for_domain(c)
    missing_parameter_for_domain(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped
