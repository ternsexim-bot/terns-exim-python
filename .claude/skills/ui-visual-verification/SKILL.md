---
name: ui-visual-verification
description: Use proactively after every UI/CSS/visual/design change in this project — before presenting the result or asking for approval. Runs the app locally, captures desktop/tablet/mobile screenshots via Playwright, and checks for console errors, broken images, layout overflow, and working animations.
---

# UI Visual Verification

## Purpose

No UI/design change in this repo is "done" until it's been visually verified, not just code-reviewed. This applies to both services: the Flask marketing site (`app.py` + `templates/` + `static/`) and `crm-frontend/` (React/Vite). Apply this skill after every change covered by [[premium-ui]], [[accessibility]], [[performance]], [[framer-motion]], [[tailwind]], or [[terns-exim]] — before writing "here's the result" to the user.

**Never describe a visual change in prose alone and ask for approval.** Screenshot it first.

**Never move to the next section/component of a multi-step redesign without the user's explicit approval of the current one**, even if verification passes cleanly.

---

## Step 1 — Ensure Playwright is available

Check first; install only if missing. This is an ephemeral verification tool for *this session's* use — **never add it to `requirements.txt` or `package.json`**, it is not a project dependency.

```bash
# Python side (Flask marketing site)
./venv/Scripts/python.exe -c "import playwright" 2>&1 || pip install --quiet playwright
python -m playwright install chromium   # installs browser binaries if missing; add --with-deps on Linux if system libs are missing too
```

If `--with-deps` fails or isn't applicable (Windows has no such flag — browser binaries are self-contained), just `python -m playwright install chromium` is sufficient here.

## Step 2 — Run the app locally

**Flask marketing site** (repo root) — use the existing venv, a non-default port to avoid clashing with anything else running, and poll rather than sleep:

```bash
cd C:/Users/Prakash/terns-exim-python
PORT=5050 ./venv/Scripts/python.exe app.py > /tmp/flask-dev.log 2>&1 &
timeout 30 bash -c 'until curl -sf http://localhost:5050/ >/dev/null 2>&1; do sleep 1; done'
```

**`crm-frontend/`** (Vite/React):

```bash
cd C:/Users/Prakash/terns-exim-python/crm-frontend
npm run dev > /tmp/vite-dev.log 2>&1 &
timeout 30 bash -c 'until curl -sf http://localhost:3000/ >/dev/null 2>&1; do sleep 1; done'
```

Stop with a port-based kill when done (via `netstat -ano | grep :5050` → `Stop-Process -Id <pid> -Force` in PowerShell, since `$!`/job control across Bash tool calls on this Windows setup is unreliable) — never a broad `pkill -f`.

## Step 3 — Capture screenshots at three breakpoints, full page

Write a small one-off Playwright script to the scratchpad directory (not the repo) and run it with the venv's `python`. Always **full-page** screenshots (`full_page=True`) so nothing below the fold is missed, at:

```python
from playwright.sync_api import sync_playwright

BREAKPOINTS = {
    "desktop": {"width": 1920, "height": 1080},
    "tablet":  {"width": 834,  "height": 1194},
    "mobile":  {"width": 390,  "height": 844},
}

with sync_playwright() as p:
    browser = p.chromium.launch()
    errors, page_errors = [], []
    for name, viewport in BREAKPOINTS.items():
        page = browser.new_page(viewport=viewport)
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: page_errors.append(str(exc)))
        page.goto("http://localhost:5050/", wait_until="networkidle")
        page.screenshot(path=f"{OUT}/{name}-full.png", full_page=True)
        # broken images, overflow checks — see Steps 5-6
        page.close()
    browser.close()
```

Capture the specific section under review as its own cropped screenshot too (`page.locator(selector).screenshot(...)`), same as was done for the nav — full-page is for context, the cropped shot is what the user actually reviews closely.

## Step 4 — Console errors

Collect `console` (type `error`) and `pageerror` events during navigation and any interaction exercised in Step 7. **Distinguish pre-existing baseline noise from newly introduced errors** — e.g. this project already has a known CSP warning from the Google Analytics script tag in `base.html`, unrelated to any UI work. Report new errors as blocking; note pre-existing ones only if directly relevant.

## Step 5 — Broken images

```python
broken = page.eval_on_selector_all(
    "img",
    "imgs => imgs.filter(img => img.complete && img.naturalWidth === 0).map(img => img.src)"
)
```

Any non-empty result is a blocking finding — report the src(s).

## Step 6 — Layout overflow / shift

Horizontal overflow check (the most common CSS regression) at every breakpoint:

```python
overflow = page.evaluate(
    "document.documentElement.scrollWidth > document.documentElement.clientWidth"
)
```

If `true`, find the offending element:

```python
culprit = page.evaluate("""
  () => {
    const vw = document.documentElement.clientWidth;
    return [...document.querySelectorAll('*')]
      .filter(el => el.getBoundingClientRect().right > vw)
      .map(el => el.tagName + '.' + el.className)
      .slice(0, 5);
  }
""")
```

For layout shift, Playwright doesn't expose CLS directly without extra instrumentation — a lightweight proxy is comparing an element's bounding box immediately after `domcontentloaded` vs. after `networkidle` + a short wait; a delta indicates content jumping in after initial paint (see [[performance]] for the underlying CLS causes to check against: unset image dimensions, web-font swap, late-loading embeds).

## Step 7 — Animations

Don't just screenshot the resting state — trigger the actual interaction and capture the result:

- Scroll-triggered reveal → `page.evaluate("window.scrollTo(0, N)")`, wait, screenshot (as done for the navbar's `scrolled` state)
- Hover micro-interaction → `page.hover(selector)`, screenshot
- Modal/menu open → `page.click(trigger)`, wait for the element, screenshot (as done for the mobile nav menu and the enquiry modal)
- Confirm `prefers-reduced-motion` doesn't break layout: `page.emulate_media(reduced_motion="reduce")`, reload, screenshot — the element should still render correctly with animation simply skipped, never end up stuck mid-transition or invisible

## Step 8 — Compare against the previous version

Keep the prior verification's screenshots in the scratchpad (don't overwrite filenames between rounds — suffix with a section name or short label). When presenting the new set, explicitly note what's different from the last-shown version, not just from the pre-redesign baseline — the user is tracking incremental changes across a section-by-section redesign (per [[terns-exim]] and [[premium-ui]]), and needs to see the delta each round, not re-derive it from two screenshots themselves.

## Step 9 — Verify existing functionality wasn't touched

Re-exercise the functional paths adjacent to the visual change (this is what actually proves "100% functionality preserved," not just the absence of console errors): click through to confirm forms still submit / open, links still route, existing unrelated routes still return 200. Keep this scoped to what's plausibly affected by the change, not the entire site on every pass.

## Step 10 — Clean up and report

Stop the dev server (port-based kill, Step 2). Then present, in this order:
1. The screenshots (full-page + the relevant cropped section, across all three breakpoints)
2. A concise summary of what changed and why, tied to the specific design principle it fixes (not just "made it nicer")
3. Explicit confirmation that console/image/overflow/animation/functionality checks passed (or a blocking finding if not — fix before presenting, don't present broken work)
4. A direct, explicit wait for approval — do not start the next section, component, or page until the user says to proceed
