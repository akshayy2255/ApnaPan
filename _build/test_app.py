#!/usr/bin/env python3
"""Acceptance tests for dashboard/index.html (auth + dashboard).

  python3 serve.py 8000 --no-open &          # or any static server
  python3 _build/test_app.py [base_url]

Exits non-zero if any check fails.
"""
import sys
import time

from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000").rstrip("/")
URL = BASE + "/dashboard/"
VIEWS = ["impact", "catalogue", "farmer", "trace", "meet", "join"]

seen, failed = [], []


def check(name, ok, detail=""):
    seen.append(name)
    if ok:
        print(f"  PASS  {name}" + (f"  — {detail}" if detail else ""))
    else:
        failed.append(f"{name}  {detail}")
        print(f"  FAIL  {name}  — {detail}")


def no_overflow(p, label):
    return p.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")


with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 1440, "height": 950})
    p = ctx.new_page()
    errors = []
    p.on("pageerror", lambda e: errors.append("pageerror: " + str(e)))
    p.on("console", lambda m: errors.append("console: " + m.text) if m.type == "error" else None)

    print("\n[1] Auth screen")
    reqs = []
    p.on("request", lambda r: reqs.append(r.url))
    p.goto(URL, wait_until="networkidle")
    time.sleep(0.3)
    check("page loads with no errors", not errors, "; ".join(errors[:2]))
    check("no external requests (offline-safe)", reqs == [URL], f"{len(reqs)} request(s): {reqs[1:]}")
    check("auth screen visible, dashboard hidden",
          p.locator("#auth").is_visible() and p.locator("#app").is_hidden())
    check("no horizontal overflow", no_overflow(p, "auth") <= 1, f"{no_overflow(p,'auth')}px")
    check("wordmark shows the logo text", p.locator(".wordmark").inner_text().strip() == "ApnaPan.")
    check("tagline present",
          "FROM FARM" in p.locator(".tagline").inner_text().upper(),
          p.locator(".tagline").inner_text())
    check("theme toggle is on the auth screen", p.locator(".auth__fab").is_visible())

    print("\n[2] Tabs, fields and validation")
    check("sign-in panel is the default",
          p.locator("#tab-signin").get_attribute("aria-selected") == "true"
          and p.locator("#panel-signin").is_visible()
          and p.locator("#panel-signup").is_hidden())
    p.locator("#tab-signup").click()
    time.sleep(0.15)
    flds = p.eval_on_selector_all("#panel-signup [name]", "els => els.map(e => e.name)")
    check("sign-up asks for full name, email, password", flds == ["name", "email", "password"], str(flds))
    check("sign-up panel shown", p.locator("#panel-signup").is_visible() and p.locator("#panel-signin").is_hidden())

    p.locator("#panel-signup button[type=submit]").click()
    time.sleep(0.2)
    errs = p.eval_on_selector_all("#panel-signup .err:not([hidden])", "els => els.map(e => e.textContent.trim())")
    check("empty submit blocked with messages", len(errs) == 3, str(errs))
    check("no account created on invalid submit", p.locator("#app").is_hidden())

    p.fill("#su-name", "Lakshmi Devi")
    p.fill("#su-email", "not-an-email")
    p.fill("#su-pass", "123")
    p.locator("#panel-signup button[type=submit]").click()
    time.sleep(0.2)
    errs = p.eval_on_selector_all("#panel-signup .err:not([hidden])", "els => els.map(e => e.textContent.trim())")
    check("bad email and short password rejected", len(errs) == 2, str(errs))
    check("name error cleared once filled", "name" not in " ".join(errs))

    print("\n[3] Password reveal")
    p.fill("#su-pass", "sunflower")
    p.locator('#su-pass ~ [data-peek], [data-peek="su-pass"]').first.click()
    time.sleep(0.15)
    check("reveal switches the field to text", p.get_attribute("#su-pass", "type") == "text")
    check("reveal button reports its state", p.locator('[data-peek="su-pass"]').get_attribute("aria-pressed") == "true")

    print("\n[4] Demo account goes straight to the dashboard")
    p.locator("#panel-signup [data-demo]").click()
    time.sleep(0.4)
    check("dashboard shown, auth hidden",
          p.locator("#app").is_visible() and p.locator("#auth").is_hidden())
    check("lands on the Impact Dashboard by default",
          p.locator("#page-title").inner_text() == "Impact Dashboard"
          and p.locator('[data-view="impact"]').is_visible())
    check("no errors during sign-in", not errors, "; ".join(errors[:2]))

    print("\n[5] Sidebar, top bar and sections")
    nav = p.eval_on_selector_all(".nav__item b", "els => els.map(e => e.textContent.trim())")
    check("sidebar lists all six sections",
          nav == ["Impact Dashboard", "Product Catalogue", "Know Your Farmer", "Trace Your Product",
                  "Meet Our ApnaPan", "Become an ApnaPan"], str(nav))
    check("sidebar has a sign-out button", p.locator(".side [data-signout]").is_visible())
    check("top bar has the theme toggle", p.locator(".topbar [data-theme-toggle]").is_visible())
    check("top bar has the user avatar", p.locator("[data-user-btn]").is_visible())
    check("avatar shows demo initials", p.locator("[data-user-btn]").inner_text().strip() == "LD",
          p.locator("[data-user-btn]").inner_text().strip())

    for v in VIEWS[1:]:
        p.locator(f'.nav__item[data-route="{v}"]').click()
        time.sleep(0.25)
        title = p.locator("#page-title").inner_text()
        shown = p.locator(f'[data-view="{v}"]').is_visible()
        others = p.eval_on_selector_all(".view", "els => els.filter(e => !e.hidden).length")
        check(f"{v}: shows only its own view", shown and others == 1, f"visible views={others}, title={title!r}")
        check(f"{v}: sidebar marks it current",
              p.locator(f'.nav__item[data-route="{v}"]').get_attribute("aria-current") == "page")
        check(f"{v}: hash deep-links", p.evaluate("location.hash") == f"#/{v}", p.evaluate("location.hash"))

    print("\n[6] Impact Dashboard content")
    p.locator('.nav__item[data-route="impact"]').click()
    time.sleep(0.25)
    stats = p.eval_on_selector_all(".stat", "els => els.map(e => e.innerText.replace(/\\n/g, ' | '))")
    check("four stat cards", len(stats) >= 4, f"{len(stats)} cards")
    nums = p.eval_on_selector_all("[data-stats] .stat__num", "els => els.map(e => e.textContent.trim())")
    check("stats show the brand numbers 128 / 480+ / 216 / 1",
          [n.split("+")[0] for n in nums] == ["128", "480", "216", "1"], str(nums))
    labels = p.eval_on_selector_all("[data-stats] .stat__label", "els => els.map(e => e.textContent.trim())")
    check("stat labels match the brief",
          labels == ["Women Employed", "Farmers Partnered", "Children Supported", "Processing Units"], str(labels))
    check("stat cards alternate terracotta / olive",
          p.eval_on_selector_all("[data-stats] .stat", "els => els.map(e => e.className.includes('terra') ? 'terra' : 'olive')")
          == ["terra", "olive", "terra", "olive"])
    growth = p.eval_on_selector_all(".growth__k", "els => els.map(e => e.textContent.trim())")
    check("growth timeline has Year 1 / Year 3 / Long-term", growth == ["Year 1", "Year 3", "Long-term"], str(growth))
    check("allocation chart has segments and a legend",
          p.locator(".alloc__seg").count() == 6 and p.locator(".alloc__legend div").count() == 6)
    check("education-fund panel is present", p.locator("[data-fund] .stat").count() >= 3)

    print("\n[7] Product catalogue")
    p.locator('.nav__item[data-route="catalogue"]').click()
    time.sleep(0.25)
    cards = p.locator("[data-products] .pcard")
    check("eight product cards", cards.count() == 8, str(cards.count()))
    names = p.eval_on_selector_all("[data-products] h3", "els => els.map(e => e.textContent.trim())")
    check("names come from the brand's real SKUs",
          "Bisibelebath Masala" in names and "Nellikai Pickle" in names and "Akki Rotti Mix" in names, str(names[:3]))
    check("prices shown as rupees", all("₹" in t for t in
          p.eval_on_selector_all("[data-products] .pcard__price", "els => els.map(e => e.textContent)")))
    check("each card names its maker and farmer",
          p.locator("[data-products] .pcard__meta").count() == 8
          and "Shivamma B." in p.locator("[data-products]").inner_text())

    print("\n[8] Know Your Farmer + Meet Our ApnaPan")
    p.locator('.nav__item[data-route="farmer"]').click()
    time.sleep(0.25)
    check("eight farmer cards", p.locator("[data-farmers] .person").count() == 8)
    check("farmer cards carry place and crop",
          "Byadagi" in p.locator("[data-farmers]").inner_text()
          and "Byadagi chilli" in p.locator("[data-farmers]").inner_text())
    p.locator('.nav__item[data-route="meet"]').click()
    time.sleep(0.25)
    check("maker cards present", p.locator("[data-makers] .person").count() >= 9,
          str(p.locator("[data-makers] .person").count()))

    print("\n[9] Trace Your Product")
    p.locator('.nav__item[data-route="trace"]').click()
    time.sleep(0.25)
    check("empty state shown before a search", p.locator("[data-trace-empty]").is_visible())
    p.fill("#batch", "AP-2609-BB-0142")
    p.locator("[data-trace-form] button[type=submit]").click()
    time.sleep(0.3)
    check("known batch renders the journey",
          p.locator("[data-trace-out]").is_visible() and p.locator("[data-trace-steps] li").count() == 6)
    check("batch header names product and code",
          "Bisibelebath Masala" in p.locator("[data-trace-title]").inner_text()
          and "AP-2609-BB-0142" in p.locator("[data-trace-title]").inner_text(),
          p.locator("[data-trace-title]").inner_text())
    meta = p.locator("[data-trace-meta]").inner_text()
    check("record lists farmer, maker, packer and line",
          all(k in meta for k in ["Farmer", "Made by", "Packed", "Line", "Best before"]))
    check("sample chips work", p.locator("[data-sample]").count() == 4)
    p.locator('[data-sample="AP-2608-NP-0076"]').click()
    time.sleep(0.3)
    check("sample chip loads that batch",
          "Nellikai Pickle" in p.locator("[data-trace-title]").inner_text(),
          p.locator("[data-trace-title]").inner_text())
    p.fill("#batch", "NOPE-123")
    p.locator("[data-trace-form] button[type=submit]").click()
    time.sleep(0.3)
    check("unknown code falls back to the empty state with the code echoed",
          p.locator("[data-trace-empty]").is_visible()
          and "NOPE-123" in p.locator("[data-trace-empty]").inner_text())
    p.locator('.nav__item[data-route="catalogue"]').click()
    time.sleep(0.25)
    p.locator("[data-trace-product]").first.click()
    time.sleep(0.35)
    check("catalogue Trace button opens the trace view with a batch loaded",
          p.locator('[data-view="trace"]').is_visible() and p.locator("[data-trace-out]").is_visible(),
          p.locator("[data-trace-title]").inner_text())

    print("\n[10] Become an ApnaPan form")
    p.locator('.nav__item[data-route="join"]').click()
    time.sleep(0.25)
    p.locator("[data-join-form] button[type=submit]").click()
    time.sleep(0.2)
    check("empty submit is blocked", p.locator("[data-join-form] .err:not([hidden])").count() == 2)
    p.fill("#j-name", "Rudrappa H.")
    p.fill("#j-phone", "9845012345")
    p.locator("[data-join-form] button[type=submit]").click()
    time.sleep(0.3)
    check("valid submit shows a toast", p.locator(".toast").count() >= 1,
          p.locator(".toast").first.inner_text() if p.locator(".toast").count() else "")
    check("form resets after submit", p.input_value("#j-name") == "")

    print("\n[11] Dark / light mode")
    start = p.evaluate("document.documentElement.dataset.theme")
    p.locator(".topbar [data-theme-toggle]").click()
    time.sleep(0.25)
    toggled = p.evaluate("document.documentElement.dataset.theme")
    check("toggle flips data-theme", start != toggled, f"{start} -> {toggled}")
    check("preference persisted", p.evaluate("localStorage.getItem('apnapan_theme')") == toggled)
    check("aria-pressed reflects state",
          p.locator(".topbar [data-theme-toggle]").get_attribute("aria-pressed") == ("true" if toggled == "dark" else "false"))
    bg = p.evaluate("getComputedStyle(document.body).backgroundColor")
    check("dark mode paints the espresso background", toggled == "light" or bg != "rgb(247, 243, 236)", bg)
    p.reload(wait_until="networkidle")
    time.sleep(0.3)
    check("theme survives a reload", p.evaluate("document.documentElement.dataset.theme") == toggled)
    p.locator(".topbar [data-theme-toggle]").click()
    time.sleep(0.2)

    print("\n[12] User menu, sign out, session")
    p.locator("[data-user-btn]").click()
    time.sleep(0.2)
    check("user menu opens", p.locator("[data-user-pop]").is_visible())
    p.keyboard.press("Escape")
    time.sleep(0.2)
    check("Escape closes the user menu", p.locator("[data-user-pop]").is_hidden())
    p.reload(wait_until="networkidle")
    time.sleep(0.3)
    check("session survives a reload", p.locator("#app").is_visible() and p.locator("#auth").is_hidden())
    p.locator(".side [data-signout]").click()
    time.sleep(0.35)
    check("sign out returns to the auth screen",
          p.locator("#auth").is_visible() and p.locator("#app").is_hidden())
    check("session cleared", p.evaluate("localStorage.getItem('apnapan_session_v1')") is None)
    p.reload(wait_until="networkidle")
    time.sleep(0.3)
    check("still signed out after reload", p.locator("#auth").is_visible())

    print("\n[13] Keyboard access")
    p.goto(URL, wait_until="networkidle")
    p.keyboard.press("Tab")
    check("first Tab reaches the skip link", "Skip to content" in p.evaluate("document.activeElement.textContent"),
          p.evaluate("document.activeElement.textContent")[:40])
    p.locator("#si-email").focus()
    p.keyboard.press("Tab")
    check("Tab from email reaches the password row", p.evaluate("document.activeElement.id") in ("si-pass", "si-pass"),
          p.evaluate("document.activeElement.id"))
    p.locator('[data-peek="si-pass"]').focus()
    p.keyboard.press("Enter")
    time.sleep(0.2)
    check("reveal works from the keyboard", p.get_attribute("#si-pass", "type") == "text")

    print("\n[14] Mobile (390x844)")
    m = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True).new_page()
    merr = []
    m.on("pageerror", lambda e: merr.append(str(e)))
    m.goto(URL, wait_until="networkidle")
    time.sleep(0.3)
    check("auth fits the phone with no side scroll", no_overflow(m, "mobile auth") <= 1, f"{no_overflow(m,'mobile auth')}px")
    check("demo button is reachable", m.locator("[data-demo]").first.is_visible())
    m.locator("[data-demo]").first.click()
    time.sleep(0.4)
    check("dashboard loads on mobile", m.locator("#app").is_visible())
    check("no overflow on the dashboard", no_overflow(m, "mobile app") <= 1, f"{no_overflow(m,'mobile app')}px")
    check("sidebar is off-canvas at this width", m.locator("#side").get_attribute("data-open") != "true")
    check("top bar shows the menu button", m.locator("[data-side-open]").is_visible())
    m.locator("[data-side-open]").click()
    time.sleep(0.35)
    check("drawer opens", m.locator("#side").get_attribute("data-open") == "true")
    check("scrim shown with the drawer", m.locator("[data-scrim]").get_attribute("data-open") == "true")
    check("drawer exposes all six sections", m.locator("#side .nav__item").count() == 6)
    m.locator('.nav__item[data-route="farmer"]').click()
    time.sleep(0.35)
    check("choosing a section closes the drawer", m.locator("#side").get_attribute("data-open") != "true")
    check("and switches the view", m.locator('[data-view="farmer"]').is_visible())
    check("no overflow after navigating", no_overflow(m, "mobile app 2") <= 1)
    check("no mobile page errors", not merr, "; ".join(merr[:2]))

    print("\n[15] Storage blocked (sandboxed preview / private mode)")
    b2 = b.new_context(viewport={"width": 1280, "height": 900})
    b2.add_init_script("""
      const boom = () => { throw new DOMException('denied', 'SecurityError'); };
      Object.defineProperty(window, 'localStorage', {get: boom});
      Object.defineProperty(window, 'sessionStorage', {get: boom});
    """)
    p2 = b2.new_page()
    serr = []
    p2.on("pageerror", lambda e: serr.append(str(e)))
    p2.goto(URL, wait_until="networkidle")
    time.sleep(0.3)
    check("auth screen still renders", p2.locator("#auth").is_visible())
    p2.locator("[data-demo]").first.click()
    time.sleep(0.4)
    check("demo sign-in works without storage", p2.locator("#app").is_visible())
    p2.locator('.nav__item[data-route="catalogue"]').click()
    time.sleep(0.25)
    check("navigation works without storage", p2.locator('[data-view="catalogue"]').is_visible())
    p2.locator(".topbar [data-theme-toggle]").click()
    time.sleep(0.2)
    check("theme toggle works without storage",
          p2.evaluate("document.documentElement.dataset.theme") == "dark")
    check("no page errors with storage blocked", not serr, "; ".join(serr[:2]))

    print("\n[16] Deep link + sign out / sign in round trip")
    p3 = b.new_context(viewport={"width": 1280, "height": 900}).new_page()
    p3.goto(URL + "#/meet", wait_until="networkidle")
    time.sleep(0.3)
    check("signed-out deep link shows auth first", p3.locator("#auth").is_visible())
    p3.locator("[data-demo]").first.click()
    time.sleep(0.4)
    check("after sign-in the deep link is honoured",
          p3.locator('[data-view="meet"]').is_visible() and p3.locator("#page-title").inner_text() == "Meet Our ApnaPan",
          p3.locator("#page-title").inner_text())
    p3.locator(".side [data-signout]").click()
    time.sleep(0.3)
    p3.fill("#si-email", "savithramma@example.com")
    p3.fill("#si-pass", "coriander")
    p3.locator("#panel-signin button[type=submit]").click()
    time.sleep(0.4)
    check("real sign-in works", p3.locator("#app").is_visible())
    check("email-derived name used for the avatar",
          p3.locator("[data-user-btn]").inner_text().strip() == "S",
          p3.locator("[data-user-btn]").inner_text().strip())

    print("\n[17] Dashboard data cannot drift from the website content")
    import json, os, re, sys as _sys
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _sys.path.insert(0, os.path.join(_root, "_build"))
    import app_data  # noqa: E402  (_build/app_data.py)
    page = open(os.path.join(_root, "dashboard", "index.html"), encoding="utf-8").read()
    m = re.search(r"var DATA = (\{.*?\n  \});", page, re.S)
    check("data block found in the page", bool(m))
    if m:
        inline = json.loads(m.group(1))
        truth = app_data.build_data()
        drift = [k for k in truth if inline.get(k) != truth[k]]
        check("embedded data still equals _build/content.py (run _build/app_data.py after editing it)",
              not drift, f"drifted: {drift}" if drift else f"{len(truth)} groups verified")
        check("eight products, eight farmers, eight makers carried over",
              len(inline["products"]) == 8 and len(inline["farmers"]) == 8 and len(inline["makers"]) == 8)
        check("impact figures agree with the site's own numbers",
              inline["impact"]["women"]["value"] == 128
              and inline["impact"]["farmers"]["value"] == 480
              and inline["impact"]["children"]["value"] == 216)

    b.close()

print("\n" + "=" * 64)
print(f"  {len(seen) - len(failed)}/{len(seen)} checks passed")
if failed:
    print(f"  {len(failed)} FAILED:")
    for f in failed:
        print("   -", f)
print("=" * 64)
sys.exit(1 if failed else 0)
