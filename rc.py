# coding = utf-8
# 2017.11.01

from ssh_connect import ssh_conn
import time
from cli_test import cli_test

data = 'data/rc.xlsx'


def start_rc(c):

    cli_test.need_manual_test()


def list_rc(c):

    cli_test.need_manual_test()


def stop_rc(c):

    cli_test.need_manual_test()


def invalid_setting_parameter(c):

    cli_test.failed_test(c, data, 'invalid_setting_parameter')


def invalid_option(c):

    cli_test.failed_test(c, data, 'invalid_option')


def missing_parameter(c):

    cli_test.failed_test(c, data, 'missing_parameter')


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    invalid_setting_parameter(c)
    invalid_option(c)
    missing_parameter(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped