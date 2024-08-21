users_list_queries = 'select usr\
                      from users;'
                      
username_search  = \
            "select *\
            from (\
                select DISTINCT *\
                from (select *\
                      from users\
                      ORDER BY length(name) ASC)\
                where name LIKE ? collate nocase\
                \
                union\
                \
                select DISTINCT *\
                from (select *\
                      from users\
                      ORDER BY length(city) ASC)\
                where city LIKE ? collate nocase and name not like ? collate nocase)\
            limit 5 offset ?"

user_details = "select \
                from users as u, tweets as t, "

get_single_user = "select *\
                    from users\
                    where usr = ?"