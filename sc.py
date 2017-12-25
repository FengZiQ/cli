# --coding = utf-8--
# 2017.12.08

from ssh_connect import ssh_conn
import time
import json
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/sc.xlsx'


def precondition():

    try:

        pdId = find_pd_id()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        # create pool
        server.webapi('post', 'pool', {"name": "test_phy_1", "pds": pdId[:4], "raid_level": "raid5"})

        # create spare
        server.webapi('post', 'spare', {"pd_id": pdId[4], "dedicated": 'global', "revertible": 0})
        server.webapi('post', 'spare', {"pd_id": pdId[5], "dedicated": 'dedicated', "revertible": 0, "pool_list": [0]})


def start_sc(c):

    # precondition
    precondition()

    cli_other_action = cli_test_other_action()

    cli_other_action.other(c, data, 'start_sc')

    return cli_other_action.FailFlag


def list_sc(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_sc')

    return cli_list.FailFlag


def invalid_setting_for_sc(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_sc')

    return cli_failed_test.FailFlag


def invalid_option_for_sc(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_sc')

    return cli_failed_test.FailFlag


def missing_parameter_for_sc(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_sc')

    # clean up environment
    try:

        find_pd_id()

    except TypeError:

        tolog('to clean up environment is failed\r\n')

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    start_sc(c)
    list_sc(c)
    invalid_setting_for_sc(c)
    invalid_option_for_sc(c)
    missing_parameter_for_sc(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped