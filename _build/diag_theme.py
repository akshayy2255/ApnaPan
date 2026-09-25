#!/usr/bin/env python3
"""Contrast audit for dark mode: walks every visible text node, resolves the
effective background behind it, and reports anything below WCAG AA."""
import sys, time
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
THEME = sys.argv[2] if len(sys.argv) > 2 else "dark"
PAGES = ["/", "/shop/", "/products/bisibelebath-masala/", "/our-story/", "/our-impact/",
         "/how-it-works/", "/for-farmers/", "/careers/", "/blog/",
         "/blog/byadagi-chilli-guide/", "/contact/", "/checkout/"]

JS = r"""
() => {
  function lum(c) {
    const [r,g,b] = c.map(v => { v/=255; return v <= .03928 ? v/12.92 : Math.pow((v+.055)/1.055, 2.4); });
    return .2126*r + .7152*g + .0722*b;
  }
  function parse(s) {
    const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(',').map(x => parseFloat(x));
    return {rgb: p.slice(0,3), a: p.length > 3 ? p[3] : 1};
  }
  function bgOf(el) {
    let n = el, stack = [];
    while (n && n !== document.documentElement) {
      const cs = getComputedStyle(n);
      const c = parse(cs.backgroundColor);
      if (c && c.a > 0) { stack.push(c); if (c.a === 1) break; }
      n = n.parentElement;
    }
    let out = [255,255,255];
    for (let i = stack.length-1; i >= 0; i--) {
      const c = stack[i];
      out = out.map((v,k) => c.rgb[k]*c.a + v*(1-c.a));
    }
    return out;
  }
  const bad = [];
  document.querySelectorAll('body *').forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) < .35) return;
    const rect = el.getBoundingClientRect();
    if (rect.width < 2 || rect.height < 2) return;
    if (el.closest('.sr-only,.skip-link,[aria-hidden="true"]')) return;
    if (el.tagName === 'SCRIPT' || el.tagName === 'STYLE') return;
    const txt = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join(' ').trim();
    if (txt.length < 2) return;
    const fg = parse(cs.color); if (!fg) return;
    const bg = bgOf(el);
    const l1 = lum(fg.rgb), l2 = lum(bg);
    const ratio = (Math.max(l1,l2)+.05) / (Math.min(l1,l2)+.05);
    const size = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight) >= 700;
    const large = size >= 24 || (size >= 18.66 && bold);
    const min = large ? 3 : 4.5;
    if (ratio < min) {
      bad.push({ txt: txt.slice(0,42), ratio: +ratio.toFixed(2), min,
                 sel: el.className && typeof el.className === 'string' ? '.' + el.className.split(' ').slice(0,2).join('.') : el.tagName,
                 fg: cs.color, bg: 'rgb(' + bg.map(v=>Math.round(v)).join(',') + ')' });
    }
  });
  return bad;
}
"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 1440, "height": 1000})
    p = ctx.new_page()
    p.goto(BASE + "/", wait_until="domcontentloaded")
    p.evaluate(f"document.documentElement.setAttribute('data-theme-switching','');document.documentElement.setAttribute('data-theme','{THEME}')")
    total, seen = 0, {}
    for path in PAGES:
        p.goto(BASE + path, wait_until="domcontentloaded")
        p.evaluate(f"try{{localStorage.setItem('apnapan_theme','{THEME}')}}catch(e){{}}")
        p.evaluate(f"document.documentElement.setAttribute('data-theme-switching','');document.documentElement.setAttribute('data-theme','{THEME}')")
        time.sleep(0.35)
        bad = p.evaluate(JS)
        total += len(bad)
        for x in bad:
            key = (x['sel'], x['fg'], x['bg'])
            seen.setdefault(key, x)
        print(f"  {path:38s} {len(bad):3d} low-contrast")
    print(f"\n  THEME={THEME}  TOTAL flagged: {total}  (unique element/colour combos: {len(seen)})")
    for x in sorted(seen.values(), key=lambda v: v['ratio'])[:22]:
        print(f"    {x['ratio']:>5} (min {x['min']})  {x['sel'][:34]:34s} {x['fg']:22s} on {x['bg']:18s} \"{x['txt']}\"")
    b.close()
