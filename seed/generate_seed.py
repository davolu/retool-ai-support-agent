#!/usr/bin/env python3
"""Generate clearly fictional demo customers and support tickets for Retool Database.

As-of timestamp is frozen at 2026-11-23 20:00:00+01 (Africa/Lagos) so the
same SQL/CSVs are reproducible. Timestamps span the previous 30 days.
Some open/in_progress tickets are left stale (>48 hours) so the escalation
workflow has a realistic 'stuck' set.

All emails use the example.com domain. Company names are fictional.
"""

from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

LAGOS = timezone(timedelta(hours=1))
AS_OF = datetime(2026, 11, 23, 20, 0, 0, tzinfo=LAGOS)
WINDOW_DAYS = 30
STUCK_AFTER = timedelta(hours=48)
SEED = 45  # AACB-adjacent, deterministic

OUT = Path(__file__).resolve().parent

# Prefixed so these tables do not collide with anything already in an existing
# Retool org (for example Sample Users Page).
TABLE_CUSTOMERS = "support_desk_customers"
TABLE_TICKETS = "support_desk_tickets"
TABLE_EVENTS = "support_desk_ticket_events"

CUSTOMERS = [
    (1, "Maya", "Okonkwo", "maya.okonkwo@example.com", "Brightleaf Foods", "pro"),
    (2, "Tomas", "Rivera", "tomas.rivera@example.com", "Harbor and Co Demo", "starter"),
    (3, "Priya", "Nair", "priya.nair@example.com", "Lotus Paper Goods", "pro"),
    (4, "Jonah", "Adeyemi", "jonah.adeyemi@example.com", "Sahel Bike Share", "enterprise"),
    (5, "Elena", "Vasquez", "elena.vasquez@example.com", "Mesa Craft Studio", "free"),
    (6, "Kwame", "Boateng", "kwame.boateng@example.com", "Accra Lantern Labs", "pro"),
    (7, "Sophie", "Laurent", "sophie.laurent@example.com", "Rue Sage Books", "starter"),
    (8, "Daniel", "Cho", "daniel.cho@example.com", "Pacific Rim Tea", "pro"),
    (9, "Amina", "Yusuf", "amina.yusuf@example.com", "Kano Textile House", "starter"),
    (10, "Luca", "Bianchi", "luca.bianchi@example.com", "Trattoria Ficta", "free"),
    (11, "Hannah", "Berg", "hannah.berg@example.com", "Fjord Office Supply", "enterprise"),
    (12, "Omar", "Haddad", "omar.haddad@example.com", "Cedar Wellness Demo", "pro"),
    (13, "Grace", "Mwangi", "grace.mwangi@example.com", "Nairobi Plant Co", "starter"),
    (14, "Nathan", "Cole", "nathan.cole@example.com", "Maple Desk Works", "pro"),
    (15, "Yuki", "Tanaka", "yuki.tanaka@example.com", "Paper Crane Stationery", "free"),
    (16, "Fatima", "Diallo", "fatima.diallo@example.com", "Dakar Solar Kits", "enterprise"),
    (17, "Benito", "Cruz", "benito.cruz@example.com", "Azul Print Shop", "starter"),
    (18, "Ingrid", "Holm", "ingrid.holm@example.com", "Aurora Knitwear", "pro"),
    (19, "Samuel", "Okeke", "samuel.okeke@example.com", "Enugu Tool Library", "free"),
    (20, "Chloe", "Martin", "chloe.martin@example.com", "Pine and Needle Co", "starter"),
    (21, "Ravi", "Patel", "ravi.patel@example.com", "Midtown Spice Market", "pro"),
    (22, "Lila", "Hassan", "lila.hassan@example.com", "Oasis Learning Hub", "enterprise"),
    (23, "Peter", "Novak", "peter.novak@example.com", "Danube Components", "starter"),
    (24, "Amara", "Mensah", "amara.mensah@example.com", "Kumasi Bead Studio", "free"),
    (25, "Owen", "Fraser", "owen.fraser@example.com", "Thistle Software Demo", "pro"),
]

AGENTS = ["Ada Mensah", "Leo Grant", "Priya Shah", "Jonah Okeke"]

# (subject, body, typical priority weight hint)
TEMPLATES = [
    (
        "Cannot sign in after password reset",
        "Hi, I reset my password yesterday but the new one is not being accepted on the sign-in page. I have tried two browsers. This is a demo ticket for Brightleaf-style accounts. Please help me get back in.",
        ["high", "urgent", "medium"],
    ),
    (
        "Invoice shows the wrong plan",
        "Our latest invoice lists the starter plan, but we have been on pro since last month. The amount looks off as well. Can you check the subscription on this demo account?",
        ["high", "medium"],
    ),
    (
        "Shipment has not arrived",
        "The order we placed two weeks ago still shows as in transit. The tracking page has not updated for several days. This is sample shipping data only.",
        ["high", "urgent", "medium"],
    ),
    (
        "Refund for damaged items",
        "Two items in our last delivery arrived damaged. I have photos ready. Please start a refund or a replacement on this fictional order.",
        ["medium", "high"],
    ),
    (
        "How do I export a CSV of last month's orders?",
        "I need a CSV of last month's orders for our bookkeeper. I cannot find the export button. Walk me through it in plain English.",
        ["low", "medium"],
    ),
    (
        "Webhook stopped firing",
        "Our demo webhook to the sandbox URL stopped sending events on Friday. The endpoint is a fictional https://hooks.example.com/demo path. Can you check the delivery logs?",
        ["high", "urgent"],
    ),
    (
        "Dashboard is loading slowly",
        "The orders dashboard takes more than thirty seconds to open this morning. It was fine last week. Happy to share a screenshot of the spinner.",
        ["medium", "high"],
    ),
    (
        "Need an extra teammate seat",
        "We hired a new teammate and the workspace says we have hit our seat limit. How do we add one more person on our current plan?",
        ["medium", "low"],
    ),
    (
        "Feature request: saved filter views",
        "Could we save filter views on the orders table? Our team switches between the same three filters every day.",
        ["low", "medium"],
    ),
    (
        "Promo code is not applying at checkout",
        "The demo code SAVE10DEMO does not reduce the total at checkout. It looks valid on the discounts page. Can you test it?",
        ["medium", "high"],
    ),
    (
        "Two charges appeared for the same invoice",
        "I see two charges for invoice INV-DEMO-4421 on our card statement. Please check if one is a duplicate and advise on a reversal.",
        ["urgent", "high"],
    ),
    (
        "API sandbox returns 401",
        "Calls to the sandbox API return 401 even with a freshly generated demo key, which I will not paste here. Is the sandbox down?",
        ["high", "medium"],
    ),
    (
        "Change the company billing email",
        "Please change our billing email from the old inbox to the current example.com address on file. We missed the last receipt.",
        ["low", "medium"],
    ),
    (
        "Product photo is missing on the catalog page",
        "The listing for the sample item SKU-DEMO-88 has no photo. It showed yesterday. Can you restore it?",
        ["low", "medium"],
    ),
    (
        "Cannot invite a contractor with a guest role",
        "The invite form rejects guest@example.com and says the domain is not allowed. We need a contractor to view one report only.",
        ["medium", "high"],
    ),
    (
        "Tax amount looks incorrect",
        "The tax line on our last invoice is higher than we expected for our region. This is demo tax data. Please confirm the rule that was applied.",
        ["medium", "high"],
    ),
    (
        "Mobile app keeps logging me out",
        "The iOS demo app logs me out after a few minutes. I am on the latest TestFlight build we were given.",
        ["medium", "high"],
    ),
    (
        "Need to close this demo account",
        "We finished our trial and want the demo workspace closed. Please confirm what happens to the sample data.",
        ["low", "medium"],
    ),
    (
        "Scheduled report did not send",
        "The Monday morning sales report did not arrive in our example.com inbox. It usually lands at 9:00.",
        ["medium", "high"],
    ),
    (
        "Wrong warehouse was assigned",
        "An order was routed to the west warehouse instead of the east one. The address on the demo order looks correct to me.",
        ["high", "medium"],
    ),
]


def fmt(dt: datetime) -> str:
    # Colon in the offset is easier for Retool Database CSV import.
    return dt.strftime("%Y-%m-%d %H:%M:%S") + "+01:00"


def sql_str(value: str | None) -> str:
    if value is None:
        return "NULL"
    return "'" + value.replace("'", "''") + "'"


def sql_ts(dt: datetime | None) -> str:
    if dt is None:
        return "NULL"
    # Use an explicit +01 offset so Postgres stores the intended instant.
    return "'" + dt.strftime("%Y-%m-%d %H:%M:%S") + "+01'"


def random_time_on(day: datetime, rng: random.Random) -> datetime:
    minute = rng.randint(8 * 60, 18 * 60 + 30)
    return day.replace(hour=0, minute=0, second=0) + timedelta(
        minutes=minute, seconds=rng.randint(0, 59)
    )


def build_tickets(rng: random.Random) -> list[dict]:
    """Build 120 tickets with a controlled mix of statuses and stuck rows."""
    tickets: list[dict] = []
    ticket_id = 1

    def add(
        customer_id: int,
        created: datetime,
        updated: datetime,
        status: str,
        priority: str,
        channel: str,
        assigned: str | None,
        subject: str,
        body: str,
        first_response: datetime | None,
        resolved: datetime | None,
        escalated: datetime | None,
    ) -> None:
        nonlocal ticket_id
        tickets.append(
            {
                "id": ticket_id,
                "ticket_number": f"TCK-{1000 + ticket_id}",
                "customer_id": customer_id,
                "subject": subject,
                "body": body,
                "status": status,
                "priority": priority,
                "channel": channel,
                "assigned_to": assigned,
                "created_at": created,
                "updated_at": updated,
                "first_response_at": first_response,
                "resolved_at": resolved,
                "escalated_at": escalated,
            }
        )
        ticket_id += 1

    def pick_template() -> tuple[str, str, str]:
        subject, body, prios = rng.choice(TEMPLATES)
        return subject, body, rng.choice(prios)

    def customer_created(cid: int) -> datetime:
        # Stagger customer sign-ups across roughly 80 days so created_at < tickets.
        day = AS_OF - timedelta(days=80 - cid * 2, hours=rng.randint(0, 10))
        return day

    # --- 28 stuck tickets: open or in_progress, last update older than 48h ---
    stuck_ages_hours = (
        [50, 54, 60, 72, 80, 96, 110, 120]
        + [144, 160, 168, 180, 200, 216]
        + [240, 260, 280, 300, 312, 336]
        + [360, 384, 400, 420, 456, 480, 504, 552]
    )
    assert len(stuck_ages_hours) == 28
    for i, age_h in enumerate(stuck_ages_hours):
        subject, body, priority = pick_template()
        if age_h >= 240 and rng.random() < 0.45:
            priority = rng.choice(["high", "urgent"])
        updated = AS_OF - timedelta(hours=age_h, minutes=rng.randint(0, 40))
        created = updated - timedelta(hours=rng.randint(4, 72), minutes=rng.randint(0, 50))
        if created < AS_OF - timedelta(days=WINDOW_DAYS):
            created = AS_OF - timedelta(days=WINDOW_DAYS) + timedelta(hours=rng.randint(1, 8))
        status = "open" if i % 3 == 0 else "in_progress"
        assigned = None if status == "open" and rng.random() < 0.4 else rng.choice(AGENTS)
        first = None
        if status == "in_progress":
            gap = timedelta(hours=rng.randint(1, 30), minutes=rng.randint(0, 50))
            first = min(created + gap, updated)
        add(
            customer_id=(i % 25) + 1,
            created=created,
            updated=updated,
            status=status,
            priority=priority,
            channel=rng.choice(["email", "email", "chat", "phone"]),
            assigned=assigned,
            subject=subject,
            body=body,
            first_response=first,
            resolved=None,
            escalated=None,
        )

    # --- 16 fresh open / in_progress (updated within 48h, not stuck) ---
    for i in range(16):
        subject, body, priority = pick_template()
        updated = AS_OF - timedelta(hours=rng.randint(1, 40), minutes=rng.randint(0, 55))
        created = updated - timedelta(hours=rng.randint(0, 20), minutes=rng.randint(0, 50))
        status = "open" if i % 2 == 0 else "in_progress"
        first = None
        if status == "in_progress":
            first = created + timedelta(hours=rng.randint(0, 6), minutes=rng.randint(5, 50))
            if first > updated:
                first = updated
        add(
            customer_id=rng.randint(1, 25),
            created=created,
            updated=updated,
            status=status,
            priority=priority,
            channel=rng.choice(["email", "chat", "chat", "phone"]),
            assigned=rng.choice(AGENTS) if status == "in_progress" or rng.random() < 0.5 else None,
            subject=subject,
            body=body,
            first_response=first,
            resolved=None,
            escalated=None,
        )

    # --- 20 waiting_on_customer ---
    for i in range(20):
        subject, body, priority = pick_template()
        updated = AS_OF - timedelta(hours=rng.randint(6, 200), minutes=rng.randint(0, 55))
        created = updated - timedelta(hours=rng.randint(4, 80))
        if created < AS_OF - timedelta(days=WINDOW_DAYS):
            created = AS_OF - timedelta(days=WINDOW_DAYS - 1, hours=rng.randint(2, 10))
        first = created + timedelta(hours=rng.randint(1, 24), minutes=rng.randint(0, 50))
        if first > updated:
            first = updated - timedelta(minutes=rng.randint(15, 90))
        add(
            customer_id=rng.randint(1, 25),
            created=created,
            updated=updated,
            status="waiting_on_customer",
            priority=priority,
            channel=rng.choice(["email", "email", "chat"]),
            assigned=rng.choice(AGENTS),
            subject=subject,
            body=body,
            first_response=first,
            resolved=None,
            escalated=None,
        )

    # --- 12 already escalated ---
    for i in range(12):
        subject, body, _ = pick_template()
        priority = rng.choice(["high", "urgent", "urgent"])
        updated = AS_OF - timedelta(hours=rng.randint(2, 160), minutes=rng.randint(0, 55))
        created = updated - timedelta(hours=rng.randint(24, 160))
        if created < AS_OF - timedelta(days=WINDOW_DAYS):
            created = AS_OF - timedelta(days=WINDOW_DAYS - 1, hours=4)
        first = created + timedelta(hours=rng.randint(2, 36))
        escalated = updated - timedelta(hours=rng.randint(0, 12), minutes=rng.randint(0, 40))
        if escalated < created:
            escalated = updated
        if first > escalated:
            first = created + timedelta(hours=2)
        add(
            customer_id=rng.randint(1, 25),
            created=created,
            updated=updated,
            status="escalated",
            priority=priority,
            channel=rng.choice(["email", "chat", "phone"]),
            assigned=rng.choice(AGENTS),
            subject=subject,
            body=body,
            first_response=first,
            resolved=None,
            escalated=escalated,
        )

    # --- remaining resolved (should bring the total to 120) ---
    remaining = 120 - len(tickets)
    for i in range(remaining):
        subject, body, priority = pick_template()
        resolved = AS_OF - timedelta(
            days=rng.randint(0, 28), hours=rng.randint(0, 20), minutes=rng.randint(0, 55)
        )
        created = resolved - timedelta(hours=rng.randint(3, 96), minutes=rng.randint(0, 50))
        if created < AS_OF - timedelta(days=WINDOW_DAYS):
            created = AS_OF - timedelta(days=WINDOW_DAYS) + timedelta(hours=rng.randint(2, 12))
            if created >= resolved:
                resolved = created + timedelta(hours=rng.randint(4, 24))
        first = created + timedelta(hours=rng.randint(0, 20), minutes=rng.randint(5, 55))
        if first > resolved:
            first = created + timedelta(minutes=rng.randint(20, 180))
        updated = resolved
        add(
            customer_id=rng.randint(1, 25),
            created=created,
            updated=updated,
            status="resolved",
            priority=priority,
            channel=rng.choice(["email", "email", "chat", "phone"]),
            assigned=rng.choice(AGENTS),
            subject=subject,
            body=body,
            first_response=first,
            resolved=resolved,
            escalated=None,
        )

    assert len(tickets) == 120, len(tickets)
    # Keep ticket numbers in creation-ish order for a cleaner table, but ids stay 1..120.
    tickets.sort(key=lambda t: t["created_at"])
    for i, t in enumerate(tickets, start=1):
        t["id"] = i
        t["ticket_number"] = f"TCK-{1000 + i}"
    return tickets


def customer_rows(rng: random.Random) -> list[dict]:
    rows = []
    for cid, first, last, email, company, plan in CUSTOMERS:
        created = AS_OF - timedelta(days=90 - cid * 2, hours=rng.randint(0, 20), minutes=rng.randint(0, 59))
        rows.append(
            {
                "id": cid,
                "first_name": first,
                "last_name": last,
                "email": email,
                "company": company,
                "plan": plan,
                "created_at": created,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            out = {}
            for k in fieldnames:
                v = row[k]
                if isinstance(v, datetime):
                    out[k] = fmt(v)
                elif v is None:
                    out[k] = ""
                else:
                    out[k] = v
            writer.writerow(out)


def write_sql(path: Path, customers: list[dict], tickets: list[dict]) -> None:
    lines = [
        "-- Demo seed for Retool Database (Postgres).",
        "-- Clearly fictional support data. All emails use the example.com domain.",
        "-- As-of time for relative 'stuck' tickets: 2026-11-23 20:00:00+01 (Africa/Lagos).",
        "-- Safe to re-run: drops and recreates the three demo tables.",
        "",
        "BEGIN;",
        "",
        "DROP TABLE IF EXISTS " + TABLE_EVENTS + " CASCADE;",
        "DROP TABLE IF EXISTS " + TABLE_TICKETS + " CASCADE;",
        "DROP TABLE IF EXISTS " + TABLE_CUSTOMERS + " CASCADE;",
        "",
        "CREATE TABLE " + TABLE_CUSTOMERS + " (",
        "  id INTEGER PRIMARY KEY,",
        "  first_name TEXT NOT NULL,",
        "  last_name TEXT NOT NULL,",
        "  email TEXT NOT NULL UNIQUE,",
        "  company TEXT NOT NULL,",
        "  plan TEXT NOT NULL CHECK (plan IN ('free', 'starter', 'pro', 'enterprise')),",
        "  created_at TIMESTAMPTZ NOT NULL",
        ");",
        "",
        "CREATE TABLE " + TABLE_TICKETS + " (",
        "  id INTEGER PRIMARY KEY,",
        "  ticket_number TEXT NOT NULL UNIQUE,",
        "  customer_id INTEGER NOT NULL REFERENCES " + TABLE_CUSTOMERS + "(id),",
        "  subject TEXT NOT NULL,",
        "  body TEXT NOT NULL,",
        "  status TEXT NOT NULL CHECK (status IN ('open', 'in_progress', 'waiting_on_customer', 'resolved', 'escalated')),",
        "  priority TEXT NOT NULL CHECK (priority IN ('low', 'medium', 'high', 'urgent')),",
        "  channel TEXT NOT NULL CHECK (channel IN ('email', 'chat', 'phone')),",
        "  assigned_to TEXT,",
        "  created_at TIMESTAMPTZ NOT NULL,",
        "  updated_at TIMESTAMPTZ NOT NULL,",
        "  first_response_at TIMESTAMPTZ,",
        "  resolved_at TIMESTAMPTZ,",
        "  escalated_at TIMESTAMPTZ",
        ");",
        "",
        "CREATE TABLE " + TABLE_EVENTS + " (",
        "  id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,",
        "  ticket_id INTEGER NOT NULL REFERENCES " + TABLE_TICKETS + "(id),",
        "  event_type TEXT NOT NULL,",
        "  note TEXT,",
        "  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()",
        ");",
        "",
        "CREATE INDEX support_desk_tickets_status_idx ON " + TABLE_TICKETS + " (status);",
        "CREATE INDEX support_desk_tickets_customer_idx ON " + TABLE_TICKETS + " (customer_id);",
        "CREATE INDEX support_desk_tickets_updated_idx ON " + TABLE_TICKETS + " (updated_at);",
        "",
        "INSERT INTO " + TABLE_CUSTOMERS + " (id, first_name, last_name, email, company, plan, created_at) VALUES",
    ]
    cust_values = []
    for c in customers:
        cust_values.append(
            "  ({id}, {first_name}, {last_name}, {email}, {company}, {plan}, {created_at})".format(
                id=c["id"],
                first_name=sql_str(c["first_name"]),
                last_name=sql_str(c["last_name"]),
                email=sql_str(c["email"]),
                company=sql_str(c["company"]),
                plan=sql_str(c["plan"]),
                created_at=sql_ts(c["created_at"]),
            )
        )
    lines.append(",\n".join(cust_values) + ";")
    lines.append("")
    lines.append(
        "INSERT INTO " + TABLE_TICKETS + " ("
        "id, ticket_number, customer_id, subject, body, status, priority, channel, "
        "assigned_to, created_at, updated_at, first_response_at, resolved_at, escalated_at"
        ") VALUES"
    )
    t_values = []
    for t in tickets:
        t_values.append(
            "  ({id}, {ticket_number}, {customer_id}, {subject}, {body}, {status}, {priority}, {channel}, "
            "{assigned_to}, {created_at}, {updated_at}, {first_response_at}, {resolved_at}, {escalated_at})".format(
                id=t["id"],
                ticket_number=sql_str(t["ticket_number"]),
                customer_id=t["customer_id"],
                subject=sql_str(t["subject"]),
                body=sql_str(t["body"]),
                status=sql_str(t["status"]),
                priority=sql_str(t["priority"]),
                channel=sql_str(t["channel"]),
                assigned_to=sql_str(t["assigned_to"]),
                created_at=sql_ts(t["created_at"]),
                updated_at=sql_ts(t["updated_at"]),
                first_response_at=sql_ts(t["first_response_at"]),
                resolved_at=sql_ts(t["resolved_at"]),
                escalated_at=sql_ts(t["escalated_at"]),
            )
        )
    lines.append(",\n".join(t_values) + ";")
    lines.append("")
    # Keep serial-like sequences in sync if a later INSERT omits id.
    lines.append("SELECT setval(pg_get_serial_sequence('" + TABLE_EVENTS + "', 'id'), 1, false);")
    lines.append("")
    lines.append("COMMIT;")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def summarize(tickets: list[dict]) -> str:
    from collections import Counter

    status = Counter(t["status"] for t in tickets)
    stuck = [
        t
        for t in tickets
        if t["status"] in ("open", "in_progress") and t["updated_at"] < AS_OF - STUCK_AFTER
    ]
    lines = [
        f"as_of={AS_OF.isoformat()}",
        f"customers=25 tickets={len(tickets)}",
        f"status={dict(status)}",
        f"stuck_open_or_in_progress_over_48h={len(stuck)}",
        "stuck_ticket_numbers=" + ", ".join(t["ticket_number"] for t in stuck),
        "sample_stuck=",
    ]
    for t in stuck[:8]:
        hours = (AS_OF - t["updated_at"]).total_seconds() / 3600
        lines.append(
            f"  {t['ticket_number']} customer_id={t['customer_id']} status={t['status']} "
            f"priority={t['priority']} hours_stale={hours:.1f} subject={t['subject']}"
        )
    # Helpful named customers for the agent test prompts
    maya = [t for t in tickets if t["customer_id"] == 1]
    lines.append(f"maya_okonkwo_tickets={len(maya)}")
    for t in maya:
        lines.append(
            f"  {t['ticket_number']} {t['status']} {t['priority']} {t['subject']}"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    rng = random.Random(SEED)
    customers = customer_rows(rng)
    tickets = build_tickets(rng)

    fields_c = ["id", "first_name", "last_name", "email", "company", "plan", "created_at"]
    fields_t = [
        "id",
        "ticket_number",
        "customer_id",
        "subject",
        "body",
        "status",
        "priority",
        "channel",
        "assigned_to",
        "created_at",
        "updated_at",
        "first_response_at",
        "resolved_at",
        "escalated_at",
    ]
    write_csv(OUT / "customers.csv", customers, fields_c)
    write_csv(OUT / "tickets.csv", tickets, fields_t)
    # Empty events table file with header only, for optional CSV import.
    write_csv(OUT / "ticket_events.csv", [], ["id", "ticket_id", "event_type", "note", "created_at"])
    write_sql(OUT / "seed.sql", customers, tickets)
    summary = summarize(tickets)
    (OUT / "SEED_SUMMARY.txt").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()
