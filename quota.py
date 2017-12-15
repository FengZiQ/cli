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

    return


def clean_up_environment():
    # clean up environment
    # delete pool
    server.webapi('delete', 'pool/0?force=1')

    # delete nas user
    ds_users_request = server.webapi('get', 'dsusers?page=1&page_size=200')
    ds_users = json.loads(ds_users_request["text"])

    for ds_use in ds_users:

        if ds_use["id"] != 'admin':

            server.webapi('delete', 'dsuser/' + ds_use["id"])

    # delete nas group
    ds_groups_request = server.webapi('get', 'dsgroups?page=1&page_size=200')
    ds_groups = json.loads(ds_groups_request["text"])

    for ds_group in ds_groups:

        if ds_group["id"] != 'users':

            server.webapi('delete', 'dsgroup/' + ds_group["id"])

    return


def set_quota(c):

    clean_up_environment()
    # precondition
    precondition()

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'set_quota', 3)

    return cli_setting.FailFlag


def list_quota(c):
    # precondition
    server.webapi('post', 'dsuser', {"id": 'test_quota_followed', "password": '000000', "grp_name": 'test_quota_group_0'})

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_quota')

    return cli_list.FailFlag


def list_quota_by_verbose_mode(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_quota_by_verbose_mode')

    return cli_list.FailFlag


def refresh_quota(c):

    cli_test_other = cli_test_other_action()

    cli_test_other.other(c, data, 'refresh_quota')

    return cli_test_other.FailFlag


def cancel_quota(c):
    # precondition
    server.webapi('post', 'quota/editcancel/nasshare_0')

    cli_test_other = cli_test_other_action()

    cli_test_other.other(c, data, 'cancel_quota')

    return cli_test_other.FailFlag


def delete_quota(c):
    # precondition
    server.webapi('post', 'quota/editcancel/nasshare_0')

    cli_delete = cli_test_delete()

    cli_delete.delete(c, data, 'delete_quota', 3)

    return cli_delete.FailFlag


def invalid_setting_for_quota(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_quota', 2)

    return cli_failed_test.FailFlag


def invalid_option_for_quota(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_quota')

    return cli_failed_test.FailFlag


def missing_parameter_for_quota(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_for_quota')

    # clean up environment
    clean_up_environment()

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    set_quota(c)
    list_quota(c)
    list_quota_by_verbose_mode(c)
    refresh_quota(c)
    cancel_quota(c)
    delete_quota(c)
    invalid_setting_for_quota(c)
    invalid_option_for_quota(c)
    missing_parameter_for_quota(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped