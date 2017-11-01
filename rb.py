# coding = utf-8
# 2017.11.01

from ssh_connect import ssh_conn
import time
from cli_test import cli_test
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/rb.xlsx'


def raid1_start_rb(c):
    # precondition
    pdId = find_pd_id()

    # create pool
    server.webapi('post', 'pool', {"name": "test_rb_1", "pds": pdId[:2], "raid_level": "raid1"})

    cli_test.setting(c, data, 'raid1_start_rb', 3)


def raid5_start_rb(c):
    # precondition
    pdId = find_pd_id()

    # create pool
    server.webapi('post', 'pool', {"name": "test_rb_5", "pds": pdId[:3], "raid_level": "raid5"})

    cli_test.setting(c, data, 'raid5_start_rb', 3)


def raid6_start_rb(c):
    # precondition
    pdId = find_pd_id()

    # create pool
    server.webapi('post', 'pool', {"name": "test_rb_6", "pds": pdId[:4], "raid_level": "raid6"})

    cli_test.setting(c, data, 'raid6_start_rb', 3)


def raid10_start_rb(c):
    # precondition
    pdId = find_pd_id()

    # create pool
    server.webapi('post', 'pool', {"name": "test_rb_10", "pds": pdId[:4], "raid_level": "raid10"})

    cli_test.setting(c, data, 'raid10_start_rb', 3)


def raid50_start_rb(c):
    # precondition
    pdId = find_pd_id()

    # create pool
    server.webapi('post', 'pool', {"name": "test_rb_50", "pds": pdId[:6], "raid_level": "raid50", "axle": 2})
    time.sleep(5)

    cli_test.setting(c, data, 'raid50_start_rb', 3)


def raid60_start_rb(c):
    # precondition
    pdId = find_pd_id()

    # create pool
    server.webapi('post', 'pool', {"name": "test_rb_60", "pds": pdId[:8], "raid_level": "raid60", "axle": 2})
    time.sleep(5)

    cli_test.setting(c, data, 'raid60_start_rb', 3)


def list_rb(c):

    cli_test.list(c, data, 'list_rb')


def stop_rb(c):

    cli_test.setting(c, data, 'stop_rb', 3)


def invalid_setting_parameter(c):

    cli_test.failed_test(c, data, 'invalid_setting_parameter')


def invalid_option(c):

    cli_test.failed_test(c, data, 'invalid_option')


def missing_parameter(c):

    cli_test.failed_test(c, data, 'missing_parameter')


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