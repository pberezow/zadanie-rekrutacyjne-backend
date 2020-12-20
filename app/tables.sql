--DROP TABLE IF EXISTS books;

CREATE TABLE IF NOT EXISTS books
(
    id varchar(25),
    title varchar(100),
    author varchar(50),
    published_date date,
    isbn varchar(13),
    page_count int,
    cover_url varchar(150),
    "language" varchar(2),
    PRIMARY KEY(id)
);