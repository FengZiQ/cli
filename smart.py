# coding=utf-8

from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn

Pass = "'result': 'p'"
Fail = "'result': 'f'"

def findPdId(c):
    PdID = []
    
    result = SendCmd(c, 'phydrv')
    row = result.split('\r\n')
    
    if 'Error (' not in result:
        for r in range(4, (len(row) -2)):
            if len(row[r].split()) >= 9:
                PdID.append(row[r].split()[0])
                
    return PdID

def verifySmart(c):
    FailFlag = False
    tolog("Verify smart")
    
    PdId = findPdId(c)
    
    result = SendCmd(c, "smart")
    
    smartPdId = []
    row = result.split('\r\n')
    if "Error (" in result:
        tolog('Fail:smart Please check PD OpStatus')
        exit()

    for i in range(4, len(row) - 2):
        if len(row[i].split()) >= 5:
            smartPdId.append(row[i].split()[0])

    if smartPdId != PdId:
        FailFlag = True
        tolog('Fail: Verify smart')

    tolog("Verify smart -p ")
    PdId = findPdId(c)
    
    for m in PdId:
        result = SendCmd(c, "smart -p " + m)
        
        row = result.split("\r\n")
        
        if row[2] not in result or row[4].split()[0] != m:
            FailFlag = True
            tolog('Fail: Verify smart -p' + m)
            
    if FailFlag:
        tolog('\n<font color="red">Fail: smart </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifySmartV(c):
    FailFlag = False
    tolog("Verify smart -v")
    
    result = SendCmd(c, "smart -v")
    
    if "Error (" in result:
        FailFlag = True
        tolog('Fail: Verify smart -v')
        
    tolog(" Verify smart -v -p ")
    
    result = SendCmd(c, "smart")
    
    if "Error (" in result:
        tolog('Fail:smart Please check PD OpStatus')
        exit()
        
    enablePdId = []
    disablePdId = []
    
    row = result.split('\r\n')
    # get the smart enable and disable Id list
    for i in range(4, len(row) - 2):
        if len(row[i].split()) >= 5:
            if row[i].split()[-1] == "Disabled":
                disablePdId.append(row[i].split()[0])
            if row[i].split()[-1] == "Enabled":
                enablePdId.append(row[i].split()[0])

    # When PD smart is enable, verify smart -v -p
    if len(enablePdId) != 0:
        for m in enablePdId:
            tolog(' smart -v -p ' + m )
            result = SendCmd(c, "smart -v -p " + m)
            
            PDModel = SendCmd(c, "phydrv -v -p " + m)
            smartPDModel = result.split("\r\n")[4].split()[-1]
            
            if result.split("\r\n")[3] != "PdId: " + m:
                FailFlag = True
                tolog('Fail: Verify smart -v -p ' + m )

    # When PD smart is disable, verify smart -v -p
    if len(disablePdId) != 0:
        for m in disablePdId:
            result = SendCmd(c, "smart -p " + m + " -v")
            
            PDModel = SendCmd(c, "phydrv -v -p " + m)
            smartPDModel = result.split("\r\n")[3].split()[-1]
            
            if result.split("\r\n")[3] != "PdId: " + m:
                FailFlag = True
                tolog('Fail: Verify smart -v -p ' + m )

    if FailFlag:
        tolog('\n<font color="red">Fail: smart -v</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifySmartList(c):
    FailFlag = False
    tolog("Verify smart -a list")
    
    PdId = findPdId(c)
    
    result = SendCmd(c, "smart -a list")
    row = result.split('\r\n')
    smartPdId = []

    for i in range(4, len(row) - 2):
        if len(row[i].split()) >= 5:
            smartPdId.append(row[i].split()[0])

    if smartPdId != PdId:
        FailFlag = True
        tolog('Fail: Verify smart -a list')

    tolog("Verify smart -a list -p ")
    
    PdId = findPdId(c)
    
    for m in PdId:
        result = SendCmd(c, "smart -a list -p " + m)
        
        row = result.split("\r\n")
        
        if row[2] not in result or row[4].split()[0] != m:
            FailFlag = True
            tolog('Fail: Verify smart -a list -p' + m )

    tolog('Verify smart -a list -v ')
    
    result = SendCmd(c, 'smart -a list -v')
    
    if "Error (" in result:
        FailFlag = True
        tolog('Fail: Verify smart -a list -v')

    if FailFlag:
        tolog('\n<font color="red">Fail: smart -a list -v</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifySmartEnable(c):
    FailFlag = False
    tolog("<b> Verify smart -a enable -p pd ID </b>")
    
    PdId = findPdId(c)
    
    for p in PdId:
        for values in ['disable ', 'enable ', 'enable ']:
            
            result = SendCmd(c, "smart -a " + values + "-p " + p)
            
            if "Error (" in result:
                FailFlag = True
                tolog('\n<font color="red">Fail: smart -a ' + values + '-p ' + p + '</font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: smart -a enable </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifySmartDisable(c):
    FailFlag = False
    tolog("<b> Verify smart -a disable -p pd ID </b>")
    
    PdId = findPdId(c)
    
    for p in PdId:
        for values in ['enable ', 'disable ', 'disable ']:
            
            result = SendCmd(c, "smart -a " + values + "-p " + p)
            
            if "Error (" in result:
                FailFlag = True
                tolog('\n<font color="red">Fail: smart -a ' + values + '-p ' + p + '</font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: smart -a disable </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifySmartHelp(c):
    FailFlag = False
    tolog(" Verify smart -h ")
    
    result = SendCmd(c, "smart -h")
    
    if 'Error (' in result or "smart" not in result:
        FailFlag = True
        tolog('Fail: Verify smart -h ')
        tolog('\nCheckpoint: Usage, Summary, smart ')

    if FailFlag:
        tolog('\n<font color="red">Fail: smart -h </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifySmartSpecifyInexistentId(c):
    FailFlag = False
    tolog(" Verify smart specify inexistent Id ")
    
    command1 = [
        'smart -p 512',
        'smart -a list -p 512',
        'smart -a enable -p 512',
        'smart -a disable -p 512'
    ]
    
    command2 = [
        'smart -p 513',
        'smart -a list -p 513',
        'smart -a enable -p 513',
        'smart -a disable -p 513'
    ]
    
    for com in command1:
        tolog(' Verify ' + com)
        
        result = SendCmd(c, com)
        
        if "Error (" not in result or "not found" not in result:
            FailFlag = True
            tolog('Fail: ' + com)
            
    for com in command2:
        tolog(' Verify ' + com)
        
        result = SendCmd(c, com)
        
        if "Error (" not in result or "invalid setting 513 (1,512)" not in result:
            FailFlag = True
            tolog('Fail: ' + com)
    
    if FailFlag:
        tolog('\n<font color="red">Fail: smart specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
    
    return FailFlag

def verifySmartInvalidOption(c):
    FailFlag = False
    tolog("Verify smart invalid option")
    
    command = [
        'smart -x', 
        'smart -a list -x',
        'smart -a enable -x',
        'smart -a disable -x'
    ]
    
    for com in command:
        tolog(' Verify ' + com)
        
        result = SendCmd(c, com)
        
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('Fail: ' + com)

    if FailFlag:
        tolog('\n<font color="red">Fail: smart Invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifySmartInvalidParameters(c):
    FailFlag = False
    tolog("Verify smart invalid parameters")
    
    command = [
        'smart test',
        'smart -a test',
        'smart -a enable -p test',
        'smart -a disable -p test'
    ]
    
    for com in command:
        tolog(' Verify ' + com)
        
        result = SendCmd(c, com)
        
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('Fail: ' + com)

    if FailFlag:
        tolog('\n<font color="red">Fail: smart Invalid setting parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifySmartMissingParameters(c):
    FailFlag = False
    tolog("Verify smart missing parameters")
    
    command = [
        'smart -v -p ', 
        'smart -a list -p ',
        'smart -p ',
        'smart -a enable -p ', 
        'smart -a disable -p '
    ]
    
    for com in command:
        tolog(' Verify ' + com)
        
        result = SendCmd(c, com)
        
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('Fail: ' + com)

    if FailFlag:
        tolog('\n<font color="red">Fail: smart missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifySmart(c)
    verifySmartV(c)
    verifySmartList(c)
    verifySmartEnable(c)
    verifySmartDisable(c)
    verifySmartHelp(c)
    verifySmartSpecifyInexistentId(c)
    verifySmartInvalidOption(c)
    verifySmartInvalidParameters(c)
    verifySmartMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped