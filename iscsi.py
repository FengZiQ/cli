# coding = utf-8
# 2018.01.17

from ssh_connect import ssh_conn
from cli_test import *
from remote import server
import json

data = 'data/iscsi.xlsx'


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


def add_trunk_portal(c):
    # precondition
    precondition()

    server.webapi('post', 'linkaggr', {'ctrl_id': 2, 'master_port': 1, 'trunk_type': 'balance_xor', 'slave_ports': [2]})

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'add_trunk_portal', 1)

    return cli_setting.FailFlag


def add_phy_vlan_portal(c):
    # precondition
    precondition()

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'add_phy_vlan_portal', 1)

    return cli_setting.FailFlag


def list_iscsi(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_iscsi')

    return cli_list.FailFlag


def list_iscsi_by_verbose_mode(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'list_iscsi_by_verbose_mode')

    return cli_list.FailFlag


def mod_iscsi(c):
    # add chap of local type
    server.webapi('post', 'chap', {'name': 'test_iscsi0', 'type': 'local', 'secret': '123456123456', 'node_id': 0})
    time.sleep(3)
    server.webapi('post', 'chap', {'name': 'test_iscsi1', 'type': 'peer', 'secret': '1234561234567', 'node_id': 0})
    time.sleep(3)

    cli_setting = cli_test_setting()

    cli_setting.setting(c, data, 'mod_iscsi', 1)

    return cli_setting.FailFlag


def del_iscsi(c):

    cli_delete = cli_test_delete()

    cli_delete.delete(c, data, 'del_iscsi', 1)

    return cli_delete.FailFlag


def invalid_setting_for_iscsi(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_for_iscsi')

    return cli_failed_test.FailFlag


def invalid_option_for_iscsi(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_iscsi')

    return cli_failed_test.FailFlag


def missing_parameter_for_iscsi(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_for_iscsi')

    clean_up_environment()

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    # add_trunk_portal(c)
    add_phy_vlan_portal(c)
    list_iscsi(c)
    list_iscsi_by_verbose_mode(c)
    mod_iscsi(c)
    del_iscsi(c)
    invalid_setting_for_iscsi(c)
    invalid_option_for_iscsi(c)
    missing_parameter_for_iscsi(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped
