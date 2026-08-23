#!/usr/bin/env python3
from pathlib import Path

p=Path('assets/localization-r4.js')
s=p.read_text(encoding='utf-8')

def one(old,new,label):
    global s
    n=s.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 occurrence, found {n}')
    s=s.replace(old,new,1)

one(
"          Object.entries(state).forEach(([a, v]) => root.setAttribute(a, v));",
"          Object.entries(state).forEach(([a, v]) => node.setAttribute(a, v));",
'restoreTree descendant target')

one(
"      navigator.clipboard.writeText = wrapped;",
"      clipboard.writeText = wrapped;",
'clipboard wrapper target')

start=s.index('  function clickNative(locale) {')
end=s.index('\n\n  function updateUrl(locale)', start)
old=s[start:end]
new="""  function nativeLocale() {
    const active = document.querySelector('.lang-switch button[data-lang].active');
    return normalizeLocale((active && active.dataset.lang) || document.documentElement.lang || 'en');
  }

  function clickNative(locale) {
    locale = normalizeLocale(locale);
    const btn = nativeButton(locale);
    if (!btn) return false;
    // Locale bridging must be idempotent. On initial page load the applet is
    // already English; clicking EN again can run legacy reset/rebuild handlers
    // after Guided Challenge setup has started. Skip the bridge entirely when
    // the native interface already matches the requested locale.
    if (nativeLocale() === locale) return true;
    nativeLanguageClick = true;
    try { btn.click(); } finally { nativeLanguageClick = false; }
    return true;
  }"""
if 'hardResetClick' not in old:
    raise SystemExit('clickNative binding: expected d030 hard-reset wrapper not found')
s=s[:start]+new+s[end:]

# Preserve the capture-phase secondary guard; it remains useful only while a
# real native bridge is in progress. Assert the guard still exists.
for token in [
    "if (!nativeLanguageClick) return;",
    "target.closest('#hardReset')",
    "setLocale(initialLocale(), { immediate:true });",
]:
    if token not in s:
        raise SystemExit(f'locale bridge invariant missing after patch: {token}')

# Regression assertions for the exact bugs this repair closes.
if "Object.entries(state).forEach(([a, v]) => root.setAttribute(a, v));" in s:
    raise SystemExit('restoreTree root-target regression remains')
if 'hardResetClick' in s:
    raise SystemExit('synchronous hardReset monkeypatch remains')
if "navigator.clipboard.writeText = wrapped;" in s:
    raise SystemExit('clipboard regression remains')

p.write_text(s,encoding='utf-8',newline='\n')
print('R4_LOCALE_BRIDGE_IDEMPOTENCE_FIX=PASS')
