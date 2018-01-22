# -*- coding = utf-8 -*-
# 2018.01.22

from ssh_connect import ssh_conn
from cli_test import *
from remote import server
import json

data = 'data/initiator.xlsx'


def precondition():

    portal_request = server.webapi('get', 'iscsiportal')
    initiator_request = server.webapi('get', 'linkaggr')
    try:
        portal_info = json.loads(portal_request["text"])
        initiator_info = json.loads(initiator_request["text"])

        for portal in portal_info:
            # delete all initiator portal
            server.webapi('delete', 'iscsiportal/' + str(portal['id']))

        for initiator in initiator_info:
            # delete all initiator
            server.webapi('delete', 'linkaggr/' + str(initiator['id']))

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


def add_io_initiator(c):
    # precondition
    precondition()

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'add_io_initiator')

    return cli_setting.FailFlag


def list_initiator(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_initiator')

    return cli_list.FailFlag


def del_initiator(c):

    cli_delete = cli_test_delete()

    cli_delete.delete(c, data, 'del_initiator', 1)

    return cli_delete.FailFlag


def invalid_setting_for_initiator(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_initiator')

    return cli_failed_test.FailFlag


def invalid_option_for_initiator(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_initiator')

    return cli_failed_test.FailFlag


def missing_parameter_for_initiator(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_for_initiator')

    clean_up_environment()

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    add_initiator(c)
    list_initiator(c)
    del_initiator(c)
    invalid_setting_for_initiator(c)
    invalid_option_for_initiator(c)
    missing_parameter_for_initiator(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped
