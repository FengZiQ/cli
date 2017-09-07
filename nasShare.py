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

    return Failflag


def failedTestNASShare(c):
    Failflag = False
    tolog('NASShare of failed test \r\n')
    failedSetting = [

    ]


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    # addNASShare(c)
    # listNASShare(c)
    # modNASShare(c)
    # mountNASShare(c)
    # unmountNASShare(c)
    # deleteNASShare(c)
    failedTestNASShare(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped