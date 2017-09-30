# coding = utf-8
# 2017.9.28

from to_log import *

Pass = "'result': 'p'"
Fail = "'result': 'f'"


class Command():

    FailFlag = False

    def result(self):
        if self.FailFlag:
            tolog(Fail)
        else:
            tolog(Pass)


command = Command()