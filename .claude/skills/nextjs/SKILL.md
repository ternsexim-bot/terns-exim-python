---
name: nextjs
description: Enforce App Router, TypeScript, Server Components by default, the Metadata API, next/image, next/font, route groups, and clean project architecture for any Next.js work. Use when scaffolding, reviewing, or extending a Next.js codebase.
---

# Next.js (App Router)

## Purpose

Standardize how Next.js projects are built in this org: App Router only, TypeScript-first, Server Components by default, and a clean, conventional file architecture. This repo's current marketing site is Flask/Jinja2 (see root `CLAUDE.md`) — this skill applies to any Next.js work: the CRM dashboard if it's ever rebuilt in Next.js, a future marketing site migration, or any new standalone Next.js project for TERNS EXIM.

---

## 1. App Router Only

Never use the `pages/` directory for new work. All routing lives under `app/`.

```
app/
├── layout.tsx              # Root layout — html/body, fonts, global providers
├── page.tsx                 # Home page
├── globals.css
├── (marketing)/              # Route group — no URL segment, groups related routes
│   ├── about/page.tsx
│   ├── products/
│   │   ├── page.tsx
│   │   └── [slug]/page.tsx
│   └── layout.tsx            # Shared layout for marketing pages only
├── (dashboard)/
│   ├── layout.tsx            # Auth-gated layout
│   └── leads/page.tsx
├── api/
│   └── leads/route.ts        # Route handlers (GET/POST/etc.)
├── not-found.tsx
├── error.tsx
└── loading.tsx
```

**Rules:**
- File conventions (`page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`, `route.ts`) are the only way routes and boundaries are declared — don't hand-roll routing logic.
- `error.tsx` and `loading.tsx` boundaries are required for any route that fetches data — never leave a route with an unhandled loading/error state.
- Server Actions (`"use server"`) are preferred over client-side `fetch` to internal API routes for form mutations (e.g. lead submission) when staying within the Next.js app.

## 2. TypeScript, Strict

`tsconfig.json` must have `"strict": true`. Never use `any` — use `unknown` and narrow, or define a proper type/interface. No `// @ts-ignore` without a comment explaining why and a linked issue if it's a known upstream type gap.

```ts
// types/lead.ts
export interface Lead {
  id: string;
  name: string;
  email: string;
  phone: string;
  company: string;
  country: string;
  productInterest?: string;
  message?: string;
  status: "New" | "Contacted" | "Negotiation" | "Won" | "Lost";
  createdAt: string;
}
```

- Prefer `interface` for object shapes that might be extended; `type` for unions, intersections, and utility compositions.
- Co-locate component prop types directly above the component rather than in a separate file, unless the type is shared across multiple components.
- Enable `noUncheckedIndexedAccess` for extra safety on array/object indexing when the project can tolerate the added narrowing.

## 3. Server Components by Default

Every component is a Server Component unless it specifically needs interactivity, browser APIs, or React hooks — then, and only then, add `"use client"` at the top of that specific leaf file.

```tsx
// app/(marketing)/products/page.tsx — Server Component, no directive needed
import { getProducts } from "@/lib/products";
import ProductCard from "@/components/ProductCard"; // server component
import EnquiryButton from "@/components/EnquiryButton"; // client component (opens a modal)

export default async function ProductsPage() {
  const products = await getProducts();
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {products.map((p) => (
        <ProductCard key={p.slug} product={p} cta={<EnquiryButton product={p.slug} />} />
      ))}
    </div>
  );
}
```

```tsx
// components/EnquiryButton.tsx
"use client";
import { useState } from "react";

export default function EnquiryButton({ product }: { product: string }) {
  const [open, setOpen] = useState(false);
  return <button onClick={() => setOpen(true)}>Request Quote</button>;
}
```

**Rules:**
- Push `"use client"` as far down the tree (to the smallest leaf) as possible — never mark a whole page or layout client just because one button needs `onClick`.
- Data fetching happens in Server Components via `async`/`await` directly — no `useEffect` + `fetch` for initial page data.
- Server Components can't use hooks, browser APIs, or event handlers — if a component needs any of those, it's a client component, full stop.
- Pass Server Components as `children`/props into Client Components (the "composition" pattern above) to keep the client bundle minimal — don't import a server-only data function into a client component.

## 4. Metadata API

Use the built-in Metadata API — never hand-write `<head>` tags in a page body.

```tsx
// app/(marketing)/products/[slug]/page.tsx
import type { Metadata } from "next";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const product = await getProduct(slug);

  return {
    title: `${product.name} | TERNS EXIM`,
    description: product.metaDescription,
    alternates: { canonical: `https://ternsexim.com/products/${slug}` },
    openGraph: {
      title: product.name,
      description: product.metaDescription,
      url: `https://ternsexim.com/products/${slug}`,
      images: [{ url: product.ogImage, width: 1200, height: 630 }],
      type: "website",
    },
    twitter: {
      card: "summary_large_image",
      title: product.name,
      description: product.metaDescription,
    },
  };
}
```

Static, site-wide defaults go in the root layout:

```tsx
// app/layout.tsx
export const metadata: Metadata = {
  metadataBase: new URL("https://ternsexim.com"),
  title: { default: "TERNS EXIM", template: "%s | TERNS EXIM" },
  robots: { index: true, follow: true },
};
```

See [[seo]] for what must be present in every page's metadata.

## 5. next/image

Always use `next/image`, never a raw `<img>` tag, for any content image.

```tsx
import Image from "next/image";

<Image
  src="/products/hex-bolts.jpg"
  alt="Stainless steel hex bolts, DIN 933, A2-70 grade"
  width={800}
  height={600}
  className="rounded-xl"
  priority={isAboveFold}
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
/>
```

**Rules:**
- `alt` text is required and descriptive — never empty unless the image is purely decorative (`alt=""`), and never generic ("image1.jpg").
- `priority` only on the LCP image (usually the hero image) — every other image lazy-loads by default, which is what you want.
- Provide `sizes` whenever the image isn't a fixed pixel size, so the browser doesn't download the largest variant unnecessarily.
- Use `fill` + a positioned/sized parent container for responsive/unknown-aspect-ratio images instead of guessing `width`/`height`.
- Store product/marketing images as optimized source files (WebP/AVIF where possible) — `next/image` handles format negotiation and resizing, but starting from a bloated source still costs build time and storage.

## 6. next/font

Always load fonts via `next/font`, never a `<link>` to Google Fonts or an `@import` in CSS — this self-hosts the font, eliminates layout shift, and removes the extra DNS/connection round-trip.

```tsx
// app/layout.tsx
import { Inter, Manrope } from "next/font/google";

const inter = Inter({ subsets: ["latin"], variable: "--font-body", display: "swap" });
const manrope = Manrope({ subsets: ["latin"], variable: "--font-display", weight: ["600", "700", "800"] });

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${manrope.variable}`}>
      <body>{children}</body>
    </html>
  );
}
```

- `display: "swap"` prevents invisible text during font load (avoids FOIT).
- Only load the weights actually used — don't pull in all 9 weights of a variable font family if the design uses 3.
- For a custom/licensed font, use `next/font/local` with the same pattern.

## 7. Route Groups & Clean Architecture

```
app/
├── (marketing)/        # public site — no auth
├── (dashboard)/         # authenticated CRM views
├── (auth)/              # login/signup, minimal layout
components/
├── ui/                  # generic, reusable primitives (Button, Card, Input)
├── marketing/            # marketing-page-specific composites
├── dashboard/            # dashboard-specific composites
lib/
├── api/                  # fetch wrappers / API clients
├── utils.ts
├── motion.ts             # shared Framer Motion variants — see [[framer-motion]]
types/
├── lead.ts
public/
```

**Rules:**
- Route groups `(name)` organize routes and let different sections share different root layouts (e.g. marketing nav vs. dashboard sidebar) without affecting the URL.
- Keep `components/ui` free of business logic — those are dumb, reusable primitives styled per [[premium-ui]] and [[tailwind]].
- Never let `app/` accumulate business logic beyond composition — data fetching helpers, validation, and formatting belong in `lib/`.
- One component per file, named exports for utilities, default export for the component/page itself.
- Environment variables: `NEXT_PUBLIC_*` prefix only for values genuinely safe to expose to the browser (e.g. a public API base URL); everything else stays server-only.

---

## Quick Review Checklist

- [ ] No `pages/` directory; all routing under `app/` using file conventions
- [ ] `strict: true` in tsconfig, no `any`
- [ ] `"use client"` only on the smallest leaf components that need it
- [ ] Every route has appropriate `loading.tsx`/`error.tsx` if it fetches data
- [ ] `generateMetadata`/static `metadata` present on every page, not hand-written `<head>` tags
- [ ] All images use `next/image` with real `alt` text; `priority` only on the LCP image
- [ ] All fonts loaded via `next/font`, only the weights actually used
- [ ] Route groups separate distinct layout contexts (marketing/dashboard/auth)
- [ ] `lib/` holds logic, `components/` holds presentation, `app/` holds composition/routing only
