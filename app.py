from flask import Flask, render_template, redirect, url_for, request,flash
from flask_sqlalchemy import SQLAlchemy
import tempfile
import os.path
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
from forms import SignupForm

app = Flask(__name__)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = '2305thgwiovhewncry83ufcnnd0dci329yt8fbw'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.sqlite'

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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm()

    if request.method == 'GET':
        return render_template("sign_up.html", form=form)
    if request.method == 'POST':
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
                return render_template("sign_up.html", form=form)

        else:
            flash("Form didn't validate", "danger")
            return redirect(url_for(register))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

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
                    return redirect(url_for("index"))
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


if __name__ == '__main__':
    init_db()
    app.run(port=5000, host='localhost', debug=True)


@app.route('/protected')
@login_required
def protected():
    return "protected area"



