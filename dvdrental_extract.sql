-- Revenue & Film Perfromance
SELECT
    f.title AS film_title,
    c.name AS category,
    SUM(p.amount) AS total_rental_revenue,
    COUNT(DISTINCT r.rental_id) AS total_rentals,
    ROUND(SUM(p.amount) / COUNT(DISTINCT r.rental_id),2) AS average_revenue_per_rental,
	MAX(DATE_TRUNC('month', r.rental_date)) AS last_rental_date
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id
JOIN inventory i ON f.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
JOIN payment p ON r.rental_id = p.rental_id
GROUP BY
    f.film_id,
    f.title,
    c.name;

--customer behaviour and retention
SELECT 
	cu.first_name || ' ' || cu.last_name AS customer_name,
    ci.city,
	co.country,
	SUM(p.amount) AS total_amount_spent,
	COUNT(r.rental_id) AS total_rentals,
	MIN(DATE_TRUNC('month', r.rental_date)) AS last_rental_date,
	MAX(DATE_TRUNC('month', r.rental_date)) AS last_rental_date
FROM customer cu
JOIN rental r ON cu.customer_id = r.customer_id
JOIN payment p ON r.rental_id = p.rental_id
JOIN address a ON cu.address_id = a.address_id
JOIN city ci ON a.city_id = ci.city_id
JOIN country co ON ci.country_id = co.country_id
GROUP BY 
	customer_name,
	city,
	country
ORDER BY total_amount_spent DESC;

--time-based trends
SELECT
    TO_CHAR(r.rental_date, 'YYYY') AS rental_year,
	TO_CHAR(DATE_TRUNC('month', r.rental_date), 'Month') AS rental_month,
    COUNT(DISTINCT r.rental_id) AS total_rentals,
    SUM(p.amount) AS total_revenue,
    COUNT(DISTINCT r.customer_id) AS unique_customers,
    ROUND(AVG(p.amount), 2) AS average_rental_revenue
FROM rental r
JOIN payment p ON r.rental_id = p.rental_id
GROUP BY rental_month, rental_year
ORDER BY rental_year;

--store_staff_performance
SELECT
    s.store_id,
    s.first_name || ' ' || s.last_name AS staff_name,
    COUNT(DISTINCT r.rental_id) AS total_rentals,
    SUM(p.amount) AS total_revenue,
    COUNT(DISTINCT r.customer_id) AS unique_customers,
    ROUND(COUNT(DISTINCT r.rental_id) / COUNT(DISTINCT DATE(r.rental_date)), 2) 
	AS average_rentals_per_day
FROM staff s
JOIN rental r ON s.staff_id = r.staff_id
JOIN payment p ON r.rental_id = p.rental_id
GROUP BY
    s.store_id,
    staff_name
ORDER BY staff_name;

--geographical_market
WITH Topcategory AS (

SELECT
	co.country,
	ci.city,
	c.name AS category,
	COUNT(DISTINCT r.rental_id),
	ROW_NUMBER() OVER(
	PARTITION BY co.country,ci.city

ORDER BY COUNT(*) DESC

) AS tc

FROM rental r
JOIN customer cu ON r.customer_id=cu.customer_id
JOIN address a ON cu.address_id = a.address_id
JOIN city ci ON a.city_id = ci.city_id
JOIN country co ON ci.country_id = co.country_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film_category fc ON i.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id

GROUP BY
	co.country,
	ci.city,
	c.name
)

SELECT
	co.country,
	ci.city,
	COUNT(r.rental_id) AS total_geo_rent,
	ROUND(SUM(p.amount),2) AS total_geo_revenue,
	COUNT(DISTINCT cu.customer_id) AS unique_customers,
	Topcategory.category AS top_category
	
FROM customer cu
JOIN address a ON cu.address_id = a.address_id
JOIN city ci ON a.city_id = ci.city_id
JOIN country co ON ci.country_id = co.country_id
LEFT JOIN rental r ON cu.customer_id = r.customer_id
LEFT JOIN payment p ON r.rental_id = p.rental_id

LEFT JOIN Topcategory ON co.country = Topcategory.country
AND ci.city = Topcategory.city
AND Topcategory.tc = 1

GROUP BY
	co.country,
	ci.city,
	Topcategory.category

ORDER BY total_geo_revenue DESC;

--inventory_and_operations
SELECT
	f.title AS film_title,
	c.name AS category,
	COUNT(DISTINCT i.inventory_id) AS inventory_count,
    COUNT(r.rental_id) AS total_rentals,
	ROUND(SUM(p.amount), 2) AS total_revenue,
	MAX(r.rental_date) AS last_rental_date,
	ROUND(AVG(f.rental_duration), 0) AS average_rental_duration
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id
JOIN inventory i ON f.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
JOIN payment p ON r.rental_id = p.rental_id
GROUP BY
	f.title,
	c.name
ORDER BY total_revenue DESC;