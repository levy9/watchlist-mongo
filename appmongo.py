from flask import Flask, url_for, escape, render_template, request, redirect, flash
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from datetime import datetime, timedelta
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

class MongoDBfile(object):
    def __init__(self, dbname, collectionname, ip):
        self.InitMongoDBConnect(dbname, collectionname, ip)
    # 初始化 MongoDB 的连接
    def InitMongoDBConnect(self, dbname, collectionname, ip):
        # 数据库 ip 地址和端口号
        # 数据库 ip 地址和端口号
        # connection = MongoClient('localhost', 27017)
        splitsign = ':'
        if splitsign in ip:
            iplist = ip.split(splitsign)
            realip = iplist[0]
            realport = int(iplist[1])
        else:
            realip = ip
            realport = 27017
        connection = MongoClient(realip, realport, tz_aware=True)
        # print(connection.server_info())
        # db_name
        db = connection[dbname]
        # document_name
        self.collection = db[collectionname]

    def FindAllRawValue(self, starttime, endtime):
        #print('ready to find!')

        if self.collection.count_documents({'updatetime': {"$gte": starttime, "$lte": endtime}}) > 0:
            rawalldata = self.collection.find({'updatetime': {"$gte": starttime, "$lte": endtime}})
            df = pd.DataFrame(list(rawalldata))
            #print(df)
            return True, df
        else:
            return False, 0
    def FindRoverList(self, basetag):
        countN = self.collection.count_documents({'basetag': basetag, 'comment': {"$ne": "d"}})
        if countN > 0:
            data = self.collection.find({'basetag': basetag, 'comment': {"$ne": "d"}})
            return True, data
        else:
            return False, 0

    def FindBaseList(self):
        countN = self.collection.count_documents({'isbase': True, 'comment': {"$ne": "d"}})

        if countN > 0:
            data = self.collection.find({'isbase': True, 'comment': {"$ne": "d"}})
            return True, data
        else:
            return False, 0
    def findNotNullSettingList(self, item):
        rawstatusdata = self.collection.find({'$and': [{item: {'$ne': ''}}, {item: {'$exists': True}}, {'isbase': False}]})
        df = pd.DataFrame(list(rawstatusdata))
        roverlist = []
        #print(df)
        for index, row in df.iterrows():
            #print(row["stationid"], row["updatetime"])
            roverlist.append(row['stationid'])
        return roverlist

    def findNotNullSettingDictList(self, item):
        rawstatusdata = self.collection.find({'$and': [{item: {'$ne': ''}}, {item: {'$exists': True}}]})
        df = pd.DataFrame(list(rawstatusdata))
        roverlist = []
        #print(df)
        for index, row in df.iterrows():
            #print(row["stationid"], row["updatetime"])
            tempdict = {'stationid': row['stationid'], 'datainport': row['datainport'], 'comment': row['comment']}
            roverlist.append(tempdict)
        return roverlist

    def findSpecificSettingList(self, item, value):
        rawstatusdata = self.collection.find({item: value})
        df = pd.DataFrame(list(rawstatusdata))
        roverlist = []
        #print(df)
        for index, row in df.iterrows():
            #print(row["stationid"], row["updatetime"])
            roverlist.append(row['stationid'])
        return roverlist
    def FindRawValueEpoch(self, item, value, starttime, endtime):
        rawstatusdata = self.collection.find({item: value, 'datetime': {'$gte': starttime, '$lte': endtime}})
        df = pd.DataFrame(list(rawstatusdata))
        #print(df)
        return df
    def FindRawValue(self, item, value):
        rawstatusdata = self.collection.find({item: value})
        df = pd.DataFrame(list(rawstatusdata))
        #print(df)
        return df
    def FindFirstValue(self, item, value):
        handler = self.collection
        rows = handler.find({item: value}).sort('datetime', 1).limit(1)  # 倒序以后，只返回1条数据
        for row in rows:  # 这个循环只会执行1次
            #print(row)
            return [row['east'], row['north'], row['up']]

app = Flask(__name__)

app_dash = dash.Dash(__name__, server=app, url_base_pathname='/dashplot/')

a = os.getenv('TEST_ENV')
print('test value', a)

dburl = 'localhost:27017'
settinghelper = MongoDBfile('setting', 'stationstatus', dburl)

name = '睿光智云'

stations = settinghelper.findNotNullSettingDictList('stationid')
"""
products = [
    {'title': '北斗高精度监测接收机', 'price': '6000-12000RMB'},
    {'title': '高精度组合导航设备', 'price': '10000-90000RMB'},
    {'title': '5G DTU', 'price': '700-2500RMB'},
    {'title': 'GNSS高精度测量型天线', 'price': '500-1000RMB'},
    {'title': 'GNSS高精度扼流圈天线', 'price': '5000-15000RMB'},
]"""

starttime = datetime(2010, 11, 13, 0, 0, 0)
endtime = datetime.utcnow()
try:
    resulthelper = MongoDBfile('setting', 'stationstatus', dburl)
    isFind, places = resulthelper.FindAllRawValue(starttime, endtime)
    if isFind:
        token = 'pk.eyJ1IjoiYmlsbDU3NTMiLCJhIjoiY2toOTZ3ZmYyMGc4ZTJ6cWRyanM0aTRyNCJ9.uCK3ibcVt2oqE5PoKlgdrw'
        # token = 'pk.eyJ1IjoiYmlsbDU3NTMiLCJhIjoiY2toOTZ6OW9hMDYwODJ1cGpicWp1enk3byJ9.YCLzds-wdzUjoCLgBjDBZQ'
        fig = go.Figure(go.Scattermapbox(mode='markers',
                                         lon=places.lon,
                                         lat=places.lat,
                                         hovertext=places.stationid,
                                         hoverinfo='text'
                                         ))
        # fig.update_layout(mapbox={'accesstoken': token, 'style': 'outdoors'})
        # fig.update_layout(mapbox={'accesstoken': token, 'style': 'satellite'})
        fig.update_layout(mapbox={'accesstoken': token, 'style': 'satellite-streets'})
        #fig.show()
except Exception as e:
    print(Exception)

app_dash.layout = html.Div([
    dcc.Graph(figure=fig)
])


@app.route('/')
def index():
    #print(os.getcwd())
    #imagesrc = url_for('static', filename='images/totoro.gif', _external=True)
    #print(imagesrc)
    #print(type(products[0]))
    #return '<h1>Hello Totoro!</h1><img src=%s>' % imagesrc
    #return 'Welcome to My Watchlist!'
    return render_template('index.html', name=name, stations=stations)

@app.route('/test')
def test_url_for():
    print(url_for('user_page', name='yqy'))
    return 'Test Page'

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)

@app.errorhandler(404)
def page_not_found(e):
    name = 'rbadmin'
    return render_template('404.html'), 404

@app.context_processor
def inject_name():
    name = 'rbadmin2'
    return dict(name=name)

app_dash.run_server(host='0.0.0.0', debug=True)
#app.run()
#app.run(host='0.0.0.0', port=3000)