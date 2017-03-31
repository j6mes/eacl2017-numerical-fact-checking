import base64
import json
import os
import uuid

import urllib3
import urllib

def bing_query(id,query,retry=True, basedir =""):
    bingUrl = 'https://api.cognitive.microsoft.com/bing/v5.0/search' #'https://api.datamarket.azure.com/Bing/SearchWeb/v1/Web'  # ?Query=%27gates%27&$top=10&$format=json'

    accountKey = "80bf084915ca460e83d242a823349105" #"e3e25c820a9c43a6adccc0a56c553150" # 'Za3DcaKVzmNfucTGZWq+sfM8G93sWPjS3sgeKUg7z7Y'#"ZAk6G5VxGSD+K/mx3QH+PX24x85Cx9lEVnQzXA5H+P0" #
    accountKeyEnc = bytes.decode(base64.b64encode(str.encode(accountKey + ":" + accountKey)))# + ':' + bytes.decode(base64.b64encode(str.encode(accountKey)))

    headers = {'Authorization': 'Basic '+accountKeyEnc,'Ocp-Apim-Subscription-Key':accountKey}
    pathName = basedir+"data/distant_supervision/raw_queries"

    if not os.path.exists(pathName):
        print("creating dir " + pathName)
        os.makedirs(pathName)

    params = {
        'q':query,
        'count':500,
        'safesearch': "Moderate"
    }


    http = urllib3.PoolManager()
    url = bingUrl + "?" + urllib.parse.urlencode(params) +"&$format=json"

    r = http.request('GET', url,headers=headers)

    if r.status == 200:
        filename = pathName + "/" + str(id) + ".json"
        content = json.loads(bytes.decode(r.data))
        with open(filename, 'w') as outfile:
            try:
                json.dump(content["webPages"]['value'], outfile)
            except KeyError:
                if retry:
                    bing_query(id,query.replace("\"",""),False)


    else:
        print(r.status)
        print(r.data)
        raise RuntimeError("Error using bing api")


if __name__ == "__main__":
    search_uuid = uuid.uuid1()
    bing_query(search_uuid,"testing test")