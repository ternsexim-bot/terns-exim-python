---
name: tailwind
description: Define design tokens, utility conventions, component consistency, responsive breakpoints, and dark mode support for Tailwind CSS projects. Use when styling any component or reviewing Tailwind usage for consistency.
---

# Tailwind CSS

## Purpose

Keep Tailwind usage systematic rather than ad hoc — every class should trace back to a defined design token (see [[premium-ui]] for the underlying spacing/color/type system this codifies). This repo's current marketing site uses hand-written CSS (`static/css/style.css`), not Tailwind — apply this skill to any React/Next.js surface (e.g. a rebuilt `crm-frontend/`, or a future Next.js site) that adopts Tailwind.

---

## 1. Design Tokens (`tailwind.config.ts`)

Never rely on Tailwind's raw default palette (`blue-600`, `gray-500`) directly in components for brand-relevant color — define semantic tokens once, use them everywhere.

```ts
// tailwind.config.ts
import type { Config } from "tailwindcss";

export default {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#EEF2F7", 100: "#D9E2EC", 200: "#BCCCDC", 300: "#9FB3C8",
          400: "#748AA6", 500: "#4A6483", 600: "#2E4763", // primary navy
          700: "#1A2A3A", 800: "#101B28", 900: "#0A121C",
        },
        accent: {
          400: "#D9BE73", 500: "#C9A84C", 600: "#A8863A", // gold
        },
        success: { 50: "#ECFDF3", 500: "#12B76A", 700: "#027A48" },
        warning: { 50: "#FFFAEB", 500: "#F79009", 700: "#B54708" },
        danger:  { 50: "#FEF3F2", 500: "#F04438", 700: "#B42318" },
      },
      fontFamily: {
        sans: ["var(--font-body)", "system-ui", "sans-serif"],
        display: ["var(--font-display)", "system-ui", "sans-serif"],
      },
      fontSize: {
        display: ["4rem", { lineHeight: "1.05", letterSpacing: "-0.02em", fontWeight: "700" }],
        h1: ["2.75rem", { lineHeight: "1.15", letterSpacing: "-0.01em", fontWeight: "700" }],
        h2: ["2rem", { lineHeight: "1.2", fontWeight: "600" }],
        h3: ["1.375rem", { lineHeight: "1.3", fontWeight: "600" }],
      },
      spacing: { 18: "4.5rem", 22: "5.5rem" }, // only add if a real recurring need exists
      borderRadius: { xl: "12px", "2xl": "16px" },
      boxShadow: {
        card: "0 1px 2px rgba(16,24,40,0.04), 0 1px 3px rgba(16,24,40,0.06)",
        "card-hover": "0 4px 12px rgba(16,24,40,0.10), 0 2px 4px rgba(16,24,40,0.06)",
      },
    },
  },
  darkMode: "class",
} satisfies Config;
```

**Rules:**
- Every brand color used in a component comes from `brand-*` / `accent-*` / semantic tokens — never a raw Tailwind default (`blue-600`, `indigo-500`) for brand-meaningful UI.
- Don't extend the spacing scale casually — Tailwind's default scale is already 4px-based (matches the 8px system in [[premium-ui]] on even steps). Only add custom spacing values for a genuine recurring gap the default scale doesn't cover.
- Centralize shadows, radii, and type scale as tokens so a brand refresh is a one-file change, not a codebase-wide find/replace.

## 2. Utility Conventions

- **Order classes consistently**: layout → box model → typography → color/visual → state/responsive. Use Prettier's `prettier-plugin-tailwindcss` to auto-sort — don't hand-order or bikeshed this.
- **Extract repeated utility strings into components, not `@apply`.** `@apply` reintroduces a CSS layer to maintain and defeats Tailwind's co-location benefit. If the same 8-class string appears 3+ times, make it a component (`<Card>`, `<Button variant="primary">`), not a new CSS class.
- **Use `cn()`/`clsx` + `tailwind-merge`** for conditional classes so conflicting utilities resolve correctly:

```ts
// lib/utils.ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

```tsx
<button className={cn(
  "rounded-lg px-6 py-3 font-semibold transition-colors",
  variant === "primary" && "bg-brand-700 text-white hover:bg-brand-800",
  variant === "outline" && "border border-brand-700 text-brand-700 hover:bg-brand-50",
  disabled && "opacity-50 pointer-events-none",
)}>
```

- **Never use arbitrary values as a first resort** (`p-[13px]`, `text-[15.5px]`) — check the token scale first; only reach for `[]` arbitrary syntax for a genuinely one-off value (e.g. matching an exact background image position).

## 3. Component Consistency

Build a small set of primitive components in `components/ui/` and never restyle the same element type differently across pages:

```tsx
// components/ui/Button.tsx
import { cn } from "@/lib/utils";
import { type ButtonHTMLAttributes } from "react";

const variants = {
  primary: "bg-brand-700 text-white hover:bg-brand-800 shadow-card",
  outline: "border border-brand-300 text-brand-700 hover:bg-brand-50",
  ghost: "text-brand-700 hover:bg-brand-50",
};

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: keyof typeof variants;
}

export function Button({ variant = "primary", className, ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center rounded-lg px-6 py-3 text-sm font-semibold transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent-500 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none",
        variants[variant],
        className,
      )}
      {...props}
    />
  );
}
```

Every button, card, input, and badge in the app renders through these primitives — a designer reviewing the live site should never spot two visually different "primary button" treatments.

## 4. Responsive Breakpoints

Use Tailwind defaults; don't invent custom breakpoints unless there's a proven real-world need:

```
sm   640px   — large phone / small tablet portrait
md   768px   — tablet portrait
lg   1024px  — tablet landscape / small desktop
xl   1280px  — desktop
2xl  1536px  — wide desktop
```

**Rules:**
- Design mobile-first: unprefixed classes are the mobile/base styles, add `md:`/`lg:` to layer up — never write desktop-first then override down with `max-md:`.
- Cap page/content container width with a token, not per-page guessing: `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8` as the standard page shell.
- Grids: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3` progressive pattern — verify no orphaned single card in the last row at each breakpoint (see [[premium-ui]] §8).
- Test real content at `375px` (small phone), not just resizing a desktop browser — text wrapping and touch target sizing often break only at true mobile widths.

## 5. Dark Mode Support

Use `darkMode: "class"` (not `media`) so dark mode can be a user-controlled toggle rather than only following OS preference, and pair every token with a `dark:` variant at the point of use — never hardcode a light-only color and forget dark mode entirely.

```tsx
<div className="bg-white text-brand-900 dark:bg-brand-900 dark:text-brand-50 border border-slate-200 dark:border-brand-700">
  <h2 className="text-h2 dark:text-white">Section Title</h2>
  <p className="text-slate-600 dark:text-slate-300">Body copy.</p>
</div>
```

**Rules:**
- Every background/text/border color pairing needs a `dark:` counterpart — audit new components against both modes before shipping, not after.
- Don't just invert to pure black — use the same tinted neutral scale (see [[premium-ui]] §3) at dark end values (e.g. `brand-900`/`brand-800`) so dark mode still feels like the same brand, not a generic inverted theme.
- Images/logos: provide a light/dark variant or an SVG that adapts via `currentColor` where the logo needs to remain legible on both backgrounds.
- Verify contrast ratios independently in dark mode — a pairing that passes WCAG AA in light mode does not automatically pass in dark (see [[accessibility]]).
- Persist the user's toggle choice (e.g. `localStorage` + a script in `<head>` to avoid a flash of wrong theme on load).

---

## Quick Review Checklist

- [ ] All brand colors come from defined tokens, not raw Tailwind defaults
- [ ] No repeated 5+ class utility strings — extracted into a component instead
- [ ] `cn()`/`tailwind-merge` used for conditional/overridable class logic
- [ ] No arbitrary `[]` values where a token already covers the case
- [ ] Buttons/cards/inputs/badges all render through shared primitives
- [ ] Mobile-first class ordering (base → `sm:` → `md:` → `lg:`)
- [ ] Every color pairing has a working `dark:` variant, checked for contrast
- [ ] No orphaned grid items at any breakpoint
