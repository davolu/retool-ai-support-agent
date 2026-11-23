UPDATE support_desk_tickets
SET
  status = 'escalated',
  priority = CASE
    WHEN priority IN ('low', 'medium') THEN 'high'
    ELSE priority
  END,
  escalated_at = COALESCE(escalated_at, NOW()),
  updated_at = NOW()
WHERE id = {{ value.id }}
  AND status IN ('open', 'in_progress')
RETURNING id, ticket_number, status, priority, escalated_at;
