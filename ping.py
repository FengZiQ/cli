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
    server.webapi('put', 'iscsiport/1_2', {"port_status": 1, "jumbo_frame": 1})
    server.webapi('put', 'iscsiport/2_2', {"port_status": 1, "jumbo_frame": 1})

    cli_test.list(c, data, 'iscsi_ping')


def mgmt_ping(c):

    cli_test.list(c, data, 'mgmt_ping')


def fc_ping(c):
    """
    precondition:
    need  to configure two fc online port on two equipment
    """
    cli_test.list(c, data, 'fc_ping')


def invalid_setting_parameter(c):

    cli_test.failed_test(c, data, 'invalid_setting_parameter')


def invalid_option(c):

    cli_test.failed_test(c, data, 'invalid_option')


def missing_parameter(c):

    cli_test.failed_test(c, data, 'missing_parameter')


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