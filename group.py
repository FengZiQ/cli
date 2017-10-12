# coding = utf-8
# 2017.10.10

from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
import time
import xlrd
import json
from command import command
from remote import server


def add_group_and_verify_name(c):

    # test data
    data = xlrd.open_workbook('data/group.xlsx')
    table = data.sheet_by_name('add_group_and_verify_name')

    for i in range(1, table.nrows):

        tolog('\r\nExpect: add group ' + table.cell(i, 0).value + '\r\n')
        result = SendCmd(c, 'group -a add -g ' + table.cell(i, 0).value)

        if 'Error (' in result:

            command.FailFlag = True
            tolog('Fail: ' + result + '\r\n')

        else:
            tolog('\r\nActual: group ' + table.cell(i, 0).value + ' is added')

    command.result()

    return command.FailFlag


def add_group_and_user(c):
    # precondition
    # create DSUser
    for i in range(10):
        server.webapi('post', 'dsuser', {
                "id": 'test_group_' + str(i),
                "password": '123456'
            })

    name_list = 'test_group_0,test_group_1'

    tolog('add group and user\r\n')
    restult = SendCmd(c, 'group -a add -g add_group_and_user -u "' + str(name_list) + '"')

    if 'Error (' in restult:
        command.FailFlag = True
        tolog('Fail: ' + restult + '\r\n')

    else:
        tolog('\r\nActual: group and user are added\r\n')

    command.result()

    return command.FailFlag


def add_user_into_group(c):
    # test data
    data = xlrd.open_workbook('data/group.xlsx')
    table = data.sheet_by_name('add_group_and_verify_name')

    tolog('Expect: add user into group ' + table.cell(1, 0).value + '\r\n')
    result = SendCmd(c, 'group -a adduser -g ' + table.cell(1, 0).value + ' -u "test_group_0,test_group_1"')

    if 'Error (' in result:

        command.FailFlag = True
        tolog('Fail: ' + result + '\r\n')

    else:

        tolog('Actual: the user are added into group ' + table.cell(1, 0).value + '\r\n')

    command.result()

    return command.FailFlag


def list_group(c):
    # test data
    data = xlrd.open_workbook('data/group.xlsx')
    table = data.sheet_by_name('add_group_and_verify_name')

    tolog('Expect: list all of group\r\n')

    result1 = SendCmd(c, 'group')

    if 'Error (' in result1:

        command.FailFlag = True
        tolog('Fail: ' + result1 + '\r\n')

    else:
        tolog('Actual: all of group is listed\r\n')

    for i in range(1, table.nrows):
        tolog('\r\nExpect: list group ' + table.cell(i, 0).value + '\r\n')

        result2 = SendCmd(c, 'group -g ' + table.cell(i, 0).value)

        if 'Error (' in result2 or 'not found' in result2:

            command.FailFlag = True
            tolog('Fail: ' + result2 + '\r\n')

        else:
            tolog('\r\nActual: the group ' + table.cell(i, 0).value + ' is listed\r\n')

    command.result()

    return command.FailFlag


def list_group_by_verbose_mode(c):
    # test data
    data = xlrd.open_workbook('data/group.xlsx')
    table = data.sheet_by_name('add_group_and_verify_name')

    tolog('Expect: list all of group by verbose mode\r\n')

    result1 = SendCmd(c, 'group -v')

    if 'Error (' in result1:

        command.FailFlag = True
        tolog('Fail: ' + result1 + '\r\n')

    else:
        tolog('Actual: all of group is listed by verbose mode\r\n')

    for i in range(1, table.nrows):
        tolog('\r\nExpect: list group ' + table.cell(i, 0).value + ' by verbose mode\r\n')

        result2 = SendCmd(c, 'group -v -g ' + table.cell(i, 0).value)

        if 'Error (' in result2 or 'not found' in result2:

            command.FailFlag = True
            tolog('Fail: ' + result2 + '\r\n')

        else:
            tolog('\r\nActual: the group ' + table.cell(i, 0).value + ' is listed by verbose mode\r\n')

    command.result()

    return command.FailFlag


def modify_group(c):
    # test data
    data = xlrd.open_workbook('data/group.xlsx')
    table = data.sheet_by_name('add_group_and_verify_name')

    tolog('Expect: modify description of group ' + table.cell(1, 0).value + '\r\n')
    result = SendCmd(c, 'group -a mod -g ' + table.cell(1, 0).value + ' -s "desc=this is the test group"')

    if 'Error (' in result:

        command.FailFlag = True
        tolog('Fail: ' + result + '\r\n')

    else:
        check = SendCmd(c, 'group -v -g ' + table.cell(1, 0).value)

        if 'this is the test group' not in check:

            command.FailFlag = True
            tolog('Fail: please check out description\r\n')

        else:
            tolog('\r\nActual: add successfully description for group\r\n')

    command.result()

    return command.FailFlag


def delete_user_from_group(c):
    # test data
    data = xlrd.open_workbook('data/group.xlsx')
    table = data.sheet_by_name('add_group_and_verify_name')

    tolog('Expect: delete user from ' + table.cell(1, 0).value + ' of group\r\n')

    group_info = SendCmd(c, 'group -v -g ' + table.cell(1, 0).value)

    data = group_info.split('UserList:')[1].split('Description:')[0].split('\r\n')[0]

    result = SendCmd(c, 'group -a deluser -g ' + table.cell(1, 0).value + ' -u ' + data)

    if 'Error (' in result:

        command.FailFlag = True
        tolog('Fail; ' + result + '\r\n')

    else:

        check = SendCmd(c, 'group -v -g ' + table.cell(1, 0).value)

        if data in check:

            command.FailFlag = True
            tolog('\r\nFail: please check out ' + data + ' in users of group\r\n')

        else:

            tolog('\r\nActual: ' + data + ' is deleted from users of group\r\n')

    command.result()

    return command.FailFlag


def delete_group(c):
    # test data
    data = xlrd.open_workbook('data/group.xlsx')
    table = data.sheet_by_name('add_group_and_verify_name')

    for i in range(1, table.nrows):
        tolog('Expect: delete group ' + table.cell(i, 0).value + '\r\n')

        result = SendCmd(c, 'group -a del -g ' + table.cell(i, 0).value)

        if 'Error (' in result:

            command.FailFlag = True
            tolog('Fail: ' + result + '\r\n')

        else:

            tolog('\r\nActual: the ' + table.cell(i, 0).value + ' of group is deleted\r\n')

    command.result()

    return command.FailFlag


def invalid_setting_parameter(c):
    # test data
    data = xlrd.open_workbook('data/group.xlsx')
    table = data.sheet_by_name('invalid_setting_parameter')

    for i in range(1, table.nrows):
        # precondition
        SendCmd(c, 'group -a cancel')

        tolog('Expect: error information contains ' + table.cell(i, 1).value + '\r\n')
        result = SendCmd(c, table.cell(i, 0).value)

        if 'Error (' not in result:

            command.FailFlag = True
            tolog('Fail: ' + result + '\r\n')

        else:

            if table.cell(i, 1).value not in result:

                command.FailFlag = True
                tolog('Fail: please check out error information\r\n')

            else:

                tolog('\r\nActual: hints error and corrects it\r\n')

    command.result()

    return command.FailFlag


def invalid_option(c):
    # test data
    data = xlrd.open_workbook('data/group.xlsx')
    table = data.sheet_by_name('invalid_option')

    for i in range(1, table.nrows):

        tolog('Expect: error information contains ' + table.cell(i, 1).value + '\r\n')
        result = SendCmd(c, table.cell(i, 0).value)

        if 'Error (' not in result:

            command.FailFlag = True
            tolog('Fail: ' + result + '\r\n')

        else:

            if table.cell(i, 1).value not in result:

                command.FailFlag = True
                tolog('Fail: please check out error information\r\n')

            else:

                tolog('\r\nActual: hints error and corrects it\r\n')

    command.result()

    return command.FailFlag


def missing_parameter(c):
    # test data
    data = xlrd.open_workbook('data/group.xlsx')
    table = data.sheet_by_name('missing_parameter')

    for i in range(1, table.nrows):

        tolog('Expect: error information contains ' + table.cell(i, 1).value + '\r\n')
        result = SendCmd(c, table.cell(i, 0).value)

        if 'Error (' not in result:

            command.FailFlag = True
            tolog('Fail: ' + result + '\r\n')

        else:

            if table.cell(i, 1).value not in result:

                command.FailFlag = True
                tolog('Fail: please check out error information\r\n')

            else:

                tolog('\r\nActual: hints error and corrects it\r\n')

    command.result()

    return command.FailFlag


def failed_process(c):
    # test data
    data = xlrd.open_workbook('data/group.xlsx')
    table = data.sheet_by_name('failed_process')

    for i in range(1, table.nrows - 2):

        tolog('Expect: error information contains ' + table.cell(i, 1).value + '\r\n')
        result = SendCmd(c, table.cell(i, 0).value)

        if 'Error (' not in result:

            command.FailFlag = True
            tolog('Fail: ' + result + '\r\n')

        else:

            if table.cell(i, 1).value not in result:

                command.FailFlag = True
                tolog('Fail: please check out error information\r\n')

            else:

                tolog('\r\nActual: hints error and corrects it\r\n')

    result1 = SendCmd(c, table.cell(table.nrows - 2, 0).value)

    if 'Error (' not in result1:
        tolog('please check out if invalid_user exists')
    else:
        result2 = SendCmd(c, table.cell(table.nrows - 1, 0).value)

        if 'Error (' in result2:
            command.FailFlag = True
            tolog('\r\nFail: ' + result2 + '\r\n')

    # clean up environment
    SendCmd(c, 'group -a cancel')
    clean_up_environment()

    command.result()

    return command.FailFlag


def clean_up_environment():
    # delete nas user
    users = server.webapi('get', 'dsuser?page=1&page_size=500')
    user_info = json.loads(users["text"])
    for user in user_info:
        server.webapi('delete', 'dsuser/' + user["id"])

    # delete group
    server.webapi('delete', 'dsgroup/add_group_and_user')


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()

    add_group_and_verify_name(c)
    add_group_and_user(c)
    add_user_into_group(c)
    list_group(c)
    list_group_by_verbose_mode(c)
    modify_group(c)
    delete_user_from_group(c)
    delete_group(c)
    invalid_setting_parameter(c)
    invalid_option(c)
    missing_parameter(c)
    failed_process(c)
    clean_up_environment()

    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped