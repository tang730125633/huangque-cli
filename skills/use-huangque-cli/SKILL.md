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
curl -fsSL https://raw.githubusercontent.com/tang730125633/huangque-cli/v0.8.0/install.sh | sh
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

Page entries are not direct execution. `text-video`, `short-drama`, `pricing-page`, `invite`, `recharge`, and `bots` only return a fixed Huangque URL; `--open-browser` only opens that page. Do not report a generation, order, payment, or Bot change from a navigation result. The device page belongs to `hq login` and is not a normal navigation capability.

The direct read-only capabilities also include inspiration catalog/likes, leads CRM, video avatars, audio slots, and short-drama projects/project/conversation/preflight. `inspiration-like` and `leads-crm-upsert` are ordinary writes and always require `--confirm`.

## Classify the side effect

- Navigation and reads: run after showing the requested target.
- External AI and ordinary writes: require current user authorization and the CLI's `--confirm` gate.
- Paid actions: first run without `--confirm`, show the returned cost and points, then wait for explicit approval. Reuse the identical input with `--confirm --quote-token <quote_token>` exactly once.
- Idempotent writes: preserve the same `request_id` after an uncertain response; use a new ID only for a genuinely new operation.
- Concurrent resources: read the latest object and preserve its `revision` or `base_version` when writing.

Never turn a read request into a write, paid task, upload, public message, or deletion.

## Prepare input safely

Pass a UTF-8 JSON object through stdin or `--input @file`. Keep input within the schema returned by `hq describe`.

For image upload, pass one explicit absolute PNG/JPG/WebP path with `--file`. For `video-upload`, pass one explicit absolute MP4/MOV/WebM path no larger than 32 MiB. Both uploads require `--confirm`; never scan directories, follow symbolic links, or expose the local path or filename as generation input.

For `image-generate`, Banana uses `provider=banana`, `model=nb2|pro`, its listed ratios, and at most 14 references. For `video-generate`, Sora uses `channel=sora`, `model=sora-2|sora-2-pro`, `seconds=4|8|12`, and at most one reference; do not send `duration` or `generate_audio`. Follow the returned `constraints` for every provider or channel.

For `digital-ip-text-generate`, use one ready `avatar_id` owned by the current account plus `text` and `voice`. For `digital-ip-audio-generate`, use one owned `avatar_id` and copy `audio_file` from the current account's asset result; never substitute a URL, local path, upload, or base64 audio. For `digital-ip-batch-generate`, pass 2–5 `avatars` objects containing distinct owned `avatar_id` values; all items share one `text` and `voice`.

For `cinematic-open-generate`, provide either one compatible `avatar_id` or 1–3 distinct `avatar_ids`, plus `prompt`; optionally use at most 8 private `reference_image_upload_ids` and 3 private `reference_video_upload_ids`. `cinematic-motion-generate` requires one owned `avatar_id` and exactly one `reference_video_upload_ids` item. `tryon-fast-generate` requires private person and clothes image upload IDs. `tryon-classic-generate` requires one private person video upload ID plus a clothes image upload ID, a background image upload ID, or both.

## Verify the result

- Check the process exit code and JSON `schema`.
- For asynchronous work, read the returned task with the supported task capability until terminal.
- A provider `completed` state alone is insufficient for media delivery; confirm the result URL exists and the requested artifact is usable.
- Report the capability, side effect, confirmation used, task or resource ID, final status, and any remaining user action. Never print credentials.
