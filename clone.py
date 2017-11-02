# coding = utf-8
# 2017.10.27

from ssh_connect import ssh_conn
import time
from cli_test import cli_test
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/clone.xlsx'


def precondition():
    pdId = find_pd_id()
    # create pool
    server.webapi('post', 'pool', {"name": "test_clone_pool", "pds": pdId[:3], "raid_level": "raid5"})

    # create nasShare snapshot
    server.webapi('post', 'nasshare', {'pool_id': 0, 'name': 'test_clone_nas', 'capacity': '2GB'})

    server.webapi('post', 'snapshot', {"name": "test_clone_nas_snap", "type": 'nasshare', "source_id": 0})

    # create volume snapshot
    server.webapi('post', 'volume', {'pool_id': 0, 'name': 'test_clone_volume', 'capacity': '2GB'})

    server.webapi('post', 'snapshot', {"name": "test_clone_vol_snap", "type": 'volume', "source_id": 0})


def clean_up_environment():

    server.webapi('delete', 'pool/0?force=1')


def add_clone(c):
    # precondition
    precondition()

    cli_test.setting(c, data, 'add_clone', 1)


def list_clone(c):

    cli_test.list(c, data, 'list_clone')


def list_clone_verbose_mode(c):

    cli_test.list(c, data, 'list_clone_verbose_mode')


def mod_clone(c):
    # precondition
    server.webapi('post', 'clone/2/unmount')

    cli_test.setting(c, data, 'mod_clone', 1)


def export_unexport_clone(c):
    # precondition
    server.webapi('post', 'clone/3/unexport')

    cli_test.setting(c, data, 'export_unexport_clone', 1)


def mount_umount_clone(c):
    # precondition
    server.webapi('post', 'clone/2/unmount')

    cli_test.setting(c, data, 'mount_umount_clone', 1)


def promote_clone(c):

    cli_test.other(c, data, 'promote_clone')


def del_clone(c):

    cli_test.delete(c, data, 'del_clone')


def invalid_setting_parameter(c):

    cli_test.failed_test(c, data, 'invalid_setting_parameter')


def invalid_option(c):

    cli_test.failed_test(c, data, 'invalid_option')


def missing_parameter(c):

    cli_test.failed_test(c, data, 'missing_parameter')

    # clean_up_environment
    clean_up_environment()


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    add_clone(c)
    list_clone(c)
    list_clone_verbose_mode(c)
    mod_clone(c)
    export_unexport_clone(c)
    mount_umount_clone(c)
    promote_clone(c)
    del_clone(c)
    invalid_setting_parameter(c)
    invalid_option(c)
    missing_parameter(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped