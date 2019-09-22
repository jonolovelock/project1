DROP DATABASE bookshop;

CREATE DATABASE bookshop
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_Australia.1252'
    LC_CTYPE = 'English_Australia.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

CREATE TABLE books (
  id SERIAL PRIMARY KEY,
  isbn VARCHAR NOT NULL,
  title VARCHAR NOT NULL,
  author VARCHAR NOT NULL,
  year INTEGER NOT NULL
);

-- User TABLE
CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username VARCHAR NOT NULL,
	firstname VARCHAR,
	lastname VARCHAR,
	email VARCHAR,
	password VARCHAR NOT NULL
);


-- Review TABLE

CREATE TABLE reviews (
	id SERIAL PRIMARY KEY,
	rating INTEGER NOT NULL,
	review VARCHAR NOT NULL,
	reviewer INTEGER references users,
	book INTEGER references books
);	



INSERT INTO users
  (username, firstname, lastname, email, password)
  VALUES ('jlove', 'Jono', 'Lovelock', 'jonolovelock@gmail.com', 'password');

INSERT INTO users
  (username, firstname, lastname, email, password)
  VALUES ('stu', 'Stu', 'Andrew', 'Stu@gmail.com', 'password'); 
 
  
INSERT INTO reviews
	(rating, review, reviewer, book)
	VALUES (5, 'Bloody great book I think everyone should read it', 1, 1);

INSERT INTO reviews
	(rating, review, reviewer, book)
	VALUES (0, 'What a piece of shit book', 2, 2);

Select b.title, r.rating, r.review, concat(u.firstname, u.lastname) as Reviewer from
	books as b join reviews as r
	on b.id = r.book
	join users as u 
	on u.id = r.reviewer
	where b.id =1
	;

select b.title as "Title", b.description as "Book Description", a.name as "Auhor Name" from books as b
join author as a
on a.id = b.author_id
;

SELECT * from books where title = 'The Dark Is Rising';
SELECT * from books where title Like'%Dark%';

