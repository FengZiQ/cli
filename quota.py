# coding = utf-8
# 2017.10.23
# 2017.11.13

from ssh_connect import ssh_conn
import time
import json
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/quota.xlsx'


def precondition():
    # disable domain, if enabled domain, to add user or group will happen error
    server.webapi('post', 'domain/leave')

    pdId = find_pd_id()
    # create pool
    server.webapi('post', 'pool', {"name": "test_quota_pool", "pds": pdId[:3], "raid_level": "raid5"})

    # create nasShare
    for i in range(2):
        server.webapi('post', 'nasshare', {'pool_id': 0, 'name': 'test_quota_nas_' + str(i), 'capacity': '2TB'})

    # create clone
    server.webapi('post', 'snapshot', {"name": "test_quota_snap", "type": 'nasshare', "source_id": 0})
    for i in range(2):
        server.webapi('post', 'clone', {"name": "test_quota_clone_" + str(i), "source_id": 0})

    # create nas user
    for i in range(10):
        server.webapi('post', 'dsuser', {"id": 'test_quota_' + str(i), "password": '000000'})

    # create nas group
    for i in range(10):
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
            "id": 'test_quota_group_' + str(i),
            "token": token,
            "page_data": page_data
        })

        server.webapi('post', 'dsgroup/editcancel')


def set_quota(c):
    cli_setting = cli_test_setting()
    # precondition
    precondition()

    cli_setting.setting(c, data, 'set_quota', 3)


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

    # clean up environment
    # delete pool
    server.webapi('delete', 'pool/0?force=1')

    # delete nas user
    for i in range(10):
        server.webapi('delete', 'dsuser/test_quota_' + str(i))

    # delete nas group
    server.webapi('delete', 'dsgroup/test_quota_group')

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    # set_quota(c)
    list_quota(c)
    list_quota_by_verbose_mode(c)
    # refresh_quota(c)
    # mod_quota(c)
    # del_quota(c)
    # invalid_setting_parameter(c)
    # invalid_option(c)
    # missing_parameter(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped