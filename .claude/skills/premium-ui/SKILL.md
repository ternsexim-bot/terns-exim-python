---
name: premium-ui
description: Design and build premium, enterprise-grade UI that looks hand-crafted by a senior design team, not AI-generated. Use whenever creating or reviewing pages, components, cards, sections, or layouts.
---

# Premium UI

## Purpose

Enforce a visual design system that reads as **premium, enterprise SaaS / industrial B2B** — the kind of polish buyers associate with companies like Stripe, Linear, or a well-funded export/manufacturing brand — and actively avoid the generic "AI-generated landing page" look (centered hero, purple-to-blue gradient, oversized rounded emoji icons, generic stock illustrations, Inter font at default weights with no hierarchy).

Apply this skill to every new page, section, or component, and when reviewing existing UI for quality.

---

## 1. The 8px Spacing System

All spacing (margin, padding, gap) must be a multiple of **8px** (or 4px for fine adjustments only — never arbitrary values like `13px` or `22px`).

```
4px   — micro (icon-to-label gap, tight inline spacing)
8px   — xs   (tight component padding, chip padding)
16px  — sm   (default component padding, form field gaps)
24px  — md   (card padding, section internal gaps)
32px  — lg   (gap between related cards/blocks)
48px  — xl   (gap between distinct content groups)
64px  — 2xl  (section vertical padding, mobile)
96px  — 3xl  (section vertical padding, desktop)
128px — 4xl  (hero section padding, major section breaks)
```

**Rules:**
- Never mix arbitrary pixel values into a layout that otherwise uses the scale — it's the fastest tell of unpolished work.
- Section vertical padding should scale down on mobile (e.g. `96px` desktop → `48px` mobile), never stay fixed.
- Card internal padding is almost always `24px` or `32px`, never less than `16px`.
- In Tailwind, this maps directly to the default spacing scale (`4 = 16px`... actually `1 = 4px`), so `p-6` (24px), `p-8` (32px), `gap-4` (16px) etc. are already 8px-aligned — just never use arbitrary `p-[13px]` values.

## 2. Professional Typography Scale

Use a constrained modular scale — never more than 6 font sizes on a single page.

```
Display   — 56–72px / weight 700–800 / line-height 1.05–1.1 / tracking -0.02em   (hero headlines only)
H1        — 40–48px / weight 700     / line-height 1.15                          (page titles)
H2        — 30–36px / weight 600–700 / line-height 1.2                          (section titles)
H3        — 22–24px / weight 600     / line-height 1.3                          (card titles, subsections)
Body Lg   — 18px    / weight 400–500 / line-height 1.6                          (intro paragraphs, lede)
Body      — 16px    / weight 400     / line-height 1.6–1.7                      (default text)
Small     — 14px    / weight 400–500 / line-height 1.5                          (captions, metadata, labels)
Micro     — 12px    / weight 500–600 / letter-spacing 0.05em / uppercase        (eyebrows, badges)
```

**Rules:**
- Headlines get **negative letter-spacing** (`-0.01em` to `-0.02em`) at large sizes — tight tracking is what separates premium from default browser typography.
- Body text gets **generous line-height** (1.6–1.75), never below 1.5 — cramped paragraphs look cheap.
- Never center-align paragraphs longer than one line. Left-align body copy; center only short headlines/eyebrows.
- Use font-weight for hierarchy before reaching for size — a 600-weight label at the same size as body text still reads as distinct.
- Pair a strong sans-serif (system stack, or a licensed grotesk) at 2–3 weights max (e.g. 400, 600, 700). Avoid using 5+ weights of one family — it looks indecisive.
- Eyebrows/kickers above headlines: uppercase, letter-spaced, small, in the accent color — signals "designed", not "typed".

## 3. Premium Color System

Never ship a UI with only "primary blue + gray" — that reads as a template default. Build a real system:

```
Neutral scale (9–11 steps)  — for text, borders, backgrounds. Should NOT be pure gray;
                               tint it 2–5% toward your brand hue (e.g. cool navy-gray, not #808080).
Brand primary (5–7 steps)   — the core identity color, with a light tint for backgrounds/badges
                               and a dark shade for hover/active states.
Accent (1 color, sparingly) — reserved for CTAs, key highlights, and nothing else. If everything
                               is highlighted, nothing is.
Semantic colors             — success, warning, error, info — each with a background tint and a
                               solid text/icon variant. Never reuse brand color for semantic meaning.
```

**Rules:**
- Body text is never pure black (`#000`) — use a dark neutral like `#101828` or `#1A2A3A`.
- Backgrounds are never pure white next to pure white cards with no distinction — use a subtle off-white (`#F8FAFC` / `#F5F7FA`) for page background against `#FFFFFF` cards, separated by a hairline border or soft shadow.
- Borders use a light neutral (`#E2E8F0` range), not the same gray as disabled text.
- Limit yourself to one accent color for interactive/CTA elements. A page using 4+ unrelated bright colors reads as unpolished.
- Gradients, if used, must be subtle (same-hue, low-contrast, e.g. navy-900 → navy-800) — avoid the purple→pink→blue "AI startup" gradient unless the brand explicitly calls for vibrancy.

## 4. Visual Hierarchy

Every screen needs one unambiguous focal point per viewport of scroll.

- **Size, weight, color, and whitespace** — in that order of effectiveness — are the tools for hierarchy. Reach for whitespace before reaching for a new color.
- The primary CTA on any section should be visually singular — one solid/filled button; secondary actions are outline or ghost/text style, never competing in visual weight.
- Group related elements with proximity (tighter gap within a group, larger gap between groups) rather than borders/dividers as the primary organizing tool.
- Numbers, stats, and key data points get their own visual treatment (larger size, tabular numerals, distinct weight) — they should not just be inline body text.

## 5. Enterprise SaaS Aesthetics

Target the visual language of Stripe, Linear, Vercel, Ramp — not generic Bootstrap or template marketplaces:

- **Restraint over decoration.** Fewer, better-considered elements beat many mediocre ones.
- **Real content over lorem-ipsum patterns.** Specs, numbers, standards, certifications — concrete facts read as trustworthy; vague adjective-only copy reads as filler.
- **Consistent iconography.** One icon set (outline or filled, not mixed), one consistent stroke width, sized consistently (usually 20px or 24px), always paired with adequate padding — never a raw SVG jammed against text.
- **Soft elevation, not heavy drop shadows.** Prefer `0 1px 2px rgba(16,24,40,0.06), 0 1px 3px rgba(16,24,40,0.1)` style layered soft shadows over a single heavy `box-shadow: 0 10px 40px black`.
- **Subtle borders + soft shadow combined** on cards, not shadow alone — this is what makes flat design feel "designed" instead of "default browser div".

## 6. Avoiding the "AI-Generated" Look

Concrete tells to eliminate:

| AI-generated tell | Premium fix |
|---|---|
| Centered hero, giant rounded gradient blob background | Asymmetric layout, real product imagery or concrete data visualization |
| Purple-to-blue or pink-to-orange gradient everywhere | One restrained brand gradient (same-hue) used once, sparingly, or none |
| Emoji as icons (🚀 ✨ 💡) | A real icon library (Lucide, Phosphor, Heroicons) at consistent weight |
| Three feature cards with generic icon + 1-sentence fluff ("Fast. Reliable. Secure.") | Specific, factual claims with numbers, standards, or named capabilities |
| Overuse of rounded-full pill buttons everywhere | Consistent, moderate corner radius (6–10px) used deliberately, pill shape reserved for tags/badges |
| Testimonials with stock headshots and no company/role verification | Real logos, named contacts, or omit the section entirely rather than fake it |
| Default Tailwind blue-600 as the only color decision made | A considered, named color system (see §3) |
| Excessive glassmorphism/blur on every card | Glassmorphism used only where it earns its place (see §9) |

## 7. Premium Card Layouts

```html
<div style="
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 1px 2px rgba(16,24,40,0.04), 0 1px 3px rgba(16,24,40,0.06);
  transition: box-shadow 200ms ease, transform 200ms ease;
">
  <!-- eyebrow/badge -->
  <span style="font-size:12px; font-weight:600; letter-spacing:0.05em; text-transform:uppercase; color:#C9A84C;">Category</span>
  <!-- title -->
  <h3 style="font-size:22px; font-weight:600; color:#101828; margin:8px 0 8px;">Card Title</h3>
  <!-- body -->
  <p style="font-size:15px; line-height:1.65; color:#475467;">Concrete, specific supporting copy — not filler.</p>
</div>
```

Hover state (desktop only): lift 2–4px, deepen shadow slightly, never scale the whole card past `1.02` (larger scale looks cheap/bouncy).

**Card checklist:**
- Consistent internal padding across all cards in a grid (never let content dictate padding per-card)
- Equal height within a row (`align-items: stretch` in the grid/flex parent)
- One clear visual anchor per card (icon, number, or image) — not zero, not three competing ones
- Border + soft shadow together, not shadow-only (shadow-only can look like it's floating awkwardly on light backgrounds)

## 8. Grid Systems

- Use a **12-column grid** conceptually even in CSS Grid/Flexbox implementations — content spans should feel proportionate (e.g. 8/12 + 4/12, not arbitrary 63%/37%).
- Card grids: `repeat(auto-fit, minmax(280px, 1fr))` or explicit breakpoint-based column counts (1 col mobile → 2 col tablet → 3–4 col desktop). Never let a 3-column grid collapse to 2 orphaned + 1 stranded card — use `auto-fit`/`auto-fill` or adjust the count.
- Consistent gutter (usually `24px` or `32px`) between grid items, matching the 8px system.
- Max content width: cap body/reading content at `680–760px`; cap full page containers at `1200–1440px` with auto side margins — full-bleed edge-to-edge text on large monitors reads as unfinished.

## 9. Glassmorphism — Only When Appropriate

Glassmorphism (translucent, blurred background) is a **strong, era-specific effect**. Use it deliberately, not by default:

**Appropriate:**
- A sticky/fixed navbar over scrolling content (`backdrop-filter: blur(12px)` + `background: rgba(255,255,255,0.8)`)
- A modal/overlay scrim
- A floating badge/pill over a photo or gradient background where legibility needs a boost

**Inappropriate:**
- Every card on the page
- Body text containers over a solid background (adds nothing, just softens contrast)
- As a substitute for an actual color/elevation system

```css
.glass-nav {
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(12px) saturate(180%);
  -webkit-backdrop-filter: blur(12px) saturate(180%);
  border-bottom: 1px solid rgba(226, 232, 240, 0.8);
}
```

## 10. Responsive Design

- Design mobile-first for content order and priority, even if desktop is the primary target for a B2B audience — many buyers first click through from a mobile email or WhatsApp link.
- Breakpoints: `640px` (mobile→tablet), `1024px` (tablet→desktop), `1280px`/`1440px` (desktop→wide). Don't invent one-off breakpoints per component.
- Typography scales down at least one step between desktop and mobile for Display/H1 (e.g. 64px → 36px), not just via `clamp()` alone without checking actual rendering at 375px width.
- Touch targets minimum `44×44px` on any interactive element for mobile.
- Never let a data/spec table overflow the viewport uncontained — wrap in `overflow-x: auto` with a visible scroll affordance.

## 11. Micro-interactions

Small, purposeful motion that confirms an action or draws the eye — never decoration for its own sake. See [[framer-motion]] for animation implementation details.

- **Buttons:** background/border color shift + subtle shadow increase on hover, `150–200ms ease`; a slight `translateY(-1px)` on hover, back to `0` on active/click for tactile feedback.
- **Links:** underline grows from `0%` to `100%` width on hover (`transition: width 200ms`) rather than an abrupt show/hide, or a color shift with `150ms ease`.
- **Cards:** shadow/elevation change + `2–4px` lift on hover, never on tap-only mobile (avoid sticky hover states on touch).
- **Form fields:** border color transitions to the brand/focus color over `150ms`, paired with a focus ring (see [[accessibility]] for required contrast).
- **Page load:** content should never "pop" in unstyled — pair with a subtle fade/slide-up on first paint for hero content only, not every element (see [[framer-motion]] stagger patterns).
- Respect `prefers-reduced-motion: reduce` — disable non-essential transitions/animations for users who request it.

---

## Quick Review Checklist

Before considering any UI work "done," verify:

- [ ] All spacing multiples of 8px (or 4px)
- [ ] No more than 6 font sizes, headlines have negative letter-spacing
- [ ] Color system has neutral scale, brand scale, one accent, semantic colors — not just "blue + gray"
- [ ] One clear focal point per section
- [ ] No emoji-as-icon, no default gradient blobs, no fake testimonials
- [ ] Cards have consistent padding, border + soft shadow, equal height in a row
- [ ] Grid gutters match the spacing scale, max content width is capped
- [ ] Glassmorphism used in ≤2 deliberate places, not everywhere
- [ ] Mobile breakpoints tested at 375px, touch targets ≥44px
- [ ] Hover/focus states exist on every interactive element with smooth transitions
