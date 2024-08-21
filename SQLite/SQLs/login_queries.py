signup_query = 'insert into users values (?, ?, ?, ?, ?, ?)'

login_query = 'select *\
                from users\
                where usr = ? and pwd = ?'
