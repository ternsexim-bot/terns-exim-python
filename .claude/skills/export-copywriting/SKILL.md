---
name: export-copywriting
description: Write B2B copy for industrial export buyers — manufacturing companies and distributors sourcing stainless steel fasteners — that builds trust, states facts precisely, and drives strong CTAs. Use for any product copy, landing page copy, email, or lead-facing content.
---

# Export Copywriting

## Purpose

Write copy that speaks credibly to **international B2B industrial buyers** — procurement managers, sourcing agents, and technical buyers at manufacturing companies, EPC contractors, and distributors — evaluating TERNS EXIM as a supplier of stainless steel fasteners. This audience is skeptical, technically literate, and risk-averse (a wrong fastener grade can mean a failed shipment, a compliance violation, or a safety incident). Copy must earn trust through precision, not adjectives.

---

## 1. Know the Reader

The reader is typically:
- A **procurement/purchasing manager** comparing 3–5 suppliers on spec compliance, price, MOQ, and lead time.
- A **quality/compliance officer** checking standards conformance (DIN/ISO/ASTM — see [[fastener-industry]]) and certification availability (Mill Test Certificates, third-party inspection).
- A **first-time importer** who needs export logistics de-risked (Incoterms, documentation, payment terms) as much as the product itself.

They are not swayed by generic superlatives ("world-class quality", "best in industry"). They are swayed by **specificity**: exact grades, exact standards, exact MOQ, exact certification chain, and evidence the exporter understands export mechanics (not just manufacturing).

## 2. Core Principles

### Fact density over adjectives

```
❌ "We offer premium, high-quality stainless steel fasteners trusted by clients worldwide."
✅ "We export A2-70 and A4-80 stainless steel hex bolts to DIN 931/933 and ISO 4014/4017,
   M5–M64, with Mill Test Certificates on every shipment and optional SGS/BV/TUV inspection."
```

Every claim should be checkable. If a sentence could apply to any competitor unchanged, rewrite it with a specific, TERNS EXIM-true detail.

### Honest capability language — never unverifiable claims

Per this repo's own commit history (`182e35b` — "remove unverifiable experience and track-record claims, use honest capability language"), **never invent**:
- Years in business / "X years of experience" unless confirmed
- Client counts, countries served counts, or shipment volumes unless confirmed
- Named clients or testimonials without explicit permission and verification
- Awards, certifications, or memberships the company doesn't actually hold

Use **capability and process language** instead — describe what the company does and how, which is true and verifiable without needing a track-record number:

```
❌ "Trusted by 500+ clients across 30 countries for over a decade."
✅ "We handle export documentation, Incoterms negotiation, and quality certification
   for every shipment, from initial enquiry through customs clearance."
```

### Structure for scanning, not reading

B2B buyers scan before they read. Lead with the direct answer (see [[seo]]'s GEO section and [[product-page-geo]]), then support with tables, bullet specs, and short paragraphs. Never open a product page with three paragraphs of brand narrative before stating what the product actually is.

## 3. Trust-Building Elements

Trust is built through **verifiable, concrete signals**, not claims of trustworthiness:

| Trust signal | Why it works |
|---|---|
| Exact standards cited (DIN 933, ASTM A325) | Proves technical competence, lets buyer's QA team verify independently |
| Certification chain named (MTC, SGS/BV/TUV) | Answers the compliance officer's first question before they ask |
| Precise MOQ and lead-time language | Signals operational maturity — vague suppliers hide this |
| Location and business type stated plainly ("Coimbatore, India-based exporter") | Geographic and legal clarity, especially for first-time importers assessing risk |
| Clear Incoterms / payment-term positioning (see [[terns-exim]] for the CIF/FOB policy) | Shows the exporter understands trade mechanics, not just manufacturing |
| Specific contact channels with real response expectations | Reduces the "will anyone actually reply" anxiety of a cold enquiry |

Avoid manufactured trust signals: stock "trusted by" logo strips with no real client relationship, fake review counts, countdown-timer urgency tactics — these read as untrustworthy to exactly the sophisticated buyer this copy targets, and actively damage credibility.

## 4. Tone & Register

- **Professional, direct, technically fluent** — write as a knowledgeable export manager would speak to a peer buyer, not as a consumer ad.
- Avoid hype adjectives: "amazing", "revolutionary", "world-class", "best-in-class", "cutting-edge" — these are near-meaningless to a technical buyer and signal inexperience.
- Prefer active voice and concrete verbs: "We export...", "We supply...", "Every shipment includes..." over passive hedging ("Quality is ensured...").
- Use industry-correct terminology precisely (see [[fastener-industry]]) — misusing a standard or grade name is an instant credibility loss with a technical reader.
- Keep sentences reasonably short; avoid marketing-speak run-ons. A buyer reading on a phone in a factory office should get the point in one pass.
- Second person ("your project", "your specification") when addressing the buyer directly in CTAs and intros; first person plural ("we supply", "our export process") when describing the company.

## 5. Structuring Product & Landing Page Copy

Recommended order for a product page (aligns with [[product-page-geo]] and [[seo]]):

1. **H1** — product name, plain and searchable (e.g. "Stainless Steel Hex Bolts")
2. **Direct-answer paragraph** — product, grades, standards, size range, MOQ, certifications, in one factual paragraph
3. **Specification table** — exact, structured data
4. **Applications/industries** — where this product is actually used (marine, construction, automotive — see [[fastener-industry]]), grounding the spec in real use cases
5. **Why source from TERNS EXIM** — process/capability language: export documentation handling, certification chain, quality inspection options — never unverifiable claims
6. **Buyer FAQ** — real procurement questions (MOQ, lead time, customization, certification, payment terms)
7. **CTA / lead form** — see §6

## 6. Strong CTAs

CTAs for a B2B export audience should be **specific to the action and low-friction**, not generic:

```
❌ "Learn More"      →  ✅ "Request a Quote for Hex Bolts"
❌ "Submit"           →  ✅ "Send Enquiry — We Respond Within 24 Hours" (only if true)
❌ "Contact Us"       →  ✅ "Get Pricing & MOQ for Your Specification"
❌ "Click Here"       →  ✅ "Download Product Specification Sheet"
```

**Rules:**
- CTA copy should state exactly what happens next (a quote, a spec sheet, a callback) — ambiguity increases hesitation for a buyer making a professional decision.
- Only promise response times, availability, or service levels that are actually true and operationally supported — an unmet promise in the first interaction destroys trust with exactly this audience.
- Primary CTA per page should be singular and consistent in label (see [[premium-ui]] §4 on visual hierarchy) — don't scatter three differently-worded competing CTAs on one page.
- Reduce form friction: only require fields genuinely needed for a first response (name, email, phone, company, country — matches this repo's `_lead_form.html` required fields); optional fields (product, message, quantity, destination port) should stay optional.
- WhatsApp/direct-channel CTAs work well for this audience for quick technical questions — pair with the formal lead form for anything requiring a documented quote trail.

## 7. Export/Documentation-Specific Copy

When writing about logistics, documentation, or trade terms, be precise — this is a domain where vague language actively confuses buyers:

- **Incoterms**: state exactly which terms are offered and any conditions (e.g. this repo's confirmed policy: CIF preferred, FOB available against advance payment or L/C — see commit `1f1e25d`). Never say "flexible terms" without specifying what that means.
- **Certification**: name the actual certificate types offered (Mill Test Certificate always; SGS/BV/TUV third-party inspection optional) rather than "fully certified" as an unsupported blanket claim.
- **MOQ**: state the real figure and any size-dependent variation (this repo's confirmed MOQ: 10,000 pieces or 700 kg depending on size) — never round down or omit conditions to sound more accessible than the actual policy.
- **Lead time**: if it varies by order (as is typical), say "quote on enquiry" rather than fabricating a fixed number that will later be contradicted.

---

## Quick Review Checklist

- [ ] Every factual claim is specific and checkable (grade, standard, size, MOQ, certification)
- [ ] No invented years-in-business, client counts, or unverified testimonials
- [ ] No hype adjectives substituting for real information
- [ ] Industry terminology used correctly (cross-check against [[fastener-industry]])
- [ ] Copy structured for scanning: direct answer → spec table → context → FAQ → CTA
- [ ] Trust signals are concrete and verifiable, not manufactured urgency/social proof
- [ ] CTA states the specific next action, matches actual operational capability
- [ ] Incoterms, certification, and MOQ language matches confirmed company policy exactly
