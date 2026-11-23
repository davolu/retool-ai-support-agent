# App export placeholder

After the Support Desk Dashboard classic app is built, export it from the Retool editor:

1. Open **Support Desk Dashboard**.
2. App actions (`...`) > **Export to JSON**.
3. Save the file here as `Support_Desk_Dashboard.json`.

The official export contains queries, components, and modules. It does not contain resources, and it should not contain API keys. Still scan the file for emails, workspace hostnames, or secrets before committing it.

To import later: create a new classic app, then `...` > **Replace app with JSON/ZIP**, and point queries at Retool Database.

This folder is empty of an export on purpose until that scan is done.
