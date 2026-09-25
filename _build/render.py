# -*- coding: utf-8 -*-
"""ApnaPan — HTML rendering helpers, page chrome and shared components."""
import html
import json

from content import BRAND, NAV, TRUST_BADGES, IMPACT, CATEGORIES, PRODUCTS
from i18n import STR, LANGS

E = html.escape


# ------------------------------------------------------------------ i18n glue
def T(key):
    """English text for a key (the HTML ships in English)."""
    return E(STR[key][0])


def Traw(key):
    return STR[key][0]


def A(key):
    """data-i18n attribute for runtime language swapping."""
    return f'data-i18n="{key}"'


def AP(key):
    """Placeholder attribute."""
    return f'data-i18n-attr="placeholder:{key}"'


# ---------------------------------------------------------------------- icons
ICONS = {
    "cart": '<circle cx="9.5" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h2.3l2.5 11.1a2 2 0 0 0 2 1.6h8.6a2 2 0 0 0 1.9-1.4L21 7H5"/>',
    "menu": '<path d="M3 6h18M3 12h18M3 18h18"/>',
    "moon": '<path d="M20.5 14.3A8.5 8.5 0 0 1 9.7 3.5a8.5 8.5 0 1 0 10.8 10.8z"/>',
    "sun-theme": '<circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.2 5.2l1.6 1.6M17.2 17.2l1.6 1.6M18.8 5.2l-1.6 1.6M6.8 17.2l-1.6 1.6"/>',
    "close": '<path d="M18 6 6 18M6 6l12 12"/>',
    "chev-r": '<path d="M9 5l7 7-7 7"/>',
    "chev-d": '<path d="M6 9l6 6 6-6"/>',
    "arrow-r": '<path d="M4 12h15M13 6l6 6-6 6"/>',
    "arrow-up": '<path d="M12 20V5M6 11l6-6 6 6"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "minus": '<path d="M5 12h14"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "star": '<path d="M12 2.6l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5L12 17.4l-5.8 3.1 1.1-6.5L2.6 9.4l6.5-.9z" fill="currentColor" stroke="none"/>',
    "star-o": '<path d="M12 3.3l2.6 5.3 5.8.8-4.2 4.1 1 5.8L12 16.6l-5.2 2.7 1-5.8-4.2-4.1 5.8-.8z"/>',
    "heart": '<path d="M20.8 5.6a5 5 0 0 0-7.1 0L12 7.3l-1.7-1.7a5 5 0 1 0-7.1 7.1L12 21l8.8-8.3a5 5 0 0 0 0-7.1z"/>',
    "women": '<circle cx="12" cy="8" r="4.2"/><path d="M12 12.2v7M8.6 16.4h6.8M5 21c1.4-3.2 4-4.4 7-4.4s5.6 1.2 7 4.4"/>',
    "farm": '<path d="M3 20h18M5 20V9l7-5 7 5v11"/><path d="M9 20v-5h6v5"/><path d="M12 4v4"/>',
    "shield": '<path d="M12 3l7.5 3v6c0 4.4-3 8-7.5 9.6C7.5 20 4.5 16.4 4.5 12V6z"/><path d="M9 12l2 2 4-4"/>',
    "leaf": '<path d="M20 4c-9 0-15 4.4-15 11.5 0 2 .5 3.6 1.3 4.9C9 14 13.6 11.4 20 10.6"/><path d="M4 20c1-4.6 3.6-8 8-10"/>',
    "school": '<path d="M12 4 2 9l10 5 10-5z"/><path d="M6 11.4V16c0 1.6 2.7 3 6 3s6-1.4 6-3v-4.6"/><path d="M22 9v6"/>',
    "pin": '<path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/>',
    "rupee": '<path d="M7 4h10M7 9h10M15.5 4c0 4.5-2.6 6.5-6.5 6.5H7l8 9.5"/>',
    "spark": '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M18.5 16.5l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7z"/>',
    "box": '<path d="M3.5 7.5 12 3l8.5 4.5v9L12 21l-8.5-4.5z"/><path d="M3.5 7.5 12 12l8.5-4.5M12 12v9"/>',
    "truck": '<path d="M2 6.5h11v9H2z"/><path d="M13 9.5h4l3 3v3h-7z"/><circle cx="6" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/>',
    "flask": '<path d="M9 3h6M10 3v5L5.5 17.2A2 2 0 0 0 7.3 20.4h9.4a2 2 0 0 0 1.8-3.2L14 8V3"/><path d="M7.6 14.5h8.8"/>',
    "phone": '<path d="M6.5 3.5h3l1.5 4-2 1.5a11 11 0 0 0 6 6l1.5-2 4 1.5v3a2 2 0 0 1-2.2 2A17 17 0 0 1 4.5 5.7a2 2 0 0 1 2-2.2z"/>',
    "mail": '<rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/><path d="M3 7l9 6 9-6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5.4l3.6 2.2"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 3.9 5.6 3.9 9s-1.3 6.4-3.9 9c-2.6-2.6-3.9-5.6-3.9-9S9.4 5.6 12 3z"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>',
    "lock": '<rect x="4.5" y="10.5" width="15" height="10" rx="2.5"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/>',
    "gift": '<path d="M4 11.5h16V20H4z"/><path d="M2.5 7.5h19v4h-19zM12 7.5V20"/><path d="M12 7.5S10.8 3 8.4 3a2.4 2.4 0 0 0 0 4.5zM12 7.5s1.2-4.5 3.6-4.5a2.4 2.4 0 0 1 0 4.5z"/>',
    "users": '<circle cx="9" cy="8" r="3.6"/><path d="M2.8 20c.6-3.4 3.1-5.4 6.2-5.4s5.6 2 6.2 5.4"/><path d="M16 5.2a3.4 3.4 0 0 1 0 6.6M17.5 14.9c2 .7 3.4 2.4 3.9 5.1"/>',
    "book": '<path d="M4 4.5h6a3 3 0 0 1 3 3V20a2.5 2.5 0 0 0-2.5-2.5H4z"/><path d="M20 4.5h-6a3 3 0 0 0-3 3V20a2.5 2.5 0 0 1 2.5-2.5H20z"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17M8 3.5V7M16 3.5V7"/>',
    "building": '<path d="M4 21V5.5A1.5 1.5 0 0 1 5.5 4H12v17"/><path d="M12 9h6.5A1.5 1.5 0 0 1 20 10.5V21M2.5 21h19"/><path d="M7 8h2M7 12h2M7 16h2M15 12h2M15 16h2"/>',
    "scale": '<path d="M12 3v18M7 21h10"/><path d="M12 6 5 9l-2.2 5.2a4 4 0 0 0 7.4 0z"/><path d="M12 6l7 3 2.2 5.2a4 4 0 0 1-7.4 0z"/>',
    "flame": '<path d="M12 21c3.6 0 6-2.3 6-5.4 0-4.6-6-12-6-12s-6 7.4-6 12C6 18.7 8.4 21 12 21z"/><path d="M12 17.5c1.2 0 2-.8 2-1.9 0-1.4-2-3.6-2-3.6s-2 2.2-2 3.6c0 1.1.8 1.9 2 1.9z"/>',
    "seed": '<path d="M12 21c0-6 3.5-10 8-11-1 6.5-4 10-8 11z"/><path d="M12 21C12 15 8.5 11 4 10c1 6.5 4 10 8 11z"/>',
    "sun": '<circle cx="12" cy="12" r="4.2"/><path d="M12 2v2.6M12 19.4V22M2 12h2.6M19.4 12H22M4.9 4.9l1.9 1.9M17.2 17.2l1.9 1.9M19.1 4.9l-1.9 1.9M6.8 17.2l-1.9 1.9"/>',
    "filter": '<path d="M3 5.5h18l-7 8V20l-4-2.5v-4z"/>',
    "trash": '<path d="M4 7h16M9.5 7V4.5h5V7M6.5 7l1 13h9l1-13"/>',
    "quote": '<path d="M9.5 6C6.4 7.4 4.8 9.9 4.8 13.2c0 2.7 1.6 4.8 4 4.8 2 0 3.6-1.5 3.6-3.5s-1.5-3.4-3.4-3.4c-.4 0-.8 0-1 .2.3-1.4 1.4-2.8 3-3.7zM20 6c-3.1 1.4-4.7 3.9-4.7 7.2 0 2.7 1.6 4.8 4 4.8 2 0 3.6-1.5 3.6-3.5S21.4 11 19.5 11c-.4 0-.8 0-1 .2.3-1.4 1.4-2.8 3-3.7z" fill="currentColor" stroke="none"/>',
    "play": '<path d="M8 5.5l11 6.5-11 6.5z" fill="currentColor" stroke="none"/>',
    "award": '<circle cx="12" cy="9" r="5.5"/><path d="M8.6 13.8 7 21l5-2.6L17 21l-1.6-7.2"/>',
    "bus": '<rect x="3.5" y="4" width="17" height="13" rx="2.5"/><path d="M3.5 10.5h17M7 20v-3M17 20v-3"/><circle cx="7.5" cy="14.5" r="1"/><circle cx="16.5" cy="14.5" r="1"/>',
    "hand-heart": '<path d="M12 21c-3.6-2.2-6-4.6-6-7.4a3.4 3.4 0 0 1 6-2.2 3.4 3.4 0 0 1 6 2.2c0 2.8-2.4 5.2-6 7.4z"/><path d="M4 20V9M20 20V9"/>',
    "instagram": '<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17" cy="7" r="1.1" fill="currentColor" stroke="none"/>',
    "facebook": '<path d="M14.5 8.5H17V5h-2.5A4.5 4.5 0 0 0 10 9.5V11H7.5v3.5H10V21h3.5v-6.5H16l.8-3.5H13.5V9.7c0-.7.3-1.2 1-1.2z"/>',
    "youtube": '<rect x="2.5" y="5.5" width="19" height="13" rx="4"/><path d="M10.5 9.5l5 2.5-5 2.5z" fill="currentColor" stroke="none"/>',
    "linkedin": '<rect x="3.5" y="3.5" width="17" height="17" rx="3"/><path d="M8 10.5V17M8 7.6v.1M12 17v-3.6c0-1 .8-1.9 1.9-1.9s1.9.9 1.9 1.9V17M12 10.5V17"/>',
    "whatsapp": '<path d="M17.5 14.4c-.3-.2-1.8-.9-2-1-.3-.1-.5-.2-.7.1-.2.3-.8 1-.9 1.2-.2.2-.4.2-.7.1-.3-.2-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.5-.5c.2-.2.2-.3.4-.5.1-.2.1-.4 0-.5-.1-.2-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.2.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3M12.1 21.5h-.1a9.9 9.9 0 0 1-5-1.4l-.4-.2-3.7 1 1-3.6-.3-.4a9.9 9.9 0 0 1-1.5-5.3c0-5.4 4.4-9.9 9.9-9.9 2.6 0 5.1 1 7 2.9a9.8 9.8 0 0 1 2.9 7c0 5.4-4.4 9.9-9.9 9.9m8.4-18.3A11.8 11.8 0 0 0 12.1 0C5.5 0 .2 5.3.2 11.9c0 2.1.5 4.1 1.6 5.9L0 24l6.3-1.7c1.7.9 3.7 1.4 5.7 1.4h.1c6.6 0 11.9-5.3 11.9-11.9 0-3.2-1.2-6.2-3.5-8.4z" fill="currentColor" stroke="none"/>',
    "sunrise": '<path d="M12 3v5M5.6 9.6 7 11M18.4 9.6 17 11M2 18h20M4.5 21h15"/><path d="M8 15a4 4 0 0 1 8 0"/>',
    "sparkle": '<path d="M12 3v6M12 15v6M3 12h6M15 12h6M6.3 6.3l3 3M14.7 14.7l3 3M17.7 6.3l-3 3M9.3 14.7l-3 3"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.6v.1"/>',
    "megaphone": '<path d="M3 10.5v3l11 5V5.5z"/><path d="M14 8.5a3.5 3.5 0 0 1 0 7"/><path d="M6.5 14v4.5a1.5 1.5 0 0 0 3 0V15.5"/>',
}

TYPE_KEY = {"Ground masala": "type.masala", "Ready mix": "type.mix", "Pickle": "type.pickle"}
SPICE_KEY = {"Mild": "spice.mild", "Medium": "spice.medium", "Medium-hot": "spice.mediumhot", "Hot": "spice.hot"}
DIET_KEY = {"Vegetarian": "diet.veg", "Vegan": "diet.vegan", "Vegan option": "diet.veganopt",
            "Gluten-free": "diet.gf", "No onion-garlic": "diet.noongarlic"}
BADGE_KEY = {"Stone-ground": "badge.stone", "Small batch": "badge.small", "High chilli": "badge.chilli",
             "Just add water": "badge.water", "Just add hot water": "badge.hotwater",
             "Makes 22–25 vadas": "badge.vada", "Makes 8–10 rottis": "badge.rotti",
             "Travel friendly": "badge.travel", "No cooking of masala": "badge.nocook",
             "Sun-cured": "badge.sun", "Mustard oil": "badge.mustard", "Oil-free option": "badge.oilfree",
             "No preservatives": "common.nopreservative"}


def mark(text, table):
    """Return an inline span carrying data-i18n when we know the key."""
    k = table.get(text)
    return f'<span {A(k)}>{E(text)}</span>' if k else E(text)


SOCIAL_ICON = {"instagram": "instagram", "facebook": "facebook", "youtube": "youtube", "linkedin": "linkedin", "whatsapp": "whatsapp"}


def live_categories():
    """Categories that actually have products — keeps empty filters out of the UI."""
    return [c for c in CATEGORIES if any(p["category"] == c["id"] for p in PRODUCTS)]


def icon(name, cls="", size=None, stroke=1.7):
    style = f' style="width:{size}px;height:{size}px"' if size else ""
    return (f'<svg class="{cls}"{style} viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS.get(name, ICONS["info"])}</svg>')


def logo_svg(cls="", color="currentColor"):
    """Lotus mark — 5 petals + bowl, matching the jar label."""
    return f'''<svg class="{cls}" viewBox="0 0 64 64" fill="none" aria-hidden="true">
  <circle cx="32" cy="32" r="30.2" stroke="{color}" stroke-opacity=".32" stroke-width="1.6"/>
  <g stroke="{color}" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <path d="M32 20c3.4 3.6 5.1 7.1 5.1 10.6S35.4 37.8 32 41c-3.4-3.2-5.1-6.9-5.1-10.4S28.6 23.6 32 20z"/>
    <path d="M32 41c-3.9-1.1-7-3.1-9.3-6-2.3-2.9-3.3-6.1-3-9.6 3.8.5 7 1.9 9.5 4.3M32 41c3.9-1.1 7-3.1 9.3-6 2.3-2.9 3.3-6.1 3-9.6-3.8.5-7 1.9-9.5 4.3"/>
    <path d="M17 41.5c4.2 3.2 9.2 4.9 15 4.9s10.8-1.7 15-4.9"/>
  </g>
</svg>'''



# -------------------------------------------------------------------- routes
# One place that defines every URL on the site. Pages are emitted as folder
# index.html files so the public URLs stay clean (/shop/, /our-story/), which
# is what GitHub Pages, Netlify and Cloudflare Pages all serve natively.
ROUTES = {
    "home":     "",
    "story":    "our-story/",
    "impact":   "our-impact/",
    "shop":     "shop/",
    "how":      "how-it-works/",
    "farmers":  "for-farmers/",
    "careers":  "careers/",
    "blog":     "blog/",
    "contact":  "contact/",
    "checkout": "checkout/",
    "notfound": "404.html",
}


def route(name):
    return ROUTES[name]


def product_route(slug):
    return f"products/{slug}/"


def post_route(slug):
    return f"blog/{slug}/"


def page_path(name, slug=None):
    """Where a page is written on disk (relative to the site root)."""
    if name == "notfound":
        return "404.html"          # must stay at the root for GitHub Pages
    if name in ROUTES:
        p = ROUTES[name]
        return (p + "index.html") if p else "index.html"
    if name == "product":
        return f"products/{slug}/index.html"
    if name == "post":
        return f"blog/{slug}/index.html"
    raise KeyError(name)


# -------------------------------------------------------------- url helpers
class Urls:
    """Relative-URL builder. depth = how many folders below the site root.

    depth 0 -> "" (root pages)          u("shop/")       -> "shop/"
    depth 1 -> ".." (/shop/index.html)  u("shop/")       -> "../shop/"
    depth 2 -> "../.." (product pages)  u("shop/")       -> "../../shop/"

    Relative links (never "/absolute") so the site works both at a domain root
    and inside a GitHub Pages project path such as /ApnaPan/.
    """

    def __init__(self, depth=0):
        self.depth = depth if isinstance(depth, int) else len(depth.split("..")) - 1
        self.base = "/".join([".."] * self.depth)

    def __call__(self, path=""):
        if path.startswith(("http", "#", "mailto:", "tel:", "data:")):
            return path
        if not path:
            # Home: "./" at the root, "../" one level down — never an empty href.
            return (self.base + "/") if self.base else "./"
        prefix = (self.base + "/") if self.base else ""
        return prefix + path

    # convenience so templates can stay readable
    def page(self, name):
        return self(route(name))

    def product(self, slug):
        return self(product_route(slug))

    def post(self, slug):
        return self(post_route(slug))


# ------------------------------------------------------------------ meta/head
def head(title, desc, path, css_url, u, jsonld=None, extra=""):
    ld = ""
    if jsonld:
        blocks = jsonld if isinstance(jsonld, list) else [jsonld]
        ld = "\n".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>' for b in blocks)
    return f'''<!DOCTYPE html>
<html lang="en-IN" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>
/* Theme before first paint — otherwise a dark-mode visitor gets a cream flash.
   Runs before the stylesheets; app.js only reads the result afterwards. */
(function () {{
  var t = null;
  try {{ t = localStorage.getItem("apnapan_theme"); }} catch (e) {{}}
  if (t !== "dark" && t !== "light") {{
    t = (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches) ? "dark" : "light";
  }}
  document.documentElement.setAttribute("data-theme", t);
}})();
</script>
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{BRAND["url"]}/{path}">
<meta name="theme-color" id="themeColor" content="#1e4436">
<meta name="color-scheme" content="light dark">
<meta name="author" content="{BRAND["legal"]}">
<meta name="keywords" content="women-led spices, farm to market pickles, ethical sourcing India, Karnataka masala, direct from farmers, ApnaPan, bisibelebath masala, mavina midi pickle">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND["name"]}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{BRAND["url"]}/{path}">
<meta property="og:locale" content="en_IN">
<meta property="og:image" content="{BRAND["url"]}/assets/images/hero-farm.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{u('assets/favicon.svg')}" type="image/svg+xml">
<link rel="apple-touch-icon" href="{u('assets/favicon.svg')}">
<link rel="preload" as="font" type="font/woff2" href="{u('assets/fonts/marcellus-latin.woff2')}" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="{u('assets/fonts/inter-latin.woff2')}" crossorigin>
<link rel="stylesheet" href="{u('assets/css/fonts.css')}">
<link rel="stylesheet" href="{css_url}">
{extra}
{ld}
</head>
<body>
<a class="skip-link" href="#main" {A("a11y.skiptocontent")}>{T("a11y.skiptocontent")}</a>
'''


def header(active, u, cart_icon_count=True):
    """Compact, fully functional header.

    Row 1 — utility bar: free shipping · impact line · phone · For Farmers · Careers
    Row 2 — brand · primary navigation · language · basket · (mobile) menu

    Every item is a real link or button: <a> for navigation, <button> for the
    menu and the language dropdown. Active state comes from `active` (a NAV key)
    so "Home" is never hard-coded.
    """
    nav_items = []
    for n in NAV:
        key = n["route"]
        is_current = (n["key"] == active)
        cur = ' aria-current="page"' if is_current else ""
        nav_items.append(
            f'<li><a class="nav__link" href="{u(route(key))}"{cur} {A(n["key"])}>{T(n["key"])}</a></li>'
        )
    nav_links = "\n        ".join(nav_items)

    langs = "\n".join(
        f'<li><button type="button" data-lang="{l["code"]}" aria-pressed="{"true" if l["code"]=="en" else "false"}">'
        f'<span>{l["label"]}</span><span class="native">{l["native"]}</span></button></li>' for l in LANGS)

    # Language block inside the mobile drawer — same buttons, same handler.
    mobile_langs = "\n          ".join(
        f'<li><button type="button" data-lang="{l["code"]}" aria-pressed="{"true" if l["code"]=="en" else "false"}">'
        f'<span>{l["label"]}</span><span class="native">{l["native"]}</span></button></li>' for l in LANGS)

    return f'''
<div class="topbar">
  <div class="wrap topbar__inner">
    <p class="topbar__msg">
      <span class="topbar__item">{icon("truck", size=14)}<span {A("common.freeship")}>{T("common.freeship")}</span></span>
      <span class="topbar__sep" aria-hidden="true">·</span>
      <span class="topbar__item topbar__extra">{icon("women", size=14)}<span {A("home.hero.stamp")}>{T("home.hero.stamp")}</span></span>
    </p>
    <div class="topbar__actions">
      <a class="topbar__phone" href="tel:{BRAND["phone"]}" aria-label="Call {BRAND['phone_display']}">
        {icon("phone", size=14)}<span>{BRAND["phone_display"]}</span>
      </a>
      <a class="topbar__extra" href="{u(route("farmers"))}" {A("nav.farmers")}>{T("nav.farmers")}</a>
      <a class="topbar__extra" href="{u(route("careers"))}" {A("nav.careers")}>{T("nav.careers")}</a>
    </div>
  </div>
</div>
<header class="site-header" id="siteHeader">
  <div class="wrap header__inner">
    <a class="brand" href="{u(route("home"))}" aria-label="{BRAND['name']} — home">
      {logo_svg("brand__mark", "#b4552d")}
      <span class="brand__text">
        <span class="brand__name">{BRAND["wordmark"]}</span>
        <span class="brand__tag">Real Food · True Care · Live More</span>
      </span>
    </a>

    <nav class="nav" id="nav" aria-label="Main navigation">
      <div class="nav__head">
        <span class="nav__title">{T("nav.menu")}</span>
        <button class="icon-btn nav__close" type="button" data-nav-close aria-label="{T('nav.close')}" aria-expanded="false">{icon("close")}</button>
      </div>
      <ul class="nav__list">
        {nav_links}
      </ul>
      <div class="nav__lang">
        <span class="nav__lang-title">{icon("globe", size=15)} <span {A("nav.language")}>{T("nav.language")}</span></span>
        <ul class="nav__lang-list">{mobile_langs}</ul>
      </div>
      <div class="nav__theme">
        <div class="nav__theme-row">
          <span class="nav__theme-title">
            {icon("sun-theme", size=16).replace('<svg', '<svg data-theme-icon="sun"', 1)}
            {icon("moon", size=16).replace('<svg', '<svg data-theme-icon="moon"', 1)}
            <span {A("nav.theme")}>{T("nav.theme")}</span>
          </span>
          <button class="switch" type="button" data-theme-toggle role="switch" aria-checked="false"
                  aria-label="{T('a11y.theme')}" data-i18n-attr="aria-label:a11y.theme">
            <span class="switch__knob">
              {icon("sun-theme", cls="switch__sun", size=13)}
              {icon("moon", cls="switch__moon", size=13)}
            </span>
          </button>
        </div>
      </div>
      <a class="btn nav__cta" href="{u(route("shop"))}">{icon("cart")} <span {A("common.shop")}>{T("common.shop")}</span></a>
    </nav>

    <div class="header__tools">
      <button class="icon-btn theme-btn" type="button" data-theme-toggle aria-pressed="false"
              aria-label="{T('a11y.theme')}" title="{T('a11y.theme')}"
              data-i18n-attr="aria-label:a11y.theme;title:a11y.theme">
        {icon("sun-theme", cls="theme-icon", size=19).replace('<svg', '<svg data-theme-icon="sun"', 1)}
        {icon("moon", cls="theme-icon", size=19).replace('<svg', '<svg data-theme-icon="moon"', 1)}
      </button>
      <div class="lang">
        <button class="lang__btn" type="button" data-lang-btn aria-haspopup="true" aria-expanded="false"
                aria-controls="langMenu" aria-label="{T('nav.language')}">
          {icon("globe", size=16)}<span data-lang-current>EN</span>{icon("chev-d", size=14)}
        </button>
        <ul class="lang__menu" id="langMenu" data-lang-menu aria-label="{T('nav.language')}">
          {langs}
        </ul>
      </div>
      <button class="icon-btn cart-btn" type="button" data-cart-open aria-label="{T('cart.title')}" data-empty="true">
        {icon("cart")}<span class="cart-count" data-cart-count>0</span>
      </button>
      <button class="icon-btn burger" type="button" data-nav-open aria-label="{T('nav.menu')}" aria-controls="nav" aria-expanded="false">{icon("menu")}</button>
    </div>
  </div>
</header>
<div class="scrim" data-scrim data-open="false"></div>
'''


def marquee():
    items = [
        ("Women-led", "ಮಹಿಳೆಯರ ನೇತೃತ್ವ", "महिलाओं का नेतृत्व"),
        ("Farm-direct", "ರೈತರಿಂದ ನೇರ", "सीधे खेत से"),
        ("No preservatives", "ಸಂರಕ್ಷಕಗಳಿಲ್ಲ", "प्रिज़र्वेटिव रहित"),
        ("Made in Karnataka", "ಕರ್ನಾಟಕದಲ್ಲಿ ತಯಾರಾಗಿದೆ", "कर्नाटक में बना"),
        ("6% to children's education", "6% ಶಿಕ್ಷಣಕ್ಕೆ", "6% शिक्षा में"),
        ("Small batch · Tue & Fri", "ಸಣ್ಣ ಬ್ಯಾಚ್", "छोटा बैच"),
        ("Paid in 7 days to farmers", "ರೈತರಿಗೆ 7 ದಿನಗಳಲ್ಲಿ ಪಾವತಿ", "किसानों को 7 दिन में भुगतान"),
    ]
    spans = "".join(f'<span class="marquee__item">{t[0]}</span>' for t in items)
    return f'<div class="marquee" aria-hidden="true"><div class="marquee__track">{spans}{spans}</div></div>'


def footer(u):
    shop_links = "".join(f'<li><a href="{u(route("shop") + "?cat=" + c["id"])}">{E(c["label"])}</a></li>' for c in live_categories())
    co_links = [
        ("nav.story", "story"), ("nav.impact", "impact"), ("nav.how", "how"),
        ("nav.blog", "blog"), ("nav.careers", "careers"), ("nav.farmers", "farmers"),
    ]
    company = "".join(f'<li><a href="{u(route(h))}" {A(k)}>{T(k)}</a></li>' for k, h in co_links)
    socials = "".join(
        f'<a href="{s["url"]}" rel="noopener" aria-label="{s["name"]}" target="_blank">{icon(SOCIAL_ICON.get(s["icon"], "globe"))}</a>'
        for s in BRAND["social"])
    addr = BRAND["addresses"][0]
    year = 2026
    return f'''
<footer class="site-footer">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <div class="footer__brand">
          {logo_svg("", "#e3a62b")}
          <span><b>{BRAND["wordmark"]}</b><span>Real Food · True Care · Live More</span></span>
        </div>
        <p {A("footer.pitch")}>{T("footer.pitch")}</p>
        <div class="footer__badges">
          <span class="tag" {A("common.womenled")}>{T("common.womenled")}</span>
          <span class="tag" {A("common.farmdirect")}>{T("common.farmdirect")}</span>
          <span class="tag" {A("common.nopreservative")}>{T("common.nopreservative")}</span>
          <span class="tag">{E(BRAND["reg"]["fssai"])}</span>
        </div>
        <div class="footer__socials mt-3">{socials}</div>
      </div>
      <div>
        <h4 {A("footer.shop")}>{T("footer.shop")}</h4>
        <ul class="footer__list">
          {shop_links}
          <li><a href="{u(route("shop"))}" {A("shop.all")}>{T("shop.all")}</a></li>
          <li><a href="{u(route("shop"))}" {A("con.gifting")}>{T("con.gifting")}</a></li>
        </ul>
      </div>
      <div>
        <h4 {A("footer.company")}>{T("footer.company")}</h4>
        <ul class="footer__list">{company}</ul>
      </div>
      <div>
        <h4 {A("footer.support")}>{T("footer.support")}</h4>
        <ul class="footer__list">
          <li><a href="tel:{BRAND['phone']}">{icon("phone")} {BRAND["phone_display"]}</a></li>
          <li><a href="mailto:{BRAND['emails']['hello']}">{E(BRAND["emails"]["hello"])}</a></li>
          <li>{E(", ".join(addr["lines"][:2]))}</li>
          <li><a href="{u(route("contact"))}" {A("con.visit")}>{T("con.visit")}</a></li>
          <li><a href="{u(route("contact") + "#csr")}" {A("con.csr")}>{T("con.csr")}</a></li>
          <li><a href="{u(route("contact"))}" {A("footer.returns")}>{T("footer.returns")}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© {year} {E(BRAND["legal"])}. <span {A("footer.rights")}>{T("footer.rights")}</span> <span class="footer__credits">· {E(BRAND["reg"]["gstin"])}</span></span>
      <div class="footer__legal">
        <a href="{u(route("contact"))}" {A("footer.privacy")}>{T("footer.privacy")}</a>
        <a href="{u(route("contact"))}" {A("footer.terms")}>{T("footer.terms")}</a>
        <a href="{u(route("impact"))}" {A("footer.amenu")}>{T("footer.amenu")}</a>
      </div>
    </div>
    <p class="footer__credits" style="padding-bottom:1.4rem" {A("footer.demo")}>{T("footer.demo")}</p>
  </div>
</footer>
{drawer_and_widgets(u)}
'''


def drawer_and_widgets(u):
    wa = BRAND["whatsapp"]
    return f'''
<aside class="drawer" data-drawer data-open="false" aria-label="{T('cart.title')}" role="dialog" aria-modal="false">
  <div class="drawer__head">
    <h3>{icon("cart")} <span {A("cart.title")}>{T("cart.title")}</span></h3>
    <button class="drawer__close" type="button" data-cart-close aria-label="{T('nav.close')}">{icon("close")}</button>
  </div>
  <div class="drawer__body" data-cart-body></div>
  <div class="drawer__foot" data-cart-foot hidden></div>
</aside>
<div class="scrim" data-cart-scrim data-open="false"></div>

<div class="toast-wrap" data-toasts aria-live="polite"></div>

<a class="wa-float" href="https://wa.me/{wa}" target="_blank" rel="noopener" aria-label="{T('a11y.whatsapp')}">{icon("whatsapp")}<span>WhatsApp</span></a>
<button class="to-top" type="button" data-to-top aria-label="{T('a11y.totop')}">{icon("arrow-up")}</button>

<script>window.APNAPAN_BASE = "{u.base}";</script>
<script src="{u('assets/js/data.js')}"></script>
<script src="{u('assets/js/i18n-data.js')}"></script>
<script src="{u('assets/js/i18n.js')}"></script>
<script src="{u('assets/js/app.js')}"></script>
'''


# ---------------------------------------------------------------- components
def section_head(eyebrow_key, title_key, sub_key=None, center=False, light=False, eyebrow_text=None):
    cls = "section-head" + (" section-head--center" if center else "")
    eyebrow = f'<span class="eyebrow{" eyebrow--light" if light else ""}{" eyebrow--center" if center else ""}" {A(eyebrow_key)}>{T(eyebrow_key)}</span>' if eyebrow_key else ""
    sub = f'<p class="lede" {A(sub_key)}>{T(sub_key)}</p>' if sub_key else ""
    return f'''<div class="{cls}">
      {eyebrow}
      <h2 {A(title_key)}>{T(title_key)}</h2>
      {sub}
    </div>'''


def stars(rating, cls="rating"):
    full = int(round(rating))
    s = "".join(icon("star", size=14) if i < full else icon("star-o", size=14) for i in range(5))
    return f'<span class="{cls}">{s}</span>'


def rating_line(p, u):
    return (f'<span class="rating">{icon("star", size=14)}<b>{p["rating"]:.1f}</b> '
            f'<span class="muted">({p["reviews_count"]} <span {A("common.reviews")}>{T("common.reviews")}</span>)</span></span>')


def product_card(p, u, i18n_names=True):
    flags = ""
    if "bestseller" in p["tags"]:
        flags += f'<span class="tag tag--gold" {A("common.bestseller")}>{T("common.bestseller")}</span>'
    if "new" in p["tags"]:
        flags += f'<span class="tag tag--green" {A("common.new")}>{T("common.new")}</span>'
    if p["mrp"] > p["price"]:
        off = round((1 - p["price"] / p["mrp"]) * 100)
        flags += f'<span class="tag tag--terracotta">{off}% <span {A("common.off")}>{T("common.off")}</span></span>'
    name_attrs = ""
    if i18n_names:
        name_attrs = f' data-i18n-alt="{p["slug"]}"'
    return f'''<article class="pcard" data-product-card data-slug="{p["slug"]}"
    data-cat="{p["category"]}" data-price="{p["price"]}" data-rating="{p["rating"]}"
    data-tags="{" ".join(p["tags"])}" data-diet="{"|".join(p["diet"]).lower()}" data-new="{1 if "new" in p["tags"] else 0}">
  <a class="pcard__media" href="{u(product_route(p["slug"]))}" aria-label="{E(p["name"])}">
    <img src="{u(p["img"])}" alt="{E(p["name"])} — {E(p["type"])} by ApnaPan" loading="lazy" width="620" height="1029">
    <span class="pcard__flags">{flags}</span>
  </a>
  <button class="pcard__wish" type="button" data-wish="{p["slug"]}" aria-pressed="false" aria-label="Save {E(p['name'])}">{icon("heart")}</button>
  <div class="pcard__body">
    <span class="pcard__reg">{icon("leaf")} <span {A("common.farmdirect")}>{T("common.farmdirect")}</span> · <span {A(TYPE_KEY.get(p["type"], "")) if TYPE_KEY.get(p["type"]) else ""}>{E(p["type"])}</span></span>
    <h3 class="pcard__title" style="font-size:1.06rem"><a href="{u(product_route(p["slug"]))}" data-pname="{p["slug"]}">{E(p["name"])}</a></h3>
    {rating_line(p, u)}
    <p class="small muted" style="margin-top:.15rem">{E(p["short"])}</p>
    <p class="pcard__by">{icon("women")} <span><span {A("common.madeby")}>{T("common.madeby")}</span>: <b>{E(p["made_by"]["name"])}</b></span></p>
    <div class="card__foot">
      <span class="price">₹{p["price"]}<s>₹{p["mrp"]}</s><small>/ {E(p["unit"])}</small></span>
    </div>
    <div class="pcard__add">
      <button class="btn btn--sm" type="button" data-add="{p["slug"]}" data-size="0">{icon("cart")} <span {A("common.addcart")}>{T("common.addcart")}</span></button>
    </div>
  </div>
</article>'''


def stat_card(s, light=False):
    return f'''<div class="stat">
      <div class="stat__icon">{icon(s["icon"])}</div>
      <div class="stat__num"><span data-count="{s["value"]}">0</span><span class="suf">{E(s["suffix"])}</span></div>
      <p class="stat__label">{E(s["label"])}</p>
      <p class="stat__sub">{E(s["sub"])}</p>
    </div>'''


def badge_card(b):
    return f'''<div class="badge-trust">{icon(b["icon"])}<div><b>{E(b["title"])}</b><span>{E(b["text"])}</span></div></div>'''


def quote_card(t, img_prefix=""):
    return f'''<figure class="quote">
      <span class="tag tag--outline" style="align-self:flex-start">{E(t["type"])}</span>
      <blockquote>“{E(t["quote"])}”</blockquote>
      <figcaption class="quote__who">
        <img src="{img_prefix}{t["img"]}" alt="{E(t["name"])}" loading="lazy" width="58" height="58">
        <span><b>{E(t["name"])}</b><span>{E(t["role"])}</span></span>
      </figcaption>
    </figure>'''


def faq_block(items, heading_key=None):
    head = f'<h3 class="mb-2">{icon("info")} {T(heading_key)}</h3>' if heading_key else ""
    accs = "".join(f'''<details class="acc"><summary>{E(i["q"])}</summary><div class="acc__body">{E(i["a"])}</div></details>''' for i in items)
    return f'<div>{head}{accs}</div>'


def check_list(items, cls="check-list"):
    return f'<ul class="{cls}">' + "".join(f'<li>{icon("check")}<span>{E(i)}</span></li>' for i in items) + '</ul>'


def newsletter_block(u):
    return f'''<section class="section" id="newsletter">
  <div class="wrap">
    <div class="newsletter reveal">
      <div class="newsletter__inner">
        <div>
          <span class="eyebrow eyebrow--light">Newsletter</span>
          <h2 {A("home.news.title")}>{T("home.news.title")}</h2>
          <p {A("home.news.text")}>{T("home.news.text")}</p>
          <p class="small" style="margin-top:.9rem;color:rgba(253,248,240,.7)">
            {icon("lock", size=14)} We send one email a month. Unsubscribe in one click.</p>
        </div>
        <form data-form="newsletter" novalidate>
          <div class="form-msg form-msg--ok" data-msg="ok" hidden>{icon("check")}<span>You are on the list. The next harvest letter goes out on the 1st.</span></div>
          <label class="field" style="margin-bottom:.7rem">
            <span class="sr-only">Email</span>
            <input class="input" type="email" name="email" required placeholder="your@email.com" autocomplete="email">
            <span class="field__error">Please enter a valid email address.</span>
          </label>
          <div class="btn-row">
            <button class="btn btn--gold" type="submit">{icon("mail")} <span {A("home.news.cta")}>{T("home.news.cta")}</span></button>
            <span class="small" style="color:rgba(253,248,240,.72);align-self:center">No spam. Ever.</span>
          </div>
        </form>
      </div>
    </div>
  </div>
</section>'''


def impact_band(u, title_key="home.impact.title", eyebrow_key="home.impact.eyebrow", sub_key="home.impact.sub"):
    stats = "".join(stat_card(IMPACT[k]) for k in ["farmers", "women", "children", "mandi"])
    return f'''<section class="section section--green" id="impact">
  <div class="wrap">
    {section_head(eyebrow_key, title_key, sub_key, center=True, light=True)}
    <div class="stat-grid mt-4">{stats}</div>
    <div class="btn-row btn-row--center mt-3">
      <a class="btn btn--gold" href="{u(route("impact"))}">{icon("sunrise")} <span {A("imp.report")}>{T("imp.report")}</span></a>
      <a class="btn btn--light" href="{u(route("story"))}">{icon("book")} <span {A("common.story")}>{T("common.story")}</span></a>
    </div>
  </div>
</section>'''


def trust_strip():
    return f'''<section class="trust-strip">
  <div class="wrap trust-strip__inner">
    {''.join(badge_card(b) for b in TRUST_BADGES[:4])}
  </div>
</section>'''


def breadcrumbs(items, u):
    parts = []
    for i, (label, href) in enumerate(items):
        if href:
            parts.append(f'<a href="{u(href)}">{E(label)}</a>{icon("chev-r", size=13)}')
        else:
            parts.append(f'<span aria-current="page">{E(label)}</span>')
    return f'<nav class="wrap breadcrumb" aria-label="Breadcrumb">{"".join(parts)}</nav>'


# ------------------------------------------------------------------ JSON-LD
def ld_org():
    return {
        "@context": "https://schema.org", "@type": "Organization",
        "name": BRAND["name"], "legalName": BRAND["legal"], "url": BRAND["url"],
        "logo": f'{BRAND["url"]}/assets/favicon.svg',
        "slogan": BRAND["tagline"],
        "description": BRAND["pitch"],
        "foundingDate": str(BRAND["founded"]),
        "email": BRAND["emails"]["hello"], "telephone": BRAND["phone"],
        "address": {"@type": "PostalAddress", "streetAddress": BRAND["addresses"][1]["lines"][0],
                    "addressLocality": "Bengaluru", "addressRegion": "Karnataka",
                    "postalCode": "560064", "addressCountry": "IN"},
        "sameAs": [s["url"] for s in BRAND["social"]],
        "knowsAbout": ["farm direct spices", "women led enterprise", "ethical sourcing India", "Karnataka pickles"],
    }


def ld_product(p):
    return {
        "@context": "https://schema.org", "@type": "Product",
        "name": p["name"], "image": f'{BRAND["url"]}/{p["img"]}',
        "description": p["short"], "sku": p["slug"].upper(),
        "brand": {"@type": "Brand", "name": BRAND["name"]},
        "category": p["category"],
        "countryOfOrigin": "IN",
        "offers": {"@type": "Offer", "price": p["price"], "priceCurrency": "INR",
                   "availability": "https://schema.org/InStock", "url": f'{BRAND["url"]}/products/{p["slug"]}.html'},
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": p["rating"], "reviewCount": p["reviews_count"]},
        "review": [{"@type": "Review", "author": {"@type": "Person", "name": r["name"]},
                    "reviewRating": {"@type": "Rating", "ratingValue": r["rating"]}, "reviewBody": r["text"]}
                   for r in p["reviews"][:2]],
        "additionalProperty": [{"@type": "PropertyValue", "name": "Sourced from", "value": p["sourced"]["farmer"] + ", " + p["sourced"]["village"]},
                               {"@type": "PropertyValue", "name": "Made by", "value": p["made_by"]["name"]}],
    }


def ld_faq(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": i["q"],
                            "acceptedAnswer": {"@type": "Answer", "text": i["a"]}} for i in items]}


def ld_breadcrumb(pairs):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n,
                                 "item": f'{BRAND["url"]}/{h}' if h else BRAND["url"]}
                                for i, (n, h) in enumerate(pairs)]}
