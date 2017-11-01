# coding = utf-8
# 2017.11.01

from ssh_connect import ssh_conn
import time
from cli_test import cli_test
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/rb.xlsx'


def precondition():
    pdId = find_pd_id()

    # create pool
    server.webapi('post', 'pool', {"name": "test_phy_0", "pds": [pdId[0]], "raid_level": "RAID0"})
    server.webapi('post', 'pool', {"name": "test_phy_1", "pds": pdId[1:4], "raid_level": "raid5"})

    # create spare
    server.webapi('post', 'spare', {"pd_id": pdId[4], "dedicated": 'global', "revertible": 0})
    server.webapi('post', 'spare', {"pd_id": pdId[5], "dedicated": 'dedicated', "revertible": 0, "pool_list": [0]})

    # create cache
    server.webapi('post', 'rcache/attach', {"pd_list": [16]})
    server.webapi('post', 'wcache/attach', {"pd_list": [5, 6], "pool_list": []})















if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()


    # invalid_setting_parameter(c)
    # invalid_option(c)
    # missing_parameter(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped