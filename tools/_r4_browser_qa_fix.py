#!/usr/bin/env python3
from pathlib import Path

p=Path('tools/browser_qa.py')
s=p.read_text(encoding='utf-8')
old='''                if lang_count >= 2:\n                    page.locator("button[data-lang='zh']").first.click(timeout=1500)\n                    checks.append({"name": "zh_toggle_active", "pass": page.locator("button[data-lang='zh'].active").count() >= 1, "detail": {"active_count": page.locator("button[data-lang='zh'].active").count()}})\n                    page.locator("button[data-lang='en']").first.click(timeout=1500)\n                    checks.append({"name": "en_toggle_active", "pass": page.locator("button[data-lang='en'].active").count() >= 1, "detail": {"active_count": page.locator("button[data-lang='en'].active").count()}})\n'''
new='''                if lang_count >= 2:\n                    r4_ready = bool(page.evaluate("() => !!window.__r4Localization && window.__r4Localization.ready()"))\n                    switch_applet_locale(page, "zh")\n                    if r4_ready:\n                        zh_value = page.locator(".r4-language-select").input_value() if page.locator(".r4-language-select").count() else ""\n                        checks.append({"name": "zh_toggle_active", "pass": document_lang(page).lower().startswith("zh") and zh_value == "zh", "detail": {"lang": document_lang(page), "select": zh_value}})\n                    else:\n                        checks.append({"name": "zh_toggle_active", "pass": page.locator("button[data-lang='zh'].active").count() >= 1, "detail": {"active_count": page.locator("button[data-lang='zh'].active").count()}})\n                    switch_applet_locale(page, "en")\n                    if r4_ready:\n                        en_value = page.locator(".r4-language-select").input_value() if page.locator(".r4-language-select").count() else ""\n                        checks.append({"name": "en_toggle_active", "pass": document_lang(page).lower().startswith("en") and en_value == "en", "detail": {"lang": document_lang(page), "select": en_value}})\n                    else:\n                        checks.append({"name": "en_toggle_active", "pass": page.locator("button[data-lang='en'].active").count() >= 1, "detail": {"active_count": page.locator("button[data-lang='en'].active").count()}})\n'''
count=s.count(old)
if count != 1:
    raise SystemExit(f'browser QA language-toggle binding failed: expected 1 occurrence, found {count}')
s=s.replace(old,new,1)
if 'page.locator("button[data-lang=\'zh\']").first.click(timeout=1500)' in s:
    raise SystemExit('legacy direct applet ZH click remains')
p.write_text(s,encoding='utf-8',newline='\n')
print('R4_BROWSER_QA_COMPATIBILITY_FIX=PASS')
