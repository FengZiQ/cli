# coding = utf-8
# 2017.10.10

from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
import time
import xlrd
from command import command
from remote import server
from find_unconfigured_pd_id import find_pd_id


def precondition():
    pdId = find_pd_id("2TB")

    # create pool
    server.webapi('post', 'pool', {
        "name": 'test_protocol_pool',
        "raid_level": 'raid5',
        "pds": pdId
    })

    # create volume
    server.webapi('post', 'volume', {
        "name": 'test_protocol_volume',
        "pool_id": 0,
        "capacity": '10GB'
    })

    # create snapshot
    for i in range(3):
        server.webapi('post', 'snapshot', {
            "name": 'test_protocol_volume_' + str(i),
            "type": 'volume',
            "source_id": 0
        })

    # create clone
    for i in range(3):
        server.webapi('post', 'clone', {
            "name": 'test_protocol_clone_' + str(i),
            "source_id": 0
        })

    # create nasShare
    for i in range(3):
        server.webapi('post', 'nasshare', {
            "pool_id": 0,
            "name": 'test_protocol_nasShare_' + str(i),
            "capacity": '2GB'
        })

    # create nas user
    server.webapi('post', 'dsuser', {
        "id": 'test_protocol',
        "password": '000000'
    })


def list_all_protocol(c):
    tolog('Expect: list all of the protocol\r\n')

    result = SendCmd(c, 'protocol')

    if 'Error (' in result:

        command.FailFlag = True
        tolog('Fail: protocol\r\n')

    else:

        if 'SMB' not in result or 'FTP' not in result or 'NFS' not in result:

            command.FailFlag = True
            tolog('Fail: please check out result if contains SMB/FTP/NFS\r\n')

        else:

            tolog('\r\nActual: all of the protocol is listed\r\n')

    command.result()

    return command.FailFlag


def list_single_protocol(c):
    # precondition
    precondition()

    # test data
    data = xlrd.open_workbook('data/protocol.xlsx')
    table = data.sheet_by_name('list_single_protocol')

    for i in range(1, table.nrows):

        tolog('Expect: ' + table.cell(i, 1).value + '\r\n')
        result = SendCmd(c, table.cell(i, 0).value)

        if 'Error (' in result:

            command.FailFlag = True
            tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

        else:
            tolog('\r\nActual: ' + table.cell(i, 2).value + '\r\n')

    command.result()

    return command.FailFlag


def mod_ftp_protocol(c):
    # test data
    data = xlrd.open_workbook('data/protocol.xlsx')
    table = data.sheet_by_name('mod_ftp_protocol')

    for i in range(1, table.nrows):

        result = SendCmd(c, table.cell(i, 0).value)

        if 'Error (' in result:

            command.FailFlag = True
            tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

        else:
            check = SendCmd(c, table.cell(i, 2).value)

            for j in range(3, table.ncols):

                if table.cell(i, j).value not in check:

                    command.FailFlag = True
                    tolog('\r\nFail: please check out ' + table.cell(i, j).value + '\r\n')

            else:

                tolog('\r\nActual: modify successfully\r\n')

    command.result()


def mod_smb_protocol(c):
    # test data
    data = xlrd.open_workbook('data/protocol.xlsx')
    table = data.sheet_by_name('mod_smb_protocol')

    for i in range(1, table.nrows):

        result = SendCmdconfirm(c, table.cell(i, 0).value)

        if 'Error (' in result:

            command.FailFlag = True
            tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

        else:
            check = SendCmd(c, table.cell(i, 2).value)

            for j in range(3, table.ncols):

                if table.cell(i, j).value not in check:
                    command.FailFlag = True
                    tolog('\r\nFail: please check out ' + table.cell(i, j).value + '\r\n')

            else:

                tolog('\r\nActual: modify successfully\r\n')

    command.result()


def mod_nfs_protocol(c):
    # test data
    data = xlrd.open_workbook('data/protocol.xlsx')
    table = data.sheet_by_name('mod_nfs_protocol')

    for i in range(1, table.nrows):

        result = SendCmd(c, table.cell(i, 0).value)

        if 'Error (' in result:

            command.FailFlag = True
            tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

        else:
            check = SendCmd(c, table.cell(i, 2).value)

            for j in range(3, table.ncols):

                if table.cell(i, j).value not in check:

                    command.FailFlag = True
                    tolog('\r\nFail: please check out ' + table.cell(i, j).value + '\r\n')

            else:

                tolog('\r\nActual: modify successfully\r\n')

    command.result()


def reset_all_protocol(c):

    result = SendCmd(c, 'protocol -a reset')

    check1 = SendCmd(c, 'protocol -n smb')

    check2 = SendCmd(c, 'protocol -n nfs')

    check3 = SendCmd(c, 'protocol -n ftp')

    if 'Error (' in result:

        command.FailFlag = True
        tolog('\r\nFail: protocol -a reset\r\n')

    else:

        if 'Status: Disabled' not in check1 or 'Workgroup: WORKGROUP' not in check1 or 'NtAcl: no' not in check1:

            command.FailFlag = True
            tolog('\r\nFail: smb does not reset\r\n')

        else:
            tolog('\r\nActual: smb successfully reset\r\n')

        if 'Status: Disabled' not in check2 or 'mountd port: 56789' not in check2:

            command.FailFlag = True
            tolog('\r\nFail: nfs does not reset\r\n')

        else:
            tolog('Actual: nfs successfully reset\r\n')

        if 'Status: Disabled' not in check3 or 'CmdPort: 21' not in check3 or 'Charset: utf8' not in check3:

            command.FailFlag = True
            tolog('\r\nFail: ftp does not reset\r\n')

        else:
            tolog('Actual: ftp successfully reset\r\n')

    command.result()


def reset_single_protocol(c):
    # precondition
    for n in ['FTP', 'NFS', 'SMB']:
        server.webapi('post', 'protocol/enable/' + n)

    # test data
    data = xlrd.open_workbook('data/protocol.xlsx')
    table = data.sheet_by_name('reset_single_protocol')

    for i in range(1, table.nrows):

        tolog('Expect: reset ' + table.cell(i, 0).value[-3:] + '\r\n')

        result = SendCmd(c, table.cell(i, 0).value)

        if 'Error (' in result:

            command.FailFlag = True
            tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

        else:

            check = SendCmd(c, table.cell(i, 2).value)

            if table.cell(i, 3).value not in check:

                command.FailFlag = True
                tolog('\r\nFail: please check out protocol status\r\n')

            else:
                tolog('\r\nActual: ' + table.cell(i, 0).value[-3:] + ' is reset\r\n')

    command.result()


def enable_protocol(c):
    # precondition
    for n in ['FTP', 'NFS', 'SMB']:
        server.webapi('post', 'protocol/disable/' + n)

    # test data
    data = xlrd.open_workbook('data/protocol.xlsx')
    table = data.sheet_by_name('enable_protocol')

    for i in range(1, table.nrows):

        tolog('Expect: enable ' + table.cell(i, 0).value[-3:] + '\r\n')

        result = SendCmd(c, table.cell(i, 0).value)

        if 'Error (' in result:

            command.FailFlag = True
            tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

        else:

            check = SendCmd(c, table.cell(i, 2).value)

            if table.cell(i, 3).value not in check:

                command.FailFlag = True
                tolog('\r\nFail: please check out protocol status\r\n')

            else:
                tolog('\r\nActual: ' + table.cell(i, 0).value[-3:] + ' is enabled\r\n')

    command.result()


def disable_protocol(c):
    # precondition
    for n in ['FTP', 'NFS', 'SMB']:
        server.webapi('post', 'protocol/enable/' + n)

    # test data
    data = xlrd.open_workbook('data/protocol.xlsx')
    table = data.sheet_by_name('disable_protocol')

    for i in range(1, table.nrows):

        tolog('Expect: disable ' + table.cell(i, 0).value[-3:] + '\r\n')

        result = SendCmd(c, table.cell(i, 0).value)

        if 'Error (' in result:

            command.FailFlag = True
            tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

        else:

            check = SendCmd(c, table.cell(i, 2).value)

            if table.cell(i, 3).value not in check:

                command.FailFlag = True
                tolog('\r\nFail: please check out protocol status\r\n')

            else:
                tolog('\r\nActual: ' + table.cell(i, 0).value[-3:] + ' is disabled\r\n')

    command.result()


def invalid_setting_parameter(c):
    # test data
    data = xlrd.open_workbook('data/protocol.xlsx')
    table = data.sheet_by_name('invalid_setting_parameter')

    for i in range(1, table.nrows):

        tolog('Expect: error message should contain: ' + table.cell(i, 1).value + '\r\n')
        result = SendCmd(c, table.cell(i, 0).value)

        if 'Error (' not in result:

            command.FailFlag = True
            tolog('Fail: ' + table.cell(i, 0).value + '\r\n')

        else:

            if table.cell(i, 1).value not in result:

                command.FailFlag = True
                tolog('\r\nFail: please check out error message\r\n')

            tolog('\r\nActual: ' + table.cell(i, 2).value + ' is successful\r\n')

    command.result()


def invalid_option(c):
    # test data
    data = xlrd.open_workbook('data/protocol.xlsx')
    table = data.sheet_by_name('invalid_option')

    for i in range(1, table.nrows):

        tolog('Expect: error message should contain: ' + table.cell(i, 1).value + '\r\n')
        result = SendCmd(c, table.cell(i, 0).value)

        if 'Error (' not in result:

            command.FailFlag = True
            tolog('Fail: ' + table.cell(i, 0).value + '\r\n')

        else:

            if table.cell(i, 1).value not in result:

                command.FailFlag = True
                tolog('\r\nFail: please check out error message\r\n')

            tolog('\r\nActual: ' + table.cell(i, 2).value + ' is successful\r\n')

    command.result()


def missing_parameter(c):
    # test data
    data = xlrd.open_workbook('data/protocol.xlsx')
    table = data.sheet_by_name('missing_parameter')

    for i in range(1, table.nrows):

        tolog('Expect: error message should contain: ' + table.cell(i, 1).value + '\r\n')
        result = SendCmd(c, table.cell(i, 0).value)

        if 'Error (' not in result:

            command.FailFlag = True
            tolog('Fail: ' + table.cell(i, 0).value + '\r\n')

        else:

            if table.cell(i, 1).value not in result:

                command.FailFlag = True
                tolog('\r\nFail: please check out error message\r\n')

            tolog('\r\nActual: ' + table.cell(i, 2).value + ' is successful\r\n')

    clean_up_environment()

    command.result()


def clean_up_environment():
    # delete pool
    server.webapi('delete', 'pool/0?force=1')

    # delete nas user
    server.webapi('delete', 'dsuser/test_protocol')


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    list_all_protocol(c)
    list_single_protocol(c)
    mod_ftp_protocol(c)
    mod_smb_protocol(c)
    mod_nfs_protocol(c)
    reset_all_protocol(c)
    reset_single_protocol(c)
    enable_protocol(c)
    disable_protocol(c)
    invalid_setting_parameter(c)
    invalid_option(c)
    missing_parameter(c)

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped