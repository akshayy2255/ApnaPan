#!/usr/bin/env python3
"""Site-wide regression test: every page, both viewports, links, cart and checkout.
Run after any change to routing or asset paths:  python3 _build/test_site.py"""
import sys, time, glob, os, urllib.parse
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
PAGES = ["/", "/our-story/", "/our-impact/", "/shop/", "/how-it-works/", "/for-farmers/",
         "/careers/", "/blog/", "/contact/", "/checkout/", "/404.html"]
_root = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
PAGES += ["/products/" + os.path.basename(os.path.dirname(p)) + "/"
          for p in sorted(glob.glob(os.path.join(_root, "products", "*", "index.html")))]
PAGES += ["/blog/" + s + "/" for s in ("why-we-pay-farmers-above-mandi-price", "inside-the-class-10-fund",
                                       "byadagi-chilli-guide", "mavina-midi-pickle-calendar",
                                       "what-women-led-means-in-a-factory")]

fails, checks = [], 0

def ck(name, ok, detail=""):
    global checks
    checks += 1
    if not ok:
        fails.append(f"{name} {detail}".strip())
        print(f"  FAIL {name} {detail}")
    return ok

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    p = ctx.new_page()
    errs = []
    p.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    p.on("pageerror", lambda e: errs.append(str(e)))

    print("== every page loads, no console errors, no overflow (desktop + mobile) ==")
    for path in PAGES:
        errs.clear()
        r = p.goto(BASE + path, wait_until="networkidle")
        ck(f"{path} status", r.status in (200, 404) and not (r.status == 404 and path != "/404.html"), str(r.status))
        ck(f"{path} console clean", not errs, "; ".join(errs[:1]))
        ow = p.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        ck(f"{path} desktop overflow", ow <= 1, f"{ow}px")
        ck(f"{path} has header nav", p.locator(".nav__list a.nav__link").count() == 9,
           str(p.locator(".nav__list a.nav__link").count()))
        ck(f"{path} has basket button", p.locator("[data-cart-open]").count() == 1)
    print(f"  -> {len(PAGES)} pages checked")

    print("\n== mobile overflow census (390px) ==")
    m = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True).new_page()
    for path in PAGES:
        m.goto(BASE + path, wait_until="domcontentloaded")
        ow = m.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        ck(f"{path} mobile overflow", ow <= 1, f"{ow}px")

    print("\n== internal links resolve (crawled from every page) ==")
    seen, broken = set(), []
    for path in PAGES:
        p.goto(BASE + path, wait_until="domcontentloaded")
        hrefs = p.eval_on_selector_all("a[href]", "els => els.map(e => e.getAttribute('href'))")
        for h in hrefs:
            if not h or h.startswith(("http", "mailto:", "tel:", "#", "javascript:")):
                continue
            target = h.split("#")[0].split("?")[0]
            if not target:
                continue
            full = urllib.parse.urljoin(BASE + path, target)
            if full in seen:
                continue
            seen.add(full)
            try:
                st = p.request.get(full).status
            except Exception as e:
                st = str(e)
            if st >= 400:
                broken.append((path, h, st))
    ck("no broken internal links", not broken, str(broken[:4]))
    print(f"  -> {len(seen)} unique internal link targets checked")

    print("\n== legacy .html redirects still work ==")
    for old, new in [("/shop.html", "/shop/"), ("/story.html", "/our-story/"),
                     ("/products/nellikai-pickle.html", "/products/nellikai-pickle/"),
                     ("/blog.html", "/blog/")]:
        r = p.goto(BASE + old, wait_until="domcontentloaded")
        time.sleep(0.6)
        ck(f"{old} redirects to {new}", new in p.url, p.url.replace(BASE, ""))

    print("\n== cart + checkout after the URL refactor ==")
    p.goto(BASE + "/products/nellikai-pickle/", wait_until="networkidle")
    p.click("[data-add]")
    time.sleep(0.5)
    ck("drawer opens after add", p.locator("[data-drawer]").get_attribute("data-open") == "true")
    ck("cart badge = 1", p.locator("[data-cart-count]").inner_text().strip() == "1",
       p.locator("[data-cart-count]").inner_text())
    img_src = p.eval_on_selector("[data-cart-body] img", "e => e.getAttribute('src')")
    ck("cart thumbnail uses a depth-correct path", img_src.startswith("../../"),
       img_src)
    img_ok = p.evaluate("""() => { const i = document.querySelector('[data-cart-body] img');
        return i && i.complete && i.naturalWidth > 0; }""")
    ck("cart thumbnail actually loads", img_ok)
    p.click("[data-cart-close]")
    time.sleep(0.3)
    p.goto(BASE + "/checkout/", wait_until="networkidle")
    ck("checkout shows the line item", p.locator(".os-line").count() == 1)
    total = p.locator("[data-co-total]").inner_text()
    ck("checkout total is a real amount", total.startswith("₹") and total != "₹0", total)
    p.fill("[name=name]", "Test Buyer")
    p.fill("[name=phone]", "9876543210")
    p.fill("[name=email]", "test@example.com")
    p.fill("[name=address1]", "1 Test Road")
    p.fill("[name=city]", "Bengaluru")
    p.select_option("[name=state]", label="Karnataka")
    p.fill("[name=pincode]", "560064")
    p.click("[data-place-order]")
    time.sleep(1.6)
    ck("order confirmation appears", p.locator("[data-checkout-success]").is_visible())
    ck("order id issued", len(p.locator("[data-order-id]").inner_text().strip()) > 8,
       p.locator("[data-order-id]").inner_text())
    ck("cart cleared after order", p.locator("[data-cart-count]").inner_text().strip() == "0")

    print("\n== language switching is site-wide ==")
    for path in ["/", "/shop/", "/our-impact/", "/products/bisibelebath-masala/", "/careers/"]:
        p.goto(BASE + path, wait_until="domcontentloaded")
        p.evaluate("window.APNAPAN_setLang('kn')")
        time.sleep(0.35)
        kn = p.locator('[data-i18n="common.freeship"]').first.text_content()
        has_kn = any("\u0c80" <= ch <= "\u0cff" for ch in (kn or ""))
        ck(f"{path} switches to Kannada", has_kn, repr((kn or "")[:20]))
        nav_ok = p.locator('.nav__list a.nav__link[href]').count() == 9
        ck(f"{path} nav intact after language switch", nav_ok)
        p.evaluate("window.APNAPAN_setLang('en')")
    b.close()

print("\n" + "=" * 62)
print(f"  {checks - len(fails)}/{checks} checks passed")
if fails:
    print(f"  {len(fails)} FAILURES:")
    for f in fails[:20]:
        print("   -", f)
print("=" * 62)
sys.exit(1 if fails else 0)
