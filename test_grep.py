# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn




command = ["about", "battery", "bbm", "bga", "buzz",  "chap", "clone", "ctrl", "date", "encldiag",
                "enclosure", "event", "export", "factorydefaul", "fc", "import", "initiator", "iscsi",
                "isns", "logout", "lunmap", "maintenance", "net", "ntp", "password", "pcie", "perfstats",
                "phydrv", "ping", "pool", "ptiflash", "rb", "rc", "rcache", "sc", "session", "shutdown",
                "smart", "snapshot", "spare", "stats", "subscription", "subsys", "swmgt", "sync",
                "topology", "trunk", "ups", "user", "volume", "wcache"]