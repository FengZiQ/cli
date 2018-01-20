# coding = utf-8
# 2018.01.12

from ssh_connect import ssh_conn
from cli_test import *
from remote import server
import json

data = 'data/net.xlsx'


def precondition():

    portal_request = server.webapi('get', 'iscsiportal')
    trunk_request = server.webapi('get', 'linkaggr')
    try:
        portal_info = json.loads(portal_request["text"])
        trunk_info = json.loads(trunk_request["text"])

        for portal in portal_info:
            # delete all iscsi portal
            server.webapi('delete', 'iscsiportal/' + str(portal['id']))

        for trunk in trunk_info:
            # delete all trunk
            server.webapi('delete', 'linkaggr/' + str(trunk['id']))

    except:
        tolog("precondition is failed\r\n")

    server.webapi('post', 'iscsiportal', {
        'if_type': 'Physical',
        'port_type': 1,
        'ctrl_id': 2,
        'port_id': 1,
        'tcp_port': 4,
        'ip_type': 'IPv4',
        'dhcp': 1
    })

    return


def clean_up_environment():

    portal_request = server.webapi('get', 'iscsiportal')

    try:
        portal_info = json.loads(portal_request["text"])

        for portal in portal_info:
            # delete all iscsi portal
            server.webapi('delete', 'iscsiportal/' + str(portal['id']))

    except:
        tolog("precondition is failed\r\n")


def need_manual_test(c):

    tolog('those cases need manual test\r\n')


def list_net(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_net')

    return cli_list.FailFlag


def list_net_by_verbose_mode(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_net_by_verbose_mode')

    return cli_list.FailFlag


def disable_enable_net(c):

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'disable_enable_net')

    return cli_setting.FailFlag


def modify_net(c):
    # precondition
    precondition()

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'modify_net')

    return cli_setting.FailFlag


def invalid_setting_for_net(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_net')

    return cli_failed_test.FailFlag


def invalid_option_for_net(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_net')

    return cli_failed_test.FailFlag


def missing_parameter_for_net(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_for_net')

    # clean up environment
    clean_up_environment()

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    list_net(c)
    list_net_by_verbose_mode(c)
    disable_enable_net(c)
    modify_net(c)
    invalid_setting_for_net(c)
    invalid_option_for_net(c)
    missing_parameter_for_net(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped
