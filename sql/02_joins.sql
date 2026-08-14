-- joining the 4 tables back together using movie_id

-- 1. full picture of a movie: rating + money + people, all in one row
SELECT
    m.NAME,
    m.GENRE,
    m.YEAR,
    r.SCORE,
    r.RATING,
    f.BUDGET,
    f.GROSS,
    p.DIRECTOR
FROM MOVIES m
JOIN RATINGS r ON m.MOVIE_ID = r.MOVIE_ID
JOIN FINANCIALS f ON m.MOVIE_ID = f.MOVIE_ID
JOIN PEOPLE p ON m.MOVIE_ID = p.MOVIE_ID
ORDER BY r.SCORE DESC
LIMIT 20;

-- 2. movies that made a profit, with the director's name
SELECT
    m.NAME,
    p.DIRECTOR,
    f.BUDGET,
    f.GROSS,
    (f.GROSS - f.BUDGET) AS PROFIT
FROM MOVIES m
JOIN FINANCIALS f ON m.MOVIE_ID = f.MOVIE_ID
JOIN PEOPLE p ON m.MOVIE_ID = p.MOVIE_ID
WHERE f.GROSS > f.BUDGET
ORDER BY PROFIT DESC
LIMIT 20;

-- 3. highly rated movies (score above 8) that most people haven't heard of
-- (low vote count but still a good score)
SELECT
    m.NAME,
    m.YEAR,
    r.SCORE,
    r.VOTES
FROM MOVIES m
JOIN RATINGS r ON m.MOVIE_ID = r.MOVIE_ID
WHERE r.SCORE > 8 AND r.VOTES < 20000
ORDER BY r.SCORE DESC;
