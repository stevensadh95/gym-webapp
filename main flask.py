from flask import Flask, request, render_template,redirect,url_for
from .forms import SignInForm

from flask_login import LoginManager,UserMixin




import sql_connection as db


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('secret'))
    return render_template('login.html', error=error)


@app.route('/create_account')
def create_account():
    return render_template('/create_account.html')


# @app.route('/create_account', methods=['POST'])
# def my_form_post():
#     text = request.form['text']
#     processed_text = text.upper()
#     print (processed_text)
#     #return processed_text
#     return render_template('create_account.html')

if __name__ == "__main__":
    app.run()


# gymder user class definition for login
class User(UserMixin):
    def __init__(self,email,password):
        self._password=password
        self._email=email


