# coding = utf-8
# 2018.01.12

from ssh_connect import ssh_conn
from cli_test import *

data = 'data/net.xlsx'


def list_net(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_net')

    return cli_list.FailFlag


def list_net_by_verbose_mode(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_net_by_verbose_mode')

    return cli_list.FailFlag


def enable_modify_disable(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'enable_modify_disable', 5)

    return cli_setting.FailFlag


def invalid_setting_for_net(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_net')

    return cli_failed_test.FailFlag


def invalid_option_for_net(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_net')

    return cli_failed_test.FailFlag


def missing_parameter_for_net(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_for_net')

    return cli_failed_test.FailFlag

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    list_net(c)
    list_net_by_verbose_mode(c)
    enable_modify_disable(c)
    invalid_setting_for_net(c)
    invalid_option_for_net(c)
    missing_parameter_for_net(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped
