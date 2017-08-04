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

buildserverurl="http://192.168.208.5/release/hyperion_ds/daily/"
tftpserver="/work/tftpboot/"
import pool
from time import sleep

import os

from send_cmd import *
from ssh_connect import *
forBVT = True
from to_log import *
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def BuildVerification(c):

    Failflag=False
    flashimage=False
    count=0
    Failflaglist = list()
    c, ssh = ssh_conn()

    import glob
    files=glob.glob("/var/lib/jenkins/workspace/HyperionDS/build/build/*.ptif")
    for file in files:


        filename=file.replace("/var/lib/jenkins/workspace/HyperionDS/build/build/","")
        SendCmdRestart(c,"ptiflash -y -t -s 10.84.2.66 -f "+filename)

        i=1
        while i< 160:
            # wait for rebooting
           tolog("ptiflash is in progress, please wait, %d seconds elapse" %i)
           i+=1
           sleep(1)

    # check if ssh connection is ok.
    # wait for another 120 seconds
        reconnectflag=False
        for x in range(30):
            try:
                c,ssh=ssh_conn()
                reconnectflag=True
                break
            except Exception, e:
                print e
                sleep(4)


    if reconnectflag:
        tolog("Start verifying pool add")
        Failflaglist.append(pool.bvtpoolcreateandlist.__name__ + ":" + 'False'
                            if not pool.bvtpoolcreateandlist(c, 1)
                            else pool.bvtpoolcreateandlist.__name__ + ":" + 'True')

        tolog("Start verifying pool global setting")
        Failflaglist.append(pool.bvtpoolglobalsetting.__name__ + ":" + 'False'
                            if not pool.bvtpoolglobalsetting(c)
                            else pool.bvtpoolglobalsetting.__name__ + ":" + 'True')

        tolog("Start verifying volume add")
        Failflaglist.append(pool.bvtvolumecreateandlist.__name__ + ":" + 'False'
                            if not pool.bvtvolumecreateandlist(c, 10)
                            else pool.bvtvolumecreateandlist.__name__ + ":" + 'True')

        tolog("Start verifying snapshot add")
        Failflaglist.append(pool.bvtsnapshotcreateandlist.__name__ + ":" + 'False'
                            if not pool.bvtsnapshotcreateandlist(c, 2)
                            else pool.bvtsnapshotcreateandlist.__name__ + ":" + 'True')

        tolog("Start verifying clone add")
        Failflaglist.append(pool.bvtclonecreateandlist.__name__ + ":" + 'False'
                            if not pool.bvtclonecreateandlist(c, 2)
                            else pool.bvtclonecreateandlist.__name__ + ":" + 'True')

        tolog("Start verifying delete clone")
        Failflaglist.append(pool.bvtclonedelete.__name__ + ":" + 'False'
                            if not pool.bvtclonedelete(c)
                            else pool.bvtclonedelete.__name__ + ":" + 'True')

        tolog("Start verifying delete snapshot")
        Failflaglist.append(pool.bvtsnapshotdelete.__name__ + ":" + 'False'
                            if not pool.bvtsnapshotdelete(c)
                            else pool.bvtsnapshotdelete.__name__ + ":" + 'True')

        tolog("Start verifying delete volume")
        Failflaglist.append(pool.bvtvolumedel.__name__ + ":" + 'False'
                            if not pool.bvtvolumedel(c)
                            else pool.bvtvolumedel.__name__ + ":" + 'True')

        tolog("Start verifying delete pool")
        Failflaglist.append(pool.bvtpooldel.__name__ + ":" + 'False'
                            if not pool.bvtpooldel(c)
                            else pool.bvtpooldel.__name__ + ":" + 'True')

        tolog("Start verifying pool add for a second time")
        Failflaglist.append(pool.bvtpoolcreateandlist.__name__ + ":" + 'False'
                            if not pool.bvtpoolcreateandlist(c, 0)
                            else pool.bvtpoolcreateandlist.__name__ + ":" + 'True')

        tolog("Start verifying pool global setting")
        Failflaglist.append(pool.bvtpoolglobalsetting.__name__ + ":" + 'False'
                            if not pool.bvtpoolglobalsetting(c)
                            else pool.bvtpoolglobalsetting.__name__ + ":" + 'True')

        tolog("Start verifying volume add many")
        Failflaglist.append(pool.bvtvolumeaddmany.__name__ + ":" + 'False'
                            if not pool.bvtvolumeaddmany(c, 2)
                            else pool.bvtvolumeaddmany.__name__ + ":" + 'True')

        tolog("Start verifying snapshot add")
        Failflaglist.append(pool.bvtsnapshotcreateandlist.__name__ + ":" + 'False'
                            if not pool.bvtsnapshotcreateandlist(c, 2)
                            else pool.bvtsnapshotcreateandlist.__name__ + ":" + 'True')

        tolog("Start verifying clone add")
        Failflaglist.append(pool.bvtclonecreateandlist.__name__ + ":" + 'False'
                            if not pool.bvtclonecreateandlist(c, 2)
                            else pool.bvtclonecreateandlist.__name__ + ":" + 'True')

        tolog("Start verifying clone export/unexport")
        Failflaglist.append(pool.bvtexportunexport.__name__ + ":" + 'False'
                            if not pool.bvtexportunexport(c, "clone")
                            else pool.bvtexportunexport.__name__ + ":" + 'True')

        tolog("Start verifying snapshot export/unexport")
        Failflaglist.append(pool.bvtexportunexport.__name__ + ":" + 'False'
                            if not pool.bvtexportunexport(c, "snapshot")
                            else pool.bvtexportunexport.__name__ + ":" + 'True')

        tolog("Start verifying volume export/unexport")
        Failflaglist.append(pool.bvtexportunexport.__name__ + ":" + 'False'
                            if not pool.bvtexportunexport(c, "volume")
                            else pool.bvtexportunexport.__name__ + ":" + 'True')

        tolog("Start verifying pool force delete")
        Failflaglist.append(pool.bvtforcedel.__name__ + ":" + 'False'
                            if not pool.bvtforcedel(c, "pool")
                            else pool.bvtforcedel.__name__ + ":" + 'True')

        tolog("Start verifying pool add for 3rd time")
        Failflaglist.append(pool.bvtpoolcreateandlist.__name__ + ":" + 'False'
                            if not pool.bvtpoolcreateandlist(c, 2)
                            else pool.bvtpoolcreateandlist.__name__ + ":" + 'True')

        tolog("Start verifying spare add")
        Failflaglist.append(pool.bvtsparedrvcreate.__name__ + ":" + 'False'
                            if not pool.bvtsparedrvcreate(c, 2)
                            else pool.bvtsparedrvcreate.__name__ + ":" + 'True')

        tolog("Start verifying delete spare")
        Failflaglist.append(pool.bvtsparedelete.__name__ + ":" + 'False'
                            if not pool.bvtsparedelete(c)
                            else pool.bvtsparedelete.__name__ + ":" + 'True')

        tolog("Start verifying pool extend")
        Failflaglist.append(pool.bvtpoolmodifyandlist.__name__ + ":" + 'False'
                            if not pool.bvtpoolmodifyandlist(c)
                            else pool.bvtpoolmodifyandlist.__name__ + ":" + 'True')

        tolog("Start verifying volume add")
        Failflaglist.append(pool.bvtvolumecreateandlist.__name__ + ":" + 'False'
                            if not pool.bvtvolumecreateandlist(c, 10)
                            else pool.bvtvolumecreateandlist.__name__ + ":" + 'True')

        tolog("Start verifying snapshot add")
        Failflaglist.append(pool.bvtsnapshotcreateandlist.__name__ + ":" + 'False'
                            if not pool.bvtsnapshotcreateandlist(c, 2)
                            else pool.bvtsnapshotcreateandlist.__name__ + ":" + 'True')

        tolog("Start verifying clone add")
        Failflaglist.append(pool.bvtclonecreateandlist.__name__ + ":" + 'False'
                            if not pool.bvtclonecreateandlist(c, 2)
                            else pool.bvtclonecreateandlist.__name__ + ":" + 'True')

        tolog("Start verifying clone force delete")
        Failflaglist.append(pool.bvtforcedel.__name__ + ":" + 'False'
                            if not pool.bvtforcedel(c, "clone")
                            else pool.bvtforcedel.__name__ + ":" + 'True')

        tolog("Start verifying snapshot force delete")
        Failflaglist.append(pool.bvtforcedel.__name__ + ":" + 'False'
                            if not pool.bvtforcedel(c, "snapshot")
                            else pool.bvtforcedel.__name__ + ":" + 'True')

        tolog("Start verifying volume force delete")
        Failflaglist.append(pool.bvtforcedel.__name__ + ":" + 'False'
                            if not pool.bvtforcedel(c, "volume")
                            else pool.bvtforcedel.__name__ + ":" + 'True')

        Failflaglist.append(pool.bvtforcedel.__name__ + ":" + 'False'
                            if not pool.bvtforcedel(c, "pool")
                            else pool.bvtforcedel.__name__ + ":" + 'True')

        # tolog("Start verifying pool create with all raid level and parameters")
        # Failflaglist.append(pool.bvtpoolcreateverify_newraidlevel(c))
        #
        # tolog("Start verifying pool output error")
        # Failflaglist.append(pool.bvtpoolcreateverifyoutputerror_newraidlevel(c))

        tolog("Start verifying about")
        import about
        Failflaglist.append(about.bvt_verifyAbout.__name__ + ":" + 'False'
                            if not about.bvt_verifyAbout(c)
                            else about.bvt_verifyAbout.__name__ + ":" + 'True')
        Failflaglist.append(about.bvt_verifyAboutHelp.__name__ + ":" + 'False'
                            if not about.bvt_verifyAboutHelp(c)
                            else about.bvt_verifyAboutHelp.__name__ + ":" + 'True')
        Failflaglist.append(about.bvt_verifyAboutInvalidOption.__name__ + ":" + 'False'
                            if not about.bvt_verifyAboutInvalidOption(c)
                            else about.bvt_verifyAboutInvalidOption.__name__ + ":" + 'True')
        Failflaglist.append(about.bvt_verifyAboutInvalidParameters.__name__ + ":" + 'False'
                            if not about.bvt_verifyAboutInvalidParameters(c)
                            else about.bvt_verifyAboutInvalidParameters.__name__ + ":" + 'True')

        tolog("Start verifying battery")
        import battery
        Failflaglist.append(battery.bvt_verifyBattery.__name__ + ":" + 'False'
                            if not battery.bvt_verifyBattery(c)
                            else battery.bvt_verifyBattery.__name__ + ":" + 'True')
        Failflaglist.append(battery.bvt_verifyBatteryList.__name__ + ":" + 'False'
                            if not battery.bvt_verifyBatteryList(c)
                            else battery.bvt_verifyBatteryList.__name__ + ":" + 'True')
        Failflaglist.append(battery.bvt_verifyBatteryRecondition.__name__ + ":" + 'False'
                            if not battery.bvt_verifyBatteryRecondition(c)
                            else battery.bvt_verifyBatteryRecondition.__name__ + ":" + 'True')
        Failflaglist.append(battery.bvt_verifyBatteryHelp.__name__ + ":" + 'False'
                            if not battery.bvt_verifyBatteryHelp(c)
                            else battery.bvt_verifyBatteryHelp.__name__ + ":" + 'True')
        Failflaglist.append(battery.bvt_verifyBatterySpecifyInexistentId.__name__ + ":" + 'False'
                            if not battery.bvt_verifyBatterySpecifyInexistentId(c)
                            else battery.bvt_verifyBatterySpecifyInexistentId.__name__ + ":" + 'True')
        Failflaglist.append(battery.bvt_verifyBatteryInvalidOption.__name__ + ":" + 'False'
                            if not battery.bvt_verifyBatteryInvalidOption(c)
                            else battery.bvt_verifyBatteryInvalidOption.__name__ + ":" + 'True')
        Failflaglist.append(battery.bvt_verifyBatteryInvalidParameters.__name__ + ":" + 'False'
                            if not battery.bvt_verifyBatteryInvalidParameters(c)
                            else battery.bvt_verifyBatteryInvalidParameters.__name__ + ":" + 'True')
        Failflaglist.append(battery.bvt_verifyBatteryMissingParameters.__name__ + ":" + 'False'
                            if not battery.bvt_verifyBatteryMissingParameters(c)
                            else battery.bvt_verifyBatteryMissingParameters.__name__ + ":" + 'True')

        tolog("Start verifying BBM")
        import bbm
        Failflaglist.append(bbm.bvt_verifyBBM.__name__ + ":" + 'False'
                            if not bbm.bvt_verifyBBM(c)
                            else bbm.bvt_verifyBBM.__name__ + ":" + 'True')
        Failflaglist.append(bbm.bvt_verifyBBMClear.__name__ + ":" + 'False'
                            if not bbm.bvt_verifyBBMClear(c)
                            else bbm.bvt_verifyBBMClear.__name__ + ":" + 'True')
        Failflaglist.append(bbm.bvt_verifyBBMClearFailedTest.__name__ + ":" + 'False'
                            if not bbm.bvt_verifyBBMClearFailedTest(c)
                            else bbm.bvt_verifyBBMClearFailedTest.__name__ + ":" + 'True')
        Failflaglist.append(bbm.bvt_verifyBBMHelp.__name__ + ":" + 'False'
                            if not bbm.bvt_verifyBBMHelp(c)
                            else bbm.bvt_verifyBBMHelp.__name__ + ":" + 'True')
        Failflaglist.append(bbm.bvt_verifyBBMInvalidOption.__name__ + ":" + 'False'
                            if not bbm.bvt_verifyBBMInvalidOption(c)
                            else bbm.bvt_verifyBBMInvalidOption.__name__ + ":" + 'True')
        Failflaglist.append(bbm.bvt_verifyBBMInvalidParameters.__name__ + ":" + 'False'
                            if not bbm.bvt_verifyBBMInvalidParameters(c)
                            else bbm.bvt_verifyBBMInvalidParameters.__name__ + ":" + 'True')
        Failflaglist.append(bbm.bvt_verifyBBMList.__name__ + ":" + 'False'
                            if not bbm.bvt_verifyBBMList(c)
                            else bbm.bvt_verifyBBMList.__name__ + ":" + 'True')
        Failflaglist.append(bbm.bvt_verifyBBMMissingParameters.__name__ + ":" + 'False'
                            if not bbm.bvt_verifyBBMMissingParameters(c)
                            else bbm.bvt_verifyBBMMissingParameters.__name__ + ":" + 'True')
        Failflaglist.append(bbm.bvt_verifyBBMSpecifyInexistentId.__name__ + ":" + 'False'
                            if not bbm.bvt_verifyBBMSpecifyInexistentId(c)
                            else bbm.bvt_verifyBBMSpecifyInexistentId.__name__ + ":" + 'True')


        tolog("Start verifying bga")
        import bga
        Failflaglist.append(bga.bvt_verifyBga.__name__ + ":" + 'False'
                            if not bga.bvt_verifyBga(c)
                            else bga.bvt_verifyBga.__name__ + ":" + 'True')
        Failflaglist.append(bga.bvt_verifyBgaList.__name__ + ":" + 'False'
                            if not bga.bvt_verifyBgaList(c)
                            else bga.bvt_verifyBgaList.__name__ + ":" + 'True')
        Failflaglist.append(bga.bvt_verifyBgaMod.__name__ + ":" + 'False'
                            if not bga.bvt_verifyBgaMod(c)
                            else bga.bvt_verifyBgaMod.__name__ + ":" + 'True')
        Failflaglist.append(bga.bvt_verifyBgaHelp.__name__ + ":" + 'False'
                            if not bga.bvt_verifyBgaHelp(c)
                            else bga.bvt_verifyBgaHelp.__name__ + ":" + 'True')
        Failflaglist.append(bga.bvt_verifyBgaInvalidOption.__name__ + ":" + 'False'
                            if not bga.bvt_verifyBgaInvalidOption(c)
                            else bga.bvt_verifyBgaInvalidOption.__name__ + ":" + 'True')
        Failflaglist.append(bga.bvt_verifyBgaInvalidParameters.__name__ + ":" + 'False'
                            if not bga.bvt_verifyBgaInvalidParameters(c)
                            else bga.bvt_verifyBgaInvalidParameters.__name__ + ":" + 'True')
        Failflaglist.append(bga.bvt_verifyBgaMissingParameters.__name__ + ":" + 'False'
                            if not bga.bvt_verifyBgaMissingParameters(c)
                            else bga.bvt_verifyBgaMissingParameters.__name__ + ":" + 'True')

        tolog("Start verifying buzzer")
        import buzzer
        Failflaglist.append(buzzer.bvt_verifyBuzzerDisableAndSilentTurnOn.__name__ + ":" + 'False'
                            if not buzzer.bvt_verifyBuzzerDisableAndSilentTurnOn(c)
                            else buzzer.bvt_verifyBuzzerDisableAndSilentTurnOn.__name__ + ":" + 'True')
        Failflaglist.append(buzzer.bvt_verifyBuzzerEnableAndSilentTurnOn.__name__ + ":" + 'False'
                            if not buzzer.bvt_verifyBuzzerEnableAndSilentTurnOn(c)
                            else buzzer.bvt_verifyBuzzerEnableAndSilentTurnOn.__name__ + ":" + 'True')
        Failflaglist.append(buzzer.bvt_verifyBuzzerEnableAndSoundingTurnOn.__name__ + ":" + 'False'
                            if not buzzer.bvt_verifyBuzzerEnableAndSoundingTurnOn(c)
                            else buzzer.bvt_verifyBuzzerEnableAndSoundingTurnOn.__name__ + ":" + 'True')
        Failflaglist.append(buzzer.bvt_verifyBuzzerDisableAndSilentTurnOff.__name__ + ":" + 'False'
                            if not buzzer.bvt_verifyBuzzerDisableAndSilentTurnOff(c)
                            else buzzer.bvt_verifyBuzzerDisableAndSilentTurnOff.__name__ + ":" + 'True')
        Failflaglist.append(buzzer.bvt_verifyBuzzerEnableAndSilentTurnOff.__name__ + ":" + 'False'
                            if not buzzer.bvt_verifyBuzzerEnableAndSilentTurnOff(c)
                            else buzzer.bvt_verifyBuzzerEnableAndSilentTurnOff.__name__ + ":" + 'True')
        Failflaglist.append(buzzer.bvt_verifyBuzzerEnableAndSoundingTurnOff.__name__ + ":" + 'False'
                            if not buzzer.bvt_verifyBuzzerEnableAndSoundingTurnOff(c)
                            else buzzer.bvt_verifyBuzzerEnableAndSoundingTurnOff.__name__ + ":" + 'True')
        Failflaglist.append(buzzer.bvt_verifyBuzzerDisableAndSilentEnable.__name__ + ":" + 'False'
                            if not buzzer.bvt_verifyBuzzerDisableAndSilentEnable(c)
                            else buzzer.bvt_verifyBuzzerDisableAndSilentEnable.__name__ + ":" + 'True')
        Failflaglist.append(buzzer.bvt_verifyBuzzerEnableAndSilentEnable.__name__ + ":" + 'False'
                            if not buzzer.bvt_verifyBuzzerEnableAndSilentEnable(c)
                            else buzzer.bvt_verifyBuzzerEnableAndSilentEnable.__name__ + ":" + 'True')
        Failflaglist.append(buzzer.bvt_verifyBuzzerEnableAndSoundingEnable.__name__ + ":" + 'False'
                            if not buzzer.bvt_verifyBuzzerEnableAndSoundingEnable(c)
                            else buzzer.bvt_verifyBuzzerEnableAndSoundingEnable.__name__ + ":" + 'True')
        Failflaglist.append(buzzer.bvt_verifyBuzzerEnableAndSoundingDisable.__name__ + ":" + 'False'
                            if not buzzer.bvt_verifyBuzzerEnableAndSoundingDisable(c)
                            else buzzer.bvt_verifyBuzzerEnableAndSoundingDisable.__name__ + ":" + 'True')
        Failflaglist.append(buzzer.bvt_verifyBuzzerEnableAndSilentDisable.__name__ + ":" + 'False'
                            if not buzzer.bvt_verifyBuzzerEnableAndSilentDisable(c)
                            else buzzer.bvt_verifyBuzzerEnableAndSilentDisable.__name__ + ":" + 'True')
        Failflaglist.append(buzzer.bvt_verifyBuzzerDisableAndSilentDisable.__name__ + ":" + 'False'
                            if not buzzer.bvt_verifyBuzzerDisableAndSilentDisable(c)
                            else buzzer.bvt_verifyBuzzerDisableAndSilentDisable.__name__ + ":" + 'True')
        Failflaglist.append(buzzer.bvt_verifyBuzzerInfo.__name__ + ":" + 'False'
                            if not buzzer.bvt_verifyBuzzerInfo(c)
                            else buzzer.bvt_verifyBuzzerInfo.__name__ + ":" + 'True')
        Failflaglist.append(buzzer.bvt_verifyBuzzerHelp.__name__ + ":" + 'False'
                            if not buzzer.bvt_verifyBuzzerHelp(c)
                            else buzzer.bvt_verifyBuzzerHelp.__name__ + ":" + 'True')
        Failflaglist.append(buzzer.bvt_verifyBuzzerInvalidParameters.__name__ + ":" + 'False'
                            if not buzzer.bvt_verifyBuzzerInvalidParameters(c)
                            else buzzer.bvt_verifyBuzzerInvalidParameters.__name__ + ":" + 'True')
        Failflaglist.append(buzzer.bvt_verifyBuzzerInvalidOption.__name__ + ":" + 'False'
                            if not buzzer.bvt_verifyBuzzerInvalidOption(c)
                            else buzzer.bvt_verifyBuzzerInvalidOption.__name__ + ":" + 'True')

        #tolog("Start verifying chap")
        import chap
        # Failflaglist.append(chap.bvt_verifyChapAdd.__name__ + ":" + 'False'
        #                     if not chap.bvt_verifyChapAdd(c)
        #                     else chap.bvt_verifyChapAdd.__name__ + ":" + 'True')
        # Failflaglist.append(chap.bvt_verifyChap.__name__ + ":" + 'False'
        #                     if not chap.bvt_verifyChap(c)
        #                     else chap.bvt_verifyChap.__name__ + ":" + 'True')
        # Failflaglist.append(chap.bvt_verifyChapList.__name__ + ":" + 'False'
        #                     if not chap.bvt_verifyChapList(c)
        #                     else chap.bvt_verifyChapList.__name__ + ":" + 'True')
        # Failflaglist.append(chap.bvt_verifyChapMod.__name__ + ":" + 'False'
        #                     if not chap.bvt_verifyChapMod(c)
        #                     else chap.bvt_verifyChapMod.__name__ + ":" + 'True')
        # Failflaglist.append(chap.bvt_verifyChapDel.__name__ + ":" + 'False'
        #                     if not chap.bvt_verifyChapDel(c)
        #                     else chap.bvt_verifyChapDel.__name__ + ":" + 'True')
        # Failflaglist.append(chap.bvt_verifyChapHelp.__name__ + ":" + 'False'
        #                     if not chap.bvt_verifyChapHelp(c)
        #                     else chap.bvt_verifyChapHelp.__name__ + ":" + 'True')
        # Failflaglist.append(chap.bvt_verifyChapSpecifyErrorId.__name__ + ":" + 'False'
        #                     if not chap.bvt_verifyChapSpecifyErrorId(c)
        #                     else chap.bvt_verifyChapSpecifyErrorId.__name__ + ":" + 'True')
        # Failflaglist.append(chap.bvt_verifyChapInvalidOption.__name__ + ":" + 'False'
        #                     if not chap.bvt_verifyChapInvalidOption(c)
        #                     else chap.bvt_verifyChapInvalidOption.__name__ + ":" + 'True')
        # Failflaglist.append(chap.bvt_verifyChapInvalidParameters.__name__ + ":" + 'False'
        #                     if not chap.bvt_verifyChapInvalidParameters(c)
        #                     else chap.bvt_verifyChapInvalidParameters.__name__ + ":" + 'True')
        # Failflaglist.append(chap.bvt_verifyChapMissingParameters.__name__ + ":" + 'False'
        #                     if not chap.bvt_verifyChapMissingParameters(c)
        #                     else chap.bvt_verifyChapMissingParameters.__name__ + ":" + 'True')

        import ctrl
        tolog("Start verifying ctrl")
        Failflaglist.append(ctrl.bvt_verifyCtrl.__name__ + ":" + 'False'
                            if not ctrl.bvt_verifyCtrl(c)
                            else ctrl.bvt_verifyCtrl.__name__ + ":" + 'True')
        Failflaglist.append(ctrl.bvt_verifyCtrlSpecifyId.__name__ + ":" + 'False'
                            if not ctrl.bvt_verifyCtrlSpecifyId(c)
                            else ctrl.bvt_verifyCtrlSpecifyId.__name__ + ":" + 'True')
        Failflaglist.append(ctrl.bvt_verifyCtrlSpecifyInexistentId.__name__ + ":" + 'False'
                            if not ctrl.bvt_verifyCtrlSpecifyInexistentId(c)
                            else ctrl.bvt_verifyCtrlSpecifyInexistentId.__name__ + ":" + 'True')
        Failflaglist.append(ctrl.bvt_verifyCtrlList.__name__ + ":" + 'False'
                            if not ctrl.bvt_verifyCtrlList(c)
                            else ctrl.bvt_verifyCtrlList.__name__ + ":" + 'True')
        Failflaglist.append(ctrl.bvt_verifyCtrlV.__name__ + ":" + 'False'
                            if not ctrl.bvt_verifyCtrlV(c)
                            else ctrl.bvt_verifyCtrlV.__name__ + ":" + 'True')
        Failflaglist.append(ctrl.bvt_verifyCtrlListV.__name__ + ":" + 'False'
                            if not ctrl.bvt_verifyCtrlListV(c)
                            else ctrl.bvt_verifyCtrlListV.__name__ + ":" + 'True')
        Failflaglist.append(ctrl.bvt_verifyCtrlModNormativeAlias.__name__ + ":" + 'False'
                            if not ctrl.bvt_verifyCtrlModNormativeAlias(c)
                            else ctrl.bvt_verifyCtrlModNormativeAlias.__name__ + ":" + 'True')
        Failflaglist.append(ctrl.bvt_verifyCtrlModValuesIsEnableOrDisable.__name__ + ":" + 'False'
                            if not ctrl.bvt_verifyCtrlModValuesIsEnableOrDisable(c)
                            else ctrl.bvt_verifyCtrlModValuesIsEnableOrDisable.__name__ + ":" + 'True')
        Failflaglist.append(ctrl.bvt_verifyCtrlModValuesIsTime.__name__ + ":" + 'False'
                            if not ctrl.bvt_verifyCtrlModValuesIsTime(c)
                            else ctrl.bvt_verifyCtrlModValuesIsTime.__name__ + ":" + 'True')
        Failflaglist.append(ctrl.bvt_verifyCtrlClear.__name__ + ":" + 'False'
                            if not ctrl.bvt_verifyCtrlClear(c)
                            else ctrl.bvt_verifyCtrlClear.__name__ + ":" + 'True')
        Failflaglist.append(ctrl.bvt_verifyCtrlHelp.__name__ + ":" + 'False'
                            if not ctrl.bvt_verifyCtrlHelp(c)
                            else ctrl.bvt_verifyCtrlHelp.__name__ + ":" + 'True')
        Failflaglist.append(ctrl.bvt_verifyCtrlInvalidOption.__name__ + ":" + 'False'
                            if not ctrl.bvt_verifyCtrlInvalidOption(c)
                            else ctrl.bvt_verifyCtrlInvalidOption.__name__ + ":" + 'True')
        Failflaglist.append(ctrl.bvt_verifyCtrlInvalidParameters.__name__ + ":" + 'False'
                            if not ctrl.bvt_verifyCtrlInvalidParameters(c)
                            else ctrl.bvt_verifyCtrlInvalidParameters.__name__ + ":" + 'True')
        Failflaglist.append(ctrl.bvt_verifyCtrlMissingParameters.__name__ + ":" + 'False'
                            if not ctrl.bvt_verifyCtrlMissingParameters(c)
                            else ctrl.bvt_verifyCtrlMissingParameters.__name__ + ":" + 'True')
        Failflaglist.append(ctrl.bvt_verifyCtrlSpecifyInexistentId.__name__ + ":" + 'False'
                            if not ctrl.bvt_verifyCtrlSpecifyInexistentId(c)
                            else ctrl.bvt_verifyCtrlSpecifyInexistentId.__name__ + ":" + 'True')

        tolog("Start verifying encldiag")
        import encldiag
        Failflaglist.append(encldiag.bvt_verifyEncldiag.__name__ + ":" + 'False'
                            if not encldiag.bvt_verifyEncldiag(c)
                            else encldiag.bvt_verifyEncldiag.__name__ + ":" + 'True')
        Failflaglist.append(encldiag.bvt_verifyEncldiagList.__name__ + ":" + 'False'
                            if not encldiag.bvt_verifyEncldiagList(c)
                            else encldiag.bvt_verifyEncldiagList.__name__ + ":" + 'True')
        Failflaglist.append(encldiag.bvt_verifyEncldiagHelp.__name__ + ":" + 'False'
                            if not encldiag.bvt_verifyEncldiagHelp(c)
                            else encldiag.bvt_verifyEncldiagHelp.__name__ + ":" + 'True')
        Failflaglist.append(encldiag.bvt_verifyEncldiagSpecifyInexistentId.__name__ + ":" + 'False'
                            if not encldiag.bvt_verifyEncldiagSpecifyInexistentId(c)
                            else encldiag.bvt_verifyEncldiagSpecifyInexistentId.__name__ + ":" + 'True')
        Failflaglist.append(encldiag.bvt_verifyEncldiagInvalidOption.__name__ + ":" + 'False'
                            if not encldiag.bvt_verifyEncldiagInvalidOption(c)
                            else encldiag.bvt_verifyEncldiagInvalidOption.__name__ + ":" + 'True')
        Failflaglist.append(encldiag.bvt_verifyEncldiagInvalidParameters.__name__ + ":" + 'False'
                            if not encldiag.bvt_verifyEncldiagInvalidParameters(c)
                            else encldiag.bvt_verifyEncldiagInvalidParameters.__name__ + ":" + 'True')
        Failflaglist.append(encldiag.bvt_verifyEncldiagMissingParameters.__name__ + ":" + 'False'
                            if not encldiag.bvt_verifyEncldiagMissingParameters(c)
                            else encldiag.bvt_verifyEncldiagMissingParameters.__name__ + ":" + 'True')

        tolog("Start verifying enclosure")
        import enclosure
        Failflaglist.append(enclosure.bvt_verifyEnclosure.__name__ + ":" + 'False'
                            if not enclosure.bvt_verifyEnclosure(c)
                            else enclosure.bvt_verifyEnclosure.__name__ + ":" + 'True')
        Failflaglist.append(enclosure.bvt_verifyEnclosureList.__name__ + ":" + 'False'
                            if not enclosure.bvt_verifyEnclosureList(c)
                            else enclosure.bvt_verifyEnclosureList.__name__ + ":" + 'True')
        Failflaglist.append(enclosure.bvt_verifyEnclosureMod.__name__ + ":" + 'False'
                            if not enclosure.bvt_verifyEnclosureMod(c)
                            else enclosure.bvt_verifyEnclosureMod.__name__ + ":" + 'True')
        Failflaglist.append(enclosure.bvt_verifyEnclosureLocate.__name__ + ":" + 'False'
                            if not enclosure.bvt_verifyEnclosureLocate(c)
                            else enclosure.bvt_verifyEnclosureLocate.__name__ + ":" + 'True')
        Failflaglist.append(enclosure.bvt_verifyEnclosureHelp.__name__ + ":" + 'False'
                            if not enclosure.bvt_verifyEnclosureHelp(c)
                            else enclosure.bvt_verifyEnclosureHelp.__name__ + ":" + 'True')
        Failflaglist.append(enclosure.bvt_verifEnclosureSpecifyInexistentId.__name__ + ":" + 'False'
                            if not enclosure.bvt_verifEnclosureSpecifyInexistentId(c)
                            else enclosure.bvt_verifEnclosureSpecifyInexistentId.__name__ + ":" + 'True')
        Failflaglist.append(enclosure.bvt_verifyEnclosureInvalidOption.__name__ + ":" + 'False'
                            if not enclosure.bvt_verifyEnclosureInvalidOption(c)
                            else enclosure.bvt_verifyEnclosureInvalidOption.__name__ + ":" + 'True')
        Failflaglist.append(enclosure.bvt_verifyEnclosureInvalidParameters.__name__ + ":" + 'False'
                            if not enclosure.bvt_verifyEnclosureInvalidParameters(c)
                            else enclosure.bvt_verifyEnclosureInvalidParameters.__name__ + ":" + 'True')
        Failflaglist.append(enclosure.bvt_verifyEnclosureMissingParameters.__name__ + ":" + 'False'
                            if not enclosure.bvt_verifyEnclosureMissingParameters(c)
                            else enclosure.bvt_verifyEnclosureMissingParameters.__name__ + ":" + 'True')

        tolog("Start verifying event")
        import event
        Failflaglist.append(event.bvt_verifyEvent.__name__ + ":" + 'False'
                            if not event.bvt_verifyEvent(c)
                            else event.bvt_verifyEvent.__name__ + ":" + 'True')
        Failflaglist.append(event.bvt_verifyEventList.__name__ + ":" + 'False'
                            if not event.bvt_verifyEventList(c)
                            else event.bvt_verifyEventList.__name__ + ":" + 'True')
        Failflaglist.append(event.bvt_verifyEventClear.__name__ + ":" + 'False'
                            if not event.bvt_verifyEventClear(c)
                            else event.bvt_verifyEventClear.__name__ + ":" + 'True')
        Failflaglist.append(event.bvt_verifyEventHelp.__name__ + ":" + 'False'
                            if not event.bvt_verifyEventHelp(c)
                            else event.bvt_verifyEventHelp.__name__ + ":" + 'True')
        Failflaglist.append(event.bvt_verifEventSpecifyInexistentId.__name__ + ":" + 'False'
                            if not event.bvt_verifEventSpecifyInexistentId(c)
                            else event.bvt_verifEventSpecifyInexistentId.__name__ + ":" + 'True')
        Failflaglist.append(event.bvt_verifyEventInvalidOption.__name__ + ":" + 'False'
                            if not event.bvt_verifyEventInvalidOption(c)
                            else event.bvt_verifyEventInvalidOption.__name__ + ":" + 'True')
        Failflaglist.append(event.bvt_verifyEventInvalidParameters.__name__ + ":" + 'False'
                            if not event.bvt_verifyEventInvalidParameters(c)
                            else event.bvt_verifyEventInvalidParameters.__name__ + ":" + 'True')
        Failflaglist.append(event.bvt_verifyEventMissingParameters.__name__ + ":" + 'False'
                            if not event.bvt_verifyEventMissingParameters(c)
                            else event.bvt_verifyEventMissingParameters.__name__ + ":" + 'True')

        tolog("Start verifying factorydefaults")
        import factorydefaults
        Failflaglist.append(factorydefaults.bvt_factorydefaultsBga.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_factorydefaultsBga(c)
                            else factorydefaults.bvt_factorydefaultsBga.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_factorydefaultsCtrl.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_factorydefaultsCtrl(c)
                            else factorydefaults.bvt_factorydefaultsCtrl.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_factorydefaultsEncl.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_factorydefaultsEncl(c)
                            else factorydefaults.bvt_factorydefaultsEncl.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_factorydefaultsFc.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_factorydefaultsFc(c)
                            else factorydefaults.bvt_factorydefaultsFc.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_factorydefaultsIscsi.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_factorydefaultsIscsi(c)
                            else factorydefaults.bvt_factorydefaultsIscsi.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_factorydefaultsPhydrv.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_factorydefaultsPhydrv(c)
                            else factorydefaults.bvt_factorydefaultsPhydrv.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_factorydefaultsSas.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_factorydefaultsSas(c)
                            else factorydefaults.bvt_factorydefaultsSas.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_factorydefaultsScsi.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_factorydefaultsScsi(c)
                            else factorydefaults.bvt_factorydefaultsScsi.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_factorydefaultsSubsys.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_factorydefaultsSubsys(c)
                            else factorydefaults.bvt_factorydefaultsSubsys.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_factorydefaultsBgasched.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_factorydefaultsBgasched(c)
                            else factorydefaults.bvt_factorydefaultsBgasched.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_factorydefaultsService.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_factorydefaultsService(c)
                            else factorydefaults.bvt_factorydefaultsService.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_factorydefaultsWebserver.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_factorydefaultsWebserver(c)
                            else factorydefaults.bvt_factorydefaultsWebserver.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_factorydefaultsSnmp.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_factorydefaultsSnmp(c)
                            else factorydefaults.bvt_factorydefaultsSnmp.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_factorydefaultsEmail.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_factorydefaultsEmail(c)
                            else factorydefaults.bvt_factorydefaultsEmail.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_factorydefaultsNtp.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_factorydefaultsNtp(c)
                            else factorydefaults.bvt_factorydefaultsNtp.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_factorydefaultsUser.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_factorydefaultsUser(c)
                            else factorydefaults.bvt_factorydefaultsUser.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_factorydefaultsUps.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_factorydefaultsUps(c)
                            else factorydefaults.bvt_factorydefaultsUps.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_factorydefaultsSyslog.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_factorydefaultsSyslog(c)
                            else factorydefaults.bvt_factorydefaultsSyslog.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_verifyFactorydefaultsHelp.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_verifyFactorydefaultsHelp(c)
                            else factorydefaults.bvt_verifyFactorydefaultsHelp.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_verifyFactorydefaultsInvalidOption.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_verifyFactorydefaultsInvalidOption(c)
                            else factorydefaults.bvt_verifyFactorydefaultsInvalidOption.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_verifyFactorydefaultsInvalidParameters.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_verifyFactorydefaultsInvalidParameters(c)
                            else factorydefaults.bvt_verifyFactorydefaultsInvalidParameters.__name__ + ":" + 'True')
        Failflaglist.append(factorydefaults.bvt_verifyFactorydefaultsMissingParameters.__name__ + ":" + 'False'
                            if not factorydefaults.bvt_verifyFactorydefaultsMissingParameters(c)
                            else factorydefaults.bvt_verifyFactorydefaultsMissingParameters.__name__ + ":" + 'True')

        tolog("Start verifying fc")
        import fc
        Failflaglist.append(fc.bvt_verifyFc.__name__ + ":" + 'False'
                            if not fc.bvt_verifyFc(c)
                            else fc.bvt_verifyFc.__name__ + ":" + 'True')
        Failflaglist.append(fc.bvt_verifyFcList.__name__ + ":" + 'False'
                            if not fc.bvt_verifyFcList(c)
                            else fc.bvt_verifyFcList.__name__ + ":" + 'True')
        Failflaglist.append(fc.bvt_verifyFcListV.__name__ + ":" + 'False'
                            if not fc.bvt_verifyFcListV(c)
                            else fc.bvt_verifyFcListV.__name__ + ":" + 'True')
        Failflaglist.append(fc.bvt_verifyFcMod.__name__ + ":" + 'False'
                            if not fc.bvt_verifyFcMod(c)
                            else fc.bvt_verifyFcMod.__name__ + ":" + 'True')
        Failflaglist.append(fc.bvt_verifyFcReset.__name__ + ":" + 'False'
                            if not fc.bvt_verifyFcReset(c)
                            else fc.bvt_verifyFcReset.__name__ + ":" + 'True')
        Failflaglist.append(fc.bvt_verifyFcClear.__name__ + ":" + 'False'
                            if not fc.bvt_verifyFcClear(c)
                            else fc.bvt_verifyFcClear.__name__ + ":" + 'True')
        Failflaglist.append(fc.bvt_verifyFcInvalidOption.__name__ + ":" + 'False'
                            if not fc.bvt_verifyFcInvalidOption(c)
                            else fc.bvt_verifyFcInvalidOption.__name__ + ":" + 'True')
        Failflaglist.append(fc.bvt_verifyFcInvalidParameters.__name__ + ":" + 'False'
                            if not fc.bvt_verifyFcInvalidParameters(c)
                            else fc.bvt_verifyFcInvalidParameters.__name__ + ":" + 'True')
        Failflaglist.append(fc.bvt_verifyFcMissingParameters.__name__ + ":" + 'False'
                            if not fc.bvt_verifyFcMissingParameters(c)
                            else fc.bvt_verifyFcMissingParameters.__name__ + ":" + 'True')


        tolog("Start verifying help")
        import help
        Failflaglist.append(help.bvt_verifyHelp(c))

        tolog("Start verifying initiator")
        import initiator
        Failflaglist.append(initiator.bvt_verifyInitiatorAdd.__name__ + ":" + 'False'
                            if not initiator.bvt_verifyInitiatorAdd(c)
                            else initiator.bvt_verifyInitiatorAdd.__name__ + ":" + 'True')
        Failflaglist.append(initiator.bvt_verifyInitiator.__name__ + ":" + 'False'
                            if not initiator.bvt_verifyInitiator(c)
                            else initiator.bvt_verifyInitiator.__name__ + ":" + 'True')
        Failflaglist.append(initiator.bvt_verifyInitiatorList.__name__ + ":" + 'False'
                            if not initiator.bvt_verifyInitiatorList(c)
                            else initiator.bvt_verifyInitiatorList.__name__ + ":" + 'True')
        Failflaglist.append(initiator.bvt_verifyInitiatorDel.__name__ + ":" + 'False'
                            if not initiator.bvt_verifyInitiatorDel(c)
                            else initiator.bvt_verifyInitiatorDel.__name__ + ":" + 'True')
        Failflaglist.append(initiator.bvt_verifyInitiatorSpecifyInexistentId.__name__ + ":" + 'False'
                            if not initiator.bvt_verifyInitiatorSpecifyInexistentId(c)
                            else initiator.bvt_verifyInitiatorSpecifyInexistentId.__name__ + ":" + 'True')
        Failflaglist.append(initiator.bvt_verifyInitiatorInvalidOption.__name__ + ":" + 'False'
                            if not initiator.bvt_verifyInitiatorInvalidOption(c)
                            else initiator.bvt_verifyInitiatorInvalidOption.__name__ + ":" + 'True')
        Failflaglist.append(initiator.bvt_verifyInitiatorInvalidParameters.__name__ + ":" + 'False'
                            if not initiator.bvt_verifyInitiatorInvalidParameters(c)
                            else initiator.bvt_verifyInitiatorInvalidParameters.__name__ + ":" + 'True')
        Failflaglist.append(initiator.bvt_verifyInitiatorMissingParameters.__name__ + ":" + 'False'
                            if not initiator.bvt_verifyInitiatorMissingParameters(c)
                            else initiator.bvt_verifyInitiatorMissingParameters.__name__ + ":" + 'True')

        tolog("Start verifying iscsi")
        import iscsi
        Failflaglist.append(iscsi.bvt_verifyIscsi.__name__ + ":" + 'False'
                            if not iscsi.bvt_verifyIscsi(c)
                            else iscsi.bvt_verifyIscsi.__name__ + ":" + 'True')
        Failflaglist.append(iscsi.bvt_verifyIscsiList.__name__ + ":" + 'False'
                            if not iscsi.bvt_verifyIscsiList(c)
                            else iscsi.bvt_verifyIscsiList.__name__ + ":" + 'True')
        Failflaglist.append(iscsi.bvt_verifyIscsiAdd.__name__ + ":" + 'False'
                            if not iscsi.bvt_verifyIscsiAdd(c)
                            else iscsi.bvt_verifyIscsiAdd.__name__ + ":" + 'True')
        Failflaglist.append(iscsi.bvt_verifyIscsiMod.__name__ + ":" + 'False'
                            if not iscsi.bvt_verifyIscsiMod(c)
                            else iscsi.bvt_verifyIscsiMod.__name__ + ":" + 'True')
        Failflaglist.append(iscsi.bvt_verifyIscsiDel.__name__ + ":" + 'False'
                            if not iscsi.bvt_verifyIscsiDel(c)
                            else iscsi.bvt_verifyIscsiDel.__name__ + ":" + 'True')
        Failflaglist.append(iscsi.bvt_verifyIscsiInvalidOption.__name__ + ":" + 'False'
                            if not iscsi.bvt_verifyIscsiInvalidOption(c)
                            else iscsi.bvt_verifyIscsiInvalidOption.__name__ + ":" + 'True')
        Failflaglist.append(iscsi.bvt_verifyIscsiInvalidParameters.__name__ + ":" + 'False'
                            if not iscsi.bvt_verifyIscsiInvalidParameters(c)
                            else iscsi.bvt_verifyIscsiInvalidParameters.__name__ + ":" + 'True')
        Failflaglist.append(iscsi.bvt_verifyIscsiMissingParameters.__name__ + ":" + 'False'
                            if not iscsi.bvt_verifyIscsiMissingParameters(c)
                            else iscsi.bvt_verifyIscsiMissingParameters.__name__ + ":" + 'True')

        tolog("Start verifying isns")
        import isns
        Failflaglist.append(isns.bvt_verifyIsns.__name__ + ":" + 'False'
                            if not isns.bvt_verifyIsns(c)
                            else isns.bvt_verifyIsns.__name__ + ":" + 'True')
        Failflaglist.append(isns.bvt_verifyIsnsList.__name__ + ":" + 'False'
                            if not isns.bvt_verifyIsnsList(c)
                            else isns.bvt_verifyIsnsList.__name__ + ":" + 'True')
        Failflaglist.append(isns.bvt_verifyIsnsMod.__name__ + ":" + 'False'
                            if not isns.bvt_verifyIsnsMod(c)
                            else isns.bvt_verifyIsnsMod.__name__ + ":" + 'True')
        Failflaglist.append(isns.bvt_verifyIsnsSpecifyInexistentId.__name__ + ":" + 'False'
                            if not isns.bvt_verifyIsnsSpecifyInexistentId(c)
                            else isns.bvt_verifyIsnsSpecifyInexistentId.__name__ + ":" + 'True')
        Failflaglist.append(isns.bvt_verifyIsnsInvalidOption.__name__ + ":" + 'False'
                            if not isns.bvt_verifyIsnsInvalidOption(c)
                            else isns.bvt_verifyIsnsInvalidOption.__name__ + ":" + 'True')
        Failflaglist.append(isns.bvt_verifyIsnsInvalidParameters.__name__ + ":" + 'False'
                            if not isns.bvt_verifyIsnsInvalidParameters(c)
                            else isns.bvt_verifyIsnsInvalidParameters.__name__ + ":" + 'True')
        Failflaglist.append(isns.bvt_verifyIsnsMissingParameters.__name__ + ":" + 'False'
                            if not isns.bvt_verifyIsnsMissingParameters(c)
                            else isns.bvt_verifyIsnsMissingParameters.__name__ + ":" + 'True')

        tolog("Start verifying logout")
        import logout
        Failflaglist.append(logout.bvt_verifyLogoutInvalidOption.__name__ + ":" + 'False'
                            if not logout.bvt_verifyLogoutInvalidOption(c)
                            else logout.bvt_verifyLogoutInvalidOption.__name__ + ":" + 'True')
        Failflaglist.append(logout.bvt_verifyLogoutInvalidParameters.__name__ + ":" + 'False'
                            if not logout.bvt_verifyLogoutInvalidParameters(c)
                            else logout.bvt_verifyLogoutInvalidParameters.__name__ + ":" + 'True')
        Failflaglist.append(logout.bvt_verifyLogout.__name__ + ":" + 'False'
                            if not logout.bvt_verifyLogout(c)
                            else logout.bvt_verifyLogout.__name__ + ":" + 'True')

        tolog("Start verifying lunmap")
        import lunmap
        Failflaglist.append(lunmap.bvt_verifyLunmapAdd.__name__ + ":" + 'False'
                            if not lunmap.bvt_verifyLunmapAdd(c)
                            else lunmap.bvt_verifyLunmapAdd.__name__ + ":" + 'True')
        Failflaglist.append(lunmap.bvt_verifyLunmap.__name__ + ":" + 'False'
                            if not lunmap.bvt_verifyLunmap(c)
                            else lunmap.bvt_verifyLunmap.__name__ + ":" + 'True')
        Failflaglist.append(lunmap.bvt_verifyLunmapList.__name__ + ":" + 'False'
                            if not lunmap.bvt_verifyLunmapList(c)
                            else lunmap.bvt_verifyLunmapList.__name__ + ":" + 'True')
        Failflaglist.append(lunmap.bvt_verifyLunmapAddlun.__name__ + ":" + 'False'
                            if not lunmap.bvt_verifyLunmapAddlun(c)
                            else lunmap.bvt_verifyLunmapAddlun.__name__ + ":" + 'True')
        Failflaglist.append(lunmap.bvt_verifyLunmapDellun.__name__ + ":" + 'False'
                            if not lunmap.bvt_verifyLunmapDellun(c)
                            else lunmap.bvt_verifyLunmapDellun.__name__ + ":" + 'True')
        Failflaglist.append(lunmap.bvt_verifyLunmapEnable.__name__ + ":" + 'False'
                            if not lunmap.bvt_verifyLunmapEnable(c)
                            else lunmap.bvt_verifyLunmapEnable.__name__ + ":" + 'True')
        Failflaglist.append(lunmap.bvt_verifyLunmapDel.__name__ + ":" + 'False'
                            if not lunmap.bvt_verifyLunmapDel(c)
                            else lunmap.bvt_verifyLunmapDel.__name__ + ":" + 'True')
        Failflaglist.append(lunmap.bvt_verifyLunmapDisable.__name__ + ":" + 'False'
                            if not lunmap.bvt_verifyLunmapDisable(c)
                            else lunmap.bvt_verifyLunmapDisable.__name__ + ":" + 'True')
        Failflaglist.append(lunmap.bvt_verifyLunmapSpecifyInexistentId.__name__ + ":" + 'False'
                            if not lunmap.bvt_verifyLunmapSpecifyInexistentId(c)
                            else lunmap.bvt_verifyLunmapSpecifyInexistentId.__name__ + ":" + 'True')
        Failflaglist.append(lunmap.bvt_verifyLunmapInvalidOption.__name__ + ":" + 'False'
                            if not lunmap.bvt_verifyLunmapInvalidOption(c)
                            else lunmap.bvt_verifyLunmapInvalidOption.__name__ + ":" + 'True')
        Failflaglist.append(lunmap.bvt_verifyLunmapInvalidParameters.__name__ + ":" + 'False'
                            if not lunmap.bvt_verifyLunmapInvalidParameters(c)
                            else lunmap.bvt_verifyLunmapInvalidParameters.__name__ + ":" + 'True')
        Failflaglist.append(lunmap.bvt_verifyLunmapMissingParameters.__name__ + ":" + 'False'
                            if not lunmap.bvt_verifyLunmapMissingParameters(c)
                            else lunmap.bvt_verifyLunmapMissingParameters.__name__ + ":" + 'True')


        tolog("Start verifying NTP")
        import ntp
        Failflaglist.append(ntp.bvt_verifyNtpMod.__name__ + ":" + 'False'
                            if not ntp.bvt_verifyNtpMod(c)
                            else ntp.bvt_verifyNtpMod.__name__ + ":" + 'True')
        Failflaglist.append(ntp.bvt_verifyNtp.__name__ + ":" + 'False'
                            if not ntp.bvt_verifyNtp(c)
                            else ntp.bvt_verifyNtp.__name__ + ":" + 'True')
        Failflaglist.append(ntp.bvt_verifyNtpList.__name__ + ":" + 'False'
                            if not ntp.bvt_verifyNtpList(c)
                            else ntp.bvt_verifyNtpList.__name__ + ":" + 'True')
        Failflaglist.append(ntp.bvt_verifyNtpTest.__name__ + ":" + 'False'
                            if not ntp.bvt_verifyNtpTest(c)
                            else ntp.bvt_verifyNtpTest.__name__ + ":" + 'True')
        Failflaglist.append(ntp.bvt_verifyNtpSync.__name__ + ":" + 'False'
                            if not ntp.bvt_verifyNtpSync(c)
                            else ntp.bvt_verifyNtpSync.__name__ + ":" + 'True')
        Failflaglist.append(ntp.bvt_verifyNtpInvalidOption.__name__ + ":" + 'False'
                            if not ntp.bvt_verifyNtpInvalidOption(c)
                            else ntp.bvt_verifyNtpInvalidOption.__name__ + ":" + 'True')
        Failflaglist.append(ntp.bvt_verifyNtpInvalidParameters.__name__ + ":" + 'False'
                            if not ntp.bvt_verifyNtpInvalidParameters(c)
                            else ntp.bvt_verifyNtpInvalidParameters.__name__ + ":" + 'True')
        Failflaglist.append(ntp.bvt_verifyNtpMissingParameters.__name__ + ":" + 'False'
                            if not ntp.bvt_verifyNtpMissingParameters(c)
                            else ntp.bvt_verifyNtpMissingParameters.__name__ + ":" + 'True')

        tolog("Start verifying password")
        import password
        Failflaglist.append(password.bvt_verifyChangePassword.__name__ + ":" + 'False'
                            if not password.bvt_verifyChangePassword(c)
                            else password.bvt_verifyChangePassword.__name__ + ":" + 'True')
        Failflaglist.append(password.bvt_verifyPasswordSpecifyInexistentUsername.__name__ + ":" + 'False'
                            if not password.bvt_verifyPasswordSpecifyInexistentUsername(c)
                            else password.bvt_verifyPasswordSpecifyInexistentUsername.__name__ + ":" + 'True')
        Failflaglist.append(password.bvt_verifyPasswordInvalidOption.__name__ + ":" + 'False'
                            if not password.bvt_verifyPasswordInvalidOption(c)
                            else password.bvt_verifyPasswordInvalidOption.__name__ + ":" + 'True')
        Failflaglist.append(password.bvt_verifyPasswordInvalidParameters.__name__ + ":" + 'False'
                            if not password.bvt_verifyPasswordInvalidParameters(c)
                            else password.bvt_verifyPasswordInvalidParameters.__name__ + ":" + 'True')
        Failflaglist.append(password.bvt_verifyPasswordMissingParameters.__name__ + ":" + 'False'
                            if not password.bvt_verifyPasswordMissingParameters(c)
                            else password.bvt_verifyPasswordMissingParameters.__name__ + ":" + 'True')


        tolog("Start verifying pcie")
        import pcie
        Failflaglist.append(pcie.bvt_verifyPcie.__name__ + ":" + 'False'
                            if not pcie.bvt_verifyPcie(c)
                            else pcie.bvt_verifyPcie.__name__ + ":" + 'True')
        Failflaglist.append(pcie.bvt_verifyPcielist.__name__ + ":" + 'False'
                            if not pcie.bvt_verifyPcielist(c)
                            else pcie.bvt_verifyPcielist.__name__ + ":" + 'True')
        Failflaglist.append(pcie.bvt_verifyPcieInvalidOption.__name__ + ":" + 'False'
                            if not pcie.bvt_verifyPcieInvalidOption(c)
                            else pcie.bvt_verifyPcieInvalidOption.__name__ + ":" + 'True')
        Failflaglist.append(pcie.bvt_verifyPcieInvalidParameters.__name__ + ":" + 'False'
                            if not pcie.bvt_verifyPcieInvalidParameters(c)
                            else pcie.bvt_verifyPcieInvalidParameters.__name__ + ":" + 'True')
        Failflaglist.append(pcie.bvt_verifyPcieMissingParameters.__name__ + ":" + 'False'
                            if not pcie.bvt_verifyPcieMissingParameters(c)
                            else pcie.bvt_verifyPcieMissingParameters.__name__ + ":" + 'True')


        tolog("Start verifying smart")
        import smart
        Failflaglist.append(smart.bvt_verifySmart.__name__ + ":" + 'False'
                            if not smart.bvt_verifySmart(c)
                            else smart.bvt_verifySmart.__name__ + ":" + 'True')
        Failflaglist.append(smart.bvt_verifySmartV.__name__ + ":" + 'False'
                            if not smart.bvt_verifySmartV(c)
                            else smart.bvt_verifySmartV.__name__ + ":" + 'True')
        Failflaglist.append(smart.bvt_verifySmartList.__name__ + ":" + 'False'
                            if not smart.bvt_verifySmartList(c)
                            else smart.bvt_verifySmartList.__name__ + ":" + 'True')
        Failflaglist.append(smart.bvt_verifySmartEnable.__name__ + ":" + 'False'
                            if not smart.bvt_verifySmartEnable(c)
                            else smart.bvt_verifySmartEnable.__name__ + ":" + 'True')
        Failflaglist.append(smart.bvt_verifySmartDisable.__name__ + ":" + 'False'
                            if not smart.bvt_verifySmartDisable(c)
                            else smart.bvt_verifySmartDisable.__name__ + ":" + 'True')
        Failflaglist.append(smart.bvt_verifySmartHelp.__name__ + ":" + 'False'
                            if not smart.bvt_verifySmartHelp(c)
                            else smart.bvt_verifySmartHelp.__name__ + ":" + 'True')
        Failflaglist.append(smart.bvt_verifySmartSpecifyInexistentId.__name__ + ":" + 'False'
                            if not smart.bvt_verifySmartSpecifyInexistentId(c)
                            else smart.bvt_verifySmartSpecifyInexistentId.__name__ + ":" + 'True')
        Failflaglist.append(smart.bvt_verifySmartInvalidOption.__name__ + ":" + 'False'
                            if not smart.bvt_verifySmartInvalidOption(c)
                            else smart.bvt_verifySmartInvalidOption.__name__ + ":" + 'True')
        Failflaglist.append(smart.bvt_verifySmartInvalidParameters.__name__ + ":" + 'False'
                            if not smart.bvt_verifySmartInvalidParameters(c)
                            else smart.bvt_verifySmartInvalidParameters.__name__ + ":" + 'True')
        Failflaglist.append(smart.bvt_verifySmartMissingParameters.__name__ + ":" + 'False'
                            if not smart.bvt_verifySmartMissingParameters(c)
                            else smart.bvt_verifySmartMissingParameters.__name__ + ":" + 'True')

    else:
        tolog("Failed to connect server after ptiflash.")
        Failflag = True

    for flag in Failflaglist:
        if ':False' in flag:
            tolog("The %s case in BuildVerifiation_Jenkins failed" % flag[:-6])

    if Failflag:
        tolog(Fail)
    else:
        tolog(Pass)


    c.close()
    ssh.close()
if __name__ == "__main__":

    start=time.clock()
    c,ssh=ssh_conn()
    BuildVerification(c)
    c.close()
