
CREATE TABLE books (
  id SERIAL PRIMARY KEY,
  isbn INTEGER NOT NULL
  title VARCHAR NOT NULL,
  author VARCHAR NOT NULL,
  year INTEGER NOT NULL
);


INSERT INTO author
  (name, age)
  VALUES ('Jonathan Lovelock', 23);
  
INSERT INTO author
  (name, age)
  VALUES ('Stuart Andrew', 21);
  
INSERT INTO books
  (title, description, author_id)
  VALUES ('Wind in the willows', 'Really good book I love it', 1);

INSERT INTO books
  (title, description, author_id)
  VALUES ('Alexy Lahey Biography', 'Really good book I love it', 1);
INSERT INTO books
  (title, description, author_id)
  VALUES ('Sexy Stu Book', 'Really good book I love it', 1);


select b.title as "Title", b.description as "Book Description", a.name as "Auhor Name" from books as b
join author as a
on a.id = b.author_id
;