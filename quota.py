# coding = utf-8
# 2017.10.23

from ssh_connect import ssh_conn
import time
import json
from cli_test import cli_test
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/quota.xlsx'

def precondition():
    pdId = find_pd_id('4TB')
    # create pool
    server.webapi('post', 'pool', {"name": "test_quota", "pds": pdId, "raid_level": "raid5"})

    # create nasShare
    server.webapi('post', 'nasshare', {'pool_id': 0, 'name': 'test_quota_nas', 'capacity': '2GB'})

    # create clone
    server.webapi('post', 'snapshot', {"name": "test_quota_snap", "type": 'nasshare', "source_id": 0})
    server.webapi('post', 'clone', {"name": "test_quota_clone", "source_id": 0})

    # create nas user
    for i in range(10):
        server.webapi('post', 'dsuser', {"id": 'test_quota_' + str(i), "password": '000000'})

    # create nas group
    server.webapi('post', 'dsgroup/editcancel')
    step1 = server.webapi('post', 'dsgroup/editbegin', {
        "page": 1,
        "page_size": 20
    })

    token = json.loads(step1["text"])[0]["token"]
    get_page_data = json.loads(step1["text"])[0]["page_data"]
    page_data = [[0, uid["uid"]] for uid in get_page_data]

    server.webapi('post', 'dsgroup/editnext', {
        "page": 1,
        "page_size": 20,
        "token": token,
        "page_data": page_data
    })
    server.webapi('post', 'dsgroup/editsave', {
        "id": 'test_quota_group',
        "token": token,
        "page_data": page_data
    })

    server.webapi('post', 'dsgroup/editcancel')


def add_quota(c):
    # precondition
    precondition()

    cli_test.setting(c, data, 'add_quota', 3)


def list_quota(c):

    cli_test.list(c, data, 'list_quota')


def list_quota_by_verbose_mode(c):

    cli_test.list(c, data, 'list_quota_by_verbose_mode')


def refresh_quota(c):

    cli_test.other(c, data, 'refresh_quota')


def mod_quota(c):

    cli_test.setting(c, data, 'mod_quota', 3)


def del_quota(c):

    cli_test.delete(c, data, 'del_quota')


def invalid_setting_parameter(c):

    cli_test.failed_test(c, data, 'invalid_setting_parameter', 2)


def invalid_option(c):

    cli_test.failed_test(c, data, 'invalid_option')


def missing_parameter(c):

    cli_test.failed_test(c, data, 'missing_parameter')


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    add_quota(c)
    list_quota(c)
    list_quota_by_verbose_mode(c)
    refresh_quota(c)
    mod_quota(c)
    del_quota(c)
    invalid_setting_parameter(c)
    invalid_option(c)
    missing_parameter(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped