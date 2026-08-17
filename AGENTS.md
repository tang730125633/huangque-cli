# HQ CLI agent rules

## Scope

- This repository owns the public `hq` client, installer, MCP adapter, and tests.
- The canonical `use-huangque-cli` Skill lives in `tang730125633/huangque-agent-skill`; this CLI may install verified, versioned releases but must not keep a second copy.
- Huangque server routes, permissions, billing, and task implementations remain in the private main-site repository.

## Required checks

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/hq version --json
.venv/bin/hq doctor --json
git diff --check
```

## Security contract

- Keep the production origin and allow-listed paths fixed; never add arbitrary base URLs, methods, redirects, or admin routes.
- Never accept account passwords, browser cookies, API keys, or tokens through command arguments.
- External AI and writes require explicit confirmation. Paid actions require server quote, identical input, `quote_token`, and confirmation.
- Preserve idempotency (`request_id`) and optimistic concurrency (`revision` / `base_version`) where the capability requires them.
- Do not commit credentials, generated user data, private API implementation, or production logs.

## Release

- Bump both `setup.cfg` and `src/hq_cli/__init__.py`.
- Build one wheel, write its SHA-256 into `install.sh`, rerun tests, and publish matching tag and release assets.
- Recheck the independent Agent Skill compatibility manifest whenever commands, capability schemas, confirmation rules, or MCP mappings change.
