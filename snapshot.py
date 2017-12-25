# coding = utf-8
# 2017.10.30

from ssh_connect import ssh_conn
import time
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/snapshot.xlsx'


def precondition():

    try:

        pdId = find_pd_id()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:
        # create pool
        server.webapi('post', 'pool', {"name": "test_snap_pool", "pds": pdId[:3], "raid_level": "raid5"})

        # create nasShare
        server.webapi('post', 'nasshare', {'pool_id': 0, 'name': 'test_snap_nas', 'capacity': '2GB'})

        # create volume
        server.webapi('post', 'volume', {'pool_id': 0, 'name': 'test_snap_volume', 'capacity': '2GB'})


def clean_up_environment():

    server.webapi('delete', 'pool/0?force=1')


def add_snapshot(c):

    cli_setting = cli_test_setting()

    # precondition
    precondition()

    cli_setting.setting(c, data, 'add_snapshot', 1)

    return cli_setting.FailFlag


def list_snapshot(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_snapshot')

    return cli_list.FailFlag


def list_snapshot_by_verbose_mode(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_snapshot_by_verbose_mode')

    return cli_list.FailFlag


def mod_snapshot(c):

    cli_setting = cli_test_setting()

    # precondition
    server.webapi('post', 'snapshot/2/unmount')

    cli_setting.setting(c, data, 'mod_snapshot', 1)

    return cli_setting.FailFlag


def export_unexport_snapshot(c):

    cli_setting = cli_test_setting()

    # precondition
    server.webapi('post', 'snapshot/3/unexport')

    cli_setting.setting(c, data, 'export_unexport_snapshot', 1)

    return cli_setting.FailFlag


def mount_umount_snapshot(c):

    cli_setting = cli_test_setting()

    # precondition
    server.webapi('post', 'snapshot/2/unmount')

    cli_setting.setting(c, data, 'mount_umount_snapshot', 1)

    return cli_setting.FailFlag


def rollback_snapshot(c):

    cli_other_action = cli_test_other_action()

    # precondition
    server.webapi('post', 'snapshot', {"name": 'test_volume_rollback', "type": 'volume', "source_id": 0})

    server.webapi('post', 'snapshot', {"name": 'test_nas_rollback', "type": 'nasshare', "source_id": 0})

    cli_other_action.other_need_confirm(c, data, 'rollback_snapshot')

    return cli_other_action.FailFlag


def del_snapshot(c):

    cli_delete = cli_test_delete()

    # precondition: create clone
    server.webapi('post', 'clone', {"source_id": 2, "name": 'test_volume_snap_f'})
    server.webapi('post', 'clone', {"source_id": 3, "name": 'test_nas_snap_f'})

    cli_delete.delete(c, data, 'del_snapshot')

    return cli_delete.FailFlag


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
    clean_up_environment()

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    add_snapshot(c)
    list_snapshot(c)
    list_snapshot_by_verbose_mode(c)
    mod_snapshot(c)
    export_unexport_snapshot(c)
    mount_umount_snapshot(c)
    rollback_snapshot(c)
    del_snapshot(c)
    invalid_setting_parameter(c)
    invalid_option(c)
    missing_parameter(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped