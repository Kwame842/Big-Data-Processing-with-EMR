-- Most Rented Vehicle Type
SELECT vehicle_type, revenue_by_vehicle_type
FROM vehicle_metrics
ORDER BY revenue_by_vehicle_type DESC
LIMIT 1;