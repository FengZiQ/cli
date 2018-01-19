# coding = utf-8
# 2017.12.18

from ssh_connect import ssh_conn
from cli_test import *
import json
from remote import server
from to_log import *

data = 'data/chap.xlsx'


def clean_up_environment():

    chap_request = server.webapi('get', 'chap')
    chaps = json.loads(chap_request["text"])

    for chap in chaps:

        server.webapi('delete', 'chap/' + str(chap["id"]))


def add_chap(c):
    # precondition
    try:
        clean_up_environment()
    except:
        tolog('precondition is failed\r\n')

    cli_setting = cli_test_setting()

    cli_setting.setting_need_password(c, data, 'add_chap', 1)

    return cli_setting.FailFlag


def list_chap(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_chap')

    return cli_list.FailFlag


def mod_chap(c):

    tolog('need manual test\r\n')


def del_chap(c):

    cli_delete = cli_test_delete()

    cli_delete.delete(c, data, 'del_chap')

    return cli_delete.FailFlag


def invalid_setting_for_chap(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_chap')

    return cli_failed_test.FailFlag


def invalid_option_for_chap(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_chap')

    return cli_failed_test.FailFlag


def missing_parameter_for_chap(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_for_chap')

    # clean up environment
    try:

        clean_up_environment()

    except TypeError:

        tolog('to clean up environment is failed\r\n')

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    add_chap(c)
    list_chap(c)
    mod_chap(c)
    del_chap(c)
    invalid_setting_for_chap(c)
    invalid_option_for_chap(c)
    missing_parameter_for_chap(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped