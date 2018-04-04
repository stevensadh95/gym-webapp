import sqlite3

connection = sqlite3.connect('gymder.db')

cursor = connection.cursor()

# primary key auto increments without putting it there
# cursor.execute("""CREATE TABLE user(
#             user_id INTEGER PRIMARY KEY, name TEXT, email TEXT, state TEXT, sex TEXT,
#             birthday DATE, picture BLOB, bio BLOB
#             )""")
#
# cursor.execute("""CREATE TABLE match(
#             user_id TEXT, other_id TEXT, likes text, date_judged DATE, judged TEXT
#             )""")


def add_user(name,email,state,sex,birthday,picture=None,bio=None):
    cursor.execute('''INSERT INTO user(name,email,state,sex,birthday,picture,bio)
     VALUES (?,?,?,?,?,?,?)''', (name, email, state, sex, birthday, picture,bio))

def edit_user(user_id,name,**attributes):
    cursor.execute('''UPDATE user
    SET name='{}'
    WHERE user_id = {}'''.format(name, user_id))
    connection.commit()



def match(user,other,isLiked):
    if is_match(user,other):
        pass # handle match


def is_match(user,other):
    user_likes_other = cursor.execute('''SELECT * FROM likes WHERE user_id={}
     AND other_id = {} and likes=yes'''.format(user,other))
    other_likes_user = cursor.execute('''SELECT * FROM likes WHERE user_id={}
     AND other_id = {} and likes=yes'''.format(other,user))
    return user_likes_other and other_likes_user



edit_user(1,"Bilbo")

 # x = cursor.execute('''SELECT * from user where user_id=1''')
x = cursor.execute('''SELECT * from user''')
for i in cursor:
    print("\n")
    for j in i:
        print(j)

# example call for add_user
add_user('Steven Sadhwani', "sadhwani@mail.usf.edu", "NH", "Male", "December 8 1995", "djk")
connection.commit() # need to commit changes.






# for printing all values separately from a query
# x = cursor.execute('''SELECT * from user where name="Steven Sadhwani"''')
# for i in cursor:
#     for j in i:
#         print(j)

connection.close()