# coding = utf-8
# 2017.11.03

from ssh_connect import ssh_conn
import time
from cli_test import cli_test
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/ping.xlsx'


def iscsi_ping(c):
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

    cli_test.list(c, data, 'iscsi_ping')


def mgmt_ping(c):

    cli_test.list(c, data, 'mgmt_ping')

    return cli_test.FailFlag


def fc_ping(c):
    """
    precondition:
    need  to configure two fc online port on two equipment
    """
    cli_test.list(c, data, 'fc_ping')

    return cli_test.FailFlag


def invalid_setting_parameter(c):

    cli_test.failed_test(c, data, 'invalid_setting_parameter')

    return cli_test.FailFlag


def invalid_option(c):

    cli_test.failed_test(c, data, 'invalid_option')

    return cli_test.FailFlag


def missing_parameter(c):

    cli_test.failed_test(c, data, 'missing_parameter')

    # clean up environment
    server.webapi('delete', 'iscsiportal/0', {"id": [0]})

    return cli_test.FailFlag


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