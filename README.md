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

Opening `index.html` by double-clicking mostly works, but browsers restrict `localStorage` on `file://` URLs, which the cart, wishlist and language choice all rely on. Use one of the servers above — it's why they exist.

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
│   ├── css/styles.css         Design system (tokens, components, responsive, print)
│   ├── css/fonts.css          Self-hosted webfonts (Marcellus, Inter, Noto Kannada/Devanagari)
│   ├── fonts/*.woff2          7 files, 404 KB total
│   ├── js/app.js              Cart, filters, tabs, counters, forms, checkout, nav/drawer/dropdown
│   ├── js/i18n.js             Language switcher (writes <html data-lang-active>)
│   ├── js/i18n-data.js        Generated translations (312 strings × 3 languages)
│   ├── js/data.js             Generated product catalogue + store config
│   └── images/                16 images (hero, farm, factory, lab, children, 8 packshots)
└── _build/                    The generator — edit content here, then rebuild
    ├── content.py             ← ALL products, people, numbers, jobs, posts, FAQs
    ├── i18n.py                ← ALL interface strings (en / kn / hi)
    ├── render.py              Routes, URLs, icons, page chrome, shared components (incl. the header)
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
python3 _build/test_header.py     # 73 checks — header, nav, dropdown, drawer, keyboard, a11y
python3 _build/test_site.py       # 168 checks — all 24 pages, links, cart, checkout, languages
```

Both suites exit non-zero on any failure. Use them after touching routing, assets or the header.

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
| Colours, spacing, typography | `assets/css/styles.css` → `:root` tokens at the top |

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

## 8. Deploying

Any static host — the build output is plain files:

- **Netlify / Cloudflare Pages / Vercel** — drag the `apnapan` folder in, or connect the repo. Build command: none. Publish directory: the folder itself.
- **GitHub Pages** — push the folder, enable Pages.
- **cPanel / shared hosting** — upload everything except `_build/` to `public_html`.
- Exclude `_build/` from the upload (it is only needed to regenerate pages). Keep it in version control.

After deploying, submit `sitemap.xml` in Google Search Console and update `BRAND["url"]` first so the canonical URLs match your domain.

---

*Design system: terracotta `#b4552d` · mustard `#e3a62b` · deep green `#1e4436` · cream `#fdf8f0`, with Marcellus for display type and Inter for the interface.*
