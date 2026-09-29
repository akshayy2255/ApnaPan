/* ==========================================================================
   ApnaPan — Government Schemes app  (/schemes/ and /schemes/<slug>/)

   Three screens, for a woman who may never have filled a web form:
     1. four tap questions  — no typing, no keyboard, anywhere
     2. one card per scheme — name, one line, amount, listen, act
     3. "Request help"      — makes a TASK for her Sakhi Champion, not a form

   Offline is a first-class case, not a fallback: the quiz, the matching and
   the cards all work with no network (the service worker caches the pages,
   the scheme data ships as a file). A "request help" tap made offline is
   stored on the phone and sent when the phone is back online.

   Everything is data-driven from window.APNAPAN_SCHEMES (generated from
   _build/schemes.py) and translated through window.APNAPAN_I18N.
   ========================================================================== */
(function () {
  'use strict';

  var app = document.querySelector('[data-sch-app]');
  if (!app) return;
  var DATA = window.APNAPAN_SCHEMES;
  if (!DATA || !DATA.schemes) return;

  /* ------------------------------------------------------------ plumbing */
  // localStorage throws in sandboxed frames and private mode — same shim as i18n.js
  var store = (function () {
    var mem = {}, live = false;
    try { window.localStorage.setItem('__sch_t', '1'); window.localStorage.removeItem('__sch_t'); live = true; }
    catch (e) { live = false; }
    return {
      get: function (k) { if (live) { try { return window.localStorage.getItem(k); } catch (e) { live = false; } } return (k in mem) ? mem[k] : null; },
      set: function (k, v) { mem[k] = String(v); if (live) { try { window.localStorage.setItem(k, v); } catch (e) { live = false; } } },
      json: function (k, d) { try { var v = this.get(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
    };
  })();

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return [].slice.call((root || document).querySelectorAll(sel)); }

  function lang() { return (window.APNAPAN_lang && window.APNAPAN_lang()) || 'en'; }

  // t('sch.start') -> text in the language the site is currently showing
  function t(key) {
    var all = window.APNAPAN_I18N || {};
    var dict = all[lang()] || all.en || {};
    return dict[key] != null ? dict[key] : (all.en && all.en[key]) || key;
  }
  function tFill(key, vars) {
    var s = t(key);
    Object.keys(vars || {}).forEach(function (k) { s = s.replace('{' + k + '}', vars[k]); });
    return s;
  }
  function icon(name, cls) {
    var ICONS = window.APNAPAN_ICONS || {};
    var body = ICONS[name] || ICONS.info || '';
    return '<svg class="' + (cls || '') + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
      'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + body + '</svg>';
  }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]; }); }
  function schemeBySlug(slug) { return DATA.schemes.filter(function (s) { return s.slug === slug; })[0]; }

  var ROOT = app.getAttribute('data-sch-root') || './';   // ../schemes/ or ../../schemes/
  var here = app.getAttribute('data-sch-scheme') || '';   // set on a card page
  var openScheme = here ? schemeBySlug(here) : null;      // used by the request sheet

  /* =============================================================== the quiz
     Answers live in memory and in localStorage, so a woman who closes the app
     mid-quiz comes back to the question she was on. */
  var QUIZ_KEY = 'apnapan_sch_quiz';
  var answers = store.json(QUIZ_KEY, { state: '', business: '', need: [], bank: '' });
  var step = 0;

  var screens = {
    quiz: $('[data-sch-screen="quiz"]', app),
    results: $('[data-sch-screen="results"]', app),
    requests: $('[data-sch-screen="requests"]', app)
  };
  var startBtn = $('[data-sch-start]', app);
  var stepLabel = $('[data-sch-step]', app);
  var dots = $$('[data-sch-dot]', app);
  var qEl = $('[data-sch-question]', app);
  var qhintEl = $('[data-sch-qhint]', app);
  var optWrap = $('[data-sch-options]', app);
  var nextBtn = $('[data-sch-next]', app);
  var resWrap = $('[data-sch-results]', app);
  var noneEl = $('[data-sch-none]', app);

  function show(name) {
    Object.keys(screens).forEach(function (k) { if (screens[k]) screens[k].hidden = (k !== name); });
    if (name !== 'results') {
      // scrolling the quiz/requests screens into view keeps the question visible
      var el = screens[name];
      if (el && el.scrollIntoView) el.scrollIntoView({ block: 'nearest' });
    }
  }

  function answered(q) {
    if (q.id === 'state') return !!answers.state;
    if (q.id === 'business') return !!answers.business;
    if (q.id === 'need') return answers.need.length > 0;
    if (q.id === 'bank') return !!answers.bank;
    return false;
  }

  function paintDots() {
    var firstOpen = -1;
    DATA.quiz.forEach(function (q, i) { if (firstOpen < 0 && !answered(q)) firstOpen = i; });
    dots.forEach(function (d, i) {
      if (answered(DATA.quiz[i])) { d.setAttribute('data-done', ''); d.removeAttribute('data-now'); }
      else if (i === (firstOpen < 0 ? DATA.quiz.length - 1 : firstOpen)) { d.setAttribute('data-now', ''); d.removeAttribute('data-done'); }
      else { d.removeAttribute('data-now'); d.removeAttribute('data-done'); }
    });
  }

  function renderQuestion() {
    var q = DATA.quiz[step];
    if (!q || !qEl || !optWrap) return;   // card pages have no quiz
    stepLabel.textContent = String(step + 1);
    qEl.textContent = t(q.key);
    qEl.setAttribute('tabindex', '-1');
    qhintEl.textContent = t(q.hint);
    nextBtn.hidden = !q.multi;
    nextBtn.textContent = step === DATA.quiz.length - 1 ? t('sch.see') : t('sch.next');

    var opts = [];
    if (q.id === 'state') {
      opts = DATA.states.map(function (s) { return { value: s.id, key: s.key, icon: s.icon }; });
    } else {
      opts = DATA.quizOptions[q.id] || [];
    }
    optWrap.innerHTML = opts.map(function (o) {
      var on = q.multi ? answers.need.indexOf(o.value) >= 0 : answers[q.id] === o.value;
      return '<button class="sch-opt" type="button" data-val="' + esc(o.value) + '" aria-pressed="' + (on ? 'true' : 'false') + '">' +
        '<span class="sch-opt__ico">' + icon(o.icon || 'check') + '</span>' +
        '<span>' + esc(t(o.key)) + '</span></button>';
    }).join('');
    paintDots();
    try { qEl.focus({ preventScroll: true }); } catch (e) { }
  }

  if (optWrap) optWrap.addEventListener('click', function (e) {
    var b = e.target.closest('.sch-opt');
    if (!b) return;
    var q = DATA.quiz[step];
    var val = b.getAttribute('data-val');

    if (q.multi) {
      var i = answers.need.indexOf(val);
      if (i >= 0) answers.need.splice(i, 1); else answers.need.push(val);
      b.setAttribute('aria-pressed', i >= 0 ? 'false' : 'true');
      if (answers.need.length) { nextBtn.hidden = false; }
      store.set(QUIZ_KEY, JSON.stringify(answers));
      paintDots();
      return;                                     // multi-select: she taps Next herself
    }

    answers[q.id] = val;
    store.set(QUIZ_KEY, JSON.stringify(answers));
    $$('.sch-opt', optWrap).forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
    paintDots();
    // single-answer questions move on by themselves — one tap, not two
    setTimeout(function () {
      if (step < DATA.quiz.length - 1) { step++; renderQuestion(); }
      else finish();
    }, 180);
  });

  if (nextBtn) nextBtn.addEventListener('click', function () {
    if (step < DATA.quiz.length - 1) { step++; renderQuestion(); } else { finish(); }
  });

  var backBtn = $('[data-sch-back]', app);
  if (backBtn) backBtn.addEventListener('click', function () {
    if (step > 0) { step--; renderQuestion(); } else { reset(); }
  });
  var restartBtn = $('[data-sch-restart]', app);
  if (restartBtn) restartBtn.addEventListener('click', function () { reset(); });

  function reset() {
    answers = { state: '', business: '', need: [], bank: '' };
    step = 0;
    store.set(QUIZ_KEY, JSON.stringify(answers));
    if (resWrap) resWrap.innerHTML = '';
    if (startBtn) { startBtn.hidden = false; }
    show('quiz');
    renderQuestion();
  }

  /* ============================================================= matching
     She is shown 2-3 schemes, never the whole catalogue. Scoring is
     deliberately simple and explainable: every point added also produces a
     reason chip, so the card can say WHY it was picked. */
  var PAD = ['nrlm-shg', 'ayushman-bharat'];    // two schemes that fit almost anyone rural

  function match() {
    var scored = DATA.schemes.map(function (s) {
      var score = 0, why = [];
      if (s.slug === 'stand-up-india' && answers.business === 'running') {
        return { s: s, score: 0, why: [] };     // new businesses only — never show it here
      }
      if (answers.need.indexOf('loan') >= 0 && s.tags.indexOf('loan') >= 0) { score += 3; why.push(s.slug === 'nrlm-shg' ? 'sch.why.any' : 'sch.why.loan'); }
      if (answers.need.indexOf('health') >= 0 && s.tags.indexOf('health') >= 0) { score += 4; why.push('sch.why.health'); }
      if (answers.need.indexOf('skill') >= 0 && s.tags.indexOf('skill') >= 0) { score += 3; why.push('sch.why.skill'); }
      if (answers.business === 'starting' && s.tags.indexOf('new') >= 0) { score += 2; why.push('sch.why.new'); }
      if (answers.business === 'running' && s.tags.indexOf('running') >= 0) { score += 2; why.push('sch.why.running'); }
      if (answers.bank === 'no' && !s.needs_bank) { score += 2; why.push('sch.why.nobank'); }
      if (answers.bank === 'no' && s.needs_bank) { score -= 2; why.push('sch.why.bankfirst'); }
      if (s.available_in === 'some_states') { score -= 1; }   // genuinely state-dependent: rank below
      return { s: s, score: score, why: why };
    });

    scored.sort(function (a, b) {
      if (b.score !== a.score) return b.score - a.score;
      return a.s.slug > b.s.slug ? 1 : -1;      // stable, so the order never jitters
    });

    var byScore = function (a, b) {
      if (b.score !== a.score) return b.score - a.score;
      return a.s.slug > b.s.slug ? 1 : -1;         // stable, so the order never jitters
    };
    var picked = [], used = {};

    /* What she actually asked for is represented first. Without this a woman
       who taps "a loan" could be shown three schemes that are not loans at
       all — the single worst thing this screen could do. Health cover goes
       first because it is free and most women already qualify. */
    var priority = ['health', 'loan', 'skill'].filter(function (n) { return answers.need.indexOf(n) >= 0; });
    priority.forEach(function (need) {
      if (picked.length >= 3) return;
      var best = scored.filter(function (x) {
        return x.score > 0 && !used[x.s.slug] && x.s.tags.indexOf(need) >= 0;
      }).sort(byScore)[0];
      if (best) {
        if (best.why.indexOf('sch.why.' + need) < 0) best.why.unshift('sch.why.' + need);
        used[best.s.slug] = 1;
        picked.push(best);
      }
    });

    // then the best of the rest, to fill up to three
    scored.filter(function (x) { return x.score > 0 && !used[x.s.slug]; })
      .sort(byScore)
      .forEach(function (x) { if (picked.length < 3) { used[x.s.slug] = 1; picked.push(x); } });

    // never leave her with one lonely card: pad with the near-universal ones
    PAD.forEach(function (slug) {
      if (picked.length >= 2) return;
      if (picked.some(function (x) { return x.s.slug === slug; })) return;
      var row = scored.filter(function (x) { return x.s.slug === slug; })[0];
      if (row) { row.why = row.why.length ? row.why : ['sch.why.any']; picked.push(row); }
    });

    // show them strongest-first, with the health card ahead of anything it ties with
    var rank = { 'ayushman-bharat': 0 };
    picked.sort(function (a, b) {
      var ra = rank[a.s.slug] == null ? 1 : rank[a.s.slug];
      var rb = rank[b.s.slug] == null ? 1 : rank[b.s.slug];
      if (ra !== rb) return ra - rb;
      return byScore(a, b);
    });
    if (picked.length) picked[0].best = true;
    return picked;
  }

  function chipHtml(why, max) {
    return (why || []).slice(0, max || 2).map(function (k) {
      return '<li class="sch-chip">' + icon(whyIcon(k)) + '<span>' + esc(t(k)) + '</span></li>';
    }).join('');
  }
  function whyIcon(k) {
    if (/loan/.test(k)) return 'rupee';
    if (/health/.test(k)) return 'shield';
    if (/skill/.test(k)) return 'book';
    if (/new|running/.test(k)) return 'building';
    if (/bank/.test(k)) return 'bank';
    return 'check';
  }

  function finish() {
    var picked = match();
    if (!resWrap) return;
    resWrap.innerHTML = picked.map(function (row) {
      var s = row.s;
      return '<article class="sch-scheme" data-slug="' + esc(s.slug) + '">' +
        '<div class="sch-scheme__top">' +
          '<span class="sch-scheme__ico">' + icon(s.icon) + '</span>' +
          '<h3>' + esc(t('sch.' + s.slug + '.name')) + '</h3>' +
        '</div>' +
        '<p class="sch-scheme__line">' + esc(t('sch.' + s.slug + '.one_line')) + '</p>' +
        '<p class="sch-scheme__benefit">' + esc(t('sch.' + s.slug + '.benefit')) + '</p>' +
        '<ul class="sch-chips">' + chipHtml(row.why, 2) +
          (s.check_first ? '<li class="sch-chip">' + icon('info') + '<span>' + esc(t('sch.check')) + '</span></li>' : '') +
        '</ul>' +
        '<div class="sch-scheme__actions">' +
          '<button class="btn btn--green" type="button" data-sch-play data-key="' + esc(s.slug) + '">' +
            icon('speaker') + '<span>' + esc(t('sch.play')) + '</span></button>' +
          '<button class="btn btn--gold" type="button" data-sch-ask data-scheme="' + esc(s.slug) + '">' +
            icon('hand-heart') + '<span>' + esc(t('sch.help')) + '</span></button>' +
          '<a class="sch-scheme__more" href="' + ROOT + esc(s.slug) + '/">' + esc(t('sch.full')) + icon('chev-r') + '</a>' +
        '</div>' +
      '</article>';
    }).join('');
    if (noneEl) noneEl.hidden = picked.length > 0;
    var stateNote = $('[data-sch-statenote]', app);
    if (stateNote) stateNote.hidden = (answers.state === 'karnataka' || !answers.state);
    if (startBtn) startBtn.hidden = true;
    show('results');
    // a real reason is worth stating once
    if (resWrap.firstChild) resWrap.firstChild.scrollIntoView({ block: 'nearest' });
  }

  if (startBtn) startBtn.addEventListener('click', function () {
    startBtn.hidden = true;
    step = 0;
    while (step < DATA.quiz.length && answered(DATA.quiz[step])) step++;
    if (step >= DATA.quiz.length) { finish(); return; }
    show('quiz');
    renderQuestion();
  });

  /* ====================================================== the explainer
     If the content team has dropped a recording into assets/audio/, the card
     ships an <audio> element and we use it. Until then the phone's own voice
     reads the card aloud — in her language — so the button is never dead. */
  var speaking = null;
  var audioEl = document.querySelector('[data-sch-audio]');
  // Which languages have a recording is decided at build time and recorded in
  // the data bundle, so the app never requests a file that is not there and
  // never plays a language she cannot read.
  function recordingFor(slug, l) {
    var s = schemeBySlug(slug);
    if (!s || !s.audio || s.audio.indexOf(l) < 0) return '';
    var base = app.getAttribute('data-sch-audio-base') || 'assets/audio/';
    return base + slug + '-' + l + '.mp3';
  }
  function noteEl() { return document.querySelector('.sch-script-note'); }
  function setNote(show) { var n = noteEl(); if (n) n.hidden = !show; }
  // The player and the note must agree with the language she is reading in,
  // on load and after every switch — not only after she taps play.
  function syncAudio() {
    var slug = app.getAttribute('data-sch-scheme');
    if (!audioEl) return;
    if (slug && recordingFor(slug, lang())) {
      // Only the card page shows a player; on the quiz results the recordings
      // still play, but through the existing button and nothing new appears.
      if (audioEl.hasAttribute('controls')) audioEl.hidden = false;
      setNote(false);
      return;
    }
    try { audioEl.pause(); audioEl.removeAttribute('src'); } catch (e) { }
    audioEl.hidden = true;
    if (slug) setNote(true);
  }
  function scriptFor(slug) {
    var s = schemeBySlug(slug);
    if (!s) return '';
    var keys = ['one_line', 'benefit', 'who', 'how'];
    return keys.map(function (k) { return t('sch.' + slug + '.' + k) + '.'; }).join(' ');
  }
  function stopSpeaking() {
    if (speaking && window.speechSynthesis) window.speechSynthesis.cancel();
    if (audioEl && !audioEl.paused) { try { audioEl.pause(); audioEl.currentTime = 0; } catch (e) { } }
    speaking = null;
    $$('[data-sch-play]').forEach(function (b) {
      b.setAttribute('aria-pressed', 'false');
      var lbl = b.querySelector('span');
      if (lbl) lbl.textContent = t('sch.play');
    });
  }
  function markPlaying(btn) {
    if (!btn) return;
    btn.setAttribute('aria-pressed', 'true');
    var lbl = btn.querySelector('span');
    if (lbl) lbl.textContent = t('sch.playing');
  }
  function speak(slug, btn) {
    var url = audioEl ? recordingFor(slug, lang()) : '';
    if (url) {
      // A real voice, in her language. Someone recorded this for her.
      speaking = slug;
      markPlaying(btn);
      setNote(false);
      if (audioEl.hasAttribute('controls')) audioEl.hidden = false;
      if (audioEl.getAttribute('src') !== url) audioEl.setAttribute('src', url);
      audioEl.onended = stopSpeaking;
      audioEl.onerror = function () { setNote(true); stopSpeaking(); };
      var p = audioEl.play();
      if (p && p.catch) p.catch(function () { setNote(true); stopSpeaking(); });
      return true;
    }
    if (!window.speechSynthesis || !window.SpeechSynthesisUtterance) return false;
    window.speechSynthesis.cancel();
    var u = new SpeechSynthesisUtterance(scriptFor(slug));
    u.lang = { en: 'en-IN', kn: 'kn-IN', hi: 'hi-IN' }[lang()] || 'en-IN';
    u.rate = 0.92;
    u.onend = stopSpeaking;
    // Some phones ship with no text-to-speech voice at all. Say so plainly
    // rather than leaving her staring at a button that did nothing.
    u.onerror = function () {
      stopSpeaking();
      var note = noteEl();
      if (note) { note.hidden = false; note.textContent = t('sch.audio.unavailable'); }
      toast(t('sch.audio.unavailable'), 'warn');
    };
    speaking = slug;
    markPlaying(btn);
    setNote(true);
    window.speechSynthesis.speak(u);
    return true;
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-sch-play]');
    if (!b) return;
    var slug = b.getAttribute('data-key') || app.getAttribute('data-sch-scheme');
    if (speaking === slug) { stopSpeaking(); return; }
    stopSpeaking();
    if (!speak(slug, b)) {
      var note = $('.sch-script-note', document);
      if (note) note.textContent = t('sch.play') + ' — ' + t('sch.script.note');
    }
  }, false);

  /* ==================================== request help: a task, not a form */
  var REQ_KEY = 'apnapan_help_requests';
  var DISTRICT_KEY = 'apnapan_sch_district';
  var ENDPOINT_KEY = 'apnapan_help_endpoint';       // runtime override for their server
  var requests = store.json(REQ_KEY, []);
  var sheet = $('[data-sch-sheet]', app);
  var sheetSchemeEl = $('[data-sch-sheet-scheme]', app);
  var sheetDistrictWrap = $('[data-sch-districts]', app);
  var sheetDistrictList = $('[data-sch-district-list]', app);
  var sheetSakhi = $('[data-sch-sakhi]', app);
  var sendBtn = $('[data-sch-send]', app);
  var pendingScheme = null;
  var lastFocus = null;

  function endpoint() {
    return store.get(ENDPOINT_KEY) || (window.APNAPAN && window.APNAPAN.helpEndpoint) || '';
  }
  function districtId() { return store.get(DISTRICT_KEY) || ''; }
  function sakhiFor(did) {
    var d = (DATA.districts || []).filter(function (x) { return x.id === did; })[0];
    var cid = d ? d.sakhi : 'sc-bengaluru';
    return (DATA.coordinators || []).filter(function (c) { return c.id === cid; })[0] || DATA.coordinators[0];
  }
  function saveRequests() { store.set(REQ_KEY, JSON.stringify(requests)); }

  function openSheet(slug) {
    pendingScheme = schemeBySlug(slug) || openScheme;
    if (!pendingScheme || !sheet) return;
    lastFocus = document.activeElement;
    stopSpeaking();
    sheetSchemeEl.textContent = t('sch.' + pendingScheme.slug + '.name');
    var did = districtId();
    sheetDistrictWrap.hidden = !!did;
    if (!did) paintDistricts();
    paintSakhi(did || '');
    sendBtn.disabled = !did;
    sendBtn.hidden = false;
    sheet.hidden = false;
    sheet.setAttribute('data-open', 'true');
    var first = sheetDistrictList.querySelector('.sch-opt') || sendBtn;
    try { first.focus({ preventScroll: true }); } catch (e) { }
  }
  function closeSheet() {
    if (!sheet) return;
    sheet.hidden = true;
    sheet.setAttribute('data-open', 'false');
    if (lastFocus && lastFocus.focus) { try { lastFocus.focus({ preventScroll: true }); } catch (e) { } }
  }
  function paintDistricts() {
    sheetDistrictList.innerHTML = (DATA.districts || []).map(function (d) {
      return '<button class="sch-opt sch-opt--sm" type="button" data-dist="' + esc(d.id) + '">' +
        '<span class="sch-opt__ico">' + icon('pin') + '</span><span>' + esc(t(d.key)) + '</span></button>';
    }).join('');
  }
  function paintSakhi(did) {
    if (!did) { sheetSakhi.hidden = true; return; }
    var c = sakhiFor(did);
    sheetSakhi.hidden = false;
    sheetSakhi.innerHTML = '<div class="sch-sakhi__name">' + icon('women') + esc(c.name) + '</div>' +
      '<div class="sch-sakhi__meta">' + esc(t('sch.sakhi.area')) + ': ' + esc(c.area) + '</div>' +
      '<div class="sch-sakhi__meta">' + esc(t('sch.sakhi.langs')) + ': ' + esc(c.langs) + '</div>' +
      '<div class="sch-sakhi__meta">' + esc(c.display) + '</div>';
  }

  document.addEventListener('click', function (e) {
    var ask = e.target.closest('[data-sch-ask]');
    if (ask) { e.preventDefault(); openSheet(ask.getAttribute('data-scheme')); return; }
    var dist = e.target.closest('[data-dist]');
    if (dist) {
      var did = dist.getAttribute('data-dist');
      store.set(DISTRICT_KEY, did);
      $$('.sch-opt', sheetDistrictList).forEach(function (b) { b.setAttribute('aria-pressed', b === dist ? 'true' : 'false'); });
      paintSakhi(did);
      sendBtn.disabled = false;
      try { sendBtn.focus({ preventScroll: true }); } catch (er) { }
      return;
    }
    if (e.target.closest('[data-sch-cancel]')) { closeSheet(); return; }
    if (e.target.closest('[data-sch-send]')) { createTask(sendBtn); return; }
    if (e.target.closest('[data-sch-open-requests]')) { paintRequests(); show('requests'); return; }
    if (e.target.closest('[data-sch-close-requests]')) { show(answers.bank ? 'results' : 'quiz'); return; }
    if (e.target.closest('[data-sch-req-remove]')) {
      var id = e.target.closest('[data-sch-req-remove]').getAttribute('data-sch-req-remove');
      requests = requests.filter(function (r) { return r.id !== id; });
      saveRequests(); paintRequests(); return;
    }
    var wa = e.target.closest('[data-sch-wa]');
    if (wa) { markSent(wa.getAttribute('data-sch-wa'), 'handed-off'); return; }
  }, false);

  function createTask(btn) {
    var did = districtId();
    if (!did || !pendingScheme) return;
    var c = sakhiFor(did);
    var task = {
      id: 'req-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 6),
      slug: pendingScheme.slug,
      scheme: pendingScheme.name,
      district: did,
      sakhi: { id: c.id, name: c.name, phone: c.phone, display: c.display },
      at: new Date().toISOString(),
      status: 'pending',
      tries: 0,
      lang: lang()
    };
    requests.unshift(task);
    saveRequests();
    paintRequests();
    closeSheet();
    toast(tFill('sch.help.done.body', { sakhi: c.name }), 'ok');
    if (btn) btn.blur();
    sync();
  }

  function markSent(id, status) {
    requests = requests.map(function (r) {
      if (r.id !== id) return r;
      r.status = status || 'sent';
      return r;
    });
    saveRequests();
    paintRequests();
    toast(t('sch.req.sent'), 'ok');
  }

  // Queue: POST each pending task. No endpoint configured = demo mode, where
  // the honest next step is the WhatsApp/call handoff offered on the card.
  function sync() {
    var url = endpoint();
    var pending = requests.filter(function (r) { return r.status === 'pending'; });
    updatePendingBadge();
    if (!url || !pending.length) return;
    if (!navigator.onLine) return;
    pending.forEach(function (r) {
      fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(r)
      }).then(function (res) {
        if (res && res.ok) markSent(r.id, 'sent');
        else throw new Error('bad status');
      }).catch(function () {
        requests = requests.map(function (q) {
          if (q.id !== r.id) return q;
          q.tries = (q.tries || 0) + 1;
          return q;
        });
        saveRequests();
        updatePendingBadge();
      });
    });
  }

  function waLink(r) {
    var txt = 'ApnaPan schemes app — help request\n' +
      'Scheme: ' + r.scheme + '\n' +
      'District: ' + r.district + '\n' +
      'Requested: ' + new Date(r.at).toLocaleString();
    return 'https://wa.me/' + String(r.sakhi.phone).replace(/[^0-9]/g, '') + '?text=' + encodeURIComponent(txt);
  }

  function updatePendingBadge() {
    var n = requests.filter(function (r) { return r.status === 'pending'; }).length;
    var badge = $('[data-sch-req-count]', app);
    if (!badge) return;
    badge.textContent = String(n);
    badge.hidden = n === 0;
  }

  function paintRequests() {
    var wrap = $('[data-sch-requests]', app);
    var none = $('[data-sch-req-none]', app);
    if (!wrap) return;
    if (none) none.hidden = requests.length > 0;
    wrap.innerHTML = requests.map(function (r) {
      var wait = r.status === 'pending';
      return '<article class="sch-req">' +
        '<div class="sch-req__head">' +
          '<span class="sch-req__name">' + esc(t('sch.' + r.slug + '.name')) + '</span>' +
          '<span class="sch-badge ' + (wait ? 'sch-badge--wait' : 'sch-badge--sent') + '">' +
            icon(wait ? 'cloud-off' : 'check') + '<span>' + esc(wait ? t('sch.req.pending') : t('sch.req.sent')) + '</span>' +
          '</span>' +
        '</div>' +
        '<div class="sch-req__meta">' + esc(t('sch.sakhi.title')) + ': ' + esc(r.sakhi.name) + ' · ' + esc(r.sakhi.display) +
          ' · ' + esc(new Date(r.at).toLocaleString()) + '</div>' +
        '<div class="sch-req__actions">' +
          (wait ? '<a class="btn btn--wa" href="' + waLink(r) + '" target="_blank" rel="noopener" data-sch-wa="' + esc(r.id) + '">' +
            icon('whatsapp') + '<span>' + esc(t('sch.req.whatsapp')) + '</span></a>' : '') +
          '<a class="btn btn--ghost" href="tel:' + esc(r.sakhi.phone) + '">' + icon('phone') + '<span>' + esc(t('sch.req.call')) + '</span></a>' +
          '<button class="btn btn--ghost" type="button" data-sch-req-remove="' + esc(r.id) + '">' + esc(t('sch.req.remove')) + '</button>' +
        '</div>' +
      '</article>';
    }).join('');
    updatePendingBadge();
  }

  /* ------------------------------------------------------------- status */
  function paintStatus() {
    var pill = $('[data-sch-status]', app);
    if (!pill) return;
    var online = navigator.onLine;
    pill.classList.toggle('sch-pill--on', online);
    pill.innerHTML = icon(online ? 'check' : 'cloud-off', 'sch-pill__ico') +
      '<span>' + esc(t(online ? 'sch.online' : 'sch.offline')) + '</span>';
  }

  function toast(msg, kind) {
    var wrap = $('[data-toasts]');
    if (!wrap) return;
    var el = document.createElement('div');
    el.className = 'toast' + (kind ? ' toast--' + kind : '');
    el.setAttribute('role', 'status');
    el.innerHTML = icon('check') + '<span>' + esc(msg) + '</span>';
    wrap.appendChild(el);
    setTimeout(function () { el.setAttribute('data-out', ''); }, 3200);
    setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 3800);
  }

  window.addEventListener('online', function () { paintStatus(); sync(); });
  window.addEventListener('offline', paintStatus);

  /* ------------------------------------------------ documents, remembered */
  var DOCS_KEY = 'apnapan_sch_docs';
  var docs = store.json(DOCS_KEY, {});
  $$('[data-doc]').forEach(function (input) {
    var id = input.getAttribute('data-doc');
    input.checked = !!docs[id];
    input.addEventListener('change', function () {
      docs[id] = input.checked;
      store.set(DOCS_KEY, JSON.stringify(docs));
    });
  });

  /* --------------------------------------------- context, key handling */
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (sheet && !sheet.hidden) closeSheet();
    stopSpeaking();
  });

  document.addEventListener('apnapan:lang', function () {
    // re-render everything this file drew, in the new language
    stopSpeaking();
    syncAudio();
    if (screens.quiz && !screens.quiz.hidden) renderQuestion();
    if (screens.results && !screens.results.hidden && resWrap && resWrap.children.length) finish();
    if (screens.requests && !screens.requests.hidden) paintRequests();
    if (sheet && !sheet.hidden) {
      sheetSchemeEl.textContent = pendingScheme ? t('sch.' + pendingScheme.slug + '.name') : '';
      if (sheetDistrictWrap.hidden === false) paintDistricts();
      paintSakhi(districtId() || '');
    }
    paintStatus();
  });

  syncAudio();

  /* ------------------------------------------- service worker + install */
  (function () {
    var swUrl = app.getAttribute('data-sch-sw');
    if (!swUrl || !('serviceWorker' in navigator)) return;
    if (location.protocol === 'file:') return;              // no SW over file://
    navigator.serviceWorker.register(swUrl, { scope: './' }).catch(function () { /* preview frames, old browsers */ });
  })();

  /* ---------------------------------------------------------- test hook
     The browser suite drives EVERY answer combination through this real
     matcher, rather than a copy of it that could drift. Nothing else uses
     it, and nothing here writes to her stored answers. */
  window.APNAPAN_sch = {
    match: function (a) {
      var prev = answers;
      answers = { state: a.state || 'karnataka', business: a.business || 'starting',
                  need: a.need || [], bank: a.bank || 'yes' };
      var out = match().map(function (r) {
        return { slug: r.s.slug, tags: r.s.tags, why: r.why, score: r.score };
      });
      answers = prev;
      return out;
    }
  };

  /* --------------------------------------------------------------- boot */
  paintStatus();
  updatePendingBadge();
  paintRequests();
  if (startBtn) startBtn.hidden = false;
  if (screens.quiz) screens.quiz.hidden = true;
  if (screens.results) screens.results.hidden = true;
  if (screens.requests) screens.requests.hidden = true;
  if (openScheme) {                       // on a card page: pre-focus the big action
    var ask = $('[data-sch-ask]', app);
    if (ask) ask.setAttribute('data-scheme', openScheme.slug);
  }
  sync();
})();
