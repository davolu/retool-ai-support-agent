SELECT
  t.id,
  t.ticket_number,
  t.subject,
  t.status,
  t.priority,
  t.updated_at,
  t.customer_id,
  c.email,
  c.first_name,
  c.last_name,
  c.company
FROM support_desk_tickets t
JOIN support_desk_customers c ON c.id = t.customer_id
WHERE t.status IN ('open', 'in_progress')
  AND t.updated_at < NOW() - INTERVAL '48 hours'
ORDER BY t.updated_at ASC;
