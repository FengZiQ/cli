# coding=utf-8
# 2017.9.5

from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
import time

Pass = "'result': 'p'"
Fail = "'result': 'f'"

def findPoolId(c):
    pdInfo = SendCmd(c, 'phydrv')
    pdId = []
    poolId = []
    if 'Pool' in pdInfo:
        poolInfo = SendCmd(c, 'pool')
        poolRow = poolInfo.split('\r\n')
        for row in poolRow:
            if len(row.split()) >= 9:
                poolId.append(row.split()[0])
        for i in poolId:
            SendCmd(c, 'pool -a del -y -f -i ' + i)
        findPoolId(c)
    else:
        pdRows = pdInfo.split('\r\n')
        for row in pdRows:
            if len(row.split()) >= 10 and "HDD" in row and 'Unconfigured' in row:
                pdId.append(row.split()[0])

    if len(pdId) >= 3:
        SendCmd(c, 'pool -a add -s "name=TestNASShare,raid=5" -p ' + pdId[0] + ',' + pdId[1] + ',' + pdId[3])

    plId = '0'
    return plId

def addNASShare(c):
    Failflag = False
    tolog('Add NASShare \r\n')

    # test data
    poolId = findPoolId(c)
    parameters = {
        "name": ['X', '1_a', 'N'*32],
        "capacity": ['1GB', '2GB', '1TB'],
        "recsize": ['128KB', '512B', '1MB'],
        "sync": ['always', 'standard', 'disabled'],
        "logbias": ['latency', 'throughput', 'throughput']
    }
    capacity = ['TotalCapacity: 1 GB', 'TotalCapacity: 2 GB', 'TotalCapacity: 1 TB']
    recsize = ['RecordSize: 128 KB', 'RecordSize: 512 Bytes', 'RecordSize: 1 MB']

    for i in range(3):
        settings = 'name=' + parameters["name"][i] + ',' + \
        'capacity=' + parameters["capacity"][i] + ',' + \
        'recsize='+ parameters["recsize"][i] + ',' + \
        'sync=' + parameters["sync"][i] + ',' + \
        'logbias=' + parameters["logbias"][i]

        tolog('Expect: NASShare settings are ' + settings + '\r\n')

        result = SendCmd(c, 'nasshare -a add -p ' + poolId + ' -s "' + settings + '"')
        checkResult = SendCmd(c, 'nasshare -v -i ' + str(i))

        if 'Error (' in result:
            Failflag = True
            tolog('Fail: NASShare settings are ' + settings + '\r\n')
        else:
            tolog('Actual: NASShare is added successful \r\n')

            if parameters["name"][i] not in checkResult:
                Failflag = True
                tolog('Fail: please checkout parameter ' + parameters["name"][i] + '\r\n')

            if capacity[i] not in checkResult:
                Failflag = True
                tolog('Fail: please checkout parameter ' + parameters["capacity"][i] + '\r\n')

            if recsize[i] not in checkResult:
                Failflag = True
                tolog('Fail: please checkout parameter ' + parameters["recsize"][i] + '\r\n')

            if parameters["sync"][i] not in checkResult:
                Failflag = True
                tolog('Fail: please checkout parameter ' + parameters["sync"][i] + '\r\n')

            if parameters["logbias"][i] not in checkResult:
                Failflag = True
                tolog('Fail: please checkout parameter ' + parameters["logbias"][i] + '\r\n')

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

    return Failflag

def listNASShare(c):
    Failflag = False
    # list all of NASShare
    tolog('List all of NASShare \r\n')

    # test data
    nasShareId = []

    tolog('Expect: list all of NASShare \r\n')
    nasShareInfo = SendCmd(c, 'nasshare')

    if 'Error (' in nasShareInfo:
        tolog('Fail: Did not list all of NASShare')
    else:
        tolog('Actual: all of NASShare are listed \r\n')

    totalRow = nasShareInfo.split('\r\n')

    for row in totalRow:
        if len(row.split()) >= 9:
            nasShareId.append(row.split()[0])

    if len(nasShareId) > 0:
        tolog('To list specify NASShare \r\n')
        for i in nasShareId:
            tolog('Expect: To list ' + i + ' NASShare \r\n')
            result = SendCmd(c, 'nasshare -i ' + i)

            if 'Error (' in result:
                Failflag = True
                tolog('Fail: To list ' + i + ' NASShare \r\n')
            else:
                tolog('Actual: NASShare ' + i + ' is listed')

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

    return Failflag

def listVerboseNASShare(c):
    Failflag = False
    # list all of NASShare by verbose model
    tolog('List all of NASShare by verbose model \r\n')

    # test data
    nasShareId = []
    nasShareInfo = SendCmd(c, 'nasshare')
    totalRow = nasShareInfo.split('\r\n')

    for row in totalRow:
        if len(row.split()) >= 9:
            nasShareId.append(row.split()[0])

    tolog('Expect: list all of NASShare by verbose model \r\n')

    VnasShareInfo = SendCmd(c, 'nasshare -v')

    if 'Error (' in VnasShareInfo:
        tolog('Fail: Did not list all of NASShare by verbose model')
    else:
        tolog('Actual: all of NASShare by verbose model are listed \r\n')

    if len(nasShareId) > 0:
        tolog('To list specify NASShare by verbose model \r\n')
        for i in nasShareId:
            tolog('Expect: To list ' + i + ' NASShare by verbose model \r\n')
            result = SendCmd(c, 'nasshare -v -i ' + i)

            if 'Error (' in result:
                Failflag = True
                tolog('Fail: To list ' + i + ' NASShare by verbose model \r\n')
            else:
                tolog('Actual: NASShare by verbose model ' + i + ' is listed')

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

    return Failflag

def modNASShare(c):
    Failflag = False
    tolog('Modify NASShare \r\n')

    # test data
    parameters = {
        "name": ['test_modify', '1', 'N'*31],
        "capacity": ['1GB', '2GB', '1TB']
    }
    capacity = ['TotalCapacity: 1 GB', 'TotalCapacity: 2 GB', 'TotalCapacity: 1 TB']

    nasShareId = []
    nasShareInfo = SendCmd(c, 'nasshare')
    totalRow = nasShareInfo.split('\r\n')

    for row in totalRow:
        if len(row.split()) >= 9:
            nasShareId.append(row.split()[0])

    if len(nasShareId) > 0:
        for i in range(3):
            settings = 'name=' + parameters["name"][i] + ',' + \
            'capacity=' + parameters["capacity"][i]

            tolog('Expect: The NASShare ' + nasShareId[0] + ' can be modified \r\n')

            result = SendCmd(c, 'nasshare -a mod -i ' + nasShareId[0] + ' -s "' + settings + '"')
            checkResult = SendCmd(c, 'nasshare -v -i ' + nasShareId[0])

            if 'Error (' in result:
                Failflag = True
                tolog('Fail: To modify NASShare ' + nasShareId[0] + ' is failed')
            else:
                tolog('Actual: The NASShare ' + nasShareId[0] + ' is modified \r\n')

                if parameters["name"][i] not in checkResult:
                    Failflag = True
                    tolog('Fail: please checkout parameter ' + parameters["name"][i] + '\r\n')

                if capacity[i] not in checkResult:
                    Failflag = True
                    tolog('Fail: please checkout parameter ' + parameters["capacity"][i] + '\r\n')
    else:
        tolog('No NASShare can be used')

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

    return Failflag

def mountNASShare(c):
    Failflag = False
    tolog('Mounted NASShare \r\n')

    # test data
    nasShareId = []
    nasShareInfo = SendCmd(c, 'nasshare')
    totalRow = nasShareInfo.split('\r\n')

    for row in totalRow:
        if len(row.split()) >= 9:
            nasShareId.append(row.split()[0])

    if 'Un-Mounted' in totalRow[4]:
        tolog('Expect: Mount NASShare ' + nasShareId[0] + '\r\n')

        result = SendCmd(c, 'nasshare -a mount -i ' + nasShareId[0])
        checkResult = SendCmd(c, 'nasshare -i ' + nasShareId[0])

        if 'Error (' in result:
            Failflag = True
            tolog('Fail: Mount NASShare ' + nasShareId[0] + '\r\n')
        else:
            if 'Mounted' in checkResult:
                tolog('Actual: NASShare ' + nasShareId[0] + ' is mounted\r\n')
            else:
                Failflag = True
                tolog('Fail: please check NASShare status')
    else:
        SendCmd(c, 'nasshare -a unmount -i ' + nasShareId[0])

        tolog('Expect: Mount NASShare ' + nasShareId[0] + '\r\n')

        result = SendCmd(c, 'nasshare -a mount -i ' + nasShareId[0])
        checkResult = SendCmd(c, 'nasshare -i ' + nasShareId[0])

        if 'Error (' in result:
            Failflag = True
            tolog('Fail: Mount NASShare ' + nasShareId[0] + '\r\n')
        else:
            if 'Mounted' in checkResult:
                tolog('Actual: NASShare ' + nasShareId[0] + ' is mounted\r\n')
            else:
                Failflag = True
                tolog('Fail: please check NASShare status')

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

    return Failflag

def unmountNASShare(c):
    Failflag = False
    tolog('Un-Mount NASShare \r\n')

    # test data
    nasShareId = []
    nasShareInfo = SendCmd(c, 'nasshare')
    totalRow = nasShareInfo.split('\r\n')

    for row in totalRow:
        if len(row.split()) >= 9:
            nasShareId.append(row.split()[0])

    if 'Mounted' in totalRow[4]:
        tolog('Expect: Un-Mount NASShare ' + nasShareId[0] + '\r\n')

        result = SendCmd(c, 'nasshare -a unmount -i ' + nasShareId[0])
        checkResult = SendCmd(c, 'nasshare -i ' + nasShareId[0])

        if 'Error (' in result:
            Failflag = True
            tolog('Fail: Un-Mount NASShare ' + nasShareId[0] + '\r\n')
        else:
            if 'Un-Mounted' in checkResult:
                tolog('Actual: NASShare ' + nasShareId[0] + ' is unmounted\r\n')
            else:
                Failflag = True
                tolog('Fail: please check NASShare status')
    else:
        SendCmd(c, 'nasshare -a mount -i ' + nasShareId[0])

        tolog('Expect: Un-Mount NASShare ' + nasShareId[0] + '\r\n')

        result = SendCmd(c, 'nasshare -a unmount -i ' + nasShareId[0])
        checkResult = SendCmd(c, 'nasshare -i ' + nasShareId[0])

        if 'Error (' in result:
            Failflag = True
            tolog('Fail: Un-Mount NASShare ' + nasShareId[0] + '\r\n')
        else:
            if 'Un-Mounted' in checkResult:
                tolog('Actual: NASShare ' + nasShareId[0] + ' is unmounted\r\n')
            else:
                Failflag = True
                tolog('Fail: please check NASShare status')
    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

    return Failflag

def helpNASShare(c):
    Failflag = False

    tolog('Verify NASShare help document\r\n')

    result = SendCmd(c, 'nasshare -h')

    if 'Error (' in result or 'Usage' not in result or 'Summary' not in result:
        Failflag = False
        tolog('Fail: nasshare -h')

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

    return Failflag

def failedTest_InexistentId(c):
    Failflag = False
    tolog('To specify inexistent id \r\n')

    failedSetting = [
        'nasshare -a add -p 100 -s "name=failTest, capacity=2GB"',
        'nasshare -a mod -i 100 -s "name=test"',
        'nasshare -a mount -i 100',
        'nasshare -a unmount -i 100',
        'nasshare -a del -i 100'
    ]

    tolog('Expect: To hint id is not existent \r\n')

    for i in range(len(failedSetting)):

        result = SendCmd(c, failedSetting[i])

        if 'Error (' not in result or 'id=[100] is not existed' not in result:
            Failflag = True
            tolog('Fail: ' + failedSetting[i] + '\r\n')

    anotherResult = SendCmd(c, 'nasshare -i 100')

    if 'specific nas share not exists' not in anotherResult:
        Failflag = True
        tolog('Fail: nasshare -a i 100')

    if Failflag:
        tolog(Fail)
    else:
        tolog('\r\nActual: To hint and correct error \r\n')
        tolog(Pass)

    return Failflag

def failedTest_InvalidOption(c):
    Failflag = False
    tolog('To input inexistent option \r\n')

    failedSetting = [
        'nasshare -x',
        'nasshare -a add -p 100 -s "option=failTest, test=2GB"',
        'nasshare -a mod -i 100 -s "invalid=test"',
        'nasshare -a mount -x 100',
        'nasshare -a unmount -x 100'
        'nasshare -a del -x'
    ]

    tolog('Expect: To input inexistent option will hint invalid option \r\n')

    for i in range(len(failedSetting)):
        result = SendCmd(c, failedSetting[i])

        if 'Error (' not in result or 'Invalid option' not in result:
            Failflag = False
            tolog('Fail: ' + failedSetting[i])

    if Failflag:
        tolog(Fail)
    else:
        tolog('\r\nActual: It will hint and correct error when inputs inexistent option \r\n')
        tolog(Pass)

    return Failflag

def failedTest_InvalidParameters(c):
    Failflag = False
    tolog('To input invalid parameter \r\n')

    failedSetting = [
        'nasshare x',
        'nasshare -a add -p 0 -s "name=%$^&@^$, capacity=2GB"',
        'nasshare -a add -p 0 -s "name=test, capacity=x"',
        'nasshare -a add -p 0 -s "name=test, capacity=2GB, recsize=x"',
        'nasshare -a add -p 0 -s "name=test, capacity=2GB, sync=x"',
        'nasshare -a add -p 0 -s "name=test, capacity=2GB, logbias=x"',
        'nasshare -a mod -i 0 -s "name=@$%&*"',
        'nasshare -a mod -i 0 -s "capacity=x"',
        'nasshare -a mount x',
        'nasshare -a unmount x'
        'nasshare -a del x'
    ]

    tolog('Expect: To hint error message that contains invalid parameter \r\n')

    for i in range(len(failedSetting)):

        result = SendCmd(c, failedSetting[i])

        if 'Error (' not in result or 'Invalid setting parameters' not in result:
            Failflag = True
            tolog('Fail: ' + failedSetting[i])

    if Failflag:
        tolog(Fail)
    else:
        tolog('\r\nActual: To hint error and correct error \r\n')
        tolog(Pass)

    return Failflag

def failedTest_MissingParameters(c):
    Failflag = False
    tolog('Verify missing parameter \r\n')

    failedSetting = [
        'nasshare -i',
        'nasshare -a add',
        'nasshare -a add -p 0 -s ',
        'nasshare -a mod -i',
        'nasshare -a mod -i 0 -s ',
        'nasshare -a mount',
        'nasshare -a mount -i',
        'nasshare -a unmount',
        'nasshare -a unmount -i',
        'nasshare -a del',
        'nasshare -a del -i'
    ]

    tolog('Expect: To hint error message that contains missing parameter \r\n')

    for i in range(len(failedSetting)):

        result = SendCmd(c, failedSetting[i])

        if 'Error (' not in result or 'Missing parameter' not in result:
            Failflag = True
            tolog('Fail: ' + failedSetting[i])

    if Failflag:
        tolog(Fail)
    else:
        tolog('\r\nActual: To hint error and correct error')
        tolog(Pass)

    return Failflag

def deleteNASShare(c):
    Failflag = False

    # test data
    nasShareId = []
    nasShareName = ['X', '1_a', 'N'*32]

    nasShareInfo = SendCmd(c, 'nasshare')
    totalRow = nasShareInfo.split('\r\n')

    for row in totalRow:
        if len(row.split()) >= 9:
            nasShareId.append(row.split()[0])

    tolog('To delete NASShare \r\n')

    for i in nasShareId:
        tolog('Expect: delete NASShare ' + i + '\r\n')
        result = SendCmd(c, 'nasshare -a del -i ' + i)
        checkResult = SendCmd(c, 'nasshare')

        if 'Error (' in result or nasShareName[int(i)] in checkResult:
            Failflag = True
            tolog('Fail: to delete NASShare ' + i + ' is failed \r\n')
        else:
            tolog('Actual: NASShare ' + i + ' is deleted \r\n')

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

    # clean up environment
    tolog('\r\nclean up environment \r\n')
    SendCmd(c, 'pool -a del -y -f -i 0')

    return Failflag

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    addNASShare(c)
    listNASShare(c)
    listVerboseNASShare(c)
    modNASShare(c)
    mountNASShare(c)
    unmountNASShare(c)
    helpNASShare(c)
    failedTest_InexistentId(c)
    failedTest_InvalidOption(c)
    failedTest_InvalidParameters(c)
    failedTest_MissingParameters(c)
    deleteNASShare(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped