from Models.Users import *
from getpass import getpass
import Interfaces.login_interfaces as interfaces
import SQLs.users_queries as users_queries
import SQLs.login_queries as login_queries

def id_generate(get_single_user, cursor) -> int:
    usr_id = 1

    while True:
        cursor.execute(get_single_user, (usr_id, ))
        row = cursor.fetchone()
        if row == None:
            return usr_id
        else:
            usr_id += 1 


def signup(conn, cursor):
    usr_id = id_generate(users_queries.get_single_user, cursor)

    name = input("Enter your name: ")
    pwd = getpass(prompt = 'Enter the password: ')
    email = input("Enter email: ")
    city = input("Enter city: ")
    timezone = input("Enter timezone: ")

    while True:
        try:
            float(timezone)
            break
        except:
            timezone = input("Invalid timezone! Enter the timezone again: ")

    cursor.execute(login_queries.signup_query, (usr_id, pwd, name, email, city, float(timezone)))
    conn.commit()
    print("Your new user ID is: " + str(usr_id))


def login(cursor):
    while(True):
        usr = input("Enter unique usr id: ")
        pwd = getpass(prompt='Enter the password: ')

        cursor.execute(login_queries.login_query, (usr, pwd))
        res = cursor.fetchone()

        if res == None:
            print("User ID doesn't exist: try again!")
        else:
            return Users(res[0], res[1], res[2], res[3], res[4], res[5])
        

def login_screen(conn, cursor) -> Users:
    print(interfaces.welcome_text)

    while True:
        input_option = input(interfaces.options)

        if input_option.lower() == 'exit':
            return (None, True)

        elif input_option.lower() == 'login':
            user = login(cursor)
            return (user, False)
        
        elif input_option.lower() == 'signup':
            signup(conn, cursor)

        else:
            print('Unrecognizable command, try again!')
