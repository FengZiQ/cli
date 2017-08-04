# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
import random
import re
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyCtrl(c):
    FailFlag = False
    tolog("<b>Verify ctrl</b>")
    result = SendCmd(c, "ctrl")
    if "CtrlId" not in result or "Alias" not in result or "OperationalStatus" not in result or "ReadinessStatus" not in result or "is Primary" not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: ctrl</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ctrl</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyCtrlSpecifyId(c):
    FailFlag = False
    tolog("<b>Verify ctrl -i CtrlId </b>")
    for CtrlId in ['1', '2']:
        result = SendCmd(c, "ctrl -i " + CtrlId)
        if "CtrlId" not in result or "Alias" not in result or "OperationalStatus" not in result or "ReadinessStatus" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ctrl -i ' + CtrlId + '</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ctrl -i CtrlId</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyCtrlList(c):
    FailFlag = False
    tolog("<b>Verify ctrl -a list </b>")
    result = SendCmd(c, "ctrl -a list")
    if "Error (" in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: Verify ctrl -a list</font>')
    for CtrlId in ['1', '2']:
        tolog('Verify ctrl -a list -i ' + CtrlId)
        result = SendCmd(c, "ctrl -a list -i " + CtrlId)
        if "CtrlId" not in result or "Alias" not in result or "OperationalStatus" not in result or "ReadinessStatus" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ctrl -a list -i ' + CtrlId + '</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ctrl -a list</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyCtrlV(c):
    FailFlag = False
    result = SendCmd(c, 'ctrl -v')
    if "Error (" in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: ctrl -v </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ctrl -v</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyCtrlListV(c):
    FailFlag = False
    result = SendCmd(c, 'ctrl -a list -v')
    if "Error (" in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: ctrl -a list -v </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ctrl -a list -v</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyCtrlL(c):
    FailFlag = False
    tolog("<b>Verify ctrl -l </b>")
    result = SendCmd(c, "ctrl -l")
    if "LocalCtrlId: " not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: ctrl -l</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ctrl -l </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyCtrlModNormativeAlias(c):
    FailFlag = False
    tolog("<b> verify ctrl alias by character type and length </b>")
    ctrlInfo = SendCmd(c, "ctrl")
    for i in [4, 5]:
        row = ctrlInfo.split("\r\n")[i]
        if row.split()[-2] == "OK" or row.split()[-4][0:2] == "OK":
            CtrlID = row.split()[0]
            values = 'aaaa1aaaa2aaaa3aaaa4aaaa5aaaa6aaaa7aaaa8aaaa9aaa'
            result = SendCmd(c, "ctrl -a mod -i " + str(CtrlID) + ' -s "alias = ' + values + '"')
            checkResult = SendCmd(c, "ctrl -v -i " + str(CtrlID))
            if "Error (" in result or values not in checkResult:
                FailFlag = True
                tolog('\n<font color="red">Fail: ctrl -a mod -i ' + str(CtrlID) + ' -s "alias = ' + values + '" </font>')
            for values in ['test_12', '12_test', 'test 12', '_', '123', '  TEST  ']:
                result = SendCmd(c, "ctrl -a mod -i " + str(CtrlID) + " -s " + '"alias = ' + values + '"')
                checkResult = SendCmd(c, "ctrl -i " + str(CtrlID))
                if "Error (" in result or values not in checkResult:
                    FailFlag = True
                    tolog('\n<font color="red">Fail: ctrl -a mod -i ' + str(CtrlID) + " -s alias = " + values + '"</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ctrl -a mod -i CtrlId -s "alias = " </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyCtrlModValuesIsEnableOrDisable(c):
    FailFlag = False
    tolog('<b>Verify ctrl -a mod -i CtrlId -s "Option = enable or disable "  </b>')
    result = SendCmd(c, "ctrl")
    for index in [4, 5]:
        row = result.split("\r\n")[index]
        if row.split()[-2] == "OK" or row.split()[-4][0:2] == "OK":
            CtrlID = row.split()[0]
            for values in ['disable', 'enable']:
                tolog('\n<b> Verify ctrl -a mod -i ' + str(CtrlID) + '-s "VAAIsupport = ' + values + '" </b>')
                result = SendCmd(c, 'ctrl -a mod -i ' + str(CtrlID) + ' -s "VAAIsupport = ' + values + '"')
                if "Error (" in result or "The VAAIsupport setting will take affect only after next reboot" not in result:
                    FailFlag = True
                    tolog('\n<font color="red">Fail: ctrl -a mod -i ' + str(CtrlID) + '-s "VAAIsupport = ' + values + '" </font>')
            for values in ['disable', 'enable']:
                option = ["SMART = " + values,
                          "AdaptiveWBCache = " + values,
                          "HostCacheFlushing = " + values,
                          "ForcedReadAhead = " + values,
                          "SSDTrimSupport = " + values,
                          "Coercion = " + values,
                          ]
                for Op in option:
                    tolog('\n<b>Verify ctrl -a mod -s "' + Op + '" </b>')
                    SendCmd(c, "ctrl -a mod -i " + str(CtrlID) + " -s " + '"' + Op + '"')
                    result = SendCmd(c, "ctrl -v -i " + str(CtrlID))
                    if Op.split()[0] + ': ' + Op.split()[-1].capitalize() + 'd' not in result:
                        FailFlag = True
                        tolog('\n<font color="red">Fail: ctrl -a mod -s "' + Op + '" </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ctrl -a mod -i CtrlId -s "Option = enable or disable " </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyCtrlModValuesIsTime(c):
    FailFlag = False
    tolog('<b>Verify ctrl -a mod -i CtrlId -s "Option = Time " </b>')
    ctrlInfo = SendCmd(c, "ctrl")
    for index in [4, 5]:
        row = ctrlInfo.split("\r\n")[index]
        # 2             test         OK                       Active
        # 2             test         OK, BGA Running          Active
        if row.split()[-2] == "OK" or row.split()[-4][0:2] == "OK":
            CtrlID = row.split()[0]
            for option in ["powersavingidletime", "powersavingstandbytime", "powersavingstoppedtime"]:
                for values in [0, 15, 1380, 1440]:
                    result = SendCmd(c, "ctrl -a mod -i " + str(CtrlID) + " -s " + '"' + option + " = " + str(values) + '"')
                    if "Error" in result:
                        FailFlag = True
                        tolog('\n<font color="red">Fail: ctrl -a mod -i ' + str(CtrlID) + " -s " + '"' + option + " = " + str(values) + '"</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ctrl -a mod -i CtrlId -s "Option = Time " </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyCtrlModNonstandardValues(c):
    FailFlag = False
    tolog('<b>Verify ctrl -a mod -i CtrlId -s "Option = Nonstandard Values " </b>')
    result = SendCmd(c, "ctrl")
    for index in [4, 5]:
        row = result.split("\r\n")[index]
        if row.split()[-2] == "OK" or row.split()[-4][0:2] == "OK":
            CtrlID = row.split()[0]
            for values in ['123']:
                option = ["SMART = " + values,
                          "AdaptiveWBCache = " + values,
                          "HostCacheFlushing = " + values,
                          "ForcedReadAhead = " + values,
                          "SSDTrimSupport = " + values,
                          "VAAIsupport = " + values,
                          "Coercion = " + values,
                          ]
                for Op in option:
                    result = SendCmd(c, "ctrl -a mod -i " + str(CtrlID) + " -s " + '"' + Op + '"')
                    tolog("<b> ctrl -a mod -i " + str(CtrlID) + " -s " + '"' + Op + '" <\b>')
                    if "Error" not in result or "Invalid setting parameters" not in result:
                        FailFlag = True
                        tolog('\n<font color="red">Fail: ctrl -a mod -i ' + str(CtrlID) + ' -s ' + '"' + Op + '"</font>')

            for option in ["powersavingidletime", "powersavingstandbytime", "powersavingstoppedtime"]:
                for values in [-1, 1441]:
                    result = SendCmd(c, "ctrl -a mod -i " + str(CtrlID) + ' -s "' + option + " = " + str(values) + '"')
                    tolog('<b> ctrl -a mod -i ' + str(CtrlID) + ' -s "' + option + " = " + str(values) + '"</b>')
                    if "Error" not in result or "Invalid setting parameters" not in result:
                        FailFlag = True
                        tolog('\n<font color="red"> Fail: ctrl -a mod -i ' + str(CtrlID) + ' -s "' + option + " = " + str(values) + '"</font>')

            if row.split()[-2] == "OK" or row.split()[-4][0:2] == "OK":
                CtrlID = row.split()[0]
                for values in ['aaaa1aaaa2aaaa3aaaa4aaaa5aaaa6aaaa7aaaa8aaaa9aaaa']:
                    result = SendCmd(c, "ctrl -a mod -i " + str(CtrlID) + ' -s "alias = ' + values + '"')
                    if "Error (" not in result:
                        FailFlag = True
                        tolog('\n<font color="red">Fail: ' + "ctrl -a mod -i " + str(CtrlID) + '-s "alias = "' + values + '"</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ctrl -a mod -i CtrlId -s "Option = Nonstandard Values " </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyCtrlClear(c):
    FailFlag = False
    tolog('<b> Verify ctrl -a clear -i CtrlID -t watermark </b>')
    for ctrlID in [1, 2]:
        tolog('<b> verify ctrl -a clear -i '+str(ctrlID)+' -t watermark </b>')
        result = SendCmd(c, "ctrl -a clear -i "+str(ctrlID)+" -t watermark")
        if "Error" in result or "ctrl -a clear -i "+str(ctrlID)+" -t watermark" not in result:
            FailFlag = True
            tolog('\n<font color="red"> Fail: verify ctrl -a clear -i '+str(ctrlID)+' -t watermark </font>')
    tolog('<b> verify ctrl -a clear -t watermark </b>')
    result = SendCmd(c, "ctrl -a clear -t watermark")
    if "Error" in result or "ctrl -a clear -t watermark" not in result:
        FailFlag = True
        tolog('\n<font color="red"> Fail: verify ctrl -a clear -t watermark </font>')
    for ctrlID in [1, 2]:
        tolog("<b>verify ctrl -a clear -t watermark -i " + str(ctrlID) + '</b>')
        result = SendCmd(c, "ctrl -a clear -t watermark -i "+str(ctrlID))
        if "Error" in result or "ctrl -a clear -t watermark -i "+str(ctrlID) not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: verify ctrl -a clear -t watermark -i ' + str(ctrlID) + '</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ctrl -a clear -i CtrlID -t watermark  </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyCtrlHelp(c):
    FailFlag = False
    tolog("<b> Verify ctrl -h </b>")
    result = SendCmd(c, "ctrl -h")
    if "Usage" not in result or "Summary" not in result or "ctrl" not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: ctrl -h </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ctrl -h  </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyCtrlSpecifyInexistentId(c):
    FailFlag = False
    tolog("<b>Verify ctrl specify inexistent CtrlId</b>")
    command = ['ctrl -v -i 5', 'ctrl -a list -i 5', 'ctrl -a mod -i 5 -s "alias = test"', 'ctrl -a clear -i 5 -t watermark ']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "-i: invalid setting 5 (1,2)" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ctrl specify inexistent CtrlId </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyCtrlInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify ctrl invalid option</b>")
    command = ['ctrl -x', 'ctrl -a list -x', 'ctrl -a mod -x', 'ctrl -a clear -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ctrl invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyCtrlInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify ctrl invalid parameters</b>")
    command = ['ctrl test', 'ctrl -a test', 'ctrl -a mod -s test', 'ctrl -a clear -t test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ctrl invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyCtrlMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify ctrl missing parameters</b>")
    command = ['ctrl -v -i', 'ctrl -a list -i', 'ctrl -a mod -s', 'ctrl -a clear -t']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify ctrl missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def bvt_verifyCtrl(c):
    FailFlag = False
    tolog("Verify ctrl")
    result = SendCmd(c, "ctrl")
    if "CtrlId" not in result or "Alias" not in result or "OperationalStatus" not in result or "ReadinessStatus" not in result or "is Primary" not in result:
        FailFlag = True
        tolog('Fail: ctrl')

    return FailFlag

def bvt_verifyCtrlSpecifyId(c):
    FailFlag = False
    tolog("Verify ctrl -i CtrlId ")
    for CtrlId in ['1', '2']:
        result = SendCmd(c, "ctrl -i " + CtrlId)
        if "CtrlId" not in result or "Alias" not in result or "OperationalStatus" not in result or "ReadinessStatus" not in result:
            FailFlag = True
            tolog('Fail: ctrl -i ' + CtrlId + '')

    return FailFlag

def bvt_verifyCtrlList(c):
    FailFlag = False
    tolog("Verify ctrl -a list ")
    result = SendCmd(c, "ctrl -a list")
    if "Error (" in result:
        FailFlag = True
        tolog('Fail: Verify ctrl -a list')

    for CtrlId in ['1', '2']:
        tolog('Verify ctrl -a list -i ' + CtrlId)
        result = SendCmd(c, "ctrl -a list -i " + CtrlId)
        if "CtrlId" not in result or "Alias" not in result or "OperationalStatus" not in result or "ReadinessStatus" not in result:
            FailFlag = True
            tolog('Fail: ctrl -a list -i ' + CtrlId + '')

    return FailFlag

def bvt_verifyCtrlV(c):
    FailFlag = False
    result = SendCmd(c, 'ctrl -v')
    if "Error (" in result:
        FailFlag = True
        tolog('Fail: ctrl -v ')

    return FailFlag

def bvt_verifyCtrlListV(c):
    FailFlag = False
    result = SendCmd(c, 'ctrl -a list -v')
    if "Error (" in result:
        FailFlag = True
        tolog('Fail: ctrl -a list -v ')

    return FailFlag

def bvt_verifyCtrlL(c):
    FailFlag = False
    tolog("Verify ctrl -l ")
    result = SendCmd(c, "ctrl -l")
    if "LocalCtrlId: " not in result:
        FailFlag = True
        tolog('Fail: ctrl -l')

    return FailFlag

def bvt_verifyCtrlModNormativeAlias(c):
    FailFlag = False
    tolog(" verify ctrl alias by character type and length  ")
    result = SendCmd(c, "ctrl")
    for index in [4, 5]:
        row = result.split("\r\n")[index]
        if row.split()[-2] == "OK" or row.split()[-4][0:2] == "OK":
            CtrlID = row.split()[0]
            values = 'aaaa1aaaa2aaaa3aaaa4aaaa5aaaa6aaaa7aaaa8aaaa9aaa'
            result = SendCmd(c, "ctrl -a mod -i " + str(CtrlID) + ' -s "alias = ' + values + '"')
            checkResult = SendCmd(c, "ctrl -v -i " + str(CtrlID))
            if "Error (" in result or values not in checkResult:
                FailFlag = True
                tolog('Fail: ctrl -a mod -i ' + str(CtrlID) + ' -s "alias = ' + values + '" ')
            for values in ['test_12', '12_test', 'test 12', '_', '123', '  TEST  ']:
                result = SendCmd(c, "ctrl -a mod -i " + str(CtrlID) + " -s " + '"alias = ' + values + '"')
                checkResult = SendCmd(c, "ctrl -i " + str(CtrlID))
                if "Error (" in result or values not in checkResult:
                    FailFlag = True
                    tolog('Fail: ctrl -a mod -i ' + str(CtrlID) + " -s alias = " + values + '"')

    return FailFlag

def bvt_verifyCtrlModValuesIsEnableOrDisable(c):
    FailFlag = False
    tolog('Verify ctrl -a mod -i CtrlId -s "Option = enable or disable "  ')
    result = SendCmd(c, "ctrl")
    for index in [4, 5]:
        row = result.split("\r\n")[index]
        if row.split()[-2] == "OK" or row.split()[-4][0:2] == "OK":
            CtrlID = row.split()[0]
            for values in ['disable', 'enable']:
                tolog('\n Verify ctrl -a mod -i ' + str(CtrlID) + '-s "VAAIsupport = ' + values + '" ')
                result = SendCmd(c, 'ctrl -a mod -i ' + str(CtrlID) + ' -s "VAAIsupport = ' + values + '"')
                if "Error (" in result or "The VAAIsupport setting will take affect only after next reboot" not in result:
                    FailFlag = True
                    tolog('Fail: ctrl -a mod -i ' + str(CtrlID) + '-s "VAAIsupport = ' + values + '" ')
            for values in ['disable', 'enable']:
                option = ["SMART = " + values,
                          "AdaptiveWBCache = " + values,
                          "HostCacheFlushing = " + values,
                          "ForcedReadAhead = " + values,
                          "SSDTrimSupport = " + values,
                          "Coercion = " + values,
                          ]
                for Op in option:
                    tolog('\nVerify ctrl -a mod -s "' + Op + '" ')
                    SendCmd(c, "ctrl -a mod -i " + str(CtrlID) + " -s " + '"' + Op + '"')
                    result = SendCmd(c, "ctrl -v -i " + str(CtrlID))
                    if Op.split()[0] + ': ' + Op.split()[-1].capitalize() + 'd' not in result:
                        FailFlag = True
                        tolog('Fail: ctrl -a mod -s "' + Op + '" ')

    return FailFlag

def bvt_verifyCtrlModValuesIsTime(c):
    FailFlag = False
    tolog('Verify ctrl -a mod -i CtrlId -s "Option = Time " ')
    result = SendCmd(c, "ctrl")
    for index in [4, 5]:
        row = result.split("\r\n")[index]
        # 2             test         OK                       Active
        # 2             test         OK, BGA Running          Active
        if row.split()[-2] == "OK" or row.split()[-4][0:2] == "OK":
            CtrlID = row.split()[0]
            for option in ["powersavingidletime", "powersavingstandbytime", "powersavingstoppedtime"]:
                for values in [0, 15, 1380, 1440]:
                    result = SendCmd(c, "ctrl -a mod -i " + str(CtrlID) + " -s " + '"' + option + " = " + str(values) + '"')
                    if "Error" in result:
                        FailFlag = True
                        tolog('Fail: ctrl -a mod -i ' + str(CtrlID) + " -s " + '"' + option + " = " + str(values) + '"')

    return FailFlag

def bvt_verifyCtrlClear(c):
    FailFlag = False
    tolog(' Verify ctrl -a clear -i CtrlID -t watermark ')
    for ctrlID in [1, 2]:
        tolog(' verify ctrl -a clear -i '+str(ctrlID)+' -t watermark ')
        result = SendCmd(c, "ctrl -a clear -i "+str(ctrlID)+" -t watermark")
        if "Error" in result or "ctrl -a clear -i "+str(ctrlID)+" -t watermark" not in result:
            FailFlag = True
            tolog(' Fail: verify ctrl -a clear -i '+str(ctrlID)+' -t watermark ')

    tolog(' verify ctrl -a clear -t watermark ')
    result = SendCmd(c, "ctrl -a clear -t watermark")
    if "Error" in result or "ctrl -a clear -t watermark" not in result:
        FailFlag = True
        tolog(' Fail: verify ctrl -a clear -t watermark ')

    for ctrlID in [1, 2]:
        tolog("verify ctrl -a clear -t watermark -i " + str(ctrlID) + '')
        result = SendCmd(c, "ctrl -a clear -t watermark -i "+str(ctrlID))
        if "Error" in result or "ctrl -a clear -t watermark -i "+str(ctrlID) not in result:
            FailFlag = True
            tolog('Fail: verify ctrl -a clear -t watermark -i ' + str(ctrlID) + '')

    return FailFlag

def bvt_verifyCtrlHelp(c):
    FailFlag = False
    tolog(" Verify ctrl -h ")
    result = SendCmd(c, "ctrl -h")
    if "Usage" not in result or "Summary" not in result or "ctrl" not in result:
        FailFlag = True
        tolog('Fail: ctrl -h ')

    return FailFlag

def bvt_verifyCtrlSpecifyInexistentId(c):
    FailFlag = False
    tolog("Verify ctrl specify inexistent CtrlId")
    command = ['ctrl -v -i 5', 'ctrl -a list -i 5', 'ctrl -a mod -i 5 -s "alias = test"', 'ctrl -a clear -i 5 -t watermark ']
    for com in command:
        tolog(' Verify ' + com + '')
        result = SendCmd(c, com)
        if "Error (" not in result or "-i: invalid setting 5 (1,2)" not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    return FailFlag

def bvt_verifyCtrlInvalidOption(c):
    FailFlag = False
    tolog("Verify ctrl invalid option")
    command = ['ctrl -x', 'ctrl -a list -x', 'ctrl -a mod -x', 'ctrl -a clear -x']
    for com in command:
        tolog(' Verify ' + com + '')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    return FailFlag

def bvt_verifyCtrlInvalidParameters(c):
    FailFlag = False
    tolog("Verify ctrl invalid parameters")
    command = ['ctrl test', 'ctrl -a test', 'ctrl -a mod -s test', 'ctrl -a clear -t test']
    for com in command:
        tolog(' Verify ' + com + '')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    return FailFlag

def bvt_verifyCtrlMissingParameters(c):
    FailFlag = False
    tolog("Verify ctrl missing parameters")
    command = ['ctrl -v -i', 'ctrl -a list -i', 'ctrl -a mod -s', 'ctrl -a clear -t']
    for com in command:
        tolog(' Verify ' + com + '')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('Fail: ' + com + ' ')

    return FailFlag



if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    bvt_verifyCtrl(c)
    bvt_verifyCtrlSpecifyId(c)
    bvt_verifyCtrlSpecifyInexistentId(c)
    bvt_verifyCtrlList(c)
    bvt_verifyCtrlV(c)
    bvt_verifyCtrlListV(c)
    bvt_verifyCtrlModNormativeAlias(c)
    bvt_verifyCtrlModValuesIsEnableOrDisable(c)
    bvt_verifyCtrlModValuesIsTime(c)
    bvt_verifyCtrlClear(c)
    bvt_verifyCtrlHelp(c)
    bvt_verifyCtrlInvalidOption(c)
    bvt_verifyCtrlInvalidParameters(c)
    bvt_verifyCtrlMissingParameters(c)
    bvt_verifyCtrlSpecifyInexistentId(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped