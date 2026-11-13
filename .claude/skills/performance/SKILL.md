---
name: performance
description: Enforce Lighthouse scores above 95 through lazy loading, dynamic imports, code splitting, image optimization, font optimization, and minimal JavaScript bundles. Use when adding assets, dependencies, or reviewing page load performance.
---

# Performance

## Purpose

Every page should score **95+ across Performance, Accessibility, Best Practices, and SEO** in Lighthouse. For a B2B export site where buyers may be on slower connections or mobile in regions with variable network quality, load speed directly affects lead conversion and Core Web Vitals-driven SEO ranking (see [[seo]]).

---

## 1. Core Web Vitals Targets

```
LCP (Largest Contentful Paint)   ≤ 2.5s   — hero image/headline must render fast
INP (Interaction to Next Paint)  ≤ 200ms  — form/button responsiveness
CLS (Cumulative Layout Shift)    ≤ 0.1    — no content jumping as page loads
TTFB (Time to First Byte)        ≤ 0.8s   — server response speed
```

Run Lighthouse (Chrome DevTools → Lighthouse tab, or `npx lighthouse <url> --view`) on every significant page change, on **mobile** simulated throttling (the default and stricter profile), not just desktop.

## 2. Image Optimization

Images are almost always the largest contributor to page weight — audit them first.

- **Serve modern formats**: WebP or AVIF instead of JPEG/PNG where supported; in Next.js, `next/image` handles this automatically (see [[nextjs]]). For the current Flask site's static images, pre-convert source assets to WebP with a JPEG fallback via `<picture>` if broad compatibility is needed.
- **Size images for their actual display size** — never ship a 3000px-wide source image into a 400px card slot. Generate/export at the largest size actually needed (accounting for 2x retina displays), not larger.
- **Lazy-load below-the-fold images**: `loading="lazy"` on every `<img>` except the LCP candidate (usually the hero image), which should instead be prioritized (`fetchpriority="high"` or `next/image`'s `priority` prop).
- **Always set explicit `width`/`height`** (or `aspect-ratio` in CSS) on every image so the browser reserves layout space before the image loads — this is the single biggest fix for CLS.
- **Compress everything** — run images through a compressor (Squoosh, `sharp`, ImageOptim) targeting visually-lossless compression; a favicon or logo PNG should be a few KB, not hundreds.

```html
<img
  src="/images/products/hexbolt.webp"
  alt="Stainless steel hex bolts, DIN 933"
  width="800" height="600"
  loading="lazy"
  decoding="async"
/>
```

## 3. Font Optimization

- Self-host fonts (via `next/font`, see [[nextjs]], or a local `@font-face` with `font-display: swap`) — never load from a third-party CDN at request time, which adds an extra DNS lookup + connection + render-blocking delay.
- Load only the weights/styles actually used in the design (see [[premium-ui]] §2 — 2–3 weights max per family).
- `font-display: swap` (or `optional` for non-critical decorative fonts) prevents invisible text while the font loads (FOIT).
- Subset fonts to the character sets actually needed (e.g. Latin only) if using a self-hosted `@font-face` pipeline, to cut file size.
- Preload the primary body/heading font if it's not inlined via `next/font`:

```html
<link rel="preload" href="/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
```

## 4. Minimal JavaScript Bundle

- **Audit dependencies before adding them.** Check bundle-size impact (bundlephobia.com or `npx cost-of-modules`) before installing a library for a small utility — don't pull in a 40KB date library for one format call when a native `Intl.DateTimeFormat` call does the job.
- **Ship less JS to the client by default.** In React/Next.js, default to Server Components (see [[nextjs]]) — anything not marked `"use client"` never reaches the browser bundle.
- **Tree-shake and avoid barrel imports** that defeat it — `import { Button } from "@/components/ui"` re-exporting everything can pull in far more than needed if the bundler can't tree-shake the barrel; prefer direct imports (`import { Button } from "@/components/ui/button"`) for large shared libraries.
- **Remove unused code and dependencies** — periodically run `depcheck` or equivalent; dead imports still bloat the bundle in some build configurations.
- **Avoid heavy polyfills** — set a realistic `browserslist`/target rather than defaulting to maximum legacy compatibility no B2B buyer's browser actually needs.
- **Minify and compress** — ensure the production build serves gzip or brotli-compressed assets (`Content-Encoding: br`/`gzip`); most hosts (Render, Vercel, Netlify) do this automatically, but verify via response headers.

## 5. Lazy Loading & Dynamic Imports

Defer anything not needed for the initial viewport/interaction.

```tsx
// Next.js — dynamic import for a heavy, below-the-fold, or rarely-used component
import dynamic from "next/dynamic";

const PdfViewer = dynamic(() => import("@/components/PdfViewer"), {
  loading: () => <Skeleton className="h-96" />,
  ssr: false, // if it depends on browser-only APIs
});
```

- Split out anything heavy and non-critical: rich text editors, charting libraries, PDF viewers, map embeds, modals not open on load.
- Defer non-critical third-party scripts (analytics, chat widgets) using `next/script` with `strategy="lazyOnload"` or `"afterInteractive"` rather than blocking render:

```tsx
import Script from "next/script";
<Script src="https://widget.example.com/embed.js" strategy="lazyOnload" />
```

- For the current Flask site, apply the same principle with `<script defer>` / `<script async>` on non-critical JS, and load large below-the-fold assets (e.g. embedded maps, video) only via `IntersectionObserver` on scroll-into-view rather than at initial page load.

## 6. Code Splitting

- Route-based splitting is automatic in Next.js App Router (each route is its own chunk) — don't undermine it by importing heavy, route-specific code into a shared layout or root-level component.
- Component-based splitting: use `dynamic()`/`React.lazy()` for anything gated behind user interaction (a modal's content, a tab panel not currently active, an accordion body).
- Vendor splitting: verify the build's bundle analyzer (`@next/bundle-analyzer` or `webpack-bundle-analyzer`) periodically to catch a single dependency accidentally inflating the main chunk.

## 7. Rendering Strategy

- Prefer static generation / ISR for content that doesn't change per-request (product pages, blog posts, country landing pages) — these should be pre-rendered at build time or revalidated on an interval, not server-rendered fresh on every request.
- Reserve dynamic/SSR rendering for genuinely per-request content (a logged-in dashboard, personalized data).
- Cache aggressively at the edge/CDN for static assets — this repo's Flask site already sets 1-year `Cache-Control` on static files (`app.py`); mirror that discipline in any new service (immutable filenames/hashes + long cache lifetime for fingerprinted build assets).

---

## Quick Review Checklist

- [ ] Lighthouse mobile score ≥95 on Performance, Accessibility, Best Practices, SEO
- [ ] LCP ≤2.5s, CLS ≤0.1, INP ≤200ms
- [ ] All images sized correctly, modern format, lazy-loaded except the LCP image
- [ ] Every image has explicit dimensions or `aspect-ratio` (no layout shift)
- [ ] Fonts self-hosted, `font-display: swap`, only used weights loaded
- [ ] New dependencies checked for bundle-size cost before adding
- [ ] Heavy/below-the-fold components use dynamic import with a loading fallback
- [ ] Third-party scripts deferred (`lazyOnload`/`afterInteractive`/`defer`), never render-blocking
- [ ] Static/content pages pre-rendered or cached, not needlessly server-rendered per request
