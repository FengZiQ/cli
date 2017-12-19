# coding = utf-8
# 2017.9.28

from to_log import *
import xlrd
from send_cmd import *

Pass = "'result': 'p'"
Fail = "'result': 'f'"


# use to add, mod, and so on
class cli_test_setting():
    
    def __init__(self, FailFlag=False):
        self.FailFlag = FailFlag

    def setting(self, c, data_file_name, sheet_name, hold_time=0):

        # data = xlrd.open_workbook('/home/work/zach/clitest/' + data_file_name)
        data = xlrd.open_workbook(data_file_name)
        table = data.sheet_by_name(sheet_name)

        for i in range(1, table.nrows):

            tolog('\r\nExpect: ' + table.cell(i, 1).value + '\r\n')
            result = SendCmd(c, table.cell(i, 0).value)
            time.sleep(hold_time)

            if 'Error (' in result or 'unexpected error' in result:

                self.FailFlag = True
                tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

            else:
                check = SendCmd(c, table.cell(i, 2).value)

                if 'Error (' not in check:

                    for j in range(3, table.ncols):

                        if table.cell(i, j).value not in check:
                            self.FailFlag = True
                            tolog('\r\nFail: please check out ' + table.cell(i, j).value + '\r\n')

        if self.FailFlag:
            tolog(Fail)
        else:
            tolog(Pass)

    def setting_need_password(self, c, data_file_name, sheet_name, hold_time=0, password='12341234123'):

        # data = xlrd.open_workbook('/home/work/zach/clitest/' + data_file_name)
        data = xlrd.open_workbook(data_file_name)
        table = data.sheet_by_name(sheet_name)

        for i in range(1, table.nrows):

            tolog('\r\nExpect: ' + table.cell(i, 1).value + '\r\n')
            result = SendCmdpassword(c, table.cell(i, 0).value, password+str(i))
            time.sleep(hold_time)

            if 'Error (' in result or 'unexpected error' in result:

                self.FailFlag = True
                tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

            else:
                check = SendCmd(c, table.cell(i, 2).value)

                if 'Error (' not in check:

                    for j in range(3, table.ncols):

                        if table.cell(i, j).value not in check:
                            self.FailFlag = True
                            tolog('\r\nFail: please check out ' + table.cell(i, j).value + '\r\n')

        if self.FailFlag:
            tolog(Fail)
        else:
            tolog(Pass)

    def setting_need_double_password(self, c, data_file_name, sheet_name, hold_time=0):

        # data = xlrd.open_workbook('/home/work/zach/clitest/' + data_file_name)
        data = xlrd.open_workbook(data_file_name)
        table = data.sheet_by_name(sheet_name)

        for i in range(1, table.nrows):

            tolog('\r\nExpect: ' + table.cell(i, 1).value + '\r\n')
            result = SendCmdDoublepassword(c, table.cell(i, 0).value, '0123456789')
            time.sleep(hold_time)

            if 'Error (' in result or 'unexpected error' in result:

                self.FailFlag = True
                tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

            else:
                check = SendCmd(c, table.cell(i, 2).value)

                if 'Error (' not in check:

                    for j in range(3, table.ncols):

                        if table.cell(i, j).value not in check:
                            self.FailFlag = True
                            tolog('\r\nFail: please check out ' + table.cell(i, j).value + '\r\n')

        if self.FailFlag:
            tolog(Fail)
        else:
            tolog(Pass)


# use to list and so on
class cli_test_list():
    
    def __init__(self, FailFlag=False):
        self.FailFlag = FailFlag
        
    def list(self, c, data_file_name, sheet_name):

        # data = xlrd.open_workbook('/home/work/zach/clitest/' + data_file_name)
        data = xlrd.open_workbook(data_file_name)
        table = data.sheet_by_name(sheet_name)

        for i in range(1, table.nrows):

            tolog('\r\nExpect: ' + table.cell(i, 1).value + '\r\n')
            result = SendCmd(c, table.cell(i, 0).value)

            if 'Error (' in result or 'unexpected error' in result:

                self.FailFlag = True
                tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

            else:

                for j in range(2, table.ncols):

                    if table.cell(i, j).value not in result:
                        self.FailFlag = True
                        tolog('\r\nFail: please check out ' + table.cell(i, j).value + '\r\n')

        if self.FailFlag:
            tolog(Fail)
        else:
            tolog(Pass)


# use to verify nothing returned values action
class cli_test_other_action():
    
    def __init__(self, FailFlag=False):
        self.FailFlag = FailFlag
    
    def other(self, c, data_file_name, sheet_name):

        # data = xlrd.open_workbook('/home/work/zach/clitest/' + data_file_name)
        data = xlrd.open_workbook(data_file_name)
        table = data.sheet_by_name(sheet_name)

        for i in range(1, table.nrows):

            tolog('\r\nExpect: ' + table.cell(i, 1).value + '\r\n')
            result = SendCmd(c, table.cell(i, 0).value)

            if 'Error (' in result or 'unexpected error' in result:
                self.FailFlag = True
                tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

        if self.FailFlag:
            tolog(Fail)
        else:
            tolog(Pass)

    def other_need_confirm(self, c, data_file_name, sheet_name):

        # data = xlrd.open_workbook('/home/work/zach/clitest/' + data_file_name)
        data = xlrd.open_workbook(data_file_name)
        table = data.sheet_by_name(sheet_name)

        for i in range(1, table.nrows):

            tolog('\r\nExpect: ' + table.cell(i, 1).value + '\r\n')
            result = SendCmdconfirm(c, table.cell(i, 0).value)

            if 'Error (' in result or 'unexpected error' in result:
                self.FailFlag = True
                tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

        if self.FailFlag:
            tolog(Fail)
        else:
            tolog(Pass)


# use to del
class cli_test_delete():
    
    def __init__(self, FailFlag=False):
        self.FailFlag = FailFlag
    
    def delete(self, c, data_file_name, sheet_name, hold_time=0):

        # data = xlrd.open_workbook('/home/work/zach/clitest/' + data_file_name)
        data = xlrd.open_workbook(data_file_name)
        table = data.sheet_by_name(sheet_name)

        for i in range(1, table.nrows):

            tolog('\r\nExpect: ' + table.cell(i, 1).value + '\r\n')
            result = SendCmd(c, table.cell(i, 0).value)
            time.sleep(hold_time)

            if 'Error (' in result or 'unexpected error' in result:

                self.FailFlag = True
                tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

            else:
                check = SendCmd(c, table.cell(i, 2).value)

                if 'Error (' not in check:

                    for j in range(3, table.ncols):

                        if table.cell(i, j).value in check:
                            self.FailFlag = True
                            tolog('\r\nFail: please check out ' + table.cell(i, j).value + '\r\n')

        if self.FailFlag:
            tolog(Fail)
        else:
            tolog(Pass)

    def delete_need_confirm(self, c, data_file_name, sheet_name, hold_time=0):

        # data = xlrd.open_workbook('/home/work/zach/clitest/' + data_file_name)
        data = xlrd.open_workbook(data_file_name)
        table = data.sheet_by_name(sheet_name)

        for i in range(1, table.nrows):

            tolog('\r\nExpect: ' + table.cell(i, 1).value + '\r\n')
            result = SendCmdconfirm(c, table.cell(i, 0).value)
            time.sleep(hold_time)

            if 'Error (' in result or 'unexpected error' in result:

                self.FailFlag = True
                tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

            else:
                check = SendCmd(c, table.cell(i, 2).value)

                if 'Error (' not in check:

                    for j in range(3, table.ncols):

                        if table.cell(i, j).value in check:
                            self.FailFlag = True
                            tolog('\r\nFail: please check out ' + table.cell(i, j).value + '\r\n')

        if self.FailFlag:
            tolog(Fail)
        else:
            tolog(Pass)


# use to verify failed test
class cli_test_failed_test():
    
    def __init__(self, FailFlag=False):
        self.FailFlag = FailFlag
    
    def failed_test(self, c, data_file_name, sheet_name, hold_time=0):

        # data = xlrd.open_workbook('/home/work/zach/clitest/' + data_file_name)
        data = xlrd.open_workbook(data_file_name)
        table = data.sheet_by_name(sheet_name)

        for i in range(1, table.nrows):

            tolog('\r\nExpect: ' + table.cell(i, 1).value + '\r\n')
            result = SendCmd(c, table.cell(i, 0).value)
            time.sleep(hold_time)

            if 'Error (' not in result or 'unexpected error' in result:

                self.FailFlag = True
                tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

            else:

                for j in range(1, table.ncols):

                    if table.cell(i, j).value not in result:
                        self.FailFlag = True
                        tolog('\r\nFail: please check out ' + table.cell(i, j).value + '\r\n')

        if self.FailFlag:
            tolog(Fail)
        else:
            tolog(Pass)