---
name: terns-exim
description: Company-specific brand, design, and messaging guidance for TERNS EXIM — navy/gold palette, merchant exporter positioning, quality-first tone, B2B trust signals — plus the full project architecture reference. Use for any TERNS EXIM-branded page, copy, or when you need the project's routes/services/deployment layout.
---

# TERNS EXIM

## Purpose

TERNS EXIM-specific guidance that sits on top of the general-purpose skills — [[premium-ui]], [[export-copywriting]], [[fastener-industry]], [[seo]] — and pins down what's unique to this brand: the exact palette, positioning, and tone, plus a full architecture reference for the codebase so any change can be placed correctly. This is the skill to load first for any task touching this repo's branding, copy, or overall structure.

---

## Part 1 — Brand & Design

### 1.1 Brand Identity

TERNS EXIM is a **B2B industrial fastener export company** based in Coimbatore, Tamil Nadu, India, operating as a **merchant exporter** — sourcing and exporting fasteners (hex bolts, nuts, washers, screws, anchor bolts, foundation bolts, threaded rods) to international manufacturing and construction buyers.

Positioning pillars — every page/CTA/copy decision should reinforce at least one:

1. **Merchant exporter, not just a factory** — TERNS EXIM's value is sourcing, quality verification, export documentation, and logistics across a network, not being tied to one production line. Say this plainly ("we export...", "we supply...") rather than implying in-house manufacturing that isn't confirmed.
2. **Quality-first, standards-driven** — every product claim anchors to a real DIN/ISO/ASTM standard and grade (see [[fastener-industry]]), backed by Mill Test Certificates and optional third-party inspection (SGS/BV/TUV).
3. **Export-process fluency** — Incoterms handled correctly (CIF preferred; FOB available against advance payment or L/C — confirmed policy, see commit `1f1e25d`), documentation, and logistics are part of the product, not an afterthought.
4. **Honest capability language** — per commit `182e35b`, never state unverifiable years-in-business, client counts, or track-record claims. See [[export-copywriting]] §2.

### 1.2 Color Palette — Navy Blue & Gold

**Single source of truth: the CSS custom properties in `static/css/style.css`'s `:root` block.** (As of the Nov 2026 design-system reconciliation pass, this superseded an earlier version of this doc that cited `#1A2A3A`/`#C9A84C` as canonical — that was itself one of three competing hex values found scattered across templates; all three have since been folded into the tokens below. Always check `:root` directly if this doc and the live CSS ever drift again.)

```
Navy (primary, structure/trust)
  var(--navy)       #002147   — primary dark navy (nav, footer, hero, primary text-on-light headings)
  var(--navy-mid)   #003177   — mid navy (gradients, secondary elements)
  var(--navy-light) #1B4F8A   — lighter navy (hover/active accents)
  var(--navy-deep)  #001535   — deepest navy (gradient end-stops, high-contrast dark fills)
  var(--navy-rgb)   0,33,71   — raw triplet for rgba(var(--navy-rgb), x) blends

Gold (accent, premium/quality signal — use sparingly)
  var(--gold)        #D4AF37  — primary gold accent (eyebrows, borders, highlights, icons)
  var(--gold-light)  #F0D060  — light gold (hover tint, gradient highlight)
  var(--gold-dark)   #9A7B0A  — dark gold (active/pressed states, gradient shadow)
  var(--gold-rgb)    212,175,55 — raw triplet for rgba(var(--gold-rgb), x) blends (tag backgrounds, focus rings)

Neutrals
  var(--white)       #FFFFFF  — card/content background
  var(--off-white)   #F4F6FB  — page background / light section bg / answer-block fill
  var(--gray-100..800) — neutral scale (#eef1f7 → #1f2a3d), cool navy-tinted per premium-ui §3
  var(--gray-200)    #E2E8F0  — the de facto "border/divider" gray used sitewide
  var(--text)         #111827 — primary text (near-black, not pure black)
  var(--text-light)   #5A6880 — body text on light background / muted copy

Semantic (status/state UI only — never reused for brand meaning)
  var(--success) / var(--success-bg), var(--warning) / var(--warning-bg), var(--danger) / var(--danger-bg)
```

**Rules:**
- Navy carries structure and trust (nav, headers, primary CTAs, footer) — it should dominate the page's visual weight.
- Gold is the **accent only** — eyebrows/kickers, left-border accent bars (see the direct-answer block pattern in [[product-page-geo]], now the shared `.answer-block` CSS class), icons, key highlights. Never use gold as a large fill/background — it reads as garish rather than premium at scale.
- Always reference the `var(--...)` token, never a literal hex, even in a page-local `{% block extra_head %}` `<style>` block — custom properties defined in `:root` cascade to every element in the document regardless of which stylesheet or inline `<style>` references them.
- Shared components extracted during the reconciliation pass: `.answer-block`, `.spec-table-caption`, `.faq-item-card` (product-page-geo pattern), plus the existing `.em-*` (enquiry modal), `.blog-card`, `.article-body`, `.article-toc`, `.cs-infobox` — all now pull from the tokens above instead of hardcoded hex.
- Follow [[premium-ui]] §3 for the full neutral-scale/semantic-color system built around this navy/gold core.

### 1.3 Premium Website Style, Not Generic AI Layout

TERNS EXIM sells trust and precision to industrial buyers — the site must look like it was built by a firm that understands manufacturing and export, not a templated startup landing page. Apply [[premium-ui]] in full, with these TERNS EXIM-specific emphases:

- **Concrete data over marketing fluff everywhere.** Spec tables, standards, grades, MOQ, certifications — always prefer a real table or fact list over a paragraph of adjectives (see [[fastener-industry]], [[export-copywriting]]).
- **No AI-generated startup tells.** No purple/pink gradients, no emoji icons, no generic "trusted by 500+ clients" logo strips without real verified logos, no stock photography of generic handshakes — see [[premium-ui]] §6 for the full checklist.
- **Industrial-appropriate imagery.** Real product photography (bolts, nuts, washers, threaded rods), technical diagrams, and factory/export-process imagery over abstract illustrations.
- **Gold accents signal quality/premium without shouting it** — a thin gold left-border on a key fact block, a gold eyebrow label, gold on hover states — restraint is what reads as premium to this B2B audience, not saturation.
- **Dense, fact-first sections** — an industrial buyer wants specs fast; don't pad pages with generic "why choose us" filler that could apply to any exporter.

### 1.4 B2B Trust Signals (TERNS EXIM-specific)

Reinforce these consistently, using only confirmed facts (never invented per §1.1 point 4):

- Location stated plainly: Coimbatore, Tamil Nadu 641001, India
- Business hours: Monday–Saturday, 9 AM–7 PM IST
- Direct contact channels: WhatsApp +91 63690 97465, plus the lead form
- Certification chain: Mill Test Certificates always; SGS/BV/TUV third-party inspection optional
- MOQ stated exactly: 10,000 pieces or 700 kg depending on size
- Incoterms policy stated exactly: CIF preferred; FOB available against advance payment or L/C
- Standards fluency: DIN/ISO/ASTM/BS/JIS/BIS referenced correctly per [[fastener-industry]]
- 30+ target export markets across 5 continents (per `base.html`'s Schema.org `areaServed`) — cite as target markets, not as a claim of existing shipment history unless confirmed

---

## Part 2 — Project Architecture Reference

*(Consolidated from the prior `terns-exim-skills.md`. This is the durable reference for where things live and how the system works — cross-check against root `CLAUDE.md` for the canonical high-level summary, which takes precedence if they ever diverge.)*

### 2.1 Overview

- **Website:** `https://ternsexim.com`
- **CRM API:** `https://terns-exim-api.onrender.com`
- **CRM Dashboard:** Netlify (React SPA)
- **GitHub Remote:** `https://github.com/ternsexim-bot/terns-exim-python.git`
- **WhatsApp:** +91 63690 97465
- **Office:** Coimbatore, Tamil Nadu 641001, India
- **Hours:** Monday–Saturday, 9 AM–7 PM IST

Three independently deployed services:

```
terns-exim-python/
├── app.py                     ← Marketing website (Flask, Render)
├── leads.py                   ← Lead CSV storage + WhatsApp alerts
├── crm_models.py              ← Legacy Lead model factory (dead code, not imported)
├── test_leads.py              ← Integration tests
├── migrate_to_postgres.py     ← SQLite → PostgreSQL migration util
│
├── crm/                        ← CRM REST API (Flask, Render, PostgreSQL)
│   ├── app.py
│   ├── models.py                ← Actual Lead model used in production
│   └── requirements.txt
│
├── crm-frontend/               ← CRM Dashboard (React + Vite, Netlify)
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api/leads.js         ← Axios client → terns-exim-api.onrender.com (hardcoded base URL)
│   │   └── components/
│   │       ├── Dashboard.jsx
│   │       ├── LeadsTable.jsx
│   │       ├── LeadStats.jsx
│   │       ├── AddLeadModal.jsx
│   │       └── ContactForm.jsx
│   ├── vite.config.js
│   ├── netlify.toml             ← SPA redirect, publish: dist/
│   └── package.json
│
├── templates/                  ← Jinja2 HTML templates
├── static/                     ← CSS, JS, images (NOT gitignored — required by Render)
├── render.yaml                 ← Two-service Render deployment spec
├── Procfile
├── requirements.txt
└── runtime.txt                 ← Python 3.11.9
```

### 2.2 Marketing Website (`app.py`) — Routes

| Method | Path | Template | Notes |
|---|---|---|---|
| GET | `/` | `index.html` | Homepage |
| GET | `/about` | `about.html` | Company info |
| GET | `/products` | `products.html` | Product catalog |
| GET | `/contact` | `contact.html` | Contact + lead form |
| GET | `/hex-bolts` | `hex_bolts.html` | Product detail |
| GET | `/anchor-bolts` | `anchor_bolts.html` | Product detail |
| GET | `/foundation-bolts` | `foundation_bolts.html` | Product detail |
| GET | `/nuts` | `nuts.html` | Product detail |
| GET | `/washers` | `washers.html` | Product detail |
| GET | `/threaded-rods` | `threaded_rods.html` | Product detail |
| GET | `/thank-you` | `thank_you.html` | Post-submission page |
| POST | `/submit-lead` | — | Lead capture, redirects to `/thank-you` or `/contact` |
| GET | `/favicon.ico` | — | Serves `static/images/favicon.png` |
| GET | `/robots.txt` | — | Serves `static/robots.txt` |
| GET | `/sitemap.xml` | — | Serves `static/sitemap.xml` |
| GET | `/health` | — | Returns `{"status": "ok"}` |

**Lead submission (`POST /submit-lead`)**:
1. Validate — name ≥2 chars, email regex, phone 7–15 digits, company and country required (`app.py` ~L165-169)
2. Save to CSV — `leads.py::save_lead()` → `leads.csv`
3. WhatsApp alert — optional, via CallMeBot API (non-blocking)
4. Forward to CRM — `POST https://terns-exim-api.onrender.com/leads` (1 retry, 3s timeout, background thread)
5. Redirect — `/thank-you` on success, `/contact` on validation failure

**Security headers** (global via `@app.after_request`): `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Content-Security-Policy` — update the CSP here whenever adding new external scripts/fonts/iframes, or they'll be silently blocked.

**Environment variables:**

| Variable | Default | Purpose |
|---|---|---|
| `BASE_URL` | `https://ternsexim.com` | SEO canonical URL |
| `PORT` | `10000` | Server port |
| `LEADS_CSV_PATH` | `leads.csv` | Path to lead storage file |
| `WHATSAPP_ALERT_ENABLED` | `false` | Enable WhatsApp alerts |
| `CALLMEBOT_API_KEY` | — | CallMeBot API key |
| `WHATSAPP_PHONE` | — | Phone number for alerts |
| `GOOGLE_SHEET_ID` | — | Phase 2 Google Sheets (not yet active) |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | — | Phase 2 Google Sheets credentials |

Static assets: 1-year `Cache-Control` (`max-age=31536000`); `static/` is intentionally **not** gitignored — Render deploys from committed files.

### 2.3 Lead Storage (`leads.py`)

Three-phase design:
- **Phase 1 (active):** CSV — `leads.csv`, fields `timestamp, name, email, phone, company, country, product, message`, auto-creates header row.
- **Phase 2 (ready, inactive):** Google Sheets via `GOOGLE_SHEET_ID`.
- **Phase 3 (ready):** WhatsApp alerts via CallMeBot, gated on `WHATSAPP_ALERT_ENABLED=true`.

Key functions: `save_lead(name, phone, email, product, message, company, country)`, `send_whatsapp_alert(lead)`.

### 2.4 Templates

- **`base.html`** — master layout: Schema.org JSON-LD (`Organization`, `LocalBusiness`, `OfferCatalog`), Open Graph + Twitter Card tags, canonical URL via `inject_seo()` context processor, 30+ target countries in `areaServed`. Popup enquiry modal (`openEnquiryModal()`/`closeEnquiryModal()`) — all sitewide CTA buttons trigger it via `href="#" onclick="openEnquiryModal(); return false;"` (candidate for conversion to real `<button>` elements per [[accessibility]] §1 when touched).
- **`contact.html`** — "Fastener Quotation" and "Export Inquiry" buttons open the popup modal; WhatsApp buttons and the inline `POST /submit-lead` form are separate and unchanged.
- **`_lead_form.html`** — reusable Jinja2 macro: `{% from "_lead_form.html" import lead_form %}` / `{{ lead_form(product="Hex Bolts", show_product_select=false) }}`. Required fields (name, phone, email, company, country) must stay in sync with server validation in `app.py`. Client-side validation lives in this file's own `<script>` block, not `main.js`.
- **Product pages** (`hex_bolts.html`, `nuts.html`, `washers.html`, `screws.html`, `anchor_bolts.html`, `foundation_bolts.html`, `threaded_rods.html`) — each covers description, specs (DIN/ISO/ASTM), size ranges, grades, applications, and a lead form. Apply [[product-page-geo]] for the required GEO structure.

### 2.5 Static Files

```
static/
├── css/style.css          ← all site styling (hand-written, no Tailwind currently)
├── js/main.js              ← navbar scroll, hamburger menu, IntersectionObserver scroll
│                              animations, FAQ accordion (click + keyboard Enter/Space)
├── images/
│   ├── logo.png
│   ├── favicon.png          ← served at /favicon.ico
│   └── products/*.jpg|png
├── robots.txt               ← all crawlers allowed, including AI bots
└── sitemap.xml               ← all page URLs with <lastmod>
```

### 2.6 CRM API (`crm/app.py`)

| Method | Path | Description |
|---|---|---|
| GET | `/api/health` | `{status, database, persistent}` |
| GET | `/leads` | List leads, optional `?status=` filter |
| POST | `/leads` | Create lead (JSON body) |
| PUT | `/leads/<id>` | Update lead fields/status |
| DELETE | `/leads/<id>` | Delete lead |
| GET | `/leads/stats` | Count by status |

Lead model fields: `id, name, email, phone, company, country, product_interest, message, status, source, created_at`. Status values: `New | Contacted | Negotiation | Won | Lost`.

Database: PostgreSQL via `DATABASE_URL`; normalizes `postgres://` → `postgresql+psycopg://` (psycopg3, since psycopg2 isn't compatible with the deployed Python version). **Every data route 503s via `_db_unavailable()` if `DATABASE_URL` isn't set — no fallback storage in this service** (unlike the marketing site's CSV fallback).

Dependencies: Flask, Flask-SQLAlchemy, Flask-CORS, SQLAlchemy, `psycopg[binary]`, gunicorn.

### 2.7 CRM Frontend (`crm-frontend/`)

React 18.3.1 + Vite 5.3.1 (dev port 3000) + React Router DOM 7 + Axios, deployed to Netlify.

- `src/api/leads.js` — hardcoded base URL `https://terns-exim-api.onrender.com`; no local proxy/env switching, so local dev talks to production API.
- Components: `Dashboard.jsx` (stats + filter + refresh + add), `LeadsTable.jsx` (status dropdown + delete), `LeadStats.jsx` (color-coded stat cards), `AddLeadModal.jsx` (new lead form), `ContactForm.jsx` (public enquiry form → CRM API).
- Product dropdown: Hex Bolts, Anchor Bolts, Foundation Bolts, Nuts, Washers, Threaded Rods, General Enquiry.
- Source dropdown: Website, Email, Phone, WhatsApp, Trade Fair, Referral, Other.
- `netlify.toml`: publish `dist/`, build `npm run build`, SPA redirect `/* → /index.html` (200).

### 2.8 Deployment

**Render (`render.yaml`)** — two services:
- `terns-exim` (marketing): Python 3.11.0, build `pip install -r requirements.txt`, start `gunicorn app:app --workers 2 --threads 2 --timeout 120`.
- `terns-exim-api` (CRM): Python 3.11.0, build `pip install -r crm/requirements.txt`, start `gunicorn crm.app:app --workers 2 --threads 2 --timeout 120`, requires `DATABASE_URL`.

**Netlify** — auto-deploys `crm-frontend/`, build `npm run build` → publish `dist/`.

**Key rules:** `static/` must never be gitignored; `crm-frontend/.netlify/` and `crm-frontend/dist/` are gitignored; Python locked to 3.11.9 via `runtime.txt`.

Deploy after changes:
```bash
git add <files>
git commit -m "type: description"
git push origin main    # Render + Netlify auto-deploy on push to main
```

### 2.9 Tests

`test_leads.py` — standalone script (not pytest-only, though pytest-runnable), sets `LEADS_CSV_PATH` to a temp file **before** importing `app`/`leads` so production `leads.csv` is never touched. Covers: GET routes return 200 (`/`, `/contact`, `/thank-you`, `/products`), `POST /submit-lead` returns 302 to `/thank-you`, lead written to CSV correctly, all required fields present.

```bash
python test_leads.py
# or
python -m pytest test_leads.py -v
```

### 2.10 Common Tasks

**Add a new product page:**
1. `templates/<product>.html` extending `base.html`, including `_lead_form.html` macro
2. Route in `app.py`: `@app.route('/product-slug')` → `render_template('product.html')`
3. Add to `static/sitemap.xml` with `<loc>`/`<lastmod>`
4. Add product card to `templates/products.html`
5. Add product option to `AddLeadModal.jsx` dropdown
6. Add product image to `static/images/products/`
7. Apply [[product-page-geo]] structure and [[fastener-industry]]-grounded specs

**Add a new target country:** update `base.html`'s Schema.org `areaServed`, `index.html` country cards, and `sitemap.xml` if a dedicated landing page is created.

**Modify lead form fields:** keep in sync across `app.py` (server validation), `templates/_lead_form.html`, `leads.py::save_lead()`, `crm/models.py` + `crm/app.py` POST handler, and `crm-frontend/src/components/AddLeadModal.jsx`.

### 2.11 .gitignore Rules

```
# NOT ignored — required for Render deployment
static/

# Ignored
crm/*.db
crm-frontend/node_modules/
crm-frontend/dist/
crm-frontend/.netlify/
__pycache__/
.env
venv/
```

---

## Quick Review Checklist

- [ ] Navy carries structural weight; gold used only as a restrained accent (never a large fill)
- [ ] No unverifiable years-in-business/client-count/testimonial claims (§1.1 point 4)
- [ ] MOQ, Incoterms, and certification language matches confirmed policy exactly (§1.4)
- [ ] No AI-generated-startup visual tells — apply [[premium-ui]] §6 in full
- [ ] New routes registered in `app.py` AND added to `sitemap.xml` in the same change
- [ ] Lead form field changes propagated across all five sync points (§2.10)
- [ ] Product content follows [[product-page-geo]] structure and [[fastener-industry]] domain accuracy
- [ ] `static/` never gitignored; CSP in `app.py` updated if new external resources are added
