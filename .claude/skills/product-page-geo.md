# Product Page GEO Skill

## Purpose
Apply identical extraction-optimized structure to every TERNS EXIM product page so AI engines (ChatGPT, Perplexity, Gemini, Google AI Overviews) cite these pages directly as a source.

## Reference implementation
`templates/hex_bolts.html` (commit `84d7943`) is the gold-standard example. Mirror its structure exactly.

---

## Required elements (in this order, after the hero/H1)

### Element 1 — DIRECT ANSWER BLOCK
A single plain paragraph inside a gold left-border box, placed immediately after the `</section>` closing tag of the page hero and before the `<!-- OVERVIEW -->` section.

**Must mention all of:**
- Product name
- TERNS EXIM is a Coimbatore, India-based exporter
- Property classes / grades (e.g. 8.8, 10.9, 12.9)
- Size range (e.g. M5 to M64)
- Available finishes (e.g. plain, zinc-plated, hot-dip galvanized)
- MOQ: 10,000 pieces or 700 kg depending on size
- Certifications: Mill Test Certificates, optional SGS / BV / TUV

**Exact HTML pattern (copy and fill in):**
```html
<!-- DIRECT ANSWER BLOCK + SPEC TABLES -->
<section class="section section-light" style="padding-top: 2rem; padding-bottom: 2.5rem;">
  <div class="container">

    <div style="border-left: 4px solid #c9a84c; background: #f5f7fa; padding: 1.25rem 1.5rem; border-radius: 0 6px 6px 0; margin-bottom: 2.5rem;">
      <p style="margin: 0; line-height: 1.8; color: #1a2a3a; font-size: 1rem;">TERNS EXIM is a Coimbatore, India-based exporter of [PRODUCT] in [GRADES/CLASSES], manufactured to [STANDARDS]. We supply sizes from [SIZE RANGE] in [FINISHES], with a minimum order quantity of 10,000 pieces or 700 kg depending on size. Every shipment includes Mill Test Certificates, with optional third-party inspection by SGS, BV, or TUV.</p>
    </div>

    <!-- Spec table and comparison table go here (see Elements 2 and 3) -->

  </div>
</section>
```

---

### Element 2 — SPECIFICATION TABLE
Inside the same section as Element 1, after the answer block div.

**Exact HTML pattern:**
```html
    <div style="overflow-x: auto; margin-bottom: 2.5rem;">
      <table class="pl-spec-table">
        <caption style="caption-side: top; text-align: left; font-weight: 600; font-size: 1rem; color: #1a2a3a; padding-bottom: 0.6rem;">[Product] Specifications</caption>
        <thead><tr><th>Specification</th><th>Details</th></tr></thead>
        <tbody>
          <tr><td>Property Classes</td><td>[e.g. 8.8, 10.9, 12.9 (high tensile)]</td></tr>
          <tr><td>Size Range</td><td>[e.g. M5 to M64]</td></tr>
          <tr><td>Standards</td><td>[e.g. DIN 931, DIN 933, ISO 4014, ISO 4017, ASTM A325, BS, JIS, BIS]</td></tr>
          <tr><td>Finishes</td><td>[e.g. Plain / Black, Zinc Plated, Hot-Dip Galvanized (HDG)]</td></tr>
          <tr><td>Thread Type</td><td>[or Type / Form as appropriate for the product]</td></tr>
          <tr><td>Material</td><td>[e.g. Carbon steel, alloy steel]</td></tr>
          <tr><td>MOQ</td><td>10,000 pieces or 700 kg</td></tr>
          <tr><td>Certification</td><td>Mill Test Certificate; optional SGS / BV / TUV</td></tr>
          <tr><td>Lead Time</td><td>Quote on enquiry</td></tr>
        </tbody>
      </table>
    </div>
```

---

### Element 3 — COMPARISON TABLE
Inside the same section, after the spec table. For products with grades (bolts, rods): use property class vs MPa values. For products with types (nuts, washers): compare type vs use case.

**Pattern for grade comparison (ISO 898-1 values — safe to use):**
```html
    <div style="overflow-x: auto;">
      <table class="pl-spec-table">
        <caption style="caption-side: top; text-align: left; font-weight: 600; font-size: 1rem; color: #1a2a3a; padding-bottom: 0.6rem;">[Product] Property Class Comparison</caption>
        <thead><tr><th>Property Class</th><th>Tensile Strength (MPa)</th><th>Yield Strength (MPa)</th><th>Typical Application</th></tr></thead>
        <tbody>
          <tr><td>8.8</td><td>800</td><td>640</td><td>General structural, machinery, automotive</td></tr>
          <tr><td>10.9</td><td>1040</td><td>940</td><td>High-stress joints, heavy equipment, steel structures</td></tr>
          <tr><td>12.9</td><td>1220</td><td>1100</td><td>Critical high-load applications, precision engineering</td></tr>
        </tbody>
      </table>
    </div>
```

**Pattern for type comparison (nuts, washers, etc.):**
```html
    <div style="overflow-x: auto;">
      <table class="pl-spec-table">
        <caption style="caption-side: top; text-align: left; font-weight: 600; font-size: 1rem; color: #1a2a3a; padding-bottom: 0.6rem;">[Product] Type Comparison</caption>
        <thead><tr><th>Type</th><th>Standard</th><th>Typical Use</th></tr></thead>
        <tbody>
          <!-- fill in confirmed rows -->
        </tbody>
      </table>
    </div>
```

---

### Element 4 — BUYER FAQ SECTION (visible HTML)
Placed before the `<!-- REQUEST QUOTE FORM -->` comment. Three Q&As phrased as real importer questions. Use `section-light` background.

**Exact HTML pattern:**
```html
<!-- BUYER FAQ -->
<section class="section section-light">
  <div class="container">
    <div class="section-header">
      <p class="section-eyebrow">Buyer FAQ</p>
      <h2 class="section-title">Frequently Asked Questions — [Product]</h2>
    </div>
    <div style="max-width: 800px; margin: 0 auto;">
      <div style="border: 1px solid #e2e8f0; border-radius: 8px; padding: 1.25rem 1.5rem; margin-bottom: 1rem; background: #fff;">
        <h3 style="margin: 0 0 0.5rem; font-size: 1rem; font-weight: 600; color: #1a2a3a;">[Question 1]</h3>
        <p style="margin: 0; color: #4b5563; line-height: 1.75;">[Answer 1]</p>
      </div>
      <div style="border: 1px solid #e2e8f0; border-radius: 8px; padding: 1.25rem 1.5rem; margin-bottom: 1rem; background: #fff;">
        <h3 style="margin: 0 0 0.5rem; font-size: 1rem; font-weight: 600; color: #1a2a3a;">[Question 2]</h3>
        <p style="margin: 0; color: #4b5563; line-height: 1.75;">[Answer 2]</p>
      </div>
      <div style="border: 1px solid #e2e8f0; border-radius: 8px; padding: 1.25rem 1.5rem; margin-bottom: 1rem; background: #fff;">
        <h3 style="margin: 0 0 0.5rem; font-size: 1rem; font-weight: 600; color: #1a2a3a;">[Question 3]</h3>
        <p style="margin: 0; color: #4b5563; line-height: 1.75;">[Answer 3]</p>
      </div>
    </div>
  </div>
</section>
```

---

### Element 5 — FAQPage JSON-LD
Added inside `{% block extra_schema %}`, after the existing Product and WebPage `<script>` blocks, before `{% endblock %}`. NEVER remove or modify existing schema blocks.

**Exact pattern:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Question 1 — must match visible FAQ exactly]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer 1]"
      }
    },
    {
      "@type": "Question",
      "name": "[Question 2]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer 2]"
      }
    },
    {
      "@type": "Question",
      "name": "[Question 3]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer 3]"
      }
    }
  ]
}
</script>
```

After adding, `grep -c "application/ld+json"` on the page must return **3** (Product + WebPage + FAQPage).

---

## Content rules

- **Use ONLY confirmed specs.** If grades, sizes, or standards are unknown for a product, STOP and ask the user before writing anything. Never invent numbers.
- **ISO 898-1 tensile/yield MPa values are safe to use** for standard property classes (8.8, 10.9, 12.9) without asking.
- **MOQ is always:** 10,000 pieces or 700 kg — confirmed business fact, use verbatim.
- **Certifications are always:** Mill Test Certificates; optional SGS / BV / TUV — use verbatim.
- **Do not add new global CSS classes.** Use `pl-spec-table`, `section`, `section-light`, `container`, `section-header`, `section-eyebrow`, `section-title` — all already defined. Use inline styles for the answer block and FAQ cards exactly as shown above.
- **Fact density over marketing language.** Exact grades, sizes, standards, MPa values — not adjectives.
- **The visible FAQ Q&As and the JSON-LD FAQPage must match word-for-word.**

---

## Workflow (follow in order)

1. `git remote -v` — must show `ternsexim-bot/terns-exim-python`. Stop if wrong.
2. `cat templates/[product].html` — read the full page before touching anything.
3. Ask the user to confirm product-specific specs (grades, size range, standards, finishes) if not already provided.
4. Add Element 5 (FAQPage JSON-LD) to `{% block extra_schema %}`.
5. Add Elements 1–3 (answer block + two tables) after the hero `</section>`, before `<!-- OVERVIEW -->`.
6. Add Element 4 (visible FAQ) before `<!-- REQUEST QUOTE FORM -->`.
7. Verify: `grep -n "[key spec term]" templates/[product].html` and `grep -c "application/ld+json" templates/[product].html` (must be 3).
8. `git add templates/[product].html`
9. `git commit -m "feat: GEO content for [product] - answer block, spec tables, FAQ"`
10. `git push origin main` — report commit hash.
11. Touch no other files.

---

## Pages to apply this to (status)

| Template | Status |
|---|---|
| `templates/hex_bolts.html` | ✅ Done — commit `84d7943` |
| `templates/anchor_bolts.html` | ⬜ Pending |
| `templates/foundation_bolts.html` | ⬜ Pending |
| `templates/nuts.html` | ⬜ Pending |
| `templates/washers.html` | ⬜ Pending |
| `templates/screws.html` | ⬜ Pending |
| `templates/threaded_rods.html` | ⬜ Pending |
