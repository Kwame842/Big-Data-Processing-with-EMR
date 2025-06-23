-- Highest Revenue-Generating Location
SELECT pickup_location, total_revenue
FROM location_metrics
ORDER BY total_revenue DESC
LIMIT 1;