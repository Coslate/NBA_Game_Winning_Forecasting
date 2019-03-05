/*
SELECT
  DISTINCT author_lname
FROM books;
*/

SELECT
  DISTINCT CONCAT(author_fname, ' ', author_lname)
FROM books;
