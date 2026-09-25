(() => {
  'use strict';
  // v1.6.1: preserve canonical source text across VI/ES round trips, refresh native layers before overlay activation, and cancel superseded locale timers.

  const SUPPORTED = ['en', 'zh', 'vi', 'es'];
  const SELF_NAMES = { en: 'English', zh: '简体中文', vi: 'Tiếng Việt', es: 'Español' };
  const LOCALE_KEY = 'ai-playgrounds-locale4';
  const slug = window.APPLET_LEARNER_PROFILE?.slug || location.pathname.split('/').filter(Boolean).slice(-2, -1)[0] || 'applet';
  const rootData = window.__AI_PLAYGROUNDS_R4_LOCALES || {};
  rootData.common = rootData.common || {};
  rootData.common.vi = Object.assign({
    "↺ Reset all": "↺ Đặt lại",
    "↺ New world": "↺ Thế giới mới",
    "Before you read": "Trước khi đọc",
    "Misconceptions to test:": "Những hiểu lầm cần kiểm tra:",
    "Core question:": "Câu hỏi trọng tâm:",
    "Run and watch:": "Chạy và quan sát:",
    "Predict first:": "Dự đoán trước:",
    "Explain afterward:": "Giải thích sau:",
    "Apply and compare": "Áp dụng và so sánh",
    "Start with the featured experiment, then use the scenarios to test a prediction.": "Bắt đầu với thí nghiệm nổi bật, rồi dùng các tình huống để kiểm tra dự đoán.",
    "Open the mechanism view and lesson sequence when you need to explain why the result changed.": "Mở phần mô tả cơ chế và trình tự bài học khi cần giải thích vì sao kết quả thay đổi.",
    "Collect reasoning with the worksheet or the local student response packet.": "Ghi lại lập luận bằng phiếu học tập hoặc bộ câu trả lời của học sinh được lưu cục bộ.",
    "Use the text-state description and keyboard guidance when the visual display is not enough.": "Dùng mô tả trạng thái bằng văn bản và hướng dẫn bàn phím khi hình ảnh hiển thị chưa đủ.",
    "Applet learning modes": "Các chế độ học tập của applet",
    "Copy this experiment": "Sao chép thí nghiệm này",
    "Experiment link copied.": "Đã sao chép liên kết thí nghiệm.",
    "Copy this experiment URL": "Sao chép URL của thí nghiệm này",
    "Understand": "Tìm hiểu",
    "Use in class": "Dùng trong lớp",
    "Text and keyboard": "Văn bản và bàn phím",
    "What this applet shows": "Điều applet này minh họa",

    "Jump to latest": "Về trạng thái mới nhất",
    "Jump to frame": "Đến khung",
    "Jump to iteration": "Đến lần lặp",
    "Jump to step": "Đến bước",
    "Jump to episode": "Đến tập",
    "Jump to epoch": "Đến vòng huấn luyện",
    "Scrub through steps": "Xem lại các bước",
    '✓ Applied; compare the result': '✓ Đã áp dụng; hãy so sánh kết quả',
    'Learning mode': 'Chế độ học tập',
    'Explore': 'Khám phá',
    'Guided Challenge': 'Thử thách có hướng dẫn',
    'Prepare challenge': 'Chuẩn bị thử thách',
    'Lock prediction': 'Khóa dự đoán',
    'Reveal mechanism': 'Tiết lộ cơ chế',
    'Compare': 'So sánh',
    'Reset challenge': 'Đặt lại thử thách',
    'Explain the discrepancy': 'Giải thích sự khác biệt',
    'Try changed case': 'Thử trường hợp đã thay đổi',
    'Your locked prediction': 'Dự đoán đã khóa của bạn',
    'Revealed applet state': 'Trạng thái applet đã tiết lộ',
    'Before the hidden step': 'Trước bước bị ẩn',
    'After the hidden step': 'Sau bước bị ẩn',
    'The relevant result is hidden until you lock a prediction and reveal it.': 'Kết quả liên quan sẽ được ẩn cho đến khi bạn khóa dự đoán và chọn tiết lộ.',
    'Bayes Rule Playground': 'Sân chơi Quy tắc Bayes',
    'Bayesian Network': 'Mạng Bayes',
    'CNF and SAT Builder': 'Trình xây dựng CNF và SAT',
    'Convolution Playground': 'Sân chơi tích chập',
    'Hill Climbing and Simulated Annealing': 'Leo đồi và luyện kim mô phỏng',
    'K-Means Clustering': 'Phân cụm K-Means',
    'K-Nearest Neighbors': 'K láng giềng gần nhất',
    'Tiny Neural Network': 'Mạng nơ-ron nhỏ',
    'Overfitting Explorer': 'Khám phá quá khớp',
    'Q-Learning Gridworld': 'Thế giới lưới Q-Learning',
    'Pathfinding Visualizer': 'Trình trực quan hóa tìm đường',
    'Wumpus World': 'Thế giới Wumpus'
  }, rootData.common.vi || {});
  rootData.common.es = Object.assign({
    "↺ Reset all": "↺ Restablecer",
    "↺ New world": "↺ Nuevo mundo",
    "Before you read": "Antes de leer",
    "Misconceptions to test:": "Ideas erróneas que comprobar:",
    "Core question:": "Pregunta central:",
    "Run and watch:": "Ejecuta y observa:",
    "Predict first:": "Predice primero:",
    "Explain afterward:": "Explica después:",
    "Apply and compare": "Aplicar y comparar",
    "Start with the featured experiment, then use the scenarios to test a prediction.": "Empieza con el experimento destacado y usa los escenarios para comprobar una predicción.",
    "Open the mechanism view and lesson sequence when you need to explain why the result changed.": "Abre la vista del mecanismo y la secuencia de la lección para explicar por qué cambió el resultado.",
    "Collect reasoning with the worksheet or the local student response packet.": "Recoge el razonamiento con la hoja de actividades o el cuaderno de respuestas del estudiante guardado localmente.",
    "Use the text-state description and keyboard guidance when the visual display is not enough.": "Usa la descripción textual del estado y la guía del teclado cuando la visualización no sea suficiente.",
    "Applet learning modes": "Modos de aprendizaje del applet",
    "Copy this experiment": "Copiar este experimento",
    "Experiment link copied.": "Enlace del experimento copiado.",
    "Copy this experiment URL": "Copia la URL de este experimento",
    "Understand": "Comprender",
    "Use in class": "Usar en clase",
    "Text and keyboard": "Texto y teclado",
    "What this applet shows": "Lo que muestra este applet",

    "Jump to latest": "Ir al estado más reciente",
    "Jump to frame": "Ir al estado",
    "Jump to iteration": "Ir a la iteración",
    "Jump to step": "Ir al paso",
    "Jump to episode": "Ir al episodio",
    "Jump to epoch": "Ir a la época",
    "Scrub through steps": "Explorar los pasos",
    '✓ Applied; compare the result': '✓ Aplicado; compara el resultado',
    'Learning mode': 'Modo de aprendizaje',
    'Explore': 'Explorar',
    'Guided Challenge': 'Desafío guiado',
    'Prepare challenge': 'Preparar desafío',
    'Lock prediction': 'Bloquear predicción',
    'Reveal mechanism': 'Revelar mecanismo',
    'Compare': 'Comparar',
    'Reset challenge': 'Reiniciar desafío',
    'Explain the discrepancy': 'Explica la discrepancia',
    'Try changed case': 'Probar caso modificado',
    'Your locked prediction': 'Tu predicción bloqueada',
    'Revealed applet state': 'Estado revelado del applet',
    'Before the hidden step': 'Antes del paso oculto',
    'After the hidden step': 'Después del paso oculto',
    'The relevant result is hidden until you lock a prediction and reveal it.': 'El resultado relevante permanece oculto hasta que bloquees una predicción y lo reveles.',
    'Bayes Rule Playground': 'Laboratorio de la regla de Bayes',
    'Bayesian Network': 'Red bayesiana',
    'CNF and SAT Builder': 'Constructor de CNF y SAT',
    'Convolution Playground': 'Laboratorio de convolución',
    'Hill Climbing and Simulated Annealing': 'Escalada de colinas y recocido simulado',
    'K-Means Clustering': 'Agrupación K-Means',
    'K-Nearest Neighbors': 'K vecinos más cercanos',
    'Tiny Neural Network': 'Red neuronal pequeña',
    'Overfitting Explorer': 'Explorador de sobreajuste',
    'Q-Learning Gridworld': 'Entorno de cuadrícula Q-Learning',
    'Pathfinding Visualizer': 'Visualizador de búsqueda de rutas',
    'Wumpus World': 'Mundo de Wumpus'
  }, rootData.common.es || {});
  const data = rootData[slug] || null;

  // R4 stays invisible until the applet-specific VI/ES catalog is complete.
  if (!data || data.ready !== true || !data.vi || !data.es) return;

  // Scope navigation labels to the footer; Source in a mechanism is not source code.
  const footerLabels = {"vi":{"footer-top":"↑ Lên đầu trang","footer-portfolio":"Hồ sơ","footer-source":"Mã nguồn","footer-issue":"Báo lỗi"},"es":{"footer-top":"↑ Volver arriba","footer-portfolio":"Portafolio","footer-source":"Código fuente","footer-issue":"Informar de un problema"}};
  // Teacher headings and short rich-text fragments never enter substring lookup.
  const teacherLabels = {vi: {'For teachers': 'Dành cho giáo viên', 'Curriculum:': 'Nội dung học:', 'Pre-exploration prompts:': 'Câu hỏi trước khi khám phá:', 'Post-exploration prompts:': 'Câu hỏi sau khi khám phá:'}, es: {'For teachers': 'Para docentes', 'Curriculum:': 'Contenidos:', 'Pre-exploration prompts:': 'Preguntas antes de explorar:', 'Post-exploration prompts:': 'Preguntas después de explorar:'}};
  // Exact original-header titles only; never translate body or learner text in ZH.
  const headerTitlesZh = {
    "Copy an <iframe> snippet for embedding in an LMS. Strips header/essay so only the interactive area shows.": "复制用于嵌入学习管理系统（LMS）的 <iframe> 代码。隐藏页头和说明，仅显示交互区。",
    "Reset everything to defaults: empty grid, A*, default start and goal positions.": "恢复默认设置：空网格、A* 算法及默认起点和终点。",
    "Reset everything to defaults: TSP, best-improvement, T₀=10, cooling=0.995.": "恢复默认设置：旅行商问题、最佳改进法、初始温度 T₀=10、降温系数 0.995。",
    "Generate a new random world, clear the log, reset score.": "生成新的随机世界，清空日志并重置分数。",
    "Reset input to default 'modus ponens' example.": "将输入恢复为默认的“肯定前件式”示例。",
    "Reset to default disease scenario: prior=1%, sensitivity=99%, specificity=95%, population=10000.": "恢复默认疾病检测情景：患病率 1%、灵敏度 99%、特异度 95%、人数 10000。",
    "Reset CPTs to AIMA defaults and clear all evidence.": "将条件概率表恢复为 AIMA 默认值，并清除所有观测证据。",
    "Reset everything to defaults: two-moons dataset, k=5, both visualizations on.": "恢复默认设置：双月数据集、k=5，并开启两个可视化图层。",
    "Reset everything: sin truth, n=20 points, σ=0.2 noise, degree 3, λ=0.": "恢复默认设置：真实函数为 sin、n=20 个点、噪声 σ=0.2、多项式次数为 3、λ=0。",
    "Reset everything to default: two-moons dataset, [2-6-4-1] architecture, ReLU activation, LR=0.03.": "恢复默认设置：双月数据集、[2-6-4-1] 网络结构、ReLU 激活函数、学习率 0.03。",
    "Reset everything to the default: Gaussian mixture dataset, k=3, random init.": "恢复默认设置：高斯混合数据集、k=3、随机初始化。",
    "Reset to default: cross input, Sobel-X edge kernel, abs ON, ReLU OFF.": "恢复默认设置：十字形输入、Sobel-X 边缘检测核，开启绝对值变换，关闭 ReLU。",
    "Clear Q-values; restore the default grid, learning rate, discount factor, exploration rate and step reward.": "清空 Q 值；将网格、学习率、折扣因子、探索率和每步奖励恢复为默认值。",
    "Download the current grid + search trace as a PNG.": "将当前网格和搜索轨迹下载为 PNG 图片。",
    "Download the current state visualization as a PNG.": "将当前状态的可视化下载为 PNG 图片。",
    "Download the world view as a PNG.": "将世界视图下载为 PNG 图片。",
    "Download the population dot-grid as a PNG.": "将人群点阵图下载为 PNG 图片。",
    "Download the network diagram as a PNG.": "将网络图下载为 PNG 图片。",
    "Download the current points + decision boundary as a PNG.": "将当前数据点和决策边界下载为 PNG 图片。",
    "Download the fit canvas as a PNG.": "将拟合图下载为 PNG 图片。",
    "Download the decision-boundary canvas as a PNG.": "将决策边界图下载为 PNG 图片。",
    "Download the current visualization as a PNG image (for slides).": "将当前可视化下载为 PNG 图片（可用于幻灯片）。",
    "Download the convolution output as a PNG.": "将卷积输出下载为 PNG 图片。",
    "Download the current grid + Q-value heatmap as a PNG.": "将当前网格和 Q 值热力图下载为 PNG 图片。",
    "Download grid dimensions and search results (path coordinates, visited-node count, frontier snapshot) as CSV.": "将网格尺寸和搜索结果（路径坐标、已访问节点数、搜索前沿快照）下载为 CSV。",
    "Download per-iteration costs, algorithm, problem, iteration count and best cost as CSV.": "将每次迭代的代价、算法、问题、迭代次数和最佳代价下载为 CSV。",
    "Download the current Bayes scenario (prior, sens, spec, population) and the resulting contingency table + posteriors as CSV.": "将当前贝叶斯情景（先验概率、灵敏度、特异度、人数）、列联表和后验概率下载为 CSV。",
    "Download training + validation datasets and the per-degree MSE table as CSV.": "将训练集、验证集和各多项式次数的均方误差表下载为 CSV。",
    "Download points + cluster assignments + centroid positions as CSV (two sections in one file).": "将数据点、所属簇和质心位置下载为 CSV（同一文件内分为两个部分）。",
    "Download episode return history + the current Q-table snapshot as CSV.": "将各回合的回报历史和当前 Q 表快照下载为 CSV。"
  };
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
  let canonicalDocumentTitle = '';
  let canonicalHeadingText = '';
  let pendingOverlayTimer = null;

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
    return Object.assign({}, local, common);
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
    if (el.closest('.suite-guided-actual')) return false;
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
    if (!originalText.has(node)) originalText.set(node, live);
    const source = textSource(node);
    const footerKey = node.parentElement?.closest('footer [data-i18n]')?.dataset.i18n;
    // Match formatted teacher prose only; retain source and outer whitespace.
    const proseKey = node.parentElement?.closest('.for-teachers')
      ? source.replace(/\s+/g, ' ').trim() : null;
    const proseMap = proseKey === null ? null
      : Object.assign({}, mapFor(current), data[current]?.teacher || {}, teacherLabels[current] || {});
    const prose = proseMap && Object.prototype.hasOwnProperty.call(proseMap, proseKey)
      ? source.replace(/\S(?:[\s\S]*\S)?/, () => proseMap[proseKey]) : null;
    const translated = footerLabels[current]?.[footerKey] || prose || translateString(source);
    if (translated !== live) {
      lastAppliedText.set(node, translated);
      applying = true;
      node.nodeValue = translated;
      applying = false;
    }
  }

  function translateAttributes(el, attributes = ['title', 'aria-label', 'placeholder']) {
    if (!el || el.nodeType !== 1 || skipNode(el)) return;
    const state = attrState(el);
    for (const attr of attributes) {
      if (!el.hasAttribute(attr)) continue;
      const live = el.getAttribute(attr) || '';
      if (!Object.prototype.hasOwnProperty.call(state, attr)) state[attr] = live;
      const source = Object.prototype.hasOwnProperty.call(state, attr) ? state[attr] : live;
      const zhTitle = current === 'zh' && attr === 'title' && el.closest('.header-actions')
        && ['hardReset', 'embedLink', 'csvExport', 'exportPng'].includes(el.id)
        ? headerTitlesZh[source] : null;
      const translated = current === 'zh'
        ? (typeof zhTitle === 'string' ? zhTitle : live) : translateString(source);
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

  function refreshHeaderTitles() {
    if (current !== 'en' && current !== 'zh') return;
    document.querySelectorAll('.header-actions #hardReset,.header-actions #embedLink,.header-actions #csvExport,.header-actions #exportPng').forEach(el => {
      const source = originalAttrs.get(el)?.title ?? el.getAttribute('title');
      if (Object.prototype.hasOwnProperty.call(headerTitlesZh, source)) translateAttributes(el, ['title']);
    });
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
          Object.entries(state).forEach(([a, v]) => node.setAttribute(a, v));
        }
      }
    } finally { applying = false; }
  }

  function nativeButton(locale) {
    return document.querySelector(`.lang-switch button[data-lang="${locale}"]`);
  }

  function nativeLocale() {
    const active = document.querySelector('.lang-switch button[data-lang].active');
    return normalizeLocale((active && active.dataset.lang) || document.documentElement.lang || 'en');
  }

  function clickNative(locale) {
    locale = normalizeLocale(locale);
    const btn = nativeButton(locale);
    if (!btn) return false;
    // Do not re-run native language handlers when the applet is already in the
    // requested language. On initial page load a redundant EN click can race with
    // Guided Challenge setup and reset/rebuild applet state after the challenge
    // has begun.
    if (nativeLocale() === locale) return true;
    nativeLanguageClick = true;
    try { btn.click(); } finally { nativeLanguageClick = false; }
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

  function selectControl() {
    return document.querySelector('.r4-language-select');
  }

  function updateSelect(locale) {
    const names = {
      en: ['Language', 'Toggle dark or light theme'],
      zh: ['语言', '切换深色或浅色主题'],
      vi: ['Ngôn ngữ', 'Chuyển giao diện tối hoặc sáng'],
      es: ['Idioma', 'Cambiar entre tema oscuro y claro']
    }[locale];
    const select = selectControl();
    if (select) {
      select.value = locale;
      select.setAttribute('aria-label', names[0]);
    }
    const theme = document.getElementById('themeToggle');
    if (theme) {
      theme.setAttribute('data-r4-no-translate', '1');
      theme.setAttribute('aria-label', names[1]);
      theme.setAttribute('title', names[1]);
    }
  }

  function activateOverlay(locale) {
    current = 'en';
    document.documentElement.lang = 'en';
    refreshKnownLayers();
    current = locale;
    document.documentElement.lang = locale;
    wrapTr();
    // Exporters localize their labels; never translate learner-authored clipboard data.
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
    if (pendingOverlayTimer !== null) {
      clearTimeout(pendingOverlayTimer);
      pendingOverlayTimer = null;
    }
    restoreTree(document.body);
    if (locale === 'en' || locale === 'zh') {
      current = locale;
      clickNative(locale);
      document.documentElement.lang = locale === 'zh' ? 'zh' : 'en';
      refreshKnownLayers();
      refreshHeaderTitles();
      if (locale === 'en') {
        const heading = document.querySelector('h1');
        if (heading && canonicalHeadingText) {
          applying = true;
          try { heading.textContent = canonicalHeadingText; } finally { applying = false; }
        }
      }
      applyMetadata(locale);
      if (locale === 'en' && canonicalDocumentTitle) document.title = canonicalDocumentTitle;
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
    pendingOverlayTimer = setTimeout(() => {
      pendingOverlayTimer = null;
      activateOverlay(locale);
    }, options.immediate ? 0 : 60);
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
        // Several queued records can observe the same final translated value.
        // Retain its marker until a genuinely different applet value arrives.
        if (lastAppliedText.get(mutation.target) === live) continue;
        lastAppliedText.delete(mutation.target);
        // Applet-authored dynamic state is always a new source value, including
        // while English or Chinese is active. This is what prevents a later locale
        // switch from restoring stale page-load state.
        originalText.set(mutation.target, live);
        if (current === 'vi' || current === 'es') translateTextNode(mutation.target);
      } else if (mutation.type === 'attributes') {
        const attr = mutation.attributeName;
        const live = mutation.target.getAttribute(attr) || '';
        const applied = lastAppliedAttrs.get(mutation.target) || {};
        if (applied[attr] === live) continue;
        delete applied[attr];
        const state = attrState(mutation.target);
        state[attr] = live;
        // Do not overwrite a sibling attribute whose native write is still queued.
        if (current === 'vi' || current === 'es' || current === 'zh' && attr === 'title') translateAttributes(mutation.target, [attr]);
      } else {
        // The native original galleries have no Chinese confirmation entry.
        // Localize only this generated button message, never learner text.
        if (current === 'zh' && mutation.target.matches?.('.scenario-card button')
            && mutation.target.textContent === '✓ Applied; compare the result') {
          mutation.target.textContent = '✓ 已应用；请比较结果';
        }
        // Locale renderers replace the original gallery's cards, not its model.
        // Carry the last applied marker by stable ID; never click/reapply a case.
        if (mutation.target.id === 'scenarioGalleryCards' && !mutation.target.querySelector('.applied')) {
          const previous = [...mutation.removedNodes].find(node => node.nodeType === 1 && node.matches('.scenario-card.applied'));
          const index = previous?.dataset.scenarioIndex;
          if (index !== undefined) [...mutation.target.children]
            .find(node => node.dataset.scenarioIndex === index)?.classList.add('applied');
        }
        mutation.addedNodes.forEach(node => {
          if (current === 'vi' || current === 'es') translateTree(node);
        });
      }
    }
  });

  function init() {
    canonicalDocumentTitle = document.title;
    const initialHeading = document.querySelector('h1');
    canonicalHeadingText = initialHeading ? initialHeading.textContent : '';
    installSelect();
    wrapTr();
    // Exporters localize their labels; never translate learner-authored clipboard data.
    observer.observe(document.body, { subtree:true, childList:true, characterData:true, attributes:true, attributeFilter:['title','aria-label','placeholder'] });
    // Legacy language handlers in some applets rebuild or reset the experiment as
    // part of their EN/ZH switch. R4 invokes those buttons only as an internal
    // rendering bridge; locale changes must not mutate learner/challenge state.
    // A synchronous hard-reset click dispatched by that bridge is therefore
    // suppressed in capture phase. Normal user reset clicks are unaffected.
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
        refreshHeaderTitles();
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
