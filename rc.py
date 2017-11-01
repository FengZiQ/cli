# coding = utf-8
# 2017.11.01

from ssh_connect import ssh_conn
import time
from cli_test import cli_test
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/rc.xlsx'






def invalid_setting_parameter(c):

    cli_test.failed_test(c, data, 'invalid_setting_parameter')


def invalid_option(c):

    cli_test.failed_test(c, data, 'invalid_option')


def missing_parameter(c):

    cli_test.failed_test(c, data, 'missing_parameter')


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()


    # invalid_setting_parameter(c)
    # invalid_option(c)
    # missing_parameter(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped