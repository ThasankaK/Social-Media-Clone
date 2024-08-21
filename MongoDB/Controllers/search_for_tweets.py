import Commands.users_commands as users_commands
import json
import string
import MongoDB.mongodb_queries as mongodb_queries

punctuations_marks = list(string.punctuation + ' ')  #list(".,:;-‘?!''\"\"[](){}…") 

def keywords_preprocessing(keywords_all):
    keywords_all += " "
    keyword = ''
    keywords = []

    for i in keywords_all:
        if i not in punctuations_marks:
            keyword += i
        else:
            if keyword != '':
                keywords.append(keyword.lower())
                keyword = ''

    return keywords


def print_single_tweet(tweet, index):
    print("\n{}.\nID: {} \nDate: {} \nContent: {} \nFrom User: {}".format(
        index,
        tweet.get("id"),
        tweet.get("date")[:10] if tweet.get("date") is not None else None,
        tweet.get("content"),
        tweet.get("user").get("username")
        ))


def return_tweets(collections, keywords_all):
    keywords = keywords_preprocessing(keywords_all)
    conditions = []
    index = 1

    for keyword in keywords:
        conditions.append('{{"content": {{"$regex": "{}", "$options": "i"}}}}'.format(keyword))

    if len(keywords) == 0:
        return_tweets = collections.find({})
        matched_tweets = list()

        for tweet in return_tweets:
            print_single_tweet(tweet, index)
            matched_tweets.append(tweet)
            index += 1

    else:
        try:
            return_tweets = collections.aggregate([
                {"$match": json.loads(mongodb_queries.search_tweets_keywords.format(", ".join(conditions)))}
            ])
        except:
            return []

        matched_tweets = list()
        
        for tweet in list(return_tweets):
            if tweet.get("content") != None:
                tweet_contents_words = keywords_preprocessing(tweet.get("content"))
                contains_all = True

                for word in keywords:
                    if word not in tweet_contents_words:
                        contains_all = False
                        break
                
                if contains_all:
                    print_single_tweet(tweet, index)
                    matched_tweets.append(tweet)
                    index += 1

    return list(matched_tweets)



def print_tweet_details(matched_tweets):
    index_input = input(users_commands.search_for_tweets_index_input)

    try:
        int(index_input)
    except:
        print("\nIndex input is not an integer, try again!\n")
        return

    if int(index_input) < 1 or int(index_input) > len(matched_tweets):
        print("\nIndex input out of permissible range!\n")
        return

    print('\n')
    for key in matched_tweets[int(index_input)-1]:
        print(str(key) + ': ' + str(matched_tweets[int(index_input)-1].get(key)))
    print('\n')


def search_for_tweets(collections):
    while True:
        keywords_all = input(users_commands.search_for_tweets_keywords_input)
        matched_tweets = return_tweets(collections, keywords_all)


        while True:
            next_command = input(users_commands.search_for_tweets_next_actions)

            if next_command == '1':
                print_tweet_details(matched_tweets)
            elif next_command == '2':
                break
            elif next_command == '3':
                return
            else:
                print("\nInvalid command, try again!\n")
