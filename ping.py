# coding = utf-8
# 2017.11.03

from ssh_connect import ssh_conn
import time
from cli_test import *
from remote import server

data = 'data/ping.xlsx'


def iscsi_ping(c):

    cli_list = cli_test_list()
    # precondition

    # enable port
    server.webapi('put', 'iscsiport/1_2', {"port_status": 1, "jumbo_frame": 1})
    server.webapi('put', 'iscsiport/2_2', {"port_status": 1, "jumbo_frame": 1})

    # add portal
    server.webapi('post', 'iscsiportal', {
        "if_type": 'Physical',
        "ctrl_id": 2,
        "port_id": 1,
        "tcp_port": 3260,
        "ip_type": 'IPv4',
        "dhcp": 0,
        "primary_ip": '10.84.2.123',
        "primary_ip_mask": '255.255.255.0'
    })
    time.sleep(5)

    cli_list.list(c, data, 'iscsi_ping')

    return cli_list.FailFlag


def mgmt_ping(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'mgmt_ping')

    return cli_list.FailFlag


def fc_ping(c):

    cli_list = cli_test_list()

    """
    precondition:
    need  to configure two fc online port on two equipment
    """
    cli_list.list(c, data, 'fc_ping')

    return cli_list.FailFlag


def invalid_setting_parameter(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_setting_parameter')

    return cli_failed_test.FailFlag


def invalid_option(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option')

    return cli_failed_test.FailFlag


def missing_parameter(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter')

    # clean up environment
    server.webapi('delete', 'iscsiportal/0', {"id": [0]})

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    iscsi_ping(c)
    mgmt_ping(c)
    fc_ping(c)
    invalid_setting_parameter(c)
    invalid_option(c)
    missing_parameter(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped