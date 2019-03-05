/*
 Get the newest five books
 */
SELECT
  title, released_year
FROM books ORDER BY released_year DESC LIMIT 5;


/*
 Get the first row(starts by index 0) and get 5 descending(sort by released_year) rows
 */
SELECT
  title, released_year
FROM books ORDER BY released_year DESC LIMIT 0, 5;

/*
 Get the 11th row
*/
SELECT
  title, released_year
FROM books ORDER BY released_year DESC LIMIT 10, 1;

/*
 Get the 11th row of the table that first sorted by descending released_year, then sorted by descending title
*/
SELECT
  title, released_year
FROM books ORDER BY released_year DESC , title DESC LIMIT 10, 1;

/*
  If your table does not have up to 50000000000 rows, than you will get all the rows start from indexing 5 to the end of the table.
*/
SELECT
  title
FROM books LIMIT 5, 50000000000;
