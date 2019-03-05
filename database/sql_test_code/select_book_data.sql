
/*
SELECT
  CONCAT(
--    SUBSTRING(title, 1, 10),
--    '...'
--  ) AS 'short title'
--FROM books;
*/

SELECT
  SUBSTRING(REPLACE(title, 'e', 3), 1, 10)
FROM books;

SELECT
  SUBSTRING(REPLACE(title, 'e', 3), 1, 10) AS 'strange title'
FROM books;

SELECT
  CONCAT(author_fname, REVERSE(author_fname)) FROM books;

SELECT
  CONCAT(author_lname, ' is ', CHAR_LENGTH(author_lname), ' characters long.') AS 'author_lname-length'
FROM books;

SELECT
  CONCAT('MY FAVORITE BOOK IS ', UPPER(title))
FROM books;

SELECT
  CONCAT('MY FAVORITE BOOK IS ', LOWER(title))
FROM books;

SELECT
  title,
  CHAR_LENGTH(title) AS 'character count'
FROM books;

SELECT
  UPPER(CONCAT(author_fname, ' ', author_lname)) AS 'full name in caps'
FROM books;

SELECT
CONCAT(SUBSTRING(title, 1, 10), '...') AS 'short title',
CONCAT(author_lname, ',', author_fname) AS author,
CONCAT(stock_quantity, ' in stock') AS quantity
FROM books;
