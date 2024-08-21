import sqlite3
import Interfaces.login_interfaces as interfaces
import Models.Users as Users
from Controllers.login_screen_actions import *
from Controllers.main_screen_actions import *

conn = None
cursor = None



def connect(path):
    global conn, cursor
    
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    conn.commit()
    return


def main():
    global conn, cursor
    exit_program = False

    path = input("Enter the relative path of the database you want to run the application on: ")
    # ./prj-db.db
    # ./test.db
    try:
        connect('prj-db.db')
    except:
        print("Problems accessing data base \"{}\"".format(path))
        exit()

    while True:
        user, exit_program = login_screen(conn, cursor)

        if not exit_program:
            main_screen(conn, cursor, user)
        else:
            break

    conn.commit()
    conn.close()
    return


if __name__ == "__main__":
    main()
