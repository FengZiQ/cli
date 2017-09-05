# initial version
# March 16, 2017
# architecture
# 1. getnewbuild from buildserver
# 2. scp to tftpserver
# 3. login to hypersion-DS console, execute
#    ptiflash -t -s 10.84.2.99 -f d5k-multi-12_0_9999_xx.ptif
#    ptiflash -t -s 10.84.2.99 -f d5k-conf-12_0_9999_48.ptif
# 4. execute auto script for cli and webgui
# 5. send email according to the test result
from time import sleep
import os
from send_cmd import *
from ssh_connect import *
from to_log import *

Pass = "'result': 'p'"
Fail = "'result': 'f'"

def BuildVerification(c):
    Failflag = False
    FailCasesList = []

    # To check whether the sw is compiled successfully
    size = os.path.getsize('/var/lib/jenkins/workspace/Hyperion-DS_Hulda/sw.log')
    # size = os.path.getsize('/var/lib/jenkins/workspace/HyperionDS/sw.log')
    if size < 6000000:
        tolog('sw compiles failure')
        exit(1)

    c, ssh = ssh_conn()

    import glob

    # files = glob.glob("/var/lib/jenkins/workspace/HyperionDS/build/build/*.ptif")
    files = glob.glob("/var/lib/jenkins/workspace/Hyperion-DS_Hulda/build/build/*.ptif")

    reconnectflag = True
    for file in files:
        filename = file.replace("/var/lib/jenkins/workspace/Hyperion-DS_Hulda/build/build/","")
        # filename = file.replace("/var/lib/jenkins/workspace/HyperionDS/build/build/", "")
        SendCmdRestart(c,"ptiflash -y -t -s 10.84.2.66 -f "+filename)
        i = 1
        while i < 50:
            # wait for rebooting
           tolog("ptiflash is in progress, please wait, %d seconds elapse" %(i*4))
           i += 1
           sleep(4)

        # check if ssh connection is ok.
        # wait for another 120 seconds
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
            FailCasesList.append('The case ' + pool.bvtpoolcreateverifyoutputerror_newraidlevel.__name__ + ' failed')

        tolog("Start verifying about")
        import about
        if (about.bvt_verifyAbout(c)):
            FailCasesList.append('The case ' + about.bvt_verifyAbout.__name__ + ' failed')
        if (about.bvt_verifyAboutHelp(c)):
            FailCasesList.append('The case ' + about.bvt_verifyAboutHelp.__name__ + ' failed')
        if (about.bvt_verifyAboutInvalidOption(c)):
            FailCasesList.append('The case ' + about.bvt_verifyAboutInvalidOption.__name__ + ' failed')
        if (about.bvt_verifyAboutInvalidParameters(c)):
            FailCasesList.append('The case ' + about.bvt_verifyAboutInvalidParameters.__name__ + ' failed')

        tolog("Start verifying battery")
        import battery
        if (battery.bvt_verifyBattery(c)):
            FailCasesList.append('The case ' + battery.bvt_verifyBattery.__name__ + ' failed')
        if (battery.bvt_verifyBatteryList(c)):
            FailCasesList.append('The case ' + battery.bvt_verifyBatteryList.__name__ + ' failed')
        if (battery.bvt_verifyBatteryRecondition(c)):
            FailCasesList.append('The case ' + battery.bvt_verifyBatteryRecondition.__name__ + ' failed')
        if (battery.bvt_verifyBatteryHelp(c)):
            FailCasesList.append('The case ' + battery.bvt_verifyBatteryHelp.__name__ + ' failed')
        if (battery.bvt_verifyBatterySpecifyInexistentId(c)):
            FailCasesList.append('The case ' + battery.bvt_verifyBatterySpecifyInexistentId.__name__ + ' failed')
        if (battery.bvt_verifyBatteryInvalidOption(c)):
            FailCasesList.append('The case ' + battery.bvt_verifyBatteryInvalidOption.__name__ + ' failed')
        if (battery.bvt_verifyBatteryInvalidParameters(c)):
            FailCasesList.append('The case ' + battery.bvt_verifyBatteryInvalidParameters.__name__ + ' failed')
        if (battery.bvt_verifyBatteryMissingParameters(c)):
            FailCasesList.append('The case ' + battery.bvt_verifyBatteryMissingParameters.__name__ + ' failed')

        tolog("Start verifying BBM")
        import bbm
        if (bbm.bvt_verifyBBM(c)):
            FailCasesList.append('The case ' + bbm.bvt_verifyBBM.__name__ + ' failed')
        if (bbm.bvt_verifyBBMClear(c)):
            FailCasesList.append('The case ' + bbm.bvt_verifyBBMClear.__name__ + ' failed')
        if (bbm.bvt_verifyBBMHelp(c)):
            FailCasesList.append('The case ' + bbm.bvt_verifyBBMHelp.__name__ + ' failed')
        if (bbm.bvt_verifyBBMInvalidOption(c)):
            FailCasesList.append('The case ' + bbm.bvt_verifyBBMInvalidOption.__name__ + ' failed')
        if (bbm.bvt_verifyBBMInvalidParameters(c)):
            FailCasesList.append('The case ' + bbm.bvt_verifyBBMInvalidParameters.__name__ + ' failed')
        if (bbm.bvt_verifyBBMList(c)):
            FailCasesList.append('The case ' + bbm.bvt_verifyBBMList.__name__ + ' failed')
        if (bbm.bvt_verifyBBMMissingParameters(c)):
            FailCasesList.append('The case ' + bbm.bvt_verifyBBMMissingParameters.__name__ + ' failed')
        if (bbm.bvt_verifyBBMSpecifyInexistentId(c)):
            FailCasesList.append('The case ' + bbm.bvt_verifyBBMSpecifyInexistentId.__name__ + ' failed')
        (bbm.cleanUp(c))

        tolog("Start verifying bga")
        import bga
        if (bga.bvt_verifyBga(c)):
            FailCasesList.append('The case ' + bga.bvt_verifyBga.__name__ + ' failed')
        if (bga.bvt_verifyBgaList(c)):
            FailCasesList.append('The case ' + bga.bvt_verifyBgaList.__name__ + ' failed')
        if (bga.bvt_verifyBgaMod(c)):
            FailCasesList.append('The case ' + bga.bvt_verifyBgaMod.__name__ + ' failed')
        if (bga.bvt_verifyBgaHelp(c)):
            FailCasesList.append('The case ' + bga.bvt_verifyBgaHelp.__name__ + ' failed')
        if (bga.bvt_verifyBgaInvalidOption(c)):
            FailCasesList.append('The case ' + bga.bvt_verifyBgaInvalidOption.__name__ + ' failed')
        if (bga.bvt_verifyBgaInvalidParameters(c)):
            FailCasesList.append('The case ' + bga.bvt_verifyBgaInvalidParameters.__name__ + ' failed')
        if (bga.bvt_verifyBgaMissingParameters(c)):
            FailCasesList.append('The case ' + bga.bvt_verifyBgaMissingParameters.__name__ + ' failed')

        tolog("Start verifying buzzer")
        import buzzer
        if (buzzer.bvt_verifyBuzzerDisableAndSilentTurnOn((c))):
            FailCasesList.append('The case ' + buzzer.bvt_verifyBuzzerDisableAndSilentTurnOn.__name__ + ' failed')
        if (buzzer.bvt_verifyBuzzerEnableAndSilentTurnOn((c))):
            FailCasesList.append('The case ' + buzzer.bvt_verifyBuzzerEnableAndSilentTurnOn.__name__ + ' failed')
        if (buzzer.bvt_verifyBuzzerEnableAndSoundingTurnOn((c))):
            FailCasesList.append('The case ' + buzzer.bvt_verifyBuzzerEnableAndSoundingTurnOn.__name__ + ' failed')
        if (buzzer.bvt_verifyBuzzerDisableAndSilentTurnOff((c))):
            FailCasesList.append('The case ' + buzzer.bvt_verifyBuzzerDisableAndSilentTurnOff.__name__ + ' failed')
        if (buzzer.bvt_verifyBuzzerEnableAndSilentTurnOff((c))):
            FailCasesList.append('The case ' + buzzer.bvt_verifyBuzzerEnableAndSilentTurnOff.__name__ + ' failed')
        if (buzzer.bvt_verifyBuzzerEnableAndSoundingTurnOff((c))):
            FailCasesList.append('The case ' + buzzer.bvt_verifyBuzzerEnableAndSoundingTurnOff.__name__ + ' failed')
        if (buzzer.bvt_verifyBuzzerDisableAndSilentEnable((c))):
            FailCasesList.append('The case ' + buzzer.bvt_verifyBuzzerDisableAndSilentEnable.__name__ + ' failed')
        if (buzzer.bvt_verifyBuzzerEnableAndSilentEnable((c))):
            FailCasesList.append('The case ' + buzzer.bvt_verifyBuzzerEnableAndSilentEnable.__name__ + ' failed')
        if (buzzer.bvt_verifyBuzzerEnableAndSoundingEnable((c))):
            FailCasesList.append('The case ' + buzzer.bvt_verifyBuzzerEnableAndSoundingEnable.__name__ + ' failed')
        if (buzzer.bvt_verifyBuzzerEnableAndSoundingDisable((c))):
            FailCasesList.append('The case ' + buzzer.bvt_verifyBuzzerEnableAndSoundingDisable.__name__ + ' failed')
        if (buzzer.bvt_verifyBuzzerEnableAndSilentDisable((c))):
            FailCasesList.append('The case ' + buzzer.bvt_verifyBuzzerEnableAndSilentDisable.__name__ + ' failed')
        if (buzzer.bvt_verifyBuzzerDisableAndSilentDisable((c))):
            FailCasesList.append('The case ' + buzzer.bvt_verifyBuzzerDisableAndSilentDisable.__name__ + ' failed')
        if (buzzer.bvt_verifyBuzzerInfo((c))):
            FailCasesList.append('The case ' + buzzer.bvt_verifyBuzzerInfo.__name__ + ' failed')
        if (buzzer.bvt_verifyBuzzerHelp((c))):
            FailCasesList.append('The case ' + buzzer.bvt_verifyBuzzerHelp.__name__ + ' failed')
        if (buzzer.bvt_verifyBuzzerInvalidParameters((c))):
            FailCasesList.append('The case ' + buzzer.bvt_verifyBuzzerInvalidParameters.__name__ + ' failed')
        if (buzzer.bvt_verifyBuzzerInvalidOption((c))):
            FailCasesList.append('The case ' + buzzer.bvt_verifyBuzzerInvalidOption.__name__ + ' failed')

        #tolog("Start verifying chap")
        #import chap
        #(chap.bvt_verifyChapAdd(c))
        #(chap.bvt_verifyChap(c))
        #(chap.bvt_verifyChapList(c))
        #(chap.bvt_verifyChapMod(c))
        #(chap.bvt_verifyChapDel(c))
        #(chap.bvt_verifyChapHelp(c))
        #(chap.bvt_verifyChapSpecifyErrorId(c))
        #(chap.bvt_verifyChapInvalidOption(c))
        #(chap.bvt_verifyChapInvalidParameters(c))
        #(chap.bvt_verifyChapMissingParameters(c))

        import ctrl
        tolog("Start verifying ctrl")
        if (ctrl.bvt_verifyCtrl(c)):
            FailCasesList.append('The case ' + ctrl.bvt_verifyCtrl.__name__ + ' failed')
        if (ctrl.bvt_verifyCtrlSpecifyId(c)):
            FailCasesList.append('The case ' + ctrl.bvt_verifyCtrlSpecifyId.__name__ + ' failed')
        if (ctrl.bvt_verifyCtrlSpecifyInexistentId(c)):
            FailCasesList.append('The case ' + ctrl.bvt_verifyCtrlSpecifyInexistentId.__name__ + ' failed')
        if (ctrl.bvt_verifyCtrlList(c)):
            FailCasesList.append('The case ' + ctrl.bvt_verifyCtrlList.__name__ + ' failed')
        if (ctrl.bvt_verifyCtrlV(c)):
            FailCasesList.append('The case ' + ctrl.bvt_verifyCtrlV.__name__ + ' failed')
        if (ctrl.bvt_verifyCtrlListV(c)):
            FailCasesList.append('The case ' + ctrl.bvt_verifyCtrlListV.__name__ + ' failed')
        if (ctrl.bvt_verifyCtrlModNormativeAlias(c)):
            FailCasesList.append('The case ' + ctrl.bvt_verifyCtrlModNormativeAlias.__name__ + ' failed')
        if (ctrl.bvt_verifyCtrlModValuesIsEnableOrDisable(c)):
            FailCasesList.append('The case ' + ctrl.bvt_verifyCtrlModValuesIsEnableOrDisable.__name__ + ' failed')
        if (ctrl.bvt_verifyCtrlModValuesIsTime(c)):
            FailCasesList.append('The case ' + ctrl.bvt_verifyCtrlModValuesIsTime.__name__ + ' failed')
        if (ctrl.bvt_verifyCtrlClear(c)):
            FailCasesList.append('The case ' + ctrl.bvt_verifyCtrlClear.__name__ + ' failed')
        if (ctrl.bvt_verifyCtrlHelp(c)):
            FailCasesList.append('The case ' + ctrl.bvt_verifyCtrlHelp.__name__ + ' failed')
        if (ctrl.bvt_verifyCtrlInvalidOption(c)):
            FailCasesList.append('The case ' + ctrl.bvt_verifyCtrlInvalidOption.__name__ + ' failed')
        if (ctrl.bvt_verifyCtrlInvalidParameters(c)):
            FailCasesList.append('The case ' + ctrl.bvt_verifyCtrlInvalidParameters.__name__ + ' failed')
        if (ctrl.bvt_verifyCtrlMissingParameters(c)):
            FailCasesList.append('The case ' + ctrl.bvt_verifyCtrlMissingParameters.__name__ + ' failed')
        if (ctrl.bvt_verifyCtrlSpecifyInexistentId(c)):
            FailCasesList.append('The case ' + ctrl.bvt_verifyCtrlSpecifyInexistentId.__name__ + ' failed')


        tolog("Start verifying encldiag")
        import encldiag
        if (encldiag.bvt_verifyEncldiag(c)):
            FailCasesList.append('The case ' + encldiag.bvt_verifyEncldiag.__name__ + ' failed')
        if (encldiag.bvt_verifyEncldiagList(c)):
            FailCasesList.append('The case ' + encldiag.bvt_verifyEncldiagList.__name__ + ' failed')
        if (encldiag.bvt_verifyEncldiagHelp(c)):
            FailCasesList.append('The case ' + encldiag.bvt_verifyEncldiagHelp.__name__ + ' failed')
        if (encldiag.bvt_verifyEncldiagSpecifyInexistentId(c)):
            FailCasesList.append('The case ' + encldiag.bvt_verifyEncldiagSpecifyInexistentId.__name__ + ' failed')
        if (encldiag.bvt_verifyEncldiagInvalidOption(c)):
            FailCasesList.append('The case ' + encldiag.bvt_verifyEncldiagInvalidOption.__name__ + ' failed')
        if (encldiag.bvt_verifyEncldiagInvalidParameters(c)):
            FailCasesList.append('The case ' + encldiag.bvt_verifyEncldiagInvalidParameters.__name__ + ' failed')
        if (encldiag.bvt_verifyEncldiagMissingParameters(c)):
            FailCasesList.append('The case ' + encldiag.bvt_verifyEncldiagMissingParameters.__name__ + ' failed')

        tolog("Start verifying enclosure")
        import enclosure
        if (enclosure.bvt_verifyEnclosure(c)):
            FailCasesList.append('The case ' + enclosure.bvt_verifyEnclosure.__name__ + ' failed')
        if (enclosure.bvt_verifyEnclosureList(c)):
            FailCasesList.append('The case ' + enclosure.bvt_verifyEnclosureList.__name__ + ' failed')
        if (enclosure.bvt_verifyEnclosureMod(c)):
            FailCasesList.append('The case ' + enclosure.bvt_verifyEnclosureMod.__name__ + ' failed')
        if (enclosure.bvt_verifyEnclosureLocate(c)):
            FailCasesList.append('The case ' + enclosure.bvt_verifyEnclosureLocate.__name__ + ' failed')
        if (enclosure.bvt_verifyEnclosureHelp(c)):
            FailCasesList.append('The case ' + enclosure.bvt_verifyEnclosureHelp.__name__ + ' failed')
        if (enclosure.bvt_verifEnclosureSpecifyInexistentId(c)):
            FailCasesList.append('The case ' + enclosure.bvt_verifEnclosureSpecifyInexistentId.__name__ + ' failed')
        if (enclosure.bvt_verifyEnclosureInvalidOption(c)):
            FailCasesList.append('The case ' + enclosure.bvt_verifyEnclosureInvalidOption.__name__ + ' failed')
        if (enclosure.bvt_verifyEnclosureInvalidParameters(c)):
            FailCasesList.append('The case ' + enclosure.bvt_verifyEnclosureInvalidParameters.__name__ + ' failed')
        if (enclosure.bvt_verifyEnclosureMissingParameters(c)):
            FailCasesList.append('The case ' + enclosure.bvt_verifyEnclosureMissingParameters.__name__ + ' failed')


        tolog("Start verifying event")
        import event
        if (event.bvt_verifyEvent(c)):
            FailCasesList.append('The case ' + event.bvt_verifyEvent.__name__ + ' failed')
        if (event.bvt_verifyEventList(c)):
            FailCasesList.append('The case ' + event.bvt_verifyEventList.__name__ + ' failed')
        if (event.bvt_verifyEventClear(c)):
            FailCasesList.append('The case ' + event.bvt_verifyEventClear.__name__ + ' failed')
        if (event.bvt_verifyEventHelp(c)):
            FailCasesList.append('The case ' + event.bvt_verifyEventHelp.__name__ + ' failed')
        if (event.bvt_verifEventSpecifyInexistentId(c)):
            FailCasesList.append('The case ' + event.bvt_verifEventSpecifyInexistentId.__name__ + ' failed')
        if (event.bvt_verifyEventInvalidOption(c)):
            FailCasesList.append('The case ' + event.bvt_verifyEventInvalidOption.__name__ + ' failed')
        if (event.bvt_verifyEventInvalidParameters(c)):
            FailCasesList.append('The case ' + event.bvt_verifyEventInvalidParameters.__name__ + ' failed')
        if (event.bvt_verifyEventMissingParameters(c)):
            FailCasesList.append('The case ' + event.bvt_verifyEventMissingParameters.__name__ + ' failed')
            

        tolog("Start verifying factorydefaults")
        import factorydefaults
        if (factorydefaults.bvt_factorydefaultsBga(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_factorydefaultsBga.__name__ + ' failed')
        if (factorydefaults.bvt_factorydefaultsCtrl(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_factorydefaultsCtrl.__name__ + ' failed')
        if (factorydefaults.bvt_factorydefaultsEncl(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_factorydefaultsEncl.__name__ + ' failed')
        if (factorydefaults.bvt_factorydefaultsFc(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_factorydefaultsFc.__name__ + ' failed')
        if (factorydefaults.bvt_factorydefaultsIscsi(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_factorydefaultsIscsi.__name__ + ' failed')
        if (factorydefaults.bvt_factorydefaultsPhydrv(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_factorydefaultsPhydrv.__name__ + ' failed')
        if (factorydefaults.bvt_factorydefaultsSubsys(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_factorydefaultsSubsys.__name__ + ' failed')
        if (factorydefaults.bvt_factorydefaultsBgasched(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_factorydefaultsBgasched.__name__ + ' failed')
        if (factorydefaults.bvt_factorydefaultsService(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_factorydefaultsService.__name__ + ' failed')
        if (factorydefaults.bvt_factorydefaultsWebserver(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_factorydefaultsWebserver.__name__ + ' failed')
        if (factorydefaults.bvt_factorydefaultsSnmp(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_factorydefaultsSnmp.__name__ + ' failed')
        #if (factorydefaults.bvt_factorydefaultsSsh(c)):
        if (factorydefaults.bvt_factorydefaultsEmail(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_factorydefaultsEmail.__name__ + ' failed')
        if (factorydefaults.bvt_factorydefaultsNtp(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_factorydefaultsNtp.__name__ + ' failed')
        if (factorydefaults.bvt_factorydefaultsUser(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_factorydefaultsUser.__name__ + ' failed')
        if (factorydefaults.bvt_factorydefaultsUps(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_factorydefaultsUps.__name__ + ' failed')
        if (factorydefaults.bvt_factorydefaultsSyslog(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_factorydefaultsSyslog.__name__ + ' failed')
        if (factorydefaults.bvt_verifyFactorydefaultsHelp(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_verifyFactorydefaultsHelp.__name__ + ' failed')
        if (factorydefaults.bvt_verifyFactorydefaultsInvalidOption(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_verifyFactorydefaultsInvalidOption.__name__ + ' failed')
        if (factorydefaults.bvt_verifyFactorydefaultsInvalidParameters(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_verifyFactorydefaultsInvalidParameters.__name__ + ' failed')
        if (factorydefaults.bvt_verifyFactorydefaultsMissingParameters(c)):
            FailCasesList.append('The case ' + factorydefaults.bvt_verifyFactorydefaultsMissingParameters.__name__ + ' failed')


        tolog("Start verifying fc")
        import fc
        if (fc.bvt_verifyFc(c)):
            FailCasesList.append('The case ' + fc.bvt_verifyFc.__name__ + ' failed')
        if (fc.bvt_verifyFcList(c)):
            FailCasesList.append('The case ' + fc.bvt_verifyFcList.__name__ + ' failed')
        if (fc.bvt_verifyFcListV(c)):
            FailCasesList.append('The case ' + fc.bvt_verifyFcListV.__name__ + ' failed')
        if (fc.bvt_verifyFcMod(c)):
            FailCasesList.append('The case ' + fc.bvt_verifyFcMod.__name__ + ' failed')
        if (fc.bvt_verifyFcReset(c)):
            FailCasesList.append('The case ' + fc.bvt_verifyFcReset.__name__ + ' failed')
        if (fc.bvt_verifyFcClear(c)):
            FailCasesList.append('The case ' + fc.bvt_verifyFcClear.__name__ + ' failed')
        if (fc.bvt_verifyFcInvalidOption(c)):
            FailCasesList.append('The case ' + fc.bvt_verifyFcInvalidOption.__name__ + ' failed')
        if (fc.bvt_verifyFcInvalidParameters(c)):
            FailCasesList.append('The case ' + fc.bvt_verifyFcInvalidParameters.__name__ + ' failed')
        if (fc.bvt_verifyFcMissingParameters(c)):
            FailCasesList.append('The case ' + fc.bvt_verifyFcMissingParameters.__name__ + ' failed')
            

        tolog("Start verifying help")
        import help
        if (help.bvt_verifyHelp(c)):
            FailCasesList.append('The case ' + help.bvt_verifyHelp.__name__ + ' failed')
            

        tolog("Start verifying initiator")
        import initiator
        if (initiator.bvt_verifyInitiatorAdd(c)):
            FailCasesList.append('The case ' + initiator.bvt_verifyInitiatorAdd.__name__ + ' failed')
        if (initiator.bvt_verifyInitiator(c)):
            FailCasesList.append('The case ' + initiator.bvt_verifyInitiator.__name__ + ' failed')
        if (initiator.bvt_verifyInitiatorList(c)):
            FailCasesList.append('The case ' + initiator.bvt_verifyInitiatorList.__name__ + ' failed')
        if (initiator.bvt_verifyInitiatorDel(c)):
            FailCasesList.append('The case ' + initiator.bvt_verifyInitiatorDel.__name__ + ' failed')
        if (initiator.bvt_verifyInitiatorSpecifyInexistentId(c)):
            FailCasesList.append('The case ' + initiator.bvt_verifyInitiatorSpecifyInexistentId.__name__ + ' failed')
        if (initiator.bvt_verifyInitiatorInvalidOption(c)):
            FailCasesList.append('The case ' + initiator.bvt_verifyInitiatorInvalidOption.__name__ + ' failed')
        if (initiator.bvt_verifyInitiatorInvalidParameters(c)):
            FailCasesList.append('The case ' + initiator.bvt_verifyInitiatorInvalidParameters.__name__ + ' failed')
        if (initiator.bvt_verifyInitiatorMissingParameters(c)):
            FailCasesList.append('The case ' + initiator.bvt_verifyInitiatorMissingParameters.__name__ + ' failed')


        tolog("Start verifying iscsi")
        import iscsi
        if (iscsi.bvt_verifyIscsi(c)):
            FailCasesList.append('The case ' + iscsi.bvt_verifyIscsi.__name__ + ' failed')
        if (iscsi.bvt_verifyIscsiList(c)):
            FailCasesList.append('The case ' + iscsi.bvt_verifyIscsiList.__name__ + ' failed')
        if (iscsi.bvt_verifyIscsiAdd(c)):
            FailCasesList.append('The case ' + iscsi.bvt_verifyIscsiAdd.__name__ + ' failed')
        if (iscsi.bvt_verifyIscsiMod(c)):
            FailCasesList.append('The case ' + iscsi.bvt_verifyIscsiMod.__name__ + ' failed')
        if (iscsi.bvt_verifyIscsiDel(c)):
            FailCasesList.append('The case ' + iscsi.bvt_verifyIscsiDel.__name__ + ' failed')
        if (iscsi.bvt_verifyIscsiSpecifyInexistentId(c)):
            FailCasesList.append('The case ' + iscsi.bvt_verifyIscsiSpecifyInexistentId.__name__ + ' failed')
        if (iscsi.bvt_verifyIscsiInvalidOption(c)):
            FailCasesList.append('The case ' + iscsi.bvt_verifyIscsiInvalidOption.__name__ + ' failed')
        if (iscsi.bvt_verifyIscsiInvalidParameters(c)):
            FailCasesList.append('The case ' + iscsi.bvt_verifyIscsiInvalidParameters.__name__ + ' failed')
        if (iscsi.bvt_verifyIscsiMissingParameters(c)):
            FailCasesList.append('The case ' + iscsi.bvt_verifyIscsiMissingParameters.__name__ + ' failed')
            

        tolog("Start verifying isns")
        import isns
        if (isns.bvt_verifyIsns(c)):
            FailCasesList.append('The case ' + isns.bvt_verifyIsns.__name__ + ' failed')
        if (isns.bvt_verifyIsnsList(c)):
            FailCasesList.append('The case ' + isns.bvt_verifyIsnsList.__name__ + ' failed')
        if (isns.bvt_verifyIsnsMod(c)):
            FailCasesList.append('The case ' + isns.bvt_verifyIsnsMod.__name__ + ' failed')
        if (isns.bvt_verifyIsnsSpecifyInexistentId(c)):
            FailCasesList.append('The case ' + isns.bvt_verifyIsnsSpecifyInexistentId.__name__ + ' failed')
        if (isns.bvt_verifyIsnsInvalidOption(c)):
            FailCasesList.append('The case ' + isns.bvt_verifyIsnsInvalidOption.__name__ + ' failed')
        if (isns.bvt_verifyIsnsInvalidParameters(c)):
            FailCasesList.append('The case ' + isns.bvt_verifyIsnsInvalidParameters.__name__ + ' failed')
        if (isns.bvt_verifyIsnsMissingParameters(c)):
            FailCasesList.append('The case ' + isns.bvt_verifyIsnsMissingParameters.__name__ + ' failed')


        tolog("Start verifying lunmap")
        import lunmap
        if (lunmap.bvt_verifyLunmapAdd(c)):
            FailCasesList.append('The case ' + lunmap.bvt_verifyLunmapAdd.__name__ + ' failed')
        if (lunmap.bvt_verifyLunmap(c)):
            FailCasesList.append('The case ' + lunmap.bvt_verifyLunmap.__name__ + ' failed')
        if (lunmap.bvt_verifyLunmapList(c)):
            FailCasesList.append('The case ' + lunmap.bvt_verifyLunmapList.__name__ + ' failed')
        if (lunmap.bvt_verifyLunmapAddlun(c)):
            FailCasesList.append('The case ' + lunmap.bvt_verifyLunmapAddlun.__name__ + ' failed')
        if (lunmap.bvt_verifyLunmapDellun(c)):
            FailCasesList.append('The case ' + lunmap.bvt_verifyLunmapDellun.__name__ + ' failed')
        if (lunmap.bvt_verifyLunmapEnable(c)):
            FailCasesList.append('The case ' + lunmap.bvt_verifyLunmapEnable.__name__ + ' failed')
        if (lunmap.bvt_verifyLunmapDel(c)):
            FailCasesList.append('The case ' + lunmap.bvt_verifyLunmapDel.__name__ + ' failed')
        if (lunmap.bvt_verifyLunmapDisable(c)):
            FailCasesList.append('The case ' + lunmap.bvt_verifyLunmapDisable.__name__ + ' failed')
        if (lunmap.bvt_verifyLunmapSpecifyInexistentId(c)):
            FailCasesList.append('The case ' + lunmap.bvt_verifyLunmapSpecifyInexistentId.__name__ + ' failed')
        if (lunmap.bvt_verifyLunmapInvalidOption(c)):
            FailCasesList.append('The case ' + lunmap.bvt_verifyLunmapInvalidOption.__name__ + ' failed')
        if (lunmap.bvt_verifyLunmapInvalidParameters(c)):
            FailCasesList.append('The case ' + lunmap.bvt_verifyLunmapInvalidParameters.__name__ + ' failed')
        if (lunmap.bvt_verifyLunmapMissingParameters(c)):
            FailCasesList.append('The case ' + lunmap.bvt_verifyLunmapMissingParameters.__name__ + ' failed')
        lunmap.bvt_cleanUp(c)

        tolog("Start verifying ntp")
        import ntp
        if (ntp.bvt_verifyNtpMod(c)):
            FailCasesList.append('The case ' + ntp.bvt_verifyNtpMod.__name__ + ' failed')
        if (ntp.bvt_verifyNtp(c)):
            FailCasesList.append('The case ' + ntp.bvt_verifyNtp.__name__ + ' failed')
        if (ntp.bvt_verifyNtpList(c)):
            FailCasesList.append('The case ' + ntp.bvt_verifyNtpList.__name__ + ' failed')
        if (ntp.bvt_verifyNtpTest(c)):
            FailCasesList.append('The case ' + ntp.bvt_verifyNtpTest.__name__ + ' failed')
        if (ntp.bvt_verifyNtpSync(c)):
            FailCasesList.append('The case ' + ntp.bvt_verifyNtpSync.__name__ + ' failed')
        if (ntp.bvt_verifyNtpInvalidOption(c)):
            FailCasesList.append('The case ' + ntp.bvt_verifyNtpInvalidOption.__name__ + ' failed')
        if (ntp.bvt_verifyNtpInvalidParameters(c)):
            FailCasesList.append('The case ' + ntp.bvt_verifyNtpInvalidParameters.__name__ + ' failed')
        if (ntp.bvt_verifyNtpMissingParameters(c)):
            FailCasesList.append('The case ' + ntp.bvt_verifyNtpMissingParameters.__name__ + ' failed')


        tolog("Start verifying password")
        import password
        if (password.bvt_verifyChangePassword(c)):
            FailCasesList.append('The case ' + password.bvt_verifyChangePassword.__name__ + ' failed')
        if (password.bvt_verifyPasswordSpecifyInexistentUsername(c)):
            FailCasesList.append('The case ' + password.bvt_verifyPasswordSpecifyInexistentUsername.__name__ + ' failed')
        if (password.bvt_verifyPasswordInvalidOption(c)):
            FailCasesList.append('The case ' + password.bvt_verifyPasswordInvalidOption.__name__ + ' failed')
        if (password.bvt_verifyPasswordInvalidParameters(c)):
            FailCasesList.append('The case ' + password.bvt_verifyPasswordInvalidParameters.__name__ + ' failed')
        if (password.bvt_verifyPasswordMissingParameters(c)):
            FailCasesList.append('The case ' + password.bvt_verifyPasswordMissingParameters.__name__ + ' failed')
            

        tolog("Start verifying pcie")
        import pcie
        if (pcie.bvt_verifyPcie(c)):
            FailCasesList.append('The case ' + pcie.bvt_verifyPcie.__name__ + ' failed')
        if (pcie.bvt_verifyPcielist(c)):
            FailCasesList.append('The case ' + pcie.bvt_verifyPcielist.__name__ + ' failed')
        if (pcie.bvt_verifyPcieInvalidOption(c)):
            FailCasesList.append('The case ' + pcie.bvt_verifyPcieInvalidOption.__name__ + ' failed')
        if (pcie.bvt_verifyPcieInvalidParameters(c)):
            FailCasesList.append('The case ' + pcie.bvt_verifyPcieInvalidParameters.__name__ + ' failed')
        if (pcie.bvt_verifyPcieMissingParameters(c)):
            FailCasesList.append('The case ' + pcie.bvt_verifyPcieMissingParameters.__name__ + ' failed')
            

        tolog("Start verifying smart")
        import smart
        if (smart.bvt_verifySmart(c)):
            FailCasesList.append('The case ' + smart.bvt_verifySmart.__name__ + ' failed')
        if (smart.bvt_verifySmartV(c)):
            FailCasesList.append('The case ' + smart.bvt_verifySmartV.__name__ + ' failed')
        if (smart.bvt_verifySmartList(c)):
            FailCasesList.append('The case ' + smart.bvt_verifySmartList.__name__ + ' failed')
        if (smart.bvt_verifySmartEnable(c)):
            FailCasesList.append('The case ' + smart.bvt_verifySmartEnable.__name__ + ' failed')
        if (smart.bvt_verifySmartDisable(c)):
            FailCasesList.append('The case ' + smart.bvt_verifySmartDisable.__name__ + ' failed')
        if (smart.bvt_verifySmartHelp(c)):
            FailCasesList.append('The case ' + smart.bvt_verifySmartHelp.__name__ + ' failed')
        if (smart.bvt_verifySmartSpecifyInexistentId(c)):
            FailCasesList.append('The case ' + smart.bvt_verifySmartSpecifyInexistentId.__name__ + ' failed')
        if (smart.bvt_verifySmartInvalidOption(c)):
            FailCasesList.append('The case ' + smart.bvt_verifySmartInvalidOption.__name__ + ' failed')
        if (smart.bvt_verifySmartInvalidParameters(c)):
            FailCasesList.append('The case ' + smart.bvt_verifySmartInvalidParameters.__name__ + ' failed')
        if (smart.bvt_verifySmartMissingParameters(c)):
            FailCasesList.append('The case ' + smart.bvt_verifySmartMissingParameters.__name__ + ' failed')
            

        tolog('Start verifying bgasched')
        import bgasched
        if (bgasched.bvt_verifyBgaschedAdd(c)):
            FailCasesList.append('The case ' + bgasched.bvt_verifyBgaschedAdd.__name__ + ' failed')
        if (bgasched.bvt_verifyBgaschedMod(c)):
            FailCasesList.append('The case ' + bgasched.bvt_verifyBgaschedMod.__name__ + ' failed')
        if (bgasched.bvt_verifyBgaschedList(c)):
            FailCasesList.append('The case ' + bgasched.bvt_verifyBgaschedList.__name__ + ' failed')
        if (bgasched.bvt_verifyBgaschedDel(c)):
            FailCasesList.append('The case ' + bgasched.bvt_verifyBgaschedDel.__name__ + ' failed')
        if (bgasched.bvt_verifyBgaschedHelp(c)):
            FailCasesList.append('The case ' + bgasched.bvt_verifyBgaschedHelp.__name__ + ' failed')
        if (bgasched.bvt_verifyBgaschedInvalidOption(c)):
            FailCasesList.append('The case ' + bgasched.bvt_verifyBgaschedInvalidOption.__name__ + ' failed')
        if (bgasched.bvt_verifyBgaschedInvalidParameters(c)):
            FailCasesList.append('The case ' + bgasched.bvt_verifyBgaschedInvalidParameters.__name__ + ' failed')
        if (bgasched.bvt_verifyBgaschedMissingParameters(c)):
            FailCasesList.append('The case ' + bgasched.bvt_verifyBgaschedMissingParameters.__name__ + ' failed')
        bgasched.bvt_clearUp(c)
            

        tolog('Start verifying rb')
        import rb
        if (rb.bvt_verifyRbStartAndStopAndList(c)):
            FailCasesList.append('The case ' + rb.bvt_verifyRbStartAndStopAndList.__name__ + ' failed')
        if (rb.bvt_verifyRbInvalidOption(c)):
            FailCasesList.append('The case ' + rb.bvt_verifyRbInvalidOption.__name__ + ' failed')
        if (rb.bvt_verifyRbInvalidParameters(c)):
            FailCasesList.append('The case ' + rb.bvt_verifyRbInvalidParameters.__name__ + ' failed')
        if (rb.bvt_verifyRbMissingParameters(c)):
            FailCasesList.append('The case ' + rb.bvt_verifyRbMissingParameters.__name__ + ' failed')



    if len(FailCasesList) != 0:
        Failflag = True
        for f in FailCasesList:
            tolog(f)

    else:
        tolog("Failed to connect server after ptiflash.")
        Failflag = True

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)

    c.close()
    ssh.close()


if __name__ == "__main__":

    start = time.clock()
    c, ssh = ssh_conn()
    BuildVerification(c)
    c.close()
