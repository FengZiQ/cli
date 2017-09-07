# coding=utf-8

from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn

Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyNtpMod(c):
    FailFlag = False
    tolog("Verify ntp -a mod")
    
    values = [
        '13:00',
        '-12:00',
        'enable',
        'enable',
        'Jan-1st-Sun',
        'Dec-Last-Sat',
        'Jun-3rd-Wed',
        'Oct-Last-Sat',
        'disable',
        'disable'
    ]

    tolog(' modify NTP dst disable ')
    
    for v in values[8:10]:
        tolog('' + 'ntp -a mod -s "ntp=' + v + '"' + '')
        
        result = SendCmd(c, 'ntp -a mod -s "ntp=' + v + '"')
        
        checkResult = SendCmd(c, 'ntp')
        
        if 'Error (' in result or 'Ntp: Disabled' not in checkResult:
            FailFlag = True
            tolog(' Fail: ' + 'ntp -a mod -s "ntp=' + v + '"' )

    SendCmd(c, 'ntp -a mod -s "ntp=enable,timezone=5:00,server1=210.72.145.44"')
    checkResult = SendCmd(c, 'ntp')
    
    if 'Ntp: Enabled' not in checkResult or "210.72.145.44" not in checkResult:
        FailFlag = True
        tolog('Fail: ntp -a mod -s "ntp=enable,timezone=5:00,server1=210.72.145.44"')

    tolog(' modify NTP server timezone')
    
    for v in values[:2]:
        tolog('Verify: ntp -a mod -s "timezone=' + v + '"')
        
        result = SendCmd(c, 'ntp -a mod -s "timezone=' + v + '"')
        checkResult = SendCmd(c, 'ntp')
        
        if v not in checkResult:
            FailFlag = True
            tolog(' Fail: ' + 'ntp -a mod -s "timezone=' + v + '"' )

    tolog(' modify NTP dst enable ')
    
    for v in values[2:4]:
        tolog('' + 'ntp -a mod -s "dst=' + v + '"' + '')
        
        result = SendCmd(c, 'ntp -a mod -s "dst=' + v + '"')
        checkResult = SendCmd(c, 'ntp')
        
        if 'Dst: Enabled' not in checkResult:
            FailFlag = True
            tolog(' Fail: ' + 'ntp -a mod -s "dst=' + v + '"' )

    tolog(' modify dststarttime settings ')
    
    for v in values[4:6]:
        tolog('' + 'ntp -a mod -s "dststarttime=' + v + '"' + '')
        
        result = SendCmd(c, 'ntp -a mod -s "dststarttime=' + v + '"')
        checkResult = SendCmd(c, 'ntp')
        
        if v not in checkResult:
            FailFlag = True
            tolog(' Fail: ' + 'ntp -a mod -s "dststarttime=' + v + '"' )

    tolog(' modify dstendtime settings ')
    
    for v in values[6:8]:
        tolog('ntp -a mod -s "dstendtime=' + v + '"')
        
        result = SendCmd(c, 'ntp -a mod -s "dstendtime=' + v + '"')
        checkResult = SendCmd(c, 'ntp')
        
        if v not in checkResult:
            FailFlag = True
            tolog(' Fail: ' + 'ntp -a mod -s "dstendtime=' + v + '"')
            
    if FailFlag:
        tolog('\n<font color="red">Fail:ntp -a mod </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyNtp(c):
    FailFlag = False
    tolog("Verify ntp ")
    
    result = SendCmd(c, 'ntp')
    
    if 'Error (' in result:
        FailFlag = True
        tolog(' Fail: ntp ')
    
    if FailFlag:
        tolog('\n<font color="red">Fail: ntp </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
        
    return FailFlag

def verifyNtpList(c):
    FailFlag = False
    tolog("Verify ntp -a list ")
    
    result = SendCmd(c, 'ntp -a list')
    
    if 'Error (' in result:
        FailFlag = True
        tolog(' Fail: ntp -a list ')

    if FailFlag:
        tolog('\n<font color="red">Fail: ntp -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
        
    return FailFlag

def verifyNtpTest(c):
    FailFlag = False
    tolog("Verify ntp -a test")
    
    result = SendCmd(c, 'ntp -a test -t 131.107.1.10'), SendCmd(c, 'ntp -a test -t abc')
    
    if 'unexpected error' in result:
        FailFlag = True
        tolog('\n Verify ntp -a test ')

    if FailFlag:
        tolog('\n<font color="red">Fail: ntp -a test</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyNtpSync(c):
    FailFlag = False
    tolog('\n Manual testing ')

    return FailFlag

def verifyNtpInvalidOption(c):
    FailFlag = False
    tolog("Verify ntp invalid option")
    
    command = [
        'ntp -x',
        'ntp -a list -x',
        'ntp -a mod -x',
        'ntp -a test -x',
        'ntp -a sync -x'
    ]
    
    for com in command:
        tolog(' Verify ' + com + '')
        
        result = SendCmd(c, com)
        
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('Fail: ' + com )
    
    if FailFlag:
        tolog('\n<font color="red">Fail: ntp Invalid Option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyNtpInvalidParameters(c):
    FailFlag = False
    tolog("Verify ntp invalid parameters")
    
    command = [
        'ntp test',
        'ntp -a list test', 
        'ntp -a mod test', 
        'ntp -a test test', 
        'ntp -a sync test', 
        'ntp -a mod -s "dststarttime=enable"'
    ]
    
    for com in command:
        tolog(' Verify ' + com + '')
        
        result = SendCmd(c, com)
        
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('Fail: ' + com )

    if FailFlag:
        tolog('\n<font color="red">Fail: ntp Invalid setting parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyNtpMissingParameters(c):
    FailFlag = False
    tolog("Verify ntp missing parameters")
    
    command = [
        'ntp -a mod -s', 
        'ntp -a ',
        'ntp -a test -t'
    ]
    
    for com in command:
        tolog(' Verify ' + com + '')
        
        result = SendCmd(c, com)
        
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('Fail: ' + com )
    
    if FailFlag:
        tolog('\n<font color="red">Fail: ntp Missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
    
    return FailFlag


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyNtpMod(c)
    verifyNtp(c)
    verifyNtpList(c)
    verifyNtpTest(c)
    verifyNtpSync(c)
    verifyNtpInvalidOption(c)
    verifyNtpInvalidParameters(c)
    verifyNtpMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped