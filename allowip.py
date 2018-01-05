# coding = utf-8
# 2017.11.15

from ssh_connect import ssh_conn
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/allowip.xlsx'


def precondition():
    pdId = find_pd_id()
    # create pool
    server.webapi('post', 'pool', {"name": "test_allowip", "pds": pdId[:3], "raid_level": "raid5"})

    # create nasShare
    for i in range(2):
        server.webapi('post', 'nasshare', {'pool_id': 0, 'name': 'test_allowip_nas_' + str(i), 'capacity': '2GB'})

    # create snapshot
    for i in range(3):
        server.webapi('post', 'snapshot', {"name": "test_allowip_snap_" + str(i), "type": 'nasshare', "source_id": 0})

    # create clone
    for i in range(2):
        server.webapi('post', 'clone', {"name": "test_allowip_clone_" + str(i), "source_id": 0})

    # clear allow ip
    for id in ['nasshare_0', 'snapshot_0', 'clone_0']:
        server.webapi('post', 'allowip/' + id, {"allow_ip": []})


def add_allowip(c):
    # precondition

    try:

        precondition()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting = cli_test_setting()

        cli_setting.setting(c, data, 'add_allowip', 3)

        return cli_setting.FailFlag


def list_allowip(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_allowip')

    return cli_list.FailFlag


def list_allowip_by_verbose_mode(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_allowip_by_verbose_mode')

    return cli_list.FailFlag


def mod_allowip(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'mod_allowip', 3)

    return cli_setting.FailFlag


def del_allowip(c):

    cli_delete = cli_test_delete()

    cli_delete.delete(c, data, 'del_allowip', 3)

    return cli_delete.FailFlag


def invalid_setting_for_allowip(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_allowip')

    return cli_failed_test.FailFlag


def invalid_option_for_allowip(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_allowip')

    return cli_failed_test.FailFlag


def missing_parameter_for_allowip(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_for_allowip')

    # clean up environment
    try:
        find_pd_id()
    except TypeError:
        tolog('to clean up environment is failed\r\n')

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    add_allowip(c)
    list_allowip(c)
    list_allowip_by_verbose_mode(c)
    mod_allowip(c)
    del_allowip(c)
    invalid_setting_for_allowip(c)
    invalid_option_for_allowip(c)
    missing_parameter_for_allowip(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped
