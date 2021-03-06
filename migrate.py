# coding = utf-8
# 2017.12.25

from ssh_connect import ssh_conn
import time
import json
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id
from remote_migrate import precondition_for_migrate, clean_up

data = 'data/migrate.xlsx'


def precondition_1():
    try:
        # stop all migrate
        vol_request = server.webapi('get', 'volume?page=1&page_size=100')

        if isinstance(vol_request, dict):

            for vol in json.loads(vol_request["text"]):

                if 'adv_role' in vol.keys() and vol['adv_role'] == 'Source':

                    server.webapi('post', 'migrate/' + str(vol['id']) + '/stop', {"location": 1})

        pdId = find_pd_id()

        if len(pdId) > 0:
            # create pool
            server.webapi('post', 'pool', {"name": "T_migrate_0", "pds": pdId[:3], "raid_level": "raid5", 'ctrl_id': 1})

            server.webapi('post', 'pool', {"name": "T_migrate_1", "pds": pdId[3:6], "raid_level": "raid5", 'ctrl_id': 1})

            server.webapi('post', 'pool', {"name": "T_migrate_2", "pds": [pdId[6]], "raid_level": "raid0", 'ctrl_id': 1})

            server.webapi('post', 'pool', {"name": "T_migrate_3", "pds": [15], "raid_level": "raid0", 'ctrl_id': 1})

            # create source volume
            for i in range(10):

                if i <= 1:
                    server.webapi('post', 'volume', {
                        'pool_id': 2,
                        'name': 'T_migrate_vol_' + str(i),
                        'capacity': '900GB',
                        'thin_prov': i
                    })

                elif i == 2 or i == 3:
                    server.webapi('post', 'volume', {
                        'pool_id': 0,
                        'name': 'T_migrate_vol_' + str(i),
                        'capacity': '1GB',
                        'block': '64kb',
                        'sector': '4kb',
                        'compress': 'gzip',
                        'sync': 'disabled',
                        'logbias': 'throughput',
                        'thin_prov': 0
                    })

                else:

                    server.webapi('post', 'volume', {
                        'pool_id': 1,
                        'name': 'T_migrate_vol_' + str(i),
                        'capacity': '2GB',
                        'thin_prov': 0
                    })

                server.webapi('post', 'volume/' + str(i) + '/export')

            server.webapi('post', 'snapshot', {"name": "test_migrate1", "type": 'volume', "source_id": 2})

        return

    except ():

        tolog('precondition is failed\r\n')


def precondition_2():
    # stop all migrate
    vol_request = server.webapi('get', 'volume?page=1&page_size=100')

    if isinstance(vol_request, dict):

        for vol in json.loads(vol_request["text"]):

            if 'adv_role' in vol.keys() and vol['adv_role'] == 'Source':
                server.webapi('post', 'migrate/' + str(vol['id']) + '/stop', {"location": 1})

    server.webapi('post', 'snapshot', {"name": "test_migrate2", "type": 'volume', "source_id": 2})

    return


def clean_up_environment():
    clean_up()

    try:
        # stop all migrate
        vol_request = server.webapi('get', 'volume?page=1&page_size=100')

        if isinstance(vol_request, dict):

            for vol in json.loads(vol_request["text"]):

                if 'adv_role' in vol.keys() and vol['adv_role'] == 'Source':
                    server.webapi('post', 'migrate/' + str(vol['id']) + '/stop', {"location": 2})

        # delete pool
        find_pd_id()

        # delete initiator
        init_request = server.webapi('get', 'initiator')

        if isinstance(init_request, dict):

            for init in json.loads(init_request["text"]):

                server.webapi('delete', 'initiator/' + str(init["id"]))

        return

    except ():

        tolog('to clean up environment is failed\r\n')


def start_local_migrate(c):

    # precondition
    precondition_1()

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'start_local_migrate', 3)

    return cli_setting.FailFlag


def start_remote_migrate(c):
    # precondition
    precondition_2()
    precondition_for_migrate()

    for i in range(2, 6):

        server.webapi('post', 'volume/' + str(i) + '/export')

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'start_remote_migrate', 3)

    return cli_setting.FailFlag


def forbidden_action(c):
    # precondition
    # create initiator
    server.webapi('post', 'initiator', {"type": 'iscsi', "name": 'test.abc.com'})
    # enable lunmap
    server.webapi('post', 'lunmap/status', {"is_enable": 1})

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'forbidden_action')

    return cli_failed_test.FailFlag


def stop_migrate(c):

    cli_delete = cli_test_delete()

    cli_delete.delete(c, data, 'stop_migrate', 1)

    return cli_delete.FailFlag


def help_migrate(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'help_migrate')

    return cli_list.FailFlag


def invalid_setting_for_migrate(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_migrate')

    return cli_failed_test.FailFlag


def invalid_option_for_migrate(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_migrate')

    return cli_failed_test.FailFlag


def missing_parameter_migrate(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_migrate')

    # clean up environment
    clean_up_environment()

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    start_local_migrate(c)
    stop_migrate(c)
    help_migrate(c)
    invalid_setting_for_migrate(c)
    invalid_option_for_migrate(c)
    missing_parameter_migrate(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped