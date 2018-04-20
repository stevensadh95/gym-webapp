import sqlite3
from flask import request,url_for,redirect,render_template

connection = sqlite3.connect('gymder.db')

cursor = connection.cursor()

# cursor.execute("""CREATE TABLE user(
#             username TEXT PRIMARY KEY, name TEXT, email TEXT, state TEXT, sex TEXT,
#             birthday DATE, picture BLOB, bio BLOB
#             )""")
#
# cursor.execute("""CREATE TABLE match(
#             username TEXT, other_id TEXT, likes text, date_judged DATE, judged TEXT
#             )""")


def add_user(username,name,email,state,sex,birthday,picture=None,bio=None):
    cursor.execute('''INSERT INTO user(username,name,email,state,sex,birthday,picture,bio)
     VALUES (?,?,?,?,?,?,?,?)''', (username, name,email, state, sex, birthday, picture, bio))

# needs some work to determine which attributes to edit
def edit_user(user_id,name,**attributes):
    cursor.execute('''UPDATE user
    SET name='{}'
    WHERE user_id = {}'''.format(name, user_id))
    connection.commit()


def like_user(user,other,isLiked):
    cursor.execute('''INSERT INTO match(username,other_id,likes)
         VALUES (?,?,?)''', (user, other, isLiked))
    connection.commit()

'''
Returns matches that user has as tuples
'''

def get_matches(user):
    tuples = cursor.execute("""
    SELECT * from user where username IN
    (SELECT other_id FROM match WHERE username='{user}'
    AND likes='Yes' INTERSECT SELECT username FROM match WHERE other_id='{user}' AND likes='Yes')""".format(user=user)).fetchall()

#     tuples = cursor.execute("""
# SELECT other_id FROM match WHERE username='{user}'
#         AND likes='Yes' INTERSECT SELECT username FROM match WHERE other_id='{user}' AND likes='Yes'""".format(
#         user=user)).fetchall()
    return tuples


def get_users_to_judge(username):
    return cursor.execute('''SELECT username FROM user WHERE username != {x} AND username NOT IN
    (SELECT m.other_id FROM match m where m.username = {x})'''.format(x = username))

def delete_user(username):
    cursor.execute("DELETE FROM user WHERE username = '{}'".format(username))
    delete_matches_by_username(username)
    connection.commit()

def delete_matches_by_username(username):
    cursor.execute("DELETE FROM match WHERE username = '{}'".format(username))
    cursor.execute("DELETE FROM match WHERE other_id = '{}'".format(username))
    connection.commit()

def get_user(username):
    return cursor.execute("SELECT * from user where username='{}'".format(username)).fetchall()


print("every user in DB")
tuples = cursor.execute('''SELECT * from user''').fetchall()
for tuple in tuples:
    print(tuple)

# example call for add_user
# add_user('sadhwani', "steven","sadhwani@mail.usf.edu", "NH", "Male", "December 8 1995", "djk", " ffs)

connection.commit() # need to commit changes.
#
# For debugging match table
print(cursor.execute('''SELECT * from match''').fetchall())

# delete_user("theBeast")
# delete_user("sadhwani")
#
# # To test get_matches function against first DB element
# print(get_matches("eddie"))


connection.close()


#to delete in b
# models.User.query.delete()