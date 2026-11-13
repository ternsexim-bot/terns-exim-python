---
name: accessibility
description: Enforce WCAG AA compliance — keyboard navigation, semantic HTML, ARIA labels, color contrast, and visible focus states. Use whenever creating or reviewing any UI, form, or interactive component.
---

# Accessibility (WCAG AA)

## Purpose

Every page and component must be usable by keyboard-only and screen-reader users, and meet WCAG 2.1 **AA** at minimum. This is not optional polish — for a B2B export site, procurement staff, compliance reviewers, and enterprise buyers may use assistive tech, and inaccessible forms directly cost leads (see the lead form in `templates/_lead_form.html`, which must remain fully keyboard/screen-reader operable).

---

## 1. Semantic HTML First

Use the element that already has the right behavior and semantics built in before reaching for ARIA or a `<div>`.

```html
<!-- Bad -->
<div class="button" onclick="submit()">Submit</div>
<div class="heading">Our Products</div>

<!-- Good -->
<button type="submit">Submit</button>
<h2>Our Products</h2>
```

**Rules:**
- One `<h1>` per page. Headings (`h1`–`h6`) must nest in order — never skip from `h2` to `h4` to "make it look smaller" (style with CSS, not by choosing the wrong heading level).
- Use `<nav>`, `<main>`, `<header>`, `<footer>`, `<section>`, `<article>`, `<button>`, `<a>` for their actual purpose — a screen reader user navigates by landmark region and heading outline before reading linearly.
- `<a href>` for navigation (goes somewhere / changes URL); `<button>` for actions (submits, toggles, opens). Never `<a href="#">` with a JS `onclick` as a substitute for a button — it breaks keyboard activation semantics (Space vs Enter) and screen reader "link" vs "button" announcement. Note: `templates/base.html`'s modal triggers use `href="#" onclick="..."` — prefer converting these to `<button>` elements when touched.
- Forms use `<label for="id">` explicitly associated with each `<input id="id">` — never rely on placeholder text as a label substitute (it disappears on input and fails for screen readers).
- Use `<table>` with `<th scope="col">`/`<th scope="row">` for real tabular data (like the spec/comparison tables in product pages) — never a `<div>` grid styled to look like a table.

## 2. Keyboard Navigation

Every interactive element must be reachable and operable via keyboard alone — Tab, Shift+Tab, Enter, Space, Escape, and arrow keys where applicable.

- **Tab order** follows visual/logical reading order. Never use positive `tabindex` values (`tabindex="3"`) to force an order — fix the DOM order instead. `tabindex="0"` (adds to natural order) and `tabindex="-1"` (programmatically focusable, removed from tab order — used for modal containers) are the only acceptable values.
- **Custom interactive components** (modal, dropdown, accordion, tabs, custom-styled `<div>`-based button) need explicit keyboard handling:

```js
// Accordion/FAQ item — must respond to Enter and Space, not just click
faqButton.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " ") {
    e.preventDefault();
    toggleFaq(faqButton);
  }
});
```

- **Modals** (e.g. the enquiry popup in `base.html`) must:
  - Move focus into the modal on open (usually the first input or heading)
  - Trap focus within the modal while open (Tab cycles inside, doesn't escape to page content behind it)
  - Close on `Escape`
  - Return focus to the triggering element on close
- **No keyboard traps** — a user must always be able to Tab out of any widget unless it's an intentional, documented modal focus trap with an Escape exit.
- Test manually: unplug the mouse, navigate the entire page/flow (including submitting the lead form) with keyboard only.

## 3. ARIA — Use Sparingly, Correctly

The first rule of ARIA is: don't use ARIA if a native HTML element already provides the semantics. Reach for ARIA only to fill gaps native HTML can't cover.

```html
<!-- Icon-only button needs an accessible name -->
<button aria-label="Close menu" onclick="closeMenu()">
  <svg aria-hidden="true">...</svg>
</button>

<!-- Modal -->
<div role="dialog" aria-modal="true" aria-labelledby="enquiry-modal-title">
  <h2 id="enquiry-modal-title">Request a Quote</h2>
  ...
</div>

<!-- Live region for async form feedback -->
<div role="status" aria-live="polite" id="form-status"></div>
```

**Rules:**
- Decorative images/icons: `alt=""` or `aria-hidden="true"` — don't force a screen reader to announce "decorative gear icon" on every button.
- Meaningful images: descriptive `alt` text stating content/function, not "image of..." (redundant — screen readers already announce it's an image).
- Icon-only buttons/links always get `aria-label` (or visually-hidden text) — an icon alone announces nothing useful.
- Form validation errors: associate the error message with its field via `aria-describedby`, and set `aria-invalid="true"` on the field while invalid.
- Never set `aria-hidden="true"` on an element that contains focusable content — that creates elements a keyboard user can tab to but a screen reader user can't perceive.
- Don't add redundant roles to elements that already have them natively (`<button role="button">` is noise).

## 4. Color Contrast

Minimum ratios for WCAG AA:

```
Normal text (<18px, or <14px bold)   — 4.5:1 against its background
Large text (≥18px, or ≥14px bold)     — 3:1
UI components / graphical objects     — 3:1 (borders of inputs, icon-only buttons, focus indicators)
```

**Rules:**
- Check every text/background pairing, including placeholder text, disabled states (disabled text is exempt from AA but should still be reasonably legible), and text over images (add a scrim/overlay if needed).
- Don't rely on color alone to convey meaning — a red border on an invalid field must be paired with an icon and/or text message, since colorblind users (~4-8% of men) can't distinguish it otherwise.
- Verify brand accent colors against both their typical backgrounds — e.g. the gold accent (`#C9A84C`) used in this codebase's product-page answer blocks (see [[terns-exim]] for the palette) must be checked against white/light-gray backgrounds, not assumed compliant because it "looks fine."
- Use a real contrast checker (Chrome DevTools color picker shows the ratio live, or WebAIM's contrast checker) — don't eyeball it.

## 5. Focus States

Every interactive element needs a clearly visible focus indicator — never remove `outline` without providing an equal or better replacement.

```css
/* Bad — silently removes all keyboard focus visibility */
:focus { outline: none; }

/* Good — custom, high-contrast focus ring, shown only for keyboard nav */
:focus-visible {
  outline: 2px solid #2E4763;
  outline-offset: 2px;
}

/* Or a ring-style focus indicator */
button:focus-visible {
  box-shadow: 0 0 0 2px #fff, 0 0 0 4px #2E4763;
}
```

**Rules:**
- Use `:focus-visible` (not bare `:focus`) so the ring shows for keyboard users but doesn't create visual noise on mouse click, while still meeting the requirement that keyboard focus is always visible.
- The focus indicator itself needs ≥3:1 contrast against the adjacent background (per WCAG 2.4.11), and should be visible against both the element and page background — an outline the same color as the button background is functionally invisible.
- Focus order must be logical and match visual layout — verify after any CSS reordering (flexbox `order`, CSS Grid placement) since visual order can diverge from DOM/tab order.
- Skip link: provide a "Skip to main content" link as the very first focusable element on the page, visually hidden until focused, so keyboard users don't have to tab through the entire nav on every page.

```html
<a href="#main-content" class="skip-link">Skip to main content</a>
...
<main id="main-content">
```

```css
.skip-link {
  position: absolute; left: -9999px; top: 0;
  background: #fff; padding: 12px 20px; z-index: 100;
}
.skip-link:focus { left: 16px; top: 16px; }
```

---

## Quick Review Checklist

- [ ] One `<h1>`, headings nest without skipping levels
- [ ] All interactive elements are real `<button>`/`<a href>`, not `<div onclick>`
- [ ] Every form input has an explicit associated `<label>`
- [ ] Full flow (including forms/modals) operable by keyboard alone, no traps
- [ ] Modals: focus moves in on open, traps while open, Escape closes, focus returns on close
- [ ] Icon-only controls have `aria-label`; decorative icons are `aria-hidden`
- [ ] Text contrast ≥4.5:1 (normal) / 3:1 (large); UI component contrast ≥3:1
- [ ] Color is never the only signal for state/validity
- [ ] `:focus-visible` styles present and sufficiently contrasted on every interactive element
- [ ] Skip-to-content link present on every page
