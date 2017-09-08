# -*- coding: utf-8 -*-
import unittest, time, re
import testlink
import string
from HTMLParser import HTMLParser
from ssh_connect import ssh_conn
import importlib

def getduration(timestr):
    sec_min = 0
    timelist = list()
    timelist = string.split(timestr, ':')

    if int(timelist[2]) >= 30:
        sec_min = 1
    min = int(timelist[0]) * 60 + int(timelist[1]) + sec_min

    return min

def run_function(function):
    function()

from sgmllib import SGMLParser

class URLLister(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.urls = []

    def start_a(self, attrs):
        href = [v for k, v in attrs if k =='href']
        if href:
            self.urls.extend(href)

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

if __name__ == "__main__":

    robot = "31c13726fc2bae727aa02faaaa574892"
    new_adminjl_key = robot

    new_ip_testlink = "http://192.168.252.104/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
    tls = testlink.TestlinkAPIClient(new_ip_testlink, new_adminjl_key)

    # test case notes

    c,ssh = ssh_conn()

    cmd = ''
    stepsnum = 0
    Notes = '/home/work/zach/clitest/testlink.notes'

    NeedRun = False

    for project in tls.getProjects():
        # print project
        if project['name'] == 'HyperionDS':

            #print tls.getProjectTestPlans
            #print tls.whatArgs('getTestCasesForTestSuite')
            # get test suites for the project
            #print tls.getFirstLevelTestSuitesForTestProject(project['id'])
            # -2 refers to CLIexecution
            # -1 refers to GUIexecution
            # 0 refers to APIexecution

            testsuiteID = tls.getFirstLevelTestSuitesForTestProject(project['id'])[0]['id']
            testsuiteName = tls.getFirstLevelTestSuitesForTestProject(project['id'])[0]['name']

            hastestsuite = False
            testsuite = tls.getTestCasesForTestSuite(testsuiteID,True,'full')

            for testplan in tls.getProjectTestPlans(project['id']):

                if "BuildVerification" in testplan["name"]:
                    tcdict = tls.getTestCasesForTestPlan(testplan['id'])

                    if tcdict:
                        for vaule in tcdict.values():
                            for eachplatform,testcase in vaule.items():
                                testcaseid=testcase["tcase_id"]

                                TC_Platform = eachplatform

                                Platform_Name = testcase['platform_name']
                                TC_Name = testcase['tcase_name']
                                TC_execution = testcase['exec_status']
                                TC_exec_on_build=testcase['exec_on_build']
                                TC_exec_status=testcase['exec_status']

                                tcsteps = tls.getTestCase(testcase['tcase_id'])[0]['steps']

                                steps = [{'step_number': '1',
                                          'notes': '-------------------------------------------------------------\r\nPromise VTrak Command Line Interface (CLI) Utility\r\nVersion: 11.01.0000.63 Build Date: Dec 16, 2016\r\n-------------------------------------------------------------\r\n \r\n-------------------------------------------------------------\r\nType help or ? to display all the available commands\r\n-------------------------------------------------------------\r\n \r\nadministrator@cli> array -a add -p 1,2,3 -l "ID=2,alias=L0,raid=5,capacity=10gb,stripe=512kb,sector=4kb,writepolicy=writeback,readpolicy=nocache,parity=left"\r\nWarning: ld no. 1 - exceeds max sector size, adjust to 512 Bytes\r\nError (0x4021): Physical drive in use\r\n \r\nadministrator@cli> ',
                                          'result': 'p'}, {'step_number': '2',
                                                           'notes': '-------------------------------------------------------------\r\nPromise VTrak Command Line Interface (CLI) Utility\r\nVersion: 11.01.0000.63 Build Date: Dec 16, 2016\r\n-------------------------------------------------------------\r\n \r\n-------------------------------------------------------------\r\nType help or ? to display all the available commands\r\n-------------------------------------------------------------\r\n \r\nadministrator@cli> logdrv -v\r\n \r\n-------------------------------------------------------------------------------\r\nLdId: 0                                LdType: HDD\r\nArrayId: 0                             SYNCed: Yes\r\nOperationalStatus: OK\r\nAlias: \r\nSerialNo: 495345200000000000000000E27BAA63DF120006\r\nWWN: 22bc-0001-5556-12f2               PreferredCtrlId: 1\r\nRAIDLevel: RAID5                       StripeSize: 64 KB\r\nCapacity: 2 GB                         PhysicalCapacity: 3 GB\r\nReadPolicy: NoCache                    WritePolicy: WriteThru\r\nCurrentWritePolicy: WriteThru\r\nNumOfUsedPD: 3                         NumOfAxles: 1\r\nSectorSize: 512 Bytes                  RAID5&6Algorithm: right asymmetric (4)\r\nTolerableNumOfDeadDrivesPerAxle: 1     ParityPace: N/A\r\nRaid6Scheme: N/A\r\nHostAccessibility: Normal\r\nALUAAccessStateForCtrl1: Active/optimized\r\nALUAAccessStateForCtrl2: Standby\r\nAssociationState: no association on this logical drive\r\nStorageServiceStatus: no storage service running\r\nPerfectRebuild: Disabled\r\n \r\nadministrator@cli> ',
                                                           'result': 'p'}]

                                TC_Result_Steps = list()
                                stepnote = list()

                                buildnamelist = tls.getBuildsForTestPlan(testplan['id'])
                                buildname = buildnamelist[-1]['name']
                                newbuildnum = open("/home/work/jackyl/Scripts/clitest/buildnum", "r").readline().rstrip()

                                if buildname != newbuildnum and "12.2" in newbuildnum:

                                    buildname = tls.createBuild(testplan['id'], newbuildnum, "auto")

                                buildnamelist = tls.getBuildsForTestPlan(testplan['id'])
                                buildname = buildnamelist[-1]['name']
                                testplanexec = tls.getTestCasesForTestPlan(testplan['id'])
                                exec_onbuild = TC_exec_on_build

                                if buildnamelist[-1]['id'] > exec_onbuild:
                                    NeedRun = True

                                    for each in testsuite:
                                        if each['id'] == testcaseid:
                                            testsuitename = each['tsuite_name']
                                            hastestsuite = True
                                            break

                                    loginname = tls.getTestCaseAssignedTester(testplan['id'],
                                                                              testcase['full_external_id'],
                                                                              buildname=buildname,
                                                                              platformname=Platform_Name)

                                    if hastestsuite:
                                        print "The "+testcase["tcase_name"]+" under " + testplan['name'] + " of " + project[
                                             'name'] + " are as following:\n"
                                        start = time.time()
                                        # convert the testsuite name into module that will be imported into
                                        TSuiteName = importlib.import_module(testsuitename, package="Tasks")
                                        # print tls.getTestCase(TC_Platform['tcase_id'])
                                        # if >= 2 steps, 2017-01-06
                                        stepsnum = len(tcsteps)
                                        for i in range(stepsnum):
                                            wrongflag = False
                                            open(Notes, 'w').close()
                                            stepstr = (string.replace(
                                                string.replace(string.replace(tcsteps[i]['actions'], '<p>\n\t', ''), '</p>',
                                                               ''),
                                                '&quot;', '"'))

                                            func = stepstr.split('\n')

                                            abc = getattr(TSuiteName, func[0], func[1])

                                            parameter = func[1]

                                            if ssh.get_transport().is_active() != True:
                                                c, ssh = ssh_conn()
                                            if parameter:
                                                abc(c, parameter)
                                            else:
                                                try:
                                                    abc(c)
                                                finally:
                                                    fp = open(Notes, 'r')
                                                    note = fp.read()
                                                    fp.close()
                                                    while "'result':" in note:
                                                        if "'result': 'f'" in note:
                                                            step_Result = 'f'
                                                            note = string.replace(note, "'result': 'f'", '')
                                                        else:
                                                            step_Result = 'p'
                                                            note = string.replace(note, "'result': 'p'", '')

                                                    else:
                                                        step_Result = 'f'
                                                        with open(Notes, "r+") as f:
                                                            content = f.read()
                                                            f.write(content + "\n" + "'result': 'f'")
                                                            f.close()

                                                    TC_Result_Steps.append(
                                                        {'step_number': str(i + 1), 'result': step_Result, 'notes': note})

                                        for each in TC_Result_Steps:
                                            if each['result'] != 'p':
                                                TC_Result = 'f'
                                                break
                                            else:
                                                TC_Result = 'p'

                                        # update test result remotely using API

                                        Update_timestamp = (
                                            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                                        # duration_min = getduration(str(TC_execution_duration))
                                        elasped = time.time() - start
                                        duration_min = str(elasped / 60)
                                        buildnamelist = tls.getBuildsForTestPlan(testplan['id'])
                                        buildname = buildnamelist[-1]['name']

                                        getExecution = tls.reportTCResult(testcase['tcase_id'], testplan['id'],
                                                                          buildname, TC_Result,
                                                                          'automated test cases', guess=True,
                                                                          testcaseexternalid=testcase['external_id'],
                                                                          platformname=testcase['platform_name'],
                                                                          execduration=duration_min,
                                                                          timestamp=Update_timestamp,
                                                                          steps=TC_Result_Steps)

                                        if TC_Name == "build_verification":
                                            serv = "211.150.65.81"
                                            u = "hulda.zhao@cn.promise.com"
                                            p = "ptb123456"
                                            import smtplib
                                            import urllib

                                            # Import the email modules we'll need
                                            from email.mime.text import MIMEText

                                            if getExecution[0]['status']:

                                                link = "http://192.168.252.104/testlink/lib/execute/execPrint.php?id=" + str(
                                                    getExecution[0]['id'])

                                                fp = urllib.urlopen(link)

                                                msg = MIMEText(
                                                    strip_tags(fp.read()).replace(".notprintable { display:none;}",
                                                                                  "").replace("lnl.php?type=exec=",
                                                                                              "execPrint.php?id=").replace(
                                                        "<!-- var fRoot = 'http://192.168.252.104/testlink/lib/execute/'; -->",
                                                        ""))

                                                msg[
                                                    'Subject'] = 'Build verification testing on %s is completed, the result is %s, please check the link for detail' % (
                                                buildname, TC_Result)
                                                msg['From'] = 'hulda.zhao@cn.promise.com'
                                                msg['To'] = 'hulda.zhao@cn.promise.com'
                                                # rec = ['ken.hou@cn.promise.com', 'hulda.zhao@cn.promise.com']
                                                rec = ['zach.feng@cn.promise.com','hulda.zhao@cn.promise.com']
                                                # Send the message via our own SMTP server, but don't include the
                                                # envelope header.
                                                u = u
                                                serv = serv
                                                p = p

                                                s = smtplib.SMTP(serv)
                                                s.login(u, p)
                                                s.sendmail(msg['From'], rec, msg.as_string())

    ssh.close()

