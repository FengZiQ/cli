# coding=utf-8

from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
import random

Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyEvent(c):
    FailFlag = False
    tolog("<b>Verify event </b>")
    
    result = SendCmd(c, 'event')
    
    if 'Error (' in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: event </font>')

    tolog("<b>Verify event id is continuous </b>")
    
    eventId = []
    checkResult = ''
    
    row = result.split("\r\n")
    
    for x in range(4, len(row) - 1):
        if len(row[x].split()) > 6:
            eventId.append(row[x].split()[0])
            
    for i in range(0, len(eventId) - 1):
        checkResult = checkResult + '  ' + eventId[i]
        
        if int(eventId[i]) + 1 != int(eventId[i + 1]):
            FailFlag = True
            tolog('\n<font color="red">Fail: event id is not continuous</font>')
    
    tolog('<b>' + checkResult + '</b>')

    tolog("<b>Verify event -i id -c count</b>")
    
    eId = random.choice(eventId)
    
    for count in ['1', '65535']:
        result = SendCmd(c, 'event -i ' + eId + ' -c ' + count)
        
        if 'Error (' in result or eId not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: event -i ' + eId + ' -c' + count + '</font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify event </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
        
    return FailFlag

def verifyEventList(c):
    FailFlag = False
    tolog("<b>Verify event -a list</b>")
    
    result = SendCmd(c, 'event -a list')
    
    if 'Error (' in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: event -a list </font>')

    tolog("<b>Verify event id is continuous </b>")
    
    eventId = []
    checkResult = ''
    
    row = result.split("\r\n")
    
    for x in range(4, len(row) - 1):
        if len(row[x].split()) > 6:
            eventId.append(row[x].split()[0])
            
    for i in range(0, len(eventId) - 1):
        checkResult = checkResult + '  ' + eventId[i]
        
        if int(eventId[i]) + 1 != int(eventId[i + 1]):
            FailFlag = True
            tolog('\n<font color="red">Fail: event id is not continuous</font>')
    
    tolog('<b>' + checkResult + '</b>')

    tolog("<b>Verify event -a list -i id -c count</b>")
    
    eId = random.choice(eventId)
    
    for count in ['1', '65535']:
        result = SendCmd(c, 'event -a list -i ' + eId + ' -c ' + count)
        
        if 'Error (' in result or eId not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: event -a list -i ' + eId + ' -c' + count + '</font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify event -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
        
    return FailFlag

def verifyEventClear(c):
    FailFlag = False
    tolog("<b>Verify event -a clear</b>")
    
    result = SendCmd(c, 'event -a clear')
    checkResult = SendCmd(c, 'event')
    
    if 'Error (' in result or 'Clear event log' not in checkResult or 'successfully' not in checkResult:
        FailFlag = True
        tolog('\n<font color="red">Fail: event -a clear </font>')
        
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify event -a clear </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
        
    return FailFlag

def verifyEventHelp(c):
    FailFlag = False
    tolog("<b>Verify event -h </b>")
    
    result = SendCmd(c, 'event -h')
    
    if "Error (" in result or 'Option' not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: event -h </font>')
        
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify event -h </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
        
    return FailFlag

def verifEventSpecifyInexistentId(c):
    FailFlag = False
    tolog("<b> Verify event specify inexistent Id </b>")
    eventId = []
    eId = ''
    
    # -i <sequence ID>  (0,65535)
    result = SendCmd(c, 'event')
    row = result.split("\r\n")
    
    for x in range(4, len(row)):
        if len(row[x].split()) > 6:
            eventId.append(row[x].split()[0])
            
    if int(eventId[-1]) < 65535:
        eId = str(int(eventId[-1]) + 1)
        
    result = SendCmd(c, 'event -i ' + eId)
    
    if 'Error (' not in result or 'Not found' not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: event -i ' + eId + ' </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify event specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
        
    return FailFlag

def verifyEventInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify event invalid option</b>")
    
    command = [
        'event -x',
        'event -a list -x',
        'event -a clear -x'
    ]
    
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        
        result = SendCmd(c, com)
        
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
            
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify event invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
        
    return FailFlag

def verifyEventInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify event invalid parameters</b>")
    
    command = [
        'event test', 
        'event -a test',
        'event -i test', 
        'event -i 0 -c test'
    ]
    
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        
        result = SendCmd(c, com)
        
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
            
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify event invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
        
    return FailFlag

def verifyEventMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify event missing parameters</b>")
    
    command = [
        'event -a',
        'event -a list -i ', 
        'event -a list -i 0 -c'
    ]
    
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        
        result = SendCmd(c, com)
        
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
            
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify event missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
        
    return FailFlag

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyEvent(c)
    verifyEventList(c)
    verifyEventClear(c)
    verifyEventHelp(c)
    verifEventSpecifyInexistentId(c)
    verifyEventInvalidOption(c)
    verifyEventInvalidParameters(c)
    verifyEventMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped