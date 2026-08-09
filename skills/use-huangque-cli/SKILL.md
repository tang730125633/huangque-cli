---
name: use-huangque-cli
description: Discover and safely run Huangque main-site capabilities through the `hq` command. Use when a user asks an Agent to inspect Huangque capabilities, read account-bound data, open a workbench, prepare or submit a supported AI task, manage supported assets or projects, or automate a Huangque workflow while preserving login, confirmation, quote, idempotency, and revision safeguards.
---

# Use Huangque CLI

## Establish the client

1. From this repository, prefer `.venv/bin/hq` when it exists; otherwise locate `hq` with `command -v hq`.
2. Check the selected executable with `version --json`, then use that same path for every command in the task.
3. If the executable is missing or lacks the requested capability, show the reviewed installer and ask before installing or upgrading because it changes the user's machine:

```sh
curl -fsSL https://raw.githubusercontent.com/tang730125633/huangque-cli/v0.6.2/install.sh | sh
```

4. Run `doctor --json` before account-bound work.
5. Run `login --json` when authorization is absent or expired. Let the user complete browser device approval; never request a password, Cookie, API key, or token.

In the examples below, `hq` means the executable selected above; do not resolve a different PATH binary mid-task.

## Discover before acting

Run:

```sh
hq capabilities --json
hq describe <capability> --json
```

Treat these outputs as the current capability and input contract. Do not guess undocumented actions, fields, URLs, methods, or costs.

## Classify the side effect

- Navigation and reads: run after showing the requested target.
- External AI and ordinary writes: require current user authorization and the CLI's `--confirm` gate.
- Paid actions: first run without `--confirm`, show the returned cost and points, then wait for explicit approval. Reuse the identical input with `--confirm --quote-token <quote_token>` exactly once.
- Idempotent writes: preserve the same `request_id` after an uncertain response; use a new ID only for a genuinely new operation.
- Concurrent resources: read the latest object and preserve its `revision` or `base_version` when writing.

Never turn a read request into a write, paid task, upload, public message, or deletion.

## Prepare input safely

Pass a UTF-8 JSON object through stdin or `--input @file`. Keep input within the schema returned by `hq describe`.

For image upload, pass one explicit absolute PNG/JPG/WebP path with `--file`; do not scan directories or follow symbolic links.

## Verify the result

- Check the process exit code and JSON `schema`.
- For asynchronous work, read the returned task with the supported task capability until terminal.
- A provider `completed` state alone is insufficient for media delivery; confirm the result URL exists and the requested artifact is usable.
- Report the capability, side effect, confirmation used, task or resource ID, final status, and any remaining user action. Never print credentials.
