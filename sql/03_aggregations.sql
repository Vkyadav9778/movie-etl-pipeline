-- group by / aggregate queries for insights

-- 1. average rating and total number of movies per genre
SELECT
    m.GENRE,
    COUNT(*) AS TOTAL_MOVIES,
    ROUND(AVG(r.SCORE), 2) AS AVG_SCORE
FROM MOVIES m
JOIN RATINGS r ON m.MOVIE_ID = r.MOVIE_ID
GROUP BY m.GENRE
ORDER BY AVG_SCORE DESC;

-- 2. total budget and gross collection per year
SELECT
    m.YEAR,
    SUM(f.BUDGET) AS TOTAL_BUDGET,
    SUM(f.GROSS) AS TOTAL_GROSS
FROM MOVIES m
JOIN FINANCIALS f ON m.MOVIE_ID = f.MOVIE_ID
GROUP BY m.YEAR
ORDER BY m.YEAR;

-- 3. which directors have made the most movies in the dataset
SELECT
    p.DIRECTOR,
    COUNT(*) AS MOVIE_COUNT,
    ROUND(AVG(r.SCORE), 2) AS AVG_SCORE
FROM PEOPLE p
JOIN RATINGS r ON p.MOVIE_ID = r.MOVIE_ID
GROUP BY p.DIRECTOR
HAVING COUNT(*) > 3
ORDER BY MOVIE_COUNT DESC;

-- 4. average movie runtime per decade
SELECT
    FLOOR(m.YEAR / 10) * 10 AS DECADE,
    ROUND(AVG(m.RUNTIME), 1) AS AVG_RUNTIME
FROM MOVIES m
GROUP BY DECADE
ORDER BY DECADE;
