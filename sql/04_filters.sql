-- simple filtering queries

-- 1. movies released after 2010 with a rating above 7.5
SELECT m.NAME, m.YEAR, r.SCORE
FROM MOVIES m
JOIN RATINGS r ON m.MOVIE_ID = r.MOVIE_ID
WHERE m.YEAR > 2010 AND r.SCORE > 7.5
ORDER BY r.SCORE DESC;

-- 2. big budget movies (over 100 million) that flopped at the box office
SELECT m.NAME, f.BUDGET, f.GROSS
FROM MOVIES m
JOIN FINANCIALS f ON m.MOVIE_ID = f.MOVIE_ID
WHERE f.BUDGET > 100000000 AND f.GROSS < f.BUDGET
ORDER BY f.BUDGET DESC;

-- 3. movies from a specific country and genre
SELECT m.NAME, m.YEAR, m.COMPANY
FROM MOVIES m
WHERE m.COUNTRY = 'United States' AND m.GENRE = 'Action';

-- 4. R rated movies with more than 500,000 votes (i.e. genuinely popular)
SELECT m.NAME, r.SCORE, r.VOTES
FROM MOVIES m
JOIN RATINGS r ON m.MOVIE_ID = r.MOVIE_ID
WHERE r.RATING = 'R' AND r.VOTES > 500000
ORDER BY r.VOTES DESC;
