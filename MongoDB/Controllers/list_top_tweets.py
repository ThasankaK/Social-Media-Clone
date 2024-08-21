import Commands.users_commands as users_commands
from Controllers.search_for_tweets import print_single_tweet, print_tweet_details

def select_field_sort():
    while True:
        selection = input(users_commands.list_top_tweets_select_field)

        if selection == '1':
            return 'retweetCount'
        elif selection == '2':
            return 'likeCount'
        elif selection == '3':
            return 'quoteCount'
        else:
            print("\nInvalid input option!\n")

def get_top_tweets(collections, field, n):
    index = 1
    top_tweets = list()

    return_tweets = collections.aggregate([
        {"$sort": {field: -1}},
        {"$limit": n}
    ])

    for tweet in return_tweets:
        print_single_tweet(tweet, index)
        index += 1
        top_tweets.append(tweet)

    return top_tweets


def list_top_tweets(collections):
    n = input(users_commands.list_top_tweets_get_n)

    try:
        int(n)
    except:
        print("\nInput provided for n is not an integern\n")
        return

    field = select_field_sort()
    top_tweets = get_top_tweets(collections, field, int(n))

    while True:
        next_command = input(users_commands.list_top_tweets_next_commands)

        if next_command == '1':
            print_tweet_details(top_tweets)
        elif next_command == '2':
            break
        else:
            print("\nUnrecognizable command input, try again!\n")

