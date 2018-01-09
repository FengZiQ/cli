# coding=utf-8

from time import sleep
from send_cmd import *
from ssh_connect import *
from to_log import *

Pass = "'result': 'p'"
Fail = "'result': 'f'"


def BuildVerification(c):
    FailCasesList = []

    # To check whether the sw is compiled successfully
    # size = os.path.getsize('/var/lib/jenkins/workspace/Hyperion-DS_Hulda/sw.log')
    size = os.path.getsize('/var/lib/jenkins/workspace/HyperionDS/sw.log')
    if size < 2000000:
        tolog('sw compiles failure')
        exit(1)

    c, ssh = ssh_conn()

    import glob

    files = glob.glob("/var/lib/jenkins/workspace/HyperionDS/build/build/*.ptif")
    # files = glob.glob("/var/lib/jenkins/workspace/Hyperion-DS_Hulda/build/build/*.ptif")

    reconnectflag = False

    for file in files:

        # filename = file.replace("/var/lib/jenkins/workspace/Hyperion-DS_Hulda/build/build/","")
        filename = file.replace("/var/lib/jenkins/workspace/HyperionDS/build/build/", "")

        result = SendCmdRestart(c,"ptiflash -y -t -s 10.84.2.99 -f "+filename)

        if "Error (" not in result:
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
        else:
            tolog(result)

    if reconnectflag:
        # there are 44 command that can be tested
        tolog("Start verifying pool add")
        import pool
        if (pool.add_pool_raid0(c)):
            FailCasesList.append('The case ' + pool.add_pool_raid0.__name__ + ' failed')
        if (pool.add_pool_raid1(c)):
            FailCasesList.append('The case ' + pool.add_pool_raid1.__name__ + ' failed')
        if (pool.add_pool_raid5(c)):
            FailCasesList.append('The case ' + pool.add_pool_raid5.__name__ + ' failed')
        if (pool.add_pool_raid6(c)):
            FailCasesList.append('The case ' + pool.add_pool_raid6.__name__ + ' failed')
        if (pool.add_pool_raid10(c)):
            FailCasesList.append('The case ' + pool.add_pool_raid10.__name__ + ' failed')
        if (pool.add_pool_raid50(c)):
            FailCasesList.append('The case ' + pool.add_pool_raid50.__name__ + ' failed')
        if (pool.add_pool_raid60(c)):
            FailCasesList.append('The case ' + pool.add_pool_raid60.__name__ + ' failed')
        if (pool.add_pool_default_setting(c)):
            FailCasesList.append('The case ' + pool.add_pool_default_setting.__name__ + ' failed')
        if (pool.modify_pool_name(c)):
            FailCasesList.append('The case ' + pool.modify_pool_name.__name__ + ' failed')
        if (pool.list_pool(c)):
            FailCasesList.append('The case ' + pool.list_pool.__name__ + ' failed')
        if (pool.list_verbose_mode_pool(c)):
            FailCasesList.append('The case ' + pool.list_verbose_mode_pool.__name__ + ' failed')
        if (pool.expand_raid0_pool(c)):
            FailCasesList.append('The case ' + pool.expand_raid0_pool.__name__ + ' failed')
        if (pool.expand_raid1_pool(c)):
            FailCasesList.append('The case ' + pool.expand_raid1_pool.__name__ + ' failed')
        if (pool.expand_raid5_pool(c)):
            FailCasesList.append('The case ' + pool.expand_raid5_pool.__name__ + ' failed')
        if (pool.expand_raid6_pool(c)):
            FailCasesList.append('The case ' + pool.expand_raid6_pool.__name__ + ' failed')
        if (pool.expand_raid10_pool(c)):
            FailCasesList.append('The case ' + pool.expand_raid10_pool.__name__ + ' failed')
        if (pool.expand_raid50_pool(c)):
            FailCasesList.append('The case ' + pool.expand_raid50_pool.__name__ + ' failed')
        if (pool.expand_raid60_pool(c)):
            FailCasesList.append('The case ' + pool.expand_raid60_pool.__name__ + ' failed')
        if (pool.delete_pool(c)):
            FailCasesList.append('The case ' + pool.delete_pool.__name__ + ' failed')
        if (pool.invalid_settings_parameter(c)):
            FailCasesList.append('The case ' + pool.invalid_settings_parameter.__name__ + ' failed')
        if (pool.invalid_option(c)):
            FailCasesList.append('The case ' + pool.invalid_option.__name__ + ' failed')
        if (pool.missing_parameter(c)):
            FailCasesList.append('The case ' + pool.missing_parameter.__name__ + ' failed')

        tolog('Start verifying volume')
        import volume
        if (volume.addVolume(c)):
            FailCasesList.append('The case ' + volume.addVolume.__name__ + ' failed')
        if (volume.listVolume(c)):
            FailCasesList.append('The case ' + volume.listVolume.__name__ + ' failed')
        if (volume.listVolume_by_verbose_mode(c)):
            FailCasesList.append('The case ' + volume.listVolume_by_verbose_mode.__name__ + ' failed')
        if (volume.modVolume(c)):
            FailCasesList.append('The case ' + volume.modVolume.__name__ + ' failed')
        if (volume.exportVolume(c)):
            FailCasesList.append('The case ' + volume.exportVolume.__name__ + ' failed')
        if (volume.unexportVolume(c)):
            FailCasesList.append('The case ' + volume.unexportVolume.__name__ + ' failed')
        if (volume.invalidParameter(c)):
            FailCasesList.append('The case ' + volume.invalidParameter.__name__ + ' failed')
        if (volume.invalidOption(c)):
            FailCasesList.append('The case ' + volume.invalidOption.__name__ + ' failed')
        if (volume.missingParameter(c)):
            FailCasesList.append('The case ' + volume.missingParameter.__name__ + ' failed')
        if (volume.deleteVolume(c)):
            FailCasesList.append('The case ' + volume.deleteVolume.__name__ + ' failed')

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

        tolog('Start verifying snapshot')
        import snapshot
        if (snapshot.add_snapshot(c)):
            FailCasesList.append('The case ' + snapshot.add_snapshot.__name__ + ' failed')
        if (snapshot.list_snapshot(c)):
            FailCasesList.append('The case ' + snapshot.list_snapshot.__name__ + ' failed')
        if (snapshot.list_snapshot_by_verbose_mode(c)):
            FailCasesList.append('The case ' + snapshot.list_snapshot_by_verbose_mode.__name__ + ' failed')
        if (snapshot.mod_snapshot(c)):
            FailCasesList.append('The case ' + snapshot.mod_snapshot.__name__ + ' failed')
        if (snapshot.export_unexport_snapshot(c)):
            FailCasesList.append('The case ' + snapshot.export_unexport_snapshot.__name__ + ' failed')
        if (snapshot.mount_umount_snapshot(c)):
            FailCasesList.append('The case ' + snapshot.mount_umount_snapshot.__name__ + ' failed')
        if (snapshot.rollback_snapshot(c)):
            FailCasesList.append('The case ' + snapshot.rollback_snapshot.__name__ + ' failed')
        if (snapshot.del_snapshot(c)):
            FailCasesList.append('The case ' + snapshot.del_snapshot.__name__ + ' failed')
        if (snapshot.invalid_setting_parameter(c)):
            FailCasesList.append('The case ' + snapshot.invalid_setting_parameter.__name__ + ' failed')
        if (snapshot.invalid_option(c)):
            FailCasesList.append('The case ' + snapshot.invalid_option.__name__ + ' failed')
        if (snapshot.missing_parameter(c)):
            FailCasesList.append('The case ' + snapshot.missing_parameter.__name__ + ' failed')

        tolog('Start verifying clone')
        import clone
        if (clone.add_clone(c)):
            FailCasesList.append('The case ' + clone.add_clone.__name__ + ' failed')
        if (clone.list_clone(c)):
            FailCasesList.append('The case ' + clone.list_clone.__name__ + ' failed')
        if (clone.list_clone_verbose_mode(c)):
            FailCasesList.append('The case ' + clone.list_clone_verbose_mode.__name__ + ' failed')
        if (clone.mod_clone(c)):
            FailCasesList.append('The case ' + clone.mod_clone.__name__ + ' failed')
        if (clone.export_unexport_clone(c)):
            FailCasesList.append('The case ' + clone.export_unexport_clone.__name__ + ' failed')
        if (clone.mount_umount_clone(c)):
            FailCasesList.append('The case ' + clone.mount_umount_clone.__name__ + ' failed')
        if (clone.del_clone(c)):
            FailCasesList.append('The case ' + clone.del_clone.__name__ + ' failed')
        if (clone.invalid_setting_parameter(c)):
            FailCasesList.append('The case ' + clone.invalid_setting_parameter.__name__ + ' failed')
        if (clone.invalid_option(c)):
            FailCasesList.append('The case ' + clone.invalid_option.__name__ + ' failed')
        if (clone.missing_parameter(c)):
            FailCasesList.append('The case ' + clone.missing_parameter.__name__ + ' failed')

        tolog('Start verifying replication')
        import replication
        if (replication.start_replication(c)):
            FailCasesList.append('The case ' + replication.start_replication.__name__ + ' failed')
        if (replication.forbidden_action(c)):
            FailCasesList.append('The case ' + replication.forbidden_action.__name__ + ' failed')
        if (replication.list_replication(c)):
            FailCasesList.append('The case ' + replication.list_replication.__name__ + ' failed')
        if (replication.list_replication_by_verbose(c)):
            FailCasesList.append('The case ' + replication.list_replication_by_verbose.__name__ + ' failed')
        if (replication.stop_replication(c)):
            FailCasesList.append('The case ' + replication.stop_replication.__name__ + ' failed')
        if (replication.pause_replication(c)):
            FailCasesList.append('The case ' + replication.pause_replication.__name__ + ' failed')
        if (replication.resume_replication(c)):
            FailCasesList.append('The case ' + replication.resume_replication.__name__ + ' failed')
        if (replication.help_replication(c)):
            FailCasesList.append('The case ' + replication.help_replication.__name__ + ' failed')
        if (replication.invalid_setting_for_replication(c)):
            FailCasesList.append('The case ' + replication.invalid_setting_for_replication.__name__ + ' failed')
        if (replication.invalid_option_for_replication(c)):
            FailCasesList.append('The case ' + replication.invalid_option_for_replication.__name__ + ' failed')
        if (replication.missing_parameter_replication(c)):
            FailCasesList.append('The case ' + replication.missing_parameter_replication.__name__ + ' failed')

        tolog('Start verifying migrate')
        import migrate
        if (migrate.start_local_migrate(c)):
            FailCasesList.append('The case ' + migrate.start_local_migrate.__name__ + ' failed')
        if (migrate.start_remote_migrate(c)):
            FailCasesList.append('The case ' + migrate.start_remote_migrate.__name__ + ' failed')
        if (migrate.stop_migrate(c)):
            FailCasesList.append('The case ' + migrate.stop_migrate.__name__ + ' failed')
        if (migrate.help_migrate(c)):
            FailCasesList.append('The case ' + migrate.help_migrate.__name__ + ' failed')
        if (migrate.invalid_setting_for_migrate(c)):
            FailCasesList.append('The case ' + migrate.invalid_setting_for_migrate.__name__ + ' failed')
        if (migrate.invalid_option_for_migrate(c)):
            FailCasesList.append('The case ' + migrate.invalid_option_for_migrate.__name__ + ' failed')
        if (migrate.missing_parameter_migrate(c)):
            FailCasesList.append('The case ' + migrate.missing_parameter_migrate.__name__ + ' failed')

        tolog('Start verifying spare')
        import spare
        if (spare.add_global_spare(c)):
            FailCasesList.append('The case ' + spare.add_global_spare.__name__ + ' failed')
        if (spare.add_dedicated_spare(c)):
            FailCasesList.append('The case ' + spare.add_dedicated_spare.__name__ + ' failed')
        if (spare.list_spare(c)):
            FailCasesList.append('The case ' + spare.list_spare.__name__ + ' failed')
        if (spare.list_spare_by_verbose_mode(c)):
            FailCasesList.append('The case ' + spare.list_spare_by_verbose_mode.__name__ + ' failed')
        if (spare.delete_spare(c)):
            FailCasesList.append('The case ' + spare.delete_spare.__name__ + ' failed')
        if (spare.invalid_parameter_for_spare(c)):
            FailCasesList.append('The case ' + spare.invalid_parameter_for_spare.__name__ + ' failed')
        if (spare.invalid_option_for_spare(c)):
            FailCasesList.append('The case ' + spare.invalid_option_for_spare.__name__ + ' failed')
        if (spare.missing_parameter_for_spare(c)):
            FailCasesList.append('The case ' + spare.missing_parameter_for_spare.__name__ + ' failed')

        tolog('Start verifying acl')
        import acl
        if (acl.set_acl(c)):
            FailCasesList.append('The case ' + acl.set_acl.__name__ + ' failed')
        if (acl.list_acl(c)):
            FailCasesList.append('The case ' + acl.list_acl.__name__ + ' failed')
        if (acl.list_acl_by_verbose_mode(c)):
            FailCasesList.append('The case ' + acl.list_acl_by_verbose_mode.__name__ + ' failed')
        if (acl.refresh_acl(c)):
            FailCasesList.append('The case ' + acl.refresh_acl.__name__ + ' failed')
        if (acl.acl_unset(c)):
            FailCasesList.append('The case ' + acl.acl_unset.__name__ + ' failed')
        if (acl.clear_acl(c)):
            FailCasesList.append('The case ' + acl.clear_acl.__name__ + ' failed')
        if (acl.cancel_acl(c)):
            FailCasesList.append('The case ' + acl.cancel_acl.__name__ + ' failed')
        if (acl.invalid_setting_parameter(c)):
            FailCasesList.append('The case ' + acl.invalid_setting_parameter.__name__ + ' failed')
        if (acl.invalid_option(c)):
            FailCasesList.append('The case ' + acl.invalid_option.__name__ + ' failed')
        if (acl.missing_parameter(c)):
            FailCasesList.append('The case ' + acl.missing_parameter.__name__ + ' failed')

        tolog('Start verifying periodsnap')
        import periodsnap
        if (periodsnap.add_periodsnap(c)):
            FailCasesList.append('The case ' + periodsnap.add_periodsnap.__name__ + ' failed')
        if (periodsnap.list_periodsnap(c)):
            FailCasesList.append('The case ' + periodsnap.list_periodsnap.__name__ + ' failed')
        if (periodsnap.list_periodsnap_by_verbose_mode(c)):
            FailCasesList.append('The case ' + periodsnap.list_periodsnap_by_verbose_mode.__name__ + ' failed')
        if (periodsnap.mod_periodsnap(c)):
            FailCasesList.append('The case ' + periodsnap.mod_periodsnap.__name__ + ' failed')
        if (periodsnap.del_periodsnap(c)):
            FailCasesList.append('The case ' + periodsnap.del_periodsnap.__name__ + ' failed')
        if (periodsnap.invalid_setting_for_periodsnap(c)):
            FailCasesList.append('The case ' + periodsnap.invalid_setting_for_periodsnap.__name__ + ' failed')
        if (periodsnap.invalid_option_for_periodsnap(c)):
            FailCasesList.append('The case ' + periodsnap.invalid_option_for_periodsnap.__name__ + ' failed')
        if (periodsnap.missing_parameter_periodsnap(c)):
            FailCasesList.append('The case ' + periodsnap.missing_parameter_periodsnap.__name__ + ' failed')

        tolog('Start verifying quota')
        import quota
        if (quota.set_quota(c)):
            FailCasesList.append('The case ' + quota.set_quota.__name__ + ' failed')
        if (quota.list_quota(c)):
            FailCasesList.append('The case ' + quota.list_quota.__name__ + ' failed')
        if (quota.list_quota_by_verbose_mode(c)):
            FailCasesList.append('The case ' + quota.list_quota_by_verbose_mode.__name__ + ' failed')
        if (quota.refresh_quota(c)):
            FailCasesList.append('The case ' + quota.refresh_quota.__name__ + ' failed')
        if (quota.cancel_quota(c)):
            FailCasesList.append('The case ' + quota.cancel_quota.__name__ + ' failed')
        if (quota.delete_quota(c)):
            FailCasesList.append('The case ' + quota.delete_quota.__name__ + ' failed')
        if (quota.invalid_setting_for_quota(c)):
            FailCasesList.append('The case ' + quota.invalid_setting_for_quota.__name__ + ' failed')
        if (quota.invalid_option_for_quota(c)):
            FailCasesList.append('The case ' + quota.invalid_option_for_quota.__name__ + ' failed')
        if (quota.missing_parameter_for_quota(c)):
            FailCasesList.append('The case ' + quota.missing_parameter_for_quota.__name__ + ' failed')

        tolog('Start verifying allowip')
        import allowip
        if (allowip.add_allowip(c)):
            FailCasesList.append('The case ' + allowip.add_allowip.__name__ + ' failed')
        if (allowip.list_allowip(c)):
            FailCasesList.append('The case ' + allowip.list_allowip.__name__ + ' failed')
        if (allowip.list_allowip_by_verbose_mode(c)):
            FailCasesList.append('The case ' + allowip.list_allowip_by_verbose_mode.__name__ + ' failed')
        if (allowip.mod_allowip(c)):
            FailCasesList.append('The case ' + allowip.mod_allowip.__name__ + ' failed')
        if (allowip.del_allowip(c)):
            FailCasesList.append('The case ' + allowip.del_allowip.__name__ + ' failed')
        if (allowip.invalid_setting_for_allowip(c)):
            FailCasesList.append('The case ' + allowip.invalid_setting_for_allowip.__name__ + ' failed')
        if (allowip.invalid_option_for_allowip(c)):
            FailCasesList.append('The case ' + allowip.invalid_option_for_allowip.__name__ + ' failed')
        if (allowip.missing_parameter_for_allowip(c)):
            FailCasesList.append('The case ' + allowip.missing_parameter_for_allowip.__name__ + ' failed')

        tolog('Start verifying protocol')
        import protocol
        if (protocol.list_all_protocol(c)):
            FailCasesList.append('The case ' + protocol.list_all_protocol.__name__ + ' failed')
        if (protocol.list_single_protocol(c)):
            FailCasesList.append('The case ' + protocol.list_single_protocol.__name__ + ' failed')
        if (protocol.mod_ftp_protocol(c)):
            FailCasesList.append('The case ' + protocol.mod_ftp_protocol.__name__ + ' failed')
        if (protocol.mod_smb_protocol(c)):
            FailCasesList.append('The case ' + protocol.mod_smb_protocol.__name__ + ' failed')
        if (protocol.mod_nfs_protocol(c)):
            FailCasesList.append('The case ' + protocol.mod_nfs_protocol.__name__ + ' failed')
        if (protocol.reset_all_protocol(c)):
            FailCasesList.append('The case ' + protocol.reset_all_protocol.__name__ + ' failed')
        if (protocol.reset_single_protocol(c)):
            FailCasesList.append('The case ' + protocol.reset_single_protocol.__name__ + ' failed')
        if (protocol.enable_protocol(c)):
            FailCasesList.append('The case ' + protocol.enable_protocol.__name__ + ' failed')
        if (protocol.disable_protocol(c)):
            FailCasesList.append('The case ' + protocol.disable_protocol.__name__ + ' failed')
        if (protocol.invalid_setting_parameter(c)):
            FailCasesList.append('The case ' + protocol.invalid_setting_parameter.__name__ + ' failed')
        if (protocol.invalid_option(c)):
            FailCasesList.append('The case ' + protocol.invalid_option.__name__ + ' failed')
        if (protocol.missing_parameter(c)):
            FailCasesList.append('The case ' + protocol.missing_parameter.__name__ + ' failed')

        tolog('Start verifying group')
        import group
        if (group.add_group_and_verify_name(c)):
            FailCasesList.append('The case ' + group.add_group_and_verify_name.__name__ + ' failed')
        if (group.add_group_and_user(c)):
            FailCasesList.append('The case ' + group.add_group_and_user.__name__ + ' failed')
        if (group.add_user_into_group(c)):
            FailCasesList.append('The case ' + group.add_user_into_group.__name__ + ' failed')
        if (group.list_group(c)):
            FailCasesList.append('The case ' + group.list_group.__name__ + ' failed')
        if (group.list_group_by_verbose_mode(c)):
            FailCasesList.append('The case ' + group.list_group_by_verbose_mode.__name__ + ' failed')
        if (group.modify_group(c)):
            FailCasesList.append('The case ' + group.modify_group.__name__ + ' failed')
        if (group.delete_user_from_group(c)):
            FailCasesList.append('The case ' + group.delete_user_from_group.__name__ + ' failed')
        if (group.delete_group(c)):
            FailCasesList.append('The case ' + group.delete_group.__name__ + ' failed')
        if (group.invalid_setting_for_group(c)):
            FailCasesList.append('The case ' + group.invalid_setting_for_group.__name__ + ' failed')
        if (group.invalid_option_for_group(c)):
            FailCasesList.append('The case ' + group.invalid_option_for_group.__name__ + ' failed')
        if (group.missing_parameter_for_group(c)):
            FailCasesList.append('The case ' + group.missing_parameter_for_group.__name__ + ' failed')

        tolog('Start verifying phydrv')
        import phydrv
        if (phydrv.list_phydrv(c)):
            FailCasesList.append('The case ' + phydrv.list_phydrv.__name__ + ' failed')
        if (phydrv.list_phydrv_by_verbose_mode(c)):
            FailCasesList.append('The case ' + phydrv.list_phydrv_by_verbose_mode.__name__ + ' failed')
        if (phydrv.mod_phydrv(c)):
            FailCasesList.append('The case ' + phydrv.mod_phydrv.__name__ + ' failed')
        if (phydrv.locate_phydrv(c)):
            FailCasesList.append('The case ' + phydrv.locate_phydrv.__name__ + ' failed')
        if (phydrv.online_offline_phydrv(c)):
            FailCasesList.append('The case ' + phydrv.online_offline_phydrv.__name__ + ' failed')
        if (phydrv.clear_phydrv(c)):
            FailCasesList.append('The case ' + phydrv.clear_phydrv.__name__ + ' failed')
        if (phydrv.invalid_setting_parameter(c)):
            FailCasesList.append('The case ' + phydrv.invalid_setting_parameter.__name__ + ' failed')
        if (phydrv.invalid_option(c)):
            FailCasesList.append('The case ' + phydrv.invalid_option.__name__ + ' failed')
        if (phydrv.missing_parameter(c)):
            FailCasesList.append('The case ' + phydrv.missing_parameter.__name__ + ' failed')

        tolog('Start verifying rb')
        import rb
        if (rb.raid1_start_rb(c)):
            FailCasesList.append('The case ' + rb.raid1_start_rb.__name__ + ' failed')
        if (rb.raid5_start_rb(c)):
            FailCasesList.append('The case ' + rb.raid5_start_rb.__name__ + ' failed')
        if (rb.raid6_start_rb(c)):
            FailCasesList.append('The case ' + rb.raid6_start_rb.__name__ + ' failed')
        if (rb.raid10_start_rb(c)):
            FailCasesList.append('The case ' + rb.raid10_start_rb.__name__ + ' failed')
        if (rb.raid50_start_rb(c)):
            FailCasesList.append('The case ' + rb.raid50_start_rb.__name__ + ' failed')
        if (rb.raid60_start_rb(c)):
            FailCasesList.append('The case ' + rb.raid60_start_rb.__name__ + ' failed')
        if (rb.list_rb(c)):
            FailCasesList.append('The case ' + rb.list_rb.__name__ + ' failed')
        if (rb.stop_rb(c)):
            FailCasesList.append('The case ' + rb.stop_rb.__name__ + ' failed')
        if (rb.invalid_setting_parameter(c)):
            FailCasesList.append('The case ' + rb.invalid_setting_parameter.__name__ + ' failed')
        if (rb.invalid_option(c)):
            FailCasesList.append('The case ' + rb.invalid_option.__name__ + ' failed')
        if (rb.missing_parameter(c)):
            FailCasesList.append('The case ' + rb.missing_parameter.__name__ + ' failed')

        tolog("Start verifying chap")
        import chap
        if (chap.add_chap(c)):
            FailCasesList.append('The case ' + chap.add_chap.__name__ + ' failed')
        if (chap.list_chap(c)):
            FailCasesList.append('The case ' + chap.list_chap.__name__ + ' failed')
        if (chap.mod_chap(c)):
            FailCasesList.append('The case ' + chap.mod_chap.__name__ + ' failed')
        if (chap.del_chap(c)):
            FailCasesList.append('The case ' + chap.del_chap.__name__ + ' failed')
        if (chap.invalid_setting_for_chap(c)):
            FailCasesList.append('The case ' + chap.invalid_setting_for_chap.__name__ + ' failed')
        if (chap.invalid_option_for_chap(c)):
            FailCasesList.append('The case ' + chap.invalid_option_for_chap.__name__ + ' failed')
        if (chap.missing_parameter_for_chap(c)):
            FailCasesList.append('The case ' + chap.missing_parameter_for_chap.__name__ + ' failed')

        tolog('Start verifying user')
        import user
        if (user.add_mgmt_user(c)):
            FailCasesList.append('The case ' + user.add_mgmt_user.__name__ + ' failed')
        if (user.mod_mgmt_user(c)):
            FailCasesList.append('The case ' + user.mod_mgmt_user.__name__ + ' failed')
        if (user.add_snmp_user(c)):
            FailCasesList.append('The case ' + user.add_snmp_user.__name__ + ' failed')
        if (user.mod_snmp_user(c)):
            FailCasesList.append('The case ' + user.mod_snmp_user.__name__ + ' failed')
        if (user.add_nas_user(c)):
            FailCasesList.append('The case ' + user.add_nas_user.__name__ + ' failed')
        if (user.mod_nas_user(c)):
            FailCasesList.append('The case ' + user.mod_nas_user.__name__ + ' failed')
        if (user.list_user(c)):
            FailCasesList.append('The case ' + user.list_user.__name__ + ' failed')
        if (user.list_user_by_verbose_mode(c)):
            FailCasesList.append('The case ' + user.list_user_by_verbose_mode.__name__ + ' failed')
        if (user.del_user(c)):
            FailCasesList.append('The case ' + user.del_user.__name__ + ' failed')
        if (user.invalid_setting_for_user(c)):
            FailCasesList.append('The case ' + user.invalid_setting_for_user.__name__ + ' failed')
        if (user.invalid_option_for_user(c)):
            FailCasesList.append('The case ' + user.invalid_option_for_user.__name__ + ' failed')
        if (user.missing_parameter_for_user(c)):
            FailCasesList.append('The case ' + user.missing_parameter_for_user.__name__ + ' failed')

        tolog('Start verifying wcache')
        import wcache
        if (wcache.add_wcache_dedication(c)):
            FailCasesList.append('The case ' + wcache.add_wcache_dedication.__name__ + ' failed')
        if (wcache.mod_wcache(c)):
            FailCasesList.append('The case ' + wcache.mod_wcache.__name__ + ' failed')
        if (wcache.add_wcache_no_dedication(c)):
            FailCasesList.append('The case ' + wcache.add_wcache_no_dedication.__name__ + ' failed')
        if (wcache.list_wcache(c)):
            FailCasesList.append('The case ' + wcache.list_wcache.__name__ + ' failed')
        if (wcache.def_wcache(c)):
            FailCasesList.append('The case ' + wcache.def_wcache.__name__ + ' failed')
        if (wcache.invalid_setting_for_wcache(c)):
            FailCasesList.append('The case ' + wcache.invalid_setting_for_wcache.__name__ + ' failed')
        if (wcache.invalid_option_for_wcache(c)):
            FailCasesList.append('The case ' + wcache.invalid_option_for_wcache.__name__ + ' failed')
        if (wcache.missing_parameter_for_wcache(c)):
            FailCasesList.append('The case ' + wcache.missing_parameter_for_wcache.__name__ + ' failed')

        tolog('Start verifying rcache')
        import rcache
        if (rcache.add_rcache_by_one_pd(c)):
            FailCasesList.append('The case ' + rcache.add_rcache_by_one_pd.__name__ + ' failed')
        if (rcache.add_rcache_by_multiple_pd(c)):
            FailCasesList.append('The case ' + rcache.add_rcache_by_multiple_pd.__name__ + ' failed')
        if (rcache.list_rcache(c)):
            FailCasesList.append('The case ' + rcache.list_rcache.__name__ + ' failed')
        if (rcache.def_rcache(c)):
            FailCasesList.append('The case ' + rcache.def_rcache.__name__ + ' failed')
        if (rcache.invalid_setting_for_rcache(c)):
            FailCasesList.append('The case ' + rcache.invalid_setting_for_rcache.__name__ + ' failed')
        if (rcache.invalid_option_for_rcache(c)):
            FailCasesList.append('The case ' + rcache.invalid_option_for_rcache.__name__ + ' failed')
        if (rcache.missing_parameter_for_rcache(c)):
            FailCasesList.append('The case ' + rcache.missing_parameter_for_rcache.__name__ + ' failed')

        tolog('Start verifying sc')
        import sc
        if (sc.start_sc(c)):
            FailCasesList.append('The case ' + sc.start_sc.__name__ + ' failed')
        if (sc.list_sc(c)):
            FailCasesList.append('The case ' + sc.list_sc.__name__ + ' failed')
        if (sc.invalid_setting_for_sc(c)):
            FailCasesList.append('The case ' + sc.invalid_setting_for_sc.__name__ + ' failed')
        if (sc.invalid_option_for_sc(c)):
            FailCasesList.append('The case ' + sc.invalid_option_for_sc.__name__ + ' failed')
        if (sc.missing_parameter_for_sc(c)):
            FailCasesList.append('The case ' + sc.missing_parameter_for_sc.__name__ + ' failed')

        tolog('Start verifying perfstats')
        import perfstats
        if (perfstats.start_perfstats(c)):
            FailCasesList.append('The case ' + perfstats.start_perfstats.__name__ + ' failed')
        if (perfstats.list_perfstats(c)):
            FailCasesList.append('The case ' + perfstats.list_perfstats.__name__ + ' failed')
        if (perfstats.invalid_setting_parameter(c)):
            FailCasesList.append('The case ' + perfstats.invalid_setting_parameter.__name__ + ' failed')
        if (perfstats.invalid_option(c)):
            FailCasesList.append('The case ' + perfstats.invalid_option.__name__ + ' failed')
        if (perfstats.missing_parameter(c)):
            FailCasesList.append('The case ' + perfstats.missing_parameter.__name__ + ' failed')

        tolog('Start verifying ping')
        import ping
        # if (ping.iscsi_ping(c)):
        #     FailCasesList.append('The case ' + ping.iscsi_ping.__name__ + ' failed')
        # if (ping.mgmt_ping(c)):
        #     FailCasesList.append('The case ' + ping.mgmt_ping.__name__ + ' failed')
        # if (ping.fc_ping(c)):
        #     FailCasesList.append('The case ' + ping.fc_ping.__name__ + ' failed')
        if (ping.invalid_setting_parameter(c)):
            FailCasesList.append('The case ' + ping.invalid_setting_parameter.__name__ + ' failed')
        if (ping.invalid_option(c)):
            FailCasesList.append('The case ' + ping.invalid_option.__name__ + ' failed')
        if (ping.missing_parameter(c)):
            FailCasesList.append('The case ' + ping.missing_parameter.__name__ + ' failed')

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

        tolog("Start verifying ctrl")
        import ctrl
        if (ctrl.list_ctrl(c)):
            FailCasesList.append('The case ' + ctrl.list_ctrl.__name__ + ' failed')
        if (ctrl.list_ctrl_by_verbose_mode(c)):
            FailCasesList.append('The case ' + ctrl.list_ctrl_by_verbose_mode.__name__ + ' failed')
        if (ctrl.mod_ctrl(c)):
            FailCasesList.append('The case ' + ctrl.mod_ctrl.__name__ + ' failed')
        if (ctrl.clear_ctrl(c)):
            FailCasesList.append('The case ' + ctrl.clear_ctrl.__name__ + ' failed')
        if (ctrl.invalid_setting_for_ctrl(c)):
            FailCasesList.append('The case ' + ctrl.invalid_setting_for_ctrl.__name__ + ' failed')
        if (ctrl.invalid_option_for_ctrl(c)):
            FailCasesList.append('The case ' + ctrl.invalid_option_for_ctrl.__name__ + ' failed')
        if (ctrl.missing_parameter_for_ctrl(c)):
            FailCasesList.append('The case ' + ctrl.missing_parameter_for_ctrl.__name__ + ' failed')

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
            FailCasesList.append('The case ' + factorydefaults.verifyFactorydefaultsInvalidOption.__name__ + ' failed')
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
            FailCasesList.append('The case ' + password.verifyPasswordSpecifyInexistentUsername.__name__ + ' failed')
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

        tolog('Start verifying tz')
        import tz
        if (tz.list_tz(c)):
            FailCasesList.append('The case ' + tz.list_tz.__name__ + ' failed')
        if (tz.list_tz_detail(c)):
            FailCasesList.append('The case ' + tz.list_tz_detail.__name__ + ' failed')
        if (tz.mod_tz(c)):
            FailCasesList.append('The case ' + tz.mod_tz.__name__ + ' failed')
        if (tz.invalid_parameter_for_tz(c)):
            FailCasesList.append('The case ' + tz.invalid_parameter_for_tz.__name__ + ' failed')
        if (tz.invalid_option_for_tz(c)):
            FailCasesList.append('The case ' + tz.invalid_option_for_tz.__name__ + ' failed')
        if (tz.missing_parameter_for_tz(c)):
            FailCasesList.append('The case ' + tz.missing_parameter_for_tz.__name__ + ' failed')

    if len(FailCasesList) != 0:
        for f in FailCasesList:
            tolog(f)

    else:
        tolog("Failed to connect server after ptiflash.")

    c.close()
    ssh.close()


if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    BuildVerification(c)
    c.close()
