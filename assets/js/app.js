/* ==========================================================================
   ApnaPan — storefront behaviour
   Vanilla JS, no dependencies. Cart persists in localStorage.
   ========================================================================== */
(function () {
  'use strict';

  /* localStorage is not always available — sandboxed preview iframes, Safari private
     mode and storage-blocked browsers throw even when READING it, which would abort
     this whole file before any handler is bound. Everything goes through this shim. */
  var store = (function () {
    var mem = {}, live = false;
    try {
      window.localStorage.setItem('__apnapan_t', '1');
      window.localStorage.removeItem('__apnapan_t');
      live = true;
    } catch (e) { live = false; }
    return {
      get: function (k) {
        if (live) { try { return window.localStorage.getItem(k); } catch (e) { live = false; } }
        return (k in mem) ? mem[k] : null;
      },
      set: function (k, v) {
        mem[k] = String(v);
        if (live) { try { window.localStorage.setItem(k, v); } catch (e) { live = false; } }
      },
      del: function (k) {
        delete mem[k];
        if (live) { try { window.localStorage.removeItem(k); } catch (e) { live = false; } }
      }
    };
  })();

  var CFG = window.APNAPAN || {};
  var PRODUCTS = CFG.products || [];
  var BASE = CFG.base || '';
  var LANG = store.get('apnapan_lang') || 'en';
  var CART_KEY = 'apnapan_cart_v1';
  var WISH_KEY = 'apnapan_wish_v1';
  var FREE_SHIP = CFG.freeShipOver || 599;
  var SHIP_FEE = CFG.shipFee || 49;
  var COD_FEE = CFG.codFee || 25;
  var SCHOOL_PCT = CFG.schoolPct || 6;

  /* ------------------------------------------------------------- helpers */
  function $(s, r) { return (r || document).querySelector(s); }
  /* Build a site-relative URL that works at a domain root AND inside a
     GitHub Pages project path (/ApnaPan/). BASE is "", "..", or "../..". */
  function url(p) { return (BASE ? BASE + '/' : '') + p; }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function money(n) { return '₹' + Number(n).toLocaleString('en-IN'); }

  function t(key, vars) {
    var dict = (window.APNAPAN_I18N || {})[LANG] || (window.APNAPAN_I18N || {}).en || {};
    var s = dict[key] || ((window.APNAPAN_I18N || {}).en || {})[key] || key;
    if (vars) { Object.keys(vars).forEach(function (k) { s = s.replace('{' + k + '}', vars[k]); }); }
    return s;
  }

  function pname(p) {
    if (LANG === 'kn' && p.name_kn) return p.name_kn;
    if (LANG === 'hi' && p.name_hi) return p.name_hi;
    return p.name;
  }

  function product(slug) { for (var i = 0; i < PRODUCTS.length; i++) { if (PRODUCTS[i].slug === slug) return PRODUCTS[i]; } return null; }

  function toast(msg, kind) {
    var wrap = $('[data-toasts]');
    if (!wrap) return;
    var el = document.createElement('div');
    el.className = 'toast' + (kind === 'error' ? ' toast--err' : '');
    el.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:19px;height:19px">' +
      (kind === 'error' ? '<circle cx="12" cy="12" r="9"/><path d="M12 8v4M12 16v.1"/>' : '<path d="M20 6 9 17l-5-5"/>') + '</svg><span></span>';
    el.querySelector('span').textContent = msg;
    wrap.appendChild(el);
    setTimeout(function () { el.style.transition = 'opacity .3s, transform .3s'; el.style.opacity = '0'; el.style.transform = 'translateY(10px)'; }, 2600);
    setTimeout(function () { el.remove(); }, 3000);
  }

  /* ---------------------------------------------------------------- cart */
  var cart = { items: [] };
  try { cart = JSON.parse(store.get(CART_KEY)) || { items: [] }; } catch (e) { cart = { items: [] }; }
  if (!cart.items) cart.items = [];

  function saveCart() { try { store.set(CART_KEY, JSON.stringify(cart)); } catch (e) {} }

  function lineData(l) {
    var p = product(l.slug);
    if (!p) return null;
    var size = p.sizes[l.size] || p.sizes[0];
    return { p: p, size: size, qty: l.qty, key: l.slug + ':' + l.size, lineTotal: size.price * l.qty };
  }

  function cartLines() { return cart.items.map(lineData).filter(Boolean); }
  function cartCount() { return cart.items.reduce(function (n, l) { return n + l.qty; }, 0); }
  function cartSubtotal() { return cartLines().reduce(function (n, l) { return n + l.lineTotal; }, 0); }
  function cartMrp() {
    return cartLines().reduce(function (n, l) {
      var p = l.p, idx = cart.items.filter(function (x) { return x.slug === p.slug; })[0] || { size: 0 };
      var mrp = p.sizes[idx.size] ? Math.round(p.sizes[idx.size].price * (p.mrp / p.price)) : p.mrp;
      return n + mrp * l.qty;
    }, 0);
  }

  function addToCart(slug, sizeIdx, qty) {
    sizeIdx = sizeIdx || 0; qty = qty || 1;
    var found = null;
    cart.items.forEach(function (l) { if (l.slug === slug && l.size === sizeIdx) found = l; });
    if (found) { found.qty += qty; } else { cart.items.push({ slug: slug, size: sizeIdx, qty: qty }); }
    saveCart(); renderCart(); openDrawer();
    toast(t('common.added'));
  }

  function setQty(slug, sizeIdx, qty) {
    cart.items = cart.items.filter(function (l) { return !(l.slug === slug && l.size === sizeIdx) || qty > 0; });
    cart.items.forEach(function (l) { if (l.slug === slug && l.size === sizeIdx && qty > 0) l.qty = qty; });
    saveCart(); renderCart();
  }

  function removeLine(slug, sizeIdx) {
    cart.items = cart.items.filter(function (l) { return !(l.slug === slug && l.size === sizeIdx); });
    saveCart(); renderCart();
  }

  function shipFee(sub) { return sub === 0 ? 0 : (sub >= FREE_SHIP ? 0 : SHIP_FEE); }

  function renderCart() {
    var lines = cartLines(), sub = cartSubtotal(), n = cartCount();
    var badge = $('[data-cart-count]'), btn = $('.cart-btn');
    if (badge) badge.textContent = n;
    if (btn) btn.setAttribute('data-empty', n ? 'false' : 'true');

    var body = $('[data-cart-body]'), foot = $('[data-cart-foot]');
    if (!body) return;

    if (!lines.length) {
      body.innerHTML = '<div class="cart-empty">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">' +
        '<circle cx="9.5" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h2.3l2.5 11.1a2 2 0 0 0 2 1.6h8.6a2 2 0 0 0 1.9-1.4L21 7H5"/></svg>' +
        '<p><b>' + t('cart.empty') + '</b></p><p class="small">' + t('cart.emptysub') + '</p>' +
        '<a class="btn mt-2" href="' + url('shop/') + '">' + t('common.shop') + '</a></div>';
      if (foot) foot.hidden = true;
      return;
    }

    var left = Math.max(0, FREE_SHIP - sub);
    var shipHtml = left > 0
      ? '<div class="ship-bar"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M2 6.5h11v9H2z"/><path d="M13 9.5h4l3 3v3h-7z"/><circle cx="6" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/></svg>' +
        '<div style="flex:1"><span>' + t('cart.shipprog', { amt: money(left) }) + '</span><span class="ship-bar__track"><i style="width:' + Math.min(100, (sub / FREE_SHIP) * 100) + '%"></i></span></div></div>'
      : '<div class="ship-bar"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M20 6 9 17l-5-5"/></svg><span>' + t('cart.shipdone') + '</span></div>';

    body.innerHTML = shipHtml + lines.map(function (l) {
      var img = url(l.p.img);
      return '<div class="cart-line">' +
        '<img src="' + img + '" alt="' + l.p.name + '" width="72" height="84">' +
        '<div><p class="cart-line__title">' + pname(l.p) + '</p>' +
        '<p class="cart-line__meta">' + l.size.label + '</p>' +
        '<p class="cart-line__price">' + money(l.lineTotal) + '</p>' +
        '<div class="qty"><button type="button" data-qty="-" data-slug="' + l.p.slug + '" data-size="' + cart.items.filter(function (x) { return x.slug === l.p.slug; })[0].size + '" aria-label="Decrease"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M5 12h14"/></svg></button>' +
        '<input type="text" inputmode="numeric" value="' + l.qty + '" data-qty-input data-slug="' + l.p.slug + '" aria-label="' + t('common.qty') + '">' +
        '<button type="button" data-qty="+" data-slug="' + l.p.slug + '" data-size="' + cart.items.filter(function (x) { return x.slug === l.p.slug; })[0].size + '" aria-label="Increase"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg></button></div>' +
        '<br><button class="cart-line__remove" type="button" data-remove data-slug="' + l.p.slug + '" data-size="' + cart.items.filter(function (x) { return x.slug === l.p.slug; })[0].size + '">' + t('cart.remove') + '</button>' +
        '</div><span class="small muted"></span></div>';
    }).join('');

    if (foot) {
      foot.hidden = false;
      var ship = shipFee(sub);
      foot.innerHTML =
        '<div class="summary-row"><span>' + t('common.subtotal') + '</span><span>' + money(sub) + '</span></div>' +
        '<div class="summary-row"><span>' + t('cart.ship') + '</span><span>' + (ship ? money(ship) : t('cart.free')) + '</span></div>' +
        '<div class="summary-row summary-row--total"><span>' + t('common.total') + '</span><span>' + money(sub + ship) + '</span></div>' +
        '<a class="btn btn--lg btn--block mt-2" href="' + url('checkout/') + '">' + t('cart.checkout') + '</a>' +
        '<button class="btn btn--ghost btn--sm btn--block mt-1" type="button" data-cart-clear>' + t('cart.clear') + '</button>';
    }
  }

  function openDrawer() {
    var d = $('[data-drawer]'), s = $('[data-cart-scrim]');
    if (d) d.setAttribute('data-open', 'true');
    if (s) s.setAttribute('data-open', 'true');
    document.body.style.overflow = 'hidden';
  }
  function closeDrawer() {
    var d = $('[data-drawer]'), s = $('[data-cart-scrim]');
    if (d) d.setAttribute('data-open', 'false');
    if (s) s.setAttribute('data-open', 'false');
    document.body.style.overflow = '';
  }

  /* ---------------------------------------------------- delegated clicks */
  document.addEventListener('click', function (e) {
    var el;
    if ((el = e.target.closest('[data-add]'))) {
      e.preventDefault();
      addToCart(el.getAttribute('data-add'), parseInt(el.getAttribute('data-size') || '0', 10), 1);
      return;
    }
    if ((el = e.target.closest('[data-buy]'))) {
      e.preventDefault();
      addToCart(el.getAttribute('data-buy'), parseInt(el.getAttribute('data-size') || '0', 10), 1);
      setTimeout(function () { location.href = url('checkout/'); }, 220);
      return;
    }
    if ((el = e.target.closest('[data-cart-open]'))) { e.preventDefault(); openDrawer(); return; }
    if ((el = e.target.closest('[data-cart-close]')) || (el = e.target.closest('[data-cart-scrim]'))) { closeDrawer(); return; }
    if ((el = e.target.closest('[data-qty]'))) {
      var delta = el.getAttribute('data-qty') === '+' ? 1 : -1;
      var sl = el.getAttribute('data-slug'), sz = parseInt(el.getAttribute('data-size') || '0', 10);
      var line = cart.items.filter(function (l) { return l.slug === sl && l.size === sz; })[0];
      if (line) setQty(sl, sz, Math.max(0, line.qty + delta));
      return;
    }
    if ((el = e.target.closest('[data-remove]'))) {
      removeLine(el.getAttribute('data-slug'), parseInt(el.getAttribute('data-size') || '0', 10)); return;
    }
    if ((el = e.target.closest('[data-cart-clear]'))) { cart.items = []; saveCart(); renderCart(); return; }
    if ((el = e.target.closest('[data-wish]'))) {
      var wish = {}; try { wish = JSON.parse(store.get(WISH_KEY)) || {}; } catch (err) {}
      var k = el.getAttribute('data-wish');
      wish[k] = !wish[k];
      try { store.set(WISH_KEY, JSON.stringify(wish)); } catch (err) {}
      el.setAttribute('aria-pressed', wish[k] ? 'true' : 'false');
      return;
    }
    if ((el = e.target.closest('[data-copy-link]'))) {
      if (navigator.clipboard) navigator.clipboard.writeText(location.href);
      toast('Link copied');
      return;
    }
    if ((el = e.target.closest('[data-apply]'))) {
      var sel = $('[data-role-select]');
      if (sel) { sel.value = el.getAttribute('data-apply'); }
      var form = $('[data-form="career"]');
      if (form) { form.scrollIntoView({ behavior: 'smooth', block: 'center' }); var n = form.querySelector('[name="name"]'); if (n) setTimeout(function () { n.focus(); }, 500); }
      return;
    }
    if ((el = e.target.closest('[data-review-open]'))) {
      var rf = $('[data-form="review"]');
      if (rf) { rf.hidden = false; rf.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
      return;
    }
    if ((el = e.target.closest('[data-qty-input]'))) { /* handled on change */ }
  });

  document.addEventListener('change', function (e) {
    var el = e.target;
    if (el.matches('[data-qty-input]')) {
      var line = cart.items.filter(function (l) { return l.slug === el.getAttribute('data-slug'); })[0];
      if (line) setQty(el.getAttribute('data-slug'), line.size, Math.max(0, parseInt(el.value, 10) || 0));
    }
    if (el.matches('[name="payment"]')) { renderCheckout(); }
  });

  /* -------------------------------------------------------- mobile nav */
  var nav = $('#nav'), navScrim = $('[data-scrim]');
  function setNav(open) {
    if (!nav) return;
    nav.setAttribute('data-open', open ? 'true' : 'false');
    if (navScrim) navScrim.setAttribute('data-open', open ? 'true' : 'false');
    var b = $('[data-nav-open]'), c = $('[data-nav-close]');
    if (b) b.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (c) c.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.style.overflow = open ? 'hidden' : '';
    if (open) { var first = nav.querySelector('.nav__link'); }
  }
  $$('[data-nav-open]').forEach(function (b) { b.addEventListener('click', function () { setNav(true); }); });
  $$('[data-nav-close]').forEach(function (b) { b.addEventListener('click', function () { setNav(false); }); });
  if (navScrim) navScrim.addEventListener('click', function () { setNav(false); });
  // Tapping any link inside the drawer closes it (important for same-page anchors).
  if (nav) nav.addEventListener('click', function (e) { if (e.target.closest('a')) setNav(false); });
  // Tap anywhere outside the open drawer to close it (the scrim alone cannot
  // cover the sticky header, which paints above it).
  document.addEventListener('click', function (e) {
    if (!nav || nav.getAttribute('data-open') !== 'true') return;
    if (nav.contains(e.target)) return;                 // inside the drawer
    if (e.target.closest('[data-nav-open]')) return;     // the burger toggles itself
    setNav(false);
  });

  // Desktop resize should never leave the drawer state stuck on.
  window.addEventListener('resize', function () { if (window.innerWidth > 1100) setNav(false); });

  /* --------------------------------------------------------- language UI */
  var langWrap = $('.lang'), langBtn = $('[data-lang-btn]'), langMenu = $('[data-lang-menu]');
  function langItems() { return langMenu ? $$('button', langMenu) : []; }
  function openLang(open) {
    if (!langMenu || !langBtn) return;
    langMenu.setAttribute('data-open', open ? 'true' : 'false');
    langBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  function langIsOpen() { return langMenu && langMenu.getAttribute('data-open') === 'true'; }
  if (langBtn) {
    langBtn.addEventListener('click', function (e) { e.stopPropagation(); openLang(!langIsOpen()); });
    langBtn.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault(); openLang(true);
        var items = langItems(); if (items.length) items[e.key === 'ArrowDown' ? 0 : items.length - 1].focus();
      }
    });
  }
  if (langMenu) {
    langMenu.addEventListener('keydown', function (e) {
      var items = langItems(), i = items.indexOf(document.activeElement);
      if (e.key === 'Escape') { openLang(false); if (langBtn) langBtn.focus(); return; }
      if (e.key === 'ArrowDown') { e.preventDefault(); (items[i + 1] || items[0]).focus(); }
      if (e.key === 'ArrowUp') { e.preventDefault(); (items[i - 1] || items[items.length - 1]).focus(); }
      if (e.key === 'Home') { e.preventDefault(); items[0].focus(); }
      if (e.key === 'End') { e.preventDefault(); items[items.length - 1].focus(); }
      if (e.key === 'Enter' || e.key === ' ') { if (i > -1) { e.preventDefault(); items[i].click(); } }
    });
  }
  // Click outside closes. (Selecting a language is handled in i18n.js; we just close.)
  document.addEventListener('click', function (e) {
    if (!langIsOpen()) return;
    if (langWrap && langWrap.contains(e.target)) return;
    openLang(false);
  });
  document.addEventListener('focusin', function (e) {
    if (!langIsOpen()) return;
    if (langWrap && langWrap.contains(e.target)) return;
    openLang(false);
  });

  // Choosing a language closes the dropdown and the mobile drawer.
  document.addEventListener('click', function (e) {
    if (e.target.closest('button[data-lang]')) { openLang(false); setNav(false); }
  });

  // Global Escape: close whatever overlay is open, whichever control has focus.
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape' && e.key !== 'Esc') return;
    var wasOpen = langIsOpen();
    openLang(false);
    setNav(false);
    closeDrawer();
    if (wasOpen && langBtn) langBtn.focus();
  });

  /* ----------------------------------------------------- shop filtering */
  var grid = $('[data-grid]');
  if (grid) {
    var state = { cat: '', tags: [], diets: [], max: 99999, sort: 'featured' };
    var range = $('[data-price-range]');
    var params = new URLSearchParams(location.search);
    if (params.get('cat')) state.cat = params.get('cat');
    if (params.get('tag')) state.tags = [params.get('tag')];

    function apply() {
      var cards = $$('[data-product-card]', grid), shown = 0, total = 0;
      cards.forEach(function (c) {
        var price = parseFloat(c.getAttribute('data-price'));
        var cat = c.getAttribute('data-cat');
        var tags = (c.getAttribute('data-tags') || '').split(' ');
        var diet = (c.getAttribute('data-diet') || '');
        var ok = (!state.cat || cat === state.cat) &&
          (!state.tags.length || state.tags.every(function (t) { return tags.indexOf(t) > -1; })) &&
          (!state.diets.length || state.diets.every(function (d) { return diet.indexOf(d) > -1; })) &&
          price <= state.max;
        c.hidden = !ok; if (ok) shown++;
        total++;
      });
      if (state.sort !== 'featured') {
        var sorted = cards.slice().sort(function (a, b) {
          var ap = parseFloat(a.getAttribute('data-price')), bp = parseFloat(b.getAttribute('data-price'));
          var ar = parseFloat(a.getAttribute('data-rating')), br = parseFloat(b.getAttribute('data-rating'));
          if (state.sort === 'price-low') return ap - bp;
          if (state.sort === 'price-high') return bp - ap;
          if (state.sort === 'rating') return br - ar;
          if (state.sort === 'new') return (parseInt(b.getAttribute('data-new'), 10) || 0) - (parseInt(a.getAttribute('data-new'), 10) || 0);
          return 0;
        });
        sorted.forEach(function (c) { grid.appendChild(c); });
      }
      var counter = $('[data-result-count]'); if (counter) counter.textContent = shown;
      var empty = $('[data-no-results]'); if (empty) empty.hidden = shown > 0;
      renderActive();
    }

    function renderActive() {
      var box = $('[data-active-filters]');
      if (!box) return;
      var chips = [];
      if (state.cat) chips.push(['cat', state.cat]);
      state.tags.forEach(function (t) { chips.push(['tag', t]); });
      state.diets.forEach(function (d) { chips.push(['diet', d]); });
      if (state.max < 99999) chips.push(['price', '≤ ' + money(state.max)]);
      box.innerHTML = chips.map(function (c) {
        return '<span class="tag">' + c[1] + ' <button type="button" data-drop="' + c[0] + '" data-value="' + c[1] + '" aria-label="Remove filter">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg></button></span>';
      }).join('');
      box.hidden = !chips.length;
      $$('[data-filter]').forEach(function (b) {
        var f = b.getAttribute('data-filter'), v = b.getAttribute('data-value');
        var on = (f === 'cat' && state.cat === v) || (f === 'tag' && state.tags.indexOf(v) > -1) || (f === 'diet' && state.diets.indexOf(v) > -1);
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
    }

    $$('[data-filter]').forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.getAttribute('data-filter'), v = b.getAttribute('data-value');
        if (f === 'cat') state.cat = state.cat === v ? '' : v;
        if (f === 'tag') { var i = state.tags.indexOf(v); i > -1 ? state.tags.splice(i, 1) : state.tags.push(v); }
        if (f === 'diet') { var j = state.diets.indexOf(v); j > -1 ? state.diets.splice(j, 1) : state.diets.push(v); }
        apply();
      });
    });
    if (range) range.addEventListener('input', function () {
      state.max = parseInt(range.value, 10);
      var out = $('[data-price-out]'); if (out) out.textContent = money(state.max);
      apply();
    });
    var sortSel = $('[data-sort]');
    if (sortSel) sortSel.addEventListener('change', function () { state.sort = sortSel.value; apply(); });
    $$('[data-filter-clear]').forEach(function (b) {
      b.addEventListener('click', function () {
        state.cat = ''; state.tags = []; state.diets = []; state.max = 99999;
        if (range) { range.value = range.max; var out = $('[data-price-out]'); if (out) out.textContent = money(parseInt(range.max, 10)); }
        if (sortSel) { sortSel.value = 'featured'; state.sort = 'featured'; }
        apply();
      });
    });
    document.addEventListener('click', function (e) {
      var d = e.target.closest('[data-drop]');
      if (!d) return;
      var kind = d.getAttribute('data-drop');
      if (kind === 'cat') state.cat = '';
      if (kind === 'tag') state.tags = state.tags.filter(function (x) { return x !== d.getAttribute('data-value'); });
      if (kind === 'diet') state.diets = state.diets.filter(function (x) { return x !== d.getAttribute('data-value'); });
      if (kind === 'price') { state.max = 99999; if (range) { range.value = range.max; } }
      apply();
    });
    var toggle = $('[data-filter-toggle]');
    var filtersBox = $('[data-filters]');
    if (toggle && filtersBox) toggle.addEventListener('click', function () {
      var open = filtersBox.getAttribute('data-open') !== 'true';
      filtersBox.setAttribute('data-open', open ? 'true' : 'false');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.textContent = open ? t('common.hide') : t('common.show');
    });
    apply();
  }

  /* -------------------------------------------------------- PDP details */
  var mainImg = $('[data-main-img]');
  $$('[data-thumb]').forEach(function (b) {
    b.addEventListener('click', function () {
      $$('[data-thumb]').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
      b.setAttribute('aria-pressed', 'true');
      var img = b.querySelector('img');
      if (mainImg && img) mainImg.src = img.src;
    });
  });
  var sizeBtns = $$('[data-size-opt]');
  sizeBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      sizeBtns.forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
      b.setAttribute('aria-pressed', 'true');
      var i = b.getAttribute('data-size-opt'), price = b.getAttribute('data-price');
      $$('[data-add],[data-buy]').forEach(function (btn) { btn.setAttribute('data-size', i); });
      var now = $('[data-price-now]');
      if (now) {
        var p = PRODUCTS.filter(function (x) { return x.slug === (b.closest('.pdp') ? document.querySelector('[data-add]').getAttribute('data-add') : ''); })[0];
        var srt = now.querySelector('s');
        now.innerHTML = money(price) + (srt ? '<s>' + srt.textContent + '</s>' : '');
      }
    });
  });

  $$('.tablist .tab').forEach(function (tab) {
    tab.addEventListener('click', function () {
      var list = tab.closest('.tablist');
      $$('.tab', list).forEach(function (x) { x.setAttribute('aria-selected', 'false'); });
      tab.setAttribute('aria-selected', 'true');
      var root = list.parentNode;
      $$('.tabpanel', root).forEach(function (p) { p.hidden = true; });
      var panel = document.getElementById(tab.getAttribute('aria-controls'));
      if (panel) panel.hidden = false;
    });
  });

  var stickyBar = $('[data-sticky-buy]'), pdpBuy = $('.pdp__buy');
  if (stickyBar && pdpBuy && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      var show = !entries[0].isIntersecting && entries[0].boundingClientRect.top < 0;
      stickyBar.setAttribute('data-visible', show ? 'true' : 'false');
      document.body.classList.toggle('has-sticky-buybar', show);
    }, { threshold: 0 }).observe(pdpBuy);
  }

  /* ----------------------------------------------------- checkout page */
  function renderCheckout() {
    var box = $('[data-checkout-lines]');
    if (!box) return;
    var lines = cartLines(), sub = cartSubtotal();
    var cod = (document.querySelector('[name="payment"]:checked') || {}).value === 'cod';
    if (!lines.length) {
      box.innerHTML = '<p class="muted small">' + t('cart.empty') + ' <a href="' + url('shop/') + '">' + t('common.shop') + '</a></p>';
    } else {
      box.innerHTML = lines.map(function (l) {
        var img = url(l.p.img);
        return '<div class="os-line"><img src="' + img + '" alt=""><div>' +
          '<p class="os-line__t">' + pname(l.p) + '</p><p class="os-line__m">' + l.size.label + ' · × ' + l.qty + '</p></div>' +
          '<span>' + money(l.lineTotal) + '</span></div>';
      }).join('');
    }
    var ship = shipFee(sub), codFee = cod ? COD_FEE : 0, total = sub + ship + codFee;
    function set(sel, val) { var el = $(sel); if (el) el.textContent = val; }
    set('[data-co-subtotal]', money(sub));
    set('[data-co-ship]', sub === 0 ? '—' : (ship ? money(ship) : t('cart.free')));
    set('[data-co-cod]', codFee ? money(codFee) : '—');
    set('[data-co-total]', money(total));
    set('[data-co-school]', Math.round(sub * SCHOOL_PCT / 100));
    return { sub: sub, ship: ship, codFee: codFee, total: total };
  }
  renderCheckout();

  /* -------------------------------------------------------------- forms */
  var PHONE_RE = /^(\+?91[-\s]?)?[6-9]\d{9}$/;
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i;

  function fieldError(input, on, msg) {
    var f = input.closest('.field');
    if (f) {
      f.classList.toggle('has-error', !!on);
      if (msg) { var e = f.querySelector('.field__error'); if (e) e.textContent = msg; }
    }
    input.setAttribute('aria-invalid', on ? 'true' : 'false');
  }

  function validate(form) {
    var ok = true, first = null;
    $$('[required]', form).forEach(function (input) {
      var v = (input.value || '').trim();
      var bad = !v;
      if (!bad && input.type === 'tel') bad = !PHONE_RE.test(v.replace(/\s|-/g, ''));
      if (!bad && input.type === 'email') bad = !EMAIL_RE.test(v);
      if (!bad && input.name === 'pincode') bad = !/^\d{6}$/.test(v);
      if (!bad && input.type === 'checkbox') bad = !input.checked;
      fieldError(input, bad);
      if (bad && !first) first = input;
      ok = ok && !bad;
    });
    if (first) { first.focus(); first.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
    return ok;
  }

  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form.matches('[data-form]')) return;
    e.preventDefault();
    var kind = form.getAttribute('data-form');
    var okEl = form.querySelector('[data-msg="ok"]'), errEl = form.querySelector('[data-msg="err"]');
    if (!validate(form)) {
      if (errEl) errEl.hidden = false;
      toast('Please check the highlighted fields', 'error');
      return;
    }
    if (errEl) errEl.hidden = true;

    if (kind === 'checkout') {
      var totals = renderCheckout();
      var btn = form.querySelector('[data-place-order]');
      if (btn) { btn.disabled = true; btn.innerHTML = t('common.sending'); }
      var orderId = 'AP-' + new Date().toISOString().slice(2, 10).replace(/-/g, '') + '-' + Math.floor(1000 + Math.random() * 8999);
      var key = CFG.razorpayKey;
      var finish = function () {
        var success = $('[data-checkout-success]');
        var oid = $('[data-order-id]'); if (oid) oid.textContent = orderId;
        var holder = document.querySelector('.checkout-layout');
        if (holder) holder.hidden = true;
        var hero = document.querySelector('.post-hero');
        if (hero) hero.hidden = true;
        if (success) { success.hidden = false; success.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
        cart.items = []; saveCart(); renderCart();
        if (btn) { btn.disabled = false; }
      };
      var payNow = function () {
        if (key && window.Razorpay) {
          var rzp = new window.Razorpay({
            key: key, amount: Math.round((totals ? totals.total : 0) * 100), currency: 'INR',
            name: 'ApnaPan', description: 'Order ' + orderId,
            prefill: { name: form.name.value, contact: form.phone.value, email: form.email.value },
            theme: { color: '#b4552d' },
            handler: finish,
            modal: { ondismiss: function () { if (btn) { btn.disabled = false; btn.innerHTML = t('co.place'); } } }
          });
          rzp.open();
        } else { setTimeout(finish, 700); }
      };
      payNow();
      return;
    }
    if (okEl) okEl.hidden = false;
    toast(kind === 'newsletter' ? 'You are subscribed' : 'Message received — thank you');
    form.querySelectorAll('input, textarea, select').forEach(function (i) {
      if (i.type === 'checkbox') i.checked = false; else if (i.type !== 'submit') i.value = '';
    });
    okEl && okEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });

  /* ------------------------------------------------- counters + reveals */
  function animateCount(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var dur = 1200, start = performance.now();
    function step(now) {
      var p = Math.min(1, (now - start) / dur);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased).toLocaleString('en-IN');
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        if (en.target.hasAttribute('data-count') && !en.target.dataset.done) { en.target.dataset.done = '1'; animateCount(en.target); }
        if (en.target.classList.contains('reveal')) en.target.classList.add('is-in');
        if (en.target.hasAttribute('data-alloc')) en.target.style.width = en.target.getAttribute('data-alloc') + '%';
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    $$('[data-count],[data-alloc],.reveal').forEach(function (el) { io.observe(el); });
  } else {
    $$('[data-count]').forEach(function (el) { el.textContent = Number(el.getAttribute('data-count')).toLocaleString('en-IN'); });
    $$('[data-alloc]').forEach(function (el) { el.style.width = el.getAttribute('data-alloc') + '%'; });
    $$('.reveal').forEach(function (el) { el.classList.add('is-in'); });
  }

  /* --------------------------------------------------------- misc chrome */
  var header = $('#siteHeader');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-stuck', window.scrollY > 6); };
    window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  }
  var toTop = $('[data-to-top]');
  if (toTop) {
    window.addEventListener('scroll', function () { toTop.setAttribute('data-visible', window.scrollY > 700 ? 'true' : 'false'); }, { passive: true });
    toTop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  }
  // wishlist state
  var wish = {}; try { wish = JSON.parse(store.get(WISH_KEY)) || {}; } catch (e) {}
  Object.keys(wish).forEach(function (k) {
    if (!wish[k]) return;
    var b = document.querySelector('[data-wish="' + k + '"]');
    if (b) b.setAttribute('aria-pressed', 'true');
  });

  /* ------------------------------------------------------- colour theme
     Light is the original design; dark is a purely additive stylesheet. The
     attribute is normally already set by the inline script in <head> (which
     runs before first paint); this module keeps the controls in sync, saves
     the choice, and follows the OS while no explicit choice has been made. */
  var THEME_KEY = 'apnapan_theme';
  var THEME_COLOR = { light: '#1e4436', dark: '#1c140e' };
  var mq = null;

  function themeNow() {
    return document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
  }

  function syncThemeControls(theme) {
    var goingTo = theme === 'dark' ? 'light' : 'dark';
    var label = t('theme.to' + goingTo.charAt(0).toUpperCase() + goingTo.slice(1));
    $$('[data-theme-toggle]').forEach(function (b) {
      b.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
      b.setAttribute('aria-label', label);
    });
    $$('[data-theme-set]').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-theme-set') === theme ? 'true' : 'false');
    });
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', THEME_COLOR[theme]);
  }

  function applyTheme(theme, persist) {
    theme = theme === 'dark' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', theme);
    if (persist) store.set(THEME_KEY, theme);
    syncThemeControls(theme);
  }

  function storedTheme() {
    var v = store.get(THEME_KEY);
    return (v === 'dark' || v === 'light') ? v : null;
  }

  applyTheme(themeNow(), false);

  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-theme-toggle]')) {
      applyTheme(themeNow() === 'dark' ? 'light' : 'dark', true);
      return;
    }
    var set = e.target.closest('[data-theme-set]');
    if (set) applyTheme(set.getAttribute('data-theme-set'), true);
  });

  /* while the visitor has not chosen for themselves, follow the system */
  if (window.matchMedia) {
    mq = window.matchMedia('(prefers-color-scheme: dark)');
    var onScheme = function (e) { if (!storedTheme()) applyTheme(e.matches ? 'dark' : 'light', false); };
    if (mq.addEventListener) mq.addEventListener('change', onScheme);
    else if (mq.addListener) mq.addListener(onScheme);
  }

  /* the toggle's label is written by JS, so re-translate it on language change */
  document.addEventListener('apnapan:lang', function (e) {
    LANG = (e.detail && e.detail.lang) || LANG;
    syncThemeControls(themeNow());
  });

  /* language switch re-renders the cart & checkout in the chosen tongue */
  document.addEventListener('apnapan:lang', function (e) {
    LANG = e.detail.lang; renderCart(); renderCheckout();
  });

  renderCart();
})();
