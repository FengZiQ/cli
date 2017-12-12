# --coding = utf-8--
# 2017.12.11

from ssh_connect import ssh_conn
import time, json
from cli_test import *
from remote import server
from find_unconfigured_pd_id import find_pd_id

data = 'data/user.xlsx'





if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()


    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped