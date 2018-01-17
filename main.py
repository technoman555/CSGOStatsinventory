import json
import urllib3
from flask import *
http = urllib3.PoolManager()
app = Flask("Steamer")
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def search():
    userId= request.form['id']
    userId= userId.upper()
    return redirect(url_for('hello', name=userId))


@app.route('/inventory/<name>')
def hello(name=None):
    itemlist = []
    itemname = []
    itemPrice = []

    res = http.request('GET','http://steamcommunity.com/inventory/'+name+'/730/2?l=english&count=5000')
    data= json.loads(res.data.decode('utf-8'))
    if data is None:
        return render_template('bad.html')
    else:
        for x in range(len(data['descriptions'])):
            itemname.append(data['descriptions'][x]['market_hash_name'])
            itemlist.append(data['descriptions'][x]['icon_url'])
        res = http.request('GET', 'http://api.csgofast.com/price/all')
        data = json.loads(res.data.decode('utf-8'))
        for y in itemname:
            try:
                itemPrice.append(data[y])
            except KeyError:
                itemPrice.append("No Price found")
                continue
        count = len(itemlist)

        return render_template('hello.html', name=itemname ,list=itemlist, price=itemPrice ,count=count)

@app.route('/stats/<name>')
def stats(name=None):
    statsList = []
    res = http.request('GET', 'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=4943F4DBDC56C1DD5560EA8A396B8DD5&steamid='+name)
    data = json.loads(res.data.decode('utf-8'))
    for item in range(len(data['playerstats']['stats'])):
        statsList.append(data['playerstats']['stats'][item]['value'])
    return render_template('stats.html', stats=statsList)


if __name__ == '__main__':
    app.run()