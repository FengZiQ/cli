# -*- coding: utf-8 -*-
# 2017.10.09

from remote import server
import json


def find_pd_id(physical_capacity = None):

    pd_id = []

    pd_request = server.webapi('get', 'phydrv')
    pd_info = json.loads(pd_request["text"])

    for info in pd_info:

        # delete pool
        if 'Pool' in info["cfg_status"]:

            pool_response = server.webapi('get', 'pool')

            pool_info = json.loads(pool_response["text"])

            for pool in pool_info:
                server.webapiurl('delete', 'pool', str(pool['id']) + '?force=1')

        # delete spare
        elif 'Spare' in info["cfg_status"]:

            spare_response = server.webapi('get', 'spare')

            spare_info = json.loads(spare_response["text"])

            for spare in spare_info:

                server.webapiurl('delete', 'spare', str(spare["id"]))

        # delete read cache
        elif 'ReadCache' in info["cfg_status"]:

            read_ache_response = server.webapi('get', 'rcache')

            cache_info = json.loads(read_ache_response["text"])[0]["pd_list"][0]

            sdd_id = cache_info["pd_id"]

            server.webapi('post', 'rcache/detach', {"pd_list": [sdd_id]})

        # delete write cache
        elif 'WriteCache' in info["cfg_status"]:

            server.webapi('post', 'wcache/detach', {"id": 'detach'})

    # find pd id
    pdResponse = server.webapi('get', 'phydrv')
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

    return pd_id