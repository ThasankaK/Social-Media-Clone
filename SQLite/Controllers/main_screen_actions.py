import sys
from datetime import datetime
import Interfaces.user_commands as user_commands
import Interfaces.user_search_commands as user_search_commands
import SQLs.users_queries as user_queries
import SQLs.tweets_queries as tweets_queries
import SQLs.follows_queries as follows_queries
import Controllers.search_users_actions as search_users_actions


def logout(conn, cursor, user):
    print(f"Thank you, {user.get_name()}, for using our social media app")
    conn.close()
    sys.exit(0)
    
    
def main_screen(conn, cursor, user):
    command = input (user_commands.commands)
    
    if command == '2':
        search_users_actions.search_for_users(conn, cursor, user)
        
    if command == '5':
        logout(conn, cursor, user)    