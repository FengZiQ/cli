# coding = utf-8
# 2017.11.13

from ssh_connect import ssh_conn
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/spare.xlsx'


def add_global_spare(c):
    cli_setting = cli_test_setting()

    # precondition
    pdId = find_pd_id("2TB")
    # create pool
    server.webapi('post', 'pool', {"name": "test_spare_pool", "pds": pdId[:3], "raid_level": "raid5"})

    cli_setting.setting(c, data, 'add_global_spare', 3)

    return cli_setting.FailFlag


def add_dedicated_spare(c):
    cli_setting = cli_test_setting()

    # precondition
    pdId = find_pd_id()
    # create pool
    server.webapi('post', 'pool', {"name": "test_spare_pool_0", "pds": pdId[:3], "raid_level": "raid5"})
    server.webapi('post', 'pool', {"name": "test_spare_pool_1", "pds": pdId[3:6], "raid_level": "raid5"})

    cli_setting.setting(c, data, 'add_dedicated_spare', 3)

    return cli_setting.FailFlag


def list_spare(c):
    cli_list = cli_test_list()

    # precondition
    pdId = find_pd_id()

    # create pool
    server.webapi('post', 'pool', {"name": "test_spare_pool", "pds": pdId[:3], "raid_level": "raid5"})

    # create spare
    server.webapi('post', 'spare', {"dedicated": 'global', "revertible": 0, "pool_list": [], "pd_id": pdId[3]})
    server.webapi('post', 'spare', {"dedicated": 'dedicated', "revertible": 1, "pool_list": [0], "pd_id": pdId[5]})

    cli_list.list(c, data, 'list_spare')

    return cli_list.FailFlag


def list_spare_by_verbose_mode(c):
    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_spare_by_verbose_mode')

    return cli_list.FailFlag


def delete_spare(c):
    cli_delete = cli_test_delete()

    cli_delete.delete(c, data, 'delete_spare')

    return cli_delete.FailFlag


def invalid_parameter_for_spare(c):

    cli_failed_test = cli_test_failed_test()
    # precondition
    pdId = find_pd_id()

    # create pool
    server.webapi('post', 'pool', {"name": "test_spare_pool", "pds": pdId[:3], "raid_level": "raid0"})

    cli_failed_test.failed_test(c, data, 'invalid_parameter_for_spare')

    return cli_failed_test.FailFlag


def invalid_option_for_spare(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_spare')

    return cli_failed_test.FailFlag


def missing_parameter_for_spare(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_for_spare')

    # clean up environment
    find_pd_id()

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    add_global_spare(c)
    add_dedicated_spare(c)
    list_spare(c)
    list_spare_by_verbose_mode(c)
    delete_spare(c)
    invalid_parameter_for_spare(c)
    invalid_option_for_spare(c)
    missing_parameter_for_spare(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped