from flask import Flask, url_for, escape
from dotenv import load_dotenv
import os

app = Flask(__name__)

a = os.getenv('TEST_ENV')
print('test value', a)

@app.route('/')
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'
    #return 'Welcome to My Watchlist!'

@app.route('/test')
def test_url_for():
    print(url_for('user_page', name='yqy'))
    return 'Test Page'

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)


app.run()