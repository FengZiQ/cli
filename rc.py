# coding = utf-8
# 2017.11.01

from ssh_connect import ssh_conn
import time
from cli_test import *

data = 'data/rc.xlsx'


def start_rc(c):

    pass


def list_rc(c):

    pass


def stop_rc(c):

    pass


def invalid_setting_parameter(c):

    cli_failed_test.failed_test(c, data, 'invalid_setting_parameter')

    return cli_failed_test.FailFlag


def invalid_option(c):

    cli_failed_test.failed_test(c, data, 'invalid_option')

    return cli_failed_test.FailFlag


def missing_parameter(c):

    cli_failed_test.failed_test(c, data, 'missing_parameter')

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    invalid_setting_parameter(c)
    invalid_option(c)
    missing_parameter(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped