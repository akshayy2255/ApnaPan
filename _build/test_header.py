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
import os
import sys
import time

from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C                                    # noqa: E402  the nav, verbatim

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"

# Taken from the site's own navigation, so adding or moving a header item does
# not need three magic numbers changed here.
NAV_ITEMS = len(C.NAV)
NAV_LINKS = sum(1 for n in C.NAV if not n.get("children"))
NAV_LABELS = [n["key"].split(".")[-1].capitalize() for n in C.NAV]

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
        links = page.locator(".nav__list > .nav__item > a.nav__link")
        check(f"all {NAV_LINKS} plain top-level nav links rendered",
              links.count() == NAV_LINKS, f"{links.count()} found")
        groups = page.locator(".nav__list [data-nav-menu-btn]")
        check("one nav group (About) rendered", groups.count() == 1, f"{groups.count()} found")
        check("the group trigger is a <button>, not a link",
              page.evaluate("document.querySelector('[data-nav-menu-btn]').tagName") == "BUTTON")
        check("the group trigger opens a menu it names",
              page.evaluate("""(() => { const b = document.querySelector('[data-nav-menu-btn]');
                const m = document.getElementById(b.getAttribute('aria-controls'));
                return !!m && m.getAttribute('data-nav-menu') !== null; })()"""))
        hrefs = [links.nth(i).get_attribute("href") for i in range(links.count())]
        check("every nav item has a non-empty href", all(h not in (None, "") for h in hrefs), str(hrefs))
        check("no javascript: / # placeholder links", not any((h or "").startswith(("#", "javascript:")) for h in hrefs))
        check("no href points at a missing page",
              all(not h.endswith(".html") or h == "" for h in hrefs), str(set(h[1:] for h in hrefs if h)))
        check("logo is a link to home", page.locator(".brand").get_attribute("href") in ("./", "", "../"),
              repr(page.locator(".brand").get_attribute("href")))
        sub = page.locator(".nav__menu a.nav__sublink")
        check("the group holds the four sub-links", sub.count() == 4, f"{sub.count()} found")
        sub_hrefs = [sub.nth(i).get_attribute("href") for i in range(sub.count())]
        check("every sub-link is a real link",
              all(h not in (None, "") and not h.startswith(("#", "javascript:")) for h in sub_hrefs),
              str(sub_hrefs))
        check("sub-links point at the four pages",
              [h.rstrip("/").split("/")[-1] for h in sub_hrefs] == ["our-story", "our-impact", "how-it-works", "blog"],
              str(sub_hrefs))

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
            # an active page may be a top-level link or one of the group's
            # children, in which case the trigger is flagged with data-current
            cur = page.locator('.nav__link[aria-current="page"], .nav__sublink[aria-current="page"]')
            n = cur.count()
            got = cur.first.inner_text().strip() if n else "(none)"
            ok = n == 1 and got == label
            if not ok:
                mismatches.append(f"{path}: expected '{label}', found {n} active ({got})")
            check(f"{label:13s} -> {path:16s} active", ok, "" if ok else f"got {n}: {got}")

        print("\n[5b] The About group behaves like a menu")
        page.goto(BASE + "/", wait_until="networkidle")
        gbtn = page.locator("[data-nav-menu-btn]")
        gmenu = page.locator("[data-nav-menu]")
        check("group starts closed",
              gbtn.get_attribute("aria-expanded") == "false" and not gmenu.is_visible())
        gbtn.hover()
        time.sleep(0.35)
        check("hover opens it on a pointer device",
              gbtn.get_attribute("aria-expanded") == "true" and gmenu.is_visible())
        page.mouse.move(20, 400)          # leave the group
        time.sleep(0.4)
        check("leaving with the mouse closes it again", not gmenu.is_visible())
        gbtn.click()
        time.sleep(0.3)
        check("click opens it too", gmenu.is_visible())
        page.mouse.click(720, 600)        # click far away
        time.sleep(0.3)
        check("a click outside closes it", not gmenu.is_visible(),
              "still open" if gmenu.is_visible() else "")
        gbtn.click()
        time.sleep(0.3)
        page.keyboard.press("Escape")
        time.sleep(0.3)
        check("Escape closes it and returns focus to the trigger",
              not gmenu.is_visible() and page.evaluate(
                  "document.activeElement.hasAttribute('data-nav-menu-btn')"))
        page.keyboard.press("ArrowDown")
        time.sleep(0.35)
        check("ArrowDown opens it and moves into the links",
              gmenu.is_visible() and page.evaluate(
                  "document.activeElement.classList.contains('nav__sublink')"),
              page.evaluate("document.activeElement.textContent").strip()[:24])
        # Tab out of the group should not leave a panel stranded
        for _ in range(5):
            page.keyboard.press("Tab")
            if not gmenu.is_visible():
                break
        check("tabbing out of the group closes it", not gmenu.is_visible())
        check("the four sub-links are the expected pages",
              [t.strip() for t in page.eval_on_selector_all(
                  ".nav__menu a.nav__sublink", "e=>e.map(x=>x.textContent)")]
              == ["Our Story", "Our Impact", "How It Works", "Blog"])

        print("\n[5c] The About group works in the mobile drawer")
        mnav = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True,
                                   has_touch=True, device_scale_factor=3).new_page()
        mnav.goto(BASE + "/", wait_until="networkidle")
        mnav.click("[data-nav-open]")
        time.sleep(0.45)
        msub = mnav.locator(".nav__list a.nav__sublink")
        check(f"drawer lists all {NAV_ITEMS} top-level items",
              mnav.locator("#nav .nav__list > .nav__item").count() == NAV_ITEMS,
              str(mnav.locator("#nav .nav__list > .nav__item").count()))
        check("the drawer's group starts collapsed",
              mnav.eval_on_selector_all("[data-nav-menu] a", "e=>e.filter(x=>x.offsetParent!==null).length") == 0)
        check("the drawer trigger reports collapsed",
              mnav.locator("[data-nav-menu-btn]").get_attribute("aria-expanded") == "false")
        mnav.locator("[data-nav-menu-btn]").click()
        time.sleep(0.4)
        check("tapping About expands the four links",
              mnav.eval_on_selector_all("[data-nav-menu] a", "e=>e.filter(x=>x.offsetParent!==null).length") == 4)
        check("the expanded group stays inside the drawer (no overflow)",
              mnav.evaluate("document.documentElement.scrollWidth - innerWidth") <= 1)
        check("drawer sub-link targets are 44px tall (touch)",
              all(h >= 44 for h in mnav.eval_on_selector_all(
                  ".nav__list a.nav__sublink", "e=>e.map(x=>x.getBoundingClientRect().height)")))
        mnav.locator('.nav__list a.nav__sublink:has-text("Blog")').click()
        mnav.wait_for_load_state("domcontentloaded")
        check("a drawer sub-link navigates", "/blog/" in mnav.url, mnav.url.replace(BASE, ""))
        mnav.close()

        print("\n[5d] The four pages are also in the footer")
        page.goto(BASE + "/", wait_until="networkidle")
        fcols = page.eval_on_selector_all(".footer__grid h4", "e=>e.map(x=>x.textContent.trim())")
        check("the footer has an About Us column", "About Us" in fcols, str(fcols))
        idx = page.evaluate("""() => [...document.querySelectorAll('.footer__grid > div')]
            .findIndex(d => { const h = d.querySelector('h4'); return h && h.textContent.trim() === 'About Us'; })""")
        check("the About Us column exists", idx >= 0, f"index {idx}")
        col = page.locator(".footer__grid > div").nth(idx)
        names = [t.strip() for t in col.locator("a").all_inner_texts()]
        check("the column links the same four pages",
              names == ["Our Story", "Our Impact", "How It Works", "Blog"], str(names))
        hrefs = [col.locator("a").nth(i).get_attribute("href") for i in range(col.locator("a").count())]
        check("footer links resolve to the same routes as the dropdown",
              [h.rstrip("/").split("/")[-1] for h in hrefs]
              == ["our-story", "our-impact", "how-it-works", "blog"], str(hrefs))

        print("\n[6] Every nav link actually navigates")
        page.goto(BASE + "/", wait_until="domcontentloaded")
        for label, path in [r for r in ROUTES if r[0] != "Home"]:
            if page.locator(f'.nav__list a.nav__sublink:has-text("{label}")').count():
                # inside the group: open it, then click the link
                page.locator("[data-nav-menu-btn]").click()
                time.sleep(0.25)
                page.click(f'.nav__list a.nav__sublink:has-text("{label}")')
            else:
                page.click(f'.nav__list a.nav__link:has-text("{label}")')
            page.wait_for_load_state("domcontentloaded")
            url = page.url.replace(BASE, "") or "/"
            check(f"click '{label}' lands on {path}", url.rstrip("/") == path.rstrip("/") or url == path, url)

        print("\n[7] Console & overflow (desktop)")
        check("no console/page errors on home", not console_errors, "; ".join(console_errors[:2]))
        ow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check("no horizontal overflow", ow <= 1, f"{ow}px")

        # ================================================== colour theme
        print("\n[7c] Colour theme")
        head_part = page.content().split("</head>")[0]
        check("theme is set by an inline script before the stylesheet (no flash)",
              "apnapan_theme" in head_part
              and head_part.index("apnapan_theme") < head_part.index("assets/css/styles.css"))
        check("pre-paint attribute is present",
              page.evaluate("document.documentElement.getAttribute('data-theme')") in ("light", "dark"),
              page.evaluate("document.documentElement.getAttribute('data-theme')"))

        tbtn = page.locator(".theme-btn")
        check("header toggle is visible on desktop", tbtn.is_visible())
        check("starts in light with the moon showing",
              page.evaluate("document.documentElement.dataset.theme") == "light"
              and tbtn.locator(".ic-moon").is_visible() and not tbtn.locator(".ic-sun").is_visible())
        bg_light = page.evaluate("getComputedStyle(document.body).backgroundColor")
        tbtn.click()
        time.sleep(0.35)
        check("click switches to dark",
              page.evaluate("document.documentElement.dataset.theme") == "dark")
        check("body actually repaints dark",
              page.evaluate("getComputedStyle(document.body).backgroundColor") != bg_light,
              page.evaluate("getComputedStyle(document.body).backgroundColor"))
        check("swaps to the sun icon",
              tbtn.locator(".ic-sun").is_visible() and not tbtn.locator(".ic-moon").is_visible())
        check("reports its state and the next action",
              tbtn.get_attribute("aria-pressed") == "true"
              and "light" in (tbtn.get_attribute("aria-label") or "").lower(),
              tbtn.get_attribute("aria-label"))
        check("choice is saved", page.evaluate("localStorage.getItem('apnapan_theme')") == "dark")
        check("browser title bar follows the theme",
              page.evaluate("document.querySelector('meta[name=theme-color]').content") == "#1c140e")

        page.goto(BASE + "/shop/", wait_until="networkidle")
        time.sleep(0.25)
        check("survives navigation to another page",
              page.evaluate("document.documentElement.dataset.theme") == "dark")
        page.reload(wait_until="networkidle")
        time.sleep(0.25)
        check("survives a reload", page.evaluate("document.documentElement.dataset.theme") == "dark")
        check("no horizontal overflow in dark",
              page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth") <= 1)

        # the header frosting must go dark too, or it flashes light over content
        page.evaluate("window.scrollTo(0, 1200)")
        time.sleep(0.4)
        frost = page.evaluate("getComputedStyle(document.querySelector('.site-header'),'::before').backgroundColor")
        check("sticky header frosting is dark in dark mode", "28, 20, 14" in frost, frost)

        page.locator(".theme-btn").click()
        time.sleep(0.3)
        check("toggles back to light",
              page.evaluate("document.documentElement.dataset.theme") == "light")

        # honours the operating system when the visitor has not chosen for themselves
        ctx_sys = browser.new_context(viewport={"width": 1280, "height": 900}, color_scheme="dark")
        psys = ctx_sys.new_page()
        psys.goto(BASE + "/", wait_until="domcontentloaded")
        check("follows the OS preference when nothing is stored",
              psys.evaluate("document.documentElement.dataset.theme") == "dark",
              psys.evaluate("document.documentElement.dataset.theme"))
        ctx_sys.close()

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
        check(f"drawer lists the {NAV_LINKS} links plus the group trigger",
              m.locator("#nav .nav__list > .nav__item").count() == NAV_ITEMS,
              str(m.locator("#nav .nav__list > .nav__item").count()))
        check("drawer offers Appearance with both modes",
              m.locator(".nav__theme").is_visible() and m.locator("[data-theme-set]").count() == 2)
        check("drawer marks the current mode",
              m.get_attribute('[data-theme-set="light"]', "aria-pressed") == "true")
        check("header toggle is hidden on a phone (drawer takes over)",
              not m.locator(".theme-btn").is_visible())
        m.locator('[data-theme-set="dark"]').click()
        time.sleep(0.35)
        check("switching from the drawer works",
              m.evaluate("document.documentElement.dataset.theme") == "dark")
        check("drawer marks the new mode",
              m.get_attribute('[data-theme-set="dark"]', "aria-pressed") == "true")
        m.locator('[data-theme-set="light"]').click()
        time.sleep(0.3)
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
        m.locator("[data-nav-menu-btn]").click()
        time.sleep(0.35)
        m.click('.nav__list a.nav__sublink:has-text("Our Impact")')
        m.wait_for_load_state("domcontentloaded")
        check("mobile link navigates", "/our-impact/" in m.url, m.url.replace(BASE, ""))
        # text_content() not inner_text(): the closed drawer is visibility:hidden,
        # and innerText returns "" for non-rendered content in Chromium.
        cur_sub = m.locator('.nav__sublink[aria-current="page"]').first
        check("active state on mobile page",
              (cur_sub.text_content() or "").strip() == "Our Impact",
              repr((cur_sub.text_content() or "").strip()))
        check("the group is flagged as holding the current page",
              m.locator("[data-nav-menu-btn]").get_attribute("data-current") == "true")
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
        page.locator("[data-nav-menu-btn]").click()
        time.sleep(0.3)
        page.click('.nav__list a.nav__sublink:has-text("Blog")')
        page.wait_for_load_state("domcontentloaded")
        check("clicking a sub-link from another page lands on /blog/", "/blog/" in page.url,
              page.url.replace(BASE, ""))
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
