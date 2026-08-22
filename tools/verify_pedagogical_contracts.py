#!/usr/bin/env python3
"""Fail-closed pedagogical contract checks for AI Playgrounds v1.1 R1.1."""
from __future__ import annotations
import json, sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/'release-evidence'/'pedagogical-contracts.json'
APPLETS={
 'knn':ROOT/'playgrounds/knn-classifier/index.html',
 'search':ROOT/'playgrounds/search-pathfinding/index.html',
 'hill':ROOT/'playgrounds/hill-climbing/index.html',
 'wumpus':ROOT/'playgrounds/wumpus-world/index.html',
 'sat':ROOT/'playgrounds/cnf-sat/index.html',
 'bayes':ROOT/'playgrounds/bayes-classifier/index.html',
 'bayes_network':ROOT/'playgrounds/bayes-network/index.html',
 'overfitting':ROOT/'playgrounds/overfitting/index.html',
 'neural':ROOT/'playgrounds/neural-network/index.html',
 'kmeans':ROOT/'playgrounds/kmeans/index.html',
 'convolution':ROOT/'playgrounds/convolution/index.html',
 'q_learning':ROOT/'playgrounds/q-learning-gridworld/index.html',
}
REQUIRED={
 'knn':['Guided challenge: predict before reveal','Closeness rule:','Voting rule:','metric ball with the classifier\'s full decision boundary','there is no universal sweet spot','Distance-sensitive ML pipelines often scale or standardize features','不存在普适的“最佳中间值”'],
 'search':['fixed grid and neighbor order','One trace is not a general runtime ranking','number of edges from the start'],
 'hill':['best-improvement','any finite run can still miss the global optimum','willingness to worsen and the tabu memory'],
 'wumpus':['AIMA-inspired hybrid','simplified shoot / heuristic-risk / climb policy','explicit prior assumptions','neither rule proves the selected cell safe','隐藏真相与这个简化推理系统目前实际推出的结论'],
 'sat':['Conflicting XOR constraints create a contradiction','logically equivalent','equisatisfiable','separate DPLL pruning trace'],
 'bayes':['99 percent sensitivity and 99 percent specificity','conditional-independence assumption','conditionally independent of the first given the true condition','repeated tests can share systematic errors'],
 'bayes_network':['Two reports are conditionally independent given the alarm','active-trail, Bayes-ball-style rules directly on the DAG','relative to a conditioning set','conditionally independent given Alarm'],
 'overfitting':['Validation MSE (repeatedly viewed)','functions as validation data, not as an untouched final test set','finite samples and model mismatch can still produce poor generalization','验证 MSE'],
 'neural':['one affine map','original x-y features','optimization still has to find suitable parameters','full-batch gradient descent','Gradient descent (full-batch)','全批量梯度下降'],
 'kmeans':['not proof of a uniquely true k','three generating groups','a centroid is only a point','不能证明存在唯一真实或正确的 k'],
 'convolution':['mathematically it is cross-correlation','numerically largest activation','larger theoretical receptive field','One feature-map response','数学上是互相关'],
 'q_learning':['Step costs and discounting both create time preference','gamma=0.9 with gamma=1','later terminal reward is still discounted','deterministic greedy tie-breaking','折扣本身仍可能让更早到达更有价值'],
}
FORBIDDEN={
 'knn':['sharp diamond boundaries',"Straight, axis-aligned segments: Manhattan's diamond contours",'highest CV accuracy is the right pick','CV 准确率最高的 k 才是正确选择','bias-variance sweet spot','真实的机器学习流程会先对特征做归一化'],
 'search':['Which search will reach a goal first','fast but inefficient route'],
 'hill':['Eventually finds the global optimum','Use the traveling salesperson problem (TSP) with steepest-ascent','Steepest-ascent:','Avoids ties.','Memory is the only thing pulling it out','clearly not the shortest tour','明显不是最短路线'],
 'wumpus':['Sutton-style risk-taking','higher expected value','low expected value','what the agent SHOULD know','= textbook agent','informed risk vs. naive risk','本应知道什么'],
 'sat':['Exclusive OR creates a contradiction','Load the exclusive-OR (XOR) contradiction'],
 'bayes':['99 percent accurate test','This is why doctors retest','这正是医生复检的原因','即使测试很准确'],
 'bayes_network':['Two independent reports strengthen the evidence','on the moralized DAG','两个条件独立的报告如何共同支持警报发生'],
 'overfitting':['σ=0 makes overfitting impossible','overfitting can\'t happen','Test MSE (held out)','More data also fixes it','Sweet spot (degree 5)','Ridge fixes the overfit','even a high-capacity model can\'t memorize: it has to generalize','σ=0 时无法过拟合','更多数据同样能修复','岭回归修复过拟合','即使高容量模型也无法死记硬背','"zhLabel":"测试 MSE"','"zhLiveLabel":"测试 MSE"','训练 MSE 和测试 MSE'],
 'neural':['collapse to one linear map','composition of linear maps is linear','Provably unsolvable by any linear model since Minsky 1969','>SGD</option>','Stochastic gradient descent (SGD)','随机梯度下降（SGD）','SGD step size.'],
 'kmeans':['highest mean silhouette','peaks at the true number of clusters','The highest score wins','Gaussian-shaped centroid','silhouette CAN identify the right k','轮廓系数在真实 k 处达到峰值','轮廓系数能识别正确的 k','高斯形状的质心','分数最高的获胜'],
 'convolution':['What the CNN "sees."','keeps only its strongest activation','detect a pattern larger than either filter alone','这就是卷积网络"看见"的内容。'],
 'q_learning':['every path has the same return','no time pressure','removes time pressure','Exploration is mandatory','never finds goal','it never explores and can\'t discover the goal','没有时间压力','永远找不到终点','探索是必需的','它从不探索,无法发现终点','只出现在与终点/陷阱相邻的格子'],
}

class IdParser(HTMLParser):
    def __init__(self): super().__init__(); self.ids=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k=='id' and v:self.ids.append(v)

def main()->int:
    checks=[]; failures=[]
    for slug,path in APPLETS.items():
        if not path.is_file(): failures.append(f'missing applet: {path}'); continue
        text=path.read_text(encoding='utf-8-sig')
        for phrase in REQUIRED.get(slug,[]):
            ok=phrase in text; checks.append({'applet':slug,'kind':'required','phrase':phrase,'pass':ok})
            if not ok:failures.append(f'{slug}: missing required phrase: {phrase}')
        for phrase in FORBIDDEN.get(slug,[]):
            ok=phrase not in text; checks.append({'applet':slug,'kind':'forbidden','phrase':phrase,'pass':ok})
            if not ok:failures.append(f'{slug}: forbidden phrase remains: {phrase}')
        for shared in ['Predict first','Explain afterward','Misconceptions to test']+([] if slug=='overfitting' else ['What this model leaves out']):
            ok=shared in text; checks.append({'applet':slug,'kind':'shared-learning-contract','phrase':shared,'pass':ok})
            if not ok:failures.append(f'{slug}: shared learning contract missing: {shared}')
        parser=IdParser(); parser.feed(text); dupes=sorted(x for x,n in Counter(parser.ids).items() if n>1)
        ok=not dupes; checks.append({'applet':slug,'kind':'unique-html-ids','pass':ok,'duplicates':dupes})
        if dupes:failures.append(f'{slug}: duplicate HTML ids: {dupes}')
    workflow=ROOT/'.github/workflows/verify.yml'
    wok=workflow.is_file() and 'python tools/verify_pedagogical_contracts.py' in workflow.read_text(encoding='utf-8-sig')
    checks.append({'kind':'workflow-gate','pass':wok})
    if not wok: failures.append('verify workflow does not run pedagogical contract checks')
    for doc in [ROOT/'docs/PEDAGOGICAL_RED_TEAM_V1_1.md',ROOT/'docs/GUIDED_CHALLENGE_ARCHITECTURE.md']:
        ok=doc.is_file() and doc.stat().st_size>500; checks.append({'kind':'documentation','path':str(doc.relative_to(ROOT)),'pass':ok})
        if not ok: failures.append(f'missing or undersized documentation: {doc}')
    payload={'harness':'tools/verify_pedagogical_contracts.py','applet_count':len(APPLETS),'checks':len(checks),'passed':sum(bool(c.get('pass')) for c in checks),'failed':sum(not bool(c.get('pass')) for c in checks),'failures':failures,'pass':not failures,'details':checks}
    EVIDENCE.parent.mkdir(parents=True,exist_ok=True); EVIDENCE.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:payload[k] for k in ('harness','applet_count','checks','passed','failed','pass')},indent=2))
    for f in failures: print('FAIL: '+f,file=sys.stderr)
    return 0 if not failures else 1

if __name__=='__main__': raise SystemExit(main())
