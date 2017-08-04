# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
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
    poolinfo = SendCmd(c, 'pool')
    if 'No pool in the subsystem' in poolinfo:
        pdinfo = SendCmd(c, 'phydrv')
        pdID = [pdinfo.split('\r\n')[4][0]]
        SendCmd(c, 'pool -a add -p ' + pdID[0] + ' -s "name=Ptestlunmap,raid=0"')
        for i in range(1, 35):
            SendCmd(c, 'volume -a add -p 0 -s "name=Vtestlunmap' + str(i) + ',capacity=1GB"')
    else:
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
    tolog('<b> Verify iscsi initiator lunmap</b>')
    tolog('<b>lunmap -a add -i ' + initID[0] + ' -p volume -l ' + volumeID[0] + ' -m 0</b>')
    result = SendCmd(c, 'lunmap -a add -i ' + initID[0] + ' -p volume -l ' + volumeID[0] + ' -m 0')
    checkResult = SendCmd(c, 'lunmap')
    if 'Error (' in result or 'Name: test.lunmapadd' not in checkResult:
        FailFlag = True
        tolog('<font color="red">Fail: lunmap -a add -i ' + initID[0] + ' -p volume -l ' + volumeID[0] + ' -m 0</font>')

    tolog('<b> Verify fc initiator lunmap</b>')
    tolog('<b>lunmap -a add -i ' + initID[2] + ' -p volume -l ' + volumeID[0] + ' -m 1</b>')
    result = SendCmd(c, 'lunmap -a add -i ' + initID[2] + ' -p volume -l ' + volumeID[0] + ' -m 1')
    checkResult = SendCmd(c, 'lunmap')
    if 'Error (' in result or 'Name: aa-aa-aa-aa-aa-aa-aa-1' not in checkResult:
        FailFlag = True
        tolog('<font color="red">Fail: lunmap -a add -i ' + initID[2] + ' -p volume -l ' + volumeID[0] + ' -m 1</font>')

    tolog('<b> Verify initiator map snapshot </b>')
    tolog('<b> lunmap -a add -i ' + initID[1] + ' -p snapshot -l ' + snapshotID[0] + ' -m 1022 </b>')
    result = SendCmd(c, ' lunmap -a add -i ' + initID[1] + ' -p snapshot -l ' + snapshotID[0] + ' -m 1022')
    checkResult = SendCmd(c, 'lunmap')
    if 'Error (' in result or 'snapshot' not in checkResult:
        FailFlag = True
        tolog('<font color="red">Fail: lunmap -a add -i ' + initID[1] + ' -p snapshot -l ' + snapshotID[0] + ' -m 1022</font>')

    tolog('<b> Verify initiator map clone </b>')
    tolog('<b> lunmap -a add -i ' + initID[3] + ' -p clone -l ' + cloneID[0] + ' -m 1023 </b>')
    result = SendCmd(c, ' lunmap -a add -i ' + initID[3] + ' -p clone -l ' + cloneID[0] + ' -m 1023')
    checkResult = SendCmd(c, 'lunmap')
    if 'Error (' in result or 'clone' not in checkResult:
        FailFlag = True
        tolog('<font color="red">Fail: lunmap -a add -i ' + initID[3] + ' -p snapshot -l ' + cloneID[0] + ' -m 1023</font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify lunmap -a add </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyLunmap(c):
    FailFlag = False
    tolog("<b>Verify lunmap </b>")
    result = SendCmd(c, 'lunmap')
    if 'Error (' in result:
        FailFlag = True
        tolog('<font color="red">Fail: lunmap </font>')

    lunmapID = []
    row = result.split('initiator: ')
    for i in range(1,len(row)):
        lunmapID.append(row[i][0])

    for i in lunmapID:
        tolog('<b> lunmap -i ' + i + '</b>')
        result = SendCmd(c, 'lunmap -i ' + i)
        if 'Error (' in result or 'initiator: ' + i not in result:
            FailFlag = True
            tolog('<font color="red">lunmap -i ' + i + '</font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify lunmap </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyLunmapList(c):
    FailFlag = False
    tolog("<b>Verify lunmap -a list </b>")
    result = SendCmd(c, 'lunmap -a list')
    if 'Error (' in result:
        FailFlag = True
        tolog('<font color="red">Fail: lunmap -a list</font>')

    lunmapID = []
    row = result.split('initiator: ')
    for i in range(1, len(row)):
        lunmapID.append(row[i][0])

    for i in lunmapID:
        tolog('<b> lunmap -a list -i ' + i + '</b>')
        result = SendCmd(c, 'lunmap -a list -i ' + i)
        if 'Error (' in result or 'initiator: ' + i not in result:
            FailFlag = True
            tolog('<font color="red">lunmap -a list -i ' + i + '</font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify lunmap -a list</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyLunmapAddlun(c):
    FailFlag = False
    tolog('<b> lunmap -a addlun </b>')
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

    tolog('<b> Verify addlun volume </b>')
    m = 512
    for vID in volumeID[1:]:
        tolog('<b>Verify: lunmap -a addlun -p volume -i ' + initID[1] + ' -l ' + vID + ' -m ' + str(m) + '</b>')
        result = SendCmd(c, 'lunmap -a addlun -p volume -i ' + initID[1] + ' -l ' + vID + ' -m ' + str(m))
        checkResult = SendCmd(c, 'lunmap')
        if 'Error (' in result or str(m) not in checkResult or 'volume' not in checkResult:
            FailFlag = True
            tolog('<font color="red">Fail: lunmap -a addlun -p volume -i ' + initID[1] + ' -l ' + vID + ' -m ' + str(m) + ' </font>')
        m = m + 1

    tolog('<b> Verify addlun snapshot</b>')
    m = 10
    for ssID in snapshotID:
        tolog('<b>Verify: lunmap -a addlun -p snapshot -i ' + initID[0] + ' -l ' + ssID + ' -m ' + str(m) + '</b>')
        result = SendCmd(c, 'lunmap -a addlun -p snapshot -i ' + initID[0] + ' -l ' + ssID + ' -m ' + str(m))
        checkResult = SendCmd(c, 'lunmap')
        if 'Error (' in result or str(m) not in checkResult or 'snapshot' not in checkResult:
            FailFlag = True
            tolog('<font color="red">Fail: lunmap -a addlun -p snapshot -i ' + initID[0] + ' -l ' + ssID + ' -m ' + str(m) + ' </font>')
        m = m + 1

    tolog('<b> Verify addlun clone</b>')
    m = 1000
    for cID in cloneID:
        tolog('<b>Verify: lunmap -a addlun -p clone -i ' + initID[0] + ' -l ' + cID + ' -m ' + str(m) + '</b>')
        result = SendCmd(c, 'lunmap -a addlun -p clone -i ' + initID[0] + ' -l ' + cID + ' -m ' + str(m))
        checkResult = SendCmd(c, 'lunmap')
        if 'Error (' in result or str(m) not in checkResult or 'clone':
            FailFlag = True
            tolog('<font color="red">Fail: lunmap -a addlun -p clone -i ' + initID[0] + ' -l ' + cID + ' -m ' + str(m) + ' </font>')
        m = m + 1

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify lunmap -a addlun </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyLunmapDellun(c):
    FailFlag = False
    tolog("<b>Verify lunmap -a dellun volume </b>")
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
        if 'Error (' in result or '   ' + vID + '   ' in checkResult:
            FailFlag = True
            tolog('<font color="red">Fail: lunmap -a dellun -p volume -i ' + initID[1] + ' -l ' + vID + '</font>')

    tolog('<b> lunmap -a dellun -p snapshot </b>')
    snapshotID = []
    snapshotInfo = SendCmd(c, 'snapshot')
    row = snapshotInfo.split('\r\n')

    for i in range(4, (len(row) - 2)):
        if 'testlunmapss' in row[i]:
            snapshotID.append(row[i].split()[0])
    for ssID in snapshotID:
        result = SendCmd(c, 'lunmap -a dellun -p snapshot -i ' + initID[0] + ' -l ' + ssID)
        checkResult = SendCmd(c, 'lunmap ' + initID[0])
        if 'Error (' in result or '   ' + ssID + '   ' in checkResult:
            FailFlag = True
            tolog('<font color="red">Fail: lunmap -a dellun -p snapshot -i ' + initID[0] + ' -l ' + ssID + '</font>')

    tolog('<b> lunmap -a dellun -p clone </b>')
    cloneID = []
    cloneInfo = SendCmd(c, 'clone')
    row = cloneInfo.split('\r\n')
    for i in range(4, (len(row)-2)):
        if 'testlunmapcl' in row[i]:
            cloneID.append(row[i].split()[0])
    for cID in cloneID:
        result = SendCmd(c, 'lunmap -a dellun -p clone -i ' + initID[0] + ' -l ' + cID)
        checkResult = SendCmd(c, 'lunmap ' + initID[0])
        if 'Error (' in result or '   ' + cID + "   " in checkResult:
            FailFlag = True
            tolog('<font color="red">Fail: lunmap -a dellun -p clone -i ' + initID[0] + ' -l ' + cID + '</font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify lunmap -a dellun </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyLunmapEnable(c):
    FailFlag = False
    tolog("<b>Verify lunmap -a enable when it enable</b>")
    p1 = SendCmd(c, 'lunmap -a enable')
    if 'Error (' not in p1:
        result = SendCmd(c, 'lunmap -a enable')
        checkResult = SendCmd(c, 'lunmap')
        if 'Error (' in result or 'LUN mapping and masking : Enabled' not in checkResult:
            FailFlag = True
            tolog('<font color="red">Fail: lunmap -a enable </font>')
    else:
        tolog('<font color="red"> Precondition failure </font>')

    tolog("<b>Verify lunmap -a enable when it disable</b>")
    p2 = SendCmd(c, 'lunmap -a disable')
    if 'Error (' not in p2:
        result = SendCmd(c, 'lunmap -a enable')
        checkResult = SendCmd(c, 'lunmap')
        if 'Error (' in result or 'LUN mapping and masking : Enabled' not in checkResult:
            FailFlag = True
            tolog('<font color="red">Fail: lunmap -a enable </font>')
    else:
        tolog('<font color="red"> Precondition failure </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify lunmap -a enable </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

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
            tolog('<font color="red">lunmap -a del -i ' + i + '</font>')

    checkResult = SendCmd(c, 'lunmap')
    if 'No LUN mapping entry available' not in checkResult:
        FailFlag = True
        tolog('\n<font color="red">Fail: lunmap -a del </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify lunmap -a del </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyLunmapDisable(c):
    FailFlag = False
    tolog("<b>Verify lunmap -a disable when it enable</b>")
    p1 = SendCmd(c, 'lunmap -a enable')
    if 'Error (' not in p1:
        result = SendCmd(c, 'lunmap -a disable')
        checkResult = SendCmd(c, 'lunmap')
        if 'Error (' in result or 'LUN mapping and masking : Disabled' not in checkResult:
            FailFlag = True
            tolog('<font color="red">Fail: lunmap -a enable </font>')
    else:
        tolog('<font color="red"> Precondition failure </font>')

    tolog("<b>Verify lunmap -a disable when it disable</b>")
    p2 = SendCmd(c, 'lunmap -a disable')
    if 'Error (' not in p2:
        result = SendCmd(c, 'lunmap -a disable')
        checkResult = SendCmd(c, 'lunmap')
        if 'Error (' in result or 'LUN mapping and masking : Disabled' not in checkResult:
            FailFlag = True
            tolog('<font color="red">Fail: lunmap -a enable </font>')
    else:
        tolog('<font color="red"> Precondition failure </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify lunmap -a disable </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyLunmapSpecifyInexistentId(c):
    FailFlag = False
    tolog("<b> Verify lunmap specify inexistent Id </b>")
    # -i <InitiatorId> (0,2047)
    # -l <Volume ID list> (0,1023)
    initiatorInfo = SendCmd(c, 'initiator')
    initID = initiatorInfo.split('Id: ')[-1].split()[0]

    volumeInfo = SendCmd(c, 'volume')
    volumeID = volumeInfo.split('\r\n')[-3].split()[0]
    if int(initID) != 2047:
        result = SendCmd(c, 'lunmap -a add -i ' + str(int(initID)+1) + ' -p volume -l ' + volumeID + ' -m 0')
        if 'Error (' not in result or 'Invalid initiator index' not in result:
            FailFlag = True
            tolog('<font color="red"> lunmap -a add -i ' + str(int(initID)+1) + ' -p volume -l ' + volumeID + ' -m 0</font>')
    else:
        tolog('<font color="red"> Precondition failure </font>')

    if int(volumeID) != 1023:
        result = SendCmd(c, 'lunmap -a add -i ' + initID + ' -p volume -l ' + str(int(volumeID) + 1) + ' -m 0')
        if 'Error (' not in result or 'Incorrect Parameters: Volume id' not in result:
            FailFlag = True
            tolog('<font color="red"> lunmap -a add -i ' + initID + ' -p volume -l ' + str(int(volumeID) + 1) + ' -m 0</font>')
    else:
        tolog('<font color="red"> Precondition failure </font>')

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify lunmap specify inexistent Id </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyLunmapInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify lunmap invalid option</b>")
    command = ['lunmap -x', 'lunmap -a list -x', 'lunmap -a add -x', 'lunmap -a del -x',
               'lunmap -a addlun -x', 'lunmap -a dellun -x', 'lunmap -a enable -x', 'lunmap -a disable -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify lunmap invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyLunmapInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify lunmap invalid parameters</b>")
    command = ['lunmap test', 'lunmap -a list test', 'lunmap -a add test', 'lunmap -a del test',
                'lunmap -a addlun test', 'lunmap -a dellun test', 'lunmap -a enable test', 'lunmap -a disable test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify lunmap invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyLunmapMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify lunmap missing parameters</b>")
    command = ['lunmap -i', 'lunmap -a list -i', 'lunmap -a add -i', 'lunmap -a del -i', 'lunmap -a addlun -i', 'lunmap -a dellun -i']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify lunmap missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def cleanUp(c):
    poolInfo = SendCmd(c, 'pool')
    row = poolInfo.split('\r\n')
    for i in range(4, len(row)):
        if 'Ptestlunmap' in row[i]:
            SendCmd(c, 'pool -a del -i ' + row[i].split()[0])
    else:
        volumeID = []
        volumeInfo = SendCmd(c, 'volume')
        row = volumeInfo.split('\r\n')
        for i in range(4, (len(row)-2)):
            if 'Vtestlunmap' in row[i]:
                volumeID.append(row[i].split()[0])
        for vID in volumeID:
            SendCmd(c, 'volume -a del -i ' + vID + ' -f')

    initInfo = SendCmd(c, 'initiator')
    row = initInfo.split('Id: ')
    for i in range(1, len(row)):
        if 'test.lunmapadd' in row[i] or 'aa-aa-aa-aa-aa-aa-aa-1' in row[i]:
            SendCmd(c, 'initiator -a del -i ' + row[i].split()[0])



def bvt_verifyLunmapAdd(c):
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

    return FailFlag

def bvt_verifyLunmap(c):
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

    return FailFlag

def bvt_verifyLunmapList(c):
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

    return FailFlag

def bvt_verifyLunmapAddlun(c):
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
        checkResult = SendCmd(c, 'lunmap')
        if 'Error (' in result or str(m) not in checkResult or 'volume' not in checkResult:
            FailFlag = True
            tolog('Fail: lunmap -a addlun -p volume -i ' + initID[1] + ' -l ' + vID + ' -m ' + str(m) )
        m = m + 1

    tolog(' Verify addlun snapshot')
    m = 10
    for ssID in snapshotID:
        tolog('Verify: lunmap -a addlun -p snapshot -i ' + initID[0] + ' -l ' + ssID + ' -m ' + str(m) )
        result = SendCmd(c, 'lunmap -a addlun -p snapshot -i ' + initID[0] + ' -l ' + ssID + ' -m ' + str(m))
        checkResult = SendCmd(c, 'lunmap')
        if 'Error (' in result or str(m) not in checkResult or 'snapshot' not in checkResult:
            FailFlag = True
            tolog('Fail: lunmap -a addlun -p snapshot -i ' + initID[0] + ' -l ' + ssID + ' -m ' + str(m) )
        m = m + 1

    tolog(' Verify addlun clone')
    m = 1000
    for cID in cloneID:
        tolog('Verify: lunmap -a addlun -p clone -i ' + initID[0] + ' -l ' + cID + ' -m ' + str(m) )
        result = SendCmd(c, 'lunmap -a addlun -p clone -i ' + initID[0] + ' -l ' + cID + ' -m ' + str(m))
        checkResult = SendCmd(c, 'lunmap')
        if 'Error (' in result or str(m) not in checkResult or 'clone':
            FailFlag = True
            tolog('Fail: lunmap -a addlun -p clone -i ' + initID[0] + ' -l ' + cID + ' -m ' + str(m) )
        m = m + 1

    return FailFlag

def bvt_verifyLunmapDellun(c):
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
        if 'Error (' in result or ('    ' + cID + '    ')  in checkResult:
            FailFlag = True
            tolog('Fail: lunmap -a dellun -p clone -i ' + initID[0] + ' -l ' + cID )

    return FailFlag

def bvt_verifyLunmapEnable(c):
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

    return FailFlag

def bvt_verifyLunmapDel(c):
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

    return FailFlag

def bvt_verifyLunmapDisable(c):
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

    return FailFlag

def bvt_verifyLunmapSpecifyInexistentId(c):
    FailFlag = False
    tolog(" Verify lunmap specify inexistent Id ")
    # -i <InitiatorId> (0,2047)
    # -l <Volume ID list> (0,1023)
    initiatorInfo = SendCmd(c, 'initiator')
    initID = initiatorInfo.split('Id: ')[-1].split()[0]

    volumeInfo = SendCmd(c, 'volume')
    volumeID = volumeInfo.split('\r\n')[-3].split()[0]
    if int(initID) != 2047:
        result = SendCmd(c, 'lunmap -a add -i ' + str(int(initID)+1) + ' -p volume -l ' + volumeID + ' -m 0')
        if 'Error (' not in result or 'Invalid initiator index' not in result:
            FailFlag = True
            tolog(' lunmap -a add -i ' + str(int(initID)+1) + ' -p volume -l ' + volumeID + ' -m 0')
    else:
        tolog(' Precondition failure ')

    if int(volumeID) != 1023:
        result = SendCmd(c, 'lunmap -a add -i ' + initID + ' -p volume -l ' + str(int(volumeID) + 1) + ' -m 0')
        if 'Error (' not in result or 'Incorrect Parameters: Volume id' not in result:
            FailFlag = True
            tolog(' lunmap -a add -i ' + initID + ' -p volume -l ' + str(int(volumeID) + 1) + ' -m 0')
    else:
        tolog(' Precondition failure ')

    return FailFlag

def bvt_verifyLunmapInvalidOption(c):
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

    return FailFlag

def bvt_verifyLunmapInvalidParameters(c):
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

    return FailFlag

def bvt_verifyLunmapMissingParameters(c):
    FailFlag = False
    tolog("Verify lunmap missing parameters")
    command = ['lunmap -i', 'lunmap -a list -i', 'lunmap -a add -i', 'lunmap -a del -i', 'lunmap -a addlun -i', 'lunmap -a dellun -i']
    for com in command:
        tolog(' Verify ' + com )
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('Fail: ' + com )

    return FailFlag

def bvt_cleanUp(c):
    poolInfo = SendCmd(c, 'pool')
    row = poolInfo.split('\r\n')
    for i in range(4, len(row)):
        if 'Ptestlunmap' in row[i]:
            SendCmd(c, 'pool -a del -i ' + row[i].split()[0])
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
    bvt_verifyLunmapAdd(c)
    bvt_verifyLunmap(c)
    bvt_verifyLunmapList(c)
    bvt_verifyLunmapAddlun(c)
    bvt_verifyLunmapDellun(c)
    bvt_verifyLunmapEnable(c)
    bvt_verifyLunmapDel(c)
    bvt_verifyLunmapDisable(c)
    bvt_verifyLunmapSpecifyInexistentId(c)
    bvt_verifyLunmapInvalidOption(c)
    bvt_verifyLunmapInvalidParameters(c)
    bvt_verifyLunmapMissingParameters(c)
    bvt_cleanUp(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped