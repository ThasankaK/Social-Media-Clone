import Commands.users_commands as users_commands
import Controllers.search_for_tweets as search_for_tweets
import Controllers.search_for_users as search_for_users
import Controllers.list_top_tweets as list_top_tweets
import Controllers.list_top_users as list_top_users
import Controllers.compose_tweets as compose_tweets

def home_screen(collections):
    while True:
        command = input(users_commands.home_screen_commands)

        if command == '1':
            search_for_tweets.search_for_tweets(collections)
        elif command == '2':
            search_for_users.search_for_users(collections)
        elif command == '3':
            list_top_tweets.list_top_tweets(collections)
        elif command == '4':
            list_top_users.list_top_users(collections)
        elif command == '5':
            compose_tweets.compose_tweets(collections)
        elif command == '6':
            break
        else:
            print("\nInvalid command, try again: ")
