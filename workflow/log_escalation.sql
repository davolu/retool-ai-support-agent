INSERT INTO support_desk_ticket_events (ticket_id, event_type, note)
VALUES (
  {{ value.id }},
  'escalated_by_workflow',
  {{ 'Stuck more than 48 hours. Previous status: ' + value.status }}
);
