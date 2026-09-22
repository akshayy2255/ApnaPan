/* ==========================================================================
   ApnaPan — runtime language switcher (English · ಕನ್ನಡ · हिन्दी)
   The HTML ships in English with data-i18n attributes; this swaps the text.
   ========================================================================== */
(function () {
  'use strict';

  var DICT = window.APNAPAN_I18N || { en: {} };
  var LANGS = window.APNAPAN_LANGS || [{ code: 'en', label: 'English', native: 'English', lang: 'en-IN' }];
  var KEY = 'apnapan_lang';
  var current = localStorage.getItem(KEY) || 'en';
  if (!DICT[current]) current = 'en';

  function langMeta(code) {
    for (var i = 0; i < LANGS.length; i++) { if (LANGS[i].code === code) return LANGS[i]; }
    return LANGS[0];
  }

  /* Reverse index: English text -> key. Lets us translate strings that were
     rendered by the server without a data-i18n marker (form labels, tab names,
     table headers and so on) by matching the exact English text of a text node. */
  var REV = {};
  (function () {
    var en = DICT.en || {};
    Object.keys(en).forEach(function (k) { REV[en[k]] = k; });
  })();

  var SKIP = { SCRIPT: 1, STYLE: 1, NOSCRIPT: 1, TEXTAREA: 1, CODE: 1, PRE: 1, TITLE: 1 };

  function textPass(code) {
    var dict = DICT[code] || DICT.en;
    if (!document.body) return;
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        var p = n.parentNode;
        if (!p || SKIP[p.nodeName]) return NodeFilter.FILTER_REJECT;
        if (p.hasAttribute && (p.hasAttribute('data-i18n') || p.hasAttribute('data-i18n-skip'))) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var node, guard = 0;
    while ((node = walker.nextNode()) && guard++ < 8000) {
      var raw = node.nodeValue || '';
      var text = raw.trim();
      if (!text) continue;
      var key = node.__apKey || REV[text];
      if (!key) continue;
      node.__apKey = key;                 // remember it, so we can switch again later
      var val = dict[key];
      if (val == null || val === text) continue;
      var lead = raw.match(/^\s*/)[0], tail = raw.match(/\s*$/)[0];
      node.nodeValue = lead + val + tail;
    }
  }

  function apply(code) {
    var dict = DICT[code] || DICT.en;
    current = code;
    try { localStorage.setItem(KEY, code); } catch (e) {}

    document.documentElement.setAttribute('lang', langMeta(code).lang);
    document.documentElement.setAttribute('data-lang-active', code);

    [].forEach.call(document.querySelectorAll('[data-i18n]'), function (el) {
      var k = el.getAttribute('data-i18n');
      if (dict[k] != null) el.textContent = dict[k];
    });

    [].forEach.call(document.querySelectorAll('[data-i18n-attr]'), function (el) {
      el.getAttribute('data-i18n-attr').split(';').forEach(function (pair) {
        var bits = pair.split(':');
        if (bits.length !== 2) return;
        var attr = bits[0].trim(), k = bits[1].trim();
        if (dict[k] != null) el.setAttribute(attr, dict[k]);
      });
    });

    // Product names in the local language (Kannada / Hindi packs are labelled bilingually)
    [].forEach.call(document.querySelectorAll('[data-pname]'), function (el) {
      var slug = el.getAttribute('data-pname');
      var p = (window.APNAPAN.products || []).filter(function (x) { return x.slug === slug; })[0];
      if (!p) return;
      var name = code === 'kn' ? (p.name_kn || p.name) : code === 'hi' ? (p.name_hi || p.name) : p.name;
      el.textContent = name;
    });

    textPass(code);

    var badge = document.querySelector('[data-lang-current]');
    if (badge) badge.textContent = code.toUpperCase();

    [].forEach.call(document.querySelectorAll(LANG_SELECTOR), function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-lang') === code ? 'true' : 'false');
    });

    document.dispatchEvent(new CustomEvent('apnapan:lang', { detail: { lang: code } }));
  }

  // Only genuine language buttons may be intercepted — never a link or anything
  // that merely sits inside an element carrying a language attribute.
  var LANG_SELECTOR = 'button[data-lang], [role="menuitemradio"][data-lang]';

  document.addEventListener('click', function (e) {
    var b = e.target.closest(LANG_SELECTOR);
    if (!b) return;
    var code = b.getAttribute('data-lang');
    if (!DICT[code]) return;         // unknown code -> let the click through untouched
    e.preventDefault();
    apply(code);
  });

  // First visit: respect the browser language if it is one we support.
  if (!localStorage.getItem(KEY)) {
    var nav = (navigator.language || 'en').toLowerCase();
    if (nav.indexOf('kn') === 0) current = 'kn';
    else if (nav.indexOf('hi') === 0) current = 'hi';
  }

  document.addEventListener('DOMContentLoaded', function () { apply(current); });
  if (document.readyState !== 'loading') apply(current);

  window.APNAPAN_setLang = apply;
  window.APNAPAN_lang = function () { return current; };
})();
