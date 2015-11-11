CREATE TABLE book (
title VARCHAR(256) NOT NULL,
format CHAR(9) CHECK(format = 'paperback' OR format='hardcover'),
pages INT,
language VARCHAR(32),
authors VARCHAR(256),
publisher VARCHAR(64),
year INT,
ISBN10 CHAR(10) NOT NULL UNIQUE,
ISBN13 CHAR(14) PRIMARY KEY
);

CREATE TABLE student (
name VARCHAR(32) NOT NULL,
email VARCHAR(128) PRIMARY KEY,
year DATE NOT NULL,
department VARCHAR(32) NOT NULL,
graduate DATE,
CHECK(graduate >= year)
);

CREATE TABLE copy (
owner VARCHAR(128),
book CHAR(14),
copy INT CHECK(copy>0),
available BOOLEAN NOT NULL,
PRIMARY KEY (owner, book, copy),
FOREIGN KEY (owner) REFERENCES student(email) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (book) REFERENCES book(ISBN13) ON UPDATE CASCADE
);

CREATE TABLE loan (
borrower VARCHAR(128),
owner VARCHAR(128) REFERENCES student(email),
book CHAR(14),
copy INT,
borrowed DATE,
returned DATE,
FOREIGN KEY (owner, book, copy) REFERENCES copy(owner, book, copy) ON UPDATE CASCADE ON DELETE CASCADE,
PRIMARY KEY (borrowed, borrower, owner, book, copy),
CHECK(returned >= borrowed)
);
