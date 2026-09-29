#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The "Play explainer" recording path.

The README promises the content team a simple deal: drop a recording at
assets/audio/<scheme>-<lang>.mp3, rebuild, and the card plays it. That promise
is easy to break silently — the card would still render, the button would still
look fine, and nothing would happen. So this test does the whole thing the way
the content team would: it puts a real (silent) recording on disk, rebuilds,
checks what the browser actually does with it, then removes it and rebuilds,
leaving the tree exactly as it found it.

Run the site first (`python3 serve.py 8000 --no-open`), then:

    python3 _build/test_explainer.py [base_url]

Exits non-zero if any check fails.
"""

import os
import shutil
import struct
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
AUDIO = os.path.join(ROOT, "assets", "audio")
BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000").rstrip("/")

# Scheme under test and the language we give it a recording in.
SLUG, LANG = "mudra", "kn"

fails, checks = [], 0


def check(name, ok, detail=""):
    global checks
    checks += 1
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))
    if not ok:
        fails.append(f"{name} {detail}".strip())
    return ok


def section(title):
    print(f"\n{title}")


def silence(path, seconds=1.0):
    """A real, decodable MP3: MPEG-1 Layer III, 128 kbps, 44.1 kHz, mono.

    Zeroed frames decode to silence, which is all a test needs — Chromium plays
    it exactly like a real recording, so the wiring is exercised for real.
    """
    header = bytes([0xFF, 0xFB, 0x90, 0xC0])
    frames = int(seconds * 38.28) or 1
    with open(path, "wb") as fh:
        fh.write((header + b"\x00" * 413) * frames)


def build():
    r = subprocess.run([sys.executable, os.path.join(HERE, "build.py")],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-2000:])
    return r.returncode == 0


def audio_files():
    if not os.path.isdir(AUDIO):
        return []
    return sorted(f for f in os.listdir(AUDIO) if f.endswith(".mp3"))


def main():
    before = audio_files()
    made = os.path.join(AUDIO, f"{SLUG}-{LANG}.mp3")
    os.makedirs(AUDIO, exist_ok=True)
    # If a real recording is already there, keep it and put it back untouched:
    # this test must never cost the content team a file.
    saved = open(made, "rb").read() if os.path.exists(made) else None

    # ---------------------------------------------------------------- setup
    section("[1] The content team drops in a recording")
    silence(made)
    check("a real recording is on disk", os.path.getsize(made) > 1000,
          f"{os.path.getsize(made)} bytes")
    check("the build picks it up", build())

    try:
        # ------------------------------------------------------------ markup
        section("[2] What the pages say afterwards")
        card = open(os.path.join(ROOT, "schemes", SLUG, "index.html"), encoding="utf-8").read()
        other = open(os.path.join(ROOT, "schemes", "odop", "index.html"), encoding="utf-8").read()
        check("the card ships a player", "data-sch-audio controls" in card)
        check("the card knows where recordings live",
              'data-sch-audio-base="../../assets/audio/"' in card)
        check("a scheme with no recording ships no player",
              "data-sch-audio controls" not in other)
        check("the fallback note is still on every card",
              "sch-script-note" in card and "sch-script-note" in other)

        bundle = open(os.path.join(ROOT, "assets", "js", "schemes-data.js"), encoding="utf-8").read()
        check("the bundle tells the app which languages exist",
              f'"audio":["{LANG}"]' in bundle.replace("'", '"'))

        sw = open(os.path.join(ROOT, "sw.js"), encoding="utf-8").read()
        check("the recording is cached for offline use", f"assets/audio/{SLUG}-{LANG}.mp3" in sw)

        # ----------------------------------------------------------- browser
        section("[3] What happens when she taps Play")
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={"width": 400, "height": 860})
            # her phone's own voice, recorded instead of spoken
            ctx.add_init_script("""
              window.__spoken = [];
              const synth = { speaking:false, cancel(){}, speak(u){ window.__spoken.push({text:u.text}); } };
              Object.defineProperty(window, 'speechSynthesis', { value: synth, configurable: true });
              window.SpeechSynthesisUtterance = function (t) { this.text = t; this.lang=''; this.rate=1; };
            """)
            page = ctx.new_page()
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))

            page.goto(f"{BASE}/schemes/{SLUG}/", wait_until="networkidle")
            time.sleep(0.4)

            # her language has no recording -> the phone reads it, and says so
            page.locator("[data-sch-play]").first.click()
            time.sleep(0.5)
            check("in a language with no recording, the phone reads it aloud",
                  len(page.evaluate("window.__spoken")) == 1)
            check("...and the card says that is what happened",
                  not page.eval_on_selector(".sch-script-note", "e=>e.hidden"))
            check("...and no empty player is left sitting there",
                  page.eval_on_selector("[data-sch-audio]", "e=>e.hidden"))

            # switch to the language that has a recording
            page.evaluate(f"window.APNAPAN_setLang('{LANG}')")
            time.sleep(0.7)
            check("switching language shows the recording player",
                  not page.eval_on_selector("[data-sch-audio]", "e=>e.hidden"))
            check("...and stops claiming the phone has to read it",
                  page.eval_on_selector(".sch-script-note", "e=>e.hidden"))

            spoken_before = len(page.evaluate("window.__spoken"))
            page.locator("[data-sch-play]").first.click()
            time.sleep(0.9)
            check("tapping Play plays the recording",
                  page.eval_on_selector("[data-sch-audio]", "e=>!e.paused && e.currentTime > 0"))
            check("...the right file for the language",
                  page.eval_on_selector("[data-sch-audio]",
                                        "e=>(e.currentSrc||e.src||'').split('/').pop()") == f"{SLUG}-{LANG}.mp3")
            check("...and the phone's voice is not used over the top",
                  len(page.evaluate("window.__spoken")) == spoken_before)
            page.locator("[data-sch-play]").first.click()
            time.sleep(0.4)
            check("tapping again stops the recording",
                  page.eval_on_selector("[data-sch-audio]", "e=>e.paused"))
            check("no console errors", not errors, "; ".join(errors[:3]))

            # offline: the recording must still be there
            section("[4] With no network at all")
            ctx2 = browser.new_context(viewport={"width": 400, "height": 860})
            page2 = ctx2.new_page()
            first = page2.goto(f"{BASE}/schemes/{SLUG}/", wait_until="networkidle")
            check("the card loads online first (200)",
                  first is not None and first.status == 200)
            page2.evaluate("navigator.serviceWorker.ready")
            page2.wait_for_timeout(1800)              # let the precache finish
            ctx2.set_offline(True)
            second = page2.reload(wait_until="domcontentloaded")
            time.sleep(0.6)
            check("the card still opens with the network cut",
                  second is not None and second.status == 200
                  and page2.locator("h1").count() == 1)
            check("the recording is stored on the phone",
                  # ask the cache for the exact URL the app will play, resolved
                  # the same way the app resolves it (base lives on <main>)
                  page2.evaluate("""async () => {
                      const base = document.querySelector('[data-sch-app]')
                                           .getAttribute('data-sch-audio-base');
                      const abs = new URL(base + '%s-%s.mp3', location.href).href;
                      return !!(await caches.match(abs, {ignoreSearch:true}));
                  }""" % (SLUG, LANG)))
            browser.close()
    finally:
        # ----------------------------------------------------------- restore
        section("[5] Putting the tree back")
        if saved is not None:
            with open(made, "wb") as fh:      # was here before us: restore it
                fh.write(saved)
        elif os.path.exists(made):
            os.remove(made)
        for f in audio_files():
            if f not in before:
                os.remove(os.path.join(AUDIO, f))
        if not audio_files():
            try:
                os.rmdir(AUDIO)
            except OSError:
                pass
        check("the test recording is gone", audio_files() == before,
              f"left: {audio_files()}")
        check("the site is rebuilt without it", build())
        card = open(os.path.join(ROOT, "schemes", SLUG, "index.html"), encoding="utf-8").read()
        check("...so the card is back to the phone's voice",
              "data-sch-audio controls" not in card)

    print("\n" + "=" * 66)
    if fails:
        print(f"  {checks - len(fails)}/{checks} checks passed")
        print("  failures:")
        for f in fails:
            print("    - " + f)
    else:
        print(f"  {checks}/{checks} checks passed")
    print("=" * 66)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
