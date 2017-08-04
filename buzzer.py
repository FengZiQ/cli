# coding=utf-8
# initial sample work on 2016.12.23
# this section includes verify proper cmd/parameters/options and
# some other boundary or misspelled parameters/options
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
import random
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyBuzzerEnableAndSilentTurnOn(c):
    FailFlag = False
    tolog('<b>Verify buzz -a on</b>')
    SendCmd(c, "buzz -a enable"), SendCmd(c, "buzz -a off")
    result = SendCmd(c, "buzz -a on")
    checkResult = SendCmd(c, "buzz")
    if 'Error' in result or 'Sounding' not in checkResult or 'Yes' not in checkResult:
        FailFlag = True
        tolog('\n<font color="red">Fail: buzz -a on</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify buzz -a on </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBuzzerEnableAndSoundingTurnOn(c):
    FailFlag = False
    tolog('<b>Verify buzz -a on</b>')
    SendCmd(c, "buzz -a enable"), SendCmd(c, "buzz -a on")
    result = SendCmd(c, "buzz -a on")
    checkResult = SendCmd(c, "buzz")
    if 'Error' in result or 'Sounding' not in checkResult or 'Yes' not in checkResult:
        FailFlag = True
        tolog('\n<font color="red">Fail: buzz -a on</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify buzz -a on </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBuzzerDisableAndSilentTurnOn(c):
    FailFlag = False
    tolog('<b>Verify buzz -a on</b>')
    SendCmd(c, "buzz -a disable")
    result = SendCmd(c, "buzz -a on")
    if "Error (" not in result or "Buzzer is disabled" not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: buzz -a on</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify buzz -a on </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBuzzerEnableAndSoundingTurnOff(c):
    FailFlag = False
    tolog('<b>Verify buzz -a off</b>')
    SendCmd(c, "buzz -a enable"), SendCmd(c, "buzz -a on")
    result = SendCmd(c, "buzz -a off")
    checkResult = SendCmd(c, "buzz")
    if 'Error' in result or 'Silent' not in checkResult or 'Yes' not in checkResult:
        FailFlag = True
        tolog('\n<font color="red">Fail: buzz -a off</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify buzz -a off </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBuzzerEnableAndSilentTurnOff(c):
    FailFlag = False
    tolog('<b>Verify buzz -a off</b>')
    SendCmd(c, "buzz -a enable"), SendCmd(c, "buzz -a off")
    result = SendCmd(c, "buzz -a off")
    checkResult = SendCmd(c, "buzz")
    if 'Error' in result or 'Silent' not in checkResult or 'Yes' not in checkResult:
        FailFlag = True
        tolog('\n<font color="red">Fail: buzz -a off</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify buzz -a off </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBuzzerDisableAndSilentTurnOff(c):
    FailFlag = False
    tolog('<b>Verify buzz -a off</b>')
    SendCmd(c, "buzz -a disable")
    result = SendCmd(c, "buzz -a off")
    checkResult = SendCmd(c, "buzz")
    if "Error (" in result or "No" not in checkResult or "Silent" not in checkResult:
        FailFlag = True
        tolog('\n<font color="red">Fail: buzz -a off</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify buzz -a off </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBuzzerDisableAndSilentEnable(c):
    FailFlag = False
    tolog('<b>Verify buzz -a enable</b>')
    SendCmd(c, "buzz -a disable")
    result = SendCmd(c, "buzz -a enable")
    checkResult = SendCmd(c, "buzz")
    if "Error (" in result or "Yes" not in checkResult or "Silent" not in checkResult:
        FailFlag = True
        tolog('\n<font color="red">Fail: buzz -a enable</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify buzz -a enable </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBuzzerEnableAndSilentEnable(c):
    FailFlag = False
    tolog('<b>Verify buzz -a enable</b>')
    SendCmd(c, "buzz -a enable"), SendCmd(c, "buzz -a off")
    result = SendCmd(c, "buzz -a enable")
    checkResult = SendCmd(c, "buzz")
    if 'Error (' in result or 'Silent' not in checkResult or 'Yes' not in checkResult:
        FailFlag = True
        tolog('\n<font color="red">Fail: buzz -a enable</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify buzz -a enable </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBuzzerEnableAndSoundingEnable(c):
    FailFlag = False
    tolog('<b>Verify buzz -a enable</b>')
    SendCmd(c, "buzz -a enable"), SendCmd(c, "buzz -a on")
    result = SendCmd(c, "buzz -a enable")
    checkResult = SendCmd(c, "buzz")
    if 'Error (' in result or 'Sounding' not in checkResult or 'Yes' not in checkResult:
        FailFlag = True
        tolog('\n<font color="red">Fail: buzz -a enable</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify buzz -a enable </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBuzzerEnableAndSoundingDisable(c):
    FailFlag = False
    tolog('<b>Verify buzz -a disable</b>')
    SendCmd(c, "buzz -a enable"), SendCmd(c, "buzz -a on")
    result = SendCmd(c, "buzz -a disable")
    checkResult = SendCmd(c, "buzz")
    if 'Error (' in result or 'Silent' not in checkResult or 'No' not in checkResult:
        FailFlag = True
        tolog('\n<font color="red">Fail: buzz -a disable</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify buzz -a disable </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBuzzerEnableAndSilentDisable(c):
    FailFlag = False
    tolog('<b>Verify buzz -a disable</b>')
    SendCmd(c, "buzz -a enable"), SendCmd(c, "buzz -a off")
    result = SendCmd(c, "buzz -a disable")
    checkResult = SendCmd(c, "buzz")
    if 'Error (' in result or 'Silent' not in checkResult or 'No' not in checkResult:
        FailFlag = True
        tolog('\n<font color="red">Fail: buzz -a disable</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify buzz -a disable </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBuzzerDisableAndSilentDisable(c):
    FailFlag = False
    tolog('<b>Verify buzz -a disable</b>')
    SendCmd(c, "buzz -a disable")
    result = SendCmd(c, "buzz -a disable")
    checkResult = SendCmd(c, "buzz")
    if "Error (" in result or "No" not in checkResult or "Silent" not in checkResult:
        FailFlag = True
        tolog('\n<font color="red">Fail: buzz -a disable </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify buzz -a disable </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBuzzerInfo(c):
    FailFlag = False
    tolog('<b>Verify buzz</b>')
    result = SendCmd(c, 'buzz')
    if "Error (" in result or "Enabled" not in result or "Status" not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: buzz</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify buzz </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBuzzerHelp(c):
    FailFlag = False
    tolog('<b>Verify buzz -h </b>')
    result = SendCmd(c, 'buzz -h')
    if "Error (" in result or "buzz" not in result or "Usage" not in result or "Summary" not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: buzz -h</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify buzz -h</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBuzzerInvalidParameters(c):
    FailFlag = False
    tolog('<b>Verify buzzer abc</b>')
    result = SendCmd(c, 'buzz abc')
    if "Error (" not in result or "parameters" not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: buzz abc</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify buzz abc </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyBuzzerInvalidOption(c):
    FailFlag = False
    tolog('<b>Verify buzzer -x</b>')
    result = SendCmd(c, 'buzz -x')
    if "Error (" not in result or "Invalid option" not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: buzz -x</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify buzz -x </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


def bvt_verifyBuzzerEnableAndSilentTurnOn(c):
    FailFlag = False
    tolog('Verify buzz -a on')
    SendCmd(c, "buzz -a enable"), SendCmd(c, "buzz -a off")
    result = SendCmd(c, "buzz -a on")
    checkResult = SendCmd(c, "buzz")
    if 'Error' in result or 'Sounding' not in checkResult or 'Yes' not in checkResult:
        FailFlag = True
        tolog('Fail: buzz -a on')

    return FailFlag

def bvt_verifyBuzzerEnableAndSoundingTurnOn(c):
    FailFlag = False
    tolog('Verify buzz -a on')
    SendCmd(c, "buzz -a enable"), SendCmd(c, "buzz -a on")
    result = SendCmd(c, "buzz -a on")
    checkResult = SendCmd(c, "buzz")
    if 'Error' in result or 'Sounding' not in checkResult or 'Yes' not in checkResult:
        FailFlag = True
        tolog('Fail: buzz -a on')

    return FailFlag

def bvt_verifyBuzzerDisableAndSilentTurnOn(c):
    FailFlag = False
    tolog('Verify buzz -a on')
    SendCmd(c, "buzz -a disable")
    result = SendCmd(c, "buzz -a on")
    if "Error (" not in result or "Buzzer is disabled" not in result:
        FailFlag = True
        tolog('Fail: buzz -a on')

    return FailFlag

def bvt_verifyBuzzerEnableAndSoundingTurnOff(c):
    FailFlag = False
    tolog('Verify buzz -a off')
    SendCmd(c, "buzz -a enable"), SendCmd(c, "buzz -a on")
    result = SendCmd(c, "buzz -a off")
    checkResult = SendCmd(c, "buzz")
    if 'Error' in result or 'Silent' not in checkResult or 'Yes' not in checkResult:
        FailFlag = True
        tolog('Fail: buzz -a off')

    return FailFlag

def bvt_verifyBuzzerEnableAndSilentTurnOff(c):
    FailFlag = False
    tolog('Verify buzz -a off')
    SendCmd(c, "buzz -a enable"), SendCmd(c, "buzz -a off")
    result = SendCmd(c, "buzz -a off")
    checkResult = SendCmd(c, "buzz")
    if 'Error' in result or 'Silent' not in checkResult or 'Yes' not in checkResult:
        FailFlag = True
        tolog('Fail: buzz -a off')

    return FailFlag

def bvt_verifyBuzzerDisableAndSilentTurnOff(c):
    FailFlag = False
    tolog('Verify buzz -a off')
    SendCmd(c, "buzz -a disable")
    result = SendCmd(c, "buzz -a off")
    checkResult = SendCmd(c, "buzz")
    if "Error (" in result or "No" not in checkResult or "Silent" not in checkResult:
        FailFlag = True
        tolog('Fail: buzz -a off')

    return FailFlag

def bvt_verifyBuzzerDisableAndSilentEnable(c):
    FailFlag = False
    tolog('Verify buzz -a enable')
    SendCmd(c, "buzz -a disable")
    result = SendCmd(c, "buzz -a enable")
    checkResult = SendCmd(c, "buzz")
    if "Error (" in result or "Yes" not in checkResult or "Silent" not in checkResult:
        FailFlag = True
        tolog('Fail: buzz -a enable')

    return FailFlag

def bvt_verifyBuzzerEnableAndSilentEnable(c):
    FailFlag = False
    tolog('Verify buzz -a enable')
    SendCmd(c, "buzz -a enable"), SendCmd(c, "buzz -a off")
    result = SendCmd(c, "buzz -a enable")
    checkResult = SendCmd(c, "buzz")
    if 'Error (' in result or 'Silent' not in checkResult or 'Yes' not in checkResult:
        FailFlag = True
        tolog('Fail: buzz -a enable')

    return FailFlag

def bvt_verifyBuzzerEnableAndSoundingEnable(c):
    FailFlag = False
    tolog('Verify buzz -a enable')
    SendCmd(c, "buzz -a enable"), SendCmd(c, "buzz -a on")
    result = SendCmd(c, "buzz -a enable")
    checkResult = SendCmd(c, "buzz")
    if 'Error (' in result or 'Sounding' not in checkResult or 'Yes' not in checkResult:
        FailFlag = True
        tolog('Fail: buzz -a enable')

    return FailFlag

def bvt_verifyBuzzerEnableAndSoundingDisable(c):
    FailFlag = False
    tolog('Verify buzz -a disable')
    SendCmd(c, "buzz -a enable"), SendCmd(c, "buzz -a on")
    result = SendCmd(c, "buzz -a disable")
    checkResult = SendCmd(c, "buzz")
    if 'Error (' in result or 'Silent' not in checkResult or 'No' not in checkResult:
        FailFlag = True
        tolog('Fail: buzz -a disable')

    return FailFlag

def bvt_verifyBuzzerEnableAndSilentDisable(c):
    FailFlag = False
    tolog('Verify buzz -a disable')
    SendCmd(c, "buzz -a enable"), SendCmd(c, "buzz -a off")
    result = SendCmd(c, "buzz -a disable")
    checkResult = SendCmd(c, "buzz")
    if 'Error (' in result or 'Silent' not in checkResult or 'No' not in checkResult:
        FailFlag = True
        tolog('Fail: buzz -a disable')

    return FailFlag

def bvt_verifyBuzzerDisableAndSilentDisable(c):
    FailFlag = False
    tolog('Verify buzz -a disable')
    SendCmd(c, "buzz -a disable")
    result = SendCmd(c, "buzz -a disable")
    checkResult = SendCmd(c, "buzz")
    if "Error (" in result or "No" not in checkResult or "Silent" not in checkResult:
        FailFlag = True
        tolog('Fail: buzz -a disable ')

    return FailFlag

def bvt_verifyBuzzerInfo(c):
    FailFlag = False
    tolog('Verify buzz')
    result = SendCmd(c, 'buzz')
    if "Error (" in result or "Enabled" not in result or "Status" not in result:
        FailFlag = True
        tolog('Fail: buzz')

    return FailFlag

def bvt_verifyBuzzerHelp(c):
    FailFlag = False
    tolog('Verify buzz -h ')
    result = SendCmd(c, 'buzz -h')
    if "Error (" in result or "buzz" not in result or "Usage" not in result or "Summary" not in result:
        FailFlag = True
        tolog('Fail: buzz -h')

    return FailFlag

def bvt_verifyBuzzerInvalidParameters(c):
    FailFlag = False
    tolog('Verify buzzer abc')
    result = SendCmd(c, 'buzz abc')
    if "Error (" not in result or "parameters" not in result:
        FailFlag = True
        tolog('Fail: buzz abc')

    return FailFlag

def bvt_verifyBuzzerInvalidOption(c):
    FailFlag = False
    tolog('Verify buzzer -x')
    result = SendCmd(c, 'buzz -x')
    if "Error (" not in result or "Invalid option" not in result:
        FailFlag = True
        tolog('Fail: buzz -x')

    return FailFlag



if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    bvt_verifyBuzzerDisableAndSilentTurnOn(c)
    bvt_verifyBuzzerEnableAndSilentTurnOn(c)
    bvt_verifyBuzzerEnableAndSoundingTurnOn(c)
    bvt_verifyBuzzerDisableAndSilentTurnOff(c)
    bvt_verifyBuzzerEnableAndSilentTurnOff(c)
    bvt_verifyBuzzerEnableAndSoundingTurnOff(c)
    bvt_verifyBuzzerDisableAndSilentEnable(c)
    bvt_verifyBuzzerEnableAndSilentEnable(c)
    bvt_verifyBuzzerEnableAndSoundingEnable(c)
    bvt_verifyBuzzerEnableAndSoundingDisable(c)
    bvt_verifyBuzzerEnableAndSilentDisable(c)
    bvt_verifyBuzzerDisableAndSilentDisable(c)
    bvt_verifyBuzzerInfo(c)
    bvt_verifyBuzzerHelp(c)
    bvt_verifyBuzzerInvalidParameters(c)
    bvt_verifyBuzzerInvalidOption(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped