PRAGMA foreign_keys=ON;

-- -- inserting into users table
-- insert into users values (6, 'admin', 'dsada', 'root@hahao.com', 'Edmonton', 3.0);
-- insert into users values (7, 'admin', 'anna', 'root@hahao.com', 'Edmonton', 3.0);
-- insert into users values (8, 'admin', 'kama', 'root@hahao.com', 'Edmonton', 3.0);
-- insert into users values (10, 'admin', 'baba', 'root@hahao.com', 'Edmonton', 3.0);
-- insert into users values (11, 'admin', 'wewe', 'root@hahao.com', 'Edmonton', 3.0);

INSERT INTO users (usr, pwd, name, email, city, timezone)
VALUES
  (1, 'password1', 'John Doe', 'john.doe@example.com', 'New York', -5.0),
  (2, 'password2', 'Alice Smith', 'alice.smith@example.com', 'Los Angeles', -8.0),
  (3, 'password3', 'Bob Johnson', 'bob.johnson@example.com', 'Chicago', -6.0),
  (4, 'password4', 'Eva Williams', 'eva.williams@example.com', 'Houston', -6.0),
  (5, 'password5', 'David Brown', 'david.brown@example.com', 'Miami', -5.0),
  (6, 'password6', 'Sophia Lee', 'sophia.lee@example.com', 'San Francisco', -8.0),
  (7, 'password7', 'James Wilson', 'james.wilson@example.com', 'Seattle', -8.0),
  (8, 'password8', 'Olivia Martin', 'olivia.martin@example.com', 'Dallas', -6.0),
  (9, 'password9', 'Daniel Garcia', 'daniel.garcia@example.com', 'Phoenix', -7.0),
  (10, 'password10', 'Mia Rodriguez', 'mia.rodriguez@example.com', 'Boston', -5.0),
  (11, 'password11', 'William Martinez', 'william.martinez@example.com', 'Atlanta', -5.0),
  (12, 'password12', 'Emily Brown', 'emily.brown@example.com', 'Denver', -7.0),
  (13, 'password13', 'Liam Davis', 'liam.davis@example.com', 'Philadelphia', -5.0),
  (14, 'password14', 'Ava Wilson', 'ava.wilson@example.com', 'Detroit', -5.0),
  (15, 'password15', 'Benjamin Anderson', 'benjamin.anderson@example.com', 'Minneapolis', -6.0),
  (16, 'password16', 'Emma Taylor', 'emma.taylor@example.com', 'San Diego', -8.0),
  (17, 'password17', 'Michael Hernandez', 'michael.hernandez@example.com', 'Austin', -6.0),
  (18, 'password18', 'Sofia Lewis', 'sofia.lewis@example.com', 'Las Vegas', -7.0),
  (19, 'password19', 'Jackson Clark', 'jackson.clark@example.com', 'Nashville', -6.0),
  (20, 'password20', 'Charlotte Young', 'charlotte.young@example.com', 'Portland', -8.0),
  (21, 'password21', 'Lucas Baker', 'lucas.baker@example.com', 'San Antonio', -6.0),
  (22, 'password22', 'Lily Mitchell', 'lily.mitchell@example.com', 'Raleigh', -5.0),
  (23, 'password23', 'Henry Adams', 'henry.adams@example.com', 'Orlando', -5.0),
  (24, 'password24', 'Grace White', 'grace.white@example.com', 'Salt Lake City', -7.0),
  (25, 'password25', 'Alexander King', 'alexander.king@example.com', 'Tampa', -5.0);
