# coding = utf-8
# 2017.9.28

from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
import time
import xlrd
from command import command
from find_un_pd_id import pd_id


def add_pool_raid0(c):

    # test data
    pdId = pd_id(c)
    data = xlrd.open_workbook('data/pool.xlsx')
    table = data.sheet_by_name('add_pool')

    # add raid0 pool
    tolog('Expect: add raid0 pool\r\n')

    result = SendCmd(c, table.cell(1, 0).value + pdId[0])

    if 'Error (' in result:

        command.FailFlag = True
        tolog('Fail: ' + str(table.cell(1, 0).value) + pdId[0] + '\r\n')

    else:

        check = SendCmd(c, 'pool -v -i 0')

        for i in range(1, 6):

            if table.cell(1, i).value not in check:

                command.FailFlag = True
                tolog('Fail: please check out ' + table.cell(1, i).value + '\r\n')

    command.result()


def add_pool_raid1(c):

    # test data
    pdId = pd_id(c)
    data = xlrd.open_workbook('data/pool.xlsx')
    table = data.sheet_by_name('add_pool')

    # add raid1 pool
    tolog('Expect: add raid1 pool\r\n')

    result = SendCmd(c, table.cell(2, 0).value + ','.join(pdId[:2]))

    if 'Error (' in result:

        command.FailFlag = True
        tolog('Fail: ' + str(table.cell(2, 0).value) + ','.join(pdId[:2]) + '\r\n')

    else:

        check = SendCmd(c, 'pool -v -i 0')

        for i in range(1, 6):

            if table.cell(2, i).value not in check:

                command.FailFlag = True
                tolog('Fail: please check out ' + table.cell(2, i).value + '\r\n')

    command.result()


def add_pool_raid5(c):

    # test data
    pdId = pd_id(c)
    data = xlrd.open_workbook('data/pool.xlsx')
    table = data.sheet_by_name('add_pool')

    # add raid5 pool
    tolog('Expect: add raid5 pool\r\n')

    result = SendCmd(c, table.cell(3, 0).value + ','.join(pdId[:3]))

    if 'Error (' in result:

        command.FailFlag = True
        tolog('Fail: ' + str(table.cell(3, 0).value) + ','.join(pdId[:3]) + '\r\n')

    else:

        check = SendCmd(c, 'pool -v -i 0')

        for i in range(1, 6):

            if table.cell(3, i).value not in check:

                command.FailFlag = True
                tolog('Fail: please check out ' + table.cell(3, i).value + '\r\n')

    command.result()


def add_pool_raid6(c):

    # test data
    pdId = pd_id(c)
    data = xlrd.open_workbook('data/pool.xlsx')
    table = data.sheet_by_name('add_pool')

    # add raid6 pool
    tolog('Expect: add raid6 pool\r\n')

    result = SendCmd(c, table.cell(4, 0).value + ','.join(pdId[:4]))

    if 'Error (' in result:

        command.FailFlag = True
        tolog('Fail: ' + str(table.cell(4, 0).value) + ','.join(pdId[:4]) + '\r\n')

    else:

        check = SendCmd(c, 'pool -v -i 0')

        for i in range(1, 6):

            if table.cell(4, i).value not in check:

                command.FailFlag = True
                tolog('Fail: please check out ' + table.cell(4, i).value + '\r\n')

    command.result()


def add_pool_raid10(c):

    # test data
    pdId = pd_id(c)
    data = xlrd.open_workbook('data/pool.xlsx')
    table = data.sheet_by_name('add_pool')

    # add raid10 pool
    tolog('Expect: add raid10 pool\r\n')

    result = SendCmd(c, table.cell(5, 0).value + ','.join(pdId[:4]))

    if 'Error (' in result:

        command.FailFlag = True
        tolog('Fail: ' + str(table.cell(5, 0).value) + ','.join(pdId[:4]) + '\r\n')

    else:

        check = SendCmd(c, 'pool -v -i 0')

        for i in range(1, 6):

            if table.cell(5, i).value not in check:

                command.FailFlag = True
                tolog('Fail: please check out ' + table.cell(5, i).value + '\r\n')

    command.result()


def add_pool_raid50(c):

    # test data
    pdId = pd_id(c)
    data = xlrd.open_workbook('data/pool.xlsx')
    table = data.sheet_by_name('add_pool')

    # add raid50 pool
    tolog('Expect: add raid50 pool\r\n')

    result = SendCmd(c, table.cell(6, 0).value + ','.join(pdId[:6]))

    if 'Error (' in result:

        command.FailFlag = True
        tolog('Fail: ' + str(table.cell(6, 0).value) + ','.join(pdId[:6]) + '\r\n')

    else:

        check = SendCmd(c, 'pool -v -i 0')

        for i in range(1, 7):

            if table.cell(6, i).value not in check:

                command.FailFlag = True
                tolog('Fail: please check out ' + table.cell(6, i).value + '\r\n')

    command.result()


def add_pool_raid60(c):

    # test data
    pdId = pd_id(c)
    data = xlrd.open_workbook('data/pool.xlsx')
    table = data.sheet_by_name('add_pool')

    # add raid60 pool
    tolog('Expect: add raid60 pool\r\n')

    result = SendCmd(c, table.cell(7, 0).value + ','.join(pdId[:8]))

    if 'Error (' in result:

        command.FailFlag = True
        tolog('Fail: ' + str(table.cell(7, 0).value) + ','.join(pdId[:8]) + '\r\n')

    else:

        check = SendCmd(c, 'pool -v -i 0')

        for i in range(1, 7):

            if table.cell(7, i).value not in check:

                command.FailFlag = True
                tolog('Fail: please check out ' + table.cell(7, i).value + '\r\n')

    command.result()


def add_pool_default_setting(c):

    # test data
    pdId = pd_id(c)
    data = xlrd.open_workbook('data/pool.xlsx')
    table = data.sheet_by_name('add_pool')

    # add pool by default setting
    tolog('Expect: add pool by default setting\r\n')
    result = SendCmd(c, table.cell(8, 0).value + ','.join(pdId[:8]))

    if 'Error (' in result:

        command.FailFlag = True
        tolog('Fail: ' + str(table.cell(8, 0).value) + ','.join(pdId[:8]) + '\r\n')

    else:

        check = SendCmd(c, 'pool -v -i 0')

        for i in range(1, 6):

            if table.cell(8, i).value not in check:
                command.FailFlag = True
                tolog('Fail: please check out ' + table.cell(8, i).value + '\r\n')

    command.result()


def modify_pool_name(c):

    # test data
    data = xlrd.open_workbook('data/pool.xlsx')
    table = data.sheet_by_name('mod_pool_name')

    for i in range(1, table.nrows):

        tolog('Expect: modify pool ' + table.cell(i, 1).value + '\r\n')
        result = SendCmd(c, table.cell(i, 0).value)

        if 'Error (' in result:

            command.FailFlag = True
            tolog('Fail: ' + str(table.cell(i, 0).value) + '\r\n')

        else:

            check = SendCmd(c, 'pool -v -i 0')

            if table.cell(i, 1).value not in check:

                command.FailFlag = True
                tolog('Fail: please check out ' + table.cell(i, 1).value + '\r\n')

    command.result()


def list_pool(c):

    # test data
    pdId = pd_id(c)

    # precondition
    SendCmd(c, 'pool -a add -s "name=1,raid=1" -p ' + ','.join(pdId[:2]))
    SendCmd(c, 'pool -a add -s "name=2,raid=5" -p ' + ','.join(pdId[2:]))

    # list all of pool
    tolog('Expect: list all of pool\r\n')
    result_all = SendCmd(c, 'pool')

    if 'Error' in result_all:

        command.FailFlag = True
        tolog('Fail: pool\r\n')

    # list specific pool
    tolog('Expect: list specific pool\r\n')

    for i in ['0', '1']:

        result_specific = SendCmd(c, 'pool -i ' + i)

        if 'Error (' in result_specific:

            command.FailFlag = True
            tolog('Fail: pool -i ' + i + '\r\n')

    command.result()


def list_verbose_mode_pool(c):

    # list all of pool
    tolog('Expect: list all of pool by verbose mode\r\n')
    result_all = SendCmd(c, 'pool -v')

    if 'Error' in result_all:

        command.FailFlag = True
        tolog('Fail: pool -v\r\n')

    # list specific pool
    tolog('Expect: list specific pool by verbose mode\r\n')

    for i in ['0', '1']:

        result_specific = SendCmd(c, 'pool -v -i ' + i)

        if 'Error (' in result_specific:

            command.FailFlag = True
            tolog('Fail: pool -v -i ' + i + '\r\n')

    command.result()


def extend_raid0_pool(c):

    # test data
    pdId = pd_id(c)

    # precondition
    SendCmd(c, 'pool -a add -s "name=extend, raid=0" -p ' + pdId[0])

    tolog('Expect: extend raid0 pool by pds ' + ','.join(pdId[1:]) + '\r\n')
    result = SendCmd(c, 'pool -a extend -i 0 -p ' + ','.join(pdId[1:]))

    if 'Error (' in result:

        command.FailFlag = True
        tolog('Fail: ' + 'pool -a extend -i 0 -p ' + ','.join(pdId[1:]) + '\r\n')

    else:
        check = SendCmd(c, 'pool -v -i 0')

        if ','.join(pdId) not in check:

            command.FailFlag = True
            tolog('Fail: please check out parameter pds\r\n')

    command.result()


def extend_raid1_pool(c):

    # test data
    pdId = pd_id(c)

    # precondition
    SendCmd(c, 'pool -a add -s "name=extend, raid=1" -p ' + ','.join(pdId[:2]))

    tolog('Expect: extend raid1 pool by pds ' + ','.join(pdId[2:4]) + '\r\n')
    result = SendCmd(c, 'pool -a extend -i 0 -p ' + ','.join(pdId[2:4]))

    if 'Error (' in result:

        command.FailFlag = True
        tolog('Fail: ' + 'pool -a extend -i 0 -p ' + ','.join(pdId[2:4]) + '\r\n')

    else:
        check = SendCmd(c, 'pool -v -i 0')

        if ','.join(pdId[:4]) not in check:

            command.FailFlag = True
            tolog('Fail: please check out parameter pds\r\n')

    command.result()


def extend_raid5_pool(c):

    # test data
    pdId = pd_id(c)

    # precondition
    SendCmd(c, 'pool -a add -s "name=extend, raid=5" -p ' + ','.join(pdId[:4]))

    tolog('Expect: extend raid5 pool by pds ' + ','.join(pdId[4:7]) + '\r\n')
    result = SendCmd(c, 'pool -a extend -i 0 -p ' + ','.join(pdId[4:7]))

    if 'Error (' in result:

        command.FailFlag = True
        tolog('Fail: ' + 'pool -a extend -i 0 -p ' + ','.join(pdId[4:7]) + '\r\n')

    else:
        check = SendCmd(c, 'pool -v -i 0')

        if ','.join(pdId[:7]) not in check:

            command.FailFlag = True
            tolog('Fail: please check out parameter pds\r\n')

    command.result()


def extend_raid6_pool(c):

    # test data
    pdId = pd_id(c)

    # precondition
    SendCmd(c, 'pool -a add -s "name=extend, raid=6" -p ' + ','.join(pdId[:4]))

    tolog('Expect: extend raid6 pool by pds ' + ','.join(pdId[4:]) + '\r\n')
    result = SendCmd(c, 'pool -a extend -i 0 -p ' + ','.join(pdId[4:]))

    if 'Error (' in result:

        command.FailFlag = True
        tolog('Fail: ' + 'pool -a extend -i 0 -p ' + ','.join(pdId[4:]) + '\r\n')

    else:
        check = SendCmd(c, 'pool -v -i 0')

        if ','.join(pdId) not in check:

            command.FailFlag = True
            tolog('Fail: please check out parameter pds\r\n')

    command.result()


def extend_raid10_pool(c):

    # test data
    pdId = pd_id(c)

    # precondition
    SendCmd(c, 'pool -a add -s "name=extend, raid=10" -p ' + ','.join(pdId[:4]))

    tolog('Expect: extend raid10 pool by pds ' + ','.join(pdId[4:8]) + '\r\n')
    result = SendCmd(c, 'pool -a extend -i 0 -p ' + ','.join(pdId[4:8]))

    if 'Error (' in result:

        command.FailFlag = True
        tolog('Fail: ' + 'pool -a extend -i 0 -p ' + ','.join(pdId[4:8]) + '\r\n')

    else:
        check = SendCmd(c, 'pool -v -i 0')

        if ','.join(pdId[:8]) not in check:

            command.FailFlag = True
            tolog('Fail: please check out parameter pds\r\n')

    command.result()


def extend_raid50_pool(c):

    # test data
    pdId = pd_id(c)

    # precondition
    SendCmd(c, 'pool -a add -s "name=extend, raid=50, axle=2" -p ' + ','.join(pdId[:6]))

    tolog('Expect: extend raid50 pool by pds ' + ','.join(pdId[6:]) + '\r\n')
    result = SendCmd(c, 'pool -a extend -s "axle=3" -i 0 -p ' + ','.join(pdId[6:]))

    if 'Error (' in result:

        command.FailFlag = True
        tolog('Fail: ' + 'pool -a extend -i 0 -p ' + ','.join(pdId[6:]) + '\r\n')

    else:
        check = SendCmd(c, 'pool -v -i 0')

        if ','.join(pdId) not in check:

            command.FailFlag = True
            tolog('Fail: please check out parameter pds\r\n')

    command.result()


def extend_raid60_pool(c):

    # test data
    pdId = pd_id(c)

    # precondition
    SendCmd(c, 'pool -a add -s "name=extend, raid=60, axle=2" -p ' + ','.join(pdId[:8]))

    tolog('Expect: extend raid60 pool by pds ' + ','.join(pdId[8:]) + '\r\n')
    result = SendCmd(c, 'pool -a extend -s "axle=1" -i 0 -p ' + ','.join(pdId[8:]))

    if 'Error (' in result:

        command.FailFlag = True
        tolog('Fail: ' + 'pool -a extend -i 0 -p ' + ','.join(pdId[8:]) + '\r\n')

    else:
        check = SendCmd(c, 'pool -v -i 0')

        if ','.join(pdId) not in check:

            command.FailFlag = True
            tolog('Fail: please check out parameter pds\r\n')

    command.result()


def invalid_pool_name(c):

    # test data
    data = xlrd.open_workbook('data/pool.xlsx')
    table = data.sheet_by_name('invalid_pool_name')

    for i in range(1,table.nrows):

        tolog('Expect: name can not be specified ' + table.cell(i, 2).value + '\r\n')
        result = SendCmd(c, table.cell(i, 0).value)

        if 'Error (' not in result or table.cell(i, 1).value not in result:

            command.FailFlag = True
            tolog('Fail: ' + table.cell(i, 0).value + '\r\n')

    command.result()


def invalid_settings_parameter(c):

    # test data
    data = xlrd.open_workbook('data/pool.xlsx')
    table = data.sheet_by_name('invalid_settings_parameter')

    for i in range(1, table.nrows):

        tolog('Expect: ' + table.cell(i, 2).value + '\r\n')
        result = SendCmd(c, table.cell(i, 0).value)

        if 'Error (' not in result or table.cell(i, 1).value not in result:

            command.FailFlag = True
            tolog('Fail: ' + table.cell(i, 0).value + '\r\n')

    command.result()


def invalid_option(c):

    # test data
    data = xlrd.open_workbook('data/pool.xlsx')
    table = data.sheet_by_name('invalid_option')

    for i in range(1, table.nrows):

        tolog('Expect: To hint error information contains invalid option\r\n')
        result = SendCmd(c, table.cell(i, 0).value)

        if 'Error (' not in result or table.cell(i, 1).value not in result:

            command.FailFlag = True
            tolog('Fail: ' + table.cell(i, 0).value + '\r\n')

    command.result()


def missing_parameter(c):

    # test data
    data = xlrd.open_workbook('data/pool.xlsx')
    table = data.sheet_by_name('missing_parameter')

    for i in range(1, table.nrows):

        tolog('Expect: To hint error information contains missing parameter\r\n')
        result = SendCmd(c, table.cell(i, 0).value)

        if 'Error (' not in result or table.cell(i, 1).value not in result:

            command.FailFlag = True
            tolog('Fail: ' + table.cell(i, 0).value + '\r\n')

    command.result()


def add_pool_by_configure_pd(c):

    # test data
    pdid = pd_id(c)

    # precondition
    SendCmd(c, 'spare -a add -t g -p ' + pdid[0])

    result = SendCmd(c, 'pool -a add -s "name=failed_test,raid=5" -p ' + ','.join(pdid[:4]))

    if 'Error (' not in result or 'Physical drive in use' not in result:

        command.FailFlag = True
        tolog('Fail: pool -a add -s "name=failed_test,raid=5" -p ' + ','.join(pdid[:4]) + '\r\n')

    # clean up environment
    SendCmd(c, 'spare -a del -i 0')

    command.result()


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    add_pool_raid0(c)
    add_pool_raid1(c)
    add_pool_raid5(c)
    add_pool_raid6(c)
    add_pool_raid10(c)
    add_pool_raid50(c)
    add_pool_raid60(c)
    add_pool_default_setting(c)
    modify_pool_name(c)
    list_pool(c)
    list_verbose_mode_pool(c)
    extend_raid0_pool(c)
    extend_raid1_pool(c)
    extend_raid5_pool(c)
    extend_raid6_pool(c)
    extend_raid10_pool(c)
    extend_raid50_pool(c)
    extend_raid60_pool(c)
    invalid_pool_name(c)
    invalid_settings_parameter(c)
    invalid_option(c)
    missing_parameter(c)
    add_pool_by_configure_pd(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped