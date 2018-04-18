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

def add_user(name,email,password,state,sex,birthday,picture=None,bio=None):
    cursor.execute('''INSERT INTO user(name,email,state,sex,birthday,picture,bio)
     VALUES (?,?,?,?,?,?,?)''', (name, email, state, sex, birthday, picture,bio))

# needs some work to determine which attributes to edit
def edit_user(user_id,name,**attributes):
    cursor.execute('''UPDATE user
    SET name='{}'
    WHERE user_id = {}'''.format(name, user_id))
    connection.commit()


def like_user(user,other,isLiked):
    cursor.execute('''INSERT INTO match(user_id,other_id,likes)
         VALUES (?,?,?)''', (user, other, isLiked))
    connection.commit()

'''
Returns matches that user has as tuples
'''

def get_matches(user):
    tuples = cursor.execute("""
    SELECT * from user where user_id=
    (SELECT other_id FROM match WHERE user_id={user}
    AND likes='Yes' INTERSECT SELECT user_id FROM match WHERE other_id={user} AND likes='Yes')""".format(user=user)).fetchall()
    return tuples


def get_users_to_judge(user_id):
    return cursor.execute('''SELECT user_id FROM user WHERE user_id != {x} AND user_id NOT IN
    (SELECT m.other_id FROM match m where m.user_id = {x})'''.format(x = user_id))

def delete_user(user_id):
    cursor.execute('''DELETE FROM user WHERE user_id = {}'''.format(user_id))
    delete_matches_by_user_id(user_id)

def delete_matches_by_user_id(user_id):
    cursor.execute('''DELETE FROM match WHERE user_id = {}'''.format(user_id))


# print("every user in DB")
# tuples = cursor.execute('''SELECT * from user''').fetchall()
# for tuple in tuples:
#     print(tuple)

# example call for add_user
#add_user('Steven Sadhwani', "sadhwani@mail.usf.edu", "NH", "Male", "December 8 1995", "djk")

connection.commit() # need to commit changes.

# For debugging match table
# print(cursor.execute('''SELECT * from match''').fetchall())

# To test get_matches function against first DB element
# print(get_matches("1"))


connection.close()