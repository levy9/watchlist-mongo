from flask import Flask, url_for, escape, render_template
from dotenv import load_dotenv
import os

app = Flask(__name__)

a = os.getenv('TEST_ENV')
print('test value', a)


name = '睿光智云'
products = [
    {'title': '北斗高精度监测接收机', 'price': '6000-12000RMB'},
    {'title': '高精度组合导航设备', 'price': '10000-90000RMB'},
    {'title': '5G DTU', 'price': '700-2500RMB'},
    {'title': 'GNSS高精度测量型天线', 'price': '500-1000RMB'},
    {'title': 'GNSS高精度扼流圈天线', 'price': '5000-15000RMB'},
]


@app.route('/')
def index():
    #print(os.getcwd())
    #imagesrc = url_for('static', filename='images/totoro.gif', _external=True)
    #print(imagesrc)
    #return '<h1>Hello Totoro!</h1><img src=%s>' % imagesrc
    #return 'Welcome to My Watchlist!'
    return render_template('index.html', name=name, products=products)

@app.route('/test')
def test_url_for():
    print(url_for('user_page', name='yqy'))
    return 'Test Page'

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)

app.run()
#app.run(host='0.0.0.0', port=3000)