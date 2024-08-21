select *
            from (
                select DISTINCT *
                from (select *
                      from users
                      ORDER BY length(name) ASC)
                where name LIKE '%a%' collate nocase
                
                union
                
                select DISTINCT *
                from (select *
                      from users
                      ORDER BY length(city) ASC)
                where city LIKE '%a%' collate nocase and name not like '%a%' collate nocase)
            limit 5 offset 5;

select DISTINCT *
                from (select *
                      from users
                      ORDER BY length(name) ASC) as u1
                where u1.name LIKE '&a%' collate nocase;

select *
                      from users
                       where name LIKE '%a%' collate nocase;