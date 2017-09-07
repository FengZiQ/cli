# coding=utf-8

from send_cmd import *
from to_log import *
from ssh_connect import *

Pass = "'result': 'p'"
Fail = "'result': 'f'"

def precondition(c):
    tolog("<b>add initiator</b>")
    for i in range(1, 3):
        SendCmd(c, 'initiator -a add -t iscsi -n test.lunmapadd' + str(i) + '.com')
    for i in range(1, 3):
        SendCmd(c, 'initiator -a add -t fc -n aa-aa-aa-aa-aa-aa-aa-1' + str(i))
    initID = []
    initIfor = SendCmd(c, 'initiator')
    row = initIfor.split('Id: ')
    for i in range(1, len(row)):
        if 'test.lunmapadd' in row[i] or 'aa-aa-aa-aa-aa-aa-aa-1' in row[i]:
            initID.append(row[i].split()[0])

    tolog("<b>add volume</b>")
    pdinfo = SendCmd(c, 'phydrv')
    if 'Pool' not in pdinfo:
        pdID = []
        row = pdinfo.split('\r\n')
        for i in range(4, len(row) - 2):
            if len(row[i].split()) >= 10 and 'Unconfigured' in row[i] and 'OK' in row[i]:
                pdID.append(row[i].split()[0])
        SendCmd(c, 'pool -a add -p ' + pdID[0] + ' -s "name=Ptestlunmap,raid=0"')
        for i in range(1, 35):
            SendCmd(c, 'volume -a add -p 0 -s "name=Vtestlunmap' + str(i) + ',capacity=1GB"')
    else:
        poolinfo = SendCmd(c, 'pool')
        poolID = poolinfo.split('\r\n')[4].split()[0]
        for i in range(1, 35):
            SendCmd(c, 'volume -a add -p ' + poolID + ' -s "name=Vtestlunmap' + str(i) + ',capacity=1GB"')
    volumeID = []
    volumeInfo = SendCmd(c, 'volume')
    row = volumeInfo.split('\r\n')
    for i in range(4, (len(row)-2)):
        if 'Vtestlunmap' in row[i]:
            volumeID.append(row[i].split()[0])

    tolog('<b> add snapshot</b>')
    for i in range(1, 11):
        SendCmd(c, 'snapshot -a add -t volume -d ' + volumeID[-1] + ' -s "name=testlunmapss' + str(i) + '"')
    snapshotID = []
    snapshotInfo = SendCmd(c, 'snapshot')
    row = snapshotInfo.split('\r\n')
    for i in range(4, (len(row)-2)):
        if 'testlunmapss' in row[i]:
            snapshotID.append(row[i].split()[0])
    for i in snapshotID:
        if 'Un-Exported' in snapshotInfo:
            SendCmd(c, 'snapshot -a export -i ' + i)

    tolog('<b> add clone</b>')
    for i in range(1, 11):
        SendCmd(c, 'clone -a add -d ' + snapshotID[-1] + ' -s "name=testlunmapcl' + str(i) + '"')
    cloneID = []
    cloneInfo = SendCmd(c, 'clone')
    row = cloneInfo.split('\r\n')
    for i in range(4, (len(row)-2)):
        if 'testlunmapcl' in row[i]:
            cloneID.append(row[i].split()[0])
    for i in cloneID:
        if 'Un-Exported' in cloneInfo:
            SendCmd(c, 'clone -a export -i ' + i)

    tolog('<b> To enable lunmap</b>')
    SendCmd(c, 'lunmap -a enable')

    return initID, volumeID, snapshotID, cloneID

def verifyLunmapAdd(c):
    FailFlag = False
    initID, volumeID, snapshotID, cloneID = precondition(c)
    tolog(' Verify iscsi initiator lunmap')
    tolog('Verify: lunmap -a add -i ' + initID[0] + ' -p volume -l ' + volumeID[0] + ' -m 0')
    result = SendCmd(c, 'lunmap -a add -i ' + initID[0] + ' -p volume -l ' + volumeID[0] + ' -m 0')
    checkResult = SendCmd(c, 'lunmap')
    if 'Error (' in result or 'Name: test.lunmapadd' not in checkResult:
        FailFlag = True
        tolog('Fail: lunmap -a add -i ' + initID[0] + ' -p volume -l ' + volumeID[0] + ' -m 0')

    tolog(' Verify fc initiator lunmap')
    tolog('Verify: lunmap -a add -i ' + initID[2] + ' -p volume -l ' + volumeID[0] + ' -m 1')
    result = SendCmd(c, 'lunmap -a add -i ' + initID[2] + ' -p volume -l ' + volumeID[0] + ' -m 1')
    checkResult = SendCmd(c, 'lunmap')
    if 'Error (' in result or 'Name: aa-aa-aa-aa-aa-aa-aa-1' not in checkResult:
        FailFlag = True
        tolog('Fail: lunmap -a add -i ' + initID[2] + ' -p volume -l ' + volumeID[0] + ' -m 1')

    tolog(' Verify initiator map snapshot')
    tolog('Verify: lunmap -a add -i ' + initID[1] + ' -p snapshot -l ' + snapshotID[0] + ' -m 1022 ')
    result = SendCmd(c, ' lunmap -a add -i ' + initID[1] + ' -p snapshot -l ' + snapshotID[0] + ' -m 1022')
    checkResult = SendCmd(c, 'lunmap')
    if 'Error (' in result or 'snapshot' not in checkResult:
        FailFlag = True
        tolog('Fail: lunmap -a add -i ' + initID[1] + ' -p snapshot -l ' + snapshotID[0] + ' -m 1022')

    tolog(' Verify initiator map clone ')
    tolog('Verify: lunmap -a add -i ' + initID[3] + ' -p clone -l ' + cloneID[0] + ' -m 1023 ')
    result = SendCmd(c, ' lunmap -a add -i ' + initID[3] + ' -p clone -l ' + cloneID[0] + ' -m 1023')
    checkResult = SendCmd(c, 'lunmap')
    if 'Error (' in result or 'clone' not in checkResult:
        FailFlag = True
        tolog('Fail: lunmap -a add -i ' + initID[3] + ' -p snapshot -l ' + cloneID[0] + ' -m 1023')

    if FailFlag:
        tolog('\n<font color="red">Fail: lunmap add </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


    return FailFlag

def verifyLunmap(c):
    FailFlag = False
    tolog("Verify lunmap ")
    result = SendCmd(c, 'lunmap')
    if 'Error (' in result:
        FailFlag = True
        tolog('Fail: lunmap ')

    lunmapID = []
    row = result.split('initiator: ')
    for i in range(1,len(row)):
        lunmapID.append(row[i][0])

    for i in lunmapID:
        tolog(' lunmap -i ' + i )
        result = SendCmd(c, 'lunmap -i ' + i)
        if 'Error (' in result or 'initiator: ' + i not in result:
            FailFlag = True
            tolog('lunmap -i ' + i )

    if FailFlag:
        tolog('\n<font color="red">Fail: lunmap </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyLunmapList(c):
    FailFlag = False
    tolog("Verify lunmap -a list ")
    result = SendCmd(c, 'lunmap -a list')
    if 'Error (' in result:
        FailFlag = True
        tolog('Fail: lunmap -a list')

    lunmapID = []
    row = result.split('initiator: ')
    for i in range(1, len(row)):
        lunmapID.append(row[i][0])

    for i in lunmapID:
        tolog(' lunmap -a list -i ' + i )
        result = SendCmd(c, 'lunmap -a list -i ' + i)
        if 'Error (' in result or 'initiator: ' + i not in result:
            FailFlag = True
            tolog('lunmap -a list -i ' + i )

    if FailFlag:
        tolog('\n<font color="red">Fail: lunmap list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyLunmapAddlun(c):
    FailFlag = False
    tolog(' lunmap -a addlun ')
    initID = []
    initIfor = SendCmd(c, 'initiator')
    row = initIfor.split('Id: ')
    for i in range(1, len(row)):
        if 'test.lunmapadd' in row[i] or 'aa-aa-aa-aa-aa-aa-aa-1' in row[i]:
            initID.append(row[i].split()[0])

    volumeID = []
    volumeInfo = SendCmd(c, 'volume')
    row = volumeInfo.split('\r\n')
    for i in range(4, (len(row)-2)):
        if 'Vtestlunmap' in row[i]:
            volumeID.append(row[i].split()[0])

    snapshotID = []
    snapshotInfo = SendCmd(c, 'snapshot')
    row = snapshotInfo.split('\r\n')
    for i in range(4, (len(row) - 2)):
        if 'testlunmapss' in row[i]:
            snapshotID.append(row[i].split()[0])

    cloneID = []
    cloneInfo = SendCmd(c, 'clone')
    row = cloneInfo.split('\r\n')
    for i in range(4, (len(row)-2)):
        if 'testlunmapcl' in row[i]:
            cloneID.append(row[i].split()[0])

    tolog(' Verify addlun volume ')
    m = 512
    for vID in volumeID[1:]:
        tolog('Verify: lunmap -a addlun -p volume -i ' + initID[1] + ' -l ' + vID + ' -m ' + str(m) )
        result = SendCmd(c, 'lunmap -a addlun -p volume -i ' + initID[1] + ' -l ' + vID + ' -m ' + str(m))
        checkResult = SendCmd(c, 'lunmap -i ' + initID[1])
        if 'Error (' in result or str(m) not in checkResult or 'volume' not in checkResult:
            FailFlag = True
            tolog('Fail: lunmap -a addlun -p volume -i ' + initID[1] + ' -l ' + vID + ' -m ' + str(m) )
        m = m + 1

    tolog(' Verify addlun snapshot')
    m = 10
    for ssID in snapshotID:
        tolog('Verify: lunmap -a addlun -p snapshot -i ' + initID[0] + ' -l ' + ssID + ' -m ' + str(m) )
        result = SendCmd(c, 'lunmap -a addlun -p snapshot -i ' + initID[0] + ' -l ' + ssID + ' -m ' + str(m))
        checkResult = SendCmd(c, 'lunmap -i ' + initID[0])
        if 'Error (' in result or str(m) not in checkResult or 'snapshot' not in checkResult:
            FailFlag = True
            tolog('Fail: lunmap -a addlun -p snapshot -i ' + initID[0] + ' -l ' + ssID + ' -m ' + str(m) )
        m = m + 1

    tolog(' Verify addlun clone')
    m = 1000
    for cID in cloneID:
        tolog('Verify: lunmap -a addlun -p clone -i ' + initID[0] + ' -l ' + cID + ' -m ' + str(m) )
        result = SendCmd(c, 'lunmap -a addlun -p clone -i ' + initID[0] + ' -l ' + cID + ' -m ' + str(m))
        checkResult = SendCmd(c, 'lunmap -i ' + initID[0])
        if 'Error (' in result or str(m) not in checkResult or 'clone' not in checkResult:
            FailFlag = True
            tolog('Fail: lunmap -a addlun -p clone -i ' + initID[0] + ' -l ' + cID + ' -m ' + str(m) )
        m = m + 1

    if FailFlag:
        tolog('\n<font color="red">Fail: lunmap addlun </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyLunmapDellun(c):
    FailFlag = False
    tolog("Verify lunmap -a dellun volume ")
    initID = []
    initIfor = SendCmd(c, 'initiator')
    row = initIfor.split('Id: ')
    for i in range(1, len(row)):
        if 'test.lunmapadd' in row[i] or 'aa-aa-aa-aa-aa-aa-aa-1' in row[i]:
            initID.append(row[i].split()[0])

    volumeInfo = SendCmd(c, 'volume')
    volumeID = [volumeInfo.split('\r\n')[-3].split()[0]]

    for vID in volumeID:
        result = SendCmd(c, 'lunmap -a dellun -p volume -i ' + initID[1] + ' -l ' + vID)
        checkResult = SendCmd(c, 'lunmap ' + initID[1])
        if 'Error (' in result or ('   ' + vID + '   ') in checkResult:
            FailFlag = True
            tolog('Fail: lunmap -a dellun -p volume -i ' + initID[1] + ' -l ' + vID )

    tolog(' lunmap -a dellun -p snapshot ')
    snapshotID = []
    snapshotInfo = SendCmd(c, 'snapshot')
    row = snapshotInfo.split('\r\n')

    for i in range(4, (len(row) - 2)):
        if 'testlunmapss' in row[i]:
            snapshotID.append(row[i].split()[0])
    for ssID in snapshotID:
        result = SendCmd(c, 'lunmap -a dellun -p snapshot -i ' + initID[0] + ' -l ' + ssID)
        checkResult = SendCmd(c, 'lunmap -i' + initID[0])
        if 'Error (' in result or ('    ' + ssID + '    ')  in checkResult:
            FailFlag = True
            tolog('Fail: lunmap -a dellun -p snapshot -i ' + initID[0] + ' -l ' + ssID )

    tolog(' lunmap -a dellun -p clone ')
    cloneID = []
    cloneInfo = SendCmd(c, 'clone')
    row = cloneInfo.split('\r\n')
    for i in range(4, (len(row)-2)):
        if 'testlunmapcl' in row[i]:
            cloneID.append(row[i].split()[0])
    for cID in cloneID:
        result = SendCmd(c, 'lunmap -a dellun -p clone -i ' + initID[0] + ' -l ' + cID)
        checkResult = SendCmd(c, 'lunmap -i ' + initID[0])
        if 'Error (' in result or (cID + '                        clone') in checkResult:
            FailFlag = True
            tolog('Fail: lunmap -a dellun -p clone -i ' + initID[0] + ' -l ' + cID )

    if FailFlag:
        tolog('\n<font color="red">Fail: lunmap dellun </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


    return FailFlag

def verifyLunmapEnable(c):
    FailFlag = False
    tolog("Verify lunmap -a enable when it enable")
    p1 = SendCmd(c, 'lunmap -a enable')
    if 'Error (' not in p1:
        result = SendCmd(c, 'lunmap -a enable')
        checkResult = SendCmd(c, 'lunmap')
        if 'Error (' in result or 'LUN mapping and masking : Enabled' not in checkResult:
            FailFlag = True
            tolog('Fail: lunmap -a enable ')
    else:
        tolog(' Precondition failure ')

    tolog("Verify lunmap -a enable when it disable")
    p2 = SendCmd(c, 'lunmap -a disable')
    if 'Error (' not in p2:
        result = SendCmd(c, 'lunmap -a enable')
        checkResult = SendCmd(c, 'lunmap')
        if 'Error (' in result or 'LUN mapping and masking : Enabled' not in checkResult:
            FailFlag = True
            tolog('Fail: lunmap -a enable ')
    else:
        tolog(' Precondition failure ')

    if FailFlag:
        tolog('\n<font color="red">Fail: lunmap enable </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyLunmapDel(c):
    FailFlag = False
    result = SendCmd(c, 'lunmap')
    lunmapID = []
    row = result.split('initiator: ')
    for i in range(1, len(row)):
        lunmapID.append(row[i][0])

    for i in lunmapID:
        result = SendCmd(c, 'lunmap -a del -i ' + i)
        if 'Error (' in result:
            FailFlag = True
            tolog('lunmap -a del -i ' + i )

    checkResult = SendCmd(c, 'lunmap')
    if 'No LUN mapping entry available' not in checkResult:
        FailFlag = True
        tolog('Fail: lunmap -a del ')

    if FailFlag:
        tolog('\n<font color="red">Fail: lunmap del </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyLunmapDisable(c):
    FailFlag = False
    tolog("Verify lunmap -a disable when it enable")
    p1 = SendCmd(c, 'lunmap -a enable')
    if 'Error (' not in p1:
        result = SendCmd(c, 'lunmap -a disable')
        checkResult = SendCmd(c, 'lunmap')
        if 'Error (' in result or 'LUN mapping and masking : Disabled' not in checkResult:
            FailFlag = True
            tolog('Fail: lunmap -a enable ')
    else:
        tolog(' Precondition failure ')

    tolog("Verify lunmap -a disable when it disable")
    p2 = SendCmd(c, 'lunmap -a disable')
    if 'Error (' not in p2:
        result = SendCmd(c, 'lunmap -a disable')
        checkResult = SendCmd(c, 'lunmap')
        if 'Error (' in result or 'LUN mapping and masking : Disabled' not in checkResult:
            FailFlag = True
            tolog('Fail: lunmap -a enable ')
    else:
        tolog(' Precondition failure ')

    if FailFlag:
        tolog('\n<font color="red">Fail: lunmap disable </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyLunmapSpecifyInexistentId(c):
    FailFlag = False
    tolog(" Verify lunmap specify inexistent Id ")
    # -i <InitiatorId> (0,2047)
    # -l <Volume ID list> (0,1023)

    result = SendCmd(c, 'lunmap -a add -i 200 -p volume -l 0 -m 0')
    if 'Error (' not in result or 'Invalid initiator index' not in result:
        FailFlag = True
        tolog(' lunmap -a add -i 200 -p volume -l 0 -m 0')

    result = SendCmd(c, 'lunmap -a add -i 0 -p volume -l 1000 -m 0')
    if 'Error (' not in result or 'Volume id=[1000] is not existed' not in result:
        FailFlag = True
        tolog(' lunmap -a add -i 0 -p volume -l 1000 -m 0')

    if FailFlag:
        tolog('\n<font color="red">Fail: lunmap Specify Inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyLunmapInvalidOption(c):
    FailFlag = False
    tolog("Verify lunmap invalid option")
    command = ['lunmap -x', 'lunmap -a list -x', 'lunmap -a add -x', 'lunmap -a del -x',
               'lunmap -a addlun -x', 'lunmap -a dellun -x', 'lunmap -a enable -x', 'lunmap -a disable -x']
    for com in command:
        tolog(' Verify ' + com )
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('Fail: ' + com )

    if FailFlag:
        tolog('\n<font color="red">Fail: lunmap invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyLunmapInvalidParameters(c):
    FailFlag = False
    tolog("Verify lunmap invalid parameters")
    command = ['lunmap test', 'lunmap -a list test', 'lunmap -a add test', 'lunmap -a del test',
                'lunmap -a addlun test', 'lunmap -a dellun test', 'lunmap -a enable test', 'lunmap -a disable test']
    for com in command:
        tolog(' Verify ' + com )
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('Fail: ' + com )

    if FailFlag:
        tolog('\n<font color="red">Fail: lunmap invalid setting parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

    return FailFlag

def verifyLunmapMissingParameters(c):
    FailFlag = False
    tolog("Verify lunmap missing parameters")
    command = ['lunmap -i', 'lunmap -a list -i', 'lunmap -a add -i', 'lunmap -a del -i', 'lunmap -a addlun -i', 'lunmap -a dellun -i']
    for com in command:
        tolog(' Verify ' + com )
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('Fail: ' + com )

    if FailFlag:
        tolog('\n<font color="red">Fail: lunmap missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)


    return FailFlag

def cleanUp(c):
    poolInfo = SendCmd(c, 'pool')
    row = poolInfo.split('\r\n')
    for i in range(4, len(row)):
        if 'Ptestlunmap' in row[i]:
            SendCmdconfirm(c, 'pool -a del -f -i ' + row[i].split()[0])
    else:
        volumeID = []
        volumeInfo = SendCmd(c, 'volume')
        row = volumeInfo.split('\r\n')
        for i in range(4, (len(row)-2)):
            if 'Vtestlunmap' in row[i]:
                volumeID.append(row[i].split()[0])
        for vID in volumeID:
            SendCmdconfirm(c, 'volume -a del -i ' + vID + ' -f')

    initInfo = SendCmd(c, 'initiator')
    row = initInfo.split('Id: ')
    for i in range(1, len(row)):
        if 'test.lunmapadd' in row[i] or 'aa-aa-aa-aa-aa-aa-aa-1' in row[i]:
            SendCmd(c, 'initiator -a del -i ' + row[i].split()[0])

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyLunmapAdd(c)
    verifyLunmap(c)
    verifyLunmapList(c)
    verifyLunmapAddlun(c)
    verifyLunmapDellun(c)
    verifyLunmapEnable(c)
    verifyLunmapDel(c)
    verifyLunmapDisable(c)
    verifyLunmapSpecifyInexistentId(c)
    verifyLunmapInvalidOption(c)
    verifyLunmapInvalidParameters(c)
    verifyLunmapMissingParameters(c)
    cleanUp(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped