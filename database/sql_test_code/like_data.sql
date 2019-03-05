
SELECT
  title
FROM books WHERE title LIKE '%the%';

SELECT
  title, author_fname
FROM books WHERE author_fname LIKE '%da%';

SELECT
  title, author_fname
FROM books WHERE author_fname LIKE 'da%';

/*
'_' is the wildcard which is specified exactly one character
'*' is the wildcard which is not limited to any character and any number or any thing
 */
SELECT
  title, stock_quantity
FROM books WHERE stock_quantity LIKE '____';

/*
\% will search exactly for the '%' alphabet
\_ will search exactly for the '\' alphabet
 */
SELECT
  title
FROM books WHERE title LIKE '%\%%';
SELECT
  title
FROM books WHERE title LIKE '%\_%';
