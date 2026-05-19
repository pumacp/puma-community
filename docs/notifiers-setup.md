# Notifiers setup

PUMA Community supports two optional notification channels: a Discord webhook
and a Telegram bot. Both are **disabled by default**: each workflow runs only
on a manual `workflow_dispatch` trigger and skips cleanly if its required
secrets are absent.

To enable a notifier, configure the secrets listed below in the repository
settings (**Settings → Secrets and variables → Actions → New repository
secret**) and trigger the workflow manually from the **Actions** tab. Once
you've confirmed it works end-to-end, opt into the production trigger by
uncommenting the `push:` block at the top of the workflow YAML — that block
fires the notifier whenever a new submission lands on `main`.

---

## Discord webhook

Workflow file: `.github/workflows/notify-discord.yml`.

**Required secret:** `DISCORD_WEBHOOK_URL`.

1. Open the Discord channel that should receive the notifications.
2. **Server Settings → Integrations → Webhooks → New Webhook**. Pick the
   target channel, copy the webhook URL. Discord's official walkthrough:
   <https://support.discord.com/hc/en-us/articles/228383668>.
3. Add it to the repository as a secret named `DISCORD_WEBHOOK_URL`
   (**Repo Settings → Secrets and variables → Actions → New repository
   secret**).
4. Trigger manually: **Actions → notify-discord → Run workflow**.

The workflow scans the latest commit for newly added files under
`submissions/`. For each one, it posts a single message with an embed
containing the submission ID, scenario, model, strategy, submitter alias,
the scalar metrics that are present (F1 macro, MAE, CO2 grams), and a link
back to the JSON file on `main`.

---

## Telegram bot

Workflow file: `.github/workflows/notify-telegram.yml`.

**Required secrets:** `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.

1. Open Telegram and start a chat with **@BotFather**. Send `/newbot`,
   follow the prompts, and copy the bot token BotFather returns.
2. Find the chat ID of the channel or group that should receive
   notifications:
   - Add the bot to the target channel / group.
   - Send any message to that chat (or to the bot directly for a private
     DM).
   - Fetch `https://api.telegram.org/bot<TOKEN>/getUpdates` in a browser
     and read `result[].message.chat.id`. Channel IDs are negative
     integers; group IDs are also negative; private chats are positive.
   - Alternative: forward a message from the target chat to **@userinfobot**
     and read the `Chat ID` it reports.
3. Add both `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` to the repository
   secrets.
4. Trigger manually: **Actions → notify-telegram → Run workflow**.

The workflow scans the latest commit for newly added files under
`submissions/` and posts a Markdown-formatted message per submission via
the Telegram Bot API's `sendMessage` endpoint.

---

## Trust model

Notifications go **outward only**. Neither workflow modifies the canonical
repository state, reads secrets back out of the runner environment, or
interacts with the validation workflow. A misconfigured webhook or
unreachable bot causes the workflow to exit with a non-zero status, but the
merged submission remains intact and the next run of the workflow can
retry.

Both workflows are gated on their secrets. A workflow with missing secrets
prints a "Skipping: …" message and exits 0 without making any external
request, so accidentally clicking **Run workflow** on a freshly-cloned
fork is harmless.

The helper script `scripts/notify.py` reads tokens / webhook URLs from
environment variables only, masks any token reference in log lines via a
`mask()` helper (first four + last four characters), and never echoes the
raw value to stdout.

---

## Production trigger activation

Once you've verified a notifier with `workflow_dispatch`, opt into the
production trigger by uncommenting the leading block in the YAML file:

```yaml
# push:
#   branches: [main]
#   paths: ['submissions/*.json']
```

After uncommenting, the workflow fires automatically on every push to
`main` that touches `submissions/*.json` — i.e. every time the
auto-merge workflow accepts a new submission.
