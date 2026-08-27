#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
EVIDENCE = ROOT / "release-evidence" / "v1.8.0-algorithm-modes.json"


def ensure_site() -> int:
    home = SITE / "index.html"
    if home.is_file() and '<span class="site-version">v1.8.0</span>' in home.read_text(encoding="utf-8"):
        return 0
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_site_v1_8.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=150,
    )
    if result.returncode:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
    return result.returncode


def section(source: str, start: str, end: str) -> str:
    start_index = source.index(start)
    end_index = source.index(end, start_index)
    return source[start_index:end_index]


def node_result(script: str) -> dict:
    result = subprocess.run(
        ["node", "-e", script],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=60,
    )
    if result.returncode:
        raise RuntimeError(f"Node mechanism check failed:\n{result.stderr[-6000:]}")
    return json.loads(result.stdout)


def write_evidence(payload: dict) -> None:
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    if ensure_site():
        return 1

    sources = {
        slug: (SITE / "playgrounds" / slug / "index.html").read_text(encoding="utf-8")
        for slug in ("cnf-sat", "knn-classifier", "hill-climbing")
    }
    checks: list[tuple[str, bool, object]] = []

    def check(name: str, ok: bool, detail: object = None) -> None:
        checks.append((name, bool(ok), {} if detail is None else detail))

    cdcl_code = section(
        sources["cnf-sat"],
        "  function formatClauseLits",
        "  // Persist the DPLL trace",
    )
    cdcl = node_result(
        cdcl_code
        + r"""
const canonical=[
  [{name:'A',neg:true},{name:'C',neg:true},{name:'D',neg:false}],
  [{name:'C',neg:true},{name:'D',neg:true}],
  [{name:'B',neg:false},{name:'B',neg:true}],
];
const first=cdclTrace(canonical,['A','B','C','D'],500),second=cdclTrace(canonical,['A','B','C','D'],500);
const learned=first.trace.find(row=>row.action==='learn');
const jump=first.trace.find(row=>row.action==='backjump'&&row.data.from-row.data.to>1);
const propagation=first.trace.find(row=>row.action==='propagation');
const rootUnsat=cdclTrace([[{name:'A',neg:false}],[{name:'A',neg:true}]],['A'],100);
function litValue(lit,mask,vars){const index=vars.indexOf(lit.name),value=!!(mask&(1<<index));return value!==lit.neg}
function satFormula(clauses,vars){for(let mask=0;mask<(1<<vars.length);mask++)if(clauses.every(clause=>clause.some(lit=>litValue(lit,mask,vars))))return true;return false}
function entailed(original,learnedClauses,vars){for(let mask=0;mask<(1<<vars.length);mask++){const premise=original.every(clause=>clause.some(lit=>litValue(lit,mask,vars)));if(premise&&!learnedClauses.every(clause=>clause.some(lit=>litValue(lit,mask,vars))))return false}return true}
let seed=0x180,parity=0,learnedSound=0;
const random=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
for(let caseIndex=0;caseIndex<160;caseIndex++){
  const vars=['A','B','C','D'].slice(0,2+Math.floor(random()*3));
  const clauses=[];
  const count=1+Math.floor(random()*8);
  for(let c=0;c<count;c++){
    const clause=[],width=1+Math.floor(random()*3);
    for(let i=0;i<width;i++)clause.push({name:vars[Math.floor(random()*vars.length)],neg:random()<.5});
    clauses.push(clause);
  }
  const result=cdclTrace(clauses,vars,2000);
  if(result.final.sat===satFormula(clauses,vars))parity++;
  const learnedRows=result.clauses.filter(row=>row.learned).map(row=>row.lits);
  if(entailed(clauses,learnedRows,vars))learnedSound++;
}
process.stdout.write(JSON.stringify({
  repeatable:JSON.stringify(first)===JSON.stringify(second),
  learned:learned?.data.learned||null,
  jump:jump?.data||null,
  actions:first.trace.map(row=>row.action),
  implicationReason:propagation?.data.reason||null,
  learnedInserted:first.clauses.some(row=>row.learned&&row.id==='L1'),
  rootUnsat:rootUnsat.final.sat===false&&rootUnsat.trace.at(-1)?.action==='unsat',
  parity,learnedSound,total:160,
}));
"""
    )
    check("CDCL trace is deterministic", cdcl["repeatable"], cdcl)
    check("CDCL example learns the documented first-UIP clause", cdcl["learned"] == "(¬A ∨ ¬C)", cdcl)
    check("CDCL example backjumps non-chronologically from level 3 to level 1", cdcl["jump"] and cdcl["jump"]["from"] == 3 and cdcl["jump"]["to"] == 1, cdcl)
    check("CDCL trace records implication reasons and inserts learned clauses", bool(cdcl["implicationReason"]) and cdcl["learnedInserted"], cdcl)
    check("CDCL detects a root-level contradiction", cdcl["rootUnsat"], cdcl)
    check("CDCL agrees with exhaustive SAT on a deterministic 160-formula census", cdcl["parity"] == cdcl["total"], cdcl)
    check("every learned clause in the census is entailed by its input formula", cdcl["learnedSound"] == cdcl["total"], cdcl)
    check("original DPLL remains the selected default and has one implementation", sources["cnf-sat"].count("function dpllTrace(") == 1 and '<option data-i18n="solver-dpll" selected="" value="dpll">' in sources["cnf-sat"])

    knn_code = section(
        sources["knn-classifier"],
        "  function distMetric",
        "  function render()",
    )
    knn = node_result(
        r"""
const controls={xScale:{value:'1'},metricSel:{value:'euclidean'},weightSel:{value:'uniform'},taskMode:{value:'regression'}};
const document={getElementById:id=>controls[id]||null};
const $=id=>controls[id]||null;
function taskMode(){return controls.taskMode.value==='regression'?'regression':'classification'}
let points=[];
"""
        + knn_code
        + r"""
points=[{x:0,y:0,c:'A',target:10},{x:2,y:0,c:'B',target:20},{x:4,y:0,c:'B',target:40}];
const uniform=knnPredict({x:1,y:0},2);
controls.weightSel.value='distance';
const weighted=knnPredict({x:.5,y:0},2);
controls.taskMode.value='classification';controls.weightSel.value='uniform';
const nearest=knnPredict({x:.1,y:0},1),tie=knnPredict({x:1,y:0},2);
const oversize=(()=>{controls.taskMode.value='regression';return knnPredict({x:1,y:0},99)})();
points=[];const empty=knnPredict({x:0,y:0},3);
const weightedExpected=aggregateRegressionTargets([10,20],[1/(.5+1e-6),1/(1.5+1e-6)]);
process.stdout.write(JSON.stringify({
  uniform:uniform.prediction,neighbors:uniform.neighbors.map(row=>row.target),
  weighted:weighted.prediction,weightedExpected,
  nearest:nearest.label,tie:tie.label,oversizeCount:oversize.neighbors.length,
  emptyIsNull:empty===null,emptyMean:aggregateRegressionTargets([]),zeroWeightMean:aggregateRegressionTargets([10,20],[0,0]),
}));
"""
    )
    check("KNN regression selects the exact nearest neighbors", knn["neighbors"] == [10, 20], knn)
    check("KNN uniform regression reports the arithmetic mean", abs(knn["uniform"] - 15) < 1e-9, knn)
    check("KNN distance weighting reports the normalized weighted mean", abs(knn["weighted"] - knn["weightedExpected"]) < 1e-9, knn)
    check("KNN handles empty and k-larger-than-data edges", knn["emptyIsNull"] and knn["emptyMean"] == 0 and knn["zeroWeightMean"] == 0 and knn["oversizeCount"] == 3, knn)
    check("KNN classification nearest-neighbor and historical A tie-break remain unchanged", knn["nearest"] == "A" and knn["tie"] == "A", knn)

    hill_code = section(
        sources["hill-climbing"],
        "  const BENCH_ALGOS",
        "  let lastBenchmark",
    )
    hill = node_result(
        hill_code
        + r"""
const config={problem:'queens',runs:8,steps:90,seed:1729,t0:10,cooling:.995,algorithms:['simple','steepest','stochastic','firstchoice','sa','tabu']};
const first=computeRestartBenchmark(config),second=computeRestartBenchmark(config);
const repeatable=JSON.stringify(first)===JSON.stringify(second);
const matchedStarts=Array.from({length:first.runs},(_,run)=>first.algorithms.every(name=>first.trials[name][run].startKey===first.trials[first.algorithms[0]][run].startKey)).every(Boolean);
const bounded=computeRestartBenchmark({...config,runs:1,steps:999,algorithms:['steepest']});
const recovered=computeRestartBenchmark({...config,runs:NaN,steps:NaN,seed:NaN,t0:NaN,cooling:NaN,problem:'invalid',algorithms:['steepest','steepest','invalid']});
const changedSeed=computeRestartBenchmark({...config,seed:1730,algorithms:['steepest']});
process.stdout.write(JSON.stringify({
  repeatable,matchedStarts,boundedRuns:bounded.runs,boundedSteps:bounded.steps,
  recovered:{runs:recovered.runs,steps:recovered.steps,seed:recovered.seed,problem:recovered.problem,algorithms:recovered.algorithms},
  completed:first.summary.map(row=>row.completed),
  rates:first.summary.map(row=>row.successRate),
  finiteCosts:first.summary.every(row=>Number.isFinite(row.meanFinal)&&Number.isFinite(row.meanBest)&&Number.isFinite(row.bestObserved)),
  seedChangesStarts:first.trials.steepest[0].startKey!==changedSeed.trials.steepest[0].startKey,
}));
"""
    )
    check("restart benchmark is exactly repeatable for a fixed seed", hill["repeatable"], hill)
    check("every compared algorithm receives the same start on each restart", hill["matchedStarts"], hill)
    check("restart and step inputs are bounded", hill["boundedRuns"] == 2 and hill["boundedSteps"] == 500, hill)
    check("invalid benchmark controls recover to bounded defaults and duplicate algorithms are removed", hill["recovered"] == {"runs": 20, "steps": 120, "seed": 1729, "problem": "tsp", "algorithms": ["steepest"]}, hill)
    check("every algorithm completes the requested restart count", hill["completed"] == [8] * 6, hill)
    check("success frequency and finite cost aggregates are both reported", all(0 <= value <= 1 for value in hill["rates"]) and hill["finiteCosts"], hill)
    check("changing the seed changes the generated start", hill["seedChangesStarts"], hill)
    check("browser runner yields between restarts and supports cancellation", "async function computeRestartBenchmarkResponsive" in sources["hill-climbing"] and "await new Promise(resolve=>setTimeout(resolve,0))" in sources["hill-climbing"] and "benchmarkRunToken" in sources["hill-climbing"])

    for slug, markers in {
        "cnf-sat": ("cdcl-rule", "cdcl-misread", "Trace mode", "Solver step"),
        "knn-classifier": ("regressionInspector", "Regression equation", "Task mode", "continuous target"),
        "hill-climbing": ("bench-misread", "bench-fidelity", "Benchmark results", "Restart benchmark"),
    }.items():
        source = sources[slug]
        for marker in markers:
            check(f"{slug}: explanatory/packet marker {marker}", marker in source)

    failures = [{"name": name, "detail": detail} for name, ok, detail in checks if not ok]
    payload = {
        "harness": "tools/test_v1_8_algorithm_modes.py",
        "checks": len(checks),
        "passed": len(checks) - len(failures),
        "failed": len(failures),
        "pass": not failures,
        "failures": failures,
        "evidence": {"cdcl": cdcl, "knn": knn, "hill": hill},
    }
    write_evidence(payload)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
