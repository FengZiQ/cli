# coding = utf-8
# 2017.9.17

from ssh_connect import ssh_conn
import time
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/volume.xlsx'


def addVolume(c):

    cli_setting = cli_test_setting()

    # precondition
    try:

        pdId = find_pd_id('4TB')
        # create pool
        server.webapi('post', 'pool', {"name": "test_volume", "pds": pdId[:3], "raid_level": "raid5"})

    except TypeError:

        tolog('precondition is failed\r\n')

    else:

        cli_setting.setting(c, data, 'addVolume', 3)

    return cli_setting.FailFlag


def listVolume(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'listVolume')

    return cli_list.FailFlag


def listVolume_by_verbose_mode(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'listVolume_by_verbose_mode')

    return cli_list.FailFlag


def modVolume(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'modVolume', 3)

    return cli_setting.FailFlag


def exportVolume(c):

    cli_setting = cli_test_setting()

    # precondition
    server.webapi('post', 'volume/0/unexport')

    cli_setting.setting(c, data, 'exportVolume', 3)

    return cli_setting.FailFlag


def unexportVolume(c):

    cli_setting = cli_test_setting()

    # precondition
    server.webapi('post', 'volume/0/export')

    cli_setting.setting(c, data, 'unexportVolume', 3)

    return cli_setting.FailFlag


def invalidParameter(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalidParameter')

    return cli_failed_test.FailFlag


def invalidOption(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalidOption')

    return cli_failed_test.FailFlag


def missingParameter(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missingParameter')

    return cli_failed_test.FailFlag


def deleteVolume(c):

    cli_delete = cli_test_delete()

    # precondition: create volume snapshot
    server.webapi('post', 'snapshot', {"name": "test_volume_snap", "type": 'volume', "source_id": 1})

    cli_delete.delete(c, data, 'deleteVolume', 3)

    # clean up environment
    try:

        find_pd_id()

    except TypeError:

        tolog('to clean up environment is failed\r\n')

    return cli_delete.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    addVolume(c)
    listVolume(c)
    listVolume_by_verbose_mode(c)
    modVolume(c)
    exportVolume(c)
    unexportVolume(c)
    invalidParameter(c)
    invalidOption(c)
    missingParameter(c)
    deleteVolume(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped