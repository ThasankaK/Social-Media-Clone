get_followers = "select usr, name\
                from follows, users\
                where flwee = (?)\
                and usr = flwer;"

check_follower = "select *\
                  from follows\
                  where flwee = ? and flwer = ?"

follower_count = "select count(*)\
                from follows\
                where flwee = (?)"

follwee_count = "select count(*)\
                from follows\
                where flwer = (?)"

follow_user = "insert into follows (flwer, flwee, start_date) values (?, ?, ?);"