# coding = utf-8
# 2017.12.25

from ssh_connect import ssh_conn
import time
import json
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/replication.xlsx'


def precondition():
    # stop all replication
    replica_request = server.webapi('get', 'replica')

    if isinstance(replica_request, dict):

        try:

            for replica in json.loads(replica_request["text"]):

                server.webapi('post', 'replicaloc/' + str(replica["src_id"]) + '/stop')

                time.sleep(3)

        except (TypeError, KeyError):

            tolog('precondition is failed\r\n')

        else:

            pdId = find_pd_id()
            # create pool

            if len(pdId) > 0:

                server.webapi('post', 'pool', {"name": "T_replication_0", "pds": pdId[:3], "raid_level": "raid5"})

                server.webapi('post', 'pool', {"name": "T_replication_1", "pds": pdId[3:6], "raid_level": "raid5"})

                server.webapi('post', 'pool', {"name": "T_replication_2", "pds": [pdId[6]], "raid_level": "raid0"})

                server.webapi('post', 'pool', {"name": "T_replication_3", "pds": [15], "raid_level": "raid0"})

            else:

                tolog('precondition is failed\r\n')

            # create source volume
            for i in range(6):

                if i <= 1:
                    server.webapi('post', 'volume', {
                        'pool_id': 2,
                        'name': 'T_replication_vol_' + str(i),
                        'capacity': '900GB',
                        'thin_prov': i
                    })

                elif i == 2 or i == 3:
                    server.webapi('post', 'volume', {
                        'pool_id': 0,
                        'name': 'T_replication_vol_' + str(i),
                        'capacity': '4GB',
                        'block': '64kb',
                        'sector': '4kb',
                        'compress': 'gzip',
                        'sync': 'disabled',
                        'logbias': 'throughput'
                    })

                elif i == 4 or i == 5:

                    server.webapi('post', 'volume', {
                        'pool_id': 1,
                        'name': 'T_replication_vol_' + str(i),
                        'capacity': '1GB'
                    })

    return


def clean_up_environment():
    # stop all replication
    replica_request = server.webapi('get', 'replica')
    if isinstance(replica_request, dict):

        try:

            for replica in json.loads(replica_request["text"]):

                server.webapi('post', 'replicaloc/' + str(replica["src_id"]) + '/stop')

                time.sleep(3)

        except (TypeError, KeyError):

            tolog('to clean up environment is failed\r\n')

        else:

            for i in range(3):

                server.webapi('delete', 'pool/' + str(i) + '?force=1')

    # delete pool
    find_pd_id()

    # delete initiator
    init_request = server.webapi('get', 'initiator')
    if isinstance(init_request, dict):

        try:

            for init in json.loads(init_request["text"]):

                server.webapi('delete', 'initiator/' + str(init["id"]))

        except (TypeError, KeyError):

            tolog('to clean up environment is failed\r\n')

    return


def start_replication(c):

    # precondition
    precondition()

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'start_replication', 3)

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


def list_replication(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_replication')

    return cli_list.FailFlag


def list_replication_by_verbose(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_replication_by_verbose')

    return cli_list.FailFlag


def stop_replication(c):

    cli_delete = cli_test_delete()

    cli_delete.delete(c, data, 'stop_replication', 1)

    return cli_delete.FailFlag


def pause_replication(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'pause_replication', 1)

    return cli_setting.FailFlag


def resume_replication(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'resume_replication', 1)

    return cli_setting.FailFlag


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

    # clean up environment
    clean_up_environment()

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    start_replication(c)
    forbidden_action(c)
    list_replication(c)
    list_replication_by_verbose(c)
    stop_replication(c)
    pause_replication(c)
    resume_replication(c)
    help_replication(c)
    invalid_setting_for_replication(c)
    invalid_option_for_replication(c)
    missing_parameter_replication(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped