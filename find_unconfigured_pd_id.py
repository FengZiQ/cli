# -*- coding: utf-8 -*-
# 2017.10.09

from remote import server
import json
from to_log import tolog


def find_pd_id(physical_capacity=None):

    pd_id = []

    try:

        pd_request = server.webapi('get', 'phydrv')

        if isinstance(pd_request, dict):

            pd_info = json.loads(pd_request["text"])

            str_pd_info = str(pd_info)

            # delete pool
            if 'Pool' in str_pd_info:

                vol_request = server.webapi('get', 'volume?page=1&page_size=100')

                if isinstance(vol_request, dict):

                    for vol in json.loads(vol_request["text"]):

                        if 'adv_role' in vol.keys() and vol['adv_role'] == 'Source' and vol['adv_type'] == 'Migration':
                            server.webapi('post', 'migrate/' + str(vol['id']) + '/stop', {"location": 1})

                        if vol['adv_type'] == 'Replication':

                            replica_request = server.webapi('get', 'replica')
                            if isinstance(replica_request, dict):
                                    for replica in json.loads(replica_request["text"]):
                                        server.webapi('post', 'replicaloc/' + str(replica["src_id"]) + '/stop')

                pool_response = server.webapi('get', 'pool')

                if isinstance(pool_response, dict):

                    pool_info = json.loads(pool_response["text"])

                    if len(pool_info) != 0:

                        for pool in pool_info:
                            server.webapiurl('delete', 'pool', str(pool['id']) + '?force=1')

                else:
                    tolog(str(pool_response))

            # delete spare
            if 'Spare' in str_pd_info:

                spare_response = server.webapi('get', 'spare')

                if isinstance(spare_response, dict):

                    spare_info = json.loads(spare_response["text"])

                    for spare in spare_info:

                        server.webapiurl('delete', 'spare', str(spare["id"]))

                else:

                    tolog(str(spare_response))

            # delete read cache
            if 'ReadCache' in str_pd_info:

                read_ache_response = server.webapi('get', 'rcache')

                if isinstance(read_ache_response, dict):

                    cache_info = json.loads(read_ache_response["text"])[0]["pd_list"][0]

                    sdd_id = cache_info["pd_id"]

                    server.webapi('post', 'rcache/detach', {"pd_list": [sdd_id]})

                else:
                    tolog(str(read_ache_response))

            # delete write cache
            if 'WriteCache' in str_pd_info:

                server.webapi('post', 'wcache/detach', {"id": 'detach'})

        else:
            tolog(str(pd_request))

        # find pd id
        pdResponse = server.webapi('get', 'phydrv')

        if isinstance(pdResponse, dict):

            pdInfo = json.loads(pdResponse["text"])

            if physical_capacity == None:

                for pd in pdInfo:
                    if pd["cfg_status"] == 'Unconfigured' and pd["media_type"] == 'HDD':
                        pd_id.append(pd["id"])

            elif physical_capacity == '2TB':

                for pd in pdInfo:
                    if pd["cfg_status"] == 'Unconfigured' and pd["physical_capacity"] == '2 TB' and pd["media_type"] == 'HDD':
                        pd_id.append(pd["id"])

            elif physical_capacity == '4TB':

                for pd in pdInfo:
                    if pd["cfg_status"] == 'Unconfigured' and pd["physical_capacity"] == '4 TB' and pd["media_type"] == 'HDD':
                        pd_id.append(pd["id"])

        else:
            tolog(str(pdResponse))

        pool_response1 = server.webapi('get', 'pool')

        ed_pool_info = json.loads(pool_response1['text'])

        for ed_pool in ed_pool_info:

            server.webapiurl('delete', 'pool', str(ed_pool['id']) + '?force=1')

    except:

        tolog('please check out physical drive ConfigStatus\n')

    return pd_id
