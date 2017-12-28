# coding = utf-8
# 2017.10.31

from ssh_connect import ssh_conn
import time, json
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/phydrv.xlsx'


def precondition():
    pdId = find_pd_id()
    ssd_id = []

    # create pool
    server.webapi('post', 'pool', {"name": "test_phy_0", "pds": [pdId[0]], "raid_level": "RAID0"})
    server.webapi('post', 'pool', {"name": "test_phy_1", "pds": pdId[1:4], "raid_level": "raid5"})

    # create spare
    server.webapi('post', 'spare', {"pd_id": pdId[4], "dedicated": 'global', "revertible": 0})
    server.webapi('post', 'spare', {"pd_id": pdId[5], "dedicated": 'dedicated', "revertible": 0, "pool_list": [0]})

    # create cache
    pd_request = server.webapi('get', 'phydrv')
    pd_info = json.loads(pd_request["text"])

    for info in pd_info:
        if info["media_type"] == 'SSD':
            ssd_id.append(info["id"])

    server.webapi('post', 'rcache/attach', {"pd_list": [ssd_id[0]]})
    server.webapi('post', 'wcache/attach', {"pd_list": ssd_id[1:], "pool_list": []})


def list_phydrv(c):

    cli_list = cli_test_list()

    # precondition
    try:

        precondition()

    except (TypeError, IndexError):

        tolog('precondition is failed\r\n')

    else:

        cli_list.list(c, data, 'list_phydrv')

        return cli_list.FailFlag


def list_phydrv_by_verbose_mode(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_phydrv_by_verbose_mode')

    return cli_list.FailFlag


def mod_phydrv(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'mod_phydrv', 1)

    return cli_setting.FailFlag


def locate_phydrv(c):

    cli_other_action = cli_test_other_action()

    cli_other_action.other(c, data, 'locate_phydrv')

    return cli_other_action.FailFlag


def online_offline_phydrv(c):
    cli_setting = cli_test_setting()

    # precondition: create pool
    try:

        pdId = find_pd_id()
        server.webapi('post', 'pool', {"name": "test_phy_2", "pds": pdId[:3], "raid_level": "raid5"})

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'online_offline_phydrv', 3)

        return cli_setting.FailFlag


def clear_phydrv(c):

    cli_setting = cli_test_setting()

    # precondition: create pool, create spare
    try:

        pdId = find_pd_id()
        server.webapi('post', 'pool', {"name": "test_phy_3", "pds": pdId[:3], "raid_level": "raid5"})
        server.webapi('post', 'spare', {"pd_id": pdId[4], "dedicated": 'global', "revertible": 0})

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'clear_phydrv', 3)

        return cli_setting.FailFlag


def invalid_setting_parameter(c):

    cli_failed_test = cli_test_failed_test()

    # precondition
    try:

        find_pd_id()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_failed_test.failed_test(c, data, 'invalid_setting_parameter')

        return cli_failed_test.FailFlag


def invalid_option(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option')

    return cli_failed_test.FailFlag


def missing_parameter(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter')

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    list_phydrv(c)
    list_phydrv_by_verbose_mode(c)
    mod_phydrv(c)
    locate_phydrv(c)
    online_offline_phydrv(c)
    clear_phydrv(c)
    invalid_setting_parameter(c)
    invalid_option(c)
    missing_parameter(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped