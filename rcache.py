# coding = utf-8
# 2017.11.03

from ssh_connect import ssh_conn
import time, json
from cli_test import cli_test
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/rcache.xlsx'


def add_rcache_by_one_pd(c):
    # precondition
    find_pd_id()

    cli_test.setting(c, data, 'add_rcache_by_one_pd', 1)


def add_rcache_by_multiple_pd(c):
    # precondition
    pdId = find_pd_id()

    server.webapi('post', 'pool', {"name": "test_cache_pool", "pds": pdId[:3], "raid_level": "raid5"})

    cli_test.setting(c,  data, 'add_rcache_by_multiple_pd', 1)


def list_rcache(c):

    cli_test.list(c, data, 'list_rcache')


def def_cache(c):

    cli_test.delete(c, data, 'def_cache')


def invalid_setting_parameter(c):
    # precondition
    server.webapi('post', 'rcache/detach', {"pd_list": [5, 6, 16]})
    # server.webapi('post', 'rcache/attach', {"pd_list": [5]})
    cli_test.failed_test(c, data, 'invalid_setting_parameter')


def invalid_option(c):

    cli_test.failed_test(c, data, 'invalid_option')


def missing_parameter(c):

    cli_test.failed_test(c, data, 'missing_parameter')


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    # add_rcache_by_one_pd(c)
    add_rcache_by_multiple_pd(c)

    # invalid_setting_parameter(c)
    # invalid_option(c)
    # missing_parameter(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped