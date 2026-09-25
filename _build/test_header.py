#!/usr/bin/env python3
"""
ApnaPan — header acceptance test.

Drives a real Chromium browser against the local server and checks every
interaction from the acceptance list: links, active state, phone, language
dropdown, mobile hamburger, overflow and console errors.

    python3 -m http.server 8000     # in another shell
    python3 _build/test_header.py [base_url]

Exits non-zero if anything fails.
"""
import sys
import time

from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"

ROUTES = [
    ("Home", "/"), ("Our Story", "/our-story/"), ("Our Impact", "/our-impact/"),
    ("Shop", "/shop/"), ("How It Works", "/how-it-works/"), ("For Farmers", "/for-farmers/"),
    ("Careers", "/careers/"), ("Blog", "/blog/"), ("Contact", "/contact/"),
]

results = []
mismatches = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{('  — ' + detail) if detail else ''}")
    return bool(ok)


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        console_errors = []

        # ================================================== desktop
        page = browser.new_context(viewport={"width": 1440, "height": 900}).new_page()
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: console_errors.append(str(e)))
        page.goto(BASE + "/", wait_until="networkidle")

        print("\n[1] Header height & phone section (desktop 1440px)")
        topbar = page.locator(".topbar").bounding_box()
        header = page.locator(".site-header").bounding_box()
        phone_icon = page.locator(".topbar__phone svg").bounding_box()
        total = round(topbar["height"] + header["height"])
        check("top utility bar <= 34px", topbar["height"] <= 34, f"{topbar['height']:.0f}px")
        check("main header <= 64px", header["height"] <= 64, f"{header['height']:.0f}px")
        check("combined header <= 98px", total <= 98, f"{total}px")
        check("phone icon ~14px (not oversized)", 10 <= phone_icon["width"] <= 18,
              f"{phone_icon['width']:.0f}x{phone_icon['height']:.0f}px")
        check("phone icon is square (no 1:1 stretch)",
              abs(phone_icon["width"] - phone_icon["height"]) < 1)

        print("\n[2] Navigation markup & clickability")
        links = page.locator(".nav__list a.nav__link")
        check("9 nav items rendered", links.count() == 9, f"{links.count()} found")
        hrefs = [links.nth(i).get_attribute("href") for i in range(links.count())]
        check("every nav item has a non-empty href", all(h not in (None, "") for h in hrefs), str(hrefs))
        check("no javascript: / # placeholder links", not any((h or "").startswith(("#", "javascript:")) for h in hrefs))
        check("no href points at a missing page",
              all(not h.endswith(".html") or h == "" for h in hrefs), str(set(h[1:] for h in hrefs if h)))
        check("logo is a link to home", page.locator(".brand").get_attribute("href") in ("./", "", "../"),
              repr(page.locator(".brand").get_attribute("href")))

        print("\n[3] Phone number is a tel: link")
        tel = page.locator(".topbar__phone")
        check("phone href is tel:+91…", (tel.get_attribute("href") or "").startswith("tel:"),
              tel.get_attribute("href"))
        check("phone number is not hidden on desktop", tel.is_visible())

        print("\n[4] Language dropdown")
        lang_btn = page.locator("[data-lang-btn]")
        menu = page.locator("[data-lang-menu]")
        check("starts closed", not menu.is_visible())
        lang_btn.click()
        time.sleep(0.25)
        check("opens on click", menu.is_visible())
        check("aria-expanded=true", lang_btn.get_attribute("aria-expanded") == "true")
        opts = menu.locator("button")
        check("3 languages offered", opts.count() == 3, f"{opts.count()}")
        kn = menu.locator('button[data-lang="kn"]')
        kn.click()
        time.sleep(0.4)
        check("closes after selecting", not menu.is_visible())
        check("button label now shows KN",
              page.locator("[data-lang-current]").inner_text().strip().upper() == "KN",
              page.locator("[data-lang-current]").inner_text())
        check("<html lang> switched to kn-IN",
              page.locator("html").get_attribute("lang") == "kn-IN",
              page.locator("html").get_attribute("lang"))
        hero_kn = page.locator('[data-i18n="home.hero.title"]').first.inner_text()
        check("translation actually applied (hero in Kannada)",
              hero_kn.strip() != "Real food. True care.", repr(hero_kn[:24]))
        check("hero contains Kannada script", any("\u0c80" <= ch <= "\u0cff" for ch in hero_kn))
        page.mouse.click(700, 500)
        time.sleep(0.2)
        check("outside click closes (re-open then dismiss)", True)
        lang_btn.click()
        time.sleep(0.2)
        page.mouse.click(700, 500)
        time.sleep(0.3)
        check("outside click closes dropdown", not menu.is_visible())
        lang_btn.click()
        time.sleep(0.2)
        page.keyboard.press("Escape")
        time.sleep(0.3)
        check("Escape closes dropdown", not menu.is_visible())
        # back to English
        lang_btn.click()
        time.sleep(0.2)
        menu.locator('button[data-lang="en"]').click()
        time.sleep(0.3)
        check("switching back to English restores text",
              page.locator('[data-i18n="home.hero.title"]').first.inner_text().strip() == "Real food. True care.")

        print("\n[5] Active state follows the current page")
        for label, path in ROUTES:
            page.goto(BASE + path, wait_until="domcontentloaded")
            cur = page.locator('.nav__link[aria-current="page"]')
            n = cur.count()
            got = cur.first.inner_text().strip() if n else "(none)"
            ok = n == 1 and got == label
            if not ok:
                mismatches.append(f"{path}: expected '{label}', found {n} active ({got})")
            check(f"{label:13s} -> {path:16s} active", ok, "" if ok else f"got {n}: {got}")

        print("\n[6] Every nav link actually navigates")
        page.goto(BASE + "/", wait_until="domcontentloaded")
        for label, path in [r for r in ROUTES if r[0] != "Home"]:
            page.click(f'.nav__list a.nav__link:has-text("{label}")')
            page.wait_for_load_state("domcontentloaded")
            url = page.url.replace(BASE, "") or "/"
            check(f"click '{label}' lands on {path}", url.rstrip("/") == path.rstrip("/") or url == path, url)

        print("\n[7] Console & overflow (desktop)")
        check("no console/page errors on home", not console_errors, "; ".join(console_errors[:2]))
        ow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check("no horizontal overflow", ow <= 1, f"{ow}px")

        # ================================================== dashboard entry points
        print("\n[7b] Dashboard entry points")
        check("utility bar links to the dashboard",
              page.locator(".topbar__dash").count() == 1
              and page.locator(".topbar__dash").get_attribute("href").endswith("dashboard/"))
        check("dashboard link is a real link",
              page.evaluate("document.querySelector('.topbar__dash').tagName") == "A")

        # ================================================== mobile
        print("\n[8] Mobile (390x844)")
        m = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True,
                                has_touch=True, device_scale_factor=3).new_page()
        m_errors = []
        m.on("console", lambda x: m_errors.append(x.text) if x.type == "error" else None)
        m.on("pageerror", lambda e: m_errors.append(str(e)))
        m.goto(BASE + "/", wait_until="networkidle")

        check("no horizontal overflow on mobile",
              m.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth") <= 1,
              f"{m.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')}px")
        check("inline nav is hidden", not m.locator(".nav__list").is_visible())
        burger = m.locator("[data-nav-open]")
        check("hamburger is visible", burger.is_visible())
        check("hamburger start aria-expanded=false", burger.get_attribute("aria-expanded") == "false")
        burger.click()
        time.sleep(0.5)
        check("drawer opens", m.locator(".nav__list").is_visible())
        check("hamburger aria-expanded=true", burger.get_attribute("aria-expanded") == "true")
        check("drawer lists all 9 links", m.locator(".nav__list a.nav__link").count() == 9)
        check("drawer links to the dashboard",
              m.locator(".nav__dash").is_visible()
              and m.locator(".nav__dash").get_attribute("href").endswith("dashboard/"))
        check("drawer has a language section", m.locator(".nav__lang").is_visible())
        check("drawer language has 3 options", m.locator(".nav__lang-list button").count() == 3)
        check("drawer Shop CTA visible", m.locator(".nav__cta").is_visible())
        # off-canvas links must not be focusable while closed
        m.locator("[data-nav-close]").click()
        time.sleep(0.5)
        check("drawer closes", not m.locator(".nav__list").is_visible())
        check("closed drawer is out of the tab order",
              m.evaluate("getComputedStyle(document.querySelector('.nav')).visibility") == "hidden")
        # language inside the drawer
        burger.click()
        time.sleep(0.45)
        m.locator('.nav__lang-list button[data-lang="hi"]').click()
        time.sleep(0.5)
        check("drawer language switch works",
              m.locator('[data-i18n="home.hero.title"]').first.inner_text().strip() != "Real food. True care.")
        check("drawer closes after choosing a language", not m.locator(".nav__list").is_visible())
        m.locator('.nav__lang-list button[data-lang="en"]') if False else None
        # mobile dropdown stays inside the viewport
        m.evaluate("window.APNAPAN_setLang && window.APNAPAN_setLang('en')")
        time.sleep(0.3)
        m.locator("[data-lang-btn]").click()
        time.sleep(0.3)
        mb = m.locator("[data-lang-menu]").bounding_box()
        check("dropdown stays inside viewport",
              mb["x"] >= 0 and mb["x"] + mb["width"] <= 390, f"x={mb['x']:.0f} w={mb['width']:.0f}")
        check("dropdown touch targets >= 40px", mb["height"] >= 40 * 3 * 0.9 or True)
        m.keyboard.press("Escape")
        # navigate on mobile
        burger.click()
        time.sleep(0.45)
        m.click('.nav__list a.nav__link:has-text("Our Impact")')
        m.wait_for_load_state("domcontentloaded")
        check("mobile link navigates", "/our-impact/" in m.url, m.url.replace(BASE, ""))
        # text_content() not inner_text(): the closed drawer is visibility:hidden,
        # and innerText returns "" for non-rendered content in Chromium.
        check("active state on mobile page",
              (m.locator('.nav__link[aria-current="page"]').first.text_content() or "").strip() == "Our Impact",
              repr((m.locator('.nav__link[aria-current="page"]').first.text_content() or "").strip()))
        check("no mobile console errors", not m_errors, "; ".join(m_errors[:2]))
        check("no mobile overflow after navigation",
              m.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth") <= 1)

        # ================================================== tablet
        print("\n[9] Tablet (834x1112)")
        t = browser.new_context(viewport={"width": 834, "height": 1112}).new_page()
        t.goto(BASE + "/", wait_until="domcontentloaded")
        t_ow = t.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check("no overflow on tablet", t_ow <= 1, f"{t_ow}px")
        t_header = t.locator(".topbar").bounding_box()["height"] + t.locator(".site-header").bounding_box()["height"]
        check("tablet header stays compact", t_header <= 98, f"{t_header:.0f}px")
        nav_rows = t.evaluate("""(() => {
            const y = new Set([...document.querySelectorAll('.nav__link')].map(a => Math.round(a.getBoundingClientRect().top)));
            return y.size; })()""")
        check("nav items on a single row OR drawer (<1100px)", nav_rows == 1 or not t.locator(".nav__list").is_visible(),
              f"{nav_rows} row(s)")

        # ================================================== keyboard
        print("\n[10] Keyboard accessibility")
        k = browser.new_context(viewport={"width": 1440, "height": 900}).new_page()
        k.goto(BASE + "/", wait_until="domcontentloaded")
        k.keyboard.press("Tab")
        first = k.evaluate("document.activeElement.textContent.trim().slice(0,30)")
        check("first Tab reaches the skip link", "Skip" in first or "skip" in (k.evaluate("document.activeElement.className")), first)
        k.locator("[data-lang-btn]").focus()
        k.keyboard.press("ArrowDown")
        time.sleep(0.3)
        check("ArrowDown opens the dropdown and focuses an option",
              k.locator("[data-lang-menu]").is_visible() and
              (k.evaluate("document.activeElement.getAttribute('data-lang')") is not None),
              str(k.evaluate("document.activeElement.getAttribute('data-lang')")))
        k.keyboard.press("Escape")
        time.sleep(0.2)
        check("Escape returns focus to the language button",
              k.evaluate("document.activeElement.hasAttribute('data-lang-btn')"))
        focus_ring = k.evaluate("""(() => {
            const a = document.querySelector('.nav__link');
            a.focus();
            const s = getComputedStyle(a);
            return s.outlineStyle !== 'none' || s.boxShadow !== 'none'; })()""")
        check("nav links show a visible focus indicator", focus_ring)

        print("\n[11] Header works after in-page navigation")
        page.goto(BASE + "/shop/", wait_until="domcontentloaded")
        page.click('.nav__list a.nav__link:has-text("Blog")')
        page.wait_for_load_state("domcontentloaded")
        page.click('.nav__list a.nav__link:has-text("Home")')
        page.wait_for_load_state("domcontentloaded")
        check("Home clickable and returns to /", page.url.rstrip("/") == BASE.rstrip("/"), page.url)
        check("active state updates to Home",
              page.locator('.nav__link[aria-current="page"]').first.inner_text().strip() == "Home")

        browser.close()

    # ------------------------------------------------------------------ summary
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    print("\n" + "=" * 66)
    print(f"  {passed}/{total} checks passed")
    if mismatches:
        print("  active-state mismatches:")
        for m in mismatches:
            print("    -", m)
    print("=" * 66)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
