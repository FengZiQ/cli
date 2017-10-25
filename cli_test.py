# coding = utf-8
# 2017.9.28

from to_log import *
import xlrd
from send_cmd import *

Pass = "'result': 'p'"
Fail = "'result': 'f'"


class cli_test():

    FailFlag = False

    def setting(self, c, data_file_name, sheet_name, hold_time=0):
        data = xlrd.open_workbook(data_file_name)
        table = data.sheet_by_name(sheet_name)

        for i in range(1, table.nrows):

            tolog('Expect: ' + table.cell(i, 1).value + '\r\n')
            result = SendCmd(c, table.cell(i, 0).value)
            time.sleep(hold_time)

            if 'Error (' in result:

                self.FailFlag = True
                tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

            else:
                check = SendCmd(c, table.cell(i, 2).value)

                for j in range(3, table.ncols):

                    if table.cell(i, j).value not in check:
                        self.FailFlag = True
                        tolog('\r\nFail: please check out ' + table.cell(i, j).value + '\r\n')

        if self.FailFlag:
            tolog(Fail)
            self.FailFlag = False
        else:
            tolog(Pass)

    def list(self, c, data_file_name, sheet_name):
        data = xlrd.open_workbook(data_file_name)
        table = data.sheet_by_name(sheet_name)

        for i in range(1, table.nrows):

            tolog('Expect: ' + table.cell(i, 1).value + '\r\n')
            result = SendCmd(c, table.cell(i, 0).value)

            if 'Error (' in result:

                self.FailFlag = True
                tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

            else:

                for j in range(2, table.ncols):

                    if table.cell(i, j).value not in result:
                        self.FailFlag = True
                        tolog('\r\nFail: please check out ' + table.cell(i, j).value + '\r\n')

        if self.FailFlag:
            tolog(Fail)
            self.FailFlag = False
        else:
            tolog(Pass)

    def other(self, c, data_file_name, sheet_name):
        data = xlrd.open_workbook(data_file_name)
        table = data.sheet_by_name(sheet_name)

        for i in range(1, table.nrows):

            tolog('Expect: ' + table.cell(i, 1).value + '\r\n')
            result = SendCmd(c, table.cell(i, 0).value)

            if 'Error (' in result:

                self.FailFlag = True
                tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

        if self.FailFlag:
            tolog(Fail)
            self.FailFlag = False
        else:
            tolog(Pass)

    def delete(self, c, data_file_name, sheet_name, hold_time=0):
        data = xlrd.open_workbook(data_file_name)
        table = data.sheet_by_name(sheet_name)

        for i in range(1, table.nrows):

            tolog('Expect: ' + table.cell(i, 1).value + '\r\n')
            result = SendCmd(c, table.cell(i, 0).value)
            time.sleep(hold_time)

            if 'Error (' in result:

                self.FailFlag = True
                tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

            else:
                check = SendCmd(c, table.cell(i, 2).value)

                for j in range(3, table.ncols):

                    if table.cell(i, j).value in check:
                        self.FailFlag = True
                        tolog('\r\nFail: please check out ' + table.cell(i, j).value + '\r\n')

        if self.FailFlag:
            tolog(Fail)
            self.FailFlag = False
        else:
            tolog(Pass)

    def failed_test(self, c, data_file_name, sheet_name, hold_time=0):
        data = xlrd.open_workbook(data_file_name)
        table = data.sheet_by_name(sheet_name)

        for i in range(1, table.nrows):

            tolog('Expect: ' + table.cell(i, 1).value + '\r\n')
            result = SendCmd(c, table.cell(i, 0).value)
            time.sleep(hold_time)

            if 'Error (' not in result:

                self.FailFlag = True
                tolog('\r\nFail: ' + table.cell(i, 0).value + '\r\n')

            else:

                if table.cell(i, 1).value not in result:
                    self.FailFlag = True
                    tolog('\r\nFail: please check out ' + table.cell(i, 1).value + '\r\n')

        if self.FailFlag:
            tolog(Fail)
            self.FailFlag = False
        else:
            tolog(Pass)

cli_test = cli_test()