import datetime

from bol import app
from flask import render_template, request, flash, get_flashed_messages, session, redirect, url_for, abort, g

from bol.bd_exe import connect_db, FDataBase

''' меню'''
menu = [{'name': 'Главная', 'url': 'index'},{'name': 'Отзывы', 'url': 'like'},{'name': 'Услуги', 'url': 'uslugi'}
    ,{'name': 'Врачи', 'url': 'vrach'},{'name': 'Регистрация', 'url': 'registr'},{'name': 'Авторизация', 'url': 'login'}]

app.permanent_session_lifetime = datetime.timedelta(seconds=30)

bd_contact=[]
'''Главная'''
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Наша больничка', menu=menu)
'''БД'''
def rec(bd, f):
    print(f['username'])
    bd.append({'username': f['username'], 'message': f['message']})

'''профиль'''
@app.route('/profile/<username>' , methods=["POST", "GET"] )
def profile(username):
    db = get_db()
    db = FDataBase(db)
    if 'userlogged' not in session or session['userlogged'] != username:
        abort(401)
    return render_template('profile.html', title='Профиль', menu=menu, users = db.getUserById())
'''отзывы в БД'''
@app.route('/otzivi' , methods=["POST", "GET"] )
def otzivi():
    db = get_db()
    db = FDataBase(db)
    if request.method == "POST":
        if len(request.form['username']) > 2:
            flash('Отзыв принят', category='success')
            db.add_like(request.form['username'], request.form['email'], request.form['messege'])
        else:
            flash('Ошибка, мало символов', category='error')
    return render_template('otzivi.html', title='Профиль', menu=menu)
'''Подключение БД'''
def get_db():
    if not hasattr(g,'link_db'):
        g.link_db = connect_db()
    return g.link_db

'''Закрытие БД'''
@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'link_db'):
        g.link_db.close()
'''Регистрация'''
@app.route('/registr', methods=['POST', 'GET'])
def reg():
    db = get_db()
    db = FDataBase(db)
    if request.method == "POST":
        db.add_users(request.form['login'],request.form['password'])
    return  render_template('registr.html', title='Регистрация', menu=menu)
'''Авторизация'''
@app.route('/login', methods=['POST', 'GET'])
def login():
    db = get_db()
    db = FDataBase(db)
    if 'userlogged' in session:
        return redirect(url_for('profile', username=session['userlogged']))
    elif request.method == 'POST':
        for item in db.getUser():
            if item['login'] == request.form['login'] and item['password'] == request.form['password']:
                session['userlogged'] = request.form['login']
                username = session['userlogged']
                print(username)
                return redirect(url_for('profile', username = username))
        else:
            print('Ошибка')
    return render_template('login.html', title='Авторизация', menu=menu, data=db.getUser())
'''Отзывы на сайте'''
@app.route('/like')
def poluchotz():
    db = get_db()
    db = FDataBase(db)
    print(db.getlike())
    return render_template('like.html',title = 'Отзывы', menu=menu, like=db.getlike())
'''Услуги'''
@app.route('/uslugi')
def uslugi():
    db = get_db()
    db = FDataBase(db)
    print(db.getUsl())
    return render_template('uslugi.html', title='Услуги', menu=menu, uslugi=db.getUsl())
'''Состав'''
@app.route('/vrach')
def vrach():
    return render_template('sostav.html', title='2022 Forever',menu=menu)

