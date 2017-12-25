# coding = utf-8
# 2017.11.03

from ssh_connect import ssh_conn
import time, json
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/rcache.xlsx'


def add_rcache_by_one_pd(c):

    cli_setting = cli_test_setting()

    # precondition
    try:
        find_pd_id()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'add_rcache_by_one_pd', 1)

    return cli_setting.FailFlag


def add_rcache_by_multiple_pd(c):

    cli_setting = cli_test_setting()

    # precondition
    try:
        find_pd_id()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'add_rcache_by_multiple_pd', 1)

    return cli_setting.FailFlag


def list_rcache(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_rcache')

    return cli_list.FailFlag


def def_rcache(c):

    cli_delete = cli_test_delete()

    cli_delete.delete(c, data, 'def_rcache')

    return cli_delete.FailFlag


def invalid_setting_for_rcache(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_rcache')

    return cli_failed_test.FailFlag


def invalid_option_for_rcache(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_rcache')

    return cli_failed_test.FailFlag


def missing_parameter_for_rcache(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_for_rcache')

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    add_rcache_by_one_pd(c)
    add_rcache_by_multiple_pd(c)
    list_rcache(c)
    def_rcache(c)
    invalid_setting_for_rcache(c)
    invalid_option_for_rcache(c)
    missing_parameter_for_rcache(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped