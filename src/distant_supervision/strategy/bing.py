import base64
import json
import os
import uuid

import urllib3
import urllib

def bing_query(id,query):
    bingUrl = 'https://api.datamarket.azure.com/Bing/SearchWeb/v1/Web'  # ?Query=%27gates%27&$top=10&$format=json'

    accountKey = 'Za3DcaKVzmNfucTGZWq+sfM8G93sWPjS3sgeKUg7z7Y'
    accountKeyEnc = bytes.decode(base64.b64encode(str.encode(accountKey + ":" + accountKey)))# + ':' + bytes.decode(base64.b64encode(str.encode(accountKey)))

    headers = {'Authorization': 'Basic '+accountKeyEnc}
    pathName = "data/distant_supervision/raw_queries"

    if not os.path.exists(pathName):
        print("creating dir " + pathName)
        os.makedirs(pathName)

    params = {
        'Query':"\'"+query+"\'",
        'Adult': "\'Strict\'",
        'WebFileType': "\'HTML\'",
    }


    http = urllib3.PoolManager()
    url = bingUrl + "?" + urllib.parse.urlencode(params) +"&$format=json"

    r = http.request('GET', url,headers=headers)

    filename = pathName + "/" + str(id) + ".json"
    content = json.loads(bytes.decode(r.data))
    with open(filename, 'w') as outfile:
        json.dump(content["d"]["results"], outfile)



if __name__ == "__main__":
    search_uuid = uuid.uuid1()
    bing_query(search_uuid,"testing test")