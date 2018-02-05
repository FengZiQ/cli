# coding = utf-8
# 2017.9.28

from ssh_connect import ssh_conn
import time
import json
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/pool.xlsx'


def precondition():
    flag = False
    # get fc device on fabric
    fabric_request = server.webapi('get', 'fcinitiator')
    try:
        fabric_info = json.loads(fabric_request["text"])
        for fabric in fabric_info:
            if len(fabric["initiators"]) != 0:
                temp = fabric["initiators"]
                for t in temp:
                    if t['wwnn'] == '25-00-00-01-55-59-ea-9d':
                        server.webapi('post', 'target', {"name": '25-00-00-01-55-59-ea-9d'})
                        flag = True
    except:
        tolog('precondition is failed\n')

    return flag


def add_pool_by_external_drive(c):
    # precondition
    if precondition():
        find_pd_id()

        cli_setting = cli_test_setting()

        cli_setting.setting(c, data, 'add_pool_by_external_drive', 3)

        return cli_setting.FailFlag
    else:
        tolog('precondition is failed\n')


def add_pool_raid0(c):

    cli_setting = cli_test_setting()

    # precondition
    try:
        find_pd_id()
    except TypeError:
        tolog('precondition is failed\r\n')
    else:
        cli_setting.setting(c, data, 'add_pool_raid0', 3)

    return cli_setting.FailFlag


def add_pool_raid1(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        find_pd_id()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'add_pool_raid1', 3)

    return cli_setting.FailFlag


def add_pool_raid5(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        find_pd_id()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'add_pool_raid5', 3)

    return cli_setting.FailFlag


def add_pool_raid6(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        find_pd_id()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'add_pool_raid6', 3)

    return cli_setting.FailFlag


def add_pool_raid10(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        find_pd_id()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'add_pool_raid10', 3)

    return cli_setting.FailFlag


def add_pool_raid50(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        find_pd_id()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'add_pool_raid50', 3)

    return cli_setting.FailFlag


def add_pool_raid60(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        find_pd_id()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'add_pool_raid60', 3)

    return cli_setting.FailFlag


def add_pool_default_setting(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        find_pd_id()

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'add_pool_default_setting', 3)

    return cli_setting.FailFlag


def modify_pool_name(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'modify_pool_name', 3)

    return cli_setting.FailFlag


def list_pool(c):

    cli_list = cli_test_list()

    # precondition
    try:
        pdId = find_pd_id()
        # create pool
        server.webapi('post', 'pool', {"name": "raid0_pool", "pds": [pdId[0]], "raid_level": "raid0"})
        server.webapi('post', 'pool', {"name": "raid5_pool", "pds": pdId[1:4], "raid_level": "raid5"})

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_list.list(c, data, 'list_pool')

    return cli_list.FailFlag


def list_verbose_mode_pool(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_verbose_mode_pool')

    return cli_list.FailFlag


def expand_raid0_pool(c):

    cli_setting = cli_test_setting()

    # precondition
    try:
        pdId = find_pd_id()
        # create pool
        server.webapi('post', 'pool', {"name": "expand_raid0_pool", "pds": [pdId[0]], "raid_level": "raid0"})

        time.sleep(3)

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'expand_raid0_pool', 3)

    return cli_setting.FailFlag


def expand_raid1_pool(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        pdId = find_pd_id()
        # create pool
        server.webapi('post', 'pool', {"name": "expand_raid1_pool", "pds": pdId[:2], "raid_level": "raid1"})

        time.sleep(3)

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'expand_raid1_pool', 3)

    return cli_setting.FailFlag


def expand_raid5_pool(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        pdId = find_pd_id()
        # create pool
        server.webapi('post', 'pool', {"name": "expand_raid5_pool", "pds": pdId[:3], "raid_level": "raid5"})

        time.sleep(3)

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'expand_raid5_pool', 3)

    return cli_setting.FailFlag


def expand_raid6_pool(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        pdId = find_pd_id()
        # create pool
        server.webapi('post', 'pool', {"name": "expand_raid6_pool", "pds": pdId[:4], "raid_level": "raid6"})

        time.sleep(3)

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'expand_raid6_pool', 3)

    return cli_setting.FailFlag


def expand_raid10_pool(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        pdId = find_pd_id()
        # create pool
        server.webapi('post', 'pool', {"name": "expand_raid10_pool", "pds": pdId[:4], "raid_level": "raid10"})

        time.sleep(3)

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'expand_raid10_pool', 3)

    return cli_setting.FailFlag


def expand_raid50_pool(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        pdId = find_pd_id()
        # create pool
        server.webapi('post', 'pool', {"name": "expand_raid50_pool", "pds": pdId[:6], "raid_level": "raid50", "axle": 2})

        time.sleep(3)

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'expand_raid50_pool', 3)

    return cli_setting.FailFlag


def expand_raid60_pool(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        pdId = find_pd_id()
        # create pool
        server.webapi('post', 'pool', {"name": "expand_raid60_pool", "pds": pdId[:8], "raid_level": "raid60", "axle": 2})

        time.sleep(3)

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'expand_raid60_pool', 3)

    return cli_setting.FailFlag


def delete_pool(c):

    cli_delete = cli_test_delete()

    # precondition
    try:

        pdId = find_pd_id()
        # create pool
        server.webapi('post', 'pool', {"name": "del_pool_0", "pds": [pdId[0]], "raid_level": "raid0"})

        time.sleep(3)

        server.webapi('post', 'pool', {"name": "del_pool_1", "pds": pdId[1:4], "raid_level": "raid5"})

        time.sleep(3)
        # create volume
        server.webapi('post', 'volume', {'pool_id': 1, 'name': 'del_pool_2', 'capacity': '2GB'})

        time.sleep(3)

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_delete.delete(c, data, 'delete_pool')

    return cli_delete.FailFlag


def invalid_settings_parameter(c):

    cli_failed_test = cli_test_failed_test()

    # precondition
    pdId = find_pd_id()

    if len(pdId) > 3:

        server.webapi('post', 'pool', {"name": "expand_pool", "pds": pdId[:2], "raid_level": "raid1"})

    server.webapi('post', 'rcache/attach', {"pd_list": [5]})

    time.sleep(3)

    cli_failed_test.failed_test(c, data, 'invalid_settings_parameter')

    return cli_failed_test.FailFlag


def invalid_option(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option')

    return cli_failed_test.FailFlag


def missing_parameter(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter')

    # clean up environment
    try:

        find_pd_id()

    except TypeError:

        tolog('to clean up environment is failed\r\n')

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    add_pool_by_external_drive(c)
    add_pool_raid0(c)
    add_pool_raid1(c)
    add_pool_raid5(c)
    add_pool_raid6(c)
    add_pool_raid10(c)
    add_pool_raid50(c)
    add_pool_raid60(c)
    add_pool_default_setting(c)
    modify_pool_name(c)
    list_pool(c)
    list_verbose_mode_pool(c)
    expand_raid0_pool(c)
    expand_raid1_pool(c)
    expand_raid5_pool(c)
    expand_raid6_pool(c)
    expand_raid10_pool(c)
    expand_raid50_pool(c)
    expand_raid60_pool(c)
    delete_pool(c)
    invalid_settings_parameter(c)
    invalid_option(c)
    missing_parameter(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped