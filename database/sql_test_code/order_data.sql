
SELECT
  author_lname
FROM books ORDER BY author_lname;

SELECT
  title
FROM books ORDER BY title;

SELECT
  title
FROM books ORDER BY title DESC;

SELECT
  released_year
FROM books ORDER BY released_year;

SELECT
  released_year
FROM books ORDER BY released_year DESC;

SELECT
  title, pages
FROM books ORDER BY released_year;

/*
ORDER BY 2 means order by the second select column, which is author_fname
*/
SELECT
  title, author_fname, author_lname
FROM books ORDER BY 2;

SELECT
  author_fname, author_lname
FROM books ORDER BY author_lname;

/*
After sorting by author_lname, then sort by author_fname
*/
SELECT
  author_fname, author_lname
FROM books ORDER BY author_lname, author_fname;
