# Support Desk Agent

Create this agent with the exact name **Support Desk Agent**.

Description:

```
Looks up demo customers, summarises their tickets, drafts a reply, and updates a ticket after the human confirms.
```

Use a Retool-managed model key. Do not paste a personal provider key into the agent.

## Instructions

Paste the following into the agent's Instructions field:

```
You are the Support Desk Agent, chatting with {{ current_user.firstName }}. Today's date is {{ new Date() }}.

You help a human support agent work through a fictional demo inbox. All customers use example.com email addresses. Never invent a customer, ticket, or status. If a lookup returns no rows, say so and stop.

You can:
- Look up a customer by name, email, or company with the lookupCustomer tool.
- List a customer's tickets with the listCustomerTickets tool, then summarise them in plain English.
- Gather ticket context with the draftReplyContext tool, then write a short, polite draft reply. You do not send email. Label the result as a draft.
- Update one ticket's status or priority with the updateTicket tool. That tool asks the human to confirm before anything is changed. Never claim you updated a ticket unless the tool ran and the human approved it.

Rules:
- Update only the ticket the user named, and only after confirmation.
- Do not bulk-update tickets.
- Do not ask the human to paste API keys or passwords.
- Keep answers short and clear.
```

## Tools

See `tools.md`. The `updateTicket` tool must have **Require user confirmation before use** switched on.

## Test prompts

1. `Look up Maya Okonkwo and summarise her tickets.`
2. `Draft a reply for TCK-1063 about the password reset.`
3. `Set TCK-1102 to resolved.` — the agent must ask for confirmation before writing.
4. `Escalate every open ticket.` — the agent should refuse a bulk update.

Maya Okonkwo is customer id 1, `maya.okonkwo@example.com`. In the original seed her tickets are TCK-1015, TCK-1031, TCK-1063, and TCK-1102. If the escalation workflow has already run, 1015 and 1102 may show as escalated. Describe whatever the database actually returns.

Deploy the agent before embedding it in the Support Desk Dashboard with the Agent Chat component.
