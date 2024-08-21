from datetime import datetime
import Commands.users_commands as user_commands


def compose_new_tweet(collections):
    tweet_content = input(user_commands.compose_tweets_write_tweet)

    if tweet_content == '':
        print("\nTweet text cannot be empty!")
        return

    current_time = datetime.utcnow()
    formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S+00:00")

    collections.insert_one({"date": formatted_time, "content": tweet_content, "user": {"username": "291user"}})

    print("Tweet succesfully written")



def compose_tweets(collections):
    compose_new_tweet(collections)
    
    while True:
      action = input(user_commands.compose_tweets_write_tweet_next_actions)

      if action == '1':
        compose_new_tweet(collections)
      elif action == '2':
        return
      else:
        print("\nInvalid command, try again!\n")
