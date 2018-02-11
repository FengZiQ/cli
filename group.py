# coding = utf-8
# 2017.10.10
# 2017.11.15

from ssh_connect import ssh_conn
import json
from cli_test import *
from remote import server

data = 'data/group.xlsx'


def add_group_and_verify_name(c):
    # disable domain, if enabled domain, to add user or group will happen error
    server.webapi('post', 'domain/leave')

    clean_up_environment()

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'add_group_and_verify_name', 3)

    return cli_setting.FailFlag


def add_group_and_user(c):
    cli_setting = cli_test_setting()

    # precondition: create DSUser
    for i in range(10):
        server.webapi('post', 'dsuser', {"id": 'test_group_' + str(i), "password": '123456'})

    cli_setting.setting(c, data, 'add_group_and_user', 3)

    return cli_setting.FailFlag


def add_user_into_group(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'add_user_into_group', 3)

    return cli_setting.FailFlag


def list_group(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_group')

    return cli_list.FailFlag


def list_group_by_verbose_mode(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_group_by_verbose_mode')

    return cli_list.FailFlag


def modify_group(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'modify_group', 3)

    return cli_setting.FailFlag


def delete_user_from_group(c):

    cli_delete = cli_test_delete()

    cli_delete.delete_need_confirm(c, data, 'delete_user_from_group', 3)

    return cli_delete.FailFlag


def delete_group(c):

    cli_delete = cli_test_delete()

    cli_delete.delete_need_confirm(c, data, 'delete_group', 3)

    return cli_delete.FailFlag


def invalid_setting_for_group(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_group')

    return cli_failed_test.FailFlag


def invalid_option_for_group(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_group')

    return cli_failed_test.FailFlag


def missing_parameter_for_group(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_for_group')

    # clean up environment
    try:
        clean_up_environment()

    except TypeError:
        tolog('to clean up environment is failed\r\n')

    return cli_failed_test.FailFlag


def clean_up_environment():
    # delete nas user
    users = server.webapi('get', 'dsusers?page=1&page_size=500')
    if isinstance(users, dict):
        user_info = json.loads(users["text"])[0]['user_list']
        for user in user_info:
            server.webapi('delete', 'dsuser/' + user["id"])

    # delete group
    groups = server.webapi('get', 'dsgroups?page=1&page_size=500')
    if isinstance(groups, dict):
        groups_info = json.loads(groups["text"])[0]['group_list']
        for group in groups_info:
            server.webapi('delete', 'dsgroup/' + group["id"])


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    clean_up_environment()
    # add_group_and_verify_name(c)
    # add_group_and_user(c)
    # add_user_into_group(c)
    # list_group(c)
    # list_group_by_verbose_mode(c)
    # modify_group(c)
    # delete_user_from_group(c)
    # delete_group(c)
    # invalid_setting_for_group(c)
    # invalid_option_for_group(c)
    # missing_parameter_for_group(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped