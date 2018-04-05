import sqlite3
from flask import request,url_for,redirect,render_template

connection = sqlite3.connect('gymder.db')

cursor = connection.cursor()


# cursor.execute("""CREATE TABLE user(
#             user_id INTEGER PRIMARY KEY, password TEXT, name TEXT, email TEXT, state TEXT, sex TEXT,
#             birthday DATE, picture BLOB, bio BLOB
#             )""")
#
# cursor.execute("""CREATE TABLE match(
#             user_id TEXT, other_id TEXT, likes text, date_judged DATE, judged TEXT
#             )""")
#
# # for login verification.
#
# cursor.execute("""CREATE TABLE login(
#             email TEXT PRIMARY KEY NOT NULL, password TEXT NOT NULL
#             )""")

def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate_credentials(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('secret'))
    return render_template('login.html', error=error)

def validate_credentials(username, password):
    connection = sqlite3.connect('gymder.db')
    with connection:
                cur = connection.cursor()
                cur.execute("SELECT * FROM login")
                rows = cur.fetchall()
                for row in rows:
                    user_db = row[0]
                    password_db = row[1]
                    if user_db==username:
                        return password_db==password
    return False




def add_user(name,email,password,state,sex,birthday,picture=None,bio=None):
    cursor.execute('''INSERT INTO user(name,email,state,sex,birthday,picture,bio)
     VALUES (?,?,?,?,?,?,?)''', (name, email, state, sex, birthday, picture,bio))

    cursor.execute('''INSERT INTO login(email,password)
         VALUES (?,?)''', (email, password))


# needs some work to determine which attributes to edit
def edit_user(user_id,name,**attributes):
    cursor.execute('''UPDATE user
    SET name='{}'
    WHERE user_id = {}'''.format(name, user_id))
    connection.commit()


def match(user,other,isLiked):
    # if is_match(user,other):
    #     pass # handle match
    cursor.execute('''INSERT INTO match(user_id,other_id,likes)
         VALUES (?,?,?)''', (user, other, isLiked))

def like_user(user,other,isLiked):
    cursor.execute('''INSERT INTO match(user_id,other_id,likes)
         VALUES (?,?,?)''', (user, other, isLiked))


def is_match(user,other):
    user_likes_other = cursor.execute('''SELECT * FROM likes WHERE user_id={}
     AND other_id = {} and likes=yes'''.format(user,other))
    other_likes_user = cursor.execute('''SELECT * FROM likes WHERE user_id={}
     AND other_id = {} and likes=yes'''.format(other,user))
    return user_likes_other and other_likes_user


# should work
def get_users_to_judge(user_id):
    return cursor.execute('''SELECT user_id FROM user WHERE user_id != {x} AND user_id NOT IN
    (SELECT m.other_id FROM match m where m.user_id = {x})'''.format(x = user_id))

def delete_user(user_id):
    cursor.execute('''DELETE FROM user WHERE user_id = {}'''.format(user_id))

def delete_matches_by_user_id(user_id):
    cursor.execute('''DELETE FROM match WHERE user_id = {}'''.format(user_id))


x = cursor.execute('''SELECT * from match''')
for i in cursor:
    print("\n")
    for j in i:
        print(j)

print("Other Users not matched yet")
y = get_users_to_judge(2)

for i in y:
    for e in i:
        print(e)

print("every user in DB")

x = cursor.execute('''SELECT * from user''')
for i in cursor:
    print("\n")
    for j in i:
        print(j)

# example call for add_user
# add_user('Steven Sadhwani', "sadhwani@mail.usf.edu", "NH", "Male", "December 8 1995", "djk")
connection.commit() # need to commit changes.






# for printing all values separately from a query
# x = cursor.execute('''SELECT * from user where name="Steven Sadhwani"''')
# for i in cursor:
#     for j in i:
#         print(j)

connection.close()