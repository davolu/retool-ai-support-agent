# Retool AI Support Agent

Companion files for the tutorial **Retool Full Tutorial: Build an AI Support Agent and Dashboard**, by [David Oluyale](https://github.com/davolu), Agentic AI Hub.

Video: [Retool Full Tutorial: Build an AI Support Agent and Dashboard](https://youtu.be/uHVCfgeTk4k)

This repo has the demo database seed, the workflow SQL and JavaScript, the agent instructions and tool definitions, and JSON exports of the dashboard, the workflow, and the agent in `exports/`.

The data is fictional. Customer emails use the `example.com` domain. Do not put API keys, `.env` files, workflow secrets, or database connection strings in this repo.

## What you will build

A small support desk in Retool Cloud:

1. A classic-app dashboard on Retool Database, with search and filters, a detail panel, a form to update status and priority, and charts for open work and first-response time.
2. A workflow, **Support Desk Escalate Stuck Tickets**, that flags tickets left idle for more than 48 hours. It can run on a schedule or from a webhook.
3. An agent, **Support Desk Agent** (the product may still show a Beta label), with tools to look up a customer, list tickets, draft a reply, and update a ticket after the human confirms.

Name new org-level objects with a Support Desk prefix so they stay easy to find.

## Repository layout

- `seed/` — Postgres-compatible SQL, CSVs, and the generator
- `workflow/` — blocks for the escalation workflow
- `agent/` — instructions, tool SQL, and test prompts
- `app/` — notes on exporting the classic app by hand
- `exports/` — JSON exports of the dashboard app, the escalation workflow, and the agent

## Prerequisites

- A Retool Cloud account. The Free plan is enough to follow along.
- The **classic** app editor (`Apps > Create > Classic app`). This project uses the Agent Chat component, which is documented for classic apps and is not supported in the new app builder at the time of writing.
- Retool Database, Workflows, and Agents enabled. Under Settings > AI, keep Retool AI Access and AI Agents on, and use a Retool-managed model key.

## Load the demo data

See `seed/README.md`. The safe SQL path is to run `seed/seed.sql` once. It only drops tables whose names start with `support_desk_`.

You should end up with 25 rows in `support_desk_customers` and 120 rows in `support_desk_tickets`.

## Build the app, workflow, and agent

Follow the SQL, JavaScript, component names, and agent text in `workflow/` and `agent/`. A full click-by-click build spec ships with the tutorial working files.

Suggested demo customer: Maya Okonkwo, `maya.okonkwo@example.com`. Suggested prompts are in `agent/instructions.md`.

## Import the exports

The three files in `exports/` are Retool JSON exports. Load the demo tables first (see `seed/README.md`). Each file is the app, workflow, or agent definition. Recreate the database connection after import: select your own Retool Database on every SQL block. The workflow file still carries the original database resource id, so those queries stay disconnected until you do that. These files contain no API keys. Keep workflow API keys, `.env` files, and connection strings out of the repo.

### App: `exports/Support_Desk_Dashboard.json`

This is the classic app **Support Desk Dashboard**.

Create a new classic app (`Apps > Create > Classic app`). In the app actions menu (`...`), choose **Replace app with JSON/ZIP** and select this file. That is the import path documented for classic apps. If the imported app has no name, rename it to **Support Desk Dashboard**.

### Workflow: `exports/Support_Desk_Escalate_Stuck_Tickets.json`

This is the workflow **Support Desk Escalate Stuck Tickets**.

On the Workflows landing page, click **Import** and select this file. From inside a workflow, the same action is the actions menu (`...`) > **Import from JSON**. Both labels are the ones in Retool's workflow import documentation.

Set the schedule after import. This file leaves `crontab` empty. The tutorial uses every hour in Africa/Lagos. Publish the workflow before automatic triggers will fire.

### Agent: `exports/Support_Desk_Agent.json`

This file is the agent **Support Desk Agent**.

Open the Agents area and use the import action that accepts a JSON file, when your organization shows one. Upload this file and keep the name **Support Desk Agent**. Retool's published agent docs describe importing tools from an existing agent, and they do not list a stable menu label for a full-agent JSON import, so follow the JSON import control on the Agents page. When that control is absent, create the agent from the text in `agent/instructions.md` and `agent/tools.md`.

After the agent is in your org, confirm that the `updateTicket` tool still requires the human to confirm before it writes. Deploy the agent before embedding it in the dashboard with the Agent Chat component.

## License

MIT. Copyright (c) 2026 David Oluyale, Agentic AI Hub.
