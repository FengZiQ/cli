# coding = utf-8
# 2017.9.28

from send_cmd import *


def pd_id(c):

    tolog('==================================precondition====================================\r\n')
    pd_id = []

    pd_info = SendCmd(c, 'phydrv')

    row_info = pd_info.split('\r\n')

    if 'Pool' in pd_info:
        pool_id = []

        for i in range(4, len(row_info) - 2):

            _id = row_info[i].split()[-1][-1]

            if len(row_info[i].split()) > 9 and 'Pool' in row_info[i] and _id not in str(pool_id):
                pool_id.append(_id)

        for i in pool_id:
            SendCmd(c, 'pool -a del -f -y -i ' + i)

    if 'ReadCache' in pd_info:
        pd_id_rc = []

        for i in range(4, len(row_info) - 2):

            if len(row_info[i].split()) > 9 and 'ReadCache' in row_info[i]:
                pd_id_rc.append(row_info[i].split()[0])

        SendCmd(c, 'rcache -a del -p ' + pd_id_rc[0])

    if 'WriteCache' in pd_info:
        SendCmd(c, 'wcache -a del')

    if 'Spare' in pd_info:
        spare_id = []

        spare_info = SendCmd(c, 'spare')
        spare_row = spare_info.split('\r\n')

        for i in range(4, len(spare_row) - 2):
            spare_id.append(spare_row[i].split()[0])

        for i in spare_id:
            SendCmd(c, 'spare -a del -i ' + i)

    for i in range(4, len(row_info) - 2):

        if len(row_info[i].split()) > 9 and 'HDD' in row_info[i]:
            pd_id.append(row_info[i].split()[0])

    tolog('===================================precondition====================================\r\n')
    return pd_id