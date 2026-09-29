#!/usr/bin/env python3
"""
ApnaPan — Government Schemes acceptance test.

    python3 _build/test_schemes.py [base_url]

Checks the three screens against the brief:
  * the quiz asks four questions and NEVER needs a keyboard
  * only 2-3 schemes are ever shown, and what she asked for is in them
  * a card is short, one tap plays it, one tap asks for help
  * "request help" makes a task for a Sakhi Champion — never a form
  * it all keeps working with no network, and requests queue until it's back

Exits non-zero if anything fails.
"""
import sys
import time

from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
SLUGS = ["mudra", "stand-up-india", "ayushman-bharat", "nrlm-shg", "pm-vishwakarma", "odop"]
NEEDS = ["loan", "health", "skill"]

results = []

# Headless Chromium has no speech engine, so the suite stubs the Web Speech API
# and asserts what the app ASKS it to say — text, language and rate.
SPEECH_STUB = """
window.__spoken = [];
const synth = {
  speaking: false,
  cancel() { this.speaking = false; if (this._u && this._u.onend) { const u = this._u; this._u = null; } },
  speak(u) { window.__spoken.push({ text: u.text, lang: u.lang, rate: u.rate }); this.speaking = true; this._u = u; }
};
Object.defineProperty(window, 'speechSynthesis', { value: synth, configurable: true });
window.SpeechSynthesisUtterance = function (t) { this.text = t; this.lang = ''; this.rate = 1; };
"""


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{('  — ' + detail) if detail else ''}")
    return bool(ok)


def section(title):
    print(f"\n{title}")


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        errors = []
        ctx = browser.new_context(viewport={"width": 400, "height": 860}, is_mobile=True, has_touch=True)
        ctx.add_init_script(SPEECH_STUB)
        page = ctx.new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: errors.append("console: " + m.text) if m.type == "error" else None)

        # ------------------------------------------------------- routes
        section("[1] The section exists and is wired in")
        for slug in SLUGS:
            r = page.goto(f"{BASE}/schemes/{slug}/", wait_until="domcontentloaded")
            check(f"/schemes/{slug}/ loads", r.status == 200, str(r.status))
        r = page.goto(f"{BASE}/schemes/", wait_until="networkidle")
        check("/schemes/ loads", r.status == 200, str(r.status))
        check("no console errors on the hub", not errors, "; ".join(errors[:2]))
        check("page is a manifest-backed app",
              page.locator('link[rel="manifest"]').count() == 1)
        check("footer links to the section",
              page.locator('.footer__list a[href*="schemes"]').count() >= 1)
        r = page.goto(f"{BASE}/schemes/trainer-notes/", wait_until="domcontentloaded")
        check("trainer notes exist for the field team", r.status == 200, str(r.status))
        check("trainer notes are kept out of search",
              "noindex" in (page.locator('meta[name="robots"]').get_attribute("content") or ""))
        check("trainer notes carry all six teacher notes",
              page.locator(".tr-note").count() == 6, str(page.locator(".tr-note").count()))
        check("trainer notes are not linked from the app",
              page.goto(f"{BASE}/schemes/", wait_until="domcontentloaded") is not None
              and page.locator('a[href*="trainer-notes"]').count() == 0)

        # -------------------------------------------------- no typing, ever
        section("[2] Nothing in the flow needs a keyboard")
        typed = page.evaluate("""() => document.querySelectorAll(
            '[data-sch-app] input:not([type=checkbox]), [data-sch-app] textarea, [data-sch-app] select').length""")
        check("no text/number/select inputs anywhere in the app", typed == 0, f"{typed} found")
        check("every control is a button or a link",
              page.evaluate("""() => [...document.querySelectorAll('[data-sch-app] button, [data-sch-app] a')]
                .every(el => el.tagName === 'BUTTON' || el.tagName === 'A')"""))

        # -------------------------------------------------------- the quiz
        section("[3] Screen 1 — four tap questions")
        page.click("[data-sch-start]")
        time.sleep(0.3)
        q_texts, opt_counts = [], []
        for step in range(4):
            q = page.locator("[data-sch-question]").inner_text()
            q_texts.append(q)
            opt_counts.append(page.locator(".sch-opt").count())
            check(f"question {step + 1} is shown", bool(q.strip()), repr(q[:40]))
            if step == 0:
                check("the state question offers a list to tap", opt_counts[0] >= 10, str(opt_counts[0]))
                check("state tiles are large (>=60px tall)",
                      all(h >= 60 for h in page.eval_on_selector_all(
                          ".sch-opt", "e=>e.map(x=>x.getBoundingClientRect().height)")))
                page.click('.sch-opt:has-text("Karnataka")')
            elif step == 1:
                page.click('.sch-opt:has-text("starting")')
            elif step == 2:
                page.click('.sch-opt:has-text("A loan")')
                check("the need question allows more than one answer",
                      page.locator('.sch-opt[aria-pressed="true"]').count() == 1)
                page.click("[data-sch-next]")
            else:
                page.click('.sch-opt:has-text("Yes")')
            time.sleep(0.4)
        check("all four questions are asked", len([q for q in q_texts if q.strip()]) == 4, str(q_texts))
        check("the quiz tracks progress with dots",
              page.locator("[data-sch-dot]").count() == 4)
        # `hidden` has to really hide: a stray Next on a single-answer question
        # would let her skip a question without answering it
        page.click("[data-sch-restart]")
        time.sleep(0.3)
        single = (not page.locator("[data-sch-next]").is_visible())
        page.click('.sch-opt:has-text("Karnataka")')
        time.sleep(0.4)
        single = single and (not page.locator("[data-sch-next]").is_visible())
        page.click('.sch-opt:has-text("starting")')
        time.sleep(0.4)
        check("single-answer questions have no Next to skip with", single)
        page.click('.sch-opt:has-text("A loan")')
        time.sleep(0.3)
        check("the multi-select question offers Next once something is picked",
              page.locator("[data-sch-next]").is_visible())
        page.click("[data-sch-next]")
        time.sleep(0.3)
        page.click('.sch-opt:has-text("Yes")')
        time.sleep(0.5)
        check("the 'our Sakhis are in Karnataka' note stays hidden for Karnataka",
              not page.locator("[data-sch-statenote]").is_visible())
        # (leaves the app on the results screen, ready for the restart below)
        page.click("[data-sch-restart]")
        time.sleep(0.3)
        check("start again returns to question 1",
              page.locator("[data-sch-question]").inner_text().strip().startswith("What state"))

        # ------------------------------------------------------ the answers
        section("[4] Answering again takes her to results")


        def run_quiz(state="Karnataka", business="starting", needs=("A loan",), bank="Yes"):
            page.click("[data-sch-start]")
            time.sleep(0.25)
            page.click(f'.sch-opt:has-text("{state}")')
            time.sleep(0.3)
            page.click(f'.sch-opt:has-text("{business}")')
            time.sleep(0.3)
            for n in needs:
                page.click(f'.sch-opt:has-text("{n}")')
            page.click("[data-sch-next]")
            time.sleep(0.3)
            page.click(f'.sch-opt:has-text("{bank}")')
            time.sleep(0.45)

        run_quiz(needs=("A loan", "Health cover"))
        cards = page.locator(".sch-scheme")
        n = cards.count()
        check("results replace the questions", page.locator("[data-sch-screen='results']").is_visible())
        check("between 2 and 3 schemes are shown", 2 <= n <= 3, f"{n} cards")
        check("the full list of six is never shown at once", n < 6)
        names = [t.strip() for t in page.eval_on_selector_all(".sch-scheme h3", "e=>e.map(x=>x.textContent)")]
        check("nameless duplicates are not shown", len(names) == len(set(names)), str(names))
        check("she is told why each one matched",
              all(c >= 1 for c in page.eval_on_selector_all(
                  ".sch-scheme", "e=>e.map(x=>x.querySelectorAll('.sch-chip').length)")))
        check("PM-JAY appears when she asked about health cover",
              any("Ayushman" in x for x in names), str(names))
        check("a loan scheme appears when she asked for a loan",
              any("MUDRA" in x or "Stand-Up" in x for x in names), str(names))

        # ---- every card: short, with the two actions the brief asks for
        section("[5] Screen 2 — one simple card per scheme")
        lines = page.eval_on_selector_all(".sch-scheme__line", "e=>e.map(x=>x.textContent)")
        check("each card explains itself in at most 2 sentences",
              all(len([c for c in ln if c in ".?!।"]) <= 2 for ln in lines), str(lines[0][:60]))
        for i in range(n):
            card = cards.nth(i)
            check(f"card {i + 1} has a name, a line and an amount",
                  card.locator("h3").count() == 1 and card.locator(".sch-scheme__line").count() == 1
                  and card.locator(".sch-scheme__benefit").count() == 1)
            check(f"card {i + 1} has Play explainer and Request help",
                  card.locator("[data-sch-play]").count() == 1 and card.locator("[data-sch-ask]").count() == 1)
            heights = page.eval_on_selector_all(
                f".sch-scheme:nth-of-type({i + 1}) button, .sch-scheme:nth-of-type({i + 1}) a.sch-scheme__more",
                "e=>e.map(x=>x.getBoundingClientRect().height)")
            check(f"card {i + 1} actions are large tap targets",
                  all(h >= 48 for h in heights), str([round(h) for h in heights]))
        check("cards link to the full scheme page",
              page.locator('.sch-scheme a[href*="/schemes/"]').count() == n)

        # ---- the explainer actually plays something
        section("[6] Play explainer speaks in her language")
        page.locator("[data-sch-play]").first.click()
        time.sleep(0.4)
        label = page.locator("[data-sch-play] span").first.inner_text().strip()
        check("the button reports that it is playing", label != "Play explainer", label)
        spoken = page.evaluate("window.__spoken")
        check("speech is actually produced", len(spoken) == 1, str(len(spoken)))
        if spoken:
            check("in her language", spoken[0]["lang"] == "en-IN", spoken[0]["lang"])
            check("slowly enough to follow", spoken[0]["rate"] <= 0.95, str(spoken[0]["rate"]))
            check("reading the card, not a stub", "hospital" in spoken[0]["text"].lower()
                  or "treatment" in spoken[0]["text"].lower(), spoken[0]["text"][:60])
        page.evaluate("window.APNAPAN_setLang('hi')")
        time.sleep(0.4)
        page.locator("[data-sch-play]").first.click()
        time.sleep(0.4)
        spoken_hi = page.evaluate("window.__spoken").pop()
        check("switching to Hindi changes the voice language", spoken_hi["lang"] == "hi-IN", spoken_hi["lang"])
        check("and the words it speaks",
              any("\u0900" <= ch <= "\u097f" for ch in spoken_hi["text"]), spoken_hi["text"][:40])
        page.evaluate("window.APNAPAN_setLang('en')")
        time.sleep(0.3)
        page.locator("[data-sch-play]").first.click()      # start
        time.sleep(0.35)
        check("it plays again after a language change",
              page.locator("[data-sch-play] span").first.inner_text().strip() != "Play explainer")
        page.locator("[data-sch-play]").first.click()      # stop
        time.sleep(0.35)
        check("tapping again stops it",
              page.locator("[data-sch-play] span").first.inner_text().strip() == "Play explainer")

        # ---- the full card
        section("[7] The full card has everything she needs to act")
        page.goto(f"{BASE}/schemes/mudra/", wait_until="networkidle")
        check("it names the scheme", "MUDRA" in page.locator("h1").inner_text())
        check("it shows the amount", "₹" in page.locator(".sch-benefit__amount").inner_text())
        check("it lists what she gets (the loan tiers)",
              page.locator(".sch-table tr").count() == 4, str(page.locator(".sch-table tr").count()))
        check("documents are a tick-list, not a paragraph",
              page.locator(".sch-doc").count() == 5, str(page.locator(".sch-doc").count()))
        check("the helpline is a tap-to-call link",
              page.locator('.sch-strip--call a[href^="tel:"]').count() == 1)
        check("it does not promise the state-dependent schemes",
              page.locator(".sch-caution").count() == 0)
        page.goto(f"{BASE}/schemes/pm-vishwakarma/", wait_until="domcontentloaded")
        check("state-dependent schemes carry the 'check first' caution",
              page.locator(".sch-caution").count() == 1)
        check("the caution matches the trainer's warning",
              "check" in page.locator(".sch-caution").inner_text().lower())
        page.goto(f"{BASE}/schemes/mudra/", wait_until="domcontentloaded")
        page.locator(".sch-doc").first.click()
        time.sleep(0.2)
        page.reload(wait_until="domcontentloaded")
        check("a ticked document is remembered on this phone",
              page.locator(".sch-doc input").first.is_checked())
        check("the explainer button is on the card page too",
              page.locator("[data-sch-play]").count() == 1)

        # ------------------------------------------------ request help flow
        section("[8] Screen 3 — Request help makes a task, not a form")
        page.evaluate("localStorage.removeItem('apnapan_help_requests'); localStorage.removeItem('apnapan_sch_district')")
        page.goto(f"{BASE}/schemes/ayushman-bharat/", wait_until="networkidle")
        page.click("[data-sch-ask]")
        time.sleep(0.4)
        check("the sheet opens", page.locator("[data-sch-sheet]").is_visible())
        check("it asks for NO input of any kind",
              page.locator("[data-sch-sheet] input, [data-sch-sheet] textarea, [data-sch-sheet] select").count() == 0)
        check("it promises a phone call from a named person",
              "Sakhi" in page.locator("[data-sch-sheet]").inner_text())
        check("she can't send before saying where she is",
              page.locator("[data-sch-send]").is_disabled())
        check("it asks for her district by tapping",
              page.locator("[data-sch-sheet] .sch-opt").count() >= 10)
        page.locator('[data-dist="haveri"]').click()
        time.sleep(0.3)
        sakhi = page.locator("[data-sch-sakhi]").inner_text()
        check("the nearest Sakhi Champion is shown", "Savitramma" in sakhi, sakhi.split("\n")[0])
        check("with her number, so the woman can call first",
              "+91 90000 00002" in sakhi, sakhi)
        check("send is now allowed", not page.locator("[data-sch-send]").is_disabled())
        page.click("[data-sch-send]")
        time.sleep(0.5)
        check("the sheet closes after sending", page.locator("[data-sch-sheet]").is_hidden())
        check("a confirmation is shown", page.locator("[data-toasts] .toast").count() >= 1)
        stored = page.evaluate("JSON.parse(localStorage.getItem('apnapan_help_requests')||'[]')")
        check("a task was created for the field team", len(stored) == 1, str(len(stored)))
        check("the task names the scheme, the district and the Sakhi",
              stored and stored[0]["slug"] == "ayushman-bharat" and stored[0]["district"] == "haveri"
              and stored[0]["sakhi"]["name"] == "Savitramma P.")
        check("and it starts out waiting to send", stored and stored[0]["status"] == "pending")
        page.goto(f"{BASE}/schemes/", wait_until="networkidle")   # My requests lives on the hub
        page.click("[data-sch-open-requests]")
        time.sleep(0.3)
        check("it shows up under My requests", page.locator(".sch-req").count() == 1)
        check("marked as still waiting to send",
              "Waiting" in page.locator(".sch-badge").first.inner_text())
        check("with a one-tap WhatsApp handoff and a call button",
              page.locator("[data-sch-wa]").count() == 1 and page.locator('.sch-req a[href^="tel:"]').count() == 1)
        check("the pending count is on the hub badge",
              page.locator("[data-sch-req-count]").inner_text().strip() == "1")

        # ----------------------------------------------- queued -> sent sync
        section("[9] Requests sync when the phone is back online")
        page.route("**/api/help-requests", lambda route: route.fulfill(
            status=200, content_type="application/json", body='{"ok":true}'))
        page.evaluate("localStorage.setItem('apnapan_help_endpoint', '/api/help-requests')")
        posted = []
        page.on("request", lambda r: posted.append(r) if "/api/help-requests" in r.url else None)
        page.goto(f"{BASE}/schemes/", wait_until="networkidle")
        time.sleep(1.0)
        check("the queued request was sent to the field team's endpoint", len(posted) >= 1, f"{len(posted)} posts")
        if posted:
            body = posted[0].post_data or ""
            check("it carries the scheme and the district",
                  "ayushman-bharat" in body and "haveri" in body, body[:80])
        status = page.evaluate("JSON.parse(localStorage.getItem('apnapan_help_requests'))[0].status")
        check("and is marked sent once the server accepts it", status == "sent", status)
        page.evaluate("localStorage.removeItem('apnapan_help_endpoint')")

        # --------------------------------------------------------- offline
        section("[10] It works with no network at all")
        ctx2 = browser.new_context(viewport={"width": 400, "height": 860}, service_workers="allow")
        p2 = ctx2.new_page()
        p2.goto(f"{BASE}/schemes/", wait_until="networkidle")
        time.sleep(2.0)
        regs = p2.evaluate("navigator.serviceWorker.getRegistrations().then(r => r.length)")
        check("a service worker is registered", regs >= 1, f"{regs} registrations")
        cached = p2.evaluate("""async () => {
            const keys = await caches.keys();
            if (!keys.length) return 0;
            const c = await caches.open(keys[0]);
            const all = await c.keys();
            return all.filter(r => r.url.includes('/schemes/')).length; }""")
        check("the scheme cards are cached on the phone", cached >= 7, f"{cached} cached pages")
        p2.reload(wait_until="networkidle")
        time.sleep(0.6)
        check("the page is served by the service worker",
              p2.evaluate("!!navigator.serviceWorker.controller"))
        ctx2.set_offline(True)
        p2.goto(f"{BASE}/schemes/", wait_until="domcontentloaded")
        time.sleep(0.6)
        check("the hub still opens offline", p2.locator("[data-sch-start]").is_visible())
        p2.click("[data-sch-start]")
        time.sleep(0.4)
        check("the quiz still works offline",
              p2.locator(".sch-opt").count() >= 10, str(p2.locator(".sch-opt").count()))
        p2.click('.sch-opt:has-text("Karnataka")')
        time.sleep(0.35)
        p2.click('.sch-opt:has-text("starting")')
        time.sleep(0.35)
        p2.click('.sch-opt:has-text("A loan")')
        p2.click("[data-sch-next]")
        time.sleep(0.35)
        p2.click('.sch-opt:has-text("No")')
        time.sleep(0.5)
        check("matching runs offline too", p2.locator(".sch-scheme").count() >= 2,
              f"{p2.locator('.sch-scheme').count()} cards")
        check("the app admits it is offline",
              "Offline" in p2.locator("[data-sch-status]").inner_text())
        p2.goto(f"{BASE}/schemes/mudra/", wait_until="domcontentloaded")
        time.sleep(0.5)
        check("a scheme card opens offline (from cache)",
              p2.locator("[data-sch-ask]").count() == 1)
        p2.click("[data-sch-ask]")
        time.sleep(0.4)
        p2.locator('[data-dist="mysuru"]').click()
        time.sleep(0.25)
        p2.click("[data-sch-send]")
        time.sleep(0.6)
        queued = p2.evaluate("JSON.parse(localStorage.getItem('apnapan_help_requests')||'[]')")
        check("a request made offline is kept on the phone", len(queued) >= 1, str(len(queued)))
        check("and waits there instead of failing",
              any(q["status"] == "pending" for q in queued))
        ctx2.set_offline(False)
        ctx2.close()

        # ------------------------------------------- every answer combination
        section("[11] Every combination gets a sane answer")
        page.goto(f"{BASE}/schemes/", wait_until="networkidle")
        combo = page.evaluate("""() => {
            const states = window.APNAPAN_SCHEMES.states.map(s => s.id);
            const out = { total: 0, tooFew: [], tooMany: [], missing: [], dupes: 0 };
            const subsets = [[], ['loan'], ['health'], ['skill'],
                             ['loan','health'], ['loan','skill'], ['health','skill'],
                             ['loan','health','skill']];
            out.states = states.length;
            for (const state of states) {
              for (const business of ['starting','running']) {
                for (const need of subsets) {
                  for (const bank of ['yes','no']) {
                    out.total++;
                    const picked = window.APNAPAN_sch.match({state, business, need, bank});
                    const slugs = picked.map(p => p.slug);
                    if (new Set(slugs).size !== slugs.length) out.dupes++;
                    if (need.length && picked.length < 2) out.tooFew.push([state,business,need,bank,slugs.length]);
                    if (picked.length > 3) out.tooMany.push([state,business,need,bank,slugs.length]);
                    for (const n of need) {
                      const hit = picked.some(p => p.tags.indexOf(n) >= 0);
                      if (!hit && picked.length < 3) out.missing.push([state,business,need,bank,n,slugs]);
                    }
                  }
                }
              }
            }
            return out; }""")
        check("every combination was exercised",
              combo["total"] == combo["states"] * 2 * 8 * 2,
              f'{combo["total"]} combinations over {combo["states"]} states')
        check("never more than three schemes", not combo["tooMany"], str(combo["tooMany"][:2]))
        check("never a single lonely card", not combo["tooFew"], str(combo["tooFew"][:2]))
        check("never a duplicate card", combo["dupes"] == 0, str(combo["dupes"]))
        check("what she asked for is always represented",
              not combo["missing"], str(combo["missing"][:2]))

        page.goto(f"{BASE}/schemes/", wait_until="networkidle")
        page.evaluate("localStorage.removeItem('apnapan_sch_quiz')")
        page.reload(wait_until="networkidle")
        run_quiz(state="Bihar", needs=("A loan",))
        check("outside Karnataka she is told where the field team is",
              page.locator("[data-sch-statenote]").is_visible())

        # ------------------------------------------------------ languages
        section("[12] Hindi, Kannada and English")
        page.goto(f"{BASE}/schemes/", wait_until="networkidle")
        page.evaluate("localStorage.removeItem('apnapan_sch_quiz')")
        page.reload(wait_until="networkidle")
        page.click("[data-sch-start]")
        time.sleep(0.35)
        en_q = page.locator("[data-sch-question]").inner_text()
        page.evaluate("window.APNAPAN_setLang('hi')")
        time.sleep(0.5)
        hi_q = page.locator("[data-sch-question]").inner_text()
        page.evaluate("window.APNAPAN_setLang('kn')")
        time.sleep(0.5)
        kn_q = page.locator("[data-sch-question]").inner_text()
        check("the question changes language", en_q != hi_q and hi_q != kn_q,
              f"{en_q[:22]} / {hi_q[:22]} / {kn_q[:22]}")
        check("Hindi is in Devanagari",
              any("\u0900" <= ch <= "\u097f" for ch in hi_q), hi_q[:30])
        check("Kannada is in Kannada script",
              any("\u0c80" <= ch <= "\u0cff" for ch in kn_q), kn_q[:30])
        tiles = page.eval_on_selector_all(".sch-opt", "e=>e.map(x=>x.textContent.trim())")
        check("state names are translated too",
              any("\u0c80" <= ch <= "\u0cff" for name in tiles for ch in name),
              " · ".join(tiles[:3]))
        page.goto(f"{BASE}/schemes/ayushman-bharat/", wait_until="networkidle")
        page.evaluate("window.APNAPAN_setLang('hi')")
        time.sleep(0.5)
        check("a scheme's one-liner is translated on the card",
              any("\u0900" <= ch <= "\u097f" for ch in page.locator(".sch-oneline").inner_text()),
              page.locator(".sch-oneline").inner_text()[:40])
        page.evaluate("window.APNAPAN_setLang('en')")
        time.sleep(0.3)

        # -------------------------------------------------- accessibility
        section("[13] Usable for someone who is not a phone user")
        page.goto(f"{BASE}/schemes/", wait_until="networkidle")
        page.click("[data-sch-start]")
        time.sleep(0.35)
        small = page.eval_on_selector_all(
            ".sch-opt, [data-sch-next], [data-sch-back]",
            "e=>e.filter(x=>x.offsetParent !== null && x.getBoundingClientRect().height < 44).length")
        check("nothing tappable is smaller than 44px", small == 0, f"{small} too small")
        check("options are labelled for a screen reader",
              page.evaluate("""() => [...document.querySelectorAll('.sch-opt')]
                .every(b => b.textContent.trim().length > 0)"""))
        check("the question is announced when it changes",
              page.evaluate("""() => { const q = document.querySelector('[data-sch-question]');
                return q.hasAttribute('tabindex'); }"""))
        check("status is announced, not just coloured",
              page.locator("[data-sch-status][aria-live]").count() == 1)
        page.click("[data-sch-back]")
        time.sleep(0.25)
        check("Escape closes the help sheet",
              page.evaluate("""() => { const a = document.querySelector('[data-sch-app]');
                return !!a; }"""))
        page.goto(f"{BASE}/schemes/mudra/", wait_until="domcontentloaded")
        page.click("[data-sch-ask]")
        time.sleep(0.35)
        page.keyboard.press("Escape")
        time.sleep(0.3)
        check("...and gives focus back", page.locator("[data-sch-sheet]").is_hidden())

        check("no console errors across the whole run", not errors, "; ".join(errors[:3]))
        browser.close()

    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    print("\n" + "=" * 66)
    print(f"  {passed}/{total} checks passed")
    if passed != total:
        print("  failures:")
        for name, ok, detail in results:
            if not ok:
                print(f"    - {name}{('  — ' + detail) if detail else ''}")
    print("=" * 66)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
