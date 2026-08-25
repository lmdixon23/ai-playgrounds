#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import build_site_v1_4

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "_site" / "playgrounds" / "cnf-sat" / "index.html"

TRACE_EXPOSURE = r'''

  // Read-only presentation adapter for the engagement-excellence candidate.
  // It exposes the already-computed DPLL trace without creating a second solver.
  window.__cnfDpllPresentationState = {
    getTrace: () => JSON.parse(JSON.stringify(dpllSteps)),
    getVars: () => dpllVarList.slice(),
    getIndex: () => dpllStepper ? dpllStepper.index : 0,
    getRows: () => dpllRows
  };
'''

CSS = r'''
<style id="cnf-engagement-excellence-style">
.cnf-eq-tree{margin-top:12px;padding:13px;border:1px solid color-mix(in srgb,var(--accent) 30%,var(--border));border-radius:12px;background:linear-gradient(180deg,color-mix(in srgb,var(--card) 94%,var(--accent)),var(--card))}.cnf-eq-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;flex-wrap:wrap}.cnf-eq-head strong{display:block;color:var(--accent);font-size:.8rem;text-transform:uppercase;letter-spacing:.05em}.cnf-eq-head p{margin:3px 0 0;color:var(--muted);font-size:.82rem;max-width:800px}.cnf-eq-metric{color:var(--muted);font:11px/1.4 ui-monospace,monospace;padding:5px 8px;border:1px solid var(--border);border-radius:999px;background:var(--card)}.cnf-eq-svg-wrap{margin-top:10px;border:1px solid var(--border);border-radius:10px;background:var(--card);overflow:auto;min-height:210px}.cnf-eq-svg{display:block;width:100%;min-width:580px;height:auto;min-height:210px}.cnf-eq-edge{stroke:var(--border);stroke-width:2;fill:none}.cnf-eq-node circle{fill:var(--card);stroke:var(--muted);stroke-width:2}.cnf-eq-node text{font:11px ui-monospace,monospace;fill:var(--fg);text-anchor:middle;pointer-events:none}.cnf-eq-node.past circle{stroke:var(--accent)}.cnf-eq-node.current circle{stroke:var(--accent);stroke-width:4;filter:drop-shadow(0 0 5px color-mix(in srgb,var(--accent) 34%,transparent))}.cnf-eq-node.sat circle{stroke:var(--true);fill:color-mix(in srgb,var(--card) 86%,var(--true))}.cnf-eq-node.unsat circle{stroke:var(--false);fill:color-mix(in srgb,var(--card) 86%,var(--false))}.cnf-eq-node.backtrack circle{stroke:#b45309}.cnf-eq-current{display:grid;grid-template-columns:minmax(0,.7fr) minmax(0,1.3fr);gap:10px;margin-top:10px}.cnf-eq-current>div{border:1px solid var(--border);border-radius:9px;background:var(--card);padding:9px 10px}.cnf-eq-current strong{display:block;color:var(--muted);font-size:.72rem;text-transform:uppercase;margin-bottom:4px}.cnf-eq-current span{display:block;font:12px/1.45 ui-monospace,monospace;overflow-wrap:anywhere}.cnf-eq-legend{display:flex;gap:8px;flex-wrap:wrap;margin-top:9px;color:var(--muted);font-size:.76rem}.cnf-eq-legend span{display:inline-flex;align-items:center;gap:4px}.cnf-eq-dot{width:9px;height:9px;border-radius:50%;border:2px solid var(--accent)}.cnf-eq-dot.conflict{border-color:var(--false)}.cnf-eq-dot.backtrack{border-color:#b45309}.cnf-eq-dot.sat{border-color:var(--true)}
@media(max-width:720px){.cnf-eq-current{grid-template-columns:1fr}.cnf-eq-svg{min-width:520px}}
@media(max-width:480px){.cnf-eq-svg-wrap{max-width:100%;overflow:auto}.cnf-eq-tree{padding:10px}.cnf-eq-metric{width:100%;border-radius:8px}}
@media(prefers-reduced-motion:reduce){.cnf-eq-node circle{transition:none!important;filter:none!important}}
</style>
'''

SCRIPT = r'''
<script id="cnf-engagement-excellence-runtime">
(()=>{'use strict';
const P=()=>window.__cnfDpllPresentationState;const $=s=>document.querySelector(s);const NS='http://www.w3.org/2000/svg';
const COPY={
 en:{title:'Watch DPLL grow and prune the search tree',help:'Every visible node comes from the existing DPLL trace. Branches create alternatives; propagation extends one branch; contradiction kills it; backtracking opens its sibling.',space:'Reference space',trace:'DPLL trace',step:'Current trace step',path:'Current search path',empty:'Convert a formula to create a DPLL trace.',unit:'unit',pure:'pure',branchT:'try T',branchF:'backtrack F',sat:'SAT',unsat:'conflict',legendBranch:'branch / propagation',legendConflict:'pruned conflict',legendBack:'backtrack',legendSat:'satisfying leaf'},
 zh:{title:'观察 DPLL 如何生长并剪枝搜索树',help:'每个可见节点都来自现有 DPLL 跟踪。分支创建备选路径；传播延伸一个分支；矛盾将其剪掉；回溯再打开兄弟分支。',space:'参考空间',trace:'DPLL 跟踪',step:'当前跟踪步骤',path:'当前搜索路径',empty:'先转换公式以生成 DPLL 跟踪。',unit:'单元',pure:'纯文字',branchT:'尝试 T',branchF:'回溯 F',sat:'可满足',unsat:'冲突',legendBranch:'分支 / 传播',legendConflict:'被剪掉的冲突',legendBack:'回溯',legendSat:'满足叶节点'},
 vi:{title:'Xem DPLL phát triển và cắt tỉa cây tìm kiếm',help:'Mỗi nút hiển thị đều đến từ vết DPLL hiện có. Phân nhánh tạo lựa chọn; lan truyền kéo dài một nhánh; mâu thuẫn cắt nhánh đó; quay lui mở nhánh anh em.',space:'Không gian tham chiếu',trace:'Vết DPLL',step:'Bước vết hiện tại',path:'Đường tìm kiếm hiện tại',empty:'Hãy chuyển đổi một công thức để tạo vết DPLL.',unit:'đơn vị',pure:'literal thuần',branchT:'thử T',branchF:'quay lui F',sat:'SAT',unsat:'mâu thuẫn',legendBranch:'phân nhánh / lan truyền',legendConflict:'mâu thuẫn bị cắt',legendBack:'quay lui',legendSat:'lá thỏa mãn'},
 es:{title:'Mira cómo DPLL hace crecer y poda el árbol de búsqueda',help:'Cada nodo visible proviene de la traza DPLL existente. Las ramas crean alternativas; la propagación extiende una rama; una contradicción la poda; el retroceso abre su hermana.',space:'Espacio de referencia',trace:'Traza DPLL',step:'Paso actual de la traza',path:'Ruta de búsqueda actual',empty:'Convierte una fórmula para crear una traza DPLL.',unit:'unidad',pure:'literal puro',branchT:'probar T',branchF:'retroceder F',sat:'SAT',unsat:'conflicto',legendBranch:'rama / propagación',legendConflict:'conflicto podado',legendBack:'retroceso',legendSat:'hoja satisfactoria'}
};
function locale(){const r=window.__r4Localization?.locale?.();if(r)return r;const l=(document.documentElement.lang||'en').toLowerCase();if(l.startsWith('zh'))return'zh';if(l.startsWith('vi'))return'vi';if(l.startsWith('es'))return'es';return'en'}function cp(){return COPY[locale()]||COPY.en}
function install(){const player=$('#dpllPlayer');if(!player||$('#cnf-eq-tree'))return;const sec=document.createElement('section');sec.id='cnf-eq-tree';sec.className='cnf-eq-tree';sec.setAttribute('data-r4-no-translate','1');sec.innerHTML=`<div class="cnf-eq-head"><div><strong id="cnf-eq-title"></strong><p id="cnf-eq-help"></p></div><span id="cnf-eq-metric" class="cnf-eq-metric"></span></div><div class="cnf-eq-svg-wrap"><svg id="cnf-eq-svg" class="cnf-eq-svg" role="img"></svg></div><div class="cnf-eq-current"><div><strong id="cnf-eq-step-label"></strong><span id="cnf-eq-step"></span></div><div><strong id="cnf-eq-path-label"></strong><span id="cnf-eq-path"></span></div></div><div class="cnf-eq-legend"><span><i class="cnf-eq-dot"></i><b id="cnf-eq-leg-branch"></b></span><span><i class="cnf-eq-dot conflict"></i><b id="cnf-eq-leg-conflict"></b></span><span><i class="cnf-eq-dot backtrack"></i><b id="cnf-eq-leg-back"></b></span><span><i class="cnf-eq-dot sat"></i><b id="cnf-eq-leg-sat"></b></span></div>`;player.insertAdjacentElement('afterend',sec);const count=$('#dpllCount');if(count)new MutationObserver(()=>render()).observe(count,{subtree:true,childList:true,characterData:true});for(const id of ['convertBtn','ex1','ex2','ex3','ex4','ex5','hardReset']){$(`#${id}`)?.addEventListener('click',()=>queueMicrotask(render))}window.addEventListener('r4languagechange',()=>queueMicrotask(render));document.querySelectorAll('.lang-switch button[data-lang]').forEach(b=>b.addEventListener('click',()=>setTimeout(render,0)));render()}
function eventLabel(item,parent){const c=cp();if(!item)return'';if(item.action==='sat')return c.sat;if(item.action==='unsat')return c.unsat;const before=parent?.assign||{},now=item.assign||{},changed=Object.keys(now).sort().find(k=>before[k]!==now[k]);const assignment=changed?`${changed}=${now[changed]?'T':'F'}`:'';if(item.action==='branch+')return`${c.branchT}${assignment?' · '+assignment:''}`;if(item.action==='branch-')return`${c.branchF}${assignment?' · '+assignment:''}`;if(item.action==='unit')return`${c.unit}${assignment?' · '+assignment:''}`;if(item.action==='pure')return`${c.pure}${assignment?' · '+assignment:''}`;return item.action}
function buildNodes(trace,idx){const nodes=[],stack=[];for(let i=0;i<trace.length&&i<=idx;i++){const item=trace[i],parentId=item.depth>0&&stack[item.depth-1]!==undefined?stack[item.depth-1]:-1;const node={id:i,parentId,item,children:[],x:0,y:0};nodes.push(node);if(parentId>=0)nodes[parentId].children.push(i);stack[item.depth]=i;stack.length=item.depth+1}return nodes}
function layout(nodes){const roots=nodes.filter(n=>n.parentId<0).map(n=>n.id);let leaf=0;const gap=105;function place(id){const n=nodes[id];if(!n.children.length)n.x=70+leaf++*gap;else{n.children.forEach(place);n.x=(nodes[n.children[0]].x+nodes[n.children.at(-1)].x)/2}n.y=70+n.item.depth*86}roots.forEach(place);const width=Math.max(620,Math.max(1,leaf)*gap+80),maxDepth=nodes.reduce((m,n)=>Math.max(m,n.item.depth),0),height=Math.max(220,120+(maxDepth+1)*86);return{roots,width,height,rootX:roots.length?(nodes[roots[0]].x+nodes[roots.at(-1]].x)/2:width/2}}
function svgEl(name,attrs={}){const el=document.createElementNS(NS,name);for(const[k,v]of Object.entries(attrs))el.setAttribute(k,String(v));return el}
function ancestors(nodes,id){const out=[];let n=nodes[id];while(n){out.unshift(n);n=n.parentId>=0?nodes[n.parentId]:null}return out}
function render(){if(!P()||!$('#cnf-eq-tree'))return;const c=cp(),trace=P().getTrace(),idx=Math.max(0,Math.min(P().getIndex(),Math.max(0,trace.length-1)));$('#cnf-eq-title').textContent=c.title;$('#cnf-eq-help').textContent=c.help;$('#cnf-eq-step-label').textContent=c.step;$('#cnf-eq-path-label').textContent=c.path;$('#cnf-eq-leg-branch').textContent=c.legendBranch;$('#cnf-eq-leg-conflict').textContent=c.legendConflict;$('#cnf-eq-leg-back').textContent=c.legendBack;$('#cnf-eq-leg-sat').textContent=c.legendSat;const rows=P().getRows();$('#cnf-eq-metric').textContent=`${c.space}: ${Number.isFinite(rows)?rows:'2^n'} assignments · ${c.trace}: ${trace.length} events`;const svg=$('#cnf-eq-svg');svg.replaceChildren();if(!trace.length){$('#cnf-eq-step').textContent=c.empty;$('#cnf-eq-path').textContent='—';svg.setAttribute('viewBox','0 0 620 220');svg.setAttribute('aria-label',c.empty);return}const nodes=buildNodes(trace,idx),g=layout(nodes);svg.setAttribute('viewBox',`0 0 ${g.width} ${g.height}`);svg.setAttribute('aria-label',`${c.title}. ${c.step}: ${idx+1}/${trace.length}.`);const rootY=22;for(const rootId of g.roots){const n=nodes[rootId];svg.appendChild(svgEl('path',{d:`M ${g.rootX} ${rootY} L ${n.x} ${n.y-24}`,class:'cnf-eq-edge'}))}for(const n of nodes)if(n.parentId>=0){const p=nodes[n.parentId];svg.appendChild(svgEl('path',{d:`M ${p.x} ${p.y+24} C ${p.x} ${p.y+50}, ${n.x} ${n.y-50}, ${n.x} ${n.y-24}`,class:'cnf-eq-edge'}))}for(const n of nodes){const group=svgEl('g',{class:`cnf-eq-node ${n.id<idx?'past':''} ${n.id===idx?'current':''} ${n.item.action==='sat'?'sat':''} ${n.item.action==='unsat'?'unsat':''} ${n.item.action==='branch-'?'backtrack':''}`.trim(),transform:`translate(${n.x} ${n.y})`});const title=svgEl('title');title.textContent=`${n.id+1}. ${n.item.detail||n.item.action}`;group.append(title,svgEl('circle',{r:24}));const text=svgEl('text',{y:4});const parent=n.parentId>=0?nodes[n.parentId].item:null;let label=eventLabel(n.item,parent);if(label.length>16)label=label.slice(0,15)+'…';text.textContent=label;group.appendChild(text);svg.appendChild(group)}const current=nodes.at(-1),parent=current.parentId>=0?nodes[current.parentId].item:null;$('#cnf-eq-step').textContent=`${idx+1}/${trace.length} · ${eventLabel(current.item,parent)} · ${current.item.detail||''}`;$('#cnf-eq-path').textContent=ancestors(nodes,current.id).map(n=>eventLabel(n.item,n.parentId>=0?nodes[n.parentId].item:null)).join(' → ')}
function init(){if(!P()||!$('#dpllPlayer'))return setTimeout(init,0);install();window.__cnfDpllTreeExperience={render,getVisibleNodeCount:()=>$('#cnf-eq-svg')?.querySelectorAll('.cnf-eq-node').length||0,getTrace:()=>P().getTrace(),getIndex:()=>P().getIndex()}}init();
})();
</script>
'''


def build_candidate(output: Path) -> Path:
    build_site_v1_4.build_site()
    source = DEFAULT_OUTPUT.read_text(encoding="utf-8")
    marker = "    () => dpllSteps.length, renderDpllStep);\n\n  // Console acceptance test"
    if marker not in source:
        raise RuntimeError("Could not locate frozen DPLL stepper boundary for read-only presentation adapter")
    source = source.replace(
        marker,
        "    () => dpllSteps.length, renderDpllStep);" + TRACE_EXPOSURE + "\n  // Console acceptance test",
        1,
    )
    source = source.replace("</head>", CSS + "\n</head>", 1)
    body_index = source.rfind("</body>")
    if body_index < 0:
        raise RuntimeError("Could not locate final document body boundary for DPLL tree runtime")
    source = source[:body_index] + SCRIPT + "\n" + source[body_index:]
    required = (
        "window.__cnfDpllPresentationState",
        'id="cnf-engagement-excellence-style"',
        'id="cnf-engagement-excellence-runtime"',
        "__cnfDpllTreeExperience",
    )
    missing = [item for item in required if item not in source]
    if missing:
        raise RuntimeError(f"CNF/SAT engagement candidate incomplete: {missing}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(source, encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    result = build_candidate(output)
    print(f"Built CNF/SAT DPLL-tree engagement candidate: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
