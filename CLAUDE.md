# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository overview

This repo contains **two separately deployed Flask services** plus a React admin frontend for TERNS EXIM, an industrial fastener export company site:

1. **Marketing site** (repo root `app.py`) — the public website (`ternsexim.com`): server-rendered Jinja2 pages (product pages, blog, country landing pages) plus a lead-capture form.
2. **CRM API** (`crm/app.py`) — a separate Flask service (`terns-exim-api.onrender.com`) that persists leads to PostgreSQL and is consumed by both the marketing site (lead forwarding) and the CRM frontend.
3. **CRM frontend** (`crm-frontend/`) — a Vite + React admin dashboard that talks directly to the CRM API over HTTPS (not proxied through the marketing site).

These three deploy as independent services (see `render.yaml`), each with its own `Procfile`/`requirements.txt`. Do not assume code in one is importable by another except where explicitly handled (see `crm/app.py`'s try/except import of `models`, which supports being run either as `crm.app:app` from the repo root or as `app:app` from inside `crm/`).

## Commands

### Marketing site (repo root)
```bash
pip install -r requirements.txt
python app.py                    # runs on PORT env var, default 10000
python test_leads.py             # full test suite: routes, lead submission, CSV storage, data structure
```
`test_leads.py` is a standalone script (not pytest) — it sets `LEADS_CSV_PATH` to a temp file *before* importing `app`/`leads` so production `leads.csv` is never touched, then runs sequential test functions and exits non-zero on any failure.

### CRM API (`crm/`)
```bash
cd crm
pip install -r requirements.txt
python app.py                    # runs on PORT env var, default 10000
```
Requires `DATABASE_URL` env var to enable persistence; without it the app still boots but all `/leads*` routes return 503. Render supplies `postgres://` — the app normalizes this to `postgresql+psycopg://` (psycopg3 dialect; psycopg2 is NOT compatible with the Python version this deploys on).

### CRM frontend (`crm-frontend/`)
```bash
cd crm-frontend
npm install
npm run dev          # vite dev server on port 3000
npm run build
npm run preview
```
The API base URL is hardcoded in `crm-frontend/src/api/leads.js` (`https://terns-exim-api.onrender.com`) — there's no local proxy/env-based switching, so local frontend dev talks to the production CRM API.

### One-off migration
```bash
DATABASE_URL=postgresql://user:pass@host/db python migrate_to_postgres.py
```
Migrates a local `crm.db` SQLite file into PostgreSQL, deduping on `(name, email, created_at)`. Safe to re-run.

### Datasheet PDFs
```bash
python scripts/generate_datasheets.py
```
Regenerates the 7 product PDFs in `static/datasheets/` using ReportLab. Run from repo root.

## Architecture notes

### Lead flow (marketing site → CRM)
`POST /submit-lead` in `app.py` does four things on every valid submission:
1. `leads.save_lead()` — always appends to local `leads.csv` (Phase 1, synchronous, the durable local backup).
2. `leads.send_whatsapp_alert()` — no-op unless `WHATSAPP_ALERT_ENABLED=true` + `CALLMEBOT_API_KEY` are set.
3. `leads.send_telegram_alert()` — no-op unless `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` are set.
4. `_forward_to_crm()` — forwards the lead to the CRM API's `POST /leads` in a **daemon background thread**, with one retry after a 2s sleep. `quantity` and `destination_port` are folded into the `message` string before forwarding because the CRM's `Lead` model has no dedicated columns for them.

CSV (`leads.csv`) is the guaranteed-durable store; the CRM Postgres forward is best-effort (fire-and-forget thread, logged but not surfaced to the user on failure).

### Two competing `Lead` model definitions
- `crm/models.py` — the one actually used by `crm/app.py` (module-level `Lead` class, imported directly).
- `crm_models.py` (repo root) — a `init_lead_model(db)` factory producing an equivalent model. It is **not imported anywhere** in the current codebase; treat it as dead code / legacy unless you're specifically reconciling it.

Both define the same schema — keep them in sync if either is edited, or prefer consolidating onto `crm/models.py`.

### Marketing site routing pattern
`app.py` is a flat list of `@app.route` → `render_template()` pairs, one per page — no blueprints. New pages follow the same pattern: add a template under `templates/`, add a route function. `inject_seo()` (a `context_processor`) injects `canonical_url` into every template using `BASE_URL` (env var, defaults to `https://ternsexim.com`).

Security headers (CSP, X-Frame-Options, etc.) are applied globally via `after_request` in `app.py` — if you add new external resources (scripts, fonts, iframes), update the CSP there or they'll be silently blocked by browsers.

### CRM API
Simple REST CRUD over a single `Lead` model: `GET/POST /leads`, `PUT/DELETE /leads/<id>`, `GET /leads/stats` (counts by status), `GET /api/health` (reports DB connectivity). Every data route short-circuits to a 503 via `_db_unavailable()` if `DATABASE_URL` wasn't set at boot — there is no fallback storage in this service (unlike the marketing site's CSV fallback).

### Content structure
`templates/` holds one Jinja2 template per route, including per-country landing pages (`usa.html`, `uae.html`, `uk.html`, `netherlands.html`) and per-topic blog posts (`blog_*.html`) — these are largely static HTML with shared `base.html` layout, built for SEO (structured data / schema.org markup, per the recent commit history). `_lead_form.html` is a shared partial included by pages with an enquiry form.
