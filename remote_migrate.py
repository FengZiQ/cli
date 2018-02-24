import json
from remote_113 import server


def precondition_for_migrate():

    pd_request_1 = server.webapi('get', 'phydrv')

    if isinstance(pd_request_1, dict):

        pd_info = json.loads(pd_request_1["text"])

        str_pd_info = str(pd_info)

        # delete pool
        if 'Pool' in str_pd_info:

            pool_response = server.webapi('get', 'pool')

            if isinstance(pool_response, dict):

                pool_info = json.loads(pool_response["text"])

                if len(pool_info) != 0:

                    for pool in pool_info:

                        server.webapiurl('delete', 'pool', str(pool['id']) + '?force=1')

    pd_request_2 = server.webapi('get', 'phydrv')

    if isinstance(pd_request_2, dict):

        pd_info = json.loads(pd_request_1["text"])

        pdId = [pd['id'] for pd in pd_info if pd['cfg_size'] >= 3000000]

        if len(pdId) > 0:

            server.webapi('post', 'pool', {"name": "p0", "pds": [pdId[1]], "raid_level": "raid0"})


def clean_up():

    server.webapiurl('delete', 'pool', '0?force=1')


if __name__ == "__main__":

    precondition_for_migrate()