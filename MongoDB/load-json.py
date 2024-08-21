import Commands.users_commands as users_commands
import json
from pymongo import MongoClient


def connect_mongodb(port):
    client = MongoClient('localhost', int(port))
    database = client["291db"]
    
    if "tweets" in database.list_collection_names():
        database["tweets"].drop()

    collections = database["tweets"]

    return collections


def insert_data(file_stream, collections):
    end_of_file = False

    while not end_of_file:

        # Each data pack contains at most 1k entries
        data_pack = list()

        for _ in range(1000):
            line = file_stream.readline()

            if line == "":
                end_of_file = True
                break
            else:
                data_pack.append(json.loads(line.strip()))
        
        if data_pack:
            collections.insert_many(data_pack)


def main():
    json_file = input(users_commands.load_json_filename)
    port = input(users_commands.load_json_port_number)

    while True:
        try:
            file_stream = open(json_file, "r")
            break
        except:
            json_file = input(users_commands.load_json_file_error)

    while True:
        try:
            int(port)
            break
        except:
            port = input(users_commands.load_json_port_error_format)

    collections = connect_mongodb(port)
    insert_data(file_stream, collections)
    # collections.create_index({"id": 1, "user.id": 1, "content": "text"})
    collections.create_index({"id": 1, "user.id": 1, "content": "text", "user.location": "text", "user.displayname": "text"})


if __name__ == "__main__":
    main()