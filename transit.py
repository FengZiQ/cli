# -*- coding = utf-8-*-
# 2018.02.23

from ssh_connect import ssh_conn
from send_cmd import *
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/transit.xlsx'


def precondition():
    pdId = find_pd_id()

    # create pool
    server.webapi('post', 'pool', {"name": "test_transit_0", "pds": [pdId[0]], "raid_level": "RAID0"})
    server.webapi('post', 'pool', {"name": "test_transit_1", "pds": pdId[1:4], "raid_level": "raid5"})

    # create spare
    server.webapi('post', 'spare', {"pd_id": pdId[4], "dedicated": 'global', "revertible": 0})
    # server.webapi('post', 'spare', {"pd_id": pdId[5], "dedicated": 'dedicated', "revertible": 0, "pool_list": [0]})
    server.webapi('post', 'spare', {"pd_id": pdId[6], "dedicated": 'dedicated', "revertible": 1, "pool_list": [1]})


def start_transit(c):
    # precondition
    precondition()

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'start_transit')

    return cli_setting.FailFlag


def list_transit(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_transit')

    return cli_list.FailFlag


def stop_transit(c):

    cli_delete = cli_test_delete()

    cli_delete.delete(c, data, 'stop_transit')

    return cli_delete.FailFlag


def invalid_setting_transit(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_transit')

    return cli_failed_test.FailFlag


def invalid_option_transit(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_transit')

    return cli_failed_test.FailFlag


def missing_parameter_transit(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_transit')

    # clean_up_environment
    find_pd_id()

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    start_transit(c)
    # list_transit(c)
    # stop_transit(c)
    # invalid_setting_transit(c)
    # invalid_option_transit(c)
    # missing_parameter_transit(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped