#!/usr/bin/env python3
"""Acceptance tests for the light/dark theme.

  python3 serve.py 8000 --no-open &
  python3 _build/test_theme.py [base_url]

Exits non-zero if any check fails.
"""
import sys
import time

from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000").rstrip("/")
PAGES = ["/", "/shop/", "/products/bisibelebath-masala/", "/our-impact/", "/blog/",
         "/blog/byadagi-chilli-guide/", "/contact/", "/checkout/"]

# ---------------------------------------------------------------------------
# Contrast walker: every visible text node, against the background actually
# painted behind it, at WCAG AA. Same logic as _build/diag_theme.py.
CONTRAST_JS = r"""
() => {
  function lum(c){const[r,g,b]=c.map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*r+.7152*g+.0722*b}
  function parse(s){const m=s.match(/rgba?\(([^)]+)\)/);if(!m)return null;const p=m[1].split(',').map(parseFloat);return{rgb:p.slice(0,3),a:p.length>3?p[3]:1}}
  function bgOf(el){let n=el,stack=[];while(n&&n!==document.documentElement){const c=parse(getComputedStyle(n).backgroundColor);if(c&&c.a>0){stack.push(c);if(c.a===1)break}n=n.parentElement}
    let out=[255,255,255];for(let i=stack.length-1;i>=0;i--){const c=stack[i];out=out.map((v,k)=>c.rgb[k]*c.a+v*(1-c.a))}return out}
  const bad=[];
  document.querySelectorAll('body *').forEach(el=>{
    const cs=getComputedStyle(el);
    if(cs.display==='none'||cs.visibility==='hidden'||parseFloat(cs.opacity)<.35)return;
    const r=el.getBoundingClientRect(); if(r.width<2||r.height<2)return;
    if(el.closest('.sr-only,.skip-link,[aria-hidden="true"]'))return;
    if(el.tagName==='SCRIPT'||el.tagName==='STYLE')return;
    const txt=[...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join(' ').trim();
    if(txt.length<2)return;
    const fg=parse(cs.color); if(!fg)return;
    const bg=bgOf(el), l1=lum(fg.rgb), l2=lum(bg);
    const ratio=(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);
    const size=parseFloat(cs.fontSize), bold=parseInt(cs.fontWeight)>=700;
    const min=(size>=24||(size>=18.66&&bold))?3:4.5;
    if(ratio<min)bad.push({txt:txt.slice(0,40),ratio:+ratio.toFixed(2),
      sel:(el.className&&typeof el.className==='string')?'.'+el.className.split(' ').slice(0,2).join('.'):el.tagName});
  });
  return bad;
}
"""

seen, failed = [], []


def check(name, ok, detail=""):
    seen.append(name)
    if ok:
        print(f"  PASS  {name}" + (f"  — {detail}" if detail else ""))
    else:
        failed.append(f"{name}  {detail}")
        print(f"  FAIL  {name}  — {detail}")


def theme(p):
    return p.evaluate("document.documentElement.getAttribute('data-theme')")


def overflow(p):
    return p.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")


with sync_playwright() as pw:
    b = pw.chromium.launch()
    errors = []

    print("\n[1] Defaults and system preference")
    c = b.new_context(viewport={"width": 1440, "height": 950})
    p = c.new_page()
    p.on("pageerror", lambda e: errors.append(str(e)))
    p.on("console", lambda m: errors.append("console: " + m.text) if m.type == "error" else None)
    p.goto(BASE + "/", wait_until="networkidle")
    check("<html> carries an explicit data-theme", theme(p) in ("light", "dark"), theme(p))
    check("defaults to light with no saved choice and a light OS",
          theme(p) == "light", theme(p))
    c.close()

    for scheme, want in (("dark", "dark"), ("light", "light")):
        c = b.new_context(viewport={"width": 1280, "height": 900}, color_scheme=scheme)
        p = c.new_page()
        p.goto(BASE + "/", wait_until="domcontentloaded")
        check(f"a first visit on a {scheme} OS opens in {want} mode", theme(p) == want, theme(p))
        if scheme == "dark":
            bg = p.evaluate("getComputedStyle(document.body).backgroundColor")
            check("no cream flash: dark background is already painted at first paint",
                  bg != "rgb(253, 248, 240)", bg)
            check("theme-colour meta switched for the browser chrome",
                  p.evaluate("document.getElementById('themeColor').getAttribute('content')") == "#221809",
                  p.evaluate("document.getElementById('themeColor').getAttribute('content')"))
        c.close()

    print("\n[2] The header button")
    c = b.new_context(viewport={"width": 1440, "height": 900})
    p = c.new_page()
    p.on("pageerror", lambda e: errors.append(str(e)))
    p.goto(BASE + "/", wait_until="networkidle")
    btn = p.locator(".theme-btn")
    check("header has one theme button", btn.count() == 1, str(btn.count()))
    check("it is a real <button>", p.evaluate("document.querySelector('.theme-btn').tagName") == "BUTTON")
    check("starts unpressed in light mode", btn.get_attribute("aria-pressed") == "false")
    check("it has a label", bool(btn.get_attribute("aria-label")), btn.get_attribute("aria-label"))
    check("header height unchanged by the new control",
          p.evaluate("document.querySelector('.site-header').offsetHeight") == 59,
          str(p.evaluate("document.querySelector('.site-header').offsetHeight")))
    btn.click()
    time.sleep(0.3)
    check("click switches to dark", theme(p) == "dark", theme(p))
    # The switch must land in one step. Colours on this site animate, so an
    # unguarded switch briefly put light text on the dark page; sample the very
    # first frame after the click and compare it with the settled dark value.
    p.evaluate("document.querySelector('.theme-btn').click()")   # dark -> light
    time.sleep(0.35)
    light_settled = p.evaluate("getComputedStyle(document.querySelector('.nav__link')).color")
    p.evaluate("document.querySelector('.theme-btn').click()")   # light -> dark
    first_frame = p.evaluate("getComputedStyle(document.querySelector('.nav__link')).color")
    time.sleep(0.35)
    dark_settled = p.evaluate("getComputedStyle(document.querySelector('.nav__link')).color")
    check("palette changes in one step, never half-applied",
          first_frame == dark_settled and first_frame != light_settled,
          f"first {first_frame}, settled {dark_settled}, light was {light_settled}")
    check("aria-pressed follows", btn.get_attribute("aria-pressed") == "true")
    check("body paints the dark surface",
          p.evaluate("getComputedStyle(document.body).backgroundColor") == "rgb(34, 24, 9)",
          p.evaluate("getComputedStyle(document.body).backgroundColor"))
    check("preference written to localStorage",
          p.evaluate("localStorage.getItem('apnapan_theme')") == "dark")
    check("no console errors while switching", not errors, "; ".join(errors[:2]))

    p.goto(BASE + "/shop/", wait_until="networkidle")
    check("choice survives navigation", theme(p) == "dark", theme(p))
    p.reload(wait_until="networkidle")
    check("choice survives a reload", theme(p) == "dark", theme(p))
    p.locator(".theme-btn").click()
    time.sleep(0.25)
    check("clicking again returns to light", theme(p) == "light", theme(p))
    c.close()

    print("\n[3] Following the system, until the visitor chooses")
    c = b.new_context(viewport={"width": 1280, "height": 900}, color_scheme="light")
    p = c.new_page()
    p.goto(BASE + "/", wait_until="networkidle")
    p.emulate_media(color_scheme="dark")
    time.sleep(0.4)
    check("system change is followed while nothing is saved", theme(p) == "dark", theme(p))
    p.locator(".theme-btn").click()          # visitor makes a choice
    time.sleep(0.3)
    chosen = theme(p)
    p.emulate_media(color_scheme="light" if chosen == "dark" else "dark")
    time.sleep(0.4)
    check("after an explicit choice the system no longer overrides it", theme(p) == chosen,
          f"chose {chosen}, theme went to {theme(p)}")
    c.close()

    print("\n[4] Where the control lives at each size")
    for w, want_header in ((360, False), (430, False), (480, False), (620, True), (900, True), (1440, True)):
        c = b.new_context(viewport={"width": w, "height": 900}, is_mobile=w < 600)
        p = c.new_page()
        p.goto(BASE + "/", wait_until="domcontentloaded")
        time.sleep(0.2)
        hdr = p.locator(".theme-btn").is_visible()
        check(f"{w}px: header button {'present' if want_header else 'moved to the drawer'}",
              hdr == want_header, f"visible={hdr}")
        if w < 1100:
            p.locator("[data-nav-open]").click()
            time.sleep(0.4)
            check(f"{w}px: drawer offers the theme switch",
                  p.locator(".nav__theme .switch").is_visible())
            check(f"{w}px: switch is a proper role=switch",
                  p.locator(".nav__theme .switch").get_attribute("role") == "switch")
            check(f"{w}px: switch state is exposed",
                  p.locator(".nav__theme .switch").get_attribute("aria-checked") in ("true", "false"))
            p.keyboard.press("Escape")
            time.sleep(0.2)
        check(f"{w}px: no horizontal overflow", overflow(p) <= 1, f"{overflow(p)}px")
        c.close()

    print("\n[5] Drawer switch behaves like a control, not a link")
    c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    p = c.new_page()
    p.on("pageerror", lambda e: errors.append(str(e)))
    p.goto(BASE + "/shop/", wait_until="networkidle")
    start = theme(p)
    p.locator("[data-nav-open]").click()
    time.sleep(0.4)
    p.locator(".nav__theme .switch").click()
    time.sleep(0.35)
    check("switch flips the theme", theme(p) != start, f"{start} -> {theme(p)}")
    check("switch reports its state", p.locator(".nav__theme .switch").get_attribute("aria-checked") == "true")
    check("drawer stays open (it is not a navigation link)",
          p.locator(".nav").get_attribute("data-open") == "true")
    p.keyboard.press("Escape")
    time.sleep(0.3)
    check("Escape still closes the drawer, theme kept", theme(p) == "dark", theme(p))
    check("switch label is translated", p.evaluate(
        "document.querySelector('.nav__theme-title span[data-i18n]').getAttribute('data-i18n')") == "nav.theme")
    c.close()

    print("\n[6] Keyboard")
    c = b.new_context(viewport={"width": 1440, "height": 900})
    p = c.new_page()
    p.goto(BASE + "/", wait_until="networkidle")
    p.locator(".theme-btn").focus()
    time.sleep(0.15)
    check("the button takes focus",
          "theme-btn" in p.evaluate("document.activeElement.className"),
          p.evaluate("document.activeElement.className"))
    check("focus is visible", p.evaluate("getComputedStyle(document.activeElement).outlineStyle") == "solid",
          p.evaluate("getComputedStyle(document.activeElement).outlineStyle"))
    t0 = theme(p)
    p.keyboard.press("Enter")
    time.sleep(0.3)
    t1 = theme(p)
    p.keyboard.press("Space")
    time.sleep(0.3)
    t2 = theme(p)
    check("Enter toggles", t0 != t1, f"{t0} -> {t1}")
    check("Space toggles back", t1 != t2, f"{t1} -> {t2}")
    stops = []
    p.goto(BASE + "/", wait_until="networkidle")
    for _ in range(24):
        p.keyboard.press("Tab")
        stops.append(p.evaluate("(document.activeElement.className || document.activeElement.tagName) + ''"))
    check("the theme button is reachable by Tab", any("theme-btn" in s for s in stops),
          f"{stops.index([s for s in stops if 'theme-btn' in s][0]) + 1}th stop" if any("theme-btn" in s for s in stops) else "never")
    c.close()

    print("\n[7] Nothing else broke while dark is on")
    c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
    p = c.new_page()
    p.on("pageerror", lambda e: errors.append(str(e)))
    p.goto(BASE + "/", wait_until="networkidle")
    p.locator("[data-nav-open]").click()
    time.sleep(0.4)
    p.locator(".nav__theme .switch").click()
    time.sleep(0.35)
    p.keyboard.press("Escape")
    time.sleep(0.25)
    check("theme is dark before the rest of this block", theme(p) == "dark", theme(p))
    p.goto(BASE + "/products/nellikai-pickle/", wait_until="networkidle")
    p.click("[data-add]")
    time.sleep(0.4)
    check("add to cart still works", p.locator("[data-cart-count]").inner_text().strip() == "1",
          p.locator("[data-cart-count]").inner_text())
    p.keyboard.press("Escape")
    time.sleep(0.25)
    p.goto(BASE + "/shop/", wait_until="networkidle")
    # the filter row lives inside a collapsed panel at phone width, so check it
    # where it is actually on screen
    p.set_viewport_size({"width": 1280, "height": 1000})
    time.sleep(0.3)
    chips = p.locator(".chip[aria-pressed]")
    if chips.count() and chips.first.is_visible():
        chips.nth(1).click()
        time.sleep(0.4)
        check("product filters still work", p.locator(".pcard:visible").count() >= 1,
              f"{p.locator('.pcard:visible').count()} cards")
    p.click("[data-lang-btn]")
    time.sleep(0.2)
    p.click('.lang__menu button[data-lang="kn"]')
    time.sleep(0.4)
    check("language switching still works",
          p.evaluate("document.documentElement.getAttribute('data-lang-active')") == "kn",
          p.evaluate("document.documentElement.getAttribute('data-lang-active')"))
    check("theme survives the language switch", theme(p) == "dark", theme(p))
    p.evaluate("window.APNAPAN_setLang && window.APNAPAN_setLang('en')")
    p.goto(BASE + "/checkout/", wait_until="networkidle")
    total = p.locator("[data-co-total]").inner_text() if p.locator("[data-co-total]").count() else ""
    check("checkout still totals the basket", total.startswith("₹") and total != "₹0", total)
    check("no console errors from all of that", not errors, "; ".join(errors[:2]))
    c.close()

    print("\n[8] Storage blocked (sandboxed preview / private mode)")
    c = b.new_context(viewport={"width": 1280, "height": 900})
    c.add_init_script("""
      const boom = () => { throw new DOMException('denied', 'SecurityError'); };
      Object.defineProperty(window, 'localStorage', {get: boom});
      Object.defineProperty(window, 'sessionStorage', {get: boom});
    """)
    p = c.new_page()
    serr = []
    p.on("pageerror", lambda e: serr.append(str(e)))
    p.goto(BASE + "/", wait_until="networkidle")
    check("page renders with storage blocked", p.locator(".theme-btn").is_visible())
    before = theme(p)
    p.locator(".theme-btn").click()
    time.sleep(0.3)
    check("toggle still works", theme(p) != before, f"{before} -> {theme(p)}")
    check("no errors with storage blocked", not serr, "; ".join(serr[:2]))
    c.close()

    print("\n[9] Light mode is untouched, dark mode is readable")
    c = b.new_context(viewport={"width": 1440, "height": 1000})
    p = c.new_page()
    p.goto(BASE + "/", wait_until="domcontentloaded")
    p.evaluate("document.documentElement.setAttribute('data-theme','light')")
    tokens = p.evaluate("""() => {
      const cs = getComputedStyle(document.documentElement), o = {};
      ['cream','ink','terracotta','white','sand','line','green','mustard','ink-mute',
       'terracotta-dark','mustard-dark','clay','clay-soft','sand-deep','line-strong'].forEach(k => o[k] = cs.getPropertyValue('--' + k).trim());
      return o;
    }""")
    original = {"cream": "#fdf8f0", "ink": "#2b211a", "terracotta": "#b4552d", "white": "#fffdf9",
                "sand": "#f6ecdd", "line": "#e5d6c3", "green": "#1e4436", "mustard": "#e3a62b",
                "ink-mute": "#8a7a6c", "terracotta-dark": "#8e3e1d", "mustard-dark": "#bd8317",
                "clay": "#e8cdb8", "clay-soft": "#f3e2d3", "sand-deep": "#eaddc9", "line-strong": "#d6c2a8"}
    changed = [k for k in original if tokens.get(k) != original[k]]
    check("light palette is identical to the original design", not changed,
          f"changed: {changed}" if changed else f"{len(original)} tokens matched")

    total_bad, worst = 0, []
    for path in PAGES:
        p.goto(BASE + path, wait_until="domcontentloaded")
        p.evaluate("try{localStorage.setItem('apnapan_theme','dark')}catch(e){}")
        p.evaluate("document.documentElement.setAttribute('data-theme-switching','');document.documentElement.setAttribute('data-theme','dark')")
        time.sleep(0.3)
        bad = p.evaluate(CONTRAST_JS)
        total_bad += len(bad)
        worst += [(path, x) for x in bad]
        check(f"dark mode: text meets WCAG AA on {path}", not bad,
              "; ".join(f"{x['sel']} {x['ratio']}:1" for x in bad[:2]))
    check("no low-contrast text anywhere in dark mode", total_bad == 0, f"{total_bad} flagged")

    p.goto(BASE + "/", wait_until="domcontentloaded")
    p.evaluate("document.documentElement.setAttribute('data-theme-switching','');document.documentElement.setAttribute('data-theme','dark')")
    p.emulate_media(media="print")
    time.sleep(0.3)
    bg = p.evaluate("getComputedStyle(document.body).backgroundColor")
    check("printing falls back to the light palette", bg == "rgb(255, 255, 255)", bg)
    c.close()

    b.close()

print("\n" + "=" * 64)
print(f"  {len(seen) - len(failed)}/{len(seen)} checks passed")
if failed:
    print(f"  {len(failed)} FAILED:")
    for f in failed:
        print("   -", f)
print("=" * 64)
sys.exit(1 if failed else 0)
