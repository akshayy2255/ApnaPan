# ApnaPan — website

**Real Food · True Care · Live More**
Farm-direct spices, masalas, ready mixes and pickles from Karnataka — sourced from 480 farmer families, processed by a women-run factory, with 6% of every sale funding employees' children's education.

A complete, production-ready multi-page storefront: **25 pages**, trilingual (English · ಕನ್ನಡ · हिन्दी), e-commerce with cart and checkout, SEO structured data, and a widget-driven impact story.

---

## 1. Run it locally

Everything is static — no database, no framework, no `npm install`. You only need **Python 3** (or Node.js), and the server takes one command.

### The quickest way

**macOS / Linux** — double-click `start-mac-linux.sh`, or from a terminal:

```bash
cd apnapan
./start-mac-linux.sh          # = python3 serve.py 8000
```

**Windows** — double-click `start-windows.bat`.

Both open your browser at **http://localhost:8000** automatically.

### Or run the server directly

```bash
cd apnapan
python3 serve.py              # → http://localhost:8000, opens your browser
python3 serve.py 8080         # choose your own port
python3 serve.py 8080 --no-open
```

`serve.py` is a small wrapper around Python's built-in static server that:

- serves `index.html` for `/` and for any folder (`/blog/`, `/products/`)
- shows the styled `404.html` for missing pages instead of a bare error
- sends correct MIME types for `.woff2`, `.webp` and `.svg`
- sends `no-store` headers, so a normal refresh always shows your edits
- skips to the next free port if the one you asked for is busy (8000 → 8001 → …)
- prints a compact one-line log per request

Stop it with **Ctrl + C**.

### If you don't have Python

- **Node.js:** `npx --yes serve -l 8000 .`
- **PHP:** `php -S localhost:8000`
- **VS Code:** install *Live Server*, right-click `index.html` → *Open with Live Server*

### Don't run it from `file://`

Opening `index.html` by double-clicking mostly works, but browsers restrict `localStorage` on `file://` URLs, which the cart, wishlist and language choice rely on to *remember* themselves. Every storage call goes through a shim in `assets/js/app.js` / `assets/js/i18n.js`, so when storage is blocked or unavailable — `file://`, Safari private mode, a sandboxed preview iframe — the site still works, it just forgets between page loads. Use one of the servers above and nothing is forgotten.

### Editing content

Everything on the site comes from `_build/` — see section 3. After any content edit, regenerate the pages:

```bash
python3 _build/build.py
```

Then refresh the browser; no need to restart the server. (`serve.py` sends no-cache headers precisely so this loop stays fast.)

### Deploying later

The same folder uploads as-is to Netlify, Cloudflare Pages, GitHub Pages, Vercel or any cPanel host — see section 8. `serve.py` and the two start scripts are for local use only and are harmless in production.

---

## 2. What's inside

```
apnapan/
├── index.html                 Home — hero, problem→solution, featured products, impact counters,
│                              farm-to-market journey, testimonials, press, newsletter
├── our-story/                 Our Story — problem, mission, founder's note, timeline, growth loop
├── our-impact/                women's employment, farmer partnerships, the Class 10 Fund,
│                              where every ₹100 goes, photo stories
├── shop/                      Shop — 8 products, filters (category / price / highlights / diet), sorting
├── products/<slug>/           8 individual product pages (ingredients, sourcing farmer, nutrition,
│                              "meet the women who made this", reviews, related products)
├── how-it-works/              Sourcing → Processing → QC → Packaging → Distribution, batch traceability
├── for-farmers/               For Farmers — why partner, 4 steps, 2026–27 rate card, enquiry form, FAQs
├── careers/                   6 open roles, benefits, application form, honest FAQs
├── blog/ + blog/<slug>/       5 full articles (sourcing economics, the education fund,
│                              Byadagi chilli guide, pickle calendar, "what women-led means")
├── contact/                   Contact, CSR & partnership desk, factory visit booking, map placeholder
├── checkout/                  Cart → details → payment (Razorpay-ready, simulated fallback)
├── 404.html · sitemap.xml · robots.txt · .nojekyll
├── *.html  (10 files)         Legacy redirect stubs — story.html, farmers.html, shop.html, … keep old
│                              links alive by meta-refresh + canonical to the new clean URL
├── serve.py                   Local server (python3 serve.py)
├── start-mac-linux.sh         Double-click launcher
├── start-windows.bat          Double-click launcher
├── assets/
│   ├── css/styles.css         Design system (tokens, components, responsive, print, theme)
│   ├── css/fonts.css          Self-hosted webfonts (Marcellus, Inter, Noto Kannada/Devanagari)
│   ├── fonts/*.woff2          7 files, 404 KB total
│   ├── js/app.js              Cart, filters, tabs, counters, forms, checkout, nav/drawer/dropdown
│   ├── js/i18n.js             Language switcher (writes <html data-lang-active>)
│   ├── js/i18n-data.js        Generated translations (506 strings × 3 languages)
│   ├── js/schemes-data.js     Generated scheme + quiz data for /schemes/ (works offline)
│   ├── js/schemes.js          The schemes app: quiz, matching, help queue, explainer
│   ├── icons/                 App icons (192/512) for installing the schemes section
│   ├── js/data.js             Generated product catalogue + store config
│   └── images/                16 images (hero, farm, factory, lab, children, 8 packshots)
└── _build/                    The generator — edit content here, then rebuild
    ├── content.py             ← ALL products, people, numbers, jobs, posts, FAQs
    ├── schemes.py             ← ALL 6 government schemes + the quiz + the field team
    ├── i18n.py                ← ALL interface strings (en / kn / hi)
    ├── render.py              Routes, URLs, icons, page chrome, shared components (incl. the header)
    │                          NAV lives in content.py: an entry with "children" becomes a
    │                          dropdown group in the header and a disclosure list in the drawer
    ├── pages.py               The eleven page templates
    ├── build.py               Run this to regenerate the site
    └── test_header.py / test_site.py   Browser test suites (see "Testing" below)
```

### URLs

Every page is a **folder route** (`/shop/`, `/our-story/`, `/products/nellikai-pickle/`) and every
internal link is **relative** — no leading `/`. That means the same build works at a domain root
(`https://apnapan.com/shop/`) *and* under a project path (`https://user.github.io/ApnaPan/shop/`)
with no rebuild. The 10 legacy `.html` URLs still resolve via redirect stubs.

Route table lives in `_build/render.py` (`ROUTES`, `route()`, `page_path()`). Add a page there and
every nav/footer/sitemap reference follows.

### Testing

```bash
python3 -m pip install playwright && python3 -m playwright install chromium
cd apnapan && python3 serve.py 8000 --no-open &     # any static server works
python3 _build/test_header.py     # 122 checks — header, nav, About group, drawer, keyboard, a11y, theme
python3 _build/test_schemes.py    # 114 checks — schemes quiz, matching, offline queue, help flow
python3 _build/test_explainer.py  #  24 checks — recordings: plays the right file, caches it, falls back
python3 _build/test_site.py       # 272 checks — all 31 pages, links, cart, checkout, languages
python3 _build/audit_contrast.py  # WCAG contrast of every text element, both themes
```

All suites exit non-zero on any failure. Use them after touching routing, assets, the header or the theme.

### Rebuilding after an edit

```bash
cd apnapan
python3 _build/build.py
```

It rewrites every HTML page, `sitemap.xml`, `robots.txt`, `assets/js/data.js` and `assets/js/i18n-data.js`. Takes about a second.

---

## 3. Where to make changes

| I want to change… | Edit |
|---|---|
| Prices, sizes, products, nutrition, reviews | `_build/content.py` → `PRODUCTS` |
| Impact numbers (farmers, women, children) | `_build/content.py` → `IMPACT`, `EDUCATION`, `ALLOCATION` |
| The founder's note, timeline, growth loop | `_build/content.py` → `TIMELINE`; `_build/pages.py` → `story()` |
| Job openings, pay bands, benefits | `_build/content.py` → `JOBS`, `BENEFITS`, `CAREER_FAQ` |
| Farmer rate card | `_build/pages.py` → `farmers()` (the `rates` list) |
| Blog posts | `_build/content.py` → `POSTS` |
| Contact details, addresses, social links, FSSAI/GST numbers | `_build/content.py` → `BRAND` |
| Any interface text (in all three languages) | `_build/i18n.py` → `STR` / `EXTRA_STR` |
| Free-shipping threshold, COD fee, school-fund %, Razorpay key | `_build/build.py` → `js_data()` |
| The top navigation (order, labels, grouping, footer column) | `_build/content.py` → `NAV` |
| Government schemes: text, documents, amounts, cautions | `_build/schemes.py` → `SCHEMES` |
| The four quiz questions and their answers | `_build/schemes.py` → `QUIZ`, `QUIZ_OPTIONS` |
| Sakhi Champions and the districts they cover | `_build/schemes.py` → `COORDINATORS`, `DISTRICTS` |
| Colours, spacing, typography | `assets/css/styles.css` → `:root` tokens at the top |

### The navigation

The header today is **Home · Shop · Government Schemes · About ▾ · For Farmers · Careers ·
Contact** (the scheme finder sits next to the shop, because it is free and it is what many
of the women who need ApnaPan come for). It is also in the footer's **Company** column.

`NAV` in `_build/content.py` is the single source of truth for the header **and** the footer
list. A plain entry is a link; an entry with `"children"` becomes a group:

```python
{"key": "nav.about", "children": [
    {"key": "nav.story",  "route": "story"},
    {"key": "nav.impact", "route": "impact"},
    {"key": "nav.how",    "route": "how"},
    {"key": "nav.blog",   "route": "blog"},
]},
```

The same markup adapts to the device: in the desktop header it is an **"About ▾" dropdown**
(opening on hover, on click, and on Enter/Space, with Arrow keys, Escape and Tab handled);
in the mobile drawer it is a **collapsible list**, because there is no hover on a touch
screen. The four pages are also linked in the footer's **About Us** column, so they are
reachable without the dropdown. Renaming or adding an entry means adding one line to `NAV`
plus its label in `_build/i18n.py` — no template or CSS changes, and the header
and footer tests count the items from `NAV` itself, so they follow along.

---

## 3b. The Government Schemes section

`/schemes/` is a three-screen flow for a woman on a phone, in her language, with or
without network:

1. **Four tap questions** — state, business, what she needs, bank account. No typing
   anywhere: every answer is a button, and single-answer questions advance by
   themselves. Matching happens in the browser, so the quiz works offline.
2. **Only 2-3 schemes**, never the full list. She is always shown what she asked for
   (a loan request always returns a loan scheme), health cover always brings PM-JAY,
   and every card says *why* it was picked. If fewer than two match, the two
   near-universal schemes fill the gap.
3. **"Request help applying"** — this is deliberately *not* a form. It creates a task
   for the Sakhi Champion who covers her district: her name, number, what she covers
   and a one-tap WhatsApp handoff. Requests made offline are kept on the phone and
   posted when it is back online.

    /schemes/                     the quiz, results and "My requests"
    /schemes/<slug>/              one card: benefit, what you get, documents, how to apply
    /schemes/trainer-notes/       field-team sheet — teacher notes, noindex, not linked

**Content.** Everything lives in `_build/schemes.py`, one dict per scheme in the shape
the content team maintains it (`id, category, one_line, benefit_amount, who_qualifies,
documents_needed, how_to_apply, helpline, teacher_note` plus per-scheme extras).
Two rules in that file matter:

* `teacher_note` is trainer material. It is **never rendered in the app** — it appears
  only on `/schemes/trainer-notes/` (noindex). Guidance like "teach this first" is for
  the field team, not for her.
* Where eligibility is genuinely uncertain — Vishwakarma trade lists, ODOP district
  product lists — the scheme carries a `check_first` line, and the app shows
  "ask your Sakhi to check first" instead of promising it.

**The explainer.** Drop recordings at `assets/audio/<slug>-<lang>.mp3`
(e.g. `mudra-kn.mp3`, `mudra-hi.mp3`), rebuild, and the cards play them. The
languages you have are read at build time, so the app never requests a file that
isn't there and never plays a language she can't read: if her language has no
recording yet, the card says so and the phone reads the card aloud instead. Scripts
are the card's own four lines, so whoever records only has to read what is already
on screen — and the recording works offline too, because it is cached with the rest.

    python3 _build/test_explainer.py   # proves the above, then removes its own test file

**Where requests go.** Set `helpEndpoint` in `_build/build.py` → `js_data()` to your
endpoint and every request is POSTed there as JSON (`{slug, scheme, district, sakhi,
at, status, lang}`); it is marked sent only when the server accepts it, and retried
until then. It can also be set at runtime without a rebuild by putting the URL in
`localStorage.apnapan_help_endpoint`. Left empty, the section runs in demo mode: the
request stays on the phone and the app offers the WhatsApp/call handoff to her Sakhi.
The five Sakhi Champions in `COORDINATORS` are **sample data with demo phone
numbers** — replace them with your real roster.

**Offline.** `sw.js`, the manifest and the icons are generated at build time, so the
precache list can never drift from the real routes. The quiz, the cards, the document
ticks and the request queue all work with no network; the app says "Offline — cards
saved on this phone" rather than pretending.

---

## 4. Replace before you go live

This is a **demonstration site**. Every name, number and quote was written for the build, and all imagery is AI-generated. Before publishing:

**Content & credentials**
- [ ] **Photography** — replace all 16 images with photos of your real farms, unit, team and packs (same filenames in `assets/images/`, same aspect ratios; product shots are 620×1029).
- [ ] **People** — replace `made_by` and `sourced` names, quotes and villages on each product, and all `TESTIMONIALS`.
- [ ] **Impact numbers** — `IMPACT`, `EDUCATION`, `ALLOCATION` are illustrative. Replace with audited figures and delete the "illustrative" notes in `pages.py` (`home.problem`, `impact()`).
- [ ] **Registrations** — `BRAND["reg"]`: FSSAI licence, GSTIN, Udyam. Today they are obvious placeholders marked `(SAMPLE)`.
- [ ] **Phone, WhatsApp, email, addresses** — `BRAND["phone"]`, `phone_display`, `whatsapp`, `emails`, `addresses`. The WhatsApp float button and every form fallback point at `+91 90000 00000`.
- [ ] **Social links** — `BRAND["social"]` currently points at the home pages of Instagram, Facebook, YouTube and LinkedIn.
- [ ] **Press strip** — the "Featured in" logos on the home page are placeholders (The Hindu, Deccan Herald, YourStory, Krishi Jagran, The Better India). Delete the section or use real coverage you have permission to cite.
- [ ] **Domain** — `BRAND["url"]` (`https://www.apnapan.in`) is used in canonical tags, Open Graph, JSON-LD and sitemap.
- [ ] **Founder name** — "Lakshmi Devi R." and the founder photo are placeholders.

**Commerce**
- [ ] **Payment gateway** — in `_build/build.py`, set `"razorpayKey": "rzp_live_…"`. With a key present, `app.js` opens the real Razorpay checkout; with `""` it simulates a successful payment so the flow stays demoable. Add Razorpay's `checkout.js` script tag to `render.py → drawer_and_widgets()` (there is a comment marker) or to each page's `head()` via the `extra` parameter.
- [ ] **Orders have no backend.** The checkout validates, computes totals, takes payment and clears the cart, but nothing is stored or emailed. Connect it to a server (Razorpay webhook → your ERP/Google Sheet/Shopify) before selling.
- [ ] **Order confirmation** — the success panel is client-side only; wire real order IDs from your gateway.
- [ ] **GST invoicing** — no invoice is generated. Add this if you sell B2B.
- [ ] **Shipping rates** — flat ₹49 / free above ₹599, ₹25 COD fee: `js_data()` in `build.py`.
- [ ] **Terms, privacy, returns** — currently these footer links point at `contact/`. Add real policy pages.

**Forms** (contact, careers, farmers, newsletter, review) validate and confirm on screen but do not submit anywhere. Point them at Formspree / Google Forms / your CRM / a serverless function. Each form has a `data-form="…"` attribute and a `demo.*` notice you can delete.

**Also worth doing**
- [ ] Replace the map placeholder in `contact/` with a Google Maps embed (`<iframe>` inside `.map-frame`).
- [ ] Link the batch-code lookup shown on `how-it-works/` to a real endpoint, or label it "coming soon".
- [ ] Add the last 4 whole-spice SKUs (turmeric, coriander, chilli powder, sambar powder) — the "Whole & Ground Spices" category is already defined in `content.py` and will appear in the filters automatically as soon as a product uses `"category": "whole"`.

---

## 5. How the cart and checkout work

- Cart lives in `localStorage` (`apnapan_cart_v1`) as `{slug, size, qty}` lines; prices are looked up from `assets/js/data.js`, so editing a price needs only a rebuild.
- The drawer, badge count, free-shipping progress bar and totals are rendered by `app.js`.
- `checkout/` collects contact + address + payment method, recalculates shipping and the COD fee, and shows the education-fund contribution of that order (6% of pre-tax value).
- Wishlist is also `localStorage` (`apnapan_wish_v1`) — currently a UI affordance with no account system behind it.

## 6. How the languages work

- Every page ships in **English** with `data-i18n="key"` markers; `i18n.js` swaps text at runtime, so one build serves three languages and search engines index a single canonical URL.
- For strings the server renders without a marker (form labels, table headers, tab names), `i18n.js` also walks text nodes and matches exact English strings against the dictionary — that's why validation messages, buttons and section headings all switch too.
- Product names switch via `data-pname` using `name_kn` / `name_hi` from the catalogue.
- The choice is remembered in `localStorage`; first-time visitors get Kannada or Hindi automatically if their browser asks for it.
- **Translated:** all interface chrome, buttons, forms, errors, product names, badges, categories, toasts.
- **Not translated:** editorial content — product stories, blog articles, reviews, testimonials and long-form copy stay in English. To localise them, add keys in `i18n.py` and reference them from the templates (or add per-language fields to `content.py` alongside `name_kn`).
- **To add a language** (Tamil, Telugu, Marathi…): add a code block to `LANGS` and a third value per string in `i18n.py`, plus the font if it needs a new script. Nothing else changes.

## 7. SEO, performance, accessibility

**SEO** — unique title/description per page and product, canonical URLs, Open Graph + Twitter cards, keyword-targeted copy ("women-led spices", "farm to market pickles", "ethical sourcing India"), and JSON-LD for Organization, WebSite, Product (with price, rating and reviews), JobPosting, FAQPage, Blog/BlogPosting and BreadcrumbList. `sitemap.xml` and `robots.txt` are generated, with `/checkout/` disallowed.

**Performance** — no frameworks, no CDN requests: ~64 KB of CSS (unminified), ~30 KB of app JS, 404 KB of fonts, and progressive JPEGs (roadmap imagery 100–270 KB each, packshots ~100 KB). Images carry `width`/`height` to prevent layout shift; below-the-fold images are lazy-loaded. Run `python3 -m http.server` locally, or upload as-is — a CDN or Cloudflare in front is all you need.

**Accessibility** — semantic landmarks and heading order, skip-to-content link, visible focus rings, `aria-current` on the active nav item, `aria-pressed` on all toggles, `aria-selected` tabs, dialog semantics on the cart drawer, ≥44 px touch targets, `prefers-reduced-motion` support, and alt text on every image. Forms use real labels, `aria-invalid` and inline error text.

## 8. Light and dark mode

The site ships both. Light is the original design; dark is a **purely additive
stylesheet** at the end of `assets/css/styles.css`, so nothing about the light theme
was changed to make dark possible — verified by diffing every computed colour on
twelve pages against the previous build: three differences in total, all the
gold-button label fix described below.

**How it works.** A small inline script in `<head>` (in `render.head`) sets
`data-theme` on `<html>` before the first paint, so a dark-mode visitor never sees a
light flash. It reads `apnapan_theme` from `localStorage`; with no saved choice it
follows the operating system's `prefers-color-scheme`, and keeps following it until
the visitor chooses for themselves. The choice then sticks across pages and reloads.
Storage access is wrapped, so this still works in private mode, in a sandboxed frame
and from `file://`.

**The control.** A moon / sun icon button in the header, beside the language
switcher. Both icons ship in the button and CSS shows one, so it looks right even
with JavaScript off. It carries `aria-pressed` and an `aria-label` naming the mode
you would switch *to*, translated into all three languages. Below 561px the header
runs out of room, so the header button hides and an **Appearance** block with
explicit Light / Dark buttons takes its place in the mobile drawer — a full-width
control is a better thumb target than a 40px circle.

**How the dark palette was derived.** The design system is token-driven, so this is
mostly a matter of re-declaring the palette:

| Token | Light | Dark | Why |
|---|---|---|---|
| `--cream`, `--sand`, `--white` | warm off-whites | `#1c140e`, `#241a12`, `#251b13` | espresso-brown paper |
| `--ink`, `--ink-soft`, `--ink-mute` | near-black browns | cream, then muted tans | body text |
| `--terracotta`, `--terracotta-dark` | `#b4552d`, `#8e3e1d` | `#d4704a`, `#e79070` | lifted so accents stay legible as ink |
| `--mustard` | `#e3a62b` | `#e8b04a` | ditto |
| `--green` | `#1e4436` | unchanged | it is a *background* almost everywhere (topbar, footer, newsletter, chips) |

Three things needed care, and are the reason to read the code before editing it:

1. **A token that is ink in one place and a fill in another.** `--green` is the
   topbar and footer background *and* the colour of small icons and headings. It
   cannot be lightened without breaking the dark bands, so a second token,
   `--green-ink`, carries the ink use and is lifted only in dark mode.
2. **Permanently dark surfaces.** The topbar, marquee, green sections, newsletter,
   footer, banners and toasts keep light text in both themes, so they re-declare the
   tokens they need instead of inheriting the flipped ones. Without that, `--cream`
   text on a green band would have turned near-black and disappeared.
3. **Hardcoded light values.** The sticky header's frosted background, the mobile
   buy bar and the over-photo buttons were literal `rgba(253,248,240,…)`. They never
   consulted the palette and are overridden explicitly.

The product photography is shot on dark wood and studio grounds, so images are left
completely untouched in dark mode — they sit better there than on cream.

**Printing** always uses the light palette whatever the screen shows, so a printer
never receives a full-bleed espresso page.

**Contrast.** `_build/audit_contrast.py` measures every visible text element against
its real composited background, on 13 pages, in both themes, against WCAG AA (4.5:1
body, 3:1 large). Dark mode passes completely — 0 failures. Light mode reports ~379
failures inherited from the original design, about 96% of them a single cause:
`--ink-mute` renders at 4.07:1 on cards, a hair under AA. That is the existing
muted grey, not something this feature introduced, and it was deliberately left
alone so the light theme stays exactly as designed. The audit did find and fix one
genuine bug: inside green sections `.section--green a` out-specified `.btn`, so the
gold button's label was pale yellow on gold, 1.55:1. Buttons now keep the label
colour they ask for, in both themes.

---

## 9. Deploying

Any static host — the build output is plain files:

- **Netlify / Cloudflare Pages / Vercel** — drag the `apnapan` folder in, or connect the repo. Build command: none. Publish directory: the folder itself.
- **GitHub Pages** — push the folder, enable Pages.
- **cPanel / shared hosting** — upload everything except `_build/` to `public_html`.
- Exclude `_build/` from the upload (it is only needed to regenerate pages). Keep it in version control.

After deploying, submit `sitemap.xml` in Google Search Console and update `BRAND["url"]` first so the canonical URLs match your domain.

---

*Design system: terracotta `#b4552d` · mustard `#e3a62b` · deep green `#1e4436` · cream `#fdf8f0`, with Marcellus for display type and Inter for the interface.*
