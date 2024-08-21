import sys
from datetime import datetime
import Interfaces.user_commands as user_commands
import Interfaces.user_search_commands as user_search_commands
import SQLs.users_queries as user_queries
import SQLs.tweets_queries as tweets_queries
import SQLs.follows_queries as follows_queries

def print_users(cursor, offset, keyword):
    cursor.execute(user_queries.username_search, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', offset))
    user_results = cursor.fetchall()
    
    for user_detail in user_results:
        print("User ID: " + str(user_detail[0]) + " - Name: " + user_detail[2] + " - Email: " + user_detail[3] + " - City: " + user_detail[4] + " - Timezone: " + str(user_detail[5]))


def see_user_details(conn, cursor, user):

    input_user_id = input(user_search_commands.detail_command)

    while True:
        try:
            int(input_user_id)
            break
        except:
            input_user_id  = input('User ID input cannot be converted to interger, try again!')
    
    cursor.execute(user_queries.get_single_user, (int(input_user_id), ))
    row = cursor.fetchone()

    if row == None:
        return
    
    cursor.execute(tweets_queries.tweet_count, (int(input_user_id), ))
    print(f"Number of tweets by ({int(input_user_id)}): {cursor.fetchall()[0][0]}")

    cursor.execute(follows_queries.follower_count, (int(input_user_id), ))
    print(f"Number of followers of ({int(input_user_id)}): {cursor.fetchall()[0][0]}")

    cursor.execute(follows_queries.follwee_count, (int(input_user_id), ))
    print(f"Number of users that ({int(input_user_id)}) follow: {cursor.fetchall()[0][0]}")

    offset = 0
    cursor.execute(tweets_queries.three_recent_tweets, (int(input_user_id), offset))
    print(f"{int(input_user_id)}'s three most recent tweets: {cursor.fetchall()}")
    
    while True:
        option = input(user_commands.follow_or_tweets)
        if option == '1':
            if user.get_usr() == input_user_id:
                print("You cannot follow yourself!")
            
            cursor.execute(follows_queries.check_follower, (int(input_user_id), user.get_usr()))
            follower = cursor.fetchone()
            
            if follower != None:
                print(f"You are already following {int(input_user_id)}\n")
            else:
                cursor.execute(follows_queries.follow_user, (user.get_usr(), int(input_user_id), datetime.now().date().strftime("%Y-%m-%d")))
                conn.commit()
                print(f"You are now following {int(input_user_id)}\n")

        elif option == '2':
            offset += 3
            cursor.execute(tweets_queries.get_tweets, (int(input_user_id),))
            print(cursor.fetchall())
        
        elif option == '3':
            break
        else:
            print("Invalid command! Try again!")


def search_for_users(conn, cursor, user):
    keyword = input(user_search_commands.ask_for_keyword)
    offset = 0

    print_users(cursor, offset, keyword)
    
    while True:
        command = input(user_search_commands.ask_for_command)
        if command == '1':
            offset += 5
            print_users(cursor, offset, keyword)
        elif command == '2':
            see_user_details(conn, cursor, user)
        elif command == '3':
            break
        else:
            print("Invalid command! Try again!")

            