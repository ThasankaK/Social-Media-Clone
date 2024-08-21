import os.path
import sys
import tkinter as tk
import sqlite3
from Models.Users import *
from getpass import getpass
from tkinter import font as tkFont
import Interfaces.login_interfaces as interfaces
import SQLs.users_queries as users_queries
import SQLs.login_queries as login_queries
from datetime import datetime
import sys
import Interfaces.user_commands as user_commands
import Interfaces.tweets as tweet_commands
import SQLs.tweets_queries as tweets_queries
import SQLs.hashtags_queries as hashtag_queries
import SQLs.mentions_queries as mentions_queries
import SQLs.follows_queries as follows_queries
import Interfaces.user_search_commands as user_search_commands

global conn, cursor

def id_generate(usr_ids) -> int:
    if len(usr_ids) == 0:
        return 1
    else:
        usr_id = 1

        for x in usr_ids:
            if x == usr_id:
                usr_id += 1
        return usr_id
    

def tid_generate(tweet_id) -> int:
    if len(tweet_id) == 0:
        return 1
    else:
        tid = 1

        for x in tweet_id:
            if x == tid:
                tid += 1
        return tid
    

def initial_screen(conn, cursor):

    login_frame.pack_forget()
    registration_frame.pack_forget()
    main_screen_frame.pack_forget()

    
    # to wipe all widgets currently in frame, to avoid multiple widgets spawning
    for widget in initial_frame.winfo_children():
        widget.destroy()

    welcome_text = tk.Label(
    initial_frame,
    text="Hello User, to one of the best social media apps ever!!\n"
         "Click one of these 3 buttons to proceed",
    anchor='center',
    justify='center'
    )
    welcome_text.pack()

    login_button = tk.Button(initial_frame, text="Login", command=lambda: login_action(conn, cursor, False))

    signup_button = tk.Button(initial_frame, text="Signup", command=lambda: signup_action(conn, cursor, Users, False, ''))
   
    exit_button = tk.Button(initial_frame, text="Exit", command=exit_action)
  
    # packing all the widgets
    for widget in initial_frame.winfo_children():
        widget.pack()

    initial_frame.pack(fill="both", expand=True)


def login_action(conn, cursor, error):
    initial_frame.pack_forget()
    registration_frame.pack_forget()

    for widget in login_frame.winfo_children():
        widget.destroy()

    login_label = tk.Label(login_frame, text="Please Enter Login Credentials") 

    if error:
        login_error_label = tk.Label(login_frame, text="Incorrect Username/Password", fg="red")
     
    username_label = tk.Label(login_frame, text="Username:")
    username_entry = tk.Entry(login_frame)

    login_password_label = tk.Label(login_frame, text="Password:")
    login_password_entry = tk.Entry(login_frame, show='*')

    login_submit_button = tk.Button(login_frame, text="Submit", command=lambda: get_login_values(conn, cursor, username_entry, login_password_entry))

    login_back_button = tk.Button(login_frame, text="Back", command = lambda: initial_screen(conn, cursor))

    for widget in login_frame.winfo_children():
        widget.pack()
        
    login_frame.pack()


def get_login_values(conn, cursor, username_entry, login_password_entry):

    username = username_entry.get()
    password = login_password_entry.get()
    print("Username:", username)
    print("Password:", password)

    cursor.execute(login_queries.login_query, (username, password))
    res = cursor.fetchone()

    if res == None:
        login_action(conn, cursor, True)
    else:
        main_screen(conn, cursor, Users(res[0], res[1], res[2], res[3], res[4], res[5]))


def signup_action(conn, cursor, Users, registered, usr_id):
    
    initial_frame.pack_forget()

    for widget in registration_frame.winfo_children():
        widget.destroy()

    registration_label = tk.Label(registration_frame, text="Registration") # title of registration view

    name_label = tk.Label(registration_frame, text="Name:")
    name_entry = tk.Entry(registration_frame)
    
    password_label = tk.Label(registration_frame, text="Password:")
    password_entry = tk.Entry(registration_frame, show='*')

    email_label = tk.Label(registration_frame, text="Email:")
    email_entry = tk.Entry(registration_frame)

    city_label = tk.Label(registration_frame, text="City:")
    city_entry = tk.Entry(registration_frame)
  
    timezone_label = tk.Label(registration_frame, text="Timezone:")
    timezone_entry = tk.Entry(registration_frame)
    if registered:
        registered_label = tk.Label(registration_frame, text="You have now registered!", fg="green")
        new_id_label = tk.Label(registration_frame, text=f"Your new User ID is {usr_id}. Please remember this number, it used to login.")
    else:
        register_button = tk.Button(registration_frame, text="Register", command=lambda: get_signup_values(
                                                        conn, cursor, Users, name_entry, password_entry, email_entry, city_entry, timezone_entry))
  
    registration_back_button = tk.Button(registration_frame, text="Back", command = lambda: initial_screen(conn, cursor))
    
    for widget in registration_frame.winfo_children():
        widget.pack()

    registration_frame.pack()


def get_signup_values(conn, cursor, Users, username_entry, password_entry, email_entry, city_entry, timezone_entry):
    cursor.execute(users_queries.users_list_queries)
    users_list = cursor.fetchall()
    usr_ids = [x[0] for x in users_list]
    usr_ids.sort()
    usr_id = id_generate(usr_ids)

    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    city = city_entry.get()
    timezone = timezone_entry.get()

    print("Username:", username)
    print("Password:", password)
    print("email", email)
    print("CIty", city)
    print("timezone", timezone)

    cursor.execute(login_queries.signup_query, (usr_id, password, username, email, city, float(timezone)))
    conn.commit()
    signup_action(conn, cursor, Users, True, usr_id)
    print("Your new user ID is: " + str(usr_id))


def exit_action():
    window.destroy()


def main_screen(conn, cursor, Users):

    initial_frame.pack_forget()
    login_frame.pack_forget()
    registration_frame.pack_forget()
    compose_tweet_frame.pack_forget()
    search_tweets_frame.pack_forget()
    searched_tweets_frame.pack_forget()

    list_followers_frame.pack_forget()

    for widget in main_screen_frame.winfo_children():
        widget.destroy()

    search_tweets_button = tk.Button(main_screen_frame, text="Search for tweets", command=lambda:search_tweets(conn,cursor, Users, ""))

    search_users_button = tk.Button(main_screen_frame, text="Search for users", command=lambda:search_users(conn, cursor, Users))
    
    compose_tweet_button = tk.Button(main_screen_frame, text="Compose a tweet", command=lambda: compose_tweet(conn, cursor,  Users, '', '', '','','ms', 'n'))

    list_followers_button = tk.Button(main_screen_frame, text="List all followers", command=lambda:list_followers(conn, cursor, Users))

    logout_button = tk.Button(main_screen_frame, text="Logout", command=lambda:logout(conn, cursor, Users))

    for widget in main_screen_frame.winfo_children():
        widget.pack()

    main_screen_frame.pack()


def search_tweets(conn, cursor, Users, flag):
    main_screen_frame.pack_forget()
    searched_tweets_frame.pack_forget()

    for widget in search_tweets_frame.winfo_children():
        widget.destroy()
        
    search_tweets_label = tk.Label(search_tweets_frame, text="Enter the keyword you want to search for")
    search_tweets_entry = tk.Entry(search_tweets_frame)
    search_tweets_button = tk.Button(search_tweets_frame, text="Search",  command=lambda:search_tweet_keywords(conn, cursor, Users, search_tweets_entry.get(), '', 0))

    back_button = tk.Button(search_tweets_frame, text="Back", command=lambda:main_screen(conn, cursor, Users))
    for widget in search_tweets_frame.winfo_children():
        widget.pack()

    search_tweets_frame.pack()
  

def search_tweet_keywords(conn, cursor, Users, keywords_input, shown_tweets, offset):

    search_tweets_frame.pack_forget()
    tweet_info_frame.pack_forget()

    for widget in searched_tweets_frame.winfo_children():
        widget.destroy()

    keywords = list(keywords_input.split(' '))
    conditions = ''

    for keyword in keywords:
        if keyword == '':
            continue
        elif keyword[0] == '#':
            conditions += ' or m1.term = \'{}\' collate nocase'.format(keyword[1::])
        else:
            conditions += ' or t1.text like \'%{}%\' collate nocase'.format(keyword)

    cursor.execute(tweets_queries.search_tweets.format(conditions), (offset, ))
    current_tweets_list = cursor.fetchall()

    if shown_tweets != '':
        select_shown_tweet_label = tk.Label(searched_tweets_frame, text="Click on a tweet to see more details")
        for shown_tweet in shown_tweets:
            shown_tweet_button = tk.Button(searched_tweets_frame, text=shown_tweet[3])


    if not current_tweets_list and offset == 0:

        no_tweets_label = tk.Label(searched_tweets_frame, text="There exists no tweets with those keywords", fg = 'red')
    elif not current_tweets_list and offset != 0:
        
        no_more_label = tk.Label(searched_tweets_frame, text="There exists no more tweets with those keywords", fg = 'red')
    
    else:

        select_tweet_label = tk.Label(searched_tweets_frame, text="Click on a tweet to see more details")

        for tweet in current_tweets_list:
            tweet_text_button = tk.Button(searched_tweets_frame, text=tweet[3], command=lambda:tweet_info(conn, cursor, Users, keywords_input, shown_tweets, offset, tweet[0], ''))

        show_more_tweets_button = tk.Button(searched_tweets_frame, text="Show more tweets (5 more)", command=lambda:search_tweet_keywords(conn, cursor, Users, keywords_input, current_tweets_list, offset = offset + 5))

    back_to_search_button = tk.Button(searched_tweets_frame, text="Return to search", command=lambda:search_tweets(conn, cursor, Users, ""))

    back_to_main_menu_button = tk.Button(searched_tweets_frame, text="Return to main menu", command=lambda:main_screen(conn, cursor, Users))
    
    for widget in searched_tweets_frame.winfo_children():
        widget.pack()



    searched_tweets_frame.pack()


def tweet_info(conn, cursor, Users, keywords_input, shown_tweets, offset, tweet_id, flag):
    searched_tweets_frame.pack_forget()
    compose_tweet_frame.pack_forget()

    for widget in tweet_info_frame.winfo_children():
        widget.destroy()


    cursor.execute(tweets_queries.get_tweet_info, (tweet_id, ))
    current_tweet_info = cursor.fetchone()


    # if current_tweet_info == None:
    #     no_tweet_info_label = tk.Label(tweet_info_frame, text="There is no ")
    #     return

    current_tweet_writer = tk.Label(tweet_info_frame, text=f"Writer: {current_tweet_info[1]}")
    current_tweet_date = tk.Label(tweet_info_frame, text=f"Date: {current_tweet_info[2]}")
    current_tweet_text = tk.Label(tweet_info_frame, text=f"Text: {current_tweet_info[3]}")
    current_tweet_reply_to = tk.Label(tweet_info_frame, text=f"Reply To: {current_tweet_info[4]}")
    current_tweet_retweets_count = tk.Label(tweet_info_frame, text=f"Retweets: {current_tweet_info[5]}")
    current_tweet_replies_count = tk.Label(tweet_info_frame, text=f"Replies: {current_tweet_info[6]}")

    tweets_interaction_label = tk.Label(tweet_info_frame, text="Choose what you would like to do with the tweet")

    retweet_button = tk.Button(tweet_info_frame, text="Retweet", command=lambda:retweet_tweet(conn, cursor, Users, keywords_input, shown_tweets, offset, tweet_id))
    if flag == "rt":
        retweeted_label = tk.Label(tweet_info_frame, text="You already retweeted this tweet!", fg ='red')
    elif flag == "nrt":
        retweeted_label = tk.Label(tweet_info_frame, text="You have now retweeted this tweet!", fg ='green')
    reply_button = tk.Button(tweet_info_frame, text="Reply", command=lambda:compose_tweet(conn, cursor, Users, keywords_input, shown_tweets, offset, tweet_id, return_to="ti", flag = 'r')) 
    
    back_button = tk.Button(tweet_info_frame, text="Back", command=lambda:search_tweet_keywords(conn, cursor, Users, keywords_input, shown_tweets, offset))

    for widget in tweet_info_frame.winfo_children():
        widget.pack()



    tweet_info_frame.pack()


def retweet_tweet(conn, cursor, Users, keywords_input, shown_tweets, offset, tweet_id):
    cursor.execute(tweets_queries.get_retweet, (Users.get_usr(), tweet_id))
    existing_retweet = cursor.fetchone()
    
    if existing_retweet != None:
        tweet_info(conn, cursor, Users, keywords_input, shown_tweets, offset, tweet_id, flag="rt")
    else:
        tweet_info(conn, cursor, Users, keywords_input, shown_tweets, offset, tweet_id, flag="nrt")
        cursor.execute(tweets_queries.retweets_query, (Users.get_usr(), tweet_id, datetime.now().strftime('%Y-%m-%d')))
        conn.commit()    
    

def search_users(conn, cursor, Users):

    main_screen_frame.pack_forget()

    search_keyword_label = tk.Label(search_users_frame, text="Please enter a keyword")
    search_entry = tk.Entry(search_users_frame)
    search_button = tk.Button(search_users_frame, text="Search", command=lambda:list_searched_users(conn, cursor, Users, search_entry))


    for widget in search_users_frame.winfo_children():
        widget.pack()

    search_users_frame.pack()


def list_searched_users(conn, cursor, Users, search_entry):
    search_users_frame.pack_forget()

    keyword = search_entry.get()

    cursor.execute(users_queries.username_search, [Users.get_usr(), keyword])
    user_results = cursor.fetchall()
    
    cursor.execute(users_queries.city_search, [Users.get_usr(), keyword])
    city_results = cursor.fetchall()

    for users in city_results:
        if users not in user_results:
            user_results.append(users)
    

    shown = 0
    keep_searching = True
    i = 0

    while True:
        shown = 0
        for n in range(5):
            if shown <= 5 and (len(user_results) - i) != 0:
                user_result_label = tk.Label(list_searched_users_frame, text=user_results[i]['name'])
                # print (user_results[i]['name'])
                shown += 1  
                i += 1
            else:
                while True:
                    if (len(user_results) - i) > 0:
                        ask_for_command_1 = "Please enter a number corresponding to the task you want to do: \n\
                   1. Show more\n\
                   2. User details\n\
                   3. Logout\n"
                        see_user_details_button = tk.Button(list_searched_users_frame, text="User Details", command=lambda: see_user_details(conn,
                        cursor, Users, i , user_results, shown))
                        command = input(user_search_commands.ask_for_command_1)
                        if command == '1':
                            shown = 0
                        elif command == '2':
                            see_user_details(conn, cursor, user, i, user_results, shown)
                        elif command == '3':
                            logout(conn, cursor, user)
                        else:
                            print("Invalid command! Try again!")
                    else:
                        command = input(user_search_commands.ask_for_command_2)
                        if command == '1':
                            see_user_details(conn, cursor, user, i, user_results, shown)
                        elif command == '2':
                            logout(conn, cursor, Users)
                        else:
                            print("Invalid command! Try again!")
    for widget in list_searched_users_frame.winfo_children():
        widget.pack()
    list_searched_users_frame.pack()


def see_user_details(conn, cursor, Users, i, user_results, shown): 
    print(5)


def compose_tweet(conn, cursor, Users, keywords_input, shown_tweets, offset, tweet_id, return_to, flag):

    main_screen_frame.pack_forget()
    tweet_info_frame.pack_forget()

    for widget in compose_tweet_frame.winfo_children():
        widget.destroy()
    
    if flag == 're':
        write_tweet_label = tk.Label(compose_tweet_frame, text="Write a reply here")
        write_tweet_entry = tk.Entry(compose_tweet_frame)
        error_tweet_label = tk.Label(compose_tweet_frame, text="You can not write an empty reply", fg='red')

    elif flag == "rw":
        write_tweet_label = tk.Label(compose_tweet_frame, text="Write a reply here")
        write_tweet_entry = tk.Entry(compose_tweet_frame)
        tweet_written_label = tk.Label(compose_tweet_frame, text="You have successfully written a reply", fg='green')

    elif flag == "ne":
        write_tweet_label = tk.Label(compose_tweet_frame, text="Write a tweet here")
        write_tweet_entry = tk.Entry(compose_tweet_frame)
        error_tweet_label = tk.Label(compose_tweet_frame, text="You can not write an empty tweet", fg='red')

    elif flag == "nw":
        write_tweet_label = tk.Label(compose_tweet_frame, text="Write a tweet here")
        write_tweet_entry = tk.Entry(compose_tweet_frame)
        tweet_written_label = tk.Label(compose_tweet_frame, text="You have successfully written a tweet", fg='green')
    elif flag == "n":
        write_tweet_label = tk.Label(compose_tweet_frame, text="Write a tweet here")
        write_tweet_entry = tk.Entry(compose_tweet_frame)
    elif flag == "r": 
        write_tweet_label = tk.Label(compose_tweet_frame, text="Write a reply here")
        write_tweet_entry = tk.Entry(compose_tweet_frame)

    submit_tweet_button = tk.Button(compose_tweet_frame, text="Submit", command=lambda: get_tweet_values(conn, cursor, Users, keywords_input, shown_tweets, offset, tweet_id, return_to, write_tweet_entry, flag))
    if return_to == "ms":
        compose_tweets_back_button = tk.Button(compose_tweet_frame, text="Back", command=lambda: main_screen(conn, cursor, Users))
    elif return_to == "ti":
        tweet_info_back_button = tk.Button(compose_tweet_frame, text="Back", command=lambda:tweet_info(conn, cursor, Users, keywords_input, shown_tweets, offset, tweet_id, flag))

    
    for widget in compose_tweet_frame.winfo_children():
        widget.pack()

    compose_tweet_frame.pack()


def get_tweet_values(conn, cursor, Users, keywords_input, shown_tweets, offset, tweet_id, return_to, tweet_entry, flag):

    tweet = tweet_entry.get()
    if tweet == '' or tweet == None:
        if flag == "r":
            compose_tweet(conn, cursor, Users, keywords_input, shown_tweets, offset, tweet_id, return_to="ti", flag ="re")
        else:
            compose_tweet(conn, cursor, Users, keywords_input, shown_tweets, offset, tweet_id, return_to="ms", flag = "ne")
    else:
    

        if '#' in tweet:
            hashtags_in_text = hashtag_creation(conn, cursor, tweet)

        cursor.execute(tweets_queries.all_tweets)

        tweet_list = cursor.fetchall()
        tweet_id_query = [x[0] for x in tweet_list]
        tweet_id_query.sort()
        tid = int(id_generate(tweet_id_query))

        cursor.execute(tweets_queries.new_tweet, (tid, Users.get_usr(), datetime.now().date().strftime("%Y-%m-%d"), tweet, None))
        conn.commit()

        if flag == "n":
            compose_tweet(conn, cursor, Users, keywords_input, shown_tweets, offset, tweet_id, return_to="ms", flag = "nw")
        else:
            compose_tweet(conn, cursor, Users, keywords_input, shown_tweets, offset, tweet_id, return_to="ti", flag = "rw")
        if '#' in tweet:
            create_mentions(conn, cursor, Users, tid, tweet, hashtags_in_text)


def hashtag_creation(conn, cursor, text):
    
    hashtags_in_text = []

    if '#' in text:
        text_split = text.split()
        for word in text_split:
            if word[0] == '#':
                hashtags_in_text.append(word[1:])
    else:
        pass

    cursor.execute(hashtag_queries.get_hashtags)

    existing_hastags = {row[0] for row in cursor.fetchall()}

    for hashtag in hashtags_in_text:
        if hashtag in existing_hastags:
            continue
        else:
            cursor.execute(hashtag_queries.insert_hashtags, (hashtag,))
            conn.commit()
    return hashtags_in_text


def create_mentions(conn, cursor, Users, tid, text, hashtags_in_text):
    for hashtag in hashtags_in_text:
        cursor.execute(mentions_queries.insert_into_mentions, (tid, hashtag))
        conn.commit()


def list_followers(conn, cursor, Users):

    main_screen_frame.pack_forget()
    
    list_details_frame.pack_forget()
    

    for widget in list_followers_frame.winfo_children():
        widget.destroy()

    cursor.execute(follows_queries.get_followers, (Users.get_usr(), ))
    followers = cursor.fetchall()

    for row in followers:
        followers_label = tk.Button(list_followers_frame, text=f"{row[0]}, {row[1]}", command=lambda:list_details(conn, cursor, Users, row[0], row[1]))

    if not followers:
        no_followers_label = tk.Label(list_followers_frame, text="You have no followers.")

        # return_button = tk.Button(list_followers_frame, text="Back", command=lambda: main_screen(conn, cursor, Users))

        list_followers_frame.pack()

    back_button = tk.Button(list_followers_frame, text="Back", command=lambda:main_screen(conn, cursor, Users))

    for widget in list_followers_frame.winfo_children():
        widget.pack()

    list_followers_frame.pack()

    print(followers)


def list_details(conn, cursor, Users, follower_id, follower_name, flag = 0):
    list_followers_frame.pack_forget()
    see_more_tweets_frame.pack_forget()

    for widget in list_details_frame.winfo_children():
        widget.destroy()

    cursor.execute(tweets_queries.tweet_count, (follower_id, ))

    list_tweet_count = tk.Label(list_details_frame, text=f"Number of tweets by {follower_name}: {cursor.fetchall()[0][0]}\n")

    cursor.execute(follows_queries.follower_count, (follower_id, ))

    list_follower_count = tk.Label(list_details_frame, text=f"Number of followers {follower_name} has: {cursor.fetchall()[0][0]}\n")

    cursor.execute(follows_queries.followee_count, (follower_id, ))
    list_followee_count = tk.Label(list_details_frame, text=f"Number of users that {follower_name} follows: {cursor.fetchall()[0][0]}\n")

    # might have 3 oldest tweets
    cursor.execute(tweets_queries.three_recent_tweets, (follower_id, 0))

    result = cursor.fetchall()
    three_recent_tweets = ''
    for tple in result:
        three_recent_tweets += tple[0] + ", "
    

    list_three_tweets = tk.Label(list_details_frame, text=f"{follower_name}'s three most recent tweets: {three_recent_tweets[:len(three_recent_tweets)-2]}\n")

    follow_button = tk.Button(list_details_frame, text=f"Follow {follower_name}", command=lambda:follow_follower(conn, cursor, Users, follower_id, follower_name))

    if flag == "f":
        already_following = tk.Label(list_details_frame, text=f"You already follow {follower_name}", fg="red")

    if flag == "nf":
        now_following = tk.Label(list_details_frame, text=f"You are now following {follower_name}", fg="green")

    see_more_tweets_button = tk.Button(list_details_frame, text="See more tweets", command=lambda:see_more_tweets(conn, cursor, Users, follower_id, follower_name, three_recent_tweets[:len(three_recent_tweets)-2], 0))

    back_button = tk.Button(list_details_frame, text="Back", command=lambda:list_followers(conn, cursor, Users))

    for widget in list_details_frame.winfo_children():
        widget.pack()

    list_details_frame.pack()


def follow_follower(conn, cursor, Users, follower_id, follower_name):
    cursor.execute(follows_queries.get_followers, (follower_id,))
    followers = cursor.fetchall()
    
    follower_ids = [follower[0] for follower in followers]
    
    if Users.get_usr() in follower_ids:
        flag = "f"
        list_details(conn, cursor, Users, follower_id, follower_name, flag)

    else:
        cursor.execute(follows_queries.follow_user, (Users.get_usr(), id, datetime.now().date().strftime("%Y-%m-%d")))
        conn.commit()
        list_details(conn, cursor, Users, follower_id, follower_name, "nf")


def see_more_tweets(conn, cursor, Users, follower_id, follower_name, shown_tweets, offset):
    list_details_frame.pack_forget()
    

    for widget in see_more_tweets_frame.winfo_children():
        widget.destroy()

    offset += 3

    cursor.execute(tweets_queries.three_recent_tweets, (follower_id, offset))
    result = cursor.fetchall()

    shown_tweets_label = tk.Label(see_more_tweets_frame, text=f"Tweets by {follower_name}")

    for ttext in shown_tweets.split(','):
        text_label = tk.Label(see_more_tweets_frame, text=ttext)
    three_tweets = ''

    for tple in result:
        shown_tweets += tple[0] + ", "
        three_tweets += tple[0] + ", "
    


    if not result:
        no_more_tweets = tk.Label(see_more_tweets_frame, text="User has no more tweets", fg='red')

    else:
        three_more_tweets_label = tk.Label(see_more_tweets_frame, text=f"Three more tweets: {three_tweets[:len(three_tweets)-2]}")

        see_more_tweets_button = tk.Button(see_more_tweets_frame, text="See more tweets", command=lambda:see_more_tweets(conn, cursor, Users, follower_id, follower_name, shown_tweets[:len(shown_tweets)-2], offset))

    back_tweets_button = tk.Button(see_more_tweets_frame, text="Back", command=lambda:list_details(conn, cursor, Users, follower_id, follower_name , 0))

    for widget in see_more_tweets_frame.winfo_children():
        widget.pack()   

    see_more_tweets_frame.pack()


def logout(conn, cursor, Users):
    initial_screen(conn, cursor)



conn = sqlite3.connect('prj-db.db')
cursor = conn.cursor()
cursor.execute(' PRAGMA foreign_keys=ON; ')
conn.commit()   
exit_program = False

window = tk.Tk()
window.title("Social Media App")
window.attributes('-fullscreen', True)
custom_font = tkFont.nametofont("TkDefaultFont")
custom_font.configure(size=24)
window.option_add("*Font", custom_font)


initial_frame = tk.Frame(window)
login_frame = tk.Frame(window)
registration_frame = tk.Frame(window)
main_screen_frame = tk.Frame(window)
search_tweets_frame = tk.Frame(window)
search_users_frame = tk.Frame(window)
list_searched_users_frame = tk.Frame(window)
see_user_details_frame = tk.Frame(window)
compose_tweet_frame = tk.Frame(window)
list_followers_frame = tk.Frame(window)
list_details_frame = tk.Frame(window)
see_more_tweets_frame = tk.Frame(window)
searched_tweets_frame = tk.Frame(window)
tweet_info_frame = tk.Frame(window)

initial_screen(conn, cursor)

window.mainloop()