# TERNS EXIM — Complete Project Skills
**Last Updated: 2026-06-05**

## 1. Project Overview

**TERNS EXIM** is a B2B fastener export company based in Coimbatore, Tamil Nadu, India.
This repository is a production Flask marketing website with an integrated CRM system.

- **Website:** `https://ternsexim.com`
- **CRM API:** `https://terns-exim-api.onrender.com`
- **CRM Dashboard:** Netlify (React SPA)
- **GitHub Remote:** `https://github.com/ternsexim-bot/terns-exim-python.git`
- **WhatsApp:** +91 63690 97465
- **Office:** Coimbatore, Tamil Nadu 641001, India
- **Hours:** Monday–Saturday, 9 AM–7 PM IST

---

## 2. Architecture

Three independent services, all deployed separately:

```
fastener-website/
├── app.py                     ← Marketing website (Flask, Render)
├── leads.py                   ← Lead CSV storage + WhatsApp alerts
├── crm_models.py              ← Lead model factory
├── test_leads.py              ← Integration tests
├── migrate_to_postgres.py     ← SQLite → PostgreSQL migration util
│
├── crm/                       ← CRM REST API (Flask, Render, optional PostgreSQL)
│   ├── app.py
│   ├── models.py
│   └── requirements.txt
│
├── crm-frontend/              ← CRM Dashboard (React + Vite, Netlify)
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api/leads.js       ← Axios client → terns-exim-api.onrender.com
│   │   └── components/
│   │       ├── Dashboard.jsx
│   │       ├── LeadsTable.jsx
│   │       ├── LeadStats.jsx
│   │       ├── AddLeadModal.jsx
│   │       └── ContactForm.jsx
│   ├── vite.config.js
│   ├── netlify.toml           ← SPA redirect, publish: dist/
│   └── package.json
│
├── templates/                 ← Jinja2 HTML templates
├── static/                    ← CSS, JS, images (NOT gitignored — required by Render)
├── render.yaml                ← Two-service Render deployment spec
├── Procfile                   ← gunicorn entry for Heroku/Render alt
├── requirements.txt           ← Main site: Flask, gunicorn, requests
└── runtime.txt                ← Python 3.11.9
```

---

## 3. Flask Marketing Website (app.py)

### Routes

| Method | Path | Template | Notes |
|--------|------|----------|-------|
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

### Lead Submission Logic (`POST /submit-lead`)

1. **Validate** — name ≥ 2 chars, email regex, phone 7–15 digits, company and country required
2. **Save to CSV** — `leads.py::save_lead()` → `leads.csv`
3. **WhatsApp alert** — optional, via CallMeBot API (non-blocking)
4. **Forward to CRM** — POST to `https://terns-exim-api.onrender.com/leads` (1 retry, 3s timeout)
5. **Redirect** — `/thank-you` on success, `/contact` on validation failure

### Security Headers (applied globally via `@app.after_request`)

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: SAMEORIGIN`
- `Content-Security-Policy` — restricts styles, fonts, images, scripts

### Configuration (Environment Variables)

| Variable | Default | Purpose |
|----------|---------|---------|
| `BASE_URL` | `https://ternsexim.com` | SEO canonical URL |
| `PORT` | `10000` | Server port |
| `LEADS_CSV_PATH` | `leads.csv` | Path to lead storage file |
| `WHATSAPP_ALERT_ENABLED` | `false` | Enable WhatsApp alerts |
| `CALLMEBOT_API_KEY` | — | CallMeBot API key |
| `WHATSAPP_PHONE` | — | Phone number for alerts |
| `GOOGLE_SHEET_ID` | — | Phase 2 Google Sheets (not yet active) |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | — | Phase 2 Google Sheets credentials |

### Static Asset Caching

- Cache-Control max-age: **31,536,000 seconds (1 year)** for all static files
- `static/` is **NOT gitignored** — all images, CSS, JS must be committed for Render deployment

---

## 4. Lead Storage Module (leads.py)

Three-phase architecture:

- **Phase 1 (Active):** CSV file storage — `leads.csv`
  - Fields: `timestamp, name, email, phone, company, country, product, message`
  - Auto-creates header row on first write
- **Phase 2 (Ready):** Google Sheets — enable via `GOOGLE_SHEET_ID` env var
- **Phase 3 (Ready):** WhatsApp alerts via CallMeBot — enable via `WHATSAPP_ALERT_ENABLED=true`

Key functions:
- `save_lead(name, phone, email, product, message, company, country)` → returns lead dict
- `send_whatsapp_alert(lead)` → posts to `https://api.callmebot.com/whatsapp.php`, returns bool

---

## 5. Templates

### Base Template (`templates/base.html`)

Master layout with full SEO implementation:
- Schema.org JSON-LD: `Organization`, `LocalBusiness`, `OfferCatalog`
- Open Graph + Twitter Card meta tags
- Canonical URL via context processor (`BASE_URL` env var)
- Keywords: fastener export, OEM supplier, merchant export, DIN/ISO/ASTM standards
- 30+ target countries across 5 continents

**Popup Enquiry Modal** (added 2026-06-05):
- JS functions: `openEnquiryModal()` / `closeEnquiryModal()` defined in `base.html`
- Hidden by default, animates open/closed
- **All 31 CTA buttons sitewide** use `href="#" onclick="openEnquiryModal(); return false;"` — covers index.html (4), products.html (10), about.html (1), all 7 product detail pages (2 each), and base.html footer (2)
- Fields: Name*, Email*, Phone*, Company*, Country* (required), Product dropdown (optional), Message (optional)
- Product dropdown option: `<option value="General Enquiry">Merchant / Other Products</option>`
- Submits to `POST /submit-lead` — same server handler as the inline lead form
- Navbar "Contact" link, WhatsApp button, and `contact.html` itself are NOT wired to the modal

### Contact Page (`templates/contact.html`)

- **Fastener Quotation** button (L156) — opens popup modal via `openEnquiryModal()`
- **Export Inquiry** button (L186) — opens popup modal via `openEnquiryModal()`
- Both previously linked to external Google Forms (removed 2026-06-05)
- WhatsApp buttons and the inline direct enquiry form (`POST /submit-lead`) remain unchanged

### Reusable Lead Form (`templates/_lead_form.html`)

Jinja2 macro — import and call anywhere:
```jinja
{% from "_lead_form.html" import lead_form %}
{{ lead_form(product="Hex Bolts", show_product_select=false) }}
```
- Fields: Name*, Phone*, Email*, Company*, Country* (required), Product (hidden or dropdown, optional), Message (optional)
- Client-side validation via `validateLeadForm()` defined in `_lead_form.html`'s own `<script>` block — NOT in `main.js`
- Phone validation: disallows non-digit/space/+/-/() chars; digit count must be 7–15
- Submits to `POST /submit-lead`
- **All 5 required fields must match server validation in `app.py:165-169` or lead silently redirects to `/contact`**

### Product Pages

Each product page covers: description, specifications (DIN/ISO/ASTM standards), size ranges, grades, applications, industries served, and a lead form.

| Page | Standards | Size Range |
|------|-----------|------------|
| `hex_bolts.html` | DIN 931/933, ISO 4014/4017, ASTM A307 | M4–M100 |
| `nuts.html` | DIN 934/985 | M3–M80 |
| `washers.html` | DIN 125/127 | M3–M100 |
| `screws.html` | DIN 965/7982 | — |
| `anchor_bolts.html` | — | — |
| `foundation_bolts.html` | — | — |
| `threaded_rods.html` | — | — |

---

## 6. Static Files

```
static/
├── css/style.css          ← 63KB — all site styling
├── js/main.js             ← Navbar scroll, hamburger menu, scroll animations, FAQ accordion
├── images/
│   ├── logo.png
│   ├── favicon.png        ← Active favicon (served at /favicon.ico)
│   └── products/
│       ├── hexbolt.jpg
│       ├── anchor_bolts.png
│       ├── nuts.jpg
│       ├── screws.jpg
│       ├── threaded_rods.jpg
│       └── washers.jpg
├── robots.txt             ← All crawlers allowed including AI bots
└── sitemap.xml            ← XML sitemap with all page URLs
```

### main.js Behaviours
- Navbar: adds `.scrolled` class on scroll
- Hamburger menu: toggle + close on outside click or nav link click
- Scroll animations: IntersectionObserver → fade-in for feature cards, product cards, FAQ items
- FAQ accordion: click + keyboard (Enter/Space) toggle

---

## 7. CRM API (crm/app.py)

Separate Flask service deployed to Render as `terns-exim-api`.

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Returns `{status, database, persistent}` |
| GET | `/leads` | List leads, optional `?status=` filter |
| POST | `/leads` | Create lead (JSON body) |
| PUT | `/leads/<id>` | Update lead fields/status |
| DELETE | `/leads/<id>` | Delete lead |
| GET | `/leads/stats` | Count by status |

### Lead Model Fields

```
id, name, email, phone, company, country,
product_interest, message, status, source, created_at
```

### Status Values
`New` | `Contacted` | `Negotiation` | `Won` | `Lost`

### Database
- PostgreSQL via `DATABASE_URL` env var (Render managed DB)
- Auto-converts `postgres://` → `postgresql://` (Render quirk)
- Handles psycopg2/psycopg3 dialect compatibility
- Falls back to in-memory SQLite if `DATABASE_URL` not set

### Dependencies (`crm/requirements.txt`)
Flask, Flask-SQLAlchemy, Flask-CORS, SQLAlchemy, psycopg[binary], gunicorn

---

## 8. CRM Frontend (crm-frontend/)

React 18 + Vite SPA deployed to Netlify.

### Tech Stack
- React 18.3.1
- Vite 5.3.1 (dev server: port 3000)
- React Router DOM 7.16.0
- Axios 1.7.2

### API Client (`src/api/leads.js`)
Base URL: `https://terns-exim-api.onrender.com`
Functions: `getLeads()`, `createLead()`, `updateLead()`, `deleteLead()`, `getStats()`

### Components

| Component | Purpose |
|-----------|---------|
| `Dashboard.jsx` | Main view — stats cards, filter, refresh, add lead |
| `LeadsTable.jsx` | Table with status dropdown + delete per row |
| `LeadStats.jsx` | Color-coded stat cards by status |
| `AddLeadModal.jsx` | New lead form (all fields, product/source dropdowns) |
| `ContactForm.jsx` | Public enquiry form, submits to CRM API |

### Product Dropdown Options
Hex Bolts, Anchor Bolts, Foundation Bolts, Nuts, Washers, Threaded Rods, General Enquiry

### Source Dropdown Options
Website, Email, Phone, WhatsApp, Trade Fair, Referral, Other

### Netlify Config (`netlify.toml`)
- Publish: `dist/`
- Build: `npm run build`
- SPA redirect: `/* → /index.html` (200)

---

## 9. Deployment

### Render (`render.yaml`) — Two services

**Service 1: terns-exim** (Marketing website)
- Runtime: Python 3.11.0
- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app --workers 2 --threads 2 --timeout 120`

**Service 2: terns-exim-api** (CRM API)
- Runtime: Python 3.11.0
- Build: `pip install -r crm/requirements.txt`
- Start: `gunicorn crm.app:app --workers 2 --threads 2 --timeout 120`
- Env: `DATABASE_URL` (PostgreSQL connection string)

### Netlify (CRM Frontend)
- Auto-deploy from `crm-frontend/` directory
- Build: `npm run build` → publish `dist/`

### Key Deployment Rules
- `static/` must never be gitignored — Render reads committed files, not build artifacts
- `crm-frontend/.netlify/` is gitignored (Netlify cache)
- `crm-frontend/dist/` is gitignored (build output)
- Python version locked to 3.11.9 via `runtime.txt`

---

## 10. Tests (test_leads.py)

Integration test suite using a temporary CSV (never touches `leads.csv` in prod).

Test cases:
1. GET routes return HTTP 200 — `/`, `/contact`, `/thank-you`, `/products`
2. POST `/submit-lead` returns 302 redirect to `/thank-you`
3. Lead written to CSV with correct field values
4. All required fields present in stored lead dict

Run with: `python -m pytest test_leads.py`

---

## 11. Common Tasks

### Add a New Product Page

1. Create `templates/<product_name>.html` — extend `base.html`, include `_lead_form.html` macro
2. Add route in `app.py`:
   ```python
   @app.route('/product-slug')
   def product_name():
       return render_template('product_name.html')
   ```
3. Add to `sitemap.xml` with `<loc>` and `<lastmod>`
4. Add product card to `templates/products.html`
5. Add product option to `AddLeadModal.jsx` dropdown in CRM frontend
6. Add product image to `static/images/products/`

### Add a New Country to Target Markets

- Update `base.html` Schema.org JSON-LD `areaServed` array
- Update `index.html` country/market cards section
- Update `sitemap.xml` if a dedicated page is created

### Modify Lead Form Fields

- Server validation: `app.py` — `POST /submit-lead` handler
- HTML form: `templates/_lead_form.html`
- CSV schema: `leads.py::save_lead()` function signature + field list
- CRM model: `crm/models.py` Lead class + `crm/app.py` POST handler
- CRM frontend: `crm-frontend/src/components/AddLeadModal.jsx`

### Deploy After Changes

```bash
git add <files>
git commit -m "type: description"
git push origin main
```
Render auto-deploys on push to `main`. Netlify auto-deploys `crm-frontend/` changes.

### Run Locally

```bash
# Marketing website
pip install -r requirements.txt
python app.py          # runs on port 10000

# CRM API
pip install -r crm/requirements.txt
python crm/app.py      # runs on port 5001 (or set PORT env var)

# CRM Frontend
cd crm-frontend
npm install
npm run dev            # runs on port 3000
```

### Run Tests

```bash
python -m pytest test_leads.py -v
```

---

## 12. .gitignore Rules

```
# NOT ignored — required for Render deployment
static/             ← All CSS, JS, images must be committed

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

## 13. SEO Implementation

- **Schema.org JSON-LD** in `base.html`: `Organization`, `LocalBusiness`, `OfferCatalog`
- **Open Graph** tags for social sharing
- **Twitter Card** meta tags
- **Robots.txt** — all crawlers allowed (including AI bots like GPTBot, Claude-Web)
- **Sitemap.xml** — all public URLs with `<lastmod>` and `<priority>`; all 11 URLs last updated `2026-06-05`
- **Canonical URL** — injected via Flask context processor using `BASE_URL` env var
- **Keywords** — DIN/ISO/ASTM standards, merchant export, OEM supplier, 30+ countries

---

## 14. Lead Flow (End to End)

```
User fills form on website
        ↓
POST /submit-lead (app.py)
        ↓
Server validates (name, email, phone, company, country)
        ↓
leads.py::save_lead() → appends row to leads.csv
        ↓
send_whatsapp_alert() → CallMeBot API (if WHATSAPP_ALERT_ENABLED=true)
        ↓
POST https://terns-exim-api.onrender.com/leads (async, 1 retry)
        ↓
CRM API saves to PostgreSQL Lead table
        ↓
Redirect → /thank-you
        ↓
Sales team views lead in CRM Dashboard (React, Netlify)
        ↓
Updates lead status: New → Contacted → Negotiation → Won/Lost
```
