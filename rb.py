# coding = utf-8
# 2017.11.01

from ssh_connect import ssh_conn
import time
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/rb.xlsx'


def raid1_start_rb(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        pdId = find_pd_id()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        # create pool
        server.webapi('post', 'pool', {"name": "test_rb_1", "pds": pdId[:2], "raid_level": "raid1"})

        cli_setting.setting(c, data, 'raid1_start_rb', 3)

    return cli_setting.FailFlag


def raid5_start_rb(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        pdId = find_pd_id()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        # create pool
        server.webapi('post', 'pool', {"name": "test_rb_5", "pds": pdId[:3], "raid_level": "raid5"})

        cli_setting.setting(c, data, 'raid5_start_rb', 3)

    return cli_setting.FailFlag


def raid6_start_rb(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        pdId = find_pd_id()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        # create pool
        server.webapi('post', 'pool', {"name": "test_rb_6", "pds": pdId[:4], "raid_level": "raid6"})

        cli_setting.setting(c, data, 'raid6_start_rb', 3)

    return cli_setting.FailFlag


def raid10_start_rb(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        pdId = find_pd_id()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        # create pool
        server.webapi('post', 'pool', {"name": "test_rb_10", "pds": pdId[:4], "raid_level": "raid10"})

        cli_setting.setting(c, data, 'raid10_start_rb', 3)

    return cli_setting.FailFlag


def raid50_start_rb(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        pdId = find_pd_id()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        # create pool
        server.webapi('post', 'pool', {"name": "test_rb_50", "pds": pdId[:6], "raid_level": "raid50", "axle": 2})
        time.sleep(5)

        cli_setting.setting(c, data, 'raid50_start_rb', 3)

    return cli_setting.FailFlag


def raid60_start_rb(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        pdId = find_pd_id()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        # create pool
        server.webapi('post', 'pool', {"name": "test_rb_60", "pds": pdId[:8], "raid_level": "raid60", "axle": 2})
        time.sleep(5)

        cli_setting.setting(c, data, 'raid60_start_rb', 3)

    return cli_setting.FailFlag


def list_rb(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_rb')

    return cli_list.FailFlag


def stop_rb(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'stop_rb', 3)

    return cli_setting.FailFlag


def invalid_setting_parameter(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_parameter')

    return cli_failed_test.FailFlag


def invalid_option(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option')

    return cli_failed_test.FailFlag


def missing_parameter(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter')

    # clean up environment
    server.webapi('delete', 'pool/0?force=1')

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    raid1_start_rb(c)
    raid5_start_rb(c)
    raid6_start_rb(c)
    raid10_start_rb(c)
    raid50_start_rb(c)
    raid60_start_rb(c)
    list_rb(c)
    stop_rb(c)
    invalid_setting_parameter(c)
    invalid_option(c)
    missing_parameter(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped