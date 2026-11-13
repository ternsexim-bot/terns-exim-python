---
name: fastener-industry
description: Domain knowledge for industrial fasteners — DIN, ISO, and ASTM standards, stainless steel grades (304, 316, A2-70, A4-80), terminology, and industrial applications. Use whenever writing, reviewing, or fact-checking any product, spec, or technical content.
---

# Fastener Industry Domain Knowledge

## Purpose

Provide accurate domain grounding for fastener product content so specs, standards, and terminology are correct by default. **Never invent a standard, grade, or numeric spec that isn't in this reference or explicitly confirmed by the user/existing repo content** — see the "Content rules" in [[product-page-geo]]: if a spec is unknown, stop and ask rather than guessing. This document contains only widely-published, standard industry reference facts (ISO 898-1 property class values, standard grade compositions) that are safe to state without per-instance confirmation; product-specific details (which sizes/finishes TERNS EXIM actually stocks) must come from confirmed business facts, not this file.

---

## 1. Standards Systems

### DIN (Deutsches Institut für Normung — German standards)

The most commonly referenced fastener standard family internationally, especially in Europe, India, and Middle East trade.

| Standard | Covers |
|---|---|
| DIN 931 | Hex bolts, partial thread |
| DIN 933 | Hex bolts, full thread |
| DIN 934 | Hex nuts |
| DIN 985 | Nylon insert lock nuts (nyloc) |
| DIN 125 | Flat washers, Type A |
| DIN 127 | Spring lock washers |
| DIN 965 | Countersunk flat head machine screws |
| DIN 7982 | Self-tapping countersunk screws |
| DIN 912 | Socket head cap screws (Allen bolts) |
| DIN 6923 | Hex flange nuts |
| DIN 603 | Carriage bolts (cup/round head square neck) |

### ISO (International Organization for Standardization)

The globally harmonized successor/parallel to many DIN standards — increasingly the preferred reference for cross-border trade documentation.

| Standard | Covers |
|---|---|
| ISO 4014 | Hex bolts, partial thread (harmonized successor to DIN 931) |
| ISO 4017 | Hex bolts, full thread (harmonized successor to DIN 933) |
| ISO 4032 | Hex nuts, style 1 |
| ISO 7089 / 7090 | Flat washers |
| ISO 898-1 | Mechanical properties of steel fasteners — bolts, screws, studs (property classes) |
| ISO 3506 | Mechanical properties of stainless steel fasteners (the stainless equivalent of 898-1 — defines A2/A4 property classes) |

### ASTM (American Society for Testing and Materials)

Primary standard family for the North American market — often required for US-bound shipments and oil & gas / structural steel projects globally.

| Standard | Covers |
|---|---|
| ASTM A307 | Carbon steel bolts, general purpose (Grade A/B) |
| ASTM A325 | High-strength structural bolts (steel structures, bridges) |
| ASTM A193 | Alloy/stainless steel bolting for high-temp/high-pressure service |
| ASTM A194 | Carbon/alloy steel nuts for high-pressure/temperature service |
| ASTM F593 | Stainless steel bolts, hex cap screws, and studs |
| ASTM F594 | Stainless steel nuts |

**Cross-standard note:** DIN and ISO dimensional standards for common items (e.g. DIN 933/ISO 4017) are dimensionally near-identical in most cases but are not automatically interchangeable for a buyer's compliance purposes — always cite the standard actually certified/tested to, never treat them as freely swappable in copy.

## 2. Stainless Steel Grades

### 304 (18-8 / A2 family)

- Composition: ~18% chromium, ~8% nickel, austenitic.
- Good general corrosion resistance; not ideal for chloride-heavy/marine environments (susceptible to pitting/crevice corrosion in prolonged saltwater exposure).
- Widely used for indoor/general industrial, architectural, food-processing, and mild-outdoor applications.
- ISO 3506 designates the corresponding fastener property class as **A2**.

### 316 (A4 family)

- Composition: adds ~2–3% molybdenum to the 304 base — this is the key difference driving improved corrosion resistance.
- Significantly better resistance to chlorides and marine/coastal environments, making it the standard choice for marine hardware, offshore, chemical processing, and pharmaceutical equipment.
- Costs more than 304 due to molybdenum content and higher nickel — spec this only where the corrosion environment justifies it, otherwise 304/A2 is the economical default.
- ISO 3506 designates the corresponding fastener property class as **A4**.

### A2-70 and A4-80 (ISO 3506 property classes — the actual fastener specs)

These are the **property class designations for stainless fasteners**, not separate materials — they combine the steel family (A2 = 304-type, A4 = 316-type) with a strength code:

```
A2-70  — A2 (304-type) stainless, cold-worked to a tensile strength of ~700 MPa.
         The most common general-purpose stainless fastener class — good balance
         of strength and corrosion resistance for general industrial/structural use.

A4-80  — A4 (316-type) stainless, cold-worked to a tensile strength of ~800 MPa.
         Higher strength than A2-70 plus superior (marine-grade) corrosion resistance —
         the standard spec for marine, offshore, and high-chloride-exposure applications.
```

The number after the dash (e.g. `-70`, `-80`) indicates tensile strength ÷ 10 in MPa — the same convention as carbon steel property classes (see §3), just on the stainless (A-prefixed) scale.

## 3. Property Classes — Carbon/Alloy Steel (ISO 898-1)

Reference values, safe to state without per-instance confirmation (standard published figures):

| Property Class | Tensile Strength (MPa) | Yield Strength (MPa) | Typical Application |
|---|---|---|---|
| 4.6 | 400 | 240 | Light-duty, low-stress general fastening |
| 8.8 | 800 | 640 | General structural, machinery, automotive |
| 10.9 | 1040 | 940 | High-stress joints, heavy equipment, steel structures |
| 12.9 | 1220 | 1100 | Critical high-load applications, precision engineering |

The class number encodes the spec directly: first number × 100 = approximate tensile strength (MPa) ÷ 10; the digits after the decimal represent the yield-to-tensile ratio × 10 (e.g. class "8.8" = 800 MPa tensile, yield ratio 0.8 → 640 MPa yield).

## 4. Fastener Terminology

| Term | Definition |
|---|---|
| **Property class / grade** | The strength/material designation of a fastener (e.g. 8.8, A2-70) — not the same as "size" |
| **MOQ** | Minimum Order Quantity — smallest order an exporter will accept for a given product/size |
| **Mill Test Certificate (MTC)** | A document from the manufacturing mill certifying the chemical composition and mechanical properties of a specific batch — the baseline QA document expected on every export shipment |
| **Third-party inspection (SGS/BV/TUV)** | Independent verification of shipment quality/quantity before dispatch, by an accredited inspection agency (SGS, Bureau Veritas, TÜV) — usually optional, buyer- or contract-requested |
| **Full thread vs. partial thread** | Whether the bolt shank is threaded along its entire length (full/"set" screw style) or only partway up from the tip, leaving a smooth shank section |
| **Pitch** | The distance between adjacent thread crests, usually in mm for metric fasteners (e.g. M12 × 1.75) |
| **Proof load** | The maximum tensile load a fastener can withstand without permanent deformation — used in torque/clamp-force calculations |
| **Torque-tension relationship** | The engineering relationship between applied tightening torque and resulting clamping force — grade-, lubrication-, and thread-condition-dependent, critical for structural/safety-relevant joints |
| **Passivation** | A chemical treatment (typically nitric or citric acid) applied to stainless fasteners post-manufacture to remove free iron and enhance the natural chromium-oxide corrosion-resistant layer |
| **Hot-dip galvanizing (HDG)** | Zinc coating applied by immersing carbon steel fasteners in molten zinc — the standard heavy-duty corrosion protection for outdoor/structural carbon steel fasteners |
| **Anchor bolt / foundation bolt** | Fasteners embedded in concrete (cast-in or post-installed) to anchor structural steel, machinery baseplates, or equipment to a foundation |
| **Threaded rod / stud** | A fully-threaded rod with no head, used with nuts on both ends or embedded on one end — common in structural hanging, anchoring, and flange assemblies |
| **Nyloc / nylon insert lock nut** | A hex nut with a nylon ring insert that grips the bolt thread to resist loosening under vibration (DIN 985) |

## 5. Industrial Applications by Sector

Use these to ground copy in real, specific use cases (see [[export-copywriting]] §5) rather than vague "many industries" language:

| Sector | Typical fastener needs |
|---|---|
| **Marine / offshore** | A4/316 stainless for chloride resistance; hot-dip galvanized carbon steel for structural, non-wetted applications |
| **Construction / structural steel** | High-strength carbon steel (8.8, 10.9, ASTM A325) hex bolts, anchor bolts, foundation bolts, threaded rods |
| **Automotive / machinery manufacturing** | Precision property-class bolts (8.8–12.9), often zinc-plated or black oxide finished |
| **Oil & gas / petrochemical** | ASTM A193/A194 alloy bolting for high-temperature/pressure service; A4/316 stainless in corrosive process environments |
| **Food processing / pharmaceutical** | 304/316 stainless (A2/A4) for hygiene and corrosion resistance, often passivated |
| **Architectural / façade** | A2/A4 stainless for visible, weather-exposed fastening with corrosion and finish requirements |
| **General OEM / industrial manufacturing** | Broad range — property class and finish selected per application load and environment |

---

## Quick Review Checklist

- [ ] Standards cited (DIN/ISO/ASTM) are real, correctly numbered, and match what the standard actually covers
- [ ] Grade/property class values (MPa, A2-70/A4-80) match the published reference figures in this document
- [ ] 304 vs 316 (A2 vs A4) distinction used correctly — molybdenum content, marine suitability
- [ ] Terminology used precisely (e.g. "full thread" vs "partial thread", MOQ vs lead time, MTC vs third-party inspection)
- [ ] Application/sector claims are grounded in the fastener's actual grade/finish suitability, not generic
- [ ] Any spec not covered by this reference is confirmed with the user before being published — never invented
