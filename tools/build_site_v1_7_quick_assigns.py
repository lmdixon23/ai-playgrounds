#!/usr/bin/env python3
from __future__ import annotations

import html as html_lib
import json
import re
from pathlib import Path

import build_site_v1_6_2 as base
import build_site_v1_6_1_candidate as legacy_qa
import build_site_v1_6_1_public as support

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
REGISTRY = ROOT / "tools" / "quick_assigns_v2.json"

# The first four Quick Assign translations remain owned by the historical v1.6.1
# builder. These are only the eight remaining original-app response packets.
NEW_COPY = {
 "QA-BAYES-01": {
  "vi":{"summary":"🧪 Bài tập nhanh · QA-BAYES-01 · 10–15 phút","title":"Tỷ lệ nền và báo động giả","intro":"Thay đổi tỷ lệ nền và chất lượng phép kiểm tra, rồi giải thích vì sao một kết quả dương tính không tự động có nghĩa xác suất hậu nghiệm cao.","predict":"Trước khi chạy, bạn dự đoán xác suất hậu nghiệm sau kết quả dương tính sẽ cao hay thấp? Yếu tố nào quan trọng nhất?","observe":"Chạy hai trường hợp với tỷ lệ nền khác nhau. Ghi lại prior, true positive, false positive và posterior.","explain":"Vì sao cùng một phép kiểm tra có thể cho posterior khác nhau khi tỷ lệ nền thay đổi?","transfer":"Trong tình huống thực tế nào việc bỏ qua tỷ lệ nền có thể tạo ra quá nhiều báo động giả?"},
  "es":{"summary":"🧪 Tarea rápida · QA-BAYES-01 · 10–15 min","title":"Tasas base y falsas alarmas","intro":"Cambia la tasa base y la calidad de la prueba y explica por qué un resultado positivo no implica por sí solo una probabilidad posterior alta.","predict":"Antes de ejecutar, ¿esperas una probabilidad posterior alta o baja tras un positivo? ¿Qué factor será más importante?","observe":"Ejecuta dos casos con tasas base distintas. Registra el prior, verdaderos positivos, falsos positivos y posterior.","explain":"¿Por qué la misma prueba puede producir posteriores diferentes cuando cambia la tasa base?","transfer":"¿En qué situación real ignorar la tasa base podría producir demasiadas falsas alarmas?"}},
 "QA-BN-01": {
  "vi":{"summary":"🧪 Bài tập nhanh · QA-BN-01 · 10–15 phút","title":"Hiện tượng giải thích loại trừ","intro":"Dự đoán posterior của hai nguyên nhân, thêm bằng chứng cho một nguyên nhân rồi giải thích vì sao niềm tin vào nguyên nhân kia có thể giảm.","predict":"Sau khi quan sát hiệu ứng chung, điều gì sẽ xảy ra với nguyên nhân B nếu sau đó có bằng chứng mạnh cho nguyên nhân A?","observe":"Ghi lại posterior trước và sau khi thêm bằng chứng cho một nguyên nhân chung của cùng hiệu ứng.","explain":"Vì sao thay đổi này là phụ thuộc có điều kiện qua hiệu ứng chung chứ không phải A trực tiếp làm giảm B?","transfer":"Mô tả một ví dụ khác trong đó hai lời giải thích cạnh tranh cho cùng một bằng chứng có thể giải thích loại trừ nhau."},
  "es":{"summary":"🧪 Tarea rápida · QA-BN-01 · 10–15 min","title":"Explicación alternativa","intro":"Predice los posteriores de dos causas, añade evidencia para una causa y explica por qué puede bajar la creencia en la otra.","predict":"Tras observar el efecto común, ¿qué ocurrirá con la causa B si después aparece evidencia fuerte para la causa A?","observe":"Registra el posterior antes y después de añadir evidencia para una de dos causas de un efecto común.","explain":"¿Por qué el cambio es dependencia condicional a través del efecto común y no que A reduzca directamente B?","transfer":"Describe otro caso en que dos explicaciones competidoras de la misma evidencia puedan explicarse mutuamente."}},
 "QA-KNN-01": {
  "vi":{"summary":"🧪 Bài tập nhanh · QA-KNN-01 · 10–15 phút","title":"Những láng giềng nào được bỏ phiếu?","intro":"Đặt một điểm truy vấn, dự đoán các láng giềng gần nhất và lớp, rồi thay đổi k để xem lá phiếu thay đổi thế nào.","predict":"Trước khi tiết lộ, những điểm huấn luyện nào sẽ là k láng giềng gần nhất và lớp nào sẽ thắng?","observe":"Ghi lại k, các láng giềng được chọn, khoảng cách hoặc thứ tự gần nhất và lớp dự đoán.","explain":"Khoảng cách quyết định ai được bỏ phiếu và k ảnh hưởng đến độ nhạy với nhiễu cục bộ như thế nào?","transfer":"Điều gì có thể xảy ra gần biên quyết định nếu tăng k từ 1 lên một giá trị lớn hơn?"},
  "es":{"summary":"🧪 Tarea rápida · QA-KNN-01 · 10–15 min","title":"¿Qué vecinos obtienen el voto?","intro":"Coloca un punto de consulta, predice sus vecinos más cercanos y su clase y cambia k para observar cómo cambia la votación.","predict":"Antes de revelar, ¿qué puntos serán los k vecinos más cercanos y qué clase ganará?","observe":"Registra k, los vecinos elegidos, sus distancias u orden de cercanía y la clase predicha.","explain":"¿Cómo decide la distancia quién vota y cómo afecta k a la sensibilidad al ruido local?","transfer":"¿Qué puede ocurrir cerca de una frontera de decisión al aumentar k desde 1 a un valor mayor?"}},
 "QA-OVERFIT-01": {
  "vi":{"summary":"🧪 Bài tập nhanh · QA-OVERFIT-01 · 10–15 phút","title":"Khớp dữ liệu huấn luyện, thất bại trên dữ liệu mới","intro":"Tăng độ phức tạp mô hình, so sánh lỗi huấn luyện với lỗi kiểm tra và tìm điểm mà khớp tốt hơn không còn có nghĩa tổng quát hóa tốt hơn.","predict":"Khi độ phức tạp tăng, bạn dự đoán lỗi huấn luyện và lỗi kiểm tra sẽ thay đổi thế nào?","observe":"Ghi lại ít nhất ba mức độ phức tạp cùng lỗi huấn luyện và kiểm tra tương ứng.","explain":"Dấu hiệu nào cho thấy mô hình bắt đầu overfit thay vì chỉ cải thiện?","transfer":"Nếu có nhiều dữ liệu huấn luyện hơn, bạn dự đoán điểm bắt đầu overfit sẽ thay đổi như thế nào?"},
  "es":{"summary":"🧪 Tarea rápida · QA-OVERFIT-01 · 10–15 min","title":"Ajusta el entrenamiento, falla en datos nuevos","intro":"Aumenta la complejidad, compara error de entrenamiento y prueba y encuentra cuándo un mejor ajuste deja de significar mejor generalización.","predict":"Al aumentar la complejidad, ¿cómo esperas que cambien los errores de entrenamiento y prueba?","observe":"Registra al menos tres niveles de complejidad con sus errores de entrenamiento y prueba.","explain":"¿Qué patrón muestra que el modelo empieza a sobreajustar en vez de simplemente mejorar?","transfer":"Si hubiera más datos de entrenamiento, ¿cómo esperas que cambiara el punto en que comienza el sobreajuste?"}},
 "QA-NN-01": {
  "vi":{"summary":"🧪 Bài tập nhanh · QA-NN-01 · 10–15 phút","title":"Vì sao phi tuyến làm thay đổi năng lực biểu diễn","intro":"So sánh mạng chỉ gồm các phép biến đổi affine với mạng có activation phi tuyến và giải thích sự thay đổi của biên quyết định.","predict":"Nếu xếp chồng nhiều lớp tuyến tính mà không có activation phi tuyến, mạng có thể tạo biên quyết định phi tuyến không? Vì sao?","observe":"Chạy cùng dữ liệu với activation tuyến tính và phi tuyến. Ghi lại hình dạng biên và một chỉ số loss hoặc accuracy.","explain":"Tại sao nhiều lớp affine liên tiếp vẫn tương đương một phép biến đổi affine?","transfer":"Loại mẫu dữ liệu nào đặc biệt cần biểu diễn phi tuyến thay vì một biên tuyến tính?"},
  "es":{"summary":"🧪 Tarea rápida · QA-NN-01 · 10–15 min","title":"Por qué la no linealidad cambia la capacidad","intro":"Compara una red formada solo por transformaciones afines con otra que usa activación no lineal y explica el cambio de frontera de decisión.","predict":"Si apilas varias capas lineales sin activación no lineal, ¿puede la red crear una frontera no lineal? ¿Por qué?","observe":"Ejecuta los mismos datos con activación lineal y no lineal. Registra la forma de la frontera y una medida de pérdida o precisión.","explain":"¿Por qué varias capas afines consecutivas siguen siendo equivalentes a una sola transformación afín?","transfer":"¿Qué tipo de patrón de datos necesita especialmente una representación no lineal en vez de una frontera lineal?"}},
 "QA-KMEANS-01": {
  "vi":{"summary":"🧪 Bài tập nhanh · QA-KMEANS-01 · 10–15 phút","title":"Gán điểm, di chuyển tâm, lặp lại","intro":"Dự đoán một bước gán cụm và cập nhật centroid, rồi giải thích chu kỳ xen kẽ của k-means.","predict":"Với các centroid hiện tại, điểm được chọn sẽ được gán vào cụm nào và vì sao?","observe":"Ghi lại một phép gán, centroid trước cập nhật và centroid sau cập nhật.","explain":"Hai bước gán điểm và cập nhật centroid phụ thuộc lẫn nhau như thế nào?","transfer":"Tại sao hai cách khởi tạo centroid khác nhau có thể dẫn đến kết quả cuối cùng khác nhau?"},
  "es":{"summary":"🧪 Tarea rápida · QA-KMEANS-01 · 10–15 min","title":"Asigna, mueve, repite","intro":"Predice una asignación y una actualización de centroide y explica el ciclo alternante de k-means.","predict":"Con los centroides actuales, ¿a qué grupo se asignará el punto elegido y por qué?","observe":"Registra una asignación, el centroide antes de actualizar y el centroide después.","explain":"¿Cómo dependen entre sí los pasos de asignar puntos y actualizar centroides?","transfer":"¿Por qué dos inicializaciones distintas pueden terminar en agrupamientos diferentes?"}},
 "QA-CNN-01": {
  "vi":{"summary":"🧪 Bài tập nhanh · QA-CNN-01 · 10–15 phút","title":"Một ô tích chập","intro":"Chọn một vùng ảnh và kernel, dự đoán phép nhân-và-cộng cho một ô đầu ra rồi kiểm tra giá trị feature map.","predict":"Trước khi tiết lộ, giá trị ô đầu ra này sẽ dương, âm hay gần 0? Giải thích từ patch và kernel.","observe":"Ghi lại patch, kernel, các tích quan trọng và tổng đầu ra cho một vị trí.","explain":"Vì sao cùng một kernel được áp dụng lặp lại ở các vị trí khác nhau của ảnh?","transfer":"Một kernel phát hiện cạnh theo hướng khác sẽ thay đổi phản hồi với cùng patch như thế nào?"},
  "es":{"summary":"🧪 Tarea rápida · QA-CNN-01 · 10–15 min","title":"Una celda de convolución","intro":"Elige un parche y un kernel, predice la multiplicación-y-suma de una celda y comprueba el valor del mapa de características.","predict":"Antes de revelar, ¿será el valor de esta celda positivo, negativo o cercano a 0? Razona con el parche y el kernel.","observe":"Registra el parche, el kernel, los productos importantes y la suma de salida para una posición.","explain":"¿Por qué se aplica el mismo kernel repetidamente en distintas posiciones de la imagen?","transfer":"¿Cómo cambiaría la respuesta del mismo parche con un kernel que detectara bordes en otra dirección?"}},
 "QA-QL-01": {
  "vi":{"summary":"🧪 Bài tập nhanh · QA-QL-01 · 10–15 phút","title":"Một lần cập nhật Q","intro":"Dự đoán hành động và hướng cập nhật Q, bước tác tử rồi nối reward, giá trị trạng thái kế tiếp và learning rate với thay đổi.","predict":"Trước bước tiếp theo, bạn dự đoán Q-value của hành động được chọn sẽ tăng hay giảm? Vì sao?","observe":"Ghi lại trạng thái, hành động, reward, ước lượng trạng thái kế tiếp và Q-value trước/sau cập nhật.","explain":"TD target và learning rate quyết định độ lớn/hướng cập nhật Q như thế nào?","transfer":"Exploration có thể chọn hành động khác với policy tham lam như thế nào ngay cả khi Q-values đã hình thành?"},
  "es":{"summary":"🧪 Tarea rápida · QA-QL-01 · 10–15 min","title":"Una actualización Q","intro":"Predice la acción y la dirección de la actualización, avanza el agente y conecta recompensa, valor del siguiente estado y tasa de aprendizaje con el cambio.","predict":"Antes del siguiente paso, ¿esperas que el Q-value de la acción elegida suba o baje? ¿Por qué?","observe":"Registra estado, acción, recompensa, estimación del siguiente estado y Q-value antes/después de la actualización.","explain":"¿Cómo determinan el objetivo TD y la tasa de aprendizaje la dirección y magnitud de la actualización Q?","transfer":"¿Cómo puede la exploración elegir una acción distinta de la política voraz incluso cuando ya existen Q-values aprendidos?"}}
}

ZH = {
 "QA-BAYES-01":{"title":"基础率与误报","focus":"连接先验流行率、真阳性、假阳性与后验概率。","look":"优秀回答应说明后验同时取决于检测质量和先验/基础率，不能把准确率或敏感度直接当作阳性后的患病概率。"},
 "QA-BN-01":{"title":"解释消除","focus":"预测在共同结果已知后，一项原因证据如何降低对另一原因的信念。","look":"优秀回答应比较前后后验，并用共同结果造成的条件依赖来解释变化，而不是说一个原因直接抑制另一个原因。"},
 "QA-KNN-01":{"title":"哪些邻居获得投票？","focus":"预测最近邻和类别，再把 k 与距离连接到投票结果。","look":"优秀回答应识别实际最近邻，区分距离与类别投票，并解释改变 k 如何改变对局部噪声的敏感度。"},
 "QA-OVERFIT-01":{"title":"拟合训练集，却败给新数据","focus":"随模型容量变化区分训练误差与验证/测试表现。","look":"优秀回答应指出容量增加仍改善训练拟合但留出数据表现停止改善或恶化的区间，而不是把复杂模型本身定义为过拟合。"},
 "QA-NN-01":{"title":"为什么非线性改变表示能力","focus":"比较纯仿射网络与非线性隐藏表示并解释决策边界的变化。","look":"优秀回答应说明没有非线性激活时多层仿射变换仍是仿射变换，并把非线性与表示非线性边界的能力联系起来。"},
 "QA-KMEANS-01":{"title":"分配、移动、重复","focus":"预测一次分配和质心更新，再解释 k-means 的交替循环。","look":"优秀回答应区分分配步骤与质心更新步骤，引用距离或成员关系证据，并认识到初始化可能改变最终聚类。"},
 "QA-CNN-01":{"title":"一个卷积输出单元","focus":"在揭示特征图值之前预测一个输出单元的乘加计算。","look":"优秀回答应把 kernel 元素与局部图像 patch 对齐，正确执行或解释乘加，并区分滤波响应与语义对象标签。"},
 "QA-QL-01":{"title":"一次 Q 更新","focus":"在学习器执行一步之前预测动作、TD 目标与更新方向。","look":"优秀回答应把奖励、折扣后的下一状态价值、当前 Q 值和学习率连接到更新方向，并区分探索与已学习策略。"},
 "QA-MINIMAX-01":{"title":"同一答案，更少搜索","focus":"解释安全的 Alpha-Beta 截断为何减少评估工作却不改变 minimax 结果。","look":"优秀回答应用 alpha/beta 界说明被跳过分支为何不可能改善当前决策，并明确 Alpha-Beta 返回完全相同的 minimax 值。"},
 "QA-TRANSFORMER-01":{"title":"先注意，再预测","focus":"把受控的表示/注意力变化连接到下一 token 概率分布。","look":"优秀回答应引用具体的注意力、logit 或概率变化，区分注意力权重与完整预测解释，并区分概率分布与生成选择规则。"},
 "QA-AGENT-01":{"title":"提出工具调用不等于执行动作","focus":"追踪一个工具调用通过验证、授权、执行、观察与上下文更新。","look":"优秀回答应区分模型输出、schema 有效性、授权、执行与观察，并指出无效或被拒绝动作在哪个具体 gate 停止。"}
}

MODERN = {
 "QA-TRANSFORMER-01": {
  "event":"lab13localechange","challenge_marker":'<section class="card challenge">',
  "copy":{
   "en":{"summary":"Quick Assign · QA-TRANSFORMER-01 · 10–15 min","title":"Attend, then predict","intro":"Use one Guided Challenge below. Predict first, reveal the mechanism, then connect a concrete attention/logit/probability change to the next-token distribution.","predict":"Which source token, mask condition, or temperature change do you expect to matter most, and why?","observe":"Record the challenge, one attention/logit/probability value before or after the change, and the resulting top prediction or distribution change.","explain":"What changed in the computation, and what would be incorrect about treating the largest attention weight as the complete reason for the prediction?","transfer":"How would you test whether a different token substitution or temperature changes probabilities without changing the learned weights?"},
   "zh":{"summary":"快速任务 · QA-TRANSFORMER-01 · 10–15 分钟","title":"先注意，再预测","intro":"完成下方一个引导挑战。先预测，再揭示机制，然后把具体的注意力、logit 或概率变化连接到下一 token 分布。","predict":"你预计哪个源 token、mask 条件或温度变化影响最大？为什么？","observe":"记录挑战、变化前后一个注意力/logit/概率数值，以及最高预测或分布的变化。","explain":"计算中究竟改变了什么？为什么把最大注意力权重当作预测的完整原因是不正确的？","transfer":"你会怎样检验另一种 token 替换或温度变化只改变概率而不改变学习到的权重？"},
   "vi":{"summary":"Bài tập nhanh · QA-TRANSFORMER-01 · 10–15 phút","title":"Chú ý rồi dự đoán","intro":"Làm một Guided Challenge bên dưới. Dự đoán trước, tiết lộ cơ chế, rồi nối một thay đổi cụ thể về attention/logit/xác suất với phân bố token tiếp theo.","predict":"Bạn dự đoán token nguồn, điều kiện mask hay thay đổi temperature nào quan trọng nhất, và vì sao?","observe":"Ghi lại challenge, một giá trị attention/logit/xác suất trước hoặc sau thay đổi, và thay đổi của dự đoán cao nhất hoặc phân bố.","explain":"Điều gì đã thay đổi trong phép tính, và vì sao coi attention weight lớn nhất là toàn bộ lý do của dự đoán là sai?","transfer":"Bạn sẽ kiểm tra thế nào xem một token substitution hoặc temperature khác có đổi xác suất mà không đổi learned weights?"},
   "es":{"summary":"Tarea rápida · QA-TRANSFORMER-01 · 10–15 min","title":"Atiende y luego predice","intro":"Completa un Guided Challenge de abajo. Predice primero, revela el mecanismo y conecta un cambio concreto de atención/logit/probabilidad con la distribución del siguiente token.","predict":"¿Qué token fuente, condición de máscara o cambio de temperatura esperas que importe más y por qué?","observe":"Registra el reto, un valor de atención/logit/probabilidad antes o después del cambio y el cambio de la predicción principal o de la distribución.","explain":"¿Qué cambió en el cálculo y por qué sería incorrecto tratar el mayor peso de atención como la razón completa de la predicción?","transfer":"¿Cómo comprobarías si otra sustitución de token o temperatura cambia probabilidades sin cambiar los pesos aprendidos?"}}
 },
 "QA-AGENT-01": {
  "event":"lab14localechange","challenge_marker":'<section class="card challenge">',
  "copy":{
   "en":{"summary":"Quick Assign · QA-AGENT-01 · 10–15 min","title":"A proposed call is not an executed action","intro":"Use one Guided Challenge below and trace the candidate action through the actual runtime gates before deciding whether anything executes.","predict":"Will the proposed action execute, stop at validation, stop at authorization, fail during execution, or correctly stop? Why?","observe":"Record the proposed output, the first decisive gate, whether execution occurred, and what observation/context change followed.","explain":"Why are tool availability, schema validity, authorization, execution, and observation different states?","transfer":"How should the runtime treat instruction-like text returned by a tool, and why does provenance matter?"},
   "zh":{"summary":"快速任务 · QA-AGENT-01 · 10–15 分钟","title":"提出调用不等于执行动作","intro":"完成下方一个引导挑战，在判断是否真正执行前，把候选动作逐步追踪经过实际 runtime gates。","predict":"该动作会执行、在验证停止、在授权停止、执行时失败，还是应该正确停止？为什么？","observe":"记录提出的输出、第一个决定性 gate、是否发生执行，以及随后出现的 observation/context 变化。","explain":"为什么工具可用、schema 有效、授权、执行与 observation 是不同状态？","transfer":"runtime 应如何处理工具返回的类似指令文本？为什么 provenance 很重要？"},
   "vi":{"summary":"Bài tập nhanh · QA-AGENT-01 · 10–15 phút","title":"Đề xuất gọi công cụ không phải là hành động đã thực thi","intro":"Làm một Guided Challenge bên dưới và theo dõi hành động ứng viên qua các runtime gate thật trước khi quyết định có gì được thực thi hay không.","predict":"Hành động sẽ được thực thi, dừng ở validation, dừng ở authorization, lỗi khi execution hay nên dừng đúng lúc? Vì sao?","observe":"Ghi lại output đề xuất, gate quyết định đầu tiên, execution có xảy ra không và observation/context thay đổi thế nào sau đó.","explain":"Vì sao tool availability, schema validity, authorization, execution và observation là các trạng thái khác nhau?","transfer":"Runtime nên xử lý văn bản giống chỉ dẫn do tool trả về thế nào, và vì sao provenance quan trọng?"},
   "es":{"summary":"Tarea rápida · QA-AGENT-01 · 10–15 min","title":"Una llamada propuesta no es una acción ejecutada","intro":"Completa un Guided Challenge de abajo y sigue la acción candidata por las puertas reales del runtime antes de decidir si algo se ejecuta.","predict":"¿La acción se ejecutará, se detendrá en validación, se detendrá en autorización, fallará al ejecutar o debería detenerse correctamente? ¿Por qué?","observe":"Registra la salida propuesta, la primera puerta decisiva, si hubo ejecución y qué observación/cambio de contexto siguió.","explain":"¿Por qué disponibilidad, validez de esquema, autorización, ejecución y observación son estados distintos?","transfer":"¿Cómo debería tratar el runtime texto con apariencia de instrucción devuelto por una herramienta y por qué importa la procedencia?"}}
 },
 "QA-MINIMAX-01": {
  "event":"lab15localechange","challenge_marker":'<section class="panel challenge">',
  "copy":{
   "en":{"summary":"Quick Assign · QA-MINIMAX-01 · 10–15 min","title":"Same answer, less search","intro":"Use the pruning or move-order Guided Challenge below. Predict first, reveal the trace, then justify why skipped work cannot change the exact minimax answer.","predict":"Will this branch prune, or which move order will evaluate less work? State the bound or ordering reason you expect.","observe":"Record the root value/move, evaluated-work count or first cutoff, and the relevant alpha/beta values when pruning occurs.","explain":"Why is the cutoff safe, and why does Alpha-Beta still return the exact minimax result?","transfer":"How could reordering the same children change search work without changing the game tree or optimal decision?"},
   "zh":{"summary":"快速任务 · QA-MINIMAX-01 · 10–15 分钟","title":"同一答案，更少搜索","intro":"完成下方剪枝或走法顺序引导挑战。先预测，再揭示 trace，并说明为何跳过的工作不能改变精确 minimax 答案。","predict":"该分支会剪枝吗，或哪种走法顺序评估的工作更少？写出你预计的界或排序理由。","observe":"记录根节点价值/走法、评估工作量或第一次 cutoff，以及发生剪枝时相关的 alpha/beta 值。","explain":"为什么 cutoff 是安全的？为什么 Alpha-Beta 仍返回完全相同的 minimax 结果？","transfer":"怎样只重排相同的子节点就改变搜索工作量，却不改变游戏树或最优决策？"},
   "vi":{"summary":"Bài tập nhanh · QA-MINIMAX-01 · 10–15 phút","title":"Cùng đáp án, ít tìm kiếm hơn","intro":"Làm Guided Challenge về pruning hoặc move ordering bên dưới. Dự đoán trước, tiết lộ trace, rồi giải thích vì sao phần việc bị bỏ qua không thể đổi đáp án minimax chính xác.","predict":"Nhánh này có bị prune không, hoặc thứ tự nước đi nào sẽ đánh giá ít việc hơn? Nêu bound hoặc lý do thứ tự bạn dự đoán.","observe":"Ghi lại root value/move, số công việc được đánh giá hoặc cutoff đầu tiên, và các giá trị alpha/beta liên quan khi pruning xảy ra.","explain":"Vì sao cutoff an toàn, và vì sao Alpha-Beta vẫn trả về đúng kết quả minimax chính xác?","transfer":"Đổi thứ tự cùng các child có thể đổi lượng công việc tìm kiếm mà không đổi game tree hay quyết định tối ưu như thế nào?"},
   "es":{"summary":"Tarea rápida · QA-MINIMAX-01 · 10–15 min","title":"Misma respuesta, menos búsqueda","intro":"Completa el Guided Challenge de poda u orden de movimientos. Predice primero, revela la traza y justifica por qué el trabajo omitido no puede cambiar la respuesta minimax exacta.","predict":"¿Se podará esta rama o qué orden evaluará menos trabajo? Indica el límite o razón de orden que esperas.","observe":"Registra el valor/movimiento de la raíz, el trabajo evaluado o primer corte y los valores alpha/beta relevantes cuando ocurre la poda.","explain":"¿Por qué es seguro el corte y por qué Alpha-Beta sigue devolviendo el resultado minimax exacto?","transfer":"¿Cómo puede reordenar los mismos hijos cambiar el trabajo de búsqueda sin cambiar el árbol ni la decisión óptima?"}}
 }
}


def registry() -> list[dict]:
    return list(json.loads(REGISTRY.read_text(encoding="utf-8"))["activities"])


def i18n_span(copy: dict[str,str], key: str, tag: str = "span") -> str:
    attrs=' '.join(f'data-qa-{loc}="{html_lib.escape(values, quote=True)}"' for loc,values in ((loc,copy[loc][key]) for loc in ("en","zh","vi","es")))
    return f'<{tag} class="qa-i18n" {attrs}>{html_lib.escape(copy["en"][key])}</{tag}>'


def modern_packet(row: dict) -> str:
    cfg=MODERN[row["id"]]; copy=cfg["copy"]
    fields=''.join(
      f'<label class="qa-modern-field"><strong>{i18n_span(copy,key)}</strong><textarea data-qa-answer="{key}" rows="3" aria-label="{key}"></textarea></label>'
      for key in ("predict","observe","explain","transfer")
    )
    return (
      f'<details class="card quick-assign-modern" id="{row["anchor"]}" data-quick-assign-id="{row["id"]}">'
      f'<summary><strong>{i18n_span(copy,"summary")}</strong></summary>'
      f'<div class="quick-assign-modern-body"><h2>{i18n_span(copy,"title")}</h2><p>{i18n_span(copy,"intro")}</p>'
      '<p class="tiny">Use the existing Guided Challenge immediately below for the run/reveal step. Responses stay in this browser unless you deliberately copy or print them.</p>'
      + fields +
      '<div class="challenge-controls"><button type="button" data-qa-action="copy">Copy responses</button><button type="button" data-qa-action="print">Print / PDF</button><button type="button" data-qa-action="clear">Clear local draft</button></div></div></details>'
    )


def modern_runtime(row: dict) -> str:
    cfg=MODERN[row["id"]]
    return f'''<script data-quick-assign-modern-runtime="1">(()=>{{
const id={json.dumps(row["id"])};const root=document.querySelector('[data-quick-assign-id="'+id+'"]');if(!root)return;
const key='ai-playgrounds-quick-assign:'+id;const loc=()=>{{const x=String(document.documentElement.lang||'en').toLowerCase();return x.startsWith('zh')?'zh':x.startsWith('vi')?'vi':x.startsWith('es')?'es':'en';}};
function paint(){{const l=loc();root.querySelectorAll('.qa-i18n').forEach(el=>{{el.textContent=el.getAttribute('data-qa-'+l)||el.getAttribute('data-qa-en')||'';}});}}
function save(){{try{{const data={{}};root.querySelectorAll('[data-qa-answer]').forEach(el=>data[el.dataset.qaAnswer]=el.value);localStorage.setItem(key,JSON.stringify(data));}}catch(_e){{}}}}
function load(){{try{{const data=JSON.parse(localStorage.getItem(key)||'{{}}');root.querySelectorAll('[data-qa-answer]').forEach(el=>{{if(Object.prototype.hasOwnProperty.call(data,el.dataset.qaAnswer))el.value=data[el.dataset.qaAnswer];}});}}catch(_e){{}}}}
root.addEventListener('input',e=>{{if(e.target&&e.target.matches('[data-qa-answer]'))save();}});
root.querySelector('[data-qa-action="clear"]')?.addEventListener('click',()=>{{root.querySelectorAll('[data-qa-answer]').forEach(el=>el.value='');try{{localStorage.removeItem(key);}}catch(_e){{}}}});
root.querySelector('[data-qa-action="print"]')?.addEventListener('click',()=>window.print());
root.querySelector('[data-qa-action="copy"]')?.addEventListener('click',async()=>{{const text=[...root.querySelectorAll('[data-qa-answer]')].map(el=>el.dataset.qaAnswer.toUpperCase()+': '+el.value).join('\n\n');try{{await navigator.clipboard.writeText(text);}}catch(_e){{}}}});
window.addEventListener({json.dumps(cfg["event"])},()=>setTimeout(paint,0));document.querySelector('#ap-standard-language-select')?.addEventListener('change',()=>setTimeout(paint,0));
load();paint();
}})();</script>'''


def patch_modern(row: dict) -> None:
    path=SITE/'playgrounds'/row['slug']/'index.html'; html=path.read_text(encoding='utf-8'); cfg=MODERN[row['id']]
    marker=cfg['challenge_marker']
    if marker not in html: raise RuntimeError(f"Modern Quick Assign challenge marker missing: {row['id']}")
    if f'data-quick-assign-id="{row["id"]}"' in html: raise RuntimeError(f"Modern Quick Assign duplicate: {row['id']}")
    style='''<style id="v17-modern-quick-assign">.quick-assign-modern{margin:18px 0}.quick-assign-modern summary{cursor:pointer}.quick-assign-modern-body{padding-top:10px}.qa-modern-field{display:block;margin:10px 0}.qa-modern-field textarea{width:100%;box-sizing:border-box;min-height:72px}</style>'''
    if 'id="v17-modern-quick-assign"' not in html: html=html.replace('</head>',style+'</head>',1)
    html=html.replace(marker,modern_packet(row)+marker,1)
    html=html.replace('</body>',modern_runtime(row)+'</body>',1)
    path.write_text(html,encoding='utf-8')


def patch_remaining_original(rows: list[dict]) -> None:
    legacy_qa.ACTIVE_COPY.update(NEW_COPY)
    for row in rows:
        legacy_qa.patch_quick_assign(row)


def patch_support(rows: list[dict]) -> None:
    support.ZH.update(ZH)
    support.patch_teacher(rows)
    support.patch_curriculum(rows)


def validate(rows: list[dict]) -> None:
    if len(rows)!=15 or any(r.get('status')!='active' for r in rows): raise RuntimeError('v1.7 registry must contain 15 active Quick Assigns')
    for row in rows:
        p=SITE/'playgrounds'/row['slug']/'index.html'; html=p.read_text(encoding='utf-8')
        if html.count(f'data-quick-assign-id="{row["id"]}"')!=1: raise RuntimeError(f"Quick Assign must surface exactly once: {row['id']}")
        if f'id="{row["anchor"]}"' not in html: raise RuntimeError(f"Quick Assign anchor missing: {row['id']}")
        if row['slug'] in MODERN_SLUGS:
            for k in ('predict','observe','explain','transfer'):
                if f'data-qa-answer="{k}"' not in html: raise RuntimeError(f"Modern Quick Assign field missing: {row['id']} {k}")
            if 'data-quick-assign-modern-runtime="1"' not in html: raise RuntimeError(f"Modern Quick Assign runtime missing: {row['id']}")
        else:
            for k in ('predict','observe','explain','transfer'):
                if f'data-lab-answer="{k}"' not in html: raise RuntimeError(f"Original Quick Assign field missing: {row['id']} {k}")
    for page in ('teacher-pack.html','curriculum.html'):
        html=(SITE/page).read_text(encoding='utf-8')
        for row in rows:
            href=f'playgrounds/{row["slug"]}/index.html?mode=classroom#{row["anchor"]}'
            if row['id'] not in html or href not in html: raise RuntimeError(f"{page} lacks {row['id']} canonical link")

MODERN_SLUGS={"transformer-language-model","agent-tool-context","minimax-alpha-beta"}


def build_site() -> None:
    base.build_site()
    rows=registry()
    remaining_original=[r for r in rows if r['slug'] not in MODERN_SLUGS and r['id'] not in {'QA-SEARCH-01','QA-LOCAL-01','QA-WUMPUS-01','QA-SAT-01'}]
    patch_remaining_original(remaining_original)
    for row in rows:
        if row['slug'] in MODERN_SLUGS: patch_modern(row)
    patch_support(rows)
    validate(rows)
    base.base.impl.base.validate_local_references()
    print('Built all-lab Quick Assign candidate: 15/15 active; v1.6.2 algorithms and public boundary preserved')

if __name__=='__main__': build_site()
