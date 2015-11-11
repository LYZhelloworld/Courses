CREATE TABLE Book (
	title VARCHAR(255) NOT NULL,
	fmt VARCHAR(255) CHECK (fmt = 'paperback' OR fmt = 'hardcover'),
	pages INT,
	authors VARCHAR(255),
	publisher VARCHAR(255),
	book_year INT,
	edition INT,
	ISBN10 CHAR(10) NOT NULL,
	ISBN13 CHAR(13) NOT NULL,
	PRIMARY KEY (ISBN13)
);

INSERT INTO Book VALUES ('Database Management Systems', 'hardcover', 1065, 'Raghu Ramakrishnan, Johannes Gehrke', 'McGraw-Hill Education', 2003, 3, '0072465638', '9780072465631');

INSERT INTO Book VALUES ('Database Management Systems', 'paperback', 336, 'ITL ESL', 'Pearson Education India', NULL, NULL, '8131797600', '9788131797600');
INSERT INTO Book VALUES ('Database Management Systems', 'paperback', 280, 'Seema Kedar', 'Technical Publications', 2009, NULL, '8184315848', '9788184315844');
INSERT INTO Book VALUES ('Database Management Systems', 'hardcover', 740, 'Raghu; Gehrke, Johannes Ramakrishnan', 'McGraw-Hill College', 2000, 2, '0072322063', '9780072322064');
INSERT INTO Book VALUES ('An Introduction to Database Systems', 'hardcover', 983, 'C.J. Date', 'Addison Wesley', 2004, 8, '0321197844', '9780321197849');
INSERT INTO Book VALUES ('Database Design and Relational Theory: Normal Forms and All That Jazz (Theory in Practice)', 'paperback', 278, 'C.J. Date', 'O\'Reilly Media', 2012, 1, '1449328016', '9781449328016');

SELECT * FROM Book;

UPDATE Book SET authors = 'Christopher J. Date' WHERE authors = 'C.J. Date';

SELECT title, authors, publisher, book_year, edition, ISBN10, ISBN13 FROM Book;

SELECT authors FROM Book;

SELECT authors FROM Book WHERE title = 'Database Management Systems';

ALTER TABLE Book ADD lang VARCHAR(255);
ALTER TABLE Book ALTER lang SET DEFAULT 'English';

DELETE FROM Book WHERE authors = 'C.J. Date';

DROP TABLE Book;