# -*- coding: utf-8 -*-
# Autor: christian
import requests
from pprint import pprint

def get_facebook_graph_fields(uid, token, fields=None):
    if not fields:
        fields = ['picture', 'email', 'name', 'age_range', 'link', 'gender', 'locale', 'verified']

    url = "https://graph.facebook.com/{0}?fields={1}&access_token={2}".format(
        uid, ",".join(fields), token
    )

    req = requests.get(url)
    data = req.json()
    if req.status_code != 200:
        raise Exception(data['error']['message'])
    return data

if __name__ == '__main__':
    uid = "489801714533350"
    token = "jASUobZMKJwkxNxHZ01C49OCKQV5Fsxf&code=AQB5zzjGteGdvW22q32v8BSl0A_YmsWJkzefo9HhRtaQNWFbvCoW-R7JtS_0V7gBL9DY4TGRNIiA-mArb4v8qcxAtln7b8FrqN-FioHUzfGlWwDejT9cnkwo3sYGckM0pPB-NDZvmZOovRu0O5K38g6QxAUKbpuHtkDHi-9fP-pptatihkLmS2UWI8JBU8MjJzbfQyPsSqkK_tomPNEN9QW5vCW934Qyug7UGn9dWYFurkCkZmZ8b8mGnIvCOF8Y_o3gVVuIjKLGofs2bTExRW7wyiA6QZ_21CWxFUK-5AVIB6kBDKGhdVYVvqwEO1Ft8yFHX7eBr2NVQd50w9RumupI&state=jASUobZMKJwkxNxHZ01C49OCKQV5Fsxf"
    print pprint(get_facebook_graph_fields(uid, token))
