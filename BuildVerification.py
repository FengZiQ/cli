# coding=utf-8

import pool
from time import sleep
from send_cmd import *
from ssh_connect import *
from to_log import *

Pass = "'result': 'p'"
Fail = "'result': 'f'"

def BuildVerification(c):

    flashimage = False
    Failflag = False

    count = 0
    FailCasesList = []
    c, ssh = ssh_conn()

    versioninfo = SendCmd(c, "about")

    currentbuild = versioninfo.split("Version: ")[1][:13]

    tftpbuildnumber = open("/home/work/zach/clitest/buildnum","r").readline().rstrip()

    print "currentbuild,", currentbuild
    print "tftpbuildnumber,", tftpbuildnumber

    filename = ''

    if (("13." in currentbuild and "13." in tftpbuildnumber)
        and (int(currentbuild.split(".")[-1]) < int(tftpbuildnumber.split(".")[-1]))) \
            or (("12.00" in currentbuild and "12.0" in tftpbuildnumber)
                and (int(currentbuild.split(".")[-1]) < int(tftpbuildnumber.split(".")[-1]))) \
            or (("12.01" in currentbuild and "12.1" in tftpbuildnumber)
                and (int(currentbuild.split(".")[-1]) < int(tftpbuildnumber.split(".")[-1]))) \
            or (("12.02" in currentbuild and "12.2" in tftpbuildnumber)
                and (int(currentbuild.split(".")[-1]) < int(tftpbuildnumber.split(".")[-1]))):

        if "13." in tftpbuildnumber:
            filename = "d5k-multi-13_0_0000_" + tftpbuildnumber.split(".")[-1]

        elif "12.0" in tftpbuildnumber:
            filename = "d5k-multi-12_0_9999_" + tftpbuildnumber.split(".")[-1]

        elif "12.1" in tftpbuildnumber:
            filename = "d5k-multi-12_1_9999_" + tftpbuildnumber.split(".")[-1]

        elif "12.2" in tftpbuildnumber:
            filename = "d5k-multi-12_2_9999_" + tftpbuildnumber.split(".")[-1]

        tolog("%s will be updated to the %s" % (filename, server))
        flashimage = True
        SendCmdRestart(c, "ptiflash -y -t -s 10.84.2.99 -f "+filename+".ptif")

    if flashimage:
        i = 1
        while i < 160:
            # wait for rebooting
           tolog("ptiflash is in progress, please wait, %d seconds elapse" % i)
           i += 1
           sleep(1)

        # check if ssh connection is ok.
        # wait for another 40 seconds
        reconnectflag = False

        for x in range(30):
            try:
                c,ssh = ssh_conn()
                reconnectflag = True
                break
            except Exception, e:
                print e
                sleep(4)

        if reconnectflag:
            import pool
            tolog("Start verifying pool add")
            if (pool.bvtpoolcreateandlist(c, 1)):
                FailCasesList.append('The case ' + pool.bvtpoolcreateandlist.__name__ + ' failed')

            tolog("Start verifying spare add")
            if (pool.bvtsparedrvcreate(c, 2)):
                FailCasesList.append('The case ' + pool.bvtsparedrvcreate.__name__ + ' failed')

            tolog("Start verifying delete spare")
            if (pool.bvtsparedelete(c)):
                FailCasesList.append('The case ' + pool.bvtsparedelete.__name__ + ' failed')

            tolog("Start verifying pool global setting")
            if (pool.bvtpoolglobalsetting(c)):
                FailCasesList.append('The case ' + pool.bvtpoolglobalsetting.__name__ + ' failed')

            tolog("Start verifying volume add")
            if (pool.bvtvolumecreateandlist(c, 10)):
                FailCasesList.append('The case ' + pool.bvtvolumecreateandlist.__name__ + ' failed')

            tolog("Start verifying snapshot add")
            if (pool.bvtsnapshotcreateandlist(c, 2)):
                FailCasesList.append('The case ' + pool.bvtsnapshotcreateandlist.__name__ + ' failed')

            tolog("Start verifying clone add")
            if (pool.bvtclonecreateandlist(c, 2)):
                FailCasesList.append('The case ' + pool.bvtclonecreateandlist.__name__ + ' failed')

            tolog("Start verifying delete clone")
            if (pool.bvtclonedelete(c)):
                FailCasesList.append('The case ' + pool.bvtclonedelete.__name__ + ' failed')

            tolog("Start verifying delete snapshot")
            if (pool.bvtsnapshotdelete(c)):
                FailCasesList.append('The case ' + pool.bvtsnapshotdelete.__name__ + ' failed')

            tolog("Start verifying delete volume")
            if (pool.bvtvolumedel(c)):
                FailCasesList.append('The case ' + pool.bvtvolumedel.__name__ + ' failed')

            tolog("Start verifying delete pool")
            if (pool.bvtpooldel(c)):
                FailCasesList.append('The case ' + pool.bvtpooldel.__name__ + ' failed')

            tolog("Start verifying pool add for a second time")
            if (pool.bvtpoolcreateandlist(c, 0)):
                FailCasesList.append('The case ' + pool.bvtpoolcreateandlist.__name__ + ' failed')

            tolog("Start verifying pool global setting")
            if (pool.bvtpoolglobalsetting(c)):
                FailCasesList.append('The case ' + pool.bvtpoolglobalsetting.__name__ + ' failed')

            tolog("Start verifying volume add many")
            if (pool.bvtvolumeaddmany(c, 2)):
                FailCasesList.append('The case ' + pool.bvtvolumeaddmany.__name__ + ' failed')

            tolog("Start verifying snapshot add")
            if (pool.bvtsnapshotcreateandlist(c, 2)):
                FailCasesList.append('The case ' + pool.bvtsnapshotcreateandlist.__name__ + ' failed')

            tolog("Start verifying clone add")
            if (pool.bvtclonecreateandlist(c, 2)):
                FailCasesList.append('The case ' + pool.bvtclonecreateandlist.__name__ + ' failed')

            tolog("Start verifying clone export/unexport")
            if (pool.bvtexportunexport(c, "clone")):
                FailCasesList.append('The case ' + pool.bvtexportunexport.__name__ + ' failed')

            tolog("Start verifying snapshot export/unexport")
            if (pool.bvtexportunexport(c, "snapshot")):
                FailCasesList.append('The case ' + pool.bvtexportunexport.__name__ + ' failed')

            tolog("Start verifying volume export/unexport")
            if (pool.bvtexportunexport(c, "volume")):
                FailCasesList.append('The case ' + pool.bvtexportunexport.__name__ + ' failed')

            tolog("Start verifying pool force delete")
            if (pool.bvtforcedel(c, "pool")):
                FailCasesList.append('The case ' + pool.bvtforcedel.__name__ + ' failed')

            tolog("Start verifying pool add for 3rd time")
            if (pool.bvtpoolcreateandlist(c, 2)):
                FailCasesList.append('The case ' + pool.bvtpoolcreateandlist.__name__ + ' failed')

            tolog("Start verifying pool extend")
            if (pool.bvtpoolmodifyandlist(c)):
                FailCasesList.append('The case ' + pool.bvtpoolmodifyandlist.__name__ + ' failed')

            tolog("Start verifying volume add")
            if (pool.bvtvolumecreateandlist(c, 10)):
                FailCasesList.append('The case ' + pool.bvtvolumecreateandlist.__name__ + ' failed')

            tolog("Start verifying snapshot add")
            if (pool.bvtsnapshotcreateandlist(c, 2)):
                FailCasesList.append('The case ' + pool.bvtsnapshotcreateandlist.__name__ + ' failed')

            tolog("Start verifying clone add")
            if (pool.bvtclonecreateandlist(c, 2)):
                FailCasesList.append('The case ' + pool.bvtclonecreateandlist.__name__ + ' failed')

            tolog("Start verifying clone force delete")
            if (pool.bvtforcedel(c, "clone")):
                FailCasesList.append('The case ' + pool.bvtforcedel.__name__ + ' failed')

            tolog("Start verifying snapshot force delete")
            if (pool.bvtforcedel(c, "snapshot")):
                FailCasesList.append('The case ' + pool.bvtforcedel.__name__ + ' failed')

            tolog("Start verifying volume force delete")
            if (pool.bvtforcedel(c, "volume")):
                FailCasesList.append('The case ' + pool.bvtforcedel.__name__ + ' failed')

            if (pool.bvtforcedel(c, "pool")):
                FailCasesList.append('The case ' + pool.bvtforcedel.__name__ + ' failed')

            tolog("Start verifying pool create with all raid level and parameters")
            if (pool.bvtpoolcreateverify_newraidlevel(c)):
                FailCasesList.append('The case ' + pool.bvtpoolcreateverify_newraidlevel.__name__ + ' failed')

            tolog("Start verifying pool output error")
            if (pool.bvtpoolcreateverifyoutputerror_newraidlevel(c)):
                FailCasesList.append(
                    'The case ' + pool.bvtpoolcreateverifyoutputerror_newraidlevel.__name__ + ' failed')

            tolog("Start verifying about")
            import about
            if (about.verifyAbout(c)):
                FailCasesList.append('The case ' + about.verifyAbout.__name__ + ' failed')
            if (about.verifyAboutHelp(c)):
                FailCasesList.append('The case ' + about.verifyAboutHelp.__name__ + ' failed')
            if (about.verifyAboutInvalidOption(c)):
                FailCasesList.append('The case ' + about.verifyAboutInvalidOption.__name__ + ' failed')
            if (about.verifyAboutInvalidParameters(c)):
                FailCasesList.append('The case ' + about.verifyAboutInvalidParameters.__name__ + ' failed')

            tolog("Start verifying battery")
            import battery
            if (battery.verifyBattery(c)):
                FailCasesList.append('The case ' + battery.verifyBattery.__name__ + ' failed')
            if (battery.verifyBatteryList(c)):
                FailCasesList.append('The case ' + battery.verifyBatteryList.__name__ + ' failed')
            if (battery.verifyBatteryRecondition(c)):
                FailCasesList.append('The case ' + battery.verifyBatteryRecondition.__name__ + ' failed')
            if (battery.verifyBatteryHelp(c)):
                FailCasesList.append('The case ' + battery.verifyBatteryHelp.__name__ + ' failed')
            if (battery.verifyBatterySpecifyInexistentId(c)):
                FailCasesList.append('The case ' + battery.verifyBatterySpecifyInexistentId.__name__ + ' failed')
            if (battery.verifyBatteryInvalidOption(c)):
                FailCasesList.append('The case ' + battery.verifyBatteryInvalidOption.__name__ + ' failed')
            if (battery.verifyBatteryInvalidParameters(c)):
                FailCasesList.append('The case ' + battery.verifyBatteryInvalidParameters.__name__ + ' failed')
            if (battery.verifyBatteryMissingParameters(c)):
                FailCasesList.append('The case ' + battery.verifyBatteryMissingParameters.__name__ + ' failed')

            tolog("Start verifying BBM")
            import bbm
            if (bbm.verifyBBM(c)):
                FailCasesList.append('The case ' + bbm.verifyBBM.__name__ + ' failed')
            if (bbm.verifyBBMClear(c)):
                FailCasesList.append('The case ' + bbm.verifyBBMClear.__name__ + ' failed')
            if (bbm.verifyBBMHelp(c)):
                FailCasesList.append('The case ' + bbm.verifyBBMHelp.__name__ + ' failed')
            if (bbm.verifyBBMInvalidOption(c)):
                FailCasesList.append('The case ' + bbm.verifyBBMInvalidOption.__name__ + ' failed')
            if (bbm.verifyBBMInvalidParameters(c)):
                FailCasesList.append('The case ' + bbm.verifyBBMInvalidParameters.__name__ + ' failed')
            if (bbm.verifyBBMList(c)):
                FailCasesList.append('The case ' + bbm.verifyBBMList.__name__ + ' failed')
            if (bbm.verifyBBMMissingParameters(c)):
                FailCasesList.append('The case ' + bbm.verifyBBMMissingParameters.__name__ + ' failed')
            if (bbm.verifyBBMSpecifyInexistentId(c)):
                FailCasesList.append('The case ' + bbm.verifyBBMSpecifyInexistentId.__name__ + ' failed')
            (bbm.cleanUp(c))

            tolog("Start verifying bga")
            import bga
            if (bga.verifyBga(c)):
                FailCasesList.append('The case ' + bga.verifyBga.__name__ + ' failed')
            if (bga.verifyBgaList(c)):
                FailCasesList.append('The case ' + bga.verifyBgaList.__name__ + ' failed')
            if (bga.verifyBgaMod(c)):
                FailCasesList.append('The case ' + bga.verifyBgaMod.__name__ + ' failed')
            if (bga.verifyBgaHelp(c)):
                FailCasesList.append('The case ' + bga.verifyBgaHelp.__name__ + ' failed')
            if (bga.verifyBgaInvalidOption(c)):
                FailCasesList.append('The case ' + bga.verifyBgaInvalidOption.__name__ + ' failed')
            if (bga.verifyBgaInvalidParameters(c)):
                FailCasesList.append('The case ' + bga.verifyBgaInvalidParameters.__name__ + ' failed')
            if (bga.verifyBgaMissingParameters(c)):
                FailCasesList.append('The case ' + bga.verifyBgaMissingParameters.__name__ + ' failed')

            tolog("Start verifying buzzer")
            import buzzer
            if (buzzer.verifyBuzzerDisableAndSilentTurnOn((c))):
                FailCasesList.append('The case ' + buzzer.verifyBuzzerDisableAndSilentTurnOn.__name__ + ' failed')
            if (buzzer.verifyBuzzerEnableAndSilentTurnOn((c))):
                FailCasesList.append('The case ' + buzzer.verifyBuzzerEnableAndSilentTurnOn.__name__ + ' failed')
            if (buzzer.verifyBuzzerEnableAndSoundingTurnOn((c))):
                FailCasesList.append('The case ' + buzzer.verifyBuzzerEnableAndSoundingTurnOn.__name__ + ' failed')
            if (buzzer.verifyBuzzerDisableAndSilentTurnOff((c))):
                FailCasesList.append('The case ' + buzzer.verifyBuzzerDisableAndSilentTurnOff.__name__ + ' failed')
            if (buzzer.verifyBuzzerEnableAndSilentTurnOff((c))):
                FailCasesList.append('The case ' + buzzer.verifyBuzzerEnableAndSilentTurnOff.__name__ + ' failed')
            if (buzzer.verifyBuzzerEnableAndSoundingTurnOff((c))):
                FailCasesList.append('The case ' + buzzer.verifyBuzzerEnableAndSoundingTurnOff.__name__ + ' failed')
            if (buzzer.verifyBuzzerDisableAndSilentEnable((c))):
                FailCasesList.append('The case ' + buzzer.verifyBuzzerDisableAndSilentEnable.__name__ + ' failed')
            if (buzzer.verifyBuzzerEnableAndSilentEnable((c))):
                FailCasesList.append('The case ' + buzzer.verifyBuzzerEnableAndSilentEnable.__name__ + ' failed')
            if (buzzer.verifyBuzzerEnableAndSoundingEnable((c))):
                FailCasesList.append('The case ' + buzzer.verifyBuzzerEnableAndSoundingEnable.__name__ + ' failed')
            if (buzzer.verifyBuzzerEnableAndSoundingDisable((c))):
                FailCasesList.append('The case ' + buzzer.verifyBuzzerEnableAndSoundingDisable.__name__ + ' failed')
            if (buzzer.verifyBuzzerEnableAndSilentDisable((c))):
                FailCasesList.append('The case ' + buzzer.verifyBuzzerEnableAndSilentDisable.__name__ + ' failed')
            if (buzzer.verifyBuzzerDisableAndSilentDisable((c))):
                FailCasesList.append('The case ' + buzzer.verifyBuzzerDisableAndSilentDisable.__name__ + ' failed')
            if (buzzer.verifyBuzzerInfo((c))):
                FailCasesList.append('The case ' + buzzer.verifyBuzzerInfo.__name__ + ' failed')
            if (buzzer.verifyBuzzerHelp((c))):
                FailCasesList.append('The case ' + buzzer.verifyBuzzerHelp.__name__ + ' failed')
            if (buzzer.verifyBuzzerInvalidParameters((c))):
                FailCasesList.append('The case ' + buzzer.verifyBuzzerInvalidParameters.__name__ + ' failed')
            if (buzzer.verifyBuzzerInvalidOption((c))):
                FailCasesList.append('The case ' + buzzer.verifyBuzzerInvalidOption.__name__ + ' failed')

            # tolog("Start verifying chap")
            # import chap
            # (chap.verifyChapAdd(c))
            # (chap.verifyChap(c))
            # (chap.verifyChapList(c))
            # (chap.verifyChapMod(c))
            # (chap.verifyChapDel(c))
            # (chap.verifyChapHelp(c))
            # (chap.verifyChapSpecifyErrorId(c))
            # (chap.verifyChapInvalidOption(c))
            # (chap.verifyChapInvalidParameters(c))
            # (chap.verifyChapMissingParameters(c))

            import ctrl
            tolog("Start verifying ctrl")
            if (ctrl.verifyCtrl(c)):
                FailCasesList.append('The case ' + ctrl.verifyCtrl.__name__ + ' failed')
            if (ctrl.verifyCtrlSpecifyId(c)):
                FailCasesList.append('The case ' + ctrl.verifyCtrlSpecifyId.__name__ + ' failed')
            if (ctrl.verifyCtrlSpecifyInexistentId(c)):
                FailCasesList.append('The case ' + ctrl.verifyCtrlSpecifyInexistentId.__name__ + ' failed')
            if (ctrl.verifyCtrlList(c)):
                FailCasesList.append('The case ' + ctrl.verifyCtrlList.__name__ + ' failed')
            if (ctrl.verifyCtrlV(c)):
                FailCasesList.append('The case ' + ctrl.verifyCtrlV.__name__ + ' failed')
            if (ctrl.verifyCtrlListV(c)):
                FailCasesList.append('The case ' + ctrl.verifyCtrlListV.__name__ + ' failed')
            if (ctrl.verifyCtrlModNormativeAlias(c)):
                FailCasesList.append('The case ' + ctrl.verifyCtrlModNormativeAlias.__name__ + ' failed')
            if (ctrl.verifyCtrlModValuesIsEnableOrDisable(c)):
                FailCasesList.append('The case ' + ctrl.verifyCtrlModValuesIsEnableOrDisable.__name__ + ' failed')
            if (ctrl.verifyCtrlModValuesIsTime(c)):
                FailCasesList.append('The case ' + ctrl.verifyCtrlModValuesIsTime.__name__ + ' failed')
            if (ctrl.verifyCtrlClear(c)):
                FailCasesList.append('The case ' + ctrl.verifyCtrlClear.__name__ + ' failed')
            if (ctrl.verifyCtrlHelp(c)):
                FailCasesList.append('The case ' + ctrl.verifyCtrlHelp.__name__ + ' failed')
            if (ctrl.verifyCtrlInvalidOption(c)):
                FailCasesList.append('The case ' + ctrl.verifyCtrlInvalidOption.__name__ + ' failed')
            if (ctrl.verifyCtrlInvalidParameters(c)):
                FailCasesList.append('The case ' + ctrl.verifyCtrlInvalidParameters.__name__ + ' failed')
            if (ctrl.verifyCtrlMissingParameters(c)):
                FailCasesList.append('The case ' + ctrl.verifyCtrlMissingParameters.__name__ + ' failed')
            if (ctrl.verifyCtrlSpecifyInexistentId(c)):
                FailCasesList.append('The case ' + ctrl.verifyCtrlSpecifyInexistentId.__name__ + ' failed')

            tolog("Start verifying encldiag")
            import encldiag
            if (encldiag.verifyEncldiag(c)):
                FailCasesList.append('The case ' + encldiag.verifyEncldiag.__name__ + ' failed')
            if (encldiag.verifyEncldiagList(c)):
                FailCasesList.append('The case ' + encldiag.verifyEncldiagList.__name__ + ' failed')
            if (encldiag.verifyEncldiagHelp(c)):
                FailCasesList.append('The case ' + encldiag.verifyEncldiagHelp.__name__ + ' failed')
            if (encldiag.verifyEncldiagSpecifyInexistentId(c)):
                FailCasesList.append('The case ' + encldiag.verifyEncldiagSpecifyInexistentId.__name__ + ' failed')
            if (encldiag.verifyEncldiagInvalidOption(c)):
                FailCasesList.append('The case ' + encldiag.verifyEncldiagInvalidOption.__name__ + ' failed')
            if (encldiag.verifyEncldiagInvalidParameters(c)):
                FailCasesList.append('The case ' + encldiag.verifyEncldiagInvalidParameters.__name__ + ' failed')
            if (encldiag.verifyEncldiagMissingParameters(c)):
                FailCasesList.append('The case ' + encldiag.verifyEncldiagMissingParameters.__name__ + ' failed')

            tolog("Start verifying enclosure")
            import enclosure
            if (enclosure.verifyEnclosure(c)):
                FailCasesList.append('The case ' + enclosure.verifyEnclosure.__name__ + ' failed')
            if (enclosure.verifyEnclosureList(c)):
                FailCasesList.append('The case ' + enclosure.verifyEnclosureList.__name__ + ' failed')
            if (enclosure.verifyEnclosureMod(c)):
                FailCasesList.append('The case ' + enclosure.verifyEnclosureMod.__name__ + ' failed')
            if (enclosure.verifyEnclosureLocate(c)):
                FailCasesList.append('The case ' + enclosure.verifyEnclosureLocate.__name__ + ' failed')
            if (enclosure.verifyEnclosureHelp(c)):
                FailCasesList.append('The case ' + enclosure.verifyEnclosureHelp.__name__ + ' failed')
            if (enclosure.verifEnclosureSpecifyInexistentId(c)):
                FailCasesList.append('The case ' + enclosure.verifEnclosureSpecifyInexistentId.__name__ + ' failed')
            if (enclosure.verifyEnclosureInvalidOption(c)):
                FailCasesList.append('The case ' + enclosure.verifyEnclosureInvalidOption.__name__ + ' failed')
            if (enclosure.verifyEnclosureInvalidParameters(c)):
                FailCasesList.append('The case ' + enclosure.verifyEnclosureInvalidParameters.__name__ + ' failed')
            if (enclosure.verifyEnclosureMissingParameters(c)):
                FailCasesList.append('The case ' + enclosure.verifyEnclosureMissingParameters.__name__ + ' failed')

            tolog("Start verifying event")
            import event
            if (event.verifyEvent(c)):
                FailCasesList.append('The case ' + event.verifyEvent.__name__ + ' failed')
            if (event.verifyEventList(c)):
                FailCasesList.append('The case ' + event.verifyEventList.__name__ + ' failed')
            if (event.verifyEventClear(c)):
                FailCasesList.append('The case ' + event.verifyEventClear.__name__ + ' failed')
            if (event.verifyEventHelp(c)):
                FailCasesList.append('The case ' + event.verifyEventHelp.__name__ + ' failed')
            if (event.verifEventSpecifyInexistentId(c)):
                FailCasesList.append('The case ' + event.verifEventSpecifyInexistentId.__name__ + ' failed')
            if (event.verifyEventInvalidOption(c)):
                FailCasesList.append('The case ' + event.verifyEventInvalidOption.__name__ + ' failed')
            if (event.verifyEventInvalidParameters(c)):
                FailCasesList.append('The case ' + event.verifyEventInvalidParameters.__name__ + ' failed')
            if (event.verifyEventMissingParameters(c)):
                FailCasesList.append('The case ' + event.verifyEventMissingParameters.__name__ + ' failed')

            tolog("Start verifying factorydefaults")
            import factorydefaults
            if (factorydefaults.factorydefaultsBga(c)):
                FailCasesList.append('The case ' + factorydefaults.factorydefaultsBga.__name__ + ' failed')
            if (factorydefaults.factorydefaultsCtrl(c)):
                FailCasesList.append('The case ' + factorydefaults.factorydefaultsCtrl.__name__ + ' failed')
            if (factorydefaults.factorydefaultsEncl(c)):
                FailCasesList.append('The case ' + factorydefaults.factorydefaultsEncl.__name__ + ' failed')
            if (factorydefaults.factorydefaultsFc(c)):
                FailCasesList.append('The case ' + factorydefaults.factorydefaultsFc.__name__ + ' failed')
            if (factorydefaults.factorydefaultsIscsi(c)):
                FailCasesList.append('The case ' + factorydefaults.factorydefaultsIscsi.__name__ + ' failed')
            if (factorydefaults.factorydefaultsPhydrv(c)):
                FailCasesList.append('The case ' + factorydefaults.factorydefaultsPhydrv.__name__ + ' failed')
            if (factorydefaults.factorydefaultsSubsys(c)):
                FailCasesList.append('The case ' + factorydefaults.factorydefaultsSubsys.__name__ + ' failed')
            if (factorydefaults.factorydefaultsBgasched(c)):
                FailCasesList.append('The case ' + factorydefaults.factorydefaultsBgasched.__name__ + ' failed')
            if (factorydefaults.factorydefaultsService(c)):
                FailCasesList.append('The case ' + factorydefaults.factorydefaultsService.__name__ + ' failed')
            if (factorydefaults.factorydefaultsWebserver(c)):
                FailCasesList.append('The case ' + factorydefaults.factorydefaultsWebserver.__name__ + ' failed')
            if (factorydefaults.factorydefaultsSnmp(c)):
                FailCasesList.append('The case ' + factorydefaults.factorydefaultsSnmp.__name__ + ' failed')
            if (factorydefaults.factorydefaultsEmail(c)):
                FailCasesList.append('The case ' + factorydefaults.factorydefaultsEmail.__name__ + ' failed')
            if (factorydefaults.factorydefaultsNtp(c)):
                FailCasesList.append('The case ' + factorydefaults.factorydefaultsNtp.__name__ + ' failed')
            if (factorydefaults.factorydefaultsUser(c)):
                FailCasesList.append('The case ' + factorydefaults.factorydefaultsUser.__name__ + ' failed')
            if (factorydefaults.factorydefaultsUps(c)):
                FailCasesList.append('The case ' + factorydefaults.factorydefaultsUps.__name__ + ' failed')
            if (factorydefaults.factorydefaultsSyslog(c)):
                FailCasesList.append('The case ' + factorydefaults.factorydefaultsSyslog.__name__ + ' failed')
            if (factorydefaults.verifyFactorydefaultsHelp(c)):
                FailCasesList.append('The case ' + factorydefaults.verifyFactorydefaultsHelp.__name__ + ' failed')
            if (factorydefaults.verifyFactorydefaultsInvalidOption(c)):
                FailCasesList.append(
                    'The case ' + factorydefaults.verifyFactorydefaultsInvalidOption.__name__ + ' failed')
            if (factorydefaults.verifyFactorydefaultsInvalidParameters(c)):
                FailCasesList.append(
                    'The case ' + factorydefaults.verifyFactorydefaultsInvalidParameters.__name__ + ' failed')
            if (factorydefaults.verifyFactorydefaultsMissingParameters(c)):
                FailCasesList.append(
                    'The case ' + factorydefaults.verifyFactorydefaultsMissingParameters.__name__ + ' failed')

            tolog("Start verifying fc")
            import fc
            if (fc.verifyFc(c)):
                FailCasesList.append('The case ' + fc.verifyFc.__name__ + ' failed')
            if (fc.verifyFcList(c)):
                FailCasesList.append('The case ' + fc.verifyFcList.__name__ + ' failed')
            if (fc.verifyFcListV(c)):
                FailCasesList.append('The case ' + fc.verifyFcListV.__name__ + ' failed')
            if (fc.verifyFcMod(c)):
                FailCasesList.append('The case ' + fc.verifyFcMod.__name__ + ' failed')
            if (fc.verifyFcReset(c)):
                FailCasesList.append('The case ' + fc.verifyFcReset.__name__ + ' failed')
            if (fc.verifyFcClear(c)):
                FailCasesList.append('The case ' + fc.verifyFcClear.__name__ + ' failed')
            if (fc.verifyFcInvalidOption(c)):
                FailCasesList.append('The case ' + fc.verifyFcInvalidOption.__name__ + ' failed')
            if (fc.verifyFcInvalidParameters(c)):
                FailCasesList.append('The case ' + fc.verifyFcInvalidParameters.__name__ + ' failed')
            if (fc.verifyFcMissingParameters(c)):
                FailCasesList.append('The case ' + fc.verifyFcMissingParameters.__name__ + ' failed')

            tolog("Start verifying help")
            import help
            if (help.verifyHelp(c)):
                FailCasesList.append('The case ' + help.verifyHelp.__name__ + ' failed')

            tolog("Start verifying initiator")
            import initiator
            if (initiator.verifyInitiatorAdd(c)):
                FailCasesList.append('The case ' + initiator.verifyInitiatorAdd.__name__ + ' failed')
            if (initiator.verifyInitiator(c)):
                FailCasesList.append('The case ' + initiator.verifyInitiator.__name__ + ' failed')
            if (initiator.verifyInitiatorList(c)):
                FailCasesList.append('The case ' + initiator.verifyInitiatorList.__name__ + ' failed')
            if (initiator.verifyInitiatorDel(c)):
                FailCasesList.append('The case ' + initiator.verifyInitiatorDel.__name__ + ' failed')
            if (initiator.verifyInitiatorSpecifyInexistentId(c)):
                FailCasesList.append('The case ' + initiator.verifyInitiatorSpecifyInexistentId.__name__ + ' failed')
            if (initiator.verifyInitiatorInvalidOption(c)):
                FailCasesList.append('The case ' + initiator.verifyInitiatorInvalidOption.__name__ + ' failed')
            if (initiator.verifyInitiatorInvalidParameters(c)):
                FailCasesList.append('The case ' + initiator.verifyInitiatorInvalidParameters.__name__ + ' failed')
            if (initiator.verifyInitiatorMissingParameters(c)):
                FailCasesList.append('The case ' + initiator.verifyInitiatorMissingParameters.__name__ + ' failed')

            tolog("Start verifying iscsi")
            import iscsi
            if (iscsi.verifyIscsi(c)):
                FailCasesList.append('The case ' + iscsi.verifyIscsi.__name__ + ' failed')
            if (iscsi.verifyIscsiList(c)):
                FailCasesList.append('The case ' + iscsi.verifyIscsiList.__name__ + ' failed')
            if (iscsi.verifyIscsiAdd(c)):
                FailCasesList.append('The case ' + iscsi.verifyIscsiAdd.__name__ + ' failed')
            if (iscsi.verifyIscsiMod(c)):
                FailCasesList.append('The case ' + iscsi.verifyIscsiMod.__name__ + ' failed')
            if (iscsi.verifyIscsiDel(c)):
                FailCasesList.append('The case ' + iscsi.verifyIscsiDel.__name__ + ' failed')
            if (iscsi.verifyIscsiSpecifyInexistentId(c)):
                FailCasesList.append('The case ' + iscsi.verifyIscsiSpecifyInexistentId.__name__ + ' failed')
            if (iscsi.verifyIscsiInvalidOption(c)):
                FailCasesList.append('The case ' + iscsi.verifyIscsiInvalidOption.__name__ + ' failed')
            if (iscsi.verifyIscsiInvalidParameters(c)):
                FailCasesList.append('The case ' + iscsi.verifyIscsiInvalidParameters.__name__ + ' failed')
            if (iscsi.verifyIscsiMissingParameters(c)):
                FailCasesList.append('The case ' + iscsi.verifyIscsiMissingParameters.__name__ + ' failed')

            tolog("Start verifying isns")
            import isns
            if (isns.verifyIsns(c)):
                FailCasesList.append('The case ' + isns.verifyIsns.__name__ + ' failed')
            if (isns.verifyIsnsList(c)):
                FailCasesList.append('The case ' + isns.verifyIsnsList.__name__ + ' failed')
            if (isns.verifyIsnsMod(c)):
                FailCasesList.append('The case ' + isns.verifyIsnsMod.__name__ + ' failed')
            if (isns.verifyIsnsSpecifyInexistentId(c)):
                FailCasesList.append('The case ' + isns.verifyIsnsSpecifyInexistentId.__name__ + ' failed')
            if (isns.verifyIsnsInvalidOption(c)):
                FailCasesList.append('The case ' + isns.verifyIsnsInvalidOption.__name__ + ' failed')
            if (isns.verifyIsnsInvalidParameters(c)):
                FailCasesList.append('The case ' + isns.verifyIsnsInvalidParameters.__name__ + ' failed')
            if (isns.verifyIsnsMissingParameters(c)):
                FailCasesList.append('The case ' + isns.verifyIsnsMissingParameters.__name__ + ' failed')

            tolog("Start verifying lunmap")
            import lunmap
            if (lunmap.verifyLunmapAdd(c)):
                FailCasesList.append('The case ' + lunmap.verifyLunmapAdd.__name__ + ' failed')
            if (lunmap.verifyLunmap(c)):
                FailCasesList.append('The case ' + lunmap.verifyLunmap.__name__ + ' failed')
            if (lunmap.verifyLunmapList(c)):
                FailCasesList.append('The case ' + lunmap.verifyLunmapList.__name__ + ' failed')
            if (lunmap.verifyLunmapAddlun(c)):
                FailCasesList.append('The case ' + lunmap.verifyLunmapAddlun.__name__ + ' failed')
            if (lunmap.verifyLunmapDellun(c)):
                FailCasesList.append('The case ' + lunmap.verifyLunmapDellun.__name__ + ' failed')
            if (lunmap.verifyLunmapEnable(c)):
                FailCasesList.append('The case ' + lunmap.verifyLunmapEnable.__name__ + ' failed')
            if (lunmap.verifyLunmapDel(c)):
                FailCasesList.append('The case ' + lunmap.verifyLunmapDel.__name__ + ' failed')
            if (lunmap.verifyLunmapDisable(c)):
                FailCasesList.append('The case ' + lunmap.verifyLunmapDisable.__name__ + ' failed')
            if (lunmap.verifyLunmapSpecifyInexistentId(c)):
                FailCasesList.append('The case ' + lunmap.verifyLunmapSpecifyInexistentId.__name__ + ' failed')
            if (lunmap.verifyLunmapInvalidOption(c)):
                FailCasesList.append('The case ' + lunmap.verifyLunmapInvalidOption.__name__ + ' failed')
            if (lunmap.verifyLunmapInvalidParameters(c)):
                FailCasesList.append('The case ' + lunmap.verifyLunmapInvalidParameters.__name__ + ' failed')
            if (lunmap.verifyLunmapMissingParameters(c)):
                FailCasesList.append('The case ' + lunmap.verifyLunmapMissingParameters.__name__ + ' failed')
            lunmap.cleanUp(c)

            tolog("Start verifying ntp")
            import ntp
            if (ntp.verifyNtpMod(c)):
                FailCasesList.append('The case ' + ntp.verifyNtpMod.__name__ + ' failed')
            if (ntp.verifyNtp(c)):
                FailCasesList.append('The case ' + ntp.verifyNtp.__name__ + ' failed')
            if (ntp.verifyNtpList(c)):
                FailCasesList.append('The case ' + ntp.verifyNtpList.__name__ + ' failed')
            if (ntp.verifyNtpTest(c)):
                FailCasesList.append('The case ' + ntp.verifyNtpTest.__name__ + ' failed')
            if (ntp.verifyNtpSync(c)):
                FailCasesList.append('The case ' + ntp.verifyNtpSync.__name__ + ' failed')
            if (ntp.verifyNtpInvalidOption(c)):
                FailCasesList.append('The case ' + ntp.verifyNtpInvalidOption.__name__ + ' failed')
            if (ntp.verifyNtpInvalidParameters(c)):
                FailCasesList.append('The case ' + ntp.verifyNtpInvalidParameters.__name__ + ' failed')
            if (ntp.verifyNtpMissingParameters(c)):
                FailCasesList.append('The case ' + ntp.verifyNtpMissingParameters.__name__ + ' failed')

            tolog("Start verifying password")
            import password
            if (password.verifyChangePassword(c)):
                FailCasesList.append('The case ' + password.verifyChangePassword.__name__ + ' failed')
            if (password.verifyPasswordSpecifyInexistentUsername(c)):
                FailCasesList.append(
                    'The case ' + password.verifyPasswordSpecifyInexistentUsername.__name__ + ' failed')
            if (password.verifyPasswordInvalidOption(c)):
                FailCasesList.append('The case ' + password.verifyPasswordInvalidOption.__name__ + ' failed')
            if (password.verifyPasswordInvalidParameters(c)):
                FailCasesList.append('The case ' + password.verifyPasswordInvalidParameters.__name__ + ' failed')
            if (password.verifyPasswordMissingParameters(c)):
                FailCasesList.append('The case ' + password.verifyPasswordMissingParameters.__name__ + ' failed')

            tolog("Start verifying pcie")
            import pcie
            if (pcie.verifyPcie(c)):
                FailCasesList.append('The case ' + pcie.verifyPcie.__name__ + ' failed')
            if (pcie.verifyPcielist(c)):
                FailCasesList.append('The case ' + pcie.verifyPcielist.__name__ + ' failed')
            if (pcie.verifyPcieInvalidOption(c)):
                FailCasesList.append('The case ' + pcie.verifyPcieInvalidOption.__name__ + ' failed')
            if (pcie.verifyPcieInvalidParameters(c)):
                FailCasesList.append('The case ' + pcie.verifyPcieInvalidParameters.__name__ + ' failed')
            if (pcie.verifyPcieMissingParameters(c)):
                FailCasesList.append('The case ' + pcie.verifyPcieMissingParameters.__name__ + ' failed')

            tolog("Start verifying smart")
            import smart
            if (smart.verifySmart(c)):
                FailCasesList.append('The case ' + smart.verifySmart.__name__ + ' failed')
            if (smart.verifySmartV(c)):
                FailCasesList.append('The case ' + smart.verifySmartV.__name__ + ' failed')
            if (smart.verifySmartList(c)):
                FailCasesList.append('The case ' + smart.verifySmartList.__name__ + ' failed')
            if (smart.verifySmartEnable(c)):
                FailCasesList.append('The case ' + smart.verifySmartEnable.__name__ + ' failed')
            if (smart.verifySmartDisable(c)):
                FailCasesList.append('The case ' + smart.verifySmartDisable.__name__ + ' failed')
            if (smart.verifySmartHelp(c)):
                FailCasesList.append('The case ' + smart.verifySmartHelp.__name__ + ' failed')
            if (smart.verifySmartSpecifyInexistentId(c)):
                FailCasesList.append('The case ' + smart.verifySmartSpecifyInexistentId.__name__ + ' failed')
            if (smart.verifySmartInvalidOption(c)):
                FailCasesList.append('The case ' + smart.verifySmartInvalidOption.__name__ + ' failed')
            if (smart.verifySmartInvalidParameters(c)):
                FailCasesList.append('The case ' + smart.verifySmartInvalidParameters.__name__ + ' failed')
            if (smart.verifySmartMissingParameters(c)):
                FailCasesList.append('The case ' + smart.verifySmartMissingParameters.__name__ + ' failed')

            tolog('Start verifying bgasched')
            import bgasched
            if (bgasched.verifyBgaschedAdd(c)):
                FailCasesList.append('The case ' + bgasched.verifyBgaschedAdd.__name__ + ' failed')
            if (bgasched.verifyBgaschedMod(c)):
                FailCasesList.append('The case ' + bgasched.verifyBgaschedMod.__name__ + ' failed')
            if (bgasched.verifyBgaschedList(c)):
                FailCasesList.append('The case ' + bgasched.verifyBgaschedList.__name__ + ' failed')
            if (bgasched.verifyBgaschedDel(c)):
                FailCasesList.append('The case ' + bgasched.verifyBgaschedDel.__name__ + ' failed')
            if (bgasched.verifyBgaschedHelp(c)):
                FailCasesList.append('The case ' + bgasched.verifyBgaschedHelp.__name__ + ' failed')
            if (bgasched.verifyBgaschedInvalidOption(c)):
                FailCasesList.append('The case ' + bgasched.verifyBgaschedInvalidOption.__name__ + ' failed')
            if (bgasched.verifyBgaschedInvalidParameters(c)):
                FailCasesList.append('The case ' + bgasched.verifyBgaschedInvalidParameters.__name__ + ' failed')
            if (bgasched.verifyBgaschedMissingParameters(c)):
                FailCasesList.append('The case ' + bgasched.verifyBgaschedMissingParameters.__name__ + ' failed')
            bgasched.clearUp(c)

            tolog('Start verifying rb')
            import rb
            if (rb.verifyRbStartAndStopAndList(c)):
                FailCasesList.append('The case ' + rb.verifyRbStartAndStopAndList.__name__ + ' failed')
            if (rb.verifyRbInvalidOption(c)):
                FailCasesList.append('The case ' + rb.verifyRbInvalidOption.__name__ + ' failed')
            if (rb.verifyRbInvalidParameters(c)):
                FailCasesList.append('The case ' + rb.verifyRbInvalidParameters.__name__ + ' failed')
            if (rb.verifyRbMissingParameters(c)):
                FailCasesList.append('The case ' + rb.verifyRbMissingParameters.__name__ + ' failed')

            tolog('Start verifying NASShare')
            import nasShare
            if (nasShare.addNASShare(c)):
                FailCasesList.append('The case ' + nasShare.addNASShare.__name__ + ' failed')
            if (nasShare.listNASShare(c)):
                FailCasesList.append('The case ' + nasShare.listNASShare.__name__ + ' failed')
            if (nasShare.listVerboseNASShare(c)):
                FailCasesList.append('The case ' + nasShare.listVerboseNASShare.__name__ + ' failed')
            if (nasShare.modNASShare(c)):
                FailCasesList.append('The case ' + nasShare.modNASShare.__name__ + ' failed')
            if (nasShare.mountNASShare(c)):
                FailCasesList.append('The case ' + nasShare.mountNASShare.__name__ + ' failed')
            if (nasShare.unmountNASShare(c)):
                FailCasesList.append('The case ' + nasShare.unmountNASShare.__name__ + ' failed')
            if (nasShare.helpNASShare(c)):
                FailCasesList.append('The case ' + nasShare.helpNASShare.__name__ + ' failed')
            if (nasShare.failedTest_InexistentId(c)):
                FailCasesList.append('The case ' + nasShare.failedTest_InexistentId.__name__ + ' failed')
            if (nasShare.failedTest_InvalidOption(c)):
                FailCasesList.append('The case ' + nasShare.failedTest_InvalidOption.__name__ + ' failed')
            if (nasShare.failedTest_InvalidParameters(c)):
                FailCasesList.append('The case ' + nasShare.failedTest_InvalidParameters.__name__ + ' failed')
            if (nasShare.failedTest_MissingParameters(c)):
                FailCasesList.append('The case ' + nasShare.failedTest_MissingParameters.__name__ + ' failed')
            if (nasShare.deleteNASShare(c)):
                FailCasesList.append('The case ' + nasShare.deleteNASShare.__name__ + ' failed')

        else:
            tolog("Failed to connect server after ptiflash.")

        if len(FailCasesList) != 0:
            Failflag = True
            for f in FailCasesList:
                tolog(f)

        if Failflag:
            tolog(Fail)
        else:
            tolog(Pass)
    else:
        tolog("no new build is availlable.")
        tolog(Pass)

    c.close()

if __name__ == "__main__":
    start = time.clock()
    c,ssh = ssh_conn()
    BuildVerification(c)
    c.close()
