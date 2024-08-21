import Commands.users_commands as users_commands
import json
import MongoDB.mongodb_queries as search_tweets_queries
import Controllers.home_screen as home_screen


def return_top_users(collections, n):

    try:
        users_cursor = collections.aggregate([
            # {"$match": {"user.username": {"$exists": True}, "user.displayname": {"$exists": True}, "user.followersCount": {"$exists": True}}},
            {"$match": {"user.followersCount": {"$exists": True}}},
            {"$group": {"_id": {"username": "$user.username", "id": "$user.id"}, "displayname": {"$first": "$user.displayname"}, "followersCount": {"$max": "$user.followersCount"}}},
            {"$sort": {"followersCount": -1}},
            {"$limit": int(n)}
        ])

        result = []
        users_list = list()

        for user in users_cursor:
            users_list.append(user)
            result.append(f"Username: {user.get('_id').get('username')}\nDisplayname: {user.get('displayname')}\nFollowers Count: {user.get('followersCount')}")
                
        print("\n")
        for i, user in enumerate(result):
            print(str(i + 1) + '.\n' + user.strip() + "\n")

        return users_list

    except Exception as e:
        return f"Error: {e}"


def see_user_details(collections, matched_users):
    index_input = input(users_commands.list_top_users_select_user_input)

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
    # user = collections.find_one({"user.id": matched_users[index_input-1].get("_id").get("id")}, {"user": 1, "_id": 0})
    
    user = list(list_user)[0]

    print('\n')
    for key in user.get("user"):
        print("{}: {}".format(key, user.get("user").get(key)))
    print('\n')


def display_users(listed_users):
    if listed_users:
        result = []
        for user in listed_users:
            result.append(f"Username: {user.get('_id').get('username')}\nDisplayname: {user.get('displayname')}\nFollowers Count: {user.get('followersCount')}")
            
    print("\n")
    for i, user in enumerate(result):
        print(str(i + 1) + '.\n' + user.strip() + "\n")


def list_top_users(collections):
    n = input(users_commands.list_top_users_n_users_input)

    try:
        int(n)
    except:
        print("\nInput provided for n is not an integern\n")
        return

    top_users = return_top_users(collections, n)    

    while True:
        more_details_choice = input(users_commands.list_top_users_see_more_details_of_user_input)

        if more_details_choice == "1":
            see_user_details(collections, top_users)
        elif more_details_choice == "2":
            return
        else: 
            print("\nInvalid command, try again: ")