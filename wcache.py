# --coding = utf-8--
# 2017.12.11

from ssh_connect import ssh_conn
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/wcache.xlsx'


def add_wcache_dedication(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        pdId = find_pd_id()
        # create pool
        server.webapi('post', 'pool', {"name": "test_cache_0", "pds": pdId[:3], "raid_level": "raid5"})
        server.webapi('post', 'pool', {"name": "test_cache_1", "pds": pdId[4:7], "raid_level": "raid5"})

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'add_wcache_dedication', 1)

    return cli_setting.FailFlag


def mod_wcache(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'mod_wcache', 1)

    return cli_setting.FailFlag


def add_wcache_no_dedication(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        find_pd_id()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'add_wcache_no_dedication', 1)

    return cli_setting.FailFlag


def list_wcache(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_wcache')

    return cli_list.FailFlag


def def_wcache(c):

    cli_delete = cli_test_delete()

    cli_delete.delete(c, data, 'def_wcache')

    return cli_delete.FailFlag


def invalid_setting_for_wcache(c):
    # precondition
    server.webapi('post', 'wcache/attach', {'pd_list': [5, 6]})

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_wcache')

    return cli_failed_test.FailFlag


def invalid_option_for_wcache(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_wcache')

    return cli_failed_test.FailFlag


def missing_parameter_for_wcache(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_for_wcache')

    # clean up environment
    try:

        find_pd_id()

    except TypeError:

        tolog('to clean up environment is failed\r\n')

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    add_wcache_dedication(c)
    mod_wcache(c)
    add_wcache_no_dedication(c)
    list_wcache(c)
    def_wcache(c)
    invalid_setting_for_wcache(c)
    invalid_option_for_wcache(c)
    missing_parameter_for_wcache(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped