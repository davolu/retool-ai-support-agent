# Demo seed data

Clearly fictional support data for Retool Database (Postgres).

- 25 customers in `customers.csv` / `support_desk_customers`
- 120 tickets in `tickets.csv` / `support_desk_tickets`
- `ticket_events.csv` is headers only; the workflow and agent write rows later
- All emails use the `example.com` domain
- Timestamps are frozen as-of 2026-11-23 20:00:00+01 (Africa/Lagos) and span the previous 30 days
- 28 tickets are stuck: `open` or `in_progress`, last updated more than 48 hours before that as-of time (see `SEED_SUMMARY.txt`)

Table names are prefixed so they do not collide with other tables in an existing Retool org.

## Load with SQL

Run `seed.sql` once against Retool Database. It drops and recreates only the `support_desk_*` tables.

## Load with CSV

In Retool, open Database > Import CSV > Into a new table. Import `customers.csv` first as `support_desk_customers`, then `tickets.csv` as `support_desk_tickets`. Create `support_desk_ticket_events` from the empty CSV, or create it by hand with `id`, `ticket_id`, `event_type`, `note`, and `created_at`.

## Regenerate

```bash
python3 generate_seed.py
```

The script is deterministic (random seed 45).
