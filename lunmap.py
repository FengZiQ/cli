# -*- coding = utf-8 -*-
# 2018.01.23

from ssh_connect import ssh_conn
from cli_test import *
from remote import server
import json
from find_unconfigured_pd_id import find_pd_id

data = 'data/lunmap.xlsx'


def precondition():
    try:
        clean_up_environment()

        pdId = find_pd_id()
        # create pool
        server.webapi('post', 'pool', {"name": "T_lunMap_P0", "pds": pdId[6:9], "raid_level": "raid5"})

        # create volume and export it
        for i in range(3):
            server.webapi('post', 'volume', {'pool_id': 0, 'name': 'T_lunMap_V' + str(i), 'capacity': '100GB'})
            server.webapi('post', 'volume/' + str(i) + '/export')

        # create snapshot and export it
        for i in range(3):
            server.webapi('post', 'snapshot', {"name": "T_lunMap_SS" + str(i), "type": 'volume', "source_id": 2})
            server.webapi('post', 'snapshot/' + str(i) + '/export')

        # create clone and export it
        for i in range(3):
            server.webapi('post', 'clone', {"name": "T_lunMap_C" + str(i), "source_id": 2})
            server.webapi('post', 'clone/' + str(i) + '/export')

        # create initiator
        for i in range(4):
            server.webapi('post', 'initiator', {'type': 'iSCSI', 'name': 'T.com' + str(i)})
            server.webapi('post', 'initiator', {'type': 'fc', 'name': '00-11-22-33-00-00-11-1' + str(i)})
    except:
        tolog("precondition is failed\r\n")

    return


def clean_up_environment():

    initiator_request = server.webapi('get', 'initiator')

    try:
        initiator_info = json.loads(initiator_request["text"])
        for initiator in initiator_info:
            # delete all initiator
            server.webapi('delete', 'initiator/' + str(initiator['id']))
        # delete pool
        find_pd_id()
    except:
        tolog("precondition is failed\r\n")

    return


def enable_lmm(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'enable_lmm')

    return cli_setting.FailFlag


def add_lunmap(c):
    # precondition
    precondition()

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'add_lunmap')

    return cli_setting.FailFlag


def addun_lunmap(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'addun_lunmap')

    return cli_setting.FailFlag


def list_lunmap(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_lunmap')

    return cli_list.FailFlag


def del_lunmap(c):

    cli_delete = cli_test_delete()

    cli_delete.delete(c, data, 'del_lunmap', 5)

    return cli_delete.FailFlag


def dellun_lunmap(c):

    cli_delete = cli_test_delete()

    cli_delete.delete(c, data, 'dellun_lunmap')

    return cli_delete.FailFlag


def disable_lmm(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'disable_lmm')

    return cli_setting.FailFlag


def invalid_setting_for_lunmap(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_lunmap')

    return cli_failed_test.FailFlag


def invalid_option_for_lunmap(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_lunmap')

    return cli_failed_test.FailFlag


def missing_parameter_for_lunmap(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_for_lunmap')

    # clean up environment
    clean_up_environment()

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    enable_lmm(c)
    add_lunmap(c)
    addun_lunmap(c)
    list_lunmap(c)
    del_lunmap(c)
    dellun_lunmap(c)
    disable_lmm(c)
    invalid_setting_for_lunmap(c)
    invalid_option_for_lunmap(c)
    missing_parameter_for_lunmap(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped
