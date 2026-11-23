# Support Desk Agent tools

Create these as custom tools on **Support Desk Agent**. Resource queries use Retool Database. Build them by hand. The Function Generator is optional and may consume AI credits.

Tool output must stay under 1 MB. Names must stay under 64 characters.

## 1. lookupCustomer

Description: `Find demo customers by a name, email, or company snippet. Returns matching rows.`

Parameter: `query` (string, required).

Require user confirmation: off.

```sql
SELECT id, first_name, last_name, email, company, plan, created_at
FROM support_desk_customers
WHERE
  first_name ILIKE '%' || {{ params.query }} || '%'
  OR last_name ILIKE '%' || {{ params.query }} || '%'
  OR (first_name || ' ' || last_name) ILIKE '%' || {{ params.query }} || '%'
  OR email ILIKE '%' || {{ params.query }} || '%'
  OR company ILIKE '%' || {{ params.query }} || '%'
ORDER BY last_name, first_name
LIMIT 20;
```

Return the query data with a Response block, status 200.

## 2. listCustomerTickets

Description: `List tickets for one customer id, newest first. Optionally filter by status.`

Parameters: `customer_id` (number, required); `status` (string, optional).

Require user confirmation: off.

```sql
SELECT
  id, ticket_number, subject, body, status, priority, channel,
  assigned_to, created_at, updated_at, first_response_at, resolved_at, escalated_at
FROM support_desk_tickets
WHERE customer_id = {{ params.customer_id }}
  AND (
    {{ !params.status }}
    OR status = {{ params.status }}
  )
ORDER BY updated_at DESC;
```

If the editor rejects `{{ !params.status }}`, use an equivalent empty-check that your org accepts.

## 3. draftReplyContext

Description: `Load one ticket and its customer so a reply can be drafted. Does not send email and does not change data.`

Parameters: `ticket_id` (number, optional); `ticket_number` (string, optional). Provide at least one.

Require user confirmation: off.

```sql
SELECT
  t.id, t.ticket_number, t.subject, t.body, t.status, t.priority, t.channel,
  t.assigned_to, t.created_at, t.updated_at,
  c.id AS customer_id, c.first_name, c.last_name, c.email, c.company, c.plan
FROM support_desk_tickets t
JOIN support_desk_customers c ON c.id = t.customer_id
WHERE
  ({{ !params.ticket_id }} OR t.id = {{ params.ticket_id }})
  AND ({{ !params.ticket_number }} OR t.ticket_number = {{ params.ticket_number }})
LIMIT 1;
```

## 4. updateTicket

Description: `Update a single demo ticket's status and/or priority, and write an event note. Always wait for the human to confirm.`

Parameters:

- `ticket_id` (number, required)
- `status` (string, optional): `open`, `in_progress`, `waiting_on_customer`, `resolved`, or `escalated`
- `priority` (string, optional): `low`, `medium`, `high`, or `urgent`
- `note` (string, optional)

**Require user confirmation before use: on.**

```sql
-- applyUpdate
UPDATE support_desk_tickets
SET
  status = COALESCE({{ params.status }}, status),
  priority = COALESCE({{ params.priority }}, priority),
  updated_at = NOW(),
  resolved_at = CASE
    WHEN {{ params.status }} = 'resolved' THEN NOW()
    ELSE resolved_at
  END,
  escalated_at = CASE
    WHEN {{ params.status }} = 'escalated' THEN COALESCE(escalated_at, NOW())
    ELSE escalated_at
  END
WHERE id = {{ params.ticket_id }}
RETURNING *;
```

```sql
-- logEvent
INSERT INTO support_desk_ticket_events (ticket_id, event_type, note)
VALUES (
  {{ params.ticket_id }},
  'updated_by_agent',
  {{ params.note || 'Updated by Support Desk Agent' }}
);
```

Return `applyUpdate.data` with a Response block, status 200.
