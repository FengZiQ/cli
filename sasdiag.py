# -*- coding = utf-8 -*-
# 2018.02.08

from ssh_connect import ssh_conn
from cli_test import *


data = 'data/sasdiag.xlsx'


def discover_sasdiag(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'discover_sasdiag')

    return cli_list.FailFlag


def errorlog_sasdiag(c):

    cli_list = cli_test_list()

    cli_list.list(c, data, 'errorlog_sasdiag')

    return cli_list.FailFlag


def clearerrlog_sasdiag(c):

    cli_list = cli_test_other_action()

    cli_list.other(c, data, 'clearerrlog_sasdiag')

    return cli_list.FailFlag


def invalid_parameter_sasdiag(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_parameter_sasdiag')

    return cli_failed_test.FailFlag


def invalid_option_for_sasdiag(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'invalid_option_for_sasdiag')

    return cli_failed_test.FailFlag


def missing_parameter_sasdiag(c):

    cli_failed_test = cli_test_failed_test()

    cli_failed_test.failed_test(c, data, 'missing_parameter_sasdiag')

    return cli_failed_test.FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    discover_sasdiag(c)
    errorlog_sasdiag(c)
    clearerrlog_sasdiag(c)
    invalid_parameter_sasdiag(c)
    invalid_option_for_sasdiag(c)
    missing_parameter_sasdiag(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped