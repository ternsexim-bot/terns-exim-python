---
name: seo
description: Enforce complete SEO implementation — metadata, Open Graph, Twitter cards, structured data (schema.org JSON-LD), sitemap.xml, robots.txt, canonical URLs, and semantic HTML. Use for any new page, or when reviewing SEO completeness.
---

# SEO

## Purpose

Every public page must be fully discoverable, correctly summarized in search/social previews, and marked up for both traditional search engines and AI answer engines (ChatGPT, Perplexity, Gemini, Google AI Overviews). This repo's marketing site (`app.py` + `templates/`) already has a working SEO foundation — extend it consistently rather than reinventing per page. For AI-engine-specific extraction structure on product pages, see [[product-page-geo]].

---

## 1. Metadata — Required on Every Page

Every page needs a unique, accurate `<title>` and meta description — never inherit the homepage's or leave a template default unfilled.

```html
<title>Stainless Steel Hex Bolts Exporter | DIN 933, A2-70/A4-80 | TERNS EXIM</title>
<meta name="description" content="TERNS EXIM exports stainless steel hex bolts (A2-70, A4-80) to DIN 933/931 and ISO 4014/4017 standards, M5–M64, from Coimbatore, India. MOQ 10,000 pcs. Mill Test Certificates included.">
```

**Rules:**
- Title: 50–60 characters, unique per page, primary keyword near the front, brand name at the end (`Page Topic | TERNS EXIM`).
- Meta description: 140–160 characters, includes a concrete reason to click (specs, standards, location) — not generic filler ("Learn more about our products").
- In this Flask codebase, this is Jinja2 `{% block title %}`/`{% block meta_description %}` (or equivalent) inside `base.html` — verify every template overrides these, never leaving the base default.
- In Next.js, this is the Metadata API (`generateMetadata`/static `metadata` export) — see [[nextjs]] §4. Never hand-write `<head>` tags.

## 2. Canonical URLs

Every page must self-declare its canonical URL to prevent duplicate-content penalties from trailing slashes, query params, or `www`/non-`www` variants.

```html
<link rel="canonical" href="{{ canonical_url }}">
```

This repo already injects `canonical_url` globally via `inject_seo()` (a Flask `context_processor` in `app.py`, using `BASE_URL` env var, default `https://ternsexim.com`) — confirm any new template actually renders it in `<head>`, and never hardcode a different canonical that could conflict.

## 3. Open Graph

Required on every page for correct link previews on LinkedIn, WhatsApp, Facebook — all channels a B2B exporter's leads and partners actually share links through.

```html
<meta property="og:title" content="Stainless Steel Hex Bolts Exporter | TERNS EXIM">
<meta property="og:description" content="Export-grade hex bolts, A2-70/A4-80, DIN 933/931. Coimbatore, India.">
<meta property="og:type" content="website">
<meta property="og:url" content="{{ canonical_url }}">
<meta property="og:image" content="{{ base_url }}/static/images/og/hex-bolts.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:site_name" content="TERNS EXIM">
<meta property="og:locale" content="en_US">
```

- OG image: 1200×630px, under 300KB, includes the product/page subject clearly (not just a generic logo card) — this is what shows up when a lead shares a product link on WhatsApp to a colleague.
- Provide a per-page OG image where the content justifies it (key product categories, homepage); fall back to a site-wide default banner otherwise — never a broken/missing image.

## 4. Twitter Cards

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Stainless Steel Hex Bolts Exporter | TERNS EXIM">
<meta name="twitter:description" content="Export-grade hex bolts, A2-70/A4-80, DIN 933/931. Coimbatore, India.">
<meta name="twitter:image" content="{{ base_url }}/static/images/og/hex-bolts.jpg">
```

`summary_large_image` is correct for essentially all pages here — reuse the same image/title/description as Open Graph rather than authoring separate copy.

## 5. Structured Data (schema.org JSON-LD)

This is what lets AI answer engines and Google's rich results cite the business directly rather than paraphrasing loosely.

**Site-wide (in `base.html`, already present per this repo's history)**: `Organization`, `LocalBusiness`, `OfferCatalog` — do not remove or restructure without reviewing recent commits (`b8d49dd`, `338d1d5` added/fixed schema here).

**Per product page**, additionally include a `Product` block:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Stainless Steel Hex Bolts",
  "description": "Hex bolts in A2-70 and A4-80 stainless steel, DIN 933/931, ISO 4014/4017.",
  "brand": { "@type": "Brand", "name": "TERNS EXIM" },
  "manufacturer": { "@type": "Organization", "name": "TERNS EXIM" },
  "offers": {
    "@type": "AggregateOffer",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "seller": { "@type": "Organization", "name": "TERNS EXIM" }
  }
}
</script>
```

**FAQ sections** get a matching `FAQPage` block — see [[product-page-geo]] for the exact required pattern and the rule that visible FAQ copy and JSON-LD text must match word-for-word.

**Rules:**
- Never fabricate schema data (ratings, review counts, prices) that isn't real — this violates Google's structured data guidelines and risks a manual action.
- Validate every new/changed schema block with Google's Rich Results Test or Schema Markup Validator before shipping.
- Multiple `<script type="application/ld+json">` blocks per page are fine and expected (Organization + Product + FAQPage, etc.) — verify count with `grep -c "application/ld+json"` matches what's intended, as done in [[product-page-geo]]'s workflow.

## 6. Sitemap.xml

`static/sitemap.xml` (served at `/sitemap.xml`) must list every public, indexable URL with `<lastmod>` and a reasonable `<priority>`.

```xml
<url>
  <loc>https://ternsexim.com/hex-bolts</loc>
  <lastmod>2026-08-02</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.8</priority>
</url>
```

**Rules:**
- Add every new route to the sitemap in the same change that adds the route in `app.py` — a page that exists but isn't in the sitemap is a silent SEO gap.
- Update `<lastmod>` when a page's content meaningfully changes, not on every unrelated deploy.
- Never include non-indexable pages (`/thank-you`, admin/CRM routes, `/health`) in the sitemap.
- Submit the sitemap in Google Search Console / Bing Webmaster Tools after significant additions.

## 7. Robots.txt

`static/robots.txt` (served at `/robots.txt`) controls crawler access — this site intentionally allows AI bots (GPTBot, Claude-Web, PerplexityBot, etc.) since AI-engine citation is a stated goal (see [[product-page-geo]]).

```
User-agent: *
Allow: /
Disallow: /admin
Sitemap: https://ternsexim.com/sitemap.xml
```

- Never accidentally `Disallow: /` (blocks everything) — double-check after any edit with Google Search Console's robots.txt tester.
- Explicitly `Disallow` only genuinely non-public paths (CRM/admin surfaces are on a separate domain already, so likely nothing needs blocking on the marketing site beyond utility routes).

## 8. Semantic HTML for SEO

Search engines and AI crawlers weight real semantic structure over styled `<div>` soup — this overlaps directly with [[accessibility]] §1.

- One `<h1>` per page matching the primary topic/keyword intent.
- Logical `h2`/`h3` hierarchy that mirrors a scannable outline — AI answer engines extract structure from heading hierarchy to decide what to quote.
- Use `<table>` for genuinely tabular data (spec sheets, comparison tables) — these are exactly what AI Overviews and featured snippets like to lift directly, per [[product-page-geo]]'s spec-table pattern.
- Descriptive link text (`Request a hex bolt quote`, not `click here`) — both for accessibility and because anchor text is a ranking signal.
- `alt` text on every content image, descriptive and keyword-relevant where genuinely accurate (never keyword-stuffed).

## 9. AI Answer Engine Optimization (GEO)

Beyond traditional SEO, structure key content pages (especially products) so an AI engine can lift a direct, accurate answer:

- Lead with a **direct-answer paragraph** immediately after the hero, stating the core facts (product, grades, standards, size range, MOQ, certifications) in plain prose before any marketing language — see [[product-page-geo]] for the exact required block.
- Follow with structured **spec tables** — tables are the highest-value target for extraction-based citation.
- Include a visible **FAQ section** phrased as real buyer questions, backed by matching `FAQPage` JSON-LD.
- Prioritize **fact density over adjectives** — "M5 to M64, DIN 933, A2-70" is quotable; "premium high-quality bolts" is not.

---

## Quick Review Checklist

- [ ] Unique `<title>` (50–60 chars) and meta description (140–160 chars) per page
- [ ] Canonical URL present and correct on every page
- [ ] Open Graph + Twitter Card tags present, image sized 1200×630
- [ ] Organization/LocalBusiness schema untouched; page-specific Product/FAQPage schema added where relevant
- [ ] New route added to `sitemap.xml` with `<lastmod>` in the same change
- [ ] `robots.txt` still allows all intended crawlers, including AI bots
- [ ] One `<h1>`, logical heading hierarchy, real `<table>` for tabular data
- [ ] Visible FAQ text matches FAQPage JSON-LD word-for-word
- [ ] Direct-answer block + spec table present on product/key content pages ([[product-page-geo]])
