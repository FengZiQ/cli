# -*- coding = utf-8 -*-
# 2018.01.29

from ssh_connect import ssh_conn
from cli_test import *


data = 'data/swmgt.xlsx'


def list_swmgt(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_swmgt')

    return cli_list.FailFlag


def start_stop_swmgt(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'start_stop_swmgt')

    return cli_setting.FailFlag


def restart_swmgt(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'restart_swmgt')

    return cli_setting.FailFlag


def mod_swmgt(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'mod_swmgt')

    return cli_setting.FailFlag


def add_swmgt(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'add_swmgt')

    return cli_setting.FailFlag


def delete_swmgt(c):

    cli_delete = cli_test_delete()

    cli_delete.delete(c, data, 'delete_swmgt')

    return cli_delete.FailFlag


def invalid_parameter_for_swmgt(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_parameter_for_swmgt')

    return cli_failed_test.FailFlag


def invalid_option_for_swmgt(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_swmgt')

    return cli_failed_test.FailFlag


def missing_parameter_for_swmgt(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_for_swmgt')

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    list_swmgt(c)
    start_stop_swmgt(c)
    restart_swmgt(c)
    mod_swmgt(c)
    add_swmgt(c)
    delete_swmgt(c)
    invalid_parameter_for_swmgt(c)
    invalid_option_for_swmgt(c)
    missing_parameter_for_swmgt(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped