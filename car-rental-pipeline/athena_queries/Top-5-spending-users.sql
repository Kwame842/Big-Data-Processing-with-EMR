-- Top 5 Spending Users
SELECT user_id, first_name, last_name, total_spent
FROM user_metrics
ORDER BY total_spent DESC
LIMIT 5;