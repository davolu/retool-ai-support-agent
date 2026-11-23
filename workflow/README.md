# Support Desk Escalate Stuck Tickets

Retool Workflow that finds demo tickets left in `open` or `in_progress` for more than 48 hours, marks them `escalated`, raises low or medium priority to high, and writes a row to `support_desk_ticket_events`.

Create a workflow with this exact name: **Support Desk Escalate Stuck Tickets**.

## Triggers

- **Schedule:** every 1 hour, timezone Africa/Lagos. (Optional daily cron: `0 9 * * *` in Africa/Lagos.)
- **Webhook:** enabled, for tests or an external caller.

Publish the workflow before automatic triggers will fire. Manual runs from the Workflow IDE do not count against the monthly run allowance.

Never commit or paste the workflow API key. If you test with curl, keep the key out of this repo and out of screenshots.

Test JSON payload:

```json
{ "source": "manual_test", "stuck_after_hours": 48 }
```

## Blocks

1. `getStuckTickets` — SQL in `get_stuck_tickets.sql`.
2. `ifHasStuck` — continue only when `getStuckTickets.data.length > 0`. Otherwise return `{ ok: true, escalated: 0, message: "No stuck tickets." }`.
3. `loopStuck` — loop over `getStuckTickets.data`.
   - `escalateOne` — SQL in `escalate_one.sql`.
   - `logEscalation` — SQL in `log_escalation.sql`.
4. `summarize` — JavaScript in `summarize.js`. Inspect the actual loop output shape in your run logs and adjust the mapper if needed. Do not invent a count.
5. `doneResponse` — HTTP 200, body `{{ summarize.data }}`.

The seed set (as of 2026-11-23 20:00 Africa/Lagos) contains 28 stuck tickets, listed in `../seed/SEED_SUMMARY.txt`.
