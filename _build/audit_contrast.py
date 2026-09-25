#!/usr/bin/env python3
"""WCAG contrast audit for the colour theme, on every key page and both themes.

    python3 _build/audit_contrast.py [base_url] [--verbose]

Computes the real rendered colour of each text element against its effective
background (walking up the tree until something opaque is found), then reports
anything below AA: 4.5:1 for body text, 3:1 for large text (>=24px, or >=19px
bold). Exits non-zero with --strict.
"""
import sys

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8000"
VERBOSE = "--verbose" in sys.argv
STRICT = "--strict" in sys.argv
for a in sys.argv[1:]:
    if a.startswith("http"):
        BASE = a.rstrip("/")

PAGES = ["/", "/our-story/", "/our-impact/", "/shop/", "/how-it-works/",
         "/for-farmers/", "/careers/", "/blog/", "/contact/", "/checkout/",
         "/products/bisibelebath-masala/", "/products/nellikai-pickle/",
         "/blog/byadagi-chilli-guide/"]

JS = r"""
() => {
  function parse(c) {
    const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(',').map(Number);
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  }
  function over(fg, bg) {   // composite fg (may be translucent) onto bg
    return { r: fg.r*fg.a + bg.r*(1-fg.a), g: fg.g*fg.a + bg.g*(1-fg.a), b: fg.b*fg.a + bg.b*(1-fg.a), a: 1 };
  }
  function bgOf(el) {
    let node = el, acc = null;
    while (node && node.nodeType === 1) {
      const cs = getComputedStyle(node);
      const c = parse(cs.backgroundColor);
      if (c && c.a > 0) {
        if (!acc) acc = c;
        else acc = over(acc, c);
        if (acc.a >= 0.999 || c.a >= 0.999) return acc;
      }
      const bi = cs.backgroundImage;
      if (bi && bi !== 'none' && bi.indexOf('gradient') > -1) {
        const nums = bi.match(/rgba?\([^)]+\)/g) || [];
        for (const n of nums) { const cc = parse(n); if (cc) return over(acc || cc, cc); }
      }
      node = node.parentElement;
    }
    return acc || { r: 255, g: 255, b: 255, a: 1 };
  }
  function lum(c) {
    const f = v => { v /= 255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); };
    return 0.2126*f(c.r) + 0.7152*f(c.g) + 0.0722*f(c.b);
  }
  function ratio(a, b) { const l1 = lum(a), l2 = lum(b); const hi = Math.max(l1,l2), lo = Math.min(l1,l2);
    return (hi + 0.05) / (lo + 0.05); }

  const out = [];
  const els = document.querySelectorAll('p,h1,h2,h3,h4,h5,li,a,span,strong,button,label,td,th,figcaption,dt,dd,blockquote,small,b,em');
  for (const el of els) {
    if (el.closest('[aria-hidden="true"],svg,.sr-only,.skip-link,[data-toasts]')) continue;
    const txt = (el.textContent || '').trim();
    if (!txt || txt.length < 2) continue;
    if (el.children.length && !Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim())) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) < 0.1) continue;
    const fg = parse(cs.color); if (!fg) continue;
    const bg = bgOf(el);
    const col = over(fg, bg);
    const size = parseFloat(cs.fontSize);
    const weight = parseInt(cs.fontWeight, 10) || 400;
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    const need = large ? 3 : 4.5;
    const cr = ratio(col, bg);
    if (cr < need) {
      out.push({ text: txt.slice(0, 52), tag: el.tagName.toLowerCase(),
                 cls: (el.className || '').toString().slice(0, 40),
                 ratio: Math.round(cr * 100) / 100, need, size: Math.round(size),
                 fg: cs.color, bg: `rgb(${Math.round(bg.r)},${Math.round(bg.g)},${Math.round(bg.b)})` });
    }
  }
  return out;
}
"""

fails, checked = [], 0
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for theme in ("light", "dark"):
        ctx = b.new_context(viewport={"width": 1400, "height": 950})
        ctx.add_init_script(f"try{{localStorage.setItem('apnapan_theme','{theme}')}}catch(e){{}}")
        p = ctx.new_page()
        print(f"\n=== {theme.upper()} ===")
        for path in PAGES:
            p.goto(BASE + path, wait_until="networkidle")
            p.wait_for_timeout(120)
            # reveal anything scroll-triggered so nothing is skipped
            p.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-in'))")
            p.wait_for_timeout(150)
            bad = p.evaluate(JS)
            checked += 1
            if bad:
                fails.append((theme, path, bad))
                print(f"  {path}")
                for x in bad:
                    print(f"    {x['ratio']:>5}:1 (need {x['need']}) {x['tag']}.{x['cls'][:26]:26s} "
                          f"{x['fg']} on {x['bg']}  “{x['text']}”")
            elif VERBOSE:
                print(f"  {path}  ok")
        ctx.close()
    b.close()

total = sum(len(f[2]) for f in fails)
print(f"\n{'='*70}")
print(f"  {checked} page loads audited · {total} contrast failures")
print("=" * 70)
if STRICT and total:
    sys.exit(1)
