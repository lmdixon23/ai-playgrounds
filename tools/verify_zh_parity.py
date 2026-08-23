#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'release-evidence' / 'zh-parity.json'
APPLETS = [
    'bayes-classifier','bayes-network','cnf-sat','convolution','hill-climbing','kmeans',
    'knn-classifier','neural-network','overfitting','q-learning-gridworld','search-pathfinding','wumpus-world'
]

FORBIDDEN = {
    'hill-climbing': ['最终会找到全局最优','记忆是唯一能','明显不是最短路线'],
    'wumpus-world': ['教科书智能体','智能体应该知道','信息化风险'],
    'bayes-classifier': ['99% 准确的检测'],
    'bayes-network': ['两个独立报告'],
    'overfitting': ['测试 MSE','5 阶是最佳','Ridge 修复','更多数据修复'],
    'neural-network': ['两个线性层组合成一个线性层','可以刻画任何决策边界'],
    'kmeans': ['高斯形质心','最高的轮廓系数获胜','真实 k 就是'],
    'convolution': ['CNN 看到','正是 CNN 在训练中学习滤波器','绝对值最大的值'],
    'q-learning-gridworld': ['探索是必需的','永远找不到目标','γ=0:纯贪婪','γ=0：纯贪婪','没有时间压力','只出现在与终点/陷阱相邻'],
    'knn-classifier': ['最佳中间 k','中间的 k 是偏差-方差甜点','总是应该标准化'],
    'cnf-sat': ['异或会产生矛盾'],
}

REQUIRED = {
    'hill-climbing': ['任何有限次数的重启都不能证明全局最优'],
    'bayes-classifier': ['灵敏度','特异度','条件独立假设'],
    'bayes-network': ['给定 Alarm','条件独立'],
    'overfitting': ['验证 MSE'],
    'neural-network': ['仿射映射','全批量梯度下降','工程化非线性特征'],
    'kmeans': ['不能证明存在唯一真实或正确的 k'],
    'convolution': ['池化并不是平移鲁棒性的唯一来源'],
    'q-learning-gridworld': ['折扣本身仍可能让更早到达更有价值'],
    'knn-classifier': ['不存在普适的“最佳中间值”'],
}

CJK_RE = re.compile(r'[\u3400-\u9fff]')

def check(ok: bool, kind: str, checks: list[dict], failures: list[str], **detail) -> None:
    row = {'kind': kind, 'pass': bool(ok), **detail}
    checks.append(row)
    if not ok:
        failures.append(detail.get('message') or f'{kind} failed: {detail}')

def main() -> int:
    checks: list[dict] = []
    failures: list[str] = []
    for slug in APPLETS:
        path = ROOT / 'playgrounds' / slug / 'index.html'
        text = path.read_text(encoding='utf-8-sig') if path.is_file() else ''
        check(path.is_file(), 'applet-file', checks, failures, applet=slug, message=f'{slug}: missing index.html')
        if not text:
            continue
        check('hreflang="zh-Hans"' in text, 'zh-hreflang', checks, failures, applet=slug, message=f'{slug}: zh-Hans hreflang missing')
        check('data-lang="zh"' in text, 'zh-switch', checks, failures, applet=slug, message=f'{slug}: Chinese language switch missing')
        cjk_count = len(CJK_RE.findall(text))
        check(cjk_count >= 250, 'zh-content-volume', checks, failures, applet=slug, cjk_chars=cjk_count, message=f'{slug}: unexpectedly little Chinese learner-facing content')
        for phrase in FORBIDDEN.get(slug, []):
            ok = phrase not in text
            check(ok, 'forbidden-stale-zh', checks, failures, applet=slug, phrase=phrase, message=f'{slug}: stale Chinese claim remains: {phrase}')
        for phrase in REQUIRED.get(slug, []):
            ok = phrase in text
            check(ok, 'required-precise-zh', checks, failures, applet=slug, phrase=phrase, message=f'{slug}: required Chinese precision phrase missing: {phrase}')

    guided_path = ROOT / 'assets' / 'guided-challenges.js'
    guided = guided_path.read_text(encoding='utf-8-sig') if guided_path.is_file() else ''
    check(bool(guided), 'guided-shared-file', checks, failures, message='shared Guided Challenge JS missing')
    guided_required = [
        "['dependent','Dependent','条件依赖']",
        "explore:'自由探索'", "guided:'引导挑战'", "modeLabel:'学习模式'",
        "begin:'准备挑战'", "lock:'锁定预测'", "reveal:'揭示机制'", "compare:'比较'",
        "actual:'揭示后的 applet 状态'", "before:'隐藏步骤之前'", "after:'隐藏步骤之后'",
        "zh:'预测的知识状态'", "zh:'预测中心输出单元数值'", "zh:'预测 Q 值更新方向'",
    ]
    for token in guided_required:
        check(token in guided, 'guided-zh-contract', checks, failures, token=token, message=f'Guided Challenge Chinese parity token missing: {token}')
    for token in ["['dependent','Dependent','相关']", "actual:'揭示后的工具状态'"]:
        check(token not in guided, 'guided-zh-forbidden', checks, failures, token=token, message=f'Guided Challenge stale/weaker Chinese token remains: {token}')

    knn = (ROOT/'playgrounds/knn-classifier/index.html').read_text(encoding='utf-8-sig')
    for token in [
        'Explain when standardization or another scaling choice is appropriate before comparing distances across features.',
        '解释在比较不同特征的距离之前，什么时候适合使用标准化或其他缩放方式。',
    ]:
        check(token in knn, 'knn-scaling-parity', checks, failures, token=token, message=f'KNN nuanced scaling statement missing: {token}')

    neural = (ROOT/'playgrounds/neural-network/index.html').read_text(encoding='utf-8-sig')
    check('然后与工程化的非线性输入特征进行比较。' in neural, 'neural-xor-zh-parity', checks, failures,
          message='Neural-network Chinese XOR scenario omits the engineered-feature comparison present in English')

    doc = ROOT/'docs/ZH_PARITY_AUDIT_V1_1.md'
    doc_text = doc.read_text(encoding='utf-8-sig') if doc.is_file() else ''
    for token in ['Simplified Chinese parity freeze','R3 audit boundary','Vietnamese and Spanish remain deferred']:
        check(token in doc_text, 'zh-audit-doc', checks, failures, token=token, message=f'R3 Chinese audit doc missing: {token}')

    workflow = ROOT/'.github/workflows/verify.yml'
    wt = workflow.read_text(encoding='utf-8-sig') if workflow.is_file() else ''
    for cmd in ['python tools/verify_zh_parity.py','python tools/zh_parity_qa.py']:
        check(cmd in wt, 'workflow-gate', checks, failures, command=cmd, message=f'normal Verify workflow missing {cmd}')

    payload = {
        'harness':'tools/verify_zh_parity.py', 'applets':len(APPLETS), 'checks':len(checks),
        'passed':sum(bool(x['pass']) for x in checks), 'failed':sum(not bool(x['pass']) for x in checks),
        'pass':not failures, 'failures':failures, 'details':checks,
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:payload[k] for k in ('harness','applets','checks','passed','failed','pass')},indent=2))
    for failure in failures:
        print('FAIL: '+failure,file=sys.stderr)
    return 0 if not failures else 1

if __name__ == '__main__':
    raise SystemExit(main())
