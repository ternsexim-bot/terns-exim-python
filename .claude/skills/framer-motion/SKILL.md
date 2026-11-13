---
name: framer-motion
description: Implement scroll reveals, stagger animations, hover effects, page transitions, and loading states with Framer Motion (motion/react), tuned for performance and restraint. Use when adding or reviewing any animation in a React/Next.js codebase.
---

# Framer Motion

## Purpose

Provide production-ready, performant animation patterns using Framer Motion (package `framer-motion`, or its newer alias `motion/react`). Animation should reinforce hierarchy and feel — see [[premium-ui]] — never distract from content or tank performance. Default to subtlety: if a reviewer notices the animation before the content, it's too much.

Applies to React / Next.js work (e.g. `crm-frontend/` or any future React-based surface in this repo). The current Flask marketing site uses vanilla CSS/JS (`static/js/main.js`, `IntersectionObserver`) — mirror these same principles there using CSS transitions/`IntersectionObserver` rather than importing Framer Motion into a non-React page.

---

## 1. Setup

```bash
npm install framer-motion
```

```tsx
import { motion, useReducedMotion } from "framer-motion";
```

Always respect reduced-motion preference:

```tsx
const shouldReduceMotion = useReducedMotion();

<motion.div
  initial={{ opacity: 0, y: shouldReduceMotion ? 0 : 24 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: shouldReduceMotion ? 0 : 0.5 }}
/>
```

## 2. Scroll Reveal Animations

Use `whileInView` with `viewport={{ once: true }}` — animations should play once, not re-trigger every time a user scrolls up and down (that reads as glitchy, not premium).

```tsx
const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: [0.21, 0.47, 0.32, 0.98] },
  },
};

function RevealSection({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.2 }}
      variants={fadeUp}
    >
      {children}
    </motion.div>
  );
}
```

**Rules:**
- `viewport={{ once: true }}` — always, for scroll reveals. Re-animating on every scroll direction change is the #1 "amateur animation" tell.
- `amount: 0.2` (element 20% visible) triggers earlier and feels more responsive than waiting for full visibility.
- Vertical offset (`y`) of `16–32px` is enough — don't fly elements in from `100px+` away, it delays perceived load time.
- Keep duration `0.4–0.6s` for reveals. Longer starts to feel sluggish on repeat visits.

## 3. Stagger Animations

For lists, grids, or card groups — children should cascade in, not pop simultaneously.

```tsx
const container = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.08, delayChildren: 0.1 },
  },
};

const item = {
  hidden: { opacity: 0, y: 16 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4, ease: "easeOut" } },
};

function CardGrid({ items }: { items: Item[] }) {
  return (
    <motion.div
      className="grid grid-cols-1 md:grid-cols-3 gap-6"
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.15 }}
      variants={container}
    >
      {items.map((it) => (
        <motion.div key={it.id} variants={item}>
          <Card {...it} />
        </motion.div>
      ))}
    </motion.div>
  );
}
```

**Rules:**
- `staggerChildren` between `0.05–0.1s`. Above `0.15s` per item, a 6+ item grid takes visibly too long to finish.
- Cap total stagger animation time — for long lists (10+), stagger only the first 6–8 visible items, or reduce `staggerChildren` further so the whole group settles within ~1s.
- Never stagger on every re-render — the parent `variants`/`initial`/`whileInView` combo above only fires once per mount thanks to `viewport once: true`.

## 4. Hover Effects

Keep hover animation cheap (`transform`/`opacity` only — never animate `width`, `height`, `top`/`left`, or `box-shadow` blur radius directly, all of which force layout/paint).

```tsx
<motion.div
  whileHover={{ y: -4 }}
  whileTap={{ y: 0 }}
  transition={{ duration: 0.2, ease: "easeOut" }}
  className="rounded-xl border bg-white p-8 shadow-sm"
>
  <CardContent />
</motion.div>
```

For a shadow-deepen-on-hover effect, animate a layered box-shadow via CSS transition (cheaper than via Framer Motion's style interpolation) rather than motion:

```css
.card { transition: box-shadow 200ms ease, transform 200ms ease; }
.card:hover { box-shadow: 0 8px 24px rgba(16,24,40,0.12); }
```

**Button micro-interaction pattern:**

```tsx
<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
  transition={{ duration: 0.15 }}
  className="rounded-lg bg-brand-900 px-6 py-3 text-white"
>
  Request a Quote
</motion.button>
```

Keep hover `scale` at `1.01–1.03` max — anything larger reads as bouncy/cheap, not premium.

## 5. Page Transitions (App Router)

In Next.js App Router, wrap route segments with `AnimatePresence` at a layout boundary, keyed by pathname:

```tsx
// app/template.tsx  (template.tsx re-mounts on every navigation, unlike layout.tsx)
"use client";
import { motion } from "framer-motion";

export default function Template({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}
```

For exit animations across routes, use `AnimatePresence` with `mode="wait"` in a client-side layout wrapper keyed by `usePathname()`. Use sparingly — full-page exit/enter transitions add latency to perceived navigation speed; a simple fade-in on enter (as above) is usually enough for a content-heavy B2B site.

## 6. Loading Animations

Prefer skeleton screens over spinners for content that has a predictable shape (cards, tables, lists) — skeletons reduce perceived wait time.

```tsx
function Skeleton({ className }: { className?: string }) {
  return (
    <motion.div
      className={`rounded-md bg-slate-200 ${className}`}
      animate={{ opacity: [0.5, 1, 0.5] }}
      transition={{ duration: 1.4, repeat: Infinity, ease: "easeInOut" }}
    />
  );
}
```

Spinner (use only for indeterminate short waits, e.g. form submit):

```tsx
<motion.div
  className="h-5 w-5 rounded-full border-2 border-white/30 border-t-white"
  animate={{ rotate: 360 }}
  transition={{ duration: 0.7, repeat: Infinity, ease: "linear" }}
/>
```

**Rules:**
- Never block the entire UI with a full-page spinner if only a section is loading — scope loading states to the component.
- Button loading states: swap label for spinner in place, keep button width fixed (`min-width`) so it doesn't jump.

## 7. Motion Variants — Organize, Don't Repeat

Centralize shared variants rather than redefining `{ opacity: 0, y: 24 }` inline across every component:

```tsx
// lib/motion.ts
export const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: "easeOut" } },
};

export const fadeIn = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.4 } },
};

export const staggerContainer = (stagger = 0.08, delay = 0.1) => ({
  hidden: {},
  visible: { transition: { staggerChildren: stagger, delayChildren: delay } },
});

export const scaleIn = {
  hidden: { opacity: 0, scale: 0.96 },
  visible: { opacity: 1, scale: 1, transition: { duration: 0.35, ease: "easeOut" } },
};
```

Import and reuse across the app — this also makes a future "reduce all motion" or "retune all easing" change a one-file edit.

## 8. Performance Best Practices

- **Animate only `transform` and `opacity`.** These run on the compositor thread and don't trigger layout/paint. Avoid animating `width`, `height`, `top`, `left`, `margin`, `box-shadow` spread/blur directly.
- **Use `will-change` sparingly**, only on elements actively mid-animation, and remove it after — Framer Motion handles this automatically for transform/opacity in most cases, so manual `will-change` is rarely needed.
- **`viewport={{ once: true }}`** on all scroll reveals — prevents animation logic from re-running on every scroll event/re-entry.
- **Lazy-load `framer-motion` where it's heavy** — for a marketing page with many animated sections, ensure the library is part of a client component bundle, not pulled into server-rendered critical-path code. In Next.js App Router, isolate motion usage inside small `"use client"` leaf components rather than marking large layout trees client-side.
- **Avoid animating on mount for above-the-fold hero content when it delays LCP.** If the hero headline is the Largest Contentful Paint element, keep its entrance animation short (`≤0.4s`) or skip animating it (fade only, no transform) so it doesn't delay the LCP timing recorded by Lighthouse — see [[performance]].
- **Debounce/limit `useScroll`-driven animations** (parallax, scroll-linked progress bars) — these run on every scroll frame; keep the driven properties to `transform`/`opacity` and avoid attaching scroll listeners to more than a couple of elements per page.
- **Test with CPU throttling** (Chrome DevTools 4x/6x slowdown) — stagger and scroll-reveal animations that feel smooth on a dev machine can visibly stutter on the throttled mobile CPUs your Lighthouse score is measured against.
- **Never animate layout-shifting properties on load** — this directly causes Cumulative Layout Shift penalties. Reserve space (fixed dimensions/aspect-ratio) before content animates in.

---

## Quick Review Checklist

- [ ] All scroll reveals use `viewport={{ once: true }}`
- [ ] Only `transform`/`opacity` are animated (no width/height/top/left/shadow-blur)
- [ ] Stagger delay ≤0.1s per item; long lists cap the staggered subset
- [ ] Hover scale stays within 1.01–1.03
- [ ] Shared variants live in one file, not duplicated per component
- [ ] `useReducedMotion` respected for essential-only motion
- [ ] Hero/LCP element animation is short or transform-free
- [ ] Loading states use skeletons for predictable shapes, spinners only for short indeterminate waits
