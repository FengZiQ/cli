# coding = utf-8
# 2017.10.25
# 2017.11.10

from ssh_connect import ssh_conn
import time
import json
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/acl.xlsx'


def precondition():
    pdId = find_pd_id()
    # create pool
    server.webapi('post', 'pool', {"name": "test_acl_pool", "pds": pdId[:3], "raid_level": "raid5"})

    # create nasShare
    for i in range(2):
        server.webapi('post', 'nasshare', {'pool_id': 0, 'name': 'test_acl_nas_' + str(i), 'capacity': '2GB'})

    # create clone
    server.webapi('post', 'snapshot', {"name": "test_acl_snap", "type": 'nasshare', "source_id": 0})
    for i in range(2):
        server.webapi('post', 'clone', {"name": "test_acl_clone_" + str(i), "source_id": 0})

    # create nas user
    for i in range(10):
        server.webapi('post', 'dsuser', {"id": 'test_acl_' + str(i), "password": '000000'})

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
            "id": 'test_acl_group_' + str(i),
            "token": token,
            "page_data": page_data
        })

        server.webapi('post', 'dsgroup/editcancel')


def clean_up_environment():
    # clean up environment
    # delete pool
    server.webapi('delete', 'pool/0?force=1')

    # delete nas user
    for i in range(10):
        server.webapi('delete', 'dsuser/test_acl_' + str(i))

    # delete nas group
    for i in range(10):
        server.webapi('delete', 'dsgroup/test_acl_group_' + str(i))


def set_acl(c):
    # precondition
    precondition()

    server.webapi('post', 'acl/editcancel/nasshare_0')
    server.webapi('post', 'acl/editcancel/clone_0')

    cli_setting.setting(c, data, 'set_acl', 5)

    return cli_setting.FailFlag


def list_acl(c):

    cli_list.list(c, data, 'list_acl')

    return cli_list.FailFlag


def list_acl_by_verbose_mode(c):

    cli_list.list(c, data, 'list_acl_by_verbose_mode')

    return cli_list.FailFlag


def refresh_acl(c):

    cli_other_action.other(c, data, 'refresh_acl')

    return cli_other_action.FailFlag


def acl_unset(c):

    cli_delete.delete(c, data, 'acl_unset', 3)

    return cli_delete.FailFlag


def clear_acl(c):
    # precondition
    server.webapi('post', 'acl/editcancel/nasshare_0')
    server.webapi('post', 'acl/editcancel/clone_0')

    cli_delete.delete(c, data, 'clear_acl', 3)

    return cli_delete.FailFlag


def cancel_acl(c):

    cli_other_action.other(c, data, 'cancel_acl')

    return cli_other_action.FailFlag


def invalid_setting_parameter(c):
    # precondition
    server.webapi('post', 'acl/editcancel/nasshare_0')
    server.webapi('post', 'acl/editcancel/clone_0')

    cli_failed_test.failed_test(c, data, 'invalid_setting_parameter', 1)

    return cli_failed_test.FailFlag


def invalid_option(c):

    cli_failed_test.failed_test(c, data, 'invalid_option')

    return cli_failed_test.FailFlag


def missing_parameter(c):

    cli_failed_test.failed_test(c, data, 'missing_parameter')

    # clean_up_environment
    clean_up_environment()

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    set_acl(c)
    list_acl(c)
    list_acl_by_verbose_mode(c)
    refresh_acl(c)
    acl_unset(c)
    clear_acl(c)
    cancel_acl(c)
    invalid_setting_parameter(c)
    invalid_option(c)
    missing_parameter(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped