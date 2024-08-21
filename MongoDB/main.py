from pymongo import MongoClient
import Commands.users_commands as users_commands
import Controllers.home_screen as home_screen

def connect_mongodb(port):
    client = MongoClient('localhost', int(port))
    database = client["291db"]
    collections = database["tweets"]

    return collections

def main():
    port = input(users_commands.load_json_port_number) #27017 default
    
    while True:
        try:
            int(port)
            break
        except:
            port = input(users_commands.load_json_port_error_format)
    
    collections = connect_mongodb(port)
    home_screen.home_screen(collections)

if __name__ == "__main__":
    main()
