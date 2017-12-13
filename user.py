# --coding = utf-8--
# 2017.12.11

from ssh_connect import ssh_conn
import json
from cli_test import *
from remote import server
from send_cmd import *

data = 'data/user.xlsx'


def precondition():
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
        "id": 'test_users',
        "token": token,
        "page_data": page_data
    })

    server.webapi('post', 'dsgroup/editcancel')


def clean_up_environment():
    # delete management users
    user_request = server.webapi('get', 'user')
    users = json.loads(user_request["text"])

    for user in users:
        if user["id"] != 'administrator':
            server.webapi('delete', 'user/' + user["id"])

    # delete snmp users
    snmp_user_request = server.webapi('get', 'snmpuser')
    snmp_users = json.loads(snmp_user_request["text"])

    for snmp_user in snmp_users:
        server.webapi('delete', 'snmpuser/' + snmp_user["id"])

    # delete nas users
    nas_user_request = server.webapi('get', 'dsusers?page=1&page_size=100')
    nas_users = json.loads(nas_user_request["text"])

    for nas_user in nas_users:
        if nas_user["id"] != 'admin':
            server.webapi('delete', 'dsuser/' + nas_user["id"])

    return
            

def add_mgmt_user(c):
    # precondition: clear all of user
    clean_up_environment()

    cli_setting = cli_test_setting()

    cli_setting.setting_need_password(c, data, 'add_mgmt_user', 1)

    return cli_setting.FailFlag


def mod_mgmt_user(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'mod_mgmt_user', 1)

    return cli_setting.FailFlag


def add_snmp_user(c):

    cli_setting = cli_test_setting()

    cli_setting.setting_need_double_password(c, data, 'add_snmp_user', 1)

    return cli_setting.FailFlag


def mod_snmp_user(c):

    cli_setting = cli_test_setting()

    cli_setting.setting_need_double_password(c, data, 'mod_snmp_user', 1)

    return cli_setting.FailFlag


def add_nas_user(c):
    # precondition: create group test_users
    precondition()

    cli_setting = cli_test_setting()

    cli_setting.setting_need_password(c, data, 'add_nas_user', 1)

    return cli_setting.FailFlag


def mod_nas_user(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'mod_nas_user', 1)

    return cli_setting.FailFlag


def list_user(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_user')

    return cli_list.FailFlag


def list_user_by_verbose_mode(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_user_by_verbose_mode')

    return cli_list.FailFlag


def del_user(c):

    cli_delete = cli_test_delete()

    cli_delete.delete(c, data, 'del_user')

    return cli_delete.FailFlag


def invalid_setting_for_user(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_user')

    return cli_failed_test.FailFlag


def invalid_option_for_user(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_user')

    return cli_failed_test.FailFlag


def missing_parameter_for_user(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_for_user')

    # clean up environment
    clean_up_environment()

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    add_mgmt_user(c)
    mod_mgmt_user(c)
    add_snmp_user(c)
    mod_snmp_user(c)
    add_nas_user(c)
    mod_nas_user(c)
    list_user(c)
    list_user_by_verbose_mode(c)
    del_user(c)
    invalid_setting_for_user(c)
    invalid_option_for_user(c)
    missing_parameter_for_user(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped