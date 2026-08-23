(() => {
  'use strict';

  const SUPPORTED = ['en', 'zh', 'vi', 'es'];
  const SELF_NAMES = { en: 'English', zh: '简体中文', vi: 'Tiếng Việt', es: 'Español' };
  const LOCALE_KEY = 'ai-playgrounds-locale4';
  const slug = location.pathname.split('/').filter(Boolean).slice(-2, -1)[0] || 'applet';
  const rootData = window.__AI_PLAYGROUNDS_R4_LOCALES || {};
  const data = rootData[slug] || null;

  // R4 stays invisible until the applet-specific VI/ES catalog is complete.
  if (!data || data.ready !== true || !data.vi || !data.es) return;

  let current = 'en';
  let applying = false;
  let nativeLanguageClick = false;
  const originalText = new WeakMap();
  const originalAttrs = new WeakMap();
  // MutationObserver callbacks are asynchronous, so a simple `applying` boolean
  // cannot distinguish our own translated writes from later applet updates.
  // Remember the exact values written by the localization layer instead.
  const lastAppliedText = new WeakMap();
  const lastAppliedAttrs = new WeakMap();
  const ordered = { vi: null, es: null };

  function normalizeLocale(value) {
    const raw = String(value || '').toLowerCase();
    if (raw === 'zh-hans' || raw.startsWith('zh')) return 'zh';
    if (raw.startsWith('vi')) return 'vi';
    if (raw.startsWith('es')) return 'es';
    return 'en';
  }

  function initialLocale() {
    try {
      const q = new URLSearchParams(location.search).get('lang');
      if (q && SUPPORTED.includes(normalizeLocale(q))) return normalizeLocale(q);
      const saved = localStorage.getItem(LOCALE_KEY);
      if (saved && SUPPORTED.includes(normalizeLocale(saved))) return normalizeLocale(saved);
    } catch (_) {}
    return normalizeLocale(document.documentElement.lang || 'en');
  }

  function mapFor(locale) {
    const common = rootData.common && rootData.common[locale] ? rootData.common[locale] : {};
    const local = data[locale] && data[locale].strings ? data[locale].strings : {};
    return Object.assign({}, common, local);
  }

  function orderedPairs(locale) {
    if (ordered[locale]) return ordered[locale];
    const map = mapFor(locale);
    ordered[locale] = Object.entries(map)
      .filter(([source, target]) => source && target && source !== target)
      .sort((a, b) => b[0].length - a[0].length);
    return ordered[locale];
  }

  function translateString(value, locale = current) {
    const input = String(value == null ? '' : value);
    if (locale !== 'vi' && locale !== 'es') return input;
    const map = mapFor(locale);
    if (Object.prototype.hasOwnProperty.call(map, input)) return map[input];
    let out = input;
    for (const [source, target] of orderedPairs(locale)) {
      if (source.length < 4 || !out.includes(source)) continue;
      out = out.split(source).join(target);
    }
    const patterns = (data[locale] && data[locale].patterns) || [];
    for (const row of patterns) {
      try { out = out.replace(new RegExp(row.source, row.flags || 'g'), row.target); } catch (_) {}
    }
    return out;
  }

  function skipNode(node) {
    const el = node && (node.nodeType === 1 ? node : node.parentElement);
    if (!el) return true;
    return !!el.closest('script,style,noscript,template,code,pre,kbd,samp,.lang-switch,[data-r4-no-translate]');
  }

  function textSource(node) {
    if (!originalText.has(node)) originalText.set(node, node.nodeValue || '');
    return originalText.get(node);
  }

  function attrState(el) {
    if (!originalAttrs.has(el)) originalAttrs.set(el, {});
    return originalAttrs.get(el);
  }

  function translateTextNode(node) {
    if (skipNode(node)) return;
    const live = node.nodeValue || '';
    if (!applying && current !== 'vi' && current !== 'es') originalText.set(node, live);
    if (!applying && (current === 'vi' || current === 'es')) originalText.set(node, live);
    const source = textSource(node);
    const translated = translateString(source);
    if (translated !== live) {
      lastAppliedText.set(node, translated);
      applying = true;
      node.nodeValue = translated;
      applying = false;
    }
  }

  function translateAttributes(el) {
    if (!el || el.nodeType !== 1 || skipNode(el)) return;
    const state = attrState(el);
    for (const attr of ['title', 'aria-label', 'placeholder']) {
      if (!el.hasAttribute(attr)) continue;
      const live = el.getAttribute(attr) || '';
      if (!applying) state[attr] = live;
      const source = Object.prototype.hasOwnProperty.call(state, attr) ? state[attr] : live;
      const translated = translateString(source);
      if (translated !== live) {
        const applied = lastAppliedAttrs.get(el) || {};
        applied[attr] = translated;
        lastAppliedAttrs.set(el, applied);
        applying = true;
        el.setAttribute(attr, translated);
        applying = false;
      }
    }
  }

  function translateTree(root = document.body) {
    if (current !== 'vi' && current !== 'es' || !root) return;
    if (root.nodeType === Node.TEXT_NODE) translateTextNode(root);
    if (root.nodeType === Node.ELEMENT_NODE) translateAttributes(root);
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (node.nodeType === Node.TEXT_NODE) translateTextNode(node);
      else translateAttributes(node);
    }
  }

  function restoreTree(root = document.body) {
    if (!root) return;
    applying = true;
    try {
      if (root.nodeType === Node.TEXT_NODE && originalText.has(root)) root.nodeValue = originalText.get(root);
      if (root.nodeType === Node.ELEMENT_NODE && originalAttrs.has(root)) {
        const state = originalAttrs.get(root);
        Object.entries(state).forEach(([a, v]) => root.setAttribute(a, v));
      }
      const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const node = walker.currentNode;
        if (node.nodeType === Node.TEXT_NODE && originalText.has(node)) node.nodeValue = originalText.get(node);
        else if (node.nodeType === Node.ELEMENT_NODE && originalAttrs.has(node)) {
          const state = originalAttrs.get(node);
          Object.entries(state).forEach(([a, v]) => root.setAttribute(a, v));
        }
      }
    } finally { applying = false; }
  }

  function nativeButton(locale) {
    return document.querySelector(`.lang-switch button[data-lang="${locale}"]`);
  }

  function clickNative(locale) {
    const btn = nativeButton(locale);
    if (!btn) return false;
    const hardReset = document.querySelector('#hardReset');
    const hardResetClick = hardReset && typeof hardReset.click === 'function' ? hardReset.click : null;
    nativeLanguageClick = true;
    try {
      // Some legacy language handlers call hardReset.click() synchronously while
      // refreshing their translated surface. R4 uses those handlers only as an
      // internal EN/ZH rendering bridge, so suppress that internal reset at the
      // call site before any click event can be dispatched. The original method
      // is restored immediately; user-initiated resets are unaffected.
      if (hardReset && hardResetClick) {
        hardReset.click = function () {
          if (nativeLanguageClick) return;
          return hardResetClick.call(this);
        };
      }
      btn.click();
    } finally {
      if (hardReset && hardResetClick) hardReset.click = hardResetClick;
      nativeLanguageClick = false;
    }
    return true;
  }

  function updateUrl(locale) {
    try {
      const u = new URL(location.href);
      u.searchParams.set('lang', locale);
      history.replaceState(null, '', u);
    } catch (_) {}
  }

  function persist(locale) {
    try { localStorage.setItem(LOCALE_KEY, locale); } catch (_) {}
  }

  function metaSource(kind) {
    const meta = data.meta && data.meta.en ? data.meta.en : {};
    return meta[kind] || '';
  }

  function applyMetadata(locale) {
    const localeMeta = data.meta && data.meta[locale] ? data.meta[locale] : {};
    const title = locale === 'en' ? metaSource('title') : (localeMeta.title || translateString(metaSource('title'), locale));
    const description = locale === 'en' ? metaSource('description') : (localeMeta.description || translateString(metaSource('description'), locale));
    if (title) {
      document.title = title;
      document.querySelectorAll('meta[property="og:title"],meta[name="twitter:title"]').forEach(el => el.setAttribute('content', title));
    }
    if (description) {
      document.querySelector('meta[name="description"]')?.setAttribute('content', description);
      document.querySelectorAll('meta[property="og:description"],meta[name="twitter:description"]').forEach(el => el.setAttribute('content', description));
    }
  }

  function refreshKnownLayers() {
    for (const name of ['refreshLearnerContent', 'renderAppletKeyTerms', 'renderEssayPrimer', 'refreshAppletToolbar', 'renderAccessibilityLayer', 'renderScenarioGallery', 'renderTour']) {
      try { if (typeof window[name] === 'function') window[name](); } catch (_) {}
    }
  }

  function wrapTr() {
    if (typeof window.tr !== 'function' || window.tr.__r4Wrapped) return;
    const base = window.tr;
    const wrapped = function(key, en, zh) {
      if (current === 'vi' || current === 'es') return translateString(en, current);
      return base.apply(this, arguments);
    };
    wrapped.__r4Wrapped = true;
    window.tr = wrapped;
  }

  function patchClipboard() {
    try {
      const clipboard = navigator.clipboard;
      if (!clipboard || typeof clipboard.writeText !== 'function' || clipboard.writeText.__r4Wrapped) return;
      const base = clipboard.writeText.bind(clipboard);
      const wrapped = text => base(current === 'vi' || current === 'es' ? translateString(String(text), current) : text);
      wrapped.__r4Wrapped = true;
      navigator.clipboard.writeText = wrapped;
    } catch (_) {}
  }

  function selectControl() {
    return document.querySelector('.r4-language-select');
  }

  function updateSelect(locale) {
    const select = selectControl();
    if (select) select.value = locale;
  }

  function activateOverlay(locale) {
    current = locale;
    document.documentElement.lang = locale;
    refreshKnownLayers();
    wrapTr();
    patchClipboard();
    applyMetadata(locale);
    translateTree(document.body);
    updateSelect(locale);
    updateUrl(locale);
    persist(locale);
    window.dispatchEvent(new CustomEvent('r4languagechange', { detail: { locale } }));
  }

  function setLocale(locale, options = {}) {
    locale = normalizeLocale(locale);
    if (!SUPPORTED.includes(locale)) locale = 'en';
    restoreTree(document.body);
    if (locale === 'en' || locale === 'zh') {
      current = locale;
      clickNative(locale);
      document.documentElement.lang = locale === 'zh' ? 'zh' : 'en';
      applyMetadata(locale);
      updateSelect(locale);
      updateUrl(locale);
      persist(locale);
      window.dispatchEvent(new CustomEvent('r4languagechange', { detail: { locale } }));
      return;
    }
    // Existing applet code remains the source of state. VI/ES overlays are always
    // generated from its English rendering, never translated from translated text.
    current = 'en';
    clickNative('en');
    setTimeout(() => activateOverlay(locale), options.immediate ? 0 : 60);
  }

  function installSelect() {
    const holder = document.querySelector('.lang-switch');
    if (!holder || holder.querySelector('.r4-language-select')) return;
    const select = document.createElement('select');
    select.className = 'r4-language-select';
    select.setAttribute('aria-label', 'Language');
    select.setAttribute('data-r4-no-translate', '1');
    for (const locale of SUPPORTED) {
      const option = document.createElement('option');
      option.value = locale;
      option.textContent = SELF_NAMES[locale];
      select.appendChild(option);
    }
    holder.appendChild(select);
    holder.classList.add('r4-locale-ready');
    select.addEventListener('change', () => setLocale(select.value));
  }

  const observer = new MutationObserver(mutations => {
    if (applying) return;
    for (const mutation of mutations) {
      if (mutation.type === 'characterData') {
        const live = mutation.target.nodeValue || '';
        if (lastAppliedText.get(mutation.target) === live) {
          lastAppliedText.delete(mutation.target);
          continue;
        }
        // Applet-authored dynamic state is always a new source value, including
        // while English or Chinese is active. This is what prevents a later locale
        // switch from restoring stale page-load state.
        originalText.set(mutation.target, live);
        if (current === 'vi' || current === 'es') translateTextNode(mutation.target);
      } else if (mutation.type === 'attributes') {
        const attr = mutation.attributeName;
        const live = mutation.target.getAttribute(attr) || '';
        const applied = lastAppliedAttrs.get(mutation.target) || {};
        if (applied[attr] === live) {
          delete applied[attr];
          lastAppliedAttrs.set(mutation.target, applied);
          continue;
        }
        const state = attrState(mutation.target);
        state[attr] = live;
        if (current === 'vi' || current === 'es') translateAttributes(mutation.target);
      } else {
        mutation.addedNodes.forEach(node => {
          if (current === 'vi' || current === 'es') translateTree(node);
        });
      }
    }
  });

  function init() {
    installSelect();
    wrapTr();
    patchClipboard();
    observer.observe(document.body, { subtree:true, childList:true, characterData:true, attributes:true, attributeFilter:['title','aria-label','placeholder'] });
    // Secondary guard for legacy handlers that dispatch a reset event directly
    // rather than calling the element's click() method. The clickNative() call-site
    // guard above prevents the normal path before dispatch; this capture guard
    // covers direct dispatch while R4 is bridging locales.
    document.addEventListener('click', event => {
      if (!nativeLanguageClick) return;
      const target = event.target;
      if (target && target.closest && target.closest('#hardReset')) {
        event.preventDefault();
        event.stopImmediatePropagation();
      }
    }, true);
    document.querySelectorAll('.lang-switch button[data-lang]').forEach(button => {
      button.addEventListener('click', () => {
        if (nativeLanguageClick) return;
        const locale = normalizeLocale(button.dataset.lang);
        current = locale;
        updateSelect(locale);
        persist(locale);
      });
    });
    setLocale(initialLocale(), { immediate:true });
    window.__r4Localization = {
      locale: () => current,
      setLocale,
      translateString,
      ready: () => !!data && data.ready === true,
      supported: () => [...SUPPORTED],
      slug,
    };
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => setTimeout(init, 0), { once:true });
  else setTimeout(init, 0);
})();
