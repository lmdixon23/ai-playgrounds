#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
ORIGINAL = {
    "search-pathfinding","hill-climbing","wumpus-world","cnf-sat","bayes-classifier","bayes-network",
    "knn-classifier","overfitting","neural-network","kmeans","convolution","q-learning-gridworld",
}
MODERN = {"transformer-language-model","agent-tool-context","minimax-alpha-beta"}


def launch(playwright):
    args=["--no-sandbox","--disable-dev-shm-usage"]
    managed=pathlib.Path(playwright.chromium.executable_path)
    if managed.exists(): return playwright.chromium.launch(headless=True,args=args)
    for name in ("chromium","chromium-browser","google-chrome","chrome"):
        candidate=shutil.which(name)
        if candidate: return playwright.chromium.launch(headless=True,executable_path=candidate,args=args)
    return playwright.chromium.launch(headless=True,args=args)


def main() -> int:
    build=subprocess.run([sys.executable,str(ROOT/"tools"/"build_site_v1_6_1_consistency.py")],cwd=ROOT,text=True,capture_output=True,check=False)
    if build.returncode:
        print(build.stdout);print(build.stderr,file=sys.stderr);return build.returncode
    checks=[]
    def check(name,ok,detail=None): checks.append((name,bool(ok),detail or {}))

    manifest=json.loads((SITE/"applets.json").read_text(encoding="utf-8"))
    by_slug={x["slug"]:x for x in manifest}
    required=("icon","category","category_en","category_zh","category_vi","category_es","title","title_zh","title_vi","title_es","desc","desc_zh","desc_vi","desc_es","featured","featured_zh","featured_vi","featured_es","keywords","accent","accent_name")
    check("15-app manifest is complete",len(manifest)==15 and all(all(x.get(k) for k in required) for x in manifest),{"count":len(manifest)})
    check("Lab 15 complete card schema",all(by_slug["minimax-alpha-beta"].get(k) for k in required),by_slug["minimax-alpha-beta"])

    home=(SITE/"index.html").read_text(encoding="utf-8")
    check("home has four-locale runtime","v161-home-four-locale-runtime" in home and 'hreflang="vi"' in home and 'hreflang="es"' in home)
    check("home has no literal undefined","undefinedundefined" not in home and ">undefined<" not in home)
    check("home current copy says fifteen","Explore the fifteen applets" in home and "15 inspectable applets" in home)
    check("home JSON-LD declares four languages",'"inLanguage":["en","zh","vi","es"]' in home)
    for slug in MODERN:
        source=(SITE/"playgrounds"/slug/"index.html").read_text(encoding="utf-8")
        check(f"{slug} standard shell",source.count('data-ap-standard-shell')==1 and source.count('data-ap-standard-footer')==1)
    r4=(SITE/"assets"/"localization-r4.js").read_text(encoding="utf-8")
    check("R4 source retention patch applied","preserve canonical source text across VI/ES round trips" in r4)
    for page_name in ("teacher-pack.html","curriculum.html","quality.html","research-and-citation.html"):
        source=(SITE/page_name).read_text(encoding="utf-8")
        if "v14-language-select" in source:
            check(f"{page_name} selector shell flattened",'id="v161-select-shell-fix"' in source)

    page_errors=[];console_errors=[]
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright required") from exc

    with sync_playwright() as p:
        browser=launch(p)
        try:
            ctx=browser.new_context(viewport={"width":1280,"height":900},reduced_motion="reduce")
            page=ctx.new_page()
            page.on("pageerror",lambda exc:page_errors.append(str(exc)))
            page.on("console",lambda msg:console_errors.append(msg.text) if msg.type=="error" else None)
            page.goto((SITE/"index.html").resolve().as_uri(),wait_until="load",timeout=20_000)
            page.wait_for_selector("#ap-home-language-select",timeout=5_000)
            check("home native selector has four languages",page.locator("#ap-home-language-select option").count()==4)
            check("home renders 15 cards",page.locator("#appletGrid .applet").count()==15,{"cards":page.locator("#appletGrid .applet").count()})
            check("home has one applet section heading",page.locator("#applets .section-head h2").count()==1)
            check("home card output contains no undefined","undefined" not in page.locator("#appletGrid").inner_text().lower())

            for query,slug in (("QKV","transformer-language-model"),("MCP","agent-tool-context"),("DPLL","cnf-sat"),("alpha beta","minimax-alpha-beta"),("Bellman","q-learning-gridworld")):
                page.fill("#search",query);page.wait_for_timeout(30)
                links=page.locator("#appletGrid .applet")
                hrefs=[links.nth(i).get_attribute("href") or "" for i in range(links.count())]
                check(f"search vocabulary: {query}",any(slug in href for href in hrefs),{"hrefs":hrefs})
            page.fill("#search","")

            for locale in ("vi","es"):
                page.select_option("#ap-home-language-select",locale);page.wait_for_timeout(40)
                check(f"home switches to {locale}",(page.locator("html").get_attribute("lang") or "").startswith(locale))
                check(f"home {locale} translates applet heading",page.locator("#applets h2").inner_text()!= "Explore the fifteen applets")
            page.select_option("#ap-home-language-select","en");page.wait_for_timeout(40)
            check("home round trip restores English",page.locator("#applets h2").inner_text()=="Explore the fifteen applets")

            page.goto((SITE/"teacher-pack.html").resolve().as_uri(),wait_until="load",timeout=20_000)
            sel=page.locator(".support-language-switch .v14-language-select")
            if sel.count():
                style=page.locator(".support-language-switch").evaluate("el=>{const s=getComputedStyle(el);return {bw:s.borderTopWidth,ov:s.overflow,bg:s.backgroundColor}}")
                check("Teacher Pack language selector wrapper is visually flattened",style["bw"]=="0px" and style["ov"]=="visible",style)

            for slug in sorted(ORIGINAL):
                page.goto((SITE/"playgrounds"/slug/"index.html").resolve().as_uri()+"?lang=en",wait_until="load",timeout=20_000)
                page.wait_for_selector(".r4-language-select",timeout=5_000)
                original_h1=page.locator("h1").first.inner_text()
                original_title=page.title()
                for locale in ("vi","es"):
                    page.select_option(".r4-language-select",locale);page.wait_for_timeout(35)
                    page.select_option(".r4-language-select","en");page.wait_for_timeout(35)
                    check(f"{slug} {locale}->EN h1 restores",page.locator("h1").first.inner_text()==original_h1,{"expected":original_h1,"actual":page.locator("h1").first.inner_text()})
                    check(f"{slug} {locale}->EN title restores",page.title()==original_title,{"expected":original_title,"actual":page.title()})

            for slug in sorted(MODERN):
                page.goto((SITE/"playgrounds"/slug/"index.html").resolve().as_uri()+"?lang=en",wait_until="load",timeout=20_000)
                page.wait_for_selector("#ap-standard-language-select",timeout=5_000)
                original=page.locator("#ap-standard-title").inner_text()
                for locale in ("vi","es"):
                    page.select_option("#ap-standard-language-select",locale);page.wait_for_timeout(50)
                    changed=page.locator("#ap-standard-title").inner_text()
                    check(f"{slug} shared shell translates {locale}",changed!=original,{"title":changed})
                    page.select_option("#ap-standard-language-select","en");page.wait_for_timeout(50)
                    check(f"{slug} shared shell restores EN from {locale}",page.locator("#ap-standard-title").inner_text()==original)
            ctx.close()

            mobile=browser.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True,reduced_motion="reduce")
            mpage=mobile.new_page()
            for relative in ["index.html","teacher-pack.html"]+[f"playgrounds/{s}/index.html" for s in sorted(MODERN)]:
                mpage.goto((SITE/relative).resolve().as_uri(),wait_until="load",timeout=20_000)
                overflow=mpage.evaluate("()=>Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)-innerWidth")
                check(f"390px final composition containment: {relative}",overflow<=1,{"overflow":overflow})
            mobile.close()
        finally:
            browser.close()

    failures=[{"name":n,"detail":d} for n,ok,d in checks if not ok]
    payload={"harness":"tools/test_v1_6_1_design_consistency.py","checks":len(checks),"passed":len(checks)-len(failures),"failed":len(failures),"page_errors":page_errors,"console_errors":console_errors,"pass":not failures and not page_errors and not console_errors,"failures":failures}
    print(json.dumps(payload,indent=2,ensure_ascii=False))
    return 0 if payload["pass"] else 1

if __name__=="__main__": raise SystemExit(main())
