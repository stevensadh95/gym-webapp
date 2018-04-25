

import re
from datetime import datetime


from flask import Flask, render_template, redirect, url_for, request,flash
from flask_sqlalchemy import SQLAlchemy
import tempfile
import os.path
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin,current_user
from forms import SignupForm,ProfileForm
import sqlite3



app = Flask(__name__)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

random_user = None


app.secret_key = '2305thgwiovhewncry83ufcnnd0dci329yt8fbw'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.sqlite'


def age_from_birthday(birthday):
    bdate = datetime.strptime(birthday,"%Y-%m-%d")
    today=datetime.today()
    return int((today - bdate).days/365)


@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(username=username).first()


def init_db():
    db.init_app(app)
    db.app = app
    db.create_all()


class User(db.Model, UserMixin):
    username = db.Column(db.String(80), primary_key=True, unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def get_id(self):
        return str(self.username)


class Profile():
    def __init__(self,username,name,email,state,sex,birthday,picture=None,bio=None):
        self.username = username
        self.name=name
        self.email=email
        self.state=state
        self.sex=sex
        self.birthday=birthday
        self.picture=picture
        self.bio=bio

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm()

    profile = ProfileForm()

    if request.method == 'GET':
        return render_template("sign_up.html", form=form,profile=profile)
    if request.method == 'POST':

        if profile.validate_on_submit():

            connection = sqlite3.connect('gymder.db')
            cursor = connection.cursor()

            if cursor.execute("SELECT * FROM user WHERE username='{}'".format(profile.username.data)).fetchall():
                flash("Username Already Exists", "danger")
                return redirect(url_for("register"))

            filename = profile.picture.data.filename

            profile.picture.data.save('static/uploads/' + filename)

            path = 'static/uploads/' + filename

            # user_profile = Profile(profile.username.data,profile.name.data,profile.email.data,profile.state.data,
            #         profile.sex.data,profile.birthday.data, profile.picture.data,profile.bio.data)
            # add_user(cursor,user_profile)

            user_profile = Profile(profile.username.data, profile.name.data, profile.email.data, profile.state.data,
                                   profile.sex.data, profile.birthday.data, path, profile.bio.data)
            add_user(cursor, user_profile)

            connection.commit()


        if form.validate_on_submit():
            if User.query.filter_by(username=form.username.data).first():
                flash("User Already Exists", "danger")
                return redirect(url_for("register"))
            else:
                new_user = User(form.username.data, form.password.data)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)

                flash("Registered successfully", "info")
                #return redirect(url_for("index"))
                #return render_template("sign_up.html", form=form,profile=profile)
                return redirect(url_for("index"))

        else:
            flash("Form didn't validate", "danger")
            return redirect(url_for(register))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/matches')
def match_list():
    username = current_user.username
    connection = sqlite3.connect('gymder.db')
    cursor = connection.cursor()

    #currently only returns one match only for some reason.
    matches = get_matches(cursor, username)

    #age = age_from_birthday(matches[0][5]) # need to figure out how to calculate age in template itself.

    connection.commit()
    return render_template("matches.html", username=username, matches=matches, getage=age_from_birthday)

@app.route('/profile')
def profile():
    username = current_user.username
    connection = sqlite3.connect('gymder.db')
    cursor = connection.cursor()

    user_info = get_user(cursor, username)
    age = age_from_birthday(user_info[5])
    return render_template("Profile.html", info=user_info, age=age)


def ret5():
    return 5

@app.route('/start_matching', methods=['GET','POST'])
def start_matching():
    username = current_user.username

    judge_user = ''
    global random_user

    if request.method == 'GET':
        connection = sqlite3.connect('gymder.db')
        cursor = connection.cursor()
        other_users = get_users_to_judge(cursor,username).fetchall()

        if not other_users:
            flash("No more users to match with",category="danger")
            return render_template("start_matching.html",other=None)

        random_user = other_users[0]
        age = age_from_birthday(random_user[5])

        connection.close()

        return render_template("start_matching.html", other=random_user,age=age)

    elif request.method == 'POST':
        connection = sqlite3.connect('gymder.db')
        cursor = connection.cursor()
        if request.form['submit'] == 'Yes':
            judge_user = 'Yes'
        elif request.form['submit'] == 'No':
            judge_user = 'No'

        like_user(cursor,username,random_user,judge_user)
        connection.commit()
        # process yes/no answer and add to match table
        return redirect(url_for('start_matching'))

    else:
        render_template("start_matching.html",other=None)


    # maybe use a generator here

    # def load_new_user():
    #     for user in other_users:
    #         yield user
    #     return render_template("start_matching.html", others = other_users)
    # for user in other_users:
    #     return render_template("matches.html", username=next(load_new_user))


    #age = age_from_birthday(matches[0][5])

    # connection.commit()
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SignupForm()

    if request.method == 'GET':
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if user.password == form.password.data:
                    login_user(user)
                    flash("logged in successfully", "success")
                    return redirect(url_for("profile"))
                else:
                    flash("password wrong", "danger")
                    return redirect(url_for("login"))
            else:
                flash("User does not exist","danger")
                return redirect(url_for("login"))
    else:
        return "form not validated"





# @app.route('/matches')
# @login_required
# def matches():
#     #user_id = get from session
#     #my_matches=get_matches(user_id)
#     return render_template("matches.html",profiles=my_matches)


# cursor.execute("""CREATE TABLE user(
#             username TEXT PRIMARY KEY, name TEXT, email TEXT, state TEXT, sex TEXT,
#             birthday DATE, picture BLOB, bio BLOB
#             )""")
#
# cursor.execute("""CREATE TABLE match(
#             username TEXT, other_id TEXT, likes text, date_judged DATE, judged TEXT
#             )""")


def add_user(cursor,p):
    cursor.execute('''INSERT INTO user(username,name,email,state,sex,birthday,picture,bio)
     VALUES (?,?,?,?,?,?,?,?)''', (p.username, p.name,p.email, p.state, p.sex, p.birthday, p.picture, p.bio))

# needs some work to determine which attributes to edit
def edit_user(cursor,user_id,name,**attributes):
    cursor.execute('''UPDATE user
    SET name='{}'
    WHERE user_id = {}'''.format(name, user_id))
    #connection.commit()


def like_user(cursor,user,other,isLiked):
    cursor.execute('''INSERT INTO match(username,other_id,likes)
         VALUES (?,?,?)''', (user, other[0], isLiked))
    #connection.commit()

'''
Returns matches that user has as tuples
'''

def get_matches(cursor,user):
    tuples = cursor.execute("""
    SELECT * from user where username IN
    (SELECT other_id FROM match WHERE username='{user}'
    AND likes='Yes' INTERSECT SELECT username FROM match WHERE other_id='{user}' AND likes='Yes')""".format(user=user)).fetchall()
    return tuples


def get_users_to_judge(cursor,username):
    return cursor.execute('''SELECT * from user where username = (SELECT username FROM user WHERE username != '{x}' AND username NOT IN
    (SELECT m.other_id FROM match m where m.username = '{x}'))'''.format(x = username))

def delete_user(cursor,username):
    cursor.execute("DELETE FROM user WHERE username = '{}'".format(username))
    delete_matches_by_username(cursor,username)
    #connection.commit()

def delete_matches_by_username(cursor,username):
    cursor.execute("DELETE FROM match WHERE username = '{}'".format(username))
    cursor.execute("DELETE FROM match WHERE other_id = '{}'".format(username))
    #connection.commit()

def get_user(cursor,username):
    return cursor.execute("SELECT * from user where username='{}'".format(username)).fetchall()[0]



#connection.commit() # need to commit changes.



# print("every user in DB")
# tuples = cursor.execute('''SELECT * from user''').fetchall()
# for tuple in tuples:
#     print(tuple)

# example call for add_user
# add_user('sadhwani', "steven","sadhwani@mail.usf.edu", "NH", "Male", "December 8 1995", "djk", " ffs)



# For debugging match table
# print(cursor.execute('''SELECT * from match''').fetchall())

# To test get_matches function against first DB element
# print(get_matches("<username>"))

#
# connection.close()


if __name__ == '__main__':
    init_db()
    app.run(port=5000, host='localhost', debug=True)


@app.route('/protected')
@login_required
def protected():
    return "protected area"



