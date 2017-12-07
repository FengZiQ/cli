# --coding = utf-8--
# 2017.12.06

from ssh_connect import ssh_conn
import time
import json
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/periodsnap.xlsx'


def precondition():
    pdId = find_pd_id()
    # create pool
    server.webapi('post', 'pool', {"name": "test_periodsnap_pool", "pds": pdId[:3], "raid_level": "raid5"})

    # create volume snapshot
    for i in range(15):
        server.webapi('post', 'volume', {'pool_id': 0, 'name': 'test_periodsnap' + str(i), 'capacity': '2GB'})

    # create nasShare snapshot
    for i in range(10):
        server.webapi('post', 'nasshare', {'pool_id': 0, 'name': 'test_periodsnap_' + str(i), 'capacity': '2GB'})


def clean_up_environment():

    # delete pool
    server.webapi('delete', 'pool/0?force=1')

    # delete period snap
    period_snap_request_nas = server.webapi('get', 'periodicsnap?page=1&type=nasshare')
    period_snap_nas_id = [period_nas["id"] for period_nas in json.loads(period_snap_request_nas["text"])]

    period_snap_request_vol = server.webapi('get', 'periodicsnap?page=1&type=volume')
    period_snap_vol_id = [period_nas["id"] for period_nas in json.loads(period_snap_request_vol["text"])]

    period_snap_id = period_snap_nas_id + period_snap_vol_id

    for id in period_snap_id:
        server.webapi('delete', 'periodicsnap/' + str(id) + '?clear=1')


def add_periodsnap(c):

    cli_setting = cli_test_setting()

    # precondition
    precondition()

    cli_setting.setting(c, data, 'add_periodsnap', 3)

    return cli_setting.FailFlag


def list_periodsnap(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_periodsnap')

    return cli_list.FailFlag


def list_periodsnap_by_verbose_mode(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_periodsnap_by_verbose_mode')

    return cli_list.FailFlag


def mod_periodsnap(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'mod_periodsnap', 3)

    return cli_setting.FailFlag


def del_periodsnap(c):
    pass


def invalid_setting_for_periodsnap(c):
    pass


def invalid_option_for_periodsnap(c):
    pass


def missing_parameter_periodsnap(c):
    pass


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    # add_periodsnap(c)
    list_periodsnap(c)
    # list_periodsnap_by_verbose_mode(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped