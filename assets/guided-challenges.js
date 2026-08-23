(function () {
  'use strict';

  const slug = location.pathname.split('/').filter(Boolean).slice(-2, -1)[0] || '';
  const CONFIGS = {
    'search-pathfinding': {
      scenario: 0, transferScenario: 1, action: '#stepBtn', actionClicks: 1,
      mask: ['.bento-main'], actual: ['#a11yStateSummary', '#tpCount', '.stage-caption', '.stage-metric'],
      en: {
        title: 'Predict the next frontier move',
        prompt: 'Before one search step is revealed, predict which frontier state will be expanded next and explain the ordering rule that makes it next.',
        transfer: 'Changed case: compare the next expansion under a different search scenario or heuristic.'
      },
      zh: {
        title: '预测下一次前沿展开',
        prompt: '在揭示一次搜索步骤之前，预测接下来会展开哪个前沿状态，并说明为什么当前排序规则会选中它。',
        transfer: '迁移情境：换一个搜索场景或启发式，再预测下一次展开。'
      },
      fields: [
        {key:'frontier', type:'text', en:'Next frontier state or coordinate', zh:'下一个前沿状态或坐标'},
        {key:'rule', type:'textarea', en:'Why is it next?', zh:'为什么它会被选中？'}
      ]
    },
    'hill-climbing': {
      scenario: 1, transferScenario: 2, action: '#stepBtn', actionClicks: 1,
      mask: ['.bento-main'], actual: ['#a11yStateSummary', '#tpCount', '#status'],
      en: {
        title: 'Predict the accepted candidate',
        prompt: 'Before the next local-search step is revealed, predict which candidate will be accepted and identify the comparison rule that permits or rejects it.',
        transfer: 'Changed case: repeat with a different local-search strategy and compare the acceptance rule.'
      },
      zh: {
        title: '预测会被接受的候选状态',
        prompt: '在揭示下一次局部搜索步骤之前，预测哪个候选状态会被接受，并说明当前比较规则为什么允许或拒绝它。',
        transfer: '迁移情境：换一种局部搜索策略，再比较接受规则。'
      },
      fields: [
        {key:'candidate', type:'text', en:'Candidate you expect to be accepted', zh:'你预测会被接受的候选状态'},
        {key:'rule', type:'select', en:'Expected comparison rule', zh:'预期比较规则', options:[
          ['improve','Accept only an improving move','只接受改进移动'],
          ['worse','A worsening move can be accepted','可能接受变差移动'],
          ['memory','Memory or tabu status changes the choice','记忆或禁忌状态改变选择']
        ]}
      ]
    },
    'wumpus-world': {
      scenario: 4, transferScenario: 2, action: '#stepBtn', actionClicks: 1,
      mask: ['.bento-main'], actual: ['#a11yStateSummary', '#log', '#scoreV'],
      en: {
        title: 'Classify a frontier square before the move',
        prompt: 'Choose one frontier square and predict whether the current evidence makes it proven safe, a possible hazard, or unresolved before the agent takes its next step.',
        transfer: 'Changed case: switch to the probability-based policy and reconsider the same kind of frontier evidence.'
      },
      zh: {
        title: '在移动前判断一个前沿方格',
        prompt: '选择一个前沿方格，并在智能体执行下一步之前判断当前证据是否能证明它安全、可能有危险，或仍未解决。',
        transfer: '迁移情境：切换到概率策略，再判断类似的前沿证据。'
      },
      fields: [
        {key:'square', type:'text', en:'Frontier square', zh:'前沿方格'},
        {key:'status', type:'select', en:'Predicted knowledge status', zh:'预测的知识状态', options:[
          ['safe','Proven safe','已证明安全'], ['hazard','Possible hazard','可能有危险'], ['unresolved','Unresolved','未解决']
        ]}
      ]
    },
    'cnf-sat': {
      scenario: 2, transferScenario: 3, action: '#dpllStep', actionClicks: 1,
      mask: ['#parseOut', '#cnfPlayer', '#satOut', '#dpllPlayer', '#resolveOut'],
      actual: ['#dpllAction', '#dpllDetail', '#dpllAssign', '#dpllClauses'],
      en: {
        title: 'Predict the next DPLL inference',
        prompt: 'Before the next DPLL trace step is revealed, predict whether the solver will force a literal, branch, or expose a conflict, and name the literal or branch if you can.',
        transfer: 'Changed case: use another formula and predict which pruning mechanism appears first.'
      },
      zh: {
        title: '预测下一次 DPLL 推理',
        prompt: '在揭示下一条 DPLL 轨迹之前，预测求解器会强制某个文字、进行分支，还是暴露冲突；如果可以，请写出对应文字或分支。',
        transfer: '迁移情境：换一个公式，预测最先出现哪种剪枝机制。'
      },
      fields: [
        {key:'kind', type:'select', en:'Next mechanism', zh:'下一种机制', options:[
          ['unit','Unit propagation','单元传播'], ['branch','Branch','分支'], ['conflict','Conflict','冲突'], ['pure','Pure literal','纯文字']
        ]},
        {key:'literal', type:'text', en:'Literal, branch, or contradiction source', zh:'文字、分支或冲突来源'}
      ]
    },
    'bayes-classifier': {
      scenario: 0, transferScenario: 2,
      mask: ['.bento-main'], actual: ['#counts', '#posteriorPos', '#posteriorNeg'],
      en: {
        title: 'Predict the counts before the posterior',
        prompt: 'For the prepared population, predict the true-positive and false-positive counts before the posterior probability is revealed.',
        transfer: 'Changed case: raise the base rate and predict how the two positive-count groups change.'
      },
      zh: {
        title: '在后验概率揭示前预测人数',
        prompt: '对于准备好的总体，在揭示后验概率之前预测真阳性和假阳性人数。',
        transfer: '迁移情境：提高基率，再预测两类阳性人数会怎样变化。'
      },
      fields: [
        {key:'tp', type:'number', en:'Predicted true positives', zh:'预测真阳性人数'},
        {key:'fp', type:'number', en:'Predicted false positives', zh:'预测假阳性人数'}
      ]
    },
    'bayes-network': {
      scenario: 1, transferScenario: 2,
      mask: ['.net-cpts', '.infer-section'], actual: ['#a11yStateSummary'],
      en: {
        title: 'Predict an evidence update and dependence status',
        prompt: 'Before the prepared evidence is revealed, predict the direction of the target probability update and whether the two report variables are independent under the stated conditioning set.',
        transfer: 'Changed case: add the second report and reconsider the dependence relation after conditioning on Alarm.'
      },
      zh: {
        title: '预测证据更新与条件依赖关系',
        prompt: '在揭示准备好的证据之前，预测目标概率会向哪个方向变化，并判断在给定条件集下两个报告变量是否独立。',
        transfer: '迁移情境：加入第二个报告，并在给定 Alarm 后重新判断依赖关系。'
      },
      fields: [
        {key:'direction', type:'select', en:'Predicted probability direction', zh:'预测概率方向', options:[
          ['up','Increase','上升'], ['down','Decrease','下降'], ['same','About the same','大致不变']
        ]},
        {key:'dependence', type:'select', en:'Predicted dependence status', zh:'预测依赖状态', options:[
          ['independent','Conditionally independent','条件独立'], ['dependent','Dependent','相关'], ['uncertain','Not enough information yet','信息不足']
        ]}
      ]
    },
    'overfitting': {
      scenario: 2, transferScenario: 3,
      mask: ['.bento-main'],  actual: ['#a11yStateSummary'],
      en: {
        title: 'Predict train versus validation movement',
        prompt: 'Before the high-capacity fit is revealed, predict what happens to training error and repeatedly viewed validation error relative to a lower-capacity fit.',
        transfer: 'Changed case: add regularization and predict which error changes most.'
      },
      zh: {
        title: '预测训练误差与验证误差的变化',
        prompt: '在揭示高容量拟合之前，预测与较低容量拟合相比，训练误差和反复查看的验证误差会怎样变化。',
        transfer: '迁移情境：加入正则化，再预测哪一种误差变化最大。'
      },
      fields: [
        {key:'train', type:'select', en:'Training error', zh:'训练误差', options:[['down','Lower','更低'],['up','Higher','更高'],['same','About the same','大致不变']]},
        {key:'validation', type:'select', en:'Validation error', zh:'验证误差', options:[['down','Lower','更低'],['up','Higher','更高'],['same','About the same','大致不变']]}
      ]
    },
    'neural-network': {
      scenario: 1, transferScenario: 2, action: '#stepBtn', actionClicks: 12,
      mask: ['.bento-main'], actual: ['#a11yStateSummary', '#lossV', '#accV'],
      en: {
        title: 'Predict the representational change',
        prompt: 'Before training frames are revealed, predict whether the prepared architecture is restricted to an affine boundary or can represent a curved boundary, and explain which feature or activation makes the difference.',
        transfer: 'Changed case: add a nonlinear hidden representation and predict how the boundary family changes.'
      },
      zh: {
        title: '预测表示能力的变化',
        prompt: '在揭示训练过程之前，预测当前结构是否只能形成仿射边界，还是能够表示弯曲边界，并说明是哪种特征或激活函数造成差异。',
        transfer: '迁移情境：加入非线性隐藏表示，再预测边界族会怎样变化。'
      },
      fields: [
        {key:'boundary', type:'select', en:'Predicted boundary family', zh:'预测边界类型', options:[
          ['affine','Affine only','仅仿射'], ['curved','Can become curved','可以弯曲'], ['uncertain','Unsure','不确定']
        ]},
        {key:'why', type:'textarea', en:'Mechanism: activation or engineered feature', zh:'机制：激活函数或工程化特征'}
      ]
    },
    'kmeans': {
      scenario: 4, transferScenario: 1, action: '#stepBtn', actionClicks: 2,
      mask: ['.bento-main'], actual: ['#a11yStateSummary', '#sseV', '#silV', '#iterV'],
      en: {
        title: 'Predict assignment and centroid movement',
        prompt: 'Before the next assignment/update cycle is revealed, predict which cluster a representative point will join and the direction its centroid should move.',
        transfer: 'Changed case: use a poor initialization and predict how the first update differs.'
      },
      zh: {
        title: '预测分配与质心移动',
        prompt: '在揭示下一轮分配与更新之前，预测一个代表性点会加入哪个簇，以及对应质心应向哪个方向移动。',
        transfer: '迁移情境：改用较差的初始化，再预测第一次更新有何不同。'
      },
      fields: [
        {key:'assignment', type:'text', en:'Predicted cluster assignment', zh:'预测簇分配'},
        {key:'movement', type:'text', en:'Predicted centroid movement', zh:'预测质心移动方向'}
      ]
    },
    'convolution': {
      scenario: 0, transferScenario: 1,
      mask: ['.canvas-pair'], actual: ['#a11yStateSummary', '#szOut', '#windowMath', '#hiSum'],
      en: {
        title: 'Predict one output-cell calculation',
        prompt: 'Before the output is revealed, predict the value of a representative output cell and explain which input values and kernel weights contribute to its multiply-and-sum.',
        transfer: 'Changed case: switch to an edge kernel and predict how the sign and magnitude of the response change.'
      },
      zh: {
        title: '预测一个输出单元的计算',
        prompt: '在揭示输出之前，预测一个代表性输出单元的值，并说明哪些输入值和卷积核权重参与了乘加。',
        transfer: '迁移情境：切换到边缘卷积核，再预测响应的符号和大小如何变化。'
      },
      fields: [
        {key:'value', type:'number', en:'Predicted output-cell value', zh:'预测输出单元数值'},
        {key:'products', type:'textarea', en:'Which products contribute?', zh:'哪些乘积项会参与？'}
      ]
    },
    'q-learning-gridworld': {
      scenario: 2, transferScenario: 3, action: '#stepBtn', actionClicks: 1,
      mask: ['.bento-main'], actual: ['#a11yStateSummary', '#status', '#tpCount'],
      en: {
        title: 'Predict the TD update',
        prompt: 'Before one transition is revealed, predict the selected action, the TD target or its direction, and whether the current Q value should move up, down, or stay about the same.',
        transfer: 'Changed case: restore a nonzero discount and predict how delayed value begins to propagate.'
      },
      zh: {
        title: '预测 TD 更新',
        prompt: '在揭示一次转移之前，预测会选择哪个动作、TD 目标或其方向，以及当前 Q 值应上升、下降还是大致不变。',
        transfer: '迁移情境：恢复非零折扣，再预测延迟价值如何开始向后传播。'
      },
      fields: [
        {key:'action', type:'text', en:'Predicted action', zh:'预测动作'},
        {key:'target', type:'text', en:'Predicted TD target or immediate reward', zh:'预测 TD 目标或即时奖励'},
        {key:'direction', type:'select', en:'Predicted Q update direction', zh:'预测 Q 值更新方向', options:[['up','Up','上升'],['down','Down','下降'],['same','About the same','大致不变']]}
      ]
    }
  };

  const COMMON = {
    en: {
      explore:'Explore', guided:'Guided Challenge', modeLabel:'Learning mode',
      begin:'Prepare challenge', lock:'Lock prediction', reveal:'Reveal mechanism', compare:'Compare', reset:'Reset challenge',
      explain:'Explain the discrepancy', transfer:'Try changed case', prediction:'Your locked prediction', actual:'Revealed applet state',
      hidden:'The relevant result is hidden until you lock a prediction and reveal it.',
      states:{
        inactive:'Challenge inactive. Prepare a challenge when you are ready.',
        'awaiting-prediction':'Enter the required mechanism prediction before locking.',
        'prediction-complete-unlocked':'Prediction complete. Lock it before the result can be revealed.',
        locked:'Prediction locked and immutable. The underlying applet step has run while the result remains hidden.',
        revealed:'Mechanism revealed. Compare the locked prediction with the actual applet state.',
        compared:'Comparison recorded. Explain any discrepancy before trying the transfer case.',
        reset:'Challenge reset.'
      }
    },
    zh: {
      explore:'自由探索', guided:'引导挑战', modeLabel:'学习模式',
      begin:'准备挑战', lock:'锁定预测', reveal:'揭示机制', compare:'比较', reset:'重置挑战',
      explain:'解释预测与结果的差异', transfer:'尝试变化后的情境', prediction:'已锁定的预测', actual:'揭示后的工具状态',
      hidden:'相关结果会保持隐藏，直到你锁定预测并主动揭示。',
      states:{
        inactive:'挑战未启动。准备好后开始。',
        'awaiting-prediction':'请先完成所需的机制预测，再锁定答案。',
        'prediction-complete-unlocked':'预测已完整。先锁定预测，之后才能揭示结果。',
       locked:'预测已锁定且不可修改。底层工具已运行，但结果仍保持隐藏。',
        revealed:'机制已揭示。请把锁定预测与实际工具状态进行比较。',
        compared:'比较已完成。请先解释差异，再尝试迁移情境。',
        reset:'挑战已重置。'
      }
    }
  };

  if (!CONFIGS[slug] && slug !== 'knn-classifier') return;

  const lang = () => (document.documentElement.lang || 'en').toLowerCase().startsWith('zh') ? 'zh' : 'en';
  const c = () => COMMON[lang()];
  const config = CONFIGS[slug] || null;
  const inner = document.querySelector('.interactive-inner');
  if (!inner) return;

  let mode = 'explore';
  let state = 'inactive';
  let stateHistory = ['inactive'];
  let lockedPrediction = null;
  let actualSnapshot = '';
  let internalMutation = false;
  let transferRound = false;
  const concealed = [];
  const frozen = [];

  const shell = document.createElement('section');
  shell.className = 'suite-guided-shell';
  shell.dataset.guidedState = state;
  shell.innerHTML = `
    <div class="suite-guided-modebar" role="group" aria-label="Learning mode">
      <span class="suite-guided-mode-label"></span>
      <button type="button" data-suite-mode="explore" aria-pressed="true"></button>
      <button type="button" data-suite-mode="guided" aria-pressed="false"></button>
    </div>
    <section class="suite-guided-panel" hidden>
      <div class="suite-guided-heading">
        <div><strong class="suite-guided-title"></strong><p class="suite-guided-prompt"></p></div>
        <button type="button" class="suite-guided-reset"></button>
      </div>
      <div class="suite-guided-status" aria-live="polite"></div>
      <div class="suite-guided-generic">
        <div class="suite-guided-fields"></div>
        <div class="suite-guided-actions">
          <button type="button" class="suite-guided-begin primary"></button>
          <button type="button" class="suite-guided-lock" disabled></button>
          <button type="button" class="suite-guided-reveal primary" disabled></button>
          <button type="button" class="suite-guided-compare" disabled></button>
        </div>
        <div class="suite-guided-hidden-note" hidden></div>
        <div class="suite-guided-comparison" hidden>
          <div><strong class="suite-guided-prediction-label"></strong><pre class="suite-guided-prediction"></pre></div>
          <div><strong class="suite-guided-actual-label"></strong><pre class="suite-guided-actual"></pre></div>
        </div>
        <label class="suite-guided-explain-wrap" hidden><span class="suite-guided-explain-label"></span><textarea data-guided-explanation rows="3"></textarea></label>
        <div class="suite-guided-transfer-wrap" hidden><p class="suite-guided-transfer-prompt"></p><button type="button" class="suite-guided-transfer" disabled></button></div>
      </div>
      <div class="suite-guided-native" hidden></div>
    </section>`;
  inner.insertBefore(shell, inner.firstElementChild);

  const q = sel => shell.querySelector(sel);
  const modeExplore = q('[data-suite-mode="explore"]');
  const modeGuided = q('[data-suite-mode="guided"]');
  const panel = q('.suite-guided-panel');
  const learningShell = inner.querySelector('.learning-mode-shell');
  const fieldsRoot = q('.suite-guided-fields');
  const beginBtn = q('.suite-guided-begin');
  const lockBtn = q('.suite-guided-lock');
  const revealBtn = q('.suite-guided-reveal');
  const compareBtn = q('.suite-guided-compare');
  const resetBtn = q('.suite-guided-reset');
  const transferBtn = q('.suite-guided-transfer');
  const explain = q('[data-guided-explanation]');

  function setState(next) {
    state = next;
    shell.dataset.guidedState = next;
    stateHistory.push(next);
    q('.suite-guided-status').textContent = c().states[next] || next;
  }

  function fieldValue(el) {
    return String(el.value == null ? '' : el.value).trim();
  }

  function genericFieldElements() {
    return Array.from(fieldsRoot.querySelectorAll('[data-guided-field]'));
  }

  function predictionComplete() {
    const els = genericFieldElements();
    return els.length > 0 && els.every(el => fieldValue(el) !== '');
  }

  function updatePredictionState() {
    if (state === 'locked' || state === 'revealed' || state === 'compared') return;
    if (state !== 'awaiting-prediction' && state !== 'prediction-complete-unlocked') return;
    const complete = predictionComplete();
    lockBtn.disabled = !complete;
    setState(complete ? 'prediction-complete-unlocked' : 'awaiting-prediction');
  }

  function collectPrediction() {
    const out = {};
    genericFieldElements().forEach(el => { out[el.dataset.guidedField] = fieldValue(el); });
    return out;
  }

  function predictionText(pred) {
    if (!config) return '';
    return config.fields.map(f => {
      const label = f[lang()] || f.en;
      let value = pred[f.key] || '';
      if (f.type === 'select' && f.options) {
        const found = f.options.find(x => x[0] === value);
        if (found) value = found[lang() === 'zh' ? 2 : 1];
      }
      return `${label}: ${value}`;
    }).join('\n');
  }

  function renderFields() {
    if (!config) return;
    fieldsRoot.innerHTML = '';
    config.fields.forEach(f => {
      const label = document.createElement('label');
      label.className = 'suite-guided-field';
      const span = document.createElement('span');
      span.textContent = f[lang()] || f.en;
      label.appendChild(span);
      let el;
      if (f.type === 'textarea') {
        el = document.createElement('textarea'); el.rows = 2;
      } else if (f.type === 'select') {
        el = document.createElement('select');
        const placeholder = document.createElement('option'); placeholder.value = ''; placeholder.textContent = lang() === 'zh' ? '请选择' : 'Choose';
        el.appendChild(placeholder);
        (f.options || []).forEach(opt => {
          const o = document.createElement('option'); o.value = opt[0]; o.textContent = opt[lang() === 'zh' ? 2 : 1]; el.appendChild(o);
        });
      } else {
        el = document.createElement('input'); el.type = f.type === 'number' ? 'number' : 'text';
        if (f.type === 'number') el.step = 'any';
      }
      el.dataset.guidedField = f.key;
      el.setAttribute('aria-label', f[lang()] || f.en);
      el.autocomplete = 'off';
      el.disabled = state === 'locked' || state === 'revealed' || state === 'compared';
      label.appendChild(el); fieldsRoot.appendChild(label);
    });
    fieldsRoot.addEventListener('input', updatePredictionState, {once:false});
    fieldsRoot.addEventListener('change', updatePredictionState, {once:false});
  }

  function preserveFieldDataWhileRerendering(snapshot = null) {
    if (!config) return;
    const committed = lockedPrediction && ['locked','revealed','compared'].includes(state);
    const values = committed ? {...lockedPrediction} : (snapshot ? {...snapshot} : {});
    if (!committed && !snapshot) {
      genericFieldElements().forEach(el => values[el.dataset.guidedField] = el.value);
    }
    renderFields();
    genericFieldElements().forEach(el => {
      if (Object.prototype.hasOwnProperty.call(values, el.dataset.guidedField)) el.value = values[el.dataset.guidedField];
      el.disabled = state === 'locked' || state === 'revealed' || state === 'compared';
    });
  }

  function renderCopy(fieldSnapshot = null) {
    q('.suite-guided-mode-label').textContent = c().modeLabel + ':';
    modeExplore.textContent = c().explore; modeGuided.textContent = c().guided;
    resetBtn.textContent = c().reset; beginBtn.textContent = c().begin; lockBtn.textContent = c().lock;
    revealBtn.textContent = c().reveal; compareBtn.textContent = c().compare; transferBtn.textContent = c().transfer;
    q('.suite-guided-prediction-label').textContent = c().prediction;
    q('.suite-guided-actual-label').textContent = c().actual;
    q('.suite-guided-explain-label').textContent = c().explain;
    q('.suite-guided-hidden-note').textContent = c().hidden;
    if (config) {
      q('.suite-guided-title').textContent = config[lang()].title;
      q('.suite-guided-prompt').textContent = transferRound ? config[lang()].transfer : config[lang()].prompt;
      q('.suite-guided-transfer-prompt').textContent = config[lang()].transfer;
      preserveFieldDataWhileRerendering(fieldSnapshot);
    } else {
      q('.suite-guided-title').textContent = lang() === 'zh' ? 'KNN 邻居预测挑战' : 'KNN neighbor prediction challenge';
      q('.suite-guided-prompt').textContent = lang() === 'zh'
        ? '使用原生 KNN 挑战：先放置查询点，再选择恰好 k 个预测邻居和预测类别，然后锁定并揭示。'
        : 'Use the native KNN challenge: place a query, select exactly k predicted neighbors and a class, then lock before reveal.';
      q('.suite-guided-transfer-prompt').textContent = lang() === 'zh'
        ? '迁移：改变距离规则后重新预测邻居。'
        : 'Transfer: change the closeness rule and predict the neighbors again.';
    }
    q('.suite-guided-status').textContent = c().states[state] || state;
  }

  function setMode(next) {
    mode = next;
    modeExplore.setAttribute('aria-pressed', String(next === 'explore'));
    modeGuided.setAttribute('aria-pressed', String(next === 'guided'));
    panel.hidden = next !== 'guided';
    if (learningShell) learningShell.hidden = next === 'guided';
    document.body.classList.toggle('suite-guided-mode-active', next === 'guided');
    if (next === 'explore') resetChallenge(false);
    renderCopy();
  }

  function queryAllUnique(selectors) {
    const out = [];
    (selectors || []).forEach(sel => document.querySelectorAll(sel).forEach(el => { if (!out.includes(el)) out.push(el); }));
    return out;
  }

  function concealOutputs() {
    restoreOutputs();
    let targets = queryAllUnique(config && config.mask ? config.mask : ['.bento-main']);
    if (!targets.length) targets = Array.from(inner.querySelectorAll('canvas'));
    targets.forEach(el => {
      concealed.push({el, visibility:el.style.visibility, aria:el.getAttribute('aria-hidden')});
      el.style.visibility = 'hidden'; el.setAttribute('aria-hidden','true'); el.dataset.guidedConcealed = '1';
    });
    q('.suite-guided-hidden-note').hidden = false;
  }

  function restoreOutputs() {
    while (concealed.length) {
      const item = concealed.pop(); item.el.style.visibility = item.visibility;
      if (item.aria == null) item.el.removeAttribute('aria-hidden'); else item.el.setAttribute('aria-hidden', item.aria);
      delete item.el.dataset.guidedConcealed;
    }
    q('.suite-guided-hidden-note').hidden = true;
  }

  function freezeExploreControls() {
    unfreezeExploreControls();
    inner.querySelectorAll('button,input,select,textarea').forEach(el => {
      if (shell.contains(el)) return;
      if (!('disabled' in el)) return;
      frozen.push({el, disabled:el.disabled}); el.disabled = true;
    });
    if (slug !== 'knn-classifier') inner.querySelectorAll('canvas').forEach(el => {
      frozen.push({el, pointer:el.style.pointerEvents, canvas:true}); el.style.pointerEvents = 'none';
    });
  }

  function unfreezeExploreControls() {
    while (frozen.length) {
      const item = frozen.pop();
      if (item.canvas) item.el.style.pointerEvents = item.pointer; else item.el.disabled = item.disabled;
    }
  }

  function applyScenario(index) {
    if (!Number.isInteger(index)) return;
    const btn = document.querySelector(`.scenario-card[data-scenario-index="${index}"] button`);
    if (!btn) return;
    internalMutation = true;
    try { btn.click(); } finally { internalMutation = false; }
  }

  function runDeferredAction() {
    if (!config || !config.action) return;
    const btn = document.querySelector(config.action);
    if (!btn) return;
    internalMutation = true;
    try {
      const n = Math.max(1, Number(config.actionClicks || 1));
      for (let i = 0; i < n; i += 1) {
        if (btn.disabled) btn.dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true, view:window}));
        else btn.click();
      }
    } finally { internalMutation = false; }
  }

  function actualText() {
    try { if (typeof window.renderAccessibilityLayer === 'function') window.renderAccessibilityLayer({announce:false}); } catch (_) {}
    const selectors = (config && config.actual) || ['#a11yStateSummary'];
    const parts = [];
    selectors.forEach(sel => {
      const el = document.querySelector(sel); if (!el) return;
      const txt = String(el.innerText || el.textContent || el.value || '').replace(/\s+/g,' ').trim();
      if (txt && !parts.includes(txt)) parts.push(txt);
    });
    if (!parts.length) {
      const a11y = document.querySelector('#a11yStateSummary');
      if (a11y) parts.push(String(a11y.innerText || a11y.textContent || '').replace(/\s+/g,' ').trim());
    }
    return parts.join('\n').slice(0, 1800) || (lang() === 'zh' ? '请查看已揭示的可视结果。' : 'Inspect the revealed visual result.');
  }

  function clearGenericSurface() {
    lockedPrediction = null; actualSnapshot = ''; transferRound = false;
    q('.suite-guided-comparison').hidden = true;
    q('.suite-guided-explain-wrap').hidden = true;
    q('.suite-guided-transfer-wrap').hidden = true;
    q('.suite-guided-prediction').textContent = '';
    q('.suite-guided-actual').textContent = '';
    explain.value = '';
    transferBtn.disabled = true;
    lockBtn.disabled = true; revealBtn.disabled = true; compareBtn.disabled = true;
    beginBtn.disabled = false;
    genericFieldElements().forEach(el => { el.value = ''; el.disabled = true; });
  }

  function beginGeneric() {
    clearGenericSurface();
    concealOutputs();
    unfreezeExploreControls();
    applyScenario(transferRound ? config.transferScenario : config.scenario);
    freezeExploreControls();
    genericFieldElements().forEach(el => el.disabled = false);
    beginBtn.disabled = true;
    setState('awaiting-prediction');
    updatePredictionState();
    genericFieldElements()[0]?.focus();
  }

  function lockGeneric() {
    if (lockBtn.disabled || !predictionComplete()) return;
    lockedPrediction = collectPrediction();
    genericFieldElements().forEach(el => el.disabled = true);
    lockBtn.disabled = true;
    setState('locked');
    runDeferredAction();
    revealBtn.disabled = false;
  }

  function revealGeneric() {
    if (revealBtn.disabled || state !== 'locked') return;
    restoreOutputs();
    actualSnapshot = actualText();
    q('.suite-guided-prediction').textContent = predictionText(lockedPrediction || {});
    q('.suite-guided-actual').textContent = actualSnapshot;
    q('.suite-guided-comparison').hidden = false;
    revealBtn.disabled = true; compareBtn.disabled = false;
    setState('revealed');
  }

  function compareGeneric() {
    if (compareBtn.disabled || state !== 'revealed') return;
    compareBtn.disabled = true;
    q('.suite-guided-explain-wrap').hidden = false;
    q('.suite-guided-transfer-wrap').hidden = false;
    setState('compared');
    explain.focus();
  }

  function transferGeneric() {
    if (transferBtn.disabled || state !== 'compared') return;
    unfreezeExploreControls();
    concealOutputs();
    internalMutation = true;
    try { applyScenario(config.transferScenario); } finally { internalMutation = false; }
    freezeExploreControls();
    transferRound = true; lockedPrediction = null; actualSnapshot = '';
    q('.suite-guided-comparison').hidden = true; q('.suite-guided-explain-wrap').hidden = true; q('.suite-guided-transfer-wrap').hidden = true;
    explain.value = ''; transferBtn.disabled = true; revealBtn.disabled = true; compareBtn.disabled = true; beginBtn.disabled = true;
    genericFieldElements().forEach(el => { el.value = ''; el.disabled = false; });
    setState('awaiting-prediction'); renderCopy();
    genericFieldElements()[0]?.focus();
  }

  function resetChallenge(recordReset = true) {
    if (slug === 'knn-classifier') return resetKnn(recordReset);
    unfreezeExploreControls(); restoreOutputs(); clearGenericSurface();
    if (recordReset) {
      setState('reset');
      requestAnimationFrame(() => { if (state === 'reset') setState('inactive'); });
    } else {
      state = 'inactive'; shell.dataset.guidedState = state; q('.suite-guided-status').textContent = c().states.inactive;
    }
  }

  function setupGeneric() {
    renderFields();
    genericFieldElements().forEach(el => el.disabled = true);
    beginBtn.addEventListener('click', beginGeneric);
    lockBtn.addEventListener('click', lockGeneric);
    revealBtn.addEventListener('click', revealGeneric);
    compareBtn.addEventListener('click', compareGeneric);
    transferBtn.addEventListener('click', transferGeneric);
    explain.addEventListener('input', () => { transferBtn.disabled = !String(explain.value || '').trim(); });
  }

  let knnNative = null, knnCompare = null, knnExplain = null, knnTransfer = null;
  function inferKnnState() {
    if (!knnNative) return;
    const result = document.querySelector('#guidedResult');
    const lock = document.querySelector('#guidedLock');
    const reveal = document.querySelector('#guidedReveal');
    if (result && !result.hidden && result.textContent.trim()) {
      if (state !== 'compared') setState('revealed');
      if (knnCompare) knnCompare.disabled = false;
    } else if (reveal && !reveal.disabled) {
      setState('locked');
    } else if (lock && !lock.disabled) {
      setState('prediction-complete-unlocked');
    }
  }

  function resetKnn(recordReset = true) {
    document.querySelector('#guidedReset')?.click();
    if (knnExplain) knnExplain.value = '';
    if (knnTransfer) knnTransfer.disabled = true;
    if (knnCompare) knnCompare.disabled = true;
    q('.suite-guided-explain-wrap').hidden = true; q('.suite-guided-transfer-wrap').hidden = true;
    if (recordReset) {
      setState('reset'); requestAnimationFrame(() => { if (state === 'reset') setState('inactive'); });
    } else { state = 'inactive'; shell.dataset.guidedState = state; }
  }

  function setupKnn() {
    q('.suite-guided-generic').hidden = true;
    const nativeHost = q('.suite-guided-native'); nativeHost.hidden = false;
    knnNative = document.querySelector('#knnGuided');
    if (!knnNative) return;
    nativeHost.appendChild(knnNative); knnNative.open = true;
    const extension = document.createElement('div'); extension.className = 'suite-guided-knn-extension';
    extension.innerHTML = `
      <div class="suite-guided-actions"><button type="button" class="suite-guided-knn-compare" disabled></button></div>
      <label class="suite-guided-explain-wrap" hidden><span class="suite-guided-explain-label"></span><textarea data-knn-guided-explain rows="3"></textarea></label>
      <div class="suite-guided-transfer-wrap" hidden><p class="suite-guided-transfer-prompt"></p><button type="button" class="suite-guided-knn-transfer" disabled></button></div>`;
    nativeHost.appendChild(extension);
    knnCompare = extension.querySelector('.suite-guided-knn-compare'); knnExplain = extension.querySelector('[data-knn-guided-explain]'); knnTransfer = extension.querySelector('.suite-guided-knn-transfer');
    const renderKnnCopy = () => {
      knnCompare.textContent = c().compare; extension.querySelector('.suite-guided-explain-label').textContent = c().explain;
      extension.querySelector('.suite-guided-transfer-prompt').textContent = lang() === 'zh' ? '改变距离规则后重新预测邻居。' : 'Change the closeness rule and predict the neighbors again.';
      knnTransfer.textContent = c().transfer;
    };
    renderKnnCopy(); window.addEventListener('languagechange', renderKnnCopy);
    document.querySelector('#guidedStart')?.addEventListener('click', () => setTimeout(() => setState('awaiting-prediction'), 0));
    document.querySelector('#guidedLock')?.addEventListener('click', () => setTimeout(inferKnnState, 0));
    document.querySelector('#guidedReveal')?.addEventListener('click', () => setTimeout(inferKnnState, 0));
    document.querySelector('#guidedReset')?.addEventListener('click', () => setTimeout(() => { if (state !== 'reset') setState('inactive'); }, 0));
    const mo = new MutationObserver(inferKnnState);
    ['#guidedLock','#guidedReveal','#guidedResult'].forEach(sel => { const el = document.querySelector(sel); if (el) mo.observe(el,{attributes:true,childList:true,subtree:true}); });
    knnCompare.addEventListener('click', () => {
      if (state !== 'revealed') return; knnCompare.disabled = true;
      extension.querySelector('.suite-guided-explain-wrap').hidden = false; extension.querySelector('.suite-guided-transfer-wrap').hidden = false;
      setState('compared'); knnExplain.focus();
    });
    knnExplain.addEventListener('input', () => knnTransfer.disabled = !knnExplain.value.trim());
    knnTransfer.addEventListener('click', () => {
      if (knnTransfer.disabled) return;
      document.querySelector('#guidedReset')?.click();
      const metric = document.querySelector('#metricSel');
      if (metric) { metric.value = metric.value === 'euclidean' ? 'manhattan' : 'euclidean'; metric.dispatchEvent(new Event('change',{bubbles:true})); }
      document.querySelector('#guidedStart')?.click();
      knnExplain.value = ''; knnTransfer.disabled = true; knnCompare.disabled = true;
      extension.querySelector('.suite-guided-explain-wrap').hidden = true; extension.querySelector('.suite-guided-transfer-wrap').hidden = true;
      setState('awaiting-prediction');
    });
  }

  modeExplore.addEventListener('click', () => setMode('explore'));
  modeGuided.addEventListener('click', () => setMode('guided'));
  resetBtn.addEventListener('click', () => resetChallenge(true));

  document.querySelectorAll('button[data-lang]').forEach(button => button.addEventListener('click', () => {
    const stateBeforeLanguageChange = state;
    const predictionBeforeLanguageChange = lockedPrediction ? JSON.parse(JSON.stringify(lockedPrediction)) : null;
    const liveFieldSnapshot = {};
    genericFieldElements().forEach(el => liveFieldSnapshot[el.dataset.guidedField] = el.value);
    setTimeout(() => {
      state = stateBeforeLanguageChange;
      shell.dataset.guidedState = stateBeforeLanguageChange;
      if (predictionBeforeLanguageChange) lockedPrediction = predictionBeforeLanguageChange;
      renderCopy(predictionBeforeLanguageChange || liveFieldSnapshot);
      if (stateBeforeLanguageChange === 'locked') {
        lockBtn.disabled = true; revealBtn.disabled = false; compareBtn.disabled = true;
      } else if (stateBeforeLanguageChange === 'revealed') {
        lockBtn.disabled = true; revealBtn.disabled = true; compareBtn.disabled = false;
      } else if (stateBeforeLanguageChange === 'compared') {
        lockBtn.disabled = true; revealBtn.disabled = true; compareBtn.disabled = true;
      } else if (stateBeforeLanguageChange === 'prediction-complete-unlocked') {
        lockBtn.disabled = false; revealBtn.disabled = true; compareBtn.disabled = true;
      } else if (stateBeforeLanguageChange === 'awaiting-prediction') {
        updatePredictionState();
      }
      q('.suite-guided-status').textContent = c().states[state] || state;
      if (slug === 'knn-classifier') inferKnnState();
    }, 60);
  }));

  document.querySelector('#hardReset')?.addEventListener('click', () => {
    if (state !== 'inactive' && !internalMutation) resetChallenge(true);
  }, true);

  if (slug === 'knn-classifier') setupKnn(); else setupGeneric();
  renderCopy(); setMode('explore');

  window.__suiteGuidedChallenge = {
    slug,
    mode: () => mode,
    state: () => state,
    history: () => stateHistory.slice(),
    prediction: () => lockedPrediction ? JSON.parse(JSON.stringify(lockedPrediction)) : null,
    actual: () => actualSnapshot,
    fieldKeys: () => config ? config.fields.map(f => f.key) : [],
    start: () => { setMode('guided'); if (slug === 'knn-classifier') document.querySelector('#guidedStart')?.click(); else beginGeneric(); },
    lock: () => { if (slug === 'knn-classifier') document.querySelector('#guidedLock')?.click(); else lockGeneric(); },
    reveal: () => { if (slug === 'knn-classifier') document.querySelector('#guidedReveal')?.click(); else revealGeneric(); },
    compare: () => { if (slug === 'knn-classifier') knnCompare?.click(); else compareGeneric(); },
    reset: () => resetChallenge(true)
  };
})();
