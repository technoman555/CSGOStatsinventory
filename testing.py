import json
import urllib3
urllib3.disable_warnings()
http = urllib3.PoolManager()
itemname = []
res = http.request('GET','http://steamcommunity.com/inventory/76561198114654084/730/2?l=english&count=5000')
data= json.loads(res.data.decode('utf-8'))
for x in range(len(data['descriptions'])):
    itemname.append(data['descriptions'][x]['market_hash_name'])

res = http.request('GET','http://api.csgofast.com/price/all')
data= json.loads(res.data.decode('utf-8'))
for x in itemname:
    try:
       print(data[x])
    except KeyError:
        print('no value found')
        continue








