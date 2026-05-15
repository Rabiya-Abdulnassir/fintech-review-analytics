-- Count reviews per bank
SELECT b.bank_name, COUNT(r.review_id)
FROM reviews r
JOIN banks b
ON r.bank_id = b.bank_id
GROUP BY b.bank_name;

-- Average rating per bank
SELECT b.bank_name, ROUND(AVG(r.rating), 2)
FROM reviews r
JOIN banks b
ON r.bank_id = b.bank_id
GROUP BY b.bank_name;

-- Check missing values
SELECT COUNT(*)
FROM reviews
WHERE review_text IS NULL
OR rating IS NULL;