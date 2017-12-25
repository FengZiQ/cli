# coding = utf-8
# 2017.12.25

from ssh_connect import ssh_conn
import time
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/replication.xlsx'


def precondition():

    pdId = find_pd_id()
    # create pool
    server.webapi('post', 'pool', {"name": "T_replication_0", "pds": pdId[:3], "raid_level": "raid5"})

    server.webapi('post', 'pool', {"name": "T_replication_1", "pds": pdId[3:6], "raid_level": "raid5"})

    server.webapi('post', 'pool', {"name": "T_replication_2", "pds": [pdId[6]], "raid_level": "raid0"})

    # create source volume
    for i in range(6):

        if i < 2:
            server.webapi('post', 'volume', {
                'pool_id': 2,
                'name': 'T_replication_vol_' + str(i),
                'capacity': '4GB',
                'thin_prov': i
            })

        elif i > 2 & i < 4:
            server.webapi('post', 'volume', {
                'pool_id': 0,
                'name': 'T_replication_vol_' + str(i),
                'capacity': '4GB',

            })

        else:

            server.webapi('post', 'volume', {
                'pool_id': 1,
                'name': 'T_replication_vol_' + str(i),
                'capacity': '1GB',
                'thin_prov': 1
            })

    return


def clean_up_environment():

    for i in range(3):

        server.webapi('delete', 'pool/' + str(i) + '?force=1')

    return


def add_replication(c):

    # precondition
    precondition()

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'add_replication', 1)

    return cli_setting.FailFlag


def list_replication(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_replication')

    return cli_list.FailFlag


def list_replication_by_verbose(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_replication_by_verbose')

    return cli_list.FailFlag


def del_replication(c):

    cli_delete = cli_test_delete()

    cli_delete.delete(c, data, 'del_replication', 1)

    return cli_delete.FailFlag


def help_replication(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'help_replication')

    return cli_list.FailFlag


def invalid_setting_for_replication(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_replication')

    return cli_failed_test.FailFlag


def invalid_option_for_replication(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_replication')

    return cli_failed_test.FailFlag


def missing_parameter_replication(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_replication')

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    add_replication(c)
    list_replication(c)
    list_replication_by_verbose(c)
    del_replication(c)
    help_replication(c)
    invalid_setting_for_replication(c)
    invalid_option_for_replication(c)
    missing_parameter_replication(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped