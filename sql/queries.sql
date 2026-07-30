-- 1. Топ-5 категорий по числу компаний
SELECT
    category,
    COUNT(*) AS companies_count
FROM companies
GROUP BY category
ORDER BY companies_count DESC
LIMIT 5;


-- 2. Средний рейтинг по городам (компании с 10+ отзывами)
SELECT
    city,
    ROUND(AVG(rating), 2) AS avg_rating,
    COUNT(*) AS companies_count
FROM companies
WHERE reviews_count >= 10
  AND rating IS NOT NULL
GROUP BY city
ORDER BY avg_rating DESC;


-- 3. Доля компаний с сайтом по категориям (%)
SELECT
    category,
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE site IS NOT NULL) AS with_site,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE site IS NOT NULL) / COUNT(*),
        2
    ) AS site_share_pct
FROM companies
GROUP BY category
ORDER BY site_share_pct DESC;