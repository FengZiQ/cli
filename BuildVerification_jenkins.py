# coding=utf-8

from time import sleep
from send_cmd import *
from ssh_connect import *
from to_log import *


def ptb_jenkins():

    mark = False

    # To check whether the sw is compiled successfully
    # size = os.path.getsize('/var/lib/jenkins/workspace/Hyperion-DS_Hulda/sw.log')
    size = os.path.getsize('/var/lib/jenkins/workspace/HyperionDS/sw.log')
    if size < 2000000:
        tolog('sw compiles failure')
        exit(1)

    c,ssh = ssh_conn()

    import glob

    files = glob.glob("/var/lib/jenkins/workspace/HyperionDS/build/build/*.ptif")
    # files = glob.glob("/var/lib/jenkins/workspace/Hyperion-DS_Hulda/build/build/*.ptif")

    for file in files:

        # filename = file.replace("/var/lib/jenkins/workspace/Hyperion-DS_Hulda/build/build/","")
        filename = file.replace("/var/lib/jenkins/workspace/HyperionDS/build/build/", "")

        result = SendCmdRestart(c, "ptiflash -y -t -s 10.84.2.99 -f " + filename)

        if "Error (" not in result:
            i = 1
            while i < 50:
                # wait for rebooting
                tolog("installation is in progress, please wait, %d seconds elapse" % (i * 4))
                i += 1
                sleep(4)

            # check if ssh connection is ok.
            # wait for another 120 seconds
            for x in range(30):
                try:
                    c, ssh = ssh_conn()
                    mark = True
                    break
                except Exception, e:
                    print e
                    sleep(4)
        else:
            tolog(result)

    return mark


def ptt_jenkins():

    mark = False
    target_release = open('/home/work/zach/clitest/target_release.txt', 'r')
    build_name = target_release.readline()
    target_release.close()

    if build_name:
        c, ssh = ssh_conn()

        result = SendCmdRestart(c, "ptiflash -y -t -s 10.84.2.99 -f " + build_name)

        if "Error (" not in result:
            i = 1
            while i < 50:
                # wait for rebooting
                tolog("ptiflash is in progress, please wait, %d seconds elapse" % (i * 4))
                i += 1
                sleep(4)

            # check if ssh connection is ok.
            # wait for another 120 seconds
            for x in range(30):
                try:
                    c, ssh = ssh_conn()
                    mark = True
                    break
                except Exception, e:
                    print e
                    sleep(4)
        else:
            tolog(result)

    return mark


def build_verification(c):

    failed_cases = []

    reconnect_flag = False

    if ptt_jenkins():
        reconnect_flag = True

    else:
        if ptb_jenkins():
            reconnect_flag = True
        else:
            tolog('\n new release installation is failed\n ')

    if reconnect_flag:
        c, ssh = ssh_conn()
        # there are 50 command that can be tested
        tolog("Start verifying pool add")
        import pool
        if (pool.add_pool_by_external_drive(c)):
            failed_cases.append('The case ' + pool.add_pool_by_external_drive.__name__ + ' failed')
        if (pool.add_pool_raid0(c)):
            failed_cases.append('The case ' + pool.add_pool_raid0.__name__ + ' failed')
        if (pool.add_pool_raid1(c)):
            failed_cases.append('The case ' + pool.add_pool_raid1.__name__ + ' failed')
        if (pool.add_pool_raid5(c)):
            failed_cases.append('The case ' + pool.add_pool_raid5.__name__ + ' failed')
        if (pool.add_pool_raid6(c)):
            failed_cases.append('The case ' + pool.add_pool_raid6.__name__ + ' failed')
        if (pool.add_pool_raid10(c)):
            failed_cases.append('The case ' + pool.add_pool_raid10.__name__ + ' failed')
        if (pool.add_pool_raid50(c)):
            failed_cases.append('The case ' + pool.add_pool_raid50.__name__ + ' failed')
        if (pool.add_pool_raid60(c)):
            failed_cases.append('The case ' + pool.add_pool_raid60.__name__ + ' failed')
        if (pool.add_pool_default_setting(c)):
            failed_cases.append('The case ' + pool.add_pool_default_setting.__name__ + ' failed')
        if (pool.modify_pool_name(c)):
            failed_cases.append('The case ' + pool.modify_pool_name.__name__ + ' failed')
        if (pool.list_pool(c)):
            failed_cases.append('The case ' + pool.list_pool.__name__ + ' failed')
        if (pool.list_verbose_mode_pool(c)):
            failed_cases.append('The case ' + pool.list_verbose_mode_pool.__name__ + ' failed')
        if (pool.expand_raid0_pool(c)):
            failed_cases.append('The case ' + pool.expand_raid0_pool.__name__ + ' failed')
        if (pool.expand_raid1_pool(c)):
            failed_cases.append('The case ' + pool.expand_raid1_pool.__name__ + ' failed')
        if (pool.expand_raid5_pool(c)):
            failed_cases.append('The case ' + pool.expand_raid5_pool.__name__ + ' failed')
        if (pool.expand_raid6_pool(c)):
            failed_cases.append('The case ' + pool.expand_raid6_pool.__name__ + ' failed')
        if (pool.expand_raid10_pool(c)):
            failed_cases.append('The case ' + pool.expand_raid10_pool.__name__ + ' failed')
        if (pool.expand_raid50_pool(c)):
            failed_cases.append('The case ' + pool.expand_raid50_pool.__name__ + ' failed')
        if (pool.expand_raid60_pool(c)):
            failed_cases.append('The case ' + pool.expand_raid60_pool.__name__ + ' failed')
        if (pool.delete_pool(c)):
            failed_cases.append('The case ' + pool.delete_pool.__name__ + ' failed')
        if (pool.invalid_settings_parameter(c)):
            failed_cases.append('The case ' + pool.invalid_settings_parameter.__name__ + ' failed')
        if (pool.invalid_option(c)):
            failed_cases.append('The case ' + pool.invalid_option.__name__ + ' failed')
        if (pool.missing_parameter(c)):
            failed_cases.append('The case ' + pool.missing_parameter.__name__ + ' failed')

        tolog('Start verifying volume')
        import volume
        if (volume.addVolume(c)):
            failed_cases.append('The case ' + volume.addVolume.__name__ + ' failed')
        if (volume.listVolume(c)):
            failed_cases.append('The case ' + volume.listVolume.__name__ + ' failed')
        if (volume.listVolume_by_verbose_mode(c)):
            failed_cases.append('The case ' + volume.listVolume_by_verbose_mode.__name__ + ' failed')
        if (volume.modVolume(c)):
            failed_cases.append('The case ' + volume.modVolume.__name__ + ' failed')
        if (volume.exportVolume(c)):
            failed_cases.append('The case ' + volume.exportVolume.__name__ + ' failed')
        if (volume.unexportVolume(c)):
            failed_cases.append('The case ' + volume.unexportVolume.__name__ + ' failed')
        if (volume.invalidParameter(c)):
            failed_cases.append('The case ' + volume.invalidParameter.__name__ + ' failed')
        if (volume.invalidOption(c)):
            failed_cases.append('The case ' + volume.invalidOption.__name__ + ' failed')
        if (volume.missingParameter(c)):
            failed_cases.append('The case ' + volume.missingParameter.__name__ + ' failed')
        if (volume.deleteVolume(c)):
            failed_cases.append('The case ' + volume.deleteVolume.__name__ + ' failed')

        tolog('Start verifying NASShare')
        import nasShare
        if (nasShare.addNASShare(c)):
            failed_cases.append('The case ' + nasShare.addNASShare.__name__ + ' failed')
        if (nasShare.listNASShare(c)):
            failed_cases.append('The case ' + nasShare.listNASShare.__name__ + ' failed')
        if (nasShare.listVerboseNASShare(c)):
            failed_cases.append('The case ' + nasShare.listVerboseNASShare.__name__ + ' failed')
        if (nasShare.modNASShare(c)):
            failed_cases.append('The case ' + nasShare.modNASShare.__name__ + ' failed')
        if (nasShare.mountNASShare(c)):
            failed_cases.append('The case ' + nasShare.mountNASShare.__name__ + ' failed')
        if (nasShare.unmountNASShare(c)):
            failed_cases.append('The case ' + nasShare.unmountNASShare.__name__ + ' failed')
        if (nasShare.helpNASShare(c)):
            failed_cases.append('The case ' + nasShare.helpNASShare.__name__ + ' failed')
        if (nasShare.failedTest_InexistentId(c)):
            failed_cases.append('The case ' + nasShare.failedTest_InexistentId.__name__ + ' failed')
        if (nasShare.failedTest_InvalidOption(c)):
            failed_cases.append('The case ' + nasShare.failedTest_InvalidOption.__name__ + ' failed')
        if (nasShare.failedTest_InvalidParameters(c)):
            failed_cases.append('The case ' + nasShare.failedTest_InvalidParameters.__name__ + ' failed')
        if (nasShare.failedTest_MissingParameters(c)):
            failed_cases.append('The case ' + nasShare.failedTest_MissingParameters.__name__ + ' failed')
        if (nasShare.deleteNASShare(c)):
            failed_cases.append('The case ' + nasShare.deleteNASShare.__name__ + ' failed')

        tolog('Start verifying snapshot')
        import snapshot
        if (snapshot.add_snapshot(c)):
            failed_cases.append('The case ' + snapshot.add_snapshot.__name__ + ' failed')
        if (snapshot.list_snapshot(c)):
            failed_cases.append('The case ' + snapshot.list_snapshot.__name__ + ' failed')
        if (snapshot.list_snapshot_by_verbose_mode(c)):
            failed_cases.append('The case ' + snapshot.list_snapshot_by_verbose_mode.__name__ + ' failed')
        if (snapshot.mod_snapshot(c)):
            failed_cases.append('The case ' + snapshot.mod_snapshot.__name__ + ' failed')
        if (snapshot.export_unexport_snapshot(c)):
            failed_cases.append('The case ' + snapshot.export_unexport_snapshot.__name__ + ' failed')
        if (snapshot.mount_umount_snapshot(c)):
            failed_cases.append('The case ' + snapshot.mount_umount_snapshot.__name__ + ' failed')
        if (snapshot.rollback_snapshot(c)):
            failed_cases.append('The case ' + snapshot.rollback_snapshot.__name__ + ' failed')
        if (snapshot.del_snapshot(c)):
            failed_cases.append('The case ' + snapshot.del_snapshot.__name__ + ' failed')
        if (snapshot.invalid_setting_parameter(c)):
            failed_cases.append('The case ' + snapshot.invalid_setting_parameter.__name__ + ' failed')
        if (snapshot.invalid_option(c)):
            failed_cases.append('The case ' + snapshot.invalid_option.__name__ + ' failed')
        if (snapshot.missing_parameter(c)):
            failed_cases.append('The case ' + snapshot.missing_parameter.__name__ + ' failed')

        tolog('Start verifying clone')
        import clone
        if (clone.add_clone(c)):
            failed_cases.append('The case ' + clone.add_clone.__name__ + ' failed')
        if (clone.list_clone(c)):
            failed_cases.append('The case ' + clone.list_clone.__name__ + ' failed')
        if (clone.list_clone_verbose_mode(c)):
            failed_cases.append('The case ' + clone.list_clone_verbose_mode.__name__ + ' failed')
        if (clone.mod_clone(c)):
            failed_cases.append('The case ' + clone.mod_clone.__name__ + ' failed')
        if (clone.export_unexport_clone(c)):
            failed_cases.append('The case ' + clone.export_unexport_clone.__name__ + ' failed')
        if (clone.mount_umount_clone(c)):
            failed_cases.append('The case ' + clone.mount_umount_clone.__name__ + ' failed')
        if (clone.del_clone(c)):
            failed_cases.append('The case ' + clone.del_clone.__name__ + ' failed')
        if (clone.invalid_setting_parameter(c)):
            failed_cases.append('The case ' + clone.invalid_setting_parameter.__name__ + ' failed')
        if (clone.invalid_option(c)):
            failed_cases.append('The case ' + clone.invalid_option.__name__ + ' failed')
        if (clone.missing_parameter(c)):
            failed_cases.append('The case ' + clone.missing_parameter.__name__ + ' failed')

        tolog('Start verifying replication')
        import replication
        if (replication.start_replication(c)):
            failed_cases.append('The case ' + replication.start_replication.__name__ + ' failed')
        if (replication.forbidden_action(c)):
            failed_cases.append('The case ' + replication.forbidden_action.__name__ + ' failed')
        if (replication.sync_source_attribute(c)):
            failed_cases.append('The case ' + replication.sync_source_attribute.__name__ + ' failed')
        if (replication.list_replication(c)):
            failed_cases.append('The case ' + replication.list_replication.__name__ + ' failed')
        if (replication.list_replication_by_verbose(c)):
            failed_cases.append('The case ' + replication.list_replication_by_verbose.__name__ + ' failed')
        if (replication.stop_replication(c)):
            failed_cases.append('The case ' + replication.stop_replication.__name__ + ' failed')
        if (replication.pause_replication(c)):
            failed_cases.append('The case ' + replication.pause_replication.__name__ + ' failed')
        if (replication.resume_replication(c)):
            failed_cases.append('The case ' + replication.resume_replication.__name__ + ' failed')
        if (replication.help_replication(c)):
            failed_cases.append('The case ' + replication.help_replication.__name__ + ' failed')
        if (replication.invalid_setting_for_replication(c)):
            failed_cases.append('The case ' + replication.invalid_setting_for_replication.__name__ + ' failed')
        if (replication.invalid_option_for_replication(c)):
            failed_cases.append('The case ' + replication.invalid_option_for_replication.__name__ + ' failed')
        if (replication.missing_parameter_replication(c)):
            failed_cases.append('The case ' + replication.missing_parameter_replication.__name__ + ' failed')

        tolog('Start verifying spare')
        import spare
        if (spare.add_global_spare(c)):
            failed_cases.append('The case ' + spare.add_global_spare.__name__ + ' failed')
        if (spare.add_dedicated_spare(c)):
            failed_cases.append('The case ' + spare.add_dedicated_spare.__name__ + ' failed')
        if (spare.list_spare(c)):
            failed_cases.append('The case ' + spare.list_spare.__name__ + ' failed')
        if (spare.list_spare_by_verbose_mode(c)):
            failed_cases.append('The case ' + spare.list_spare_by_verbose_mode.__name__ + ' failed')
        if (spare.delete_spare(c)):
            failed_cases.append('The case ' + spare.delete_spare.__name__ + ' failed')
        if (spare.invalid_parameter_for_spare(c)):
            failed_cases.append('The case ' + spare.invalid_parameter_for_spare.__name__ + ' failed')
        if (spare.invalid_option_for_spare(c)):
            failed_cases.append('The case ' + spare.invalid_option_for_spare.__name__ + ' failed')
        if (spare.missing_parameter_for_spare(c)):
            failed_cases.append('The case ' + spare.missing_parameter_for_spare.__name__ + ' failed')

        tolog('Start verifying acl')
        import acl
        if (acl.set_acl(c)):
            failed_cases.append('The case ' + acl.set_acl.__name__ + ' failed')
        if (acl.list_acl(c)):
            failed_cases.append('The case ' + acl.list_acl.__name__ + ' failed')
        if (acl.list_acl_by_verbose_mode(c)):
            failed_cases.append('The case ' + acl.list_acl_by_verbose_mode.__name__ + ' failed')
        if (acl.refresh_acl(c)):
            failed_cases.append('The case ' + acl.refresh_acl.__name__ + ' failed')
        if (acl.acl_unset(c)):
            failed_cases.append('The case ' + acl.acl_unset.__name__ + ' failed')
        if (acl.clear_acl(c)):
            failed_cases.append('The case ' + acl.clear_acl.__name__ + ' failed')
        if (acl.cancel_acl(c)):
            failed_cases.append('The case ' + acl.cancel_acl.__name__ + ' failed')
        if (acl.invalid_setting_parameter(c)):
            failed_cases.append('The case ' + acl.invalid_setting_parameter.__name__ + ' failed')
        if (acl.invalid_option(c)):
            failed_cases.append('The case ' + acl.invalid_option.__name__ + ' failed')
        if (acl.missing_parameter(c)):
            failed_cases.append('The case ' + acl.missing_parameter.__name__ + ' failed')

        tolog('Start verifying periodsnap')
        import periodsnap
        if (periodsnap.add_periodsnap(c)):
            failed_cases.append('The case ' + periodsnap.add_periodsnap.__name__ + ' failed')
        if (periodsnap.list_periodsnap(c)):
            failed_cases.append('The case ' + periodsnap.list_periodsnap.__name__ + ' failed')
        if (periodsnap.list_periodsnap_by_verbose_mode(c)):
            failed_cases.append('The case ' + periodsnap.list_periodsnap_by_verbose_mode.__name__ + ' failed')
        if (periodsnap.mod_periodsnap(c)):
            failed_cases.append('The case ' + periodsnap.mod_periodsnap.__name__ + ' failed')
        if (periodsnap.del_periodsnap(c)):
            failed_cases.append('The case ' + periodsnap.del_periodsnap.__name__ + ' failed')
        if (periodsnap.invalid_setting_for_periodsnap(c)):
            failed_cases.append('The case ' + periodsnap.invalid_setting_for_periodsnap.__name__ + ' failed')
        if (periodsnap.invalid_option_for_periodsnap(c)):
            failed_cases.append('The case ' + periodsnap.invalid_option_for_periodsnap.__name__ + ' failed')
        if (periodsnap.missing_parameter_periodsnap(c)):
            failed_cases.append('The case ' + periodsnap.missing_parameter_periodsnap.__name__ + ' failed')

        tolog('Start verifying quota')
        import quota
        if (quota.set_quota(c)):
            failed_cases.append('The case ' + quota.set_quota.__name__ + ' failed')
        if (quota.list_quota(c)):
            failed_cases.append('The case ' + quota.list_quota.__name__ + ' failed')
        if (quota.list_quota_by_verbose_mode(c)):
            failed_cases.append('The case ' + quota.list_quota_by_verbose_mode.__name__ + ' failed')
        if (quota.refresh_quota(c)):
            failed_cases.append('The case ' + quota.refresh_quota.__name__ + ' failed')
        if (quota.cancel_quota(c)):
            failed_cases.append('The case ' + quota.cancel_quota.__name__ + ' failed')
        if (quota.delete_quota(c)):
            failed_cases.append('The case ' + quota.delete_quota.__name__ + ' failed')
        if (quota.invalid_setting_for_quota(c)):
            failed_cases.append('The case ' + quota.invalid_setting_for_quota.__name__ + ' failed')
        if (quota.invalid_option_for_quota(c)):
            failed_cases.append('The case ' + quota.invalid_option_for_quota.__name__ + ' failed')
        if (quota.missing_parameter_for_quota(c)):
            failed_cases.append('The case ' + quota.missing_parameter_for_quota.__name__ + ' failed')

        tolog('Start verifying allowip')
        import allowip
        if (allowip.add_allowip(c)):
            failed_cases.append('The case ' + allowip.add_allowip.__name__ + ' failed')
        if (allowip.list_allowip(c)):
            failed_cases.append('The case ' + allowip.list_allowip.__name__ + ' failed')
        if (allowip.list_allowip_by_verbose_mode(c)):
            failed_cases.append('The case ' + allowip.list_allowip_by_verbose_mode.__name__ + ' failed')
        if (allowip.mod_allowip(c)):
            failed_cases.append('The case ' + allowip.mod_allowip.__name__ + ' failed')
        if (allowip.del_allowip(c)):
            failed_cases.append('The case ' + allowip.del_allowip.__name__ + ' failed')
        if (allowip.invalid_setting_for_allowip(c)):
            failed_cases.append('The case ' + allowip.invalid_setting_for_allowip.__name__ + ' failed')
        if (allowip.invalid_option_for_allowip(c)):
            failed_cases.append('The case ' + allowip.invalid_option_for_allowip.__name__ + ' failed')
        if (allowip.missing_parameter_for_allowip(c)):
            failed_cases.append('The case ' + allowip.missing_parameter_for_allowip.__name__ + ' failed')

        tolog('Start verifying protocol')
        import protocol
        if (protocol.list_all_protocol(c)):
            failed_cases.append('The case ' + protocol.list_all_protocol.__name__ + ' failed')
        if (protocol.list_single_protocol(c)):
            failed_cases.append('The case ' + protocol.list_single_protocol.__name__ + ' failed')
        if (protocol.mod_ftp_protocol(c)):
            failed_cases.append('The case ' + protocol.mod_ftp_protocol.__name__ + ' failed')
        if (protocol.mod_smb_protocol(c)):
            failed_cases.append('The case ' + protocol.mod_smb_protocol.__name__ + ' failed')
        if (protocol.mod_nfs_protocol(c)):
            failed_cases.append('The case ' + protocol.mod_nfs_protocol.__name__ + ' failed')
        if (protocol.reset_all_protocol(c)):
            failed_cases.append('The case ' + protocol.reset_all_protocol.__name__ + ' failed')
        if (protocol.reset_single_protocol(c)):
            failed_cases.append('The case ' + protocol.reset_single_protocol.__name__ + ' failed')
        if (protocol.enable_protocol(c)):
            failed_cases.append('The case ' + protocol.enable_protocol.__name__ + ' failed')
        if (protocol.disable_protocol(c)):
            failed_cases.append('The case ' + protocol.disable_protocol.__name__ + ' failed')
        if (protocol.invalid_setting_parameter(c)):
            failed_cases.append('The case ' + protocol.invalid_setting_parameter.__name__ + ' failed')
        if (protocol.invalid_option(c)):
            failed_cases.append('The case ' + protocol.invalid_option.__name__ + ' failed')
        if (protocol.missing_parameter(c)):
            failed_cases.append('The case ' + protocol.missing_parameter.__name__ + ' failed')

        tolog('Start verifying group')
        import group
        if (group.add_group_and_verify_name(c)):
            failed_cases.append('The case ' + group.add_group_and_verify_name.__name__ + ' failed')
        if (group.add_group_and_user(c)):
            failed_cases.append('The case ' + group.add_group_and_user.__name__ + ' failed')
        if (group.add_user_into_group(c)):
            failed_cases.append('The case ' + group.add_user_into_group.__name__ + ' failed')
        if (group.list_group(c)):
            failed_cases.append('The case ' + group.list_group.__name__ + ' failed')
        if (group.list_group_by_verbose_mode(c)):
            failed_cases.append('The case ' + group.list_group_by_verbose_mode.__name__ + ' failed')
        if (group.modify_group(c)):
            failed_cases.append('The case ' + group.modify_group.__name__ + ' failed')
        if (group.delete_user_from_group(c)):
            failed_cases.append('The case ' + group.delete_user_from_group.__name__ + ' failed')
        if (group.delete_group(c)):
            failed_cases.append('The case ' + group.delete_group.__name__ + ' failed')
        if (group.invalid_setting_for_group(c)):
            failed_cases.append('The case ' + group.invalid_setting_for_group.__name__ + ' failed')
        if (group.invalid_option_for_group(c)):
            failed_cases.append('The case ' + group.invalid_option_for_group.__name__ + ' failed')
        if (group.missing_parameter_for_group(c)):
            failed_cases.append('The case ' + group.missing_parameter_for_group.__name__ + ' failed')

        tolog('Start verifying phydrv')
        import phydrv
        if (phydrv.list_phydrv(c)):
            failed_cases.append('The case ' + phydrv.list_phydrv.__name__ + ' failed')
        if (phydrv.list_phydrv_by_verbose_mode(c)):
            failed_cases.append('The case ' + phydrv.list_phydrv_by_verbose_mode.__name__ + ' failed')
        if (phydrv.mod_phydrv(c)):
            failed_cases.append('The case ' + phydrv.mod_phydrv.__name__ + ' failed')
        if (phydrv.locate_phydrv(c)):
            failed_cases.append('The case ' + phydrv.locate_phydrv.__name__ + ' failed')
        if (phydrv.online_offline_phydrv(c)):
            failed_cases.append('The case ' + phydrv.online_offline_phydrv.__name__ + ' failed')
        if (phydrv.clear_phydrv(c)):
            failed_cases.append('The case ' + phydrv.clear_phydrv.__name__ + ' failed')
        if (phydrv.invalid_setting_parameter(c)):
            failed_cases.append('The case ' + phydrv.invalid_setting_parameter.__name__ + ' failed')
        if (phydrv.invalid_option(c)):
            failed_cases.append('The case ' + phydrv.invalid_option.__name__ + ' failed')
        if (phydrv.missing_parameter(c)):
            failed_cases.append('The case ' + phydrv.missing_parameter.__name__ + ' failed')

        tolog('Start verifying rb')
        import rb
        if (rb.raid1_start_rb(c)):
            failed_cases.append('The case ' + rb.raid1_start_rb.__name__ + ' failed')
        if (rb.raid5_start_rb(c)):
            failed_cases.append('The case ' + rb.raid5_start_rb.__name__ + ' failed')
        if (rb.raid6_start_rb(c)):
            failed_cases.append('The case ' + rb.raid6_start_rb.__name__ + ' failed')
        if (rb.raid10_start_rb(c)):
            failed_cases.append('The case ' + rb.raid10_start_rb.__name__ + ' failed')
        if (rb.raid50_start_rb(c)):
            failed_cases.append('The case ' + rb.raid50_start_rb.__name__ + ' failed')
        if (rb.raid60_start_rb(c)):
            failed_cases.append('The case ' + rb.raid60_start_rb.__name__ + ' failed')
        if (rb.list_rb(c)):
            failed_cases.append('The case ' + rb.list_rb.__name__ + ' failed')
        if (rb.stop_rb(c)):
            failed_cases.append('The case ' + rb.stop_rb.__name__ + ' failed')
        if (rb.invalid_setting_parameter(c)):
            failed_cases.append('The case ' + rb.invalid_setting_parameter.__name__ + ' failed')
        if (rb.invalid_option(c)):
            failed_cases.append('The case ' + rb.invalid_option.__name__ + ' failed')
        if (rb.missing_parameter(c)):
            failed_cases.append('The case ' + rb.missing_parameter.__name__ + ' failed')

        tolog("Start verifying fc")
        import fc
        if (fc.list_fc(c)):
            failed_cases.append('The case ' + fc.list_fc.__name__ + ' failed')
        if (fc.list_fc_by_verbose_mode(c)):
            failed_cases.append('The case ' + fc.list_fc_by_verbose_mode.__name__ + ' failed')
        if (fc.mod_fc(c)):
            failed_cases.append('The case ' + fc.mod_fc.__name__ + ' failed')
        if (fc.reset_fc(c)):
            failed_cases.append('The case ' + fc.reset_fc.__name__ + ' failed')
        if (fc.clear_fc(c)):
            failed_cases.append('The case ' + fc.clear_fc.__name__ + ' failed')
        if (fc.invalid_setting_for_fc(c)):
            failed_cases.append('The case ' + fc.invalid_setting_for_fc.__name__ + ' failed')
        if (fc.invalid_option_for_fc(c)):
            failed_cases.append('The case ' + fc.invalid_option_for_fc.__name__ + ' failed')
        if (fc.missing_parameter_for_fc(c)):
            failed_cases.append('The case ' + fc.missing_parameter_for_fc.__name__ + ' failed')

        tolog("Start verifying iscsi")
        import iscsi
        if (iscsi.add_phy_vlan_portal(c)):
            failed_cases.append('The case ' + iscsi.add_phy_vlan_portal.__name__ + ' failed')
        if (iscsi.list_iscsi(c)):
            failed_cases.append('The case ' + iscsi.list_iscsi.__name__ + ' failed')
        if (iscsi.list_iscsi_by_verbose_mode(c)):
            failed_cases.append('The case ' + iscsi.list_iscsi_by_verbose_mode.__name__ + ' failed')
        if (iscsi.mod_iscsi(c)):
            failed_cases.append('The case ' + iscsi.mod_iscsi.__name__ + ' failed')
        if (iscsi.del_iscsi(c)):
            failed_cases.append('The case ' + iscsi.del_iscsi.__name__ + ' failed')
        if (iscsi.invalid_setting_for_iscsi(c)):
            failed_cases.append('The case ' + iscsi.invalid_setting_for_iscsi.__name__ + ' failed')
        if (iscsi.invalid_option_for_iscsi(c)):
            failed_cases.append('The case ' + iscsi.invalid_option_for_iscsi.__name__ + ' failed')
        if (iscsi.missing_parameter_for_iscsi(c)):
            failed_cases.append('The case ' + iscsi.missing_parameter_for_iscsi.__name__ + ' failed')

        tolog("Start verifying net")
        import net
        if (net.list_net(c)):
            failed_cases.append('The case ' + net.list_net.__name__ + ' failed')
        if (net.list_net_by_verbose_mode(c)):
            failed_cases.append('The case ' + net.list_net_by_verbose_mode.__name__ + ' failed')
        if (net.disable_enable_net(c)):
            failed_cases.append('The case ' + net.disable_enable_net.__name__ + ' failed')
        if (net.modify_net(c)):
            failed_cases.append('The case ' + net.modify_net.__name__ + ' failed')
        if (net.invalid_setting_for_net(c)):
            failed_cases.append('The case ' + net.invalid_setting_for_net.__name__ + ' failed')
        if (net.invalid_option_for_net(c)):
            failed_cases.append('The case ' + net.invalid_option_for_net.__name__ + ' failed')
        if (net.missing_parameter_for_net(c)):
            failed_cases.append('The case ' + net.missing_parameter_for_net.__name__ + ' failed')

        tolog("Start verifying trunk")
        import trunk
        if (trunk.add_io_trunk(c)):
            failed_cases.append('The case ' + trunk.add_io_trunk.__name__ + ' failed')
        if (trunk.add_mgmt_trunk(c)):
            failed_cases.append('The case ' + trunk.add_mgmt_trunk.__name__ + ' failed')
        if (trunk.list_trunk(c)):
            failed_cases.append('The case ' + trunk.list_trunk.__name__ + ' failed')
        if (trunk.mod_trunk(c)):
            failed_cases.append('The case ' + trunk.mod_trunk.__name__ + ' failed')
        if (trunk.del_trunk(c)):
            failed_cases.append('The case ' + trunk.del_trunk.__name__ + ' failed')
        if (trunk.invalid_setting_for_trunk(c)):
            failed_cases.append('The case ' + trunk.invalid_setting_for_trunk.__name__ + ' failed')
        if (trunk.invalid_option_for_trunk(c)):
            failed_cases.append('The case ' + trunk.invalid_option_for_trunk.__name__ + ' failed')
        if (trunk.missing_parameter_for_trunk(c)):
            failed_cases.append('The case ' + trunk.missing_parameter_for_trunk.__name__ + ' failed')

        tolog("Start verifying initiator")
        import initiator
        if (initiator.add_initiator(c)):
            failed_cases.append('The case ' + initiator.add_initiator.__name__ + ' failed')
        if (initiator.list_initiator(c)):
            failed_cases.append('The case ' + initiator.list_initiator.__name__ + ' failed')
        if (initiator.del_initiator(c)):
            failed_cases.append('The case ' + initiator.del_initiator.__name__ + ' failed')
        if (initiator.invalid_setting_for_initiator(c)):
            failed_cases.append('The case ' + initiator.invalid_setting_for_initiator.__name__ + ' failed')
        if (initiator.invalid_option_for_initiator(c)):
            failed_cases.append('The case ' + initiator.invalid_option_for_initiator.__name__ + ' failed')
        if (initiator.missing_parameter_for_initiator(c)):
            failed_cases.append('The case ' + initiator.missing_parameter_for_initiator.__name__ + ' failed')

        tolog("Start verifying lunmap")
        import lunmap
        if (lunmap.enable_lmm(c)):
            failed_cases.append('The case ' + lunmap.enable_lmm.__name__ + ' failed')
        if (lunmap.add_lunmap(c)):
            failed_cases.append('The case ' + lunmap.add_lunmap.__name__ + ' failed')
        if (lunmap.addun_lunmap(c)):
            failed_cases.append('The case ' + lunmap.addun_lunmap.__name__ + ' failed')
        if (lunmap.list_lunmap(c)):
            failed_cases.append('The case ' + lunmap.list_lunmap.__name__ + ' failed')
        if (lunmap.del_lunmap(c)):
            failed_cases.append('The case ' + lunmap.del_lunmap.__name__ + ' failed')
        if (lunmap.dellun_lunmap(c)):
            failed_cases.append('The case ' + lunmap.dellun_lunmap.__name__ + ' failed')
        if (lunmap.disable_lmm(c)):
            failed_cases.append('The case ' + lunmap.disable_lmm.__name__ + ' failed')
        if (lunmap.invalid_setting_for_lunmap(c)):
            failed_cases.append('The case ' + lunmap.invalid_setting_for_lunmap.__name__ + ' failed')
        if (lunmap.invalid_option_for_lunmap(c)):
            failed_cases.append('The case ' + lunmap.invalid_option_for_lunmap.__name__ + ' failed')
        if (lunmap.missing_parameter_for_lunmap(c)):
            failed_cases.append('The case ' + lunmap.missing_parameter_for_lunmap.__name__ + ' failed')

        tolog("Start verifying swmgt")
        import swmgt
        if (swmgt.list_swmgt(c)):
            failed_cases.append('The case ' + swmgt.list_swmgt.__name__ + ' failed')
        if (swmgt.start_stop_swmgt(c)):
            failed_cases.append('The case ' + swmgt.start_stop_swmgt.__name__ + ' failed')
        if (swmgt.restart_swmgt(c)):
            failed_cases.append('The case ' + swmgt.restart_swmgt.__name__ + ' failed')
        if (swmgt.mod_swmgt(c)):
            failed_cases.append('The case ' + swmgt.mod_swmgt.__name__ + ' failed')
        if (swmgt.add_swmgt(c)):
            failed_cases.append('The case ' + swmgt.add_swmgt.__name__ + ' failed')
        if (swmgt.delete_swmgt(c)):
            failed_cases.append('The case ' + swmgt.delete_swmgt.__name__ + ' failed')
        if (swmgt.invalid_parameter_for_swmgt(c)):
            failed_cases.append('The case ' + swmgt.invalid_parameter_for_swmgt.__name__ + ' failed')
        if (swmgt.invalid_option_for_swmgt(c)):
            failed_cases.append('The case ' + swmgt.invalid_option_for_swmgt.__name__ + ' failed')
        if (swmgt.missing_parameter_for_swmgt(c)):
            failed_cases.append('The case ' + swmgt.missing_parameter_for_swmgt.__name__ + ' failed')

        tolog("Start verifying subscription")
        import subscription
        if (subscription.list_subscription(c)):
            failed_cases.append('The case ' + subscription.list_subscription.__name__ + ' failed')
        if (subscription.list_subscription_by_v_mode(c)):
            failed_cases.append('The case ' + subscription.list_subscription_by_v_mode.__name__ + ' failed')
        if (subscription.mod_subscription(c)):
            failed_cases.append('The case ' + subscription.mod_subscription.__name__ + ' failed')
        if (subscription.enable_disable_subscription(c)):
            failed_cases.append('The case ' + subscription.enable_disable_subscription.__name__ + ' failed')
        if (subscription.test_subscription(c)):
            failed_cases.append('The case ' + subscription.test_subscription.__name__ + ' failed')
        if (subscription.invalid_parameter_subscription(c)):
            failed_cases.append('The case ' + subscription.invalid_parameter_subscription.__name__ + ' failed')
        if (subscription.invalid_option_for_subscription(c)):
            failed_cases.append('The case ' + subscription.invalid_option_for_subscription.__name__ + ' failed')
        if (subscription.missing_parameter_subscription(c)):
            failed_cases.append('The case ' + subscription.missing_parameter_subscription.__name__ + ' failed')

        tolog("Start verifying chap")
        import chap
        if (chap.add_chap(c)):
            failed_cases.append('The case ' + chap.add_chap.__name__ + ' failed')
        if (chap.list_chap(c)):
            failed_cases.append('The case ' + chap.list_chap.__name__ + ' failed')
        if (chap.mod_chap(c)):
            failed_cases.append('The case ' + chap.mod_chap.__name__ + ' failed')
        if (chap.del_chap(c)):
            failed_cases.append('The case ' + chap.del_chap.__name__ + ' failed')
        if (chap.invalid_setting_for_chap(c)):
            failed_cases.append('The case ' + chap.invalid_setting_for_chap.__name__ + ' failed')
        if (chap.invalid_option_for_chap(c)):
            failed_cases.append('The case ' + chap.invalid_option_for_chap.__name__ + ' failed')
        if (chap.missing_parameter_for_chap(c)):
            failed_cases.append('The case ' + chap.missing_parameter_for_chap.__name__ + ' failed')

        tolog('Start verifying user')
        import user
        if (user.add_mgmt_user(c)):
            failed_cases.append('The case ' + user.add_mgmt_user.__name__ + ' failed')
        if (user.mod_mgmt_user(c)):
            failed_cases.append('The case ' + user.mod_mgmt_user.__name__ + ' failed')
        if (user.add_snmp_user(c)):
            failed_cases.append('The case ' + user.add_snmp_user.__name__ + ' failed')
        if (user.mod_snmp_user(c)):
            failed_cases.append('The case ' + user.mod_snmp_user.__name__ + ' failed')
        if (user.add_nas_user(c)):
            failed_cases.append('The case ' + user.add_nas_user.__name__ + ' failed')
        if (user.mod_nas_user(c)):
            failed_cases.append('The case ' + user.mod_nas_user.__name__ + ' failed')
        if (user.list_user(c)):
            failed_cases.append('The case ' + user.list_user.__name__ + ' failed')
        if (user.list_user_by_verbose_mode(c)):
            failed_cases.append('The case ' + user.list_user_by_verbose_mode.__name__ + ' failed')
        if (user.del_user(c)):
            failed_cases.append('The case ' + user.del_user.__name__ + ' failed')
        if (user.invalid_setting_for_user(c)):
            failed_cases.append('The case ' + user.invalid_setting_for_user.__name__ + ' failed')
        if (user.invalid_option_for_user(c)):
            failed_cases.append('The case ' + user.invalid_option_for_user.__name__ + ' failed')
        if (user.missing_parameter_for_user(c)):
            failed_cases.append('The case ' + user.missing_parameter_for_user.__name__ + ' failed')

        tolog('Start verifying sc')
        import sc
        if (sc.start_sc(c)):
            failed_cases.append('The case ' + sc.start_sc.__name__ + ' failed')
        if (sc.list_sc(c)):
            failed_cases.append('The case ' + sc.list_sc.__name__ + ' failed')
        if (sc.invalid_setting_for_sc(c)):
            failed_cases.append('The case ' + sc.invalid_setting_for_sc.__name__ + ' failed')
        if (sc.invalid_option_for_sc(c)):
            failed_cases.append('The case ' + sc.invalid_option_for_sc.__name__ + ' failed')
        if (sc.missing_parameter_for_sc(c)):
            failed_cases.append('The case ' + sc.missing_parameter_for_sc.__name__ + ' failed')

        tolog('Start verifying perfstats')
        import perfstats
        if (perfstats.start_perfstats(c)):
            failed_cases.append('The case ' + perfstats.start_perfstats.__name__ + ' failed')
        if (perfstats.list_perfstats(c)):
            failed_cases.append('The case ' + perfstats.list_perfstats.__name__ + ' failed')
        if (perfstats.invalid_setting_parameter(c)):
            failed_cases.append('The case ' + perfstats.invalid_setting_parameter.__name__ + ' failed')
        if (perfstats.invalid_option(c)):
            failed_cases.append('The case ' + perfstats.invalid_option.__name__ + ' failed')
        if (perfstats.missing_parameter(c)):
            failed_cases.append('The case ' + perfstats.missing_parameter.__name__ + ' failed')

        tolog('Start verifying ping')
        import ping
        # if (ping.iscsi_ping(c)):
        #     failed_cases.append('The case ' + ping.iscsi_ping.__name__ + ' failed')
        # if (ping.mgmt_ping(c)):
        #     failed_cases.append('The case ' + ping.mgmt_ping.__name__ + ' failed')
        # if (ping.fc_ping(c)):
        #     failed_cases.append('The case ' + ping.fc_ping.__name__ + ' failed')
        if (ping.invalid_setting_parameter(c)):
            failed_cases.append('The case ' + ping.invalid_setting_parameter.__name__ + ' failed')
        if (ping.invalid_option(c)):
            failed_cases.append('The case ' + ping.invalid_option.__name__ + ' failed')
        if (ping.missing_parameter(c)):
            failed_cases.append('The case ' + ping.missing_parameter.__name__ + ' failed')

        tolog("Start verifying about")
        import about
        if (about.verifyAbout(c)):
            failed_cases.append('The case ' + about.verifyAbout.__name__ + ' failed')
        if (about.verifyAboutHelp(c)):
            failed_cases.append('The case ' + about.verifyAboutHelp.__name__ + ' failed')
        if (about.verifyAboutInvalidOption(c)):
            failed_cases.append('The case ' + about.verifyAboutInvalidOption.__name__ + ' failed')
        if (about.verifyAboutInvalidParameters(c)):
            failed_cases.append('The case ' + about.verifyAboutInvalidParameters.__name__ + ' failed')

        tolog("Start verifying battery")
        import battery
        if (battery.verifyBattery(c)):
            failed_cases.append('The case ' + battery.verifyBattery.__name__ + ' failed')
        if (battery.verifyBatteryList(c)):
            failed_cases.append('The case ' + battery.verifyBatteryList.__name__ + ' failed')
        if (battery.verifyBatteryRecondition(c)):
            failed_cases.append('The case ' + battery.verifyBatteryRecondition.__name__ + ' failed')
        if (battery.verifyBatteryHelp(c)):
            failed_cases.append('The case ' + battery.verifyBatteryHelp.__name__ + ' failed')
        if (battery.verifyBatterySpecifyInexistentId(c)):
            failed_cases.append('The case ' + battery.verifyBatterySpecifyInexistentId.__name__ + ' failed')
        if (battery.verifyBatteryInvalidOption(c)):
            failed_cases.append('The case ' + battery.verifyBatteryInvalidOption.__name__ + ' failed')
        if (battery.verifyBatteryInvalidParameters(c)):
            failed_cases.append('The case ' + battery.verifyBatteryInvalidParameters.__name__ + ' failed')
        if (battery.verifyBatteryMissingParameters(c)):
            failed_cases.append('The case ' + battery.verifyBatteryMissingParameters.__name__ + ' failed')

        tolog("Start verifying BBM")
        import bbm
        if (bbm.verifyBBM(c)):
            failed_cases.append('The case ' + bbm.verifyBBM.__name__ + ' failed')
        if (bbm.verifyBBMClear(c)):
            failed_cases.append('The case ' + bbm.verifyBBMClear.__name__ + ' failed')
        if (bbm.verifyBBMHelp(c)):
            failed_cases.append('The case ' + bbm.verifyBBMHelp.__name__ + ' failed')
        if (bbm.verifyBBMInvalidOption(c)):
            failed_cases.append('The case ' + bbm.verifyBBMInvalidOption.__name__ + ' failed')
        if (bbm.verifyBBMInvalidParameters(c)):
            failed_cases.append('The case ' + bbm.verifyBBMInvalidParameters.__name__ + ' failed')
        if (bbm.verifyBBMList(c)):
            failed_cases.append('The case ' + bbm.verifyBBMList.__name__ + ' failed')
        if (bbm.verifyBBMMissingParameters(c)):
            failed_cases.append('The case ' + bbm.verifyBBMMissingParameters.__name__ + ' failed')
        if (bbm.verifyBBMSpecifyInexistentId(c)):
            failed_cases.append('The case ' + bbm.verifyBBMSpecifyInexistentId.__name__ + ' failed')
        (bbm.cleanUp(c))

        tolog("Start verifying bga")
        import bga
        if (bga.verifyBga(c)):
            failed_cases.append('The case ' + bga.verifyBga.__name__ + ' failed')
        if (bga.verifyBgaList(c)):
            failed_cases.append('The case ' + bga.verifyBgaList.__name__ + ' failed')
        if (bga.verifyBgaMod(c)):
            failed_cases.append('The case ' + bga.verifyBgaMod.__name__ + ' failed')
        if (bga.verifyBgaHelp(c)):
            failed_cases.append('The case ' + bga.verifyBgaHelp.__name__ + ' failed')
        if (bga.verifyBgaInvalidOption(c)):
            failed_cases.append('The case ' + bga.verifyBgaInvalidOption.__name__ + ' failed')
        if (bga.verifyBgaInvalidParameters(c)):
            failed_cases.append('The case ' + bga.verifyBgaInvalidParameters.__name__ + ' failed')
        if (bga.verifyBgaMissingParameters(c)):
            failed_cases.append('The case ' + bga.verifyBgaMissingParameters.__name__ + ' failed')

        tolog("Start verifying buzzer")
        import buzzer
        if (buzzer.verifyBuzzerDisableAndSilentTurnOn((c))):
            failed_cases.append('The case ' + buzzer.verifyBuzzerDisableAndSilentTurnOn.__name__ + ' failed')
        if (buzzer.verifyBuzzerEnableAndSilentTurnOn((c))):
            failed_cases.append('The case ' + buzzer.verifyBuzzerEnableAndSilentTurnOn.__name__ + ' failed')
        if (buzzer.verifyBuzzerEnableAndSoundingTurnOn((c))):
            failed_cases.append('The case ' + buzzer.verifyBuzzerEnableAndSoundingTurnOn.__name__ + ' failed')
        if (buzzer.verifyBuzzerDisableAndSilentTurnOff((c))):
            failed_cases.append('The case ' + buzzer.verifyBuzzerDisableAndSilentTurnOff.__name__ + ' failed')
        if (buzzer.verifyBuzzerEnableAndSilentTurnOff((c))):
            failed_cases.append('The case ' + buzzer.verifyBuzzerEnableAndSilentTurnOff.__name__ + ' failed')
        if (buzzer.verifyBuzzerEnableAndSoundingTurnOff((c))):
            failed_cases.append('The case ' + buzzer.verifyBuzzerEnableAndSoundingTurnOff.__name__ + ' failed')
        if (buzzer.verifyBuzzerDisableAndSilentEnable((c))):
            failed_cases.append('The case ' + buzzer.verifyBuzzerDisableAndSilentEnable.__name__ + ' failed')
        if (buzzer.verifyBuzzerEnableAndSilentEnable((c))):
            failed_cases.append('The case ' + buzzer.verifyBuzzerEnableAndSilentEnable.__name__ + ' failed')
        if (buzzer.verifyBuzzerEnableAndSoundingEnable((c))):
            failed_cases.append('The case ' + buzzer.verifyBuzzerEnableAndSoundingEnable.__name__ + ' failed')
        if (buzzer.verifyBuzzerEnableAndSoundingDisable((c))):
            failed_cases.append('The case ' + buzzer.verifyBuzzerEnableAndSoundingDisable.__name__ + ' failed')
        if (buzzer.verifyBuzzerEnableAndSilentDisable((c))):
            failed_cases.append('The case ' + buzzer.verifyBuzzerEnableAndSilentDisable.__name__ + ' failed')
        if (buzzer.verifyBuzzerDisableAndSilentDisable((c))):
            failed_cases.append('The case ' + buzzer.verifyBuzzerDisableAndSilentDisable.__name__ + ' failed')
        if (buzzer.verifyBuzzerInfo((c))):
            failed_cases.append('The case ' + buzzer.verifyBuzzerInfo.__name__ + ' failed')
        if (buzzer.verifyBuzzerHelp((c))):
            failed_cases.append('The case ' + buzzer.verifyBuzzerHelp.__name__ + ' failed')
        if (buzzer.verifyBuzzerInvalidParameters((c))):
            failed_cases.append('The case ' + buzzer.verifyBuzzerInvalidParameters.__name__ + ' failed')
        if (buzzer.verifyBuzzerInvalidOption((c))):
            failed_cases.append('The case ' + buzzer.verifyBuzzerInvalidOption.__name__ + ' failed')

        tolog("Start verifying ctrl")
        import ctrl
        if (ctrl.list_ctrl(c)):
            failed_cases.append('The case ' + ctrl.list_ctrl.__name__ + ' failed')
        if (ctrl.list_ctrl_by_verbose_mode(c)):
            failed_cases.append('The case ' + ctrl.list_ctrl_by_verbose_mode.__name__ + ' failed')
        if (ctrl.mod_ctrl(c)):
            failed_cases.append('The case ' + ctrl.mod_ctrl.__name__ + ' failed')
        if (ctrl.clear_ctrl(c)):
            failed_cases.append('The case ' + ctrl.clear_ctrl.__name__ + ' failed')
        if (ctrl.invalid_setting_for_ctrl(c)):
            failed_cases.append('The case ' + ctrl.invalid_setting_for_ctrl.__name__ + ' failed')
        if (ctrl.invalid_option_for_ctrl(c)):
            failed_cases.append('The case ' + ctrl.invalid_option_for_ctrl.__name__ + ' failed')
        if (ctrl.missing_parameter_for_ctrl(c)):
            failed_cases.append('The case ' + ctrl.missing_parameter_for_ctrl.__name__ + ' failed')

        tolog("Start verifying encldiag")
        import encldiag
        if (encldiag.verifyEncldiag(c)):
            failed_cases.append('The case ' + encldiag.verifyEncldiag.__name__ + ' failed')
        if (encldiag.verifyEncldiagList(c)):
            failed_cases.append('The case ' + encldiag.verifyEncldiagList.__name__ + ' failed')
        if (encldiag.verifyEncldiagHelp(c)):
            failed_cases.append('The case ' + encldiag.verifyEncldiagHelp.__name__ + ' failed')
        if (encldiag.verifyEncldiagSpecifyInexistentId(c)):
            failed_cases.append('The case ' + encldiag.verifyEncldiagSpecifyInexistentId.__name__ + ' failed')
        if (encldiag.verifyEncldiagInvalidOption(c)):
            failed_cases.append('The case ' + encldiag.verifyEncldiagInvalidOption.__name__ + ' failed')
        if (encldiag.verifyEncldiagInvalidParameters(c)):
            failed_cases.append('The case ' + encldiag.verifyEncldiagInvalidParameters.__name__ + ' failed')
        if (encldiag.verifyEncldiagMissingParameters(c)):
            failed_cases.append('The case ' + encldiag.verifyEncldiagMissingParameters.__name__ + ' failed')

        tolog("Start verifying enclosure")
        import enclosure
        if (enclosure.verifyEnclosure(c)):
            failed_cases.append('The case ' + enclosure.verifyEnclosure.__name__ + ' failed')
        if (enclosure.verifyEnclosureList(c)):
            failed_cases.append('The case ' + enclosure.verifyEnclosureList.__name__ + ' failed')
        if (enclosure.verifyEnclosureMod(c)):
            failed_cases.append('The case ' + enclosure.verifyEnclosureMod.__name__ + ' failed')
        if (enclosure.verifyEnclosureLocate(c)):
            failed_cases.append('The case ' + enclosure.verifyEnclosureLocate.__name__ + ' failed')
        if (enclosure.verifyEnclosureHelp(c)):
            failed_cases.append('The case ' + enclosure.verifyEnclosureHelp.__name__ + ' failed')
        if (enclosure.verifEnclosureSpecifyInexistentId(c)):
            failed_cases.append('The case ' + enclosure.verifEnclosureSpecifyInexistentId.__name__ + ' failed')
        if (enclosure.verifyEnclosureInvalidOption(c)):
            failed_cases.append('The case ' + enclosure.verifyEnclosureInvalidOption.__name__ + ' failed')
        if (enclosure.verifyEnclosureInvalidParameters(c)):
            failed_cases.append('The case ' + enclosure.verifyEnclosureInvalidParameters.__name__ + ' failed')
        if (enclosure.verifyEnclosureMissingParameters(c)):
            failed_cases.append('The case ' + enclosure.verifyEnclosureMissingParameters.__name__ + ' failed')

        tolog("Start verifying event")
        import event
        if (event.verifyEvent(c)):
            failed_cases.append('The case ' + event.verifyEvent.__name__ + ' failed')
        if (event.verifyEventList(c)):
            failed_cases.append('The case ' + event.verifyEventList.__name__ + ' failed')
        if (event.verifyEventClear(c)):
            failed_cases.append('The case ' + event.verifyEventClear.__name__ + ' failed')
        if (event.verifyEventHelp(c)):
            failed_cases.append('The case ' + event.verifyEventHelp.__name__ + ' failed')
        if (event.verifEventSpecifyInexistentId(c)):
            failed_cases.append('The case ' + event.verifEventSpecifyInexistentId.__name__ + ' failed')
        if (event.verifyEventInvalidOption(c)):
            failed_cases.append('The case ' + event.verifyEventInvalidOption.__name__ + ' failed')
        if (event.verifyEventInvalidParameters(c)):
            failed_cases.append('The case ' + event.verifyEventInvalidParameters.__name__ + ' failed')
        if (event.verifyEventMissingParameters(c)):
            failed_cases.append('The case ' + event.verifyEventMissingParameters.__name__ + ' failed')

        tolog("Start verifying factorydefaults")
        import factorydefaults
        if (factorydefaults.factorydefaultsBga(c)):
            failed_cases.append('The case ' + factorydefaults.factorydefaultsBga.__name__ + ' failed')
        if (factorydefaults.factorydefaultsCtrl(c)):
            failed_cases.append('The case ' + factorydefaults.factorydefaultsCtrl.__name__ + ' failed')
        if (factorydefaults.factorydefaultsEncl(c)):
            failed_cases.append('The case ' + factorydefaults.factorydefaultsEncl.__name__ + ' failed')
        if (factorydefaults.factorydefaultsFc(c)):
            failed_cases.append('The case ' + factorydefaults.factorydefaultsFc.__name__ + ' failed')
        if (factorydefaults.factorydefaultsIscsi(c)):
            failed_cases.append('The case ' + factorydefaults.factorydefaultsIscsi.__name__ + ' failed')
        if (factorydefaults.factorydefaultsPhydrv(c)):
            failed_cases.append('The case ' + factorydefaults.factorydefaultsPhydrv.__name__ + ' failed')
        if (factorydefaults.factorydefaultsSubsys(c)):
            failed_cases.append('The case ' + factorydefaults.factorydefaultsSubsys.__name__ + ' failed')
        if (factorydefaults.factorydefaultsBgasched(c)):
            failed_cases.append('The case ' + factorydefaults.factorydefaultsBgasched.__name__ + ' failed')
        if (factorydefaults.factorydefaultsService(c)):
            failed_cases.append('The case ' + factorydefaults.factorydefaultsService.__name__ + ' failed')
        if (factorydefaults.factorydefaultsWebserver(c)):
            failed_cases.append('The case ' + factorydefaults.factorydefaultsWebserver.__name__ + ' failed')
        if (factorydefaults.factorydefaultsSnmp(c)):
            failed_cases.append('The case ' + factorydefaults.factorydefaultsSnmp.__name__ + ' failed')
        if (factorydefaults.factorydefaultsEmail(c)):
            failed_cases.append('The case ' + factorydefaults.factorydefaultsEmail.__name__ + ' failed')
        if (factorydefaults.factorydefaultsNtp(c)):
            failed_cases.append('The case ' + factorydefaults.factorydefaultsNtp.__name__ + ' failed')
        if (factorydefaults.factorydefaultsUser(c)):
            failed_cases.append('The case ' + factorydefaults.factorydefaultsUser.__name__ + ' failed')
        if (factorydefaults.factorydefaultsUps(c)):
            failed_cases.append('The case ' + factorydefaults.factorydefaultsUps.__name__ + ' failed')
        if (factorydefaults.factorydefaultsSyslog(c)):
            failed_cases.append('The case ' + factorydefaults.factorydefaultsSyslog.__name__ + ' failed')
        if (factorydefaults.verifyFactorydefaultsHelp(c)):
            failed_cases.append('The case ' + factorydefaults.verifyFactorydefaultsHelp.__name__ + ' failed')
        if (factorydefaults.verifyFactorydefaultsInvalidOption(c)):
            failed_cases.append('The case ' + factorydefaults.verifyFactorydefaultsInvalidOption.__name__ + ' failed')
        if (factorydefaults.verifyFactorydefaultsInvalidParameters(c)):
            failed_cases.append(
                'The case ' + factorydefaults.verifyFactorydefaultsInvalidParameters.__name__ + ' failed')
        if (factorydefaults.verifyFactorydefaultsMissingParameters(c)):
            failed_cases.append(
                'The case ' + factorydefaults.verifyFactorydefaultsMissingParameters.__name__ + ' failed')

        tolog("Start verifying help")
        import help
        if (help.verifyHelp(c)):
            failed_cases.append('The case ' + help.verifyHelp.__name__ + ' failed')

        tolog("Start verifying isns")
        import isns
        if (isns.verifyIsns(c)):
            failed_cases.append('The case ' + isns.verifyIsns.__name__ + ' failed')
        if (isns.verifyIsnsList(c)):
            failed_cases.append('The case ' + isns.verifyIsnsList.__name__ + ' failed')
        if (isns.verifyIsnsMod(c)):
            failed_cases.append('The case ' + isns.verifyIsnsMod.__name__ + ' failed')
        if (isns.verifyIsnsSpecifyInexistentId(c)):
            failed_cases.append('The case ' + isns.verifyIsnsSpecifyInexistentId.__name__ + ' failed')
        if (isns.verifyIsnsInvalidOption(c)):
            failed_cases.append('The case ' + isns.verifyIsnsInvalidOption.__name__ + ' failed')
        if (isns.verifyIsnsInvalidParameters(c)):
            failed_cases.append('The case ' + isns.verifyIsnsInvalidParameters.__name__ + ' failed')
        if (isns.verifyIsnsMissingParameters(c)):
            failed_cases.append('The case ' + isns.verifyIsnsMissingParameters.__name__ + ' failed')

        tolog("Start verifying ntp")
        import ntp
        if (ntp.verifyNtpMod(c)):
            failed_cases.append('The case ' + ntp.verifyNtpMod.__name__ + ' failed')
        if (ntp.verifyNtp(c)):
            failed_cases.append('The case ' + ntp.verifyNtp.__name__ + ' failed')
        if (ntp.verifyNtpList(c)):
            failed_cases.append('The case ' + ntp.verifyNtpList.__name__ + ' failed')
        if (ntp.verifyNtpTest(c)):
            failed_cases.append('The case ' + ntp.verifyNtpTest.__name__ + ' failed')
        if (ntp.verifyNtpSync(c)):
            failed_cases.append('The case ' + ntp.verifyNtpSync.__name__ + ' failed')
        if (ntp.verifyNtpInvalidOption(c)):
            failed_cases.append('The case ' + ntp.verifyNtpInvalidOption.__name__ + ' failed')
        if (ntp.verifyNtpInvalidParameters(c)):
            failed_cases.append('The case ' + ntp.verifyNtpInvalidParameters.__name__ + ' failed')
        if (ntp.verifyNtpMissingParameters(c)):
            failed_cases.append('The case ' + ntp.verifyNtpMissingParameters.__name__ + ' failed')

        tolog("Start verifying password")
        import password
        if (password.verifyChangePassword(c)):
            failed_cases.append('The case ' + password.verifyChangePassword.__name__ + ' failed')
        if (password.verifyPasswordSpecifyInexistentUsername(c)):
            failed_cases.append('The case ' + password.verifyPasswordSpecifyInexistentUsername.__name__ + ' failed')
        if (password.verifyPasswordInvalidOption(c)):
            failed_cases.append('The case ' + password.verifyPasswordInvalidOption.__name__ + ' failed')
        if (password.verifyPasswordInvalidParameters(c)):
            failed_cases.append('The case ' + password.verifyPasswordInvalidParameters.__name__ + ' failed')
        if (password.verifyPasswordMissingParameters(c)):
            failed_cases.append('The case ' + password.verifyPasswordMissingParameters.__name__ + ' failed')

        tolog("Start verifying pcie")
        import pcie
        if (pcie.verifyPcie(c)):
            failed_cases.append('The case ' + pcie.verifyPcie.__name__ + ' failed')
        if (pcie.verifyPcielist(c)):
            failed_cases.append('The case ' + pcie.verifyPcielist.__name__ + ' failed')
        if (pcie.verifyPcieInvalidOption(c)):
            failed_cases.append('The case ' + pcie.verifyPcieInvalidOption.__name__ + ' failed')
        if (pcie.verifyPcieInvalidParameters(c)):
            failed_cases.append('The case ' + pcie.verifyPcieInvalidParameters.__name__ + ' failed')
        if (pcie.verifyPcieMissingParameters(c)):
            failed_cases.append('The case ' + pcie.verifyPcieMissingParameters.__name__ + ' failed')

        tolog("Start verifying smart")
        import smart
        if (smart.verifySmart(c)):
            failed_cases.append('The case ' + smart.verifySmart.__name__ + ' failed')
        if (smart.verifySmartV(c)):
            failed_cases.append('The case ' + smart.verifySmartV.__name__ + ' failed')
        if (smart.verifySmartList(c)):
            failed_cases.append('The case ' + smart.verifySmartList.__name__ + ' failed')
        if (smart.verifySmartEnable(c)):
            failed_cases.append('The case ' + smart.verifySmartEnable.__name__ + ' failed')
        if (smart.verifySmartDisable(c)):
            failed_cases.append('The case ' + smart.verifySmartDisable.__name__ + ' failed')
        if (smart.verifySmartHelp(c)):
            failed_cases.append('The case ' + smart.verifySmartHelp.__name__ + ' failed')
        if (smart.verifySmartSpecifyInexistentId(c)):
            failed_cases.append('The case ' + smart.verifySmartSpecifyInexistentId.__name__ + ' failed')
        if (smart.verifySmartInvalidOption(c)):
            failed_cases.append('The case ' + smart.verifySmartInvalidOption.__name__ + ' failed')
        if (smart.verifySmartInvalidParameters(c)):
            failed_cases.append('The case ' + smart.verifySmartInvalidParameters.__name__ + ' failed')
        if (smart.verifySmartMissingParameters(c)):
            failed_cases.append('The case ' + smart.verifySmartMissingParameters.__name__ + ' failed')

        tolog('Start verifying tz')
        import tz
        if (tz.list_tz(c)):
            failed_cases.append('The case ' + tz.list_tz.__name__ + ' failed')
        if (tz.list_tz_detail(c)):
            failed_cases.append('The case ' + tz.list_tz_detail.__name__ + ' failed')
        if (tz.mod_tz(c)):
            failed_cases.append('The case ' + tz.mod_tz.__name__ + ' failed')
        if (tz.invalid_parameter_for_tz(c)):
            failed_cases.append('The case ' + tz.invalid_parameter_for_tz.__name__ + ' failed')
        if (tz.invalid_option_for_tz(c)):
            failed_cases.append('The case ' + tz.invalid_option_for_tz.__name__ + ' failed')
        if (tz.missing_parameter_for_tz(c)):
            failed_cases.append('The case ' + tz.missing_parameter_for_tz.__name__ + ' failed')

        tolog('Start verifying domain')
        import domain
        if (domain.list_domain(c)):
            failed_cases.append('The case ' + domain.list_domain.__name__ + ' failed')
        if (domain.list_domain_by_verbose_mode(c)):
            failed_cases.append('The case ' + domain.list_domain_by_verbose_mode.__name__ + ' failed')
        if (domain.enable_refresh_check_disable(c)):
            failed_cases.append('The case ' + domain.enable_refresh_check_disable.__name__ + ' failed')
        if (domain.invalid_setting_for_domain(c)):
            failed_cases.append('The case ' + domain.invalid_setting_for_domain.__name__ + ' failed')
        if (domain.invalid_option_for_domain(c)):
            failed_cases.append('The case ' + domain.invalid_option_for_domain.__name__ + ' failed')
        if (domain.missing_parameter_for_domain(c)):
            failed_cases.append('The case ' + domain.missing_parameter_for_domain.__name__ + ' failed')

        tolog('Start verifying target')
        import target
        if (target.add_target(c)):
            failed_cases.append('The case ' + target.add_target.__name__ + ' failed')
        if (target.list_target(c)):
            failed_cases.append('The case ' + target.list_target.__name__ + ' failed')
        if (target.del_target(c)):
            failed_cases.append('The case ' + target.del_target.__name__ + ' failed')
        if (target.invalid_setting_for_target(c)):
            failed_cases.append('The case ' + target.invalid_setting_for_target.__name__ + ' failed')
        if (target.invalid_option_for_target(c)):
            failed_cases.append('The case ' + target.invalid_option_for_target.__name__ + ' failed')
        if (target.missing_parameter_for_target(c)):
            failed_cases.append('The case ' + target.missing_parameter_for_target.__name__ + ' failed')

        tolog('Start verifying migrate')
        import migrate
        if (migrate.start_local_migrate(c)):
            failed_cases.append('The case ' + migrate.start_local_migrate.__name__ + ' failed')
        if (migrate.start_remote_migrate(c)):
            failed_cases.append('The case ' + migrate.start_remote_migrate.__name__ + ' failed')
        if (migrate.stop_migrate(c)):
            failed_cases.append('The case ' + migrate.stop_migrate.__name__ + ' failed')
        if (migrate.help_migrate(c)):
            failed_cases.append('The case ' + migrate.help_migrate.__name__ + ' failed')
        if (migrate.invalid_setting_for_migrate(c)):
            failed_cases.append('The case ' + migrate.invalid_setting_for_migrate.__name__ + ' failed')
        if (migrate.invalid_option_for_migrate(c)):
            failed_cases.append('The case ' + migrate.invalid_option_for_migrate.__name__ + ' failed')
        if (migrate.missing_parameter_migrate(c)):
            failed_cases.append('The case ' + migrate.missing_parameter_migrate.__name__ + ' failed')

        tolog('Start verifying wcache')
        import wcache
        if (wcache.add_wcache_dedication(c)):
            failed_cases.append('The case ' + wcache.add_wcache_dedication.__name__ + ' failed')
        if (wcache.mod_wcache(c)):
            failed_cases.append('The case ' + wcache.mod_wcache.__name__ + ' failed')
        if (wcache.add_wcache_no_dedication(c)):
            failed_cases.append('The case ' + wcache.add_wcache_no_dedication.__name__ + ' failed')
        if (wcache.list_wcache(c)):
            failed_cases.append('The case ' + wcache.list_wcache.__name__ + ' failed')
        if (wcache.def_wcache(c)):
            failed_cases.append('The case ' + wcache.def_wcache.__name__ + ' failed')
        if (wcache.invalid_setting_for_wcache(c)):
            failed_cases.append('The case ' + wcache.invalid_setting_for_wcache.__name__ + ' failed')
        if (wcache.invalid_option_for_wcache(c)):
            failed_cases.append('The case ' + wcache.invalid_option_for_wcache.__name__ + ' failed')
        if (wcache.missing_parameter_for_wcache(c)):
            failed_cases.append('The case ' + wcache.missing_parameter_for_wcache.__name__ + ' failed')

        tolog('Start verifying rcache')
        import rcache
        if (rcache.add_rcache_by_one_pd(c)):
            failed_cases.append('The case ' + rcache.add_rcache_by_one_pd.__name__ + ' failed')
        if (rcache.add_rcache_by_multiple_pd(c)):
            failed_cases.append('The case ' + rcache.add_rcache_by_multiple_pd.__name__ + ' failed')
        if (rcache.list_rcache(c)):
            failed_cases.append('The case ' + rcache.list_rcache.__name__ + ' failed')
        if (rcache.def_rcache(c)):
            failed_cases.append('The case ' + rcache.def_rcache.__name__ + ' failed')
        if (rcache.invalid_setting_for_rcache(c)):
            failed_cases.append('The case ' + rcache.invalid_setting_for_rcache.__name__ + ' failed')
        if (rcache.invalid_option_for_rcache(c)):
            failed_cases.append('The case ' + rcache.invalid_option_for_rcache.__name__ + ' failed')
        if (rcache.missing_parameter_for_rcache(c)):
            failed_cases.append('The case ' + rcache.missing_parameter_for_rcache.__name__ + ' failed')

        tolog('Start verifying bgasched')
        import bgasched
        if (bgasched.verifyBgaschedAdd(c)):
            failed_cases.append('The case ' + bgasched.verifyBgaschedAdd.__name__ + ' failed')
        if (bgasched.verifyBgaschedMod(c)):
            failed_cases.append('The case ' + bgasched.verifyBgaschedMod.__name__ + ' failed')
        if (bgasched.verifyBgaschedList(c)):
            failed_cases.append('The case ' + bgasched.verifyBgaschedList.__name__ + ' failed')
        if (bgasched.verifyBgaschedDel(c)):
            failed_cases.append('The case ' + bgasched.verifyBgaschedDel.__name__ + ' failed')
        if (bgasched.verifyBgaschedHelp(c)):
            failed_cases.append('The case ' + bgasched.verifyBgaschedHelp.__name__ + ' failed')
        if (bgasched.verifyBgaschedInvalidOption(c)):
            failed_cases.append('The case ' + bgasched.verifyBgaschedInvalidOption.__name__ + ' failed')
        if (bgasched.verifyBgaschedInvalidParameters(c)):
            failed_cases.append('The case ' + bgasched.verifyBgaschedInvalidParameters.__name__ + ' failed')
        if (bgasched.verifyBgaschedMissingParameters(c)):
            failed_cases.append('The case ' + bgasched.verifyBgaschedMissingParameters.__name__ + ' failed')

    if len(failed_cases) != 0:
        for f in failed_cases:
            tolog(f)
    try:
        c.close()
    except:
        tolog('failed shutdown channel')


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    build_verification(c)
    c.close()
