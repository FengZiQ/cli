# -*- coding = utf-8 -*-
# 2018.01.22

from ssh_connect import ssh_conn
from cli_test import *
from remote import server
import json

data = 'data/trunk.xlsx'


def precondition():

    portal_request = server.webapi('get', 'iscsiportal')
    trunk_request = server.webapi('get', 'linkaggr')
    try:
        portal_info = json.loads(portal_request["text"])
        trunk_info = json.loads(trunk_request["text"])

        for portal in portal_info:
            # delete all trunk portal
            server.webapi('delete', 'iscsiportal/' + str(portal['id']))

        for trunk in trunk_info:
            # delete all trunk
            server.webapi('delete', 'linkaggr/' + str(trunk['id']))

    except:
        tolog("precondition is failed\r\n")

    return


def clean_up_environment():

    try:
        chap_request = server.webapi('get', 'chap')

        for chap in json.loads(chap_request['text']):
            server.webapi('delete', 'chap/' + str(chap['id']))

    except:
        tolog("to clean up environment is failed\r\n")

    precondition()

    return


def add_io_trunk(c):
    # precondition
    precondition()

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'add_io_trunk')

    return cli_setting.FailFlag


def add_mgmt_trunk(c):
    # precondition
    precondition()

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'add_mgmt_trunk')

    return cli_setting.FailFlag


def list_trunk(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_trunk')

    return cli_list.FailFlag


def mod_trunk(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'mod_trunk')

    return cli_setting.FailFlag


def del_trunk(c):

    cli_delete = cli_test_delete()

    cli_delete.delete(c, data, 'del_trunk', 1)

    return cli_delete.FailFlag


def invalid_setting_for_trunk(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_trunk')

    return cli_failed_test.FailFlag


def invalid_option_for_trunk(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_trunk')

    return cli_failed_test.FailFlag


def missing_parameter_for_trunk(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_for_trunk')

    clean_up_environment()

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    add_io_trunk(c)
    add_mgmt_trunk(c)
    list_trunk(c)
    mod_trunk(c)
    del_trunk(c)
    invalid_setting_for_trunk(c)
    invalid_option_for_trunk(c)
    missing_parameter_for_trunk(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped
