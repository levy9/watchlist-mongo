from flask import Flask, url_for, escape, render_template
from dotenv import load_dotenv
import os

app = Flask(__name__)

a = os.getenv('TEST_ENV')
print('test value', a)


name = 'YQY'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]


@app.route('/')
def index():
    #print(os.getcwd())
    #imagesrc = url_for('static', filename='images/totoro.gif', _external=True)
    #print(imagesrc)
    #return '<h1>Hello Totoro!</h1><img src=%s>' % imagesrc
    #return 'Welcome to My Watchlist!'
    return render_template('index.html', name=name, movies=movies)

@app.route('/test')
def test_url_for():
    print(url_for('user_page', name='yqy'))
    return 'Test Page'

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)


app.run()