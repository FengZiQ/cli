# coding = utf-8
# 2017.10.31

from ssh_connect import ssh_conn
import time
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/perfstats.xlsx'


def precondition():
    pdId = find_pd_id()
    # create pool
    server.webapi('post', 'pool', {"name": "test_perf_pool", "pds": pdId[:3], "raid_level": "raid5"})

    # create nasShare
    server.webapi('post', 'nasshare', {'pool_id': 0, 'name': 'test_perf_nas', 'capacity': '2GB'})
    # create snapshot of NASShare type
    server.webapi('post', 'snapshot', {"name": "test_snap_nas_perf", "type": 'nasshare', "source_id": 0})
    # create clone of NASShare type
    server.webapi('post', 'clone', {"source_id": 0, "name": 'test_perf_nas'})

    # create volume
    server.webapi('post', 'volume', {'pool_id': 0, 'name': 'test_perf_volume', 'capacity': '2GB'})
    # create snapshot of volume type
    server.webapi('post', 'snapshot', {"name": "test_snap_vol_perf", "type": 'volume', "source_id": 0})
    # create clone of volume type
    server.webapi('post', 'clone', {"source_id": 1, "name": 'test_perf_vol'})


def clean_up_environment():

    server.webapi('delete', 'pool/0?force=1')


def start_perfstats(c):
    cli_other_action = cli_test_other_action()

    # precondition
    precondition()

    cli_other_action.other(c, data, 'start_perfstats')

    return cli_other_action.FailFlag


def list_perfstats(c):
    cli_list = cli_test_list()

    # precondition
    server.webapi('post', 'perfstatsstart')

    cli_list.list(c, data, 'list_perfstats')

    return cli_list.FailFlag


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

    start_perfstats(c)
    list_perfstats(c)
    invalid_setting_parameter(c)
    invalid_option(c)
    missing_parameter(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped