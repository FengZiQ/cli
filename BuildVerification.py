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
tftpserver="root@10.84.2.99:/work/tftpboot/"
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

    flashimage=False
    Failflag=False
    count = 0
    Failflaglist = list()
    c, ssh = ssh_conn()

    versioninfo = SendCmd(c, "about")

    currentbuild = versioninfo.split("Version: ")[1][:13]



    tftpbuildnumber=open("/home/work/jackyl/Scripts/clitest/buildnum","r").readline().rstrip()
    print "currentbuild,",currentbuild
    print "tftpbuildnumber,",tftpbuildnumber

    if ("13." in currentbuild and "13." in tftpbuildnumber) and (int(currentbuild.split(".")[-1])<int(tftpbuildnumber.split(".")[-1])) or (
        "12.00" in currentbuild and "12.0" in tftpbuildnumber) and (
        int(currentbuild.split(".")[-1]) < int(tftpbuildnumber.split(".")[-1])) or (
        "12.01" in currentbuild and "12.1" in tftpbuildnumber) and (
        int(currentbuild.split(".")[-1]) < int(tftpbuildnumber.split(".")[-1])) or (
        "12.00" in currentbuild and "12.1" in tftpbuildnumber) or (
        "12.02" in currentbuild and "12.2" in tftpbuildnumber) :
        #filename="d5k-multi-13_0_0000_"+tftpbuildnumber.split(".")[-1]
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
        SendCmdRestart(c,"ptiflash -y -t -s 10.84.2.99 -f "+filename+".ptif")




    if flashimage:
        i=1
        while i< 160:
            # wait for rebooting
           tolog("ptiflash is in progress, please wait, %d seconds elapse" %i)
           i+=1
           sleep(1)

    # check if ssh connection is ok.
    # wait for another 40 seconds
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
            Failflaglist.append(pool.bvtpoolcreateandlist(c,1))
            
            tolog("Start verifying pool global setting")
            Failflaglist.append(pool.bvtpoolglobalsetting(c))

            tolog("Start verifying volume add")
            Failflaglist.append(pool.bvtvolumecreateandlist(c,10))

            tolog("Start verifying snapshot add")
            Failflaglist.append(pool.bvtsnapshotcreateandlist(c,2))

            tolog("Start verifying clone add")
            Failflaglist.append(pool.bvtclonecreateandlist(c,2))


            tolog("Start verifying delete clone")
            Failflaglist.append( pool.bvtclonedelete(c))

            tolog("Start verifying delete snapshot")
            Failflaglist.append( pool.bvtsnapshotdelete(c))

            tolog("Start verifying delete volume")
            Failflaglist.append( pool.bvtvolumedel(c))

            tolog("Start verifying delete pool")
            Failflaglist.append(pool.bvtpooldel(c))


            tolog("Start verifying pool add for a second time")
            Failflaglist.append(pool.bvtpoolcreateandlist(c, 0))

            tolog("Start verifying pool global setting")
            Failflaglist.append(pool.bvtpoolglobalsetting(c))

            tolog("Start verifying volume add many")
            Failflaglist.append(pool.bvtvolumeaddmany(c, 2))

            tolog("Start verifying snapshot add")
            Failflaglist.append(pool.bvtsnapshotcreateandlist(c, 2))

            tolog("Start verifying clone add")
            Failflaglist.append(pool.bvtclonecreateandlist(c, 2))

            tolog("Start verifying clone export/unexport")
            Failflaglist.append(pool.bvtexportunexport(c, "clone"))

            tolog("Start verifying snapshot export/unexport")
            Failflaglist.append(pool.bvtexportunexport(c, "snapshot"))

            tolog("Start verifying volume export/unexport")
            Failflaglist.append(pool.bvtexportunexport(c, "volume"))



            tolog("Start verifying pool force delete")
            Failflaglist.append(pool.bvtforcedel(c, "pool"))


            tolog("Start verifying pool add for 3rd time")
            Failflaglist.append(pool.bvtpoolcreateandlist(c, 2))

            tolog("Start verifying spare add")
            Failflaglist.append(pool.bvtsparedrvcreate(c, 2))

            tolog("Start verifying delete spare")
            Failflaglist.append(pool.bvtsparedelete(c))


            tolog("Start verifying pool extend")
            Failflaglist.append(pool.bvtpoolmodifyandlist(c))

            tolog("Start verifying volume add")
            Failflaglist.append(pool.bvtvolumecreateandlist(c, 10))

            tolog("Start verifying snapshot add")
            Failflaglist.append(pool.bvtsnapshotcreateandlist(c, 2))

            tolog("Start verifying clone add")
            Failflaglist.append(pool.bvtclonecreateandlist(c, 2))

            tolog("Start verifying clone force delete")
            Failflaglist.append(pool.bvtforcedel(c, "clone"))

            tolog("Start verifying snapshot force delete")
            Failflaglist.append(pool.bvtforcedel(c, "snapshot"))

            tolog("Start verifying volume force delete")
            Failflaglist.append(pool.bvtforcedel(c, "volume"))


            Failflaglist.append(pool.bvtforcedel(c, "pool"))

            tolog("Start verifying pool create with all raid level and parameters")
            Failflaglist.append(pool.bvtpoolcreateverify_newraidlevel(c))


            tolog("Start verifying pool output error")
            Failflaglist.append(pool.bvtpoolcreateverifyoutputerror_newraidlevel(c))

            tolog("Start verifying about")
            import about
            Failflaglist.append(about.bvt_verifyAbout(c))
            Failflaglist.append(about.bvt_verifyAboutHelp(c))
            Failflaglist.append(about.bvt_verifyAboutInvalidOption(c))
            Failflaglist.append(about.bvt_verifyAboutInvalidParameters(c))

            tolog("Start verifying battery")
            import battery
            Failflaglist.append(battery.bvt_verifyBattery(c))
            Failflaglist.append(battery.bvt_verifyBatteryList(c))
            Failflaglist.append(battery.bvt_verifyBatteryRecondition(c))
            Failflaglist.append(battery.bvt_verifyBatteryHelp(c))
            Failflaglist.append(battery.bvt_verifyBatterySpecifyInexistentId(c))
            Failflaglist.append(battery.bvt_verifyBatteryInvalidOption(c))
            Failflaglist.append(battery.bvt_verifyBatteryInvalidParameters(c))
            Failflaglist.append(battery.bvt_verifyBatteryMissingParameters(c))

            tolog("Start verifying BBM")
            import bbm
            Failflaglist.append(bbm.bvt_verifyBBM(c))
            Failflaglist.append(bbm.bvt_verifyBBMClear(c))
            Failflaglist.append(bbm.bvt_verifyBBMClearFailedTest(c))
            Failflaglist.append(bbm.bvt_verifyBBMHelp(c))
            Failflaglist.append(bbm.bvt_verifyBBMInvalidOption(c))
            Failflaglist.append(bbm.bvt_verifyBBMInvalidParameters(c))
            Failflaglist.append(bbm.bvt_verifyBBMList(c))
            Failflaglist.append(bbm.bvt_verifyBBMMissingParameters(c))
            Failflaglist.append(bbm.bvt_verifyBBMSpecifyInexistentId(c))

            tolog("Start verifying bga")
            import bga
            Failflaglist.append(bga.bvt_verifyBga(c))
            Failflaglist.append(bga.bvt_verifyBgaList(c))
            Failflaglist.append(bga.bvt_verifyBgaMod(c))
            Failflaglist.append(bga.bvt_verifyBgaHelp(c))
            Failflaglist.append(bga.bvt_verifyBgaInvalidOption(c))
            Failflaglist.append(bga.bvt_verifyBgaInvalidParameters(c))
            Failflaglist.append(bga.bvt_verifyBgaMissingParameters(c))

            tolog("Start verifying buzzer")
            import buzzer
            Failflaglist.append(buzzer.bvt_verifyBuzzerDisableAndSilentTurnOn((c)))
            Failflaglist.append(buzzer.bvt_verifyBuzzerEnableAndSilentTurnOn((c)))
            Failflaglist.append(buzzer.bvt_verifyBuzzerEnableAndSoundingTurnOn((c)))
            Failflaglist.append(buzzer.bvt_verifyBuzzerDisableAndSilentTurnOff((c)))
            Failflaglist.append(buzzer.bvt_verifyBuzzerEnableAndSilentTurnOff((c)))
            Failflaglist.append(buzzer.bvt_verifyBuzzerEnableAndSoundingTurnOff((c)))
            Failflaglist.append(buzzer.bvt_verifyBuzzerDisableAndSilentEnable((c)))
            Failflaglist.append(buzzer.bvt_verifyBuzzerEnableAndSilentEnable((c)))
            Failflaglist.append(buzzer.bvt_verifyBuzzerEnableAndSoundingEnable((c)))
            Failflaglist.append(buzzer.bvt_verifyBuzzerEnableAndSoundingDisable((c)))
            Failflaglist.append(buzzer.bvt_verifyBuzzerEnableAndSilentDisable((c)))
            Failflaglist.append(buzzer.bvt_verifyBuzzerDisableAndSilentDisable((c)))
            Failflaglist.append(buzzer.bvt_verifyBuzzerInfo((c)))
            Failflaglist.append(buzzer.bvt_verifyBuzzerHelp((c)))
            Failflaglist.append(buzzer.bvt_verifyBuzzerInvalidParameters((c)))
            Failflaglist.append(buzzer.bvt_verifyBuzzerInvalidOption((c)))

            tolog("Start verifying chap")
            import chap
            Failflaglist.append(chap.bvt_verifyChapAdd(c))
            Failflaglist.append(chap.bvt_verifyChap(c))
            Failflaglist.append(chap.bvt_verifyChapList(c))
            Failflaglist.append(chap.bvt_verifyChapMod(c))
            Failflaglist.append(chap.bvt_verifyChapDel(c))
            Failflaglist.append(chap.bvt_verifyChapHelp(c))
            Failflaglist.append(chap.bvt_verifyChapSpecifyErrorId(c))
            Failflaglist.append(chap.bvt_verifyChapInvalidOption(c))
            Failflaglist.append(chap.bvt_verifyChapInvalidParameters(c))
            Failflaglist.append(chap.bvt_verifyChapMissingParameters(c))

            import ctrl
            tolog("Start verifying ctrl")
            Failflaglist.append(ctrl.bvt_verifyCtrl(c))
            Failflaglist.append(ctrl.bvt_verifyCtrlSpecifyId(c))
            Failflaglist.append(ctrl.bvt_verifyCtrlSpecifyInexistentId(c))
            Failflaglist.append(ctrl.bvt_verifyCtrlList(c))
            Failflaglist.append(ctrl.bvt_verifyCtrlV(c))
            Failflaglist.append(ctrl.bvt_verifyCtrlListV(c))
            Failflaglist.append(ctrl.bvt_verifyCtrlModNormativeAlias(c))
            Failflaglist.append(ctrl.bvt_verifyCtrlModValuesIsEnableOrDisable(c))
            Failflaglist.append(ctrl.bvt_verifyCtrlModValuesIsTime(c))
            Failflaglist.append(ctrl.bvt_verifyCtrlClear(c))
            Failflaglist.append(ctrl.bvt_verifyCtrlHelp(c))
            Failflaglist.append(ctrl.bvt_verifyCtrlInvalidOption(c))
            Failflaglist.append(ctrl.bvt_verifyCtrlInvalidParameters(c))
            Failflaglist.append(ctrl.bvt_verifyCtrlMissingParameters(c))
            Failflaglist.append(ctrl.bvt_verifyCtrlSpecifyInexistentId(c))

            tolog("Start verifying encldiag")
            import encldiag
            Failflaglist.append(encldiag.bvt_verifyEncldiag(c))
            Failflaglist.append(encldiag.bvt_verifyEncldiagList(c))
            Failflaglist.append(encldiag.bvt_verifyEncldiagHelp(c))
            Failflaglist.append(encldiag.bvt_verifyEncldiagSpecifyInexistentId(c))
            Failflaglist.append(encldiag.bvt_verifyEncldiagInvalidOption(c))
            Failflaglist.append(encldiag.bvt_verifyEncldiagInvalidParameters(c))
            Failflaglist.append(encldiag.bvt_verifyEncldiagMissingParameters(c))

            tolog("Start verifying enclosure")
            import enclosure
            Failflaglist.append(enclosure.bvt_verifyEnclosure(c))
            Failflaglist.append(enclosure.bvt_verifyEnclosureList(c))
            Failflaglist.append(enclosure.bvt_verifyEnclosureMod(c))
            Failflaglist.append(enclosure.bvt_verifyEnclosureLocate(c))
            Failflaglist.append(enclosure.bvt_verifyEnclosureHelp(c))
            Failflaglist.append(enclosure.bvt_verifEnclosureSpecifyInexistentId(c))
            Failflaglist.append(enclosure.bvt_verifyEnclosureInvalidOption(c))
            Failflaglist.append(enclosure.bvt_verifyEnclosureInvalidParameters(c))
            Failflaglist.append(enclosure.bvt_verifyEnclosureMissingParameters(c))

            tolog("Start verifying event")
            import event
            Failflaglist.append(event.bvt_verifyEvent(c))
            Failflaglist.append(event.bvt_verifyEventList(c))
            Failflaglist.append(event.bvt_verifyEventClear(c))
            Failflaglist.append(event.bvt_verifyEventHelp(c))
            Failflaglist.append(event.bvt_verifEventSpecifyInexistentId(c))
            Failflaglist.append(event.bvt_verifyEventInvalidOption(c))
            Failflaglist.append(event.bvt_verifyEventInvalidParameters(c))
            Failflaglist.append(event.bvt_verifyEventMissingParameters(c))

            tolog("Start verifying factorydefaults")
            import factorydefaults
            Failflaglist.append(factorydefaults.bvt_factorydefaultsBga(c))
            Failflaglist.append(factorydefaults.bvt_factorydefaultsCtrl(c))
            Failflaglist.append(factorydefaults.bvt_factorydefaultsEncl(c))
            Failflaglist.append(factorydefaults.bvt_factorydefaultsFc(c))
            Failflaglist.append(factorydefaults.bvt_factorydefaultsIscsi(c))
            Failflaglist.append(factorydefaults.bvt_factorydefaultsPhydrv(c))
            Failflaglist.append(factorydefaults.bvt_factorydefaultsSas(c))
            Failflaglist.append(factorydefaults.bvt_factorydefaultsScsi(c))
            Failflaglist.append(factorydefaults.bvt_factorydefaultsSubsys(c))
            Failflaglist.append(factorydefaults.bvt_factorydefaultsBgasched(c))
            Failflaglist.append(factorydefaults.bvt_factorydefaultsService(c))
            Failflaglist.append(factorydefaults.bvt_factorydefaultsWebserver(c))
            Failflaglist.append(factorydefaults.bvt_factorydefaultsSnmp(c))
            Failflaglist.append(factorydefaults.bvt_factorydefaultsSsh(c))
            Failflaglist.append(factorydefaults.bvt_factorydefaultsEmail(c))
            Failflaglist.append(factorydefaults.bvt_factorydefaultsNtp(c))
            Failflaglist.append(factorydefaults.bvt_factorydefaultsUser(c))
            Failflaglist.append(factorydefaults.bvt_factorydefaultsUps(c))
            Failflaglist.append(factorydefaults.bvt_factorydefaultsSyslog(c))
            Failflaglist.append(factorydefaults.bvt_verifyFactorydefaultsHelp(c))
            Failflaglist.append(factorydefaults.bvt_verifyFactorydefaultsInvalidOption(c))
            Failflaglist.append(factorydefaults.bvt_verifyFactorydefaultsInvalidParameters(c))
            Failflaglist.append(factorydefaults.bvt_verifyFactorydefaultsMissingParameters(c))

            tolog("Start verifying fc")
            import fc
            Failflaglist.append(fc.bvt_verifyFc(c))
            Failflaglist.append(fc.bvt_verifyFcList(c))
            Failflaglist.append(fc.bvt_verifyFcListV(c))
            Failflaglist.append(fc.bvt_verifyFcMod(c))
            Failflaglist.append(fc.bvt_verifyFcReset(c))
            Failflaglist.append(fc.bvt_verifyFcClear(c))
            Failflaglist.append(fc.bvt_verifyFcInvalidOption(c))
            Failflaglist.append(fc.bvt_verifyFcInvalidParameters(c))
            Failflaglist.append(fc.bvt_verifyFcMissingParameters(c))

            tolog("Start verifying help")
            import help
            Failflaglist.append(help.bvt_verifyHelp(c))

            tolog("Start verifying initiator")
            import initiator
            Failflaglist.append(initiator.bvt_verifyInitiatorAdd(c))
            Failflaglist.append(initiator.bvt_verifyInitiator(c))
            Failflaglist.append(initiator.bvt_verifyInitiatorList(c))
            Failflaglist.append(initiator.bvt_verifyInitiatorDel(c))
            Failflaglist.append(initiator.bvt_verifyInitiatorSpecifyInexistentId(c))
            Failflaglist.append(initiator.bvt_verifyInitiatorInvalidOption(c))
            Failflaglist.append(initiator.bvt_verifyInitiatorInvalidParameters(c))
            Failflaglist.append(initiator.bvt_verifyInitiatorMissingParameters(c))

            tolog("Start verifying iscsi")
            import iscsi
            Failflaglist.append(iscsi.bvt_verifyIscsi(c))
            Failflaglist.append(iscsi.bvt_verifyIscsiList(c))
            Failflaglist.append(iscsi.bvt_verifyIscsiAdd(c))
            Failflaglist.append(iscsi.bvt_verifyIscsiMod(c))
            Failflaglist.append(iscsi.bvt_verifyIscsiDel(c))
            Failflaglist.append(iscsi.bvt_verifyIscsiSpecifyInexistentId(c))
            Failflaglist.append(iscsi.bvt_verifyIscsiInvalidOption(c))
            Failflaglist.append(iscsi.bvt_verifyIscsiInvalidParameters(c))
            Failflaglist.append(iscsi.bvt_verifyIscsiMissingParameters(c))

            tolog("Start verifying isns")
            import isns
            Failflaglist.append(isns.bvt_verifyIsns(c))
            Failflaglist.append(isns.bvt_verifyIsnsList(c))
            Failflaglist.append(isns.bvt_verifyIsnsMod(c))
            Failflaglist.append(isns.bvt_verifyIsnsSpecifyInexistentId(c))
            Failflaglist.append(isns.bvt_verifyIsnsInvalidOption(c))
            Failflaglist.append(isns.bvt_verifyIsnsInvalidParameters(c))
            Failflaglist.append(isns.bvt_verifyIsnsMissingParameters(c))

            tolog("Start verifying logout")
            import logout
            Failflaglist.append(logout.bvt_verifyLogoutInvalidOption(c))
            Failflaglist.append(logout.bvt_verifyLogoutInvalidParameters(c))
            Failflaglist.append(logout.bvt_verifyLogout(c))

            tolog("Start verifying lunmap")
            import lunmap
            Failflaglist.append(lunmap.bvt_verifyLunmapAdd(c))
            Failflaglist.append(lunmap.bvt_verifyLunmap(c))
            Failflaglist.append(lunmap.bvt_verifyLunmapList(c))
            Failflaglist.append(lunmap.bvt_verifyLunmapAddlun(c))
            Failflaglist.append(lunmap.bvt_verifyLunmapDellun(c))
            Failflaglist.append(lunmap.bvt_verifyLunmapEnable(c))
            Failflaglist.append(lunmap.bvt_verifyLunmapDel(c))
            Failflaglist.append(lunmap.bvt_verifyLunmapDisable(c))
            Failflaglist.append(lunmap.bvt_verifyLunmapSpecifyInexistentId(c))
            Failflaglist.append(lunmap.bvt_verifyLunmapInvalidOption(c))
            Failflaglist.append(lunmap.bvt_verifyLunmapInvalidParameters(c))
            Failflaglist.append(lunmap.bvt_verifyLunmapMissingParameters(c))

            tolog("Start verifying ntp")
            import ntp
            Failflaglist.append(ntp.bvt_verifyNtpMod(c))
            Failflaglist.append(ntp.bvt_verifyNtp(c))
            Failflaglist.append(ntp.bvt_verifyNtpList(c))
            Failflaglist.append(ntp.bvt_verifyNtpTest(c))
            Failflaglist.append(ntp.bvt_verifyNtpSync(c))
            Failflaglist.append(ntp.bvt_verifyNtpInvalidOption(c))
            Failflaglist.append(ntp.bvt_verifyNtpInvalidParameters(c))
            Failflaglist.append(ntp.bvt_verifyNtpMissingParameters(c))

            tolog("Start verifying password")
            import password
            Failflaglist.append(password.bvt_verifyChangePassword(c))
            Failflaglist.append(password.bvt_verifyPasswordSpecifyInexistentUsername(c))
            Failflaglist.append(password.bvt_verifyPasswordInvalidOption(c))
            Failflaglist.append(password.bvt_verifyPasswordInvalidParameters(c))
            Failflaglist.append(password.bvt_verifyPasswordMissingParameters(c))

            tolog("Start verifying pcie")
            import pcie
            Failflaglist.append(pcie.bvt_verifyPcie(c))
            Failflaglist.append(pcie.bvt_verifyPcielist(c))
            Failflaglist.append(pcie.bvt_verifyPcieInvalidOption(c))
            Failflaglist.append(pcie.bvt_verifyPcieInvalidParameters(c))
            Failflaglist.append(pcie.bvt_verifyPcieMissingParameters(c))

            tolog("Start verifying smart")
            import smart
            Failflaglist.append(smart.bvt_verifySmart(c))
            Failflaglist.append(smart.bvt_verifySmartV(c))
            Failflaglist.append(smart.bvt_verifySmartList(c))
            Failflaglist.append(smart.bvt_verifySmartEnable(c))
            Failflaglist.append(smart.bvt_verifySmartDisable(c))
            Failflaglist.append(smart.bvt_verifySmartHelp(c))
            Failflaglist.append(smart.bvt_verifySmartSpecifyInexistentId(c))
            Failflaglist.append(smart.bvt_verifySmartInvalidOption(c))
            Failflaglist.append(smart.bvt_verifySmartInvalidParameters(c))
            Failflaglist.append(smart.bvt_verifySmartMissingParameters(c))

        else:
            tolog("Failed to connect server after ptiflash.")
            Failflaglist.append(True)

        for flag in Failflaglist:
            if flag == False:
                # Failflag = True
                count += 1
            else:
                Failflag = True

                tolog("The %d case in BuildVerifiation failed" % (count + 1))

        if Failflag:
            tolog(Fail)
        else:
            tolog(Pass)
    else:
        tolog("no new build is availlable.")
        tolog(Pass)

    c.close()
def About(c):
    SendCmd(c,"about")
    tolog(Pass)
if __name__ == "__main__":

    start=time.clock()
    c,ssh=ssh_conn()
    BuildVerification(c)
    c.close()
