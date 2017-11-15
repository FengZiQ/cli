# coding = utf-8
# 2017.10.10
# 2017.11.15

from ssh_connect import ssh_conn
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/protocol.xlsx'


def precondition():
    pdId = find_pd_id("2TB")

    # create pool
    server.webapi('post', 'pool', {
        "name": 'test_protocol_pool',
        "raid_level": 'raid5',
        "pds": pdId
    })

    # create nasShare
    for i in range(3):
        server.webapi('post', 'nasshare', {
            "pool_id": 0,
            "name": 'test_protocol_nasShare_' + str(i),
            "capacity": '2GB'
        })

    # create snapshot
    for i in range(3):
        server.webapi('post', 'snapshot', {
            "name": 'test_protocol_snap_' + str(i),
            "type": 'nasshare',
            "source_id": 0
        })

    # create clone
    for i in range(3):
        server.webapi('post', 'clone', {
            "name": 'test_protocol_clone_' + str(i),
            "source_id": 0
        })

    # create nas user
    server.webapi('post', 'dsuser', {
        "id": 'test_protocol',
        "password": '000000'
    })


def list_all_protocol(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_all_protocol')

    return cli_list.FailFlag


def list_single_protocol(c):
    # precondition
    precondition()

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_single_protocol')

    return cli_list.FailFlag


def mod_ftp_protocol(c):
    # precondition
    server.webapi('post', 'protocol/reset')

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'mod_ftp_protocol', 3)

    return cli_setting.FailFlag


def mod_smb_protocol(c):
    # precondition
    server.webapi('post', 'protocol/reset')

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'mod_smb_protocol', 3)

    return cli_setting.FailFlag


def mod_nfs_protocol(c):
    # precondition
    server.webapi('post', 'protocol/reset')

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'mod_nfs_protocol', 3)

    return cli_setting.FailFlag


def reset_all_protocol(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'reset_all_protocol', 3)

    return cli_setting.FailFlag


def reset_single_protocol(c):
    # precondition
    for n in ['FTP', 'NFS', 'SMB']:
        server.webapi('post', 'protocol/disable/' + n)

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'reset_single_protocol', 3)

    return cli_setting.FailFlag


def enable_protocol(c):
    # precondition
    for n in ['FTP', 'NFS', 'SMB']:
        server.webapi('post', 'protocol/disable/' + n)

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'enable_protocol', 3)

    return cli_setting.FailFlag


def disable_protocol(c):
    # precondition
    for n in ['FTP', 'NFS', 'SMB']:
        server.webapi('post', 'protocol/enable/' + n)

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'disable_protocol', 3)

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

    clean_up_environment()

    return cli_failed_test.FailFlag


def clean_up_environment():
    # delete pool
    server.webapi('delete', 'pool/0?force=1')

    # delete nas user
    server.webapi('delete', 'dsuser/test_protocol')


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    list_all_protocol(c)
    list_single_protocol(c)
    mod_ftp_protocol(c)
    mod_smb_protocol(c)
    mod_nfs_protocol(c)
    reset_all_protocol(c)
    reset_single_protocol(c)
    enable_protocol(c)
    disable_protocol(c)
    invalid_setting_parameter(c)
    invalid_option(c)
    missing_parameter(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped