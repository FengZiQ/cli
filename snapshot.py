# coding = utf-8
# 2017.10.30

from ssh_connect import ssh_conn
import time
from cli_test import cli_test
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/snapshot.xlsx'


def precondition():
    pdId = find_pd_id()
    # create pool
    server.webapi('post', 'pool', {"name": "test_snap_pool", "pds": pdId[:3], "raid_level": "raid5"})

    # create nasShare
    server.webapi('post', 'nasshare', {'pool_id': 0, 'name': 'test_snap_nas', 'capacity': '2GB'})

    # create volume
    server.webapi('post', 'volume', {'pool_id': 0, 'name': 'test_snap_volume', 'capacity': '2GB'})


def clean_up_environment():

    server.webapi('delete', 'pool/0?force=1')


def add_snapshot(c):
    # precondition
    precondition()

    cli_test.setting(c, data, 'add_snapshot', 1)


def list_snapshot(c):

    cli_test.list(c, data, 'list_snapshot')


def list_snapshot_by_verbose_mode(c):

    cli_test.list(c, data, 'list_snapshot_by_verbose_mode')


def mod_snapshot(c):
    # precondition
    server.webapi('post', 'snapshot/2/unmount')

    cli_test.setting(c, data, 'mod_snapshot', 1)


def export_unexport_snapshot(c):
    # precondition
    server.webapi('post', 'snapshot/3/unexport')

    cli_test.setting(c, data, 'export_unexport_snapshot', 1)


def mount_umount_snapshot(c):
    # precondition
    server.webapi('post', 'snapshot/2/unmount')

    cli_test.setting(c, data, 'mount_umount_snapshot', 1)


def rollback_snapshot(c):
    # precondition
    server.webapi('post', 'snapshot', {"name": 'test_volume_rollback', "type": 'volume', "source_id": 0})

    server.webapi('post', 'snapshot', {"name": 'test_nas_rollback', "type": 'nasshare', "source_id": 0})

    cli_test.other(c, data, 'rollback_snapshot')


def del_snapshot(c):
    # precondition: create clone
    server.webapi('post', 'clone', {"source_id": 2, "name": 'test_volume_snap_f'})
    server.webapi('post', 'clone', {"source_id": 3, "name": 'test_nas_snap_f'})

    cli_test.delete(c, data, 'del_snapshot')


def invalid_setting_parameter(c):

    cli_test.failed_test(c, data, 'invalid_setting_parameter')


def invalid_option(c):

    cli_test.failed_test(c, data, 'invalid_option')


def missing_parameter(c):

    cli_test.failed_test(c, data, 'missing_parameter')

    # clean up environment
    clean_up_environment()


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