import json
import Commands.users_commands as users_commands
import MongoDB.mongodb_queries as mongodb_queries
from Controllers.search_for_tweets import keywords_preprocessing


def search_matched_users(collections, keywords):
    index = 1

    if len(keywords) == 0:
        matched_users = list()

        return_users = collections.aggregate([
            {"$group": {"_id": {"username": "$user.username", "id": "$user.id"}, "location": {"$first": "$user.location"}, "displayname": {"$first": "$user.displayname"}, "followersCount": {"$max": "$user.followersCount"}}},
        ])

        for user in return_users:
            print_single_user(user, index)
            matched_users.append(user)
            index += 1

    else:
        # return_users = collections.distinct("user.id", json.loads(mongodb_queries.search_for_users_distinct.format(", ".join(conditions))) )
        try:
            return_users = collections.aggregate([
                {"$match": {"$or": [{"user.displayname": {"$regex": "{}".format(keywords[0]), "$options": "i"}}, {"user.location": {"$regex": "{}".format(keywords[0]), "$options": "i"}}]}},
                {"$group": {"_id": {"username": "$user.username", "id": "$user.id"}, "location": {"$first": "$user.location"}, "displayname": {"$first": "$user.displayname"}, "followersCount": {"$max": "$user.followersCount"}}},
            ])
        except:
            return []

        matched_users = list()

        for user in return_users:
            # user = collections.find_one({"user.id": user_id}, {"user": 1, "_id": 0})
            matching_words = list()

            if user.get("displayname") != None or user.get("_id").get("location") != None:
                if user.get("displayname") != None:
                    matching_words.extend(keywords_preprocessing(user.get("displayname")))
                if user.get("location") != None:
                    matching_words.extend(keywords_preprocessing(user.get("location")))
                
                contains_all = True
                for word in keywords:
                    if word not in matching_words:
                        contains_all = False
                        break
                
                if contains_all:
                    print_single_user(user, index)
                    index += 1
                    matched_users.append(user)

    return matched_users


def print_single_user(user, index):
    print("\n{}.\nUsername: {}\nDisplay Name: {}\nLocation: {}\n".format(
        index,
        user.get("_id").get("username"),
        user.get("displayname"),
        user.get("location")
    ))



def see_user_details(collections, matched_users):
    index_input = input(users_commands.search_for_users_index_input)

    try:
        int(index_input)
    except:
        print("\nIndex input is not an integer!\n")
        return
    
    if int(index_input) < 1 or int(index_input) > len(matched_users):
        print("\nIndex input provided out of range!\n")
        return
    
    list_user = collections.aggregate([
        {"$match": {"user.id": matched_users[int(index_input)-1].get("_id").get("id")}},
        {"$sort": {"user.followersCount": -1}},
        {"$limit": 1}
        ])
    
    user = list(list_user)[0]

    print('\n')
    for key in user.get("user"):
        print("{}: {}".format(key, user.get("user").get(key)))
    print('\n')


def search_for_users(collections):
    while True:
        keyword_input = input(users_commands.search_for_users_keywords_input)
        keywords = keywords_preprocessing(keyword_input)

        matched_users = search_matched_users(collections, keywords)

        while True:
            next_command = input(users_commands.search_for_users_next_step)

            if next_command == "1":
                see_user_details(collections, matched_users)
            elif next_command == '2':
                break
            elif next_command == '3':
                return
            else:
                print("\nUnrecognizable command input, try again!\n")