---
title: "AI 时代的批判性思维与创造力：一套解决问题的方法"
date: 2026-10-27T00:00:00+08:00
tags:
  - "人工智能"
  - "批判性思维"
  - "创造力"
  - "解决问题"
draft: false
article_style: reading-notes
---

生成式 AI 把答案的生产成本降到了前所未有的水平。过去要查资料、写提纲、做比较，如今几分钟就能得到一份结构完整的结果。但答案越容易获得，另一些能力就越稀缺：判断该解决什么问题，分辨什么证据可信，发现已有选项之外的可能，以及为最终选择承担责任。

批判性思维和创造力常被当成两种相反的能力：前者负责挑错，后者负责想象。其实它们服务于同一个目标——解决问题。创造力扩大解空间，批判性思维筛掉站不住的方案；只有发散没有判断，会得到大量新奇但无用的点子；只有判断没有发散，则可能在一个错误的问题里寻找最优答案。

本文综合九本经典著作与近年的 AI 研究，尝试把两种能力整理成一套循环：**定义问题、发散选项、质疑假设、验证方案、更新认识**。

## 1. 答案过剩，判断与创造成为稀缺能力
{{< reading-note-figure src="/images/critical-thinking-and-creativity-in-ai-era/01-answer-abundance.svg" alt="左侧是不断涌出的AI答案卡片，右侧是由人把守的四道关口：问题、证据、价值与责任；中间漏斗说明答案丰富不等于问题已解决" caption="AI 扩大了答案供给，却没有替人决定该问什么、信什么和承担什么。" >}}

AI 可以迅速生成解释、方案、代码和图像，但“生成得更多”不等于“问题解决得更好”。三个研究提供了更细的观察。

2024 年，Anil Doshi 和 Oliver Hauser 让 293 名参与者写短篇故事。获得 GPT-4 构思帮助的作品，平均被读者评为更新颖、实用和易读，原本创造力较弱的人获益更多；与此同时，AI 辅助作品之间的语义相似度也更高。AI 提高了单篇作品的评分，却可能让群体产出趋同。

2025 年，Microsoft Research 与卡内基梅隆大学研究者调查了 319 名知识工作者的 936 个真实使用案例。受访者对 AI 越有信心，自报投入的批判性思考越少；他们的认知劳动也从直接完成任务，转向核验信息、整合结果和监督任务。由于这是横截面的自报告研究，它不能证明 AI 导致思考能力下降，但说明工作重心正在迁移。

同年，一项在土耳其高中开展的随机对照实验发现：学生用 GPT-4 练习数学时表现更好，但撤去工具后的独立考试中，无护栏使用组反而落后于对照组；加入教师设计提示、不给出最终答案的版本，则没有出现这种下降。工具是否替代思考，取决于使用方式。

因此，更准确的判断不是“AI 让人变聪明”或“AI 让人变笨”，而是：

| AI 降低的成本 | 仍需人承担的工作 |
| --- | --- |
| 生成一份答案 | 判断问题是否值得回答 |
| 罗列多个方案 | 判断方案是否真正不同 |
| 补全一段推理 | 检查证据、遗漏与因果跳跃 |
| 模仿成熟表达 | 决定什么有意义、有价值 |
| 快速执行指令 | 承担选择造成的现实后果 |

> **面试提醒**：最近的招聘面试中，我也会有意考察这一点：剥离 AI 的帮助后，候选人能否独立定义问题、推理并作出判断。这往往决定他们如何使用 AI，以及最终能否把事情做成。

> **工作提醒**：不要用“AI 能否完成”判断一项能力是否还重要。生成越便宜，问题定义、证据判断和原创选择越重要。

---

## 2. 先找对问题，而不是急着找答案
{{< reading-note-figure src="/images/critical-thinking-and-creativity-in-ai-era/02-frame-the-problem.svg" alt="一盏不亮的灯被拆成表面症状、问题所有者、真实目标和约束四层，红色批注提醒不要把修灯当成唯一答案" caption="问题不是一句给定条件，而是期望、现实、所有者与约束共同形成的框架。" >}}

Donald Gause 和 Gerald Weinberg 在《你的灯亮着吗？》中反复追问：问题到底是什么？它是谁的问题？如果把一个表面症状直接交给 AI，我们通常只会更快得到一个针对错误问题的完整答案。

“用户需要更多功能”可能真正意味着用户无法发现已有功能；“学生需要更高分”可能掩盖了知识没有迁移到新题型；“团队需要提高效率”也可能是目标冲突、等待审批或优先级频繁变化。问题的表达方式预先限定了答案空间。

### 2.1 用四个问题重新定义问题

面对一个任务，先写下四项：

1. **期望与现实的差距是什么？** 不要只写“哪里不好”，要写希望发生什么、现在发生什么。
2. **这是谁的问题？** 谁感受到损失，谁拥有改变条件的权力，谁承担方案的成本？
3. **真正的目标是什么？** “做一个搜索功能”是方案，“让用户在一分钟内找到资料”才可能是目标。
4. **哪些约束是真的？** 法律、预算和物理条件是硬约束；“以前一直这样做”通常不是。

一个实用技巧是把原问题改写三次。第一次去掉预设方案，第二次换一个利益相关者，第三次把目标提升一层：

- 原问题：怎样让 AI 自动回复更多工单？
- 去掉方案：怎样缩短用户解决问题的时间？
- 更换视角：怎样减少客服处理重复问题的负担？
- 提升目标：怎样让产品本身少制造这些问题？

改写不是文字游戏。每换一个框架，候选方案都会变化：自动回复、知识库、界面修正、流程调整，可能分别对应不同根因。

> **专项提醒**：最近做一个专项时，我也犯过这个错误：随着周期拉长、并行事项增多，最初的目标逐渐模糊。即使开始时来不及想透，也要在推进中及时调整、重新对焦，先确认一个值得达成的目标，再继续投入。

### 2.2 先独立写下问题，再让 AI 参与

如果一开始就让 AI 定义问题，它给出的第一个框架会成为锚点。更稳妥的顺序是：人先写一版问题、目标和约束，再让 AI 提出其他定义，最后比较每种定义会遗漏谁、鼓励什么方案、把什么当成不可改变。

> **问题定义清单**：我们看到的是原因还是症状？如果解决它，谁会受益？谁可能受损？什么证据能证明问题真的存在？如果不能采用当前方案，目标还能怎样实现？

---

## 3. 批判性思维：不是反驳，而是逼近事实
{{< reading-note-figure src="/images/critical-thinking-and-creativity-in-ai-era/03-scout-thinking.svg" alt="侦察兵在地图上标出事实、解释、预测和价值四层信息，旁边的概率刻度随着新证据移动，而不是守住原来的旗帜" caption="批判性思维不是守住立场，而是让自己的地图更接近真实地形。" >}}

Julia Galef 在 *The Scout Mindset* 中区分了两种心态：士兵要保卫阵地，侦察兵要看清地形。批判性思维的目标不是赢得争论，也不是凡事怀疑，而是降低自己被愿望、身份和既有立场误导的概率。

Adam Grant 在 *Think Again* 中给出相似的提醒：人很容易进入布道者、检察官或政客模式——证明自己正确、证明别人错误，或争取他人支持。更有效的是“科学家模式”：把观点当作暂时假设，主动设计可能推翻它的检验。

### 3.1 把一句结论拆成四层

AI 输出之所以容易显得可靠，是因为它常把不同性质的内容写成同一种确定语气。阅读任何结论时，可以把它拆成四层：

| 层次 | 要问的问题 | 例子 |
| --- | --- | --- |
| 事实 | 能否由原始资料直接核验？ | 用户流失率从 8% 升到 11% |
| 解释 | 还有哪些原因能解释同一事实？ | 可能因为价格，也可能因为渠道变化 |
| 预测 | 在什么期限和条件下会发生？ | 调价后一个月流失率将下降 |
| 价值判断 | 谁认为什么更重要？ | 增长是否值得牺牲部分体验 |

事实可以查证，解释需要比较，预测可以结算，价值判断则必须说明立场。把四层混在一起，最容易出现“数据是真的，所以建议一定正确”的跳跃。

### 3.2 主动寻找能改变自己的证据

普通搜索往往是在寻找支持，批判性搜索则要提前写下：**看到什么，我会改变观点？**

可以固定问五个问题：

1. 这个结论依赖哪些假设？
2. 最强的反例是什么？
3. 缺失的数据会不会改变方向？
4. 如果竞争对手提出同样论证，我会接受吗？
5. 我是在评价证据，还是在保护身份和过去的决定？

这并不要求无限质疑。判断有时间成本，关键是让检验强度与后果匹配：可逆、低影响的决定可以快速试；不可逆、影响大的决定需要更强证据和独立复核。

### 3.3 用概率代替“肯定”和“不会”

Philip Tetlock 和 Dan Gardner 在《超预测》中总结了一套可训练的判断习惯：把大问题拆小，先看基准率，再加入个案信息；用概率表达信心，并根据新证据小幅、持续地更新。

例如，不说“这个功能一定受欢迎”，而说“在当前样本和价格下，我估计有 65% 的概率使次周留存提高至少 2 个百分点”。这样的判断有期限、有阈值，可以被验证，也可以在结果出现后检查自己是过度自信还是过度保守。

但预测准确不等于决策正确。《超预测》的证据主要来自可结算的中短期预测；面对价值冲突、极端事件或长期未来，概率只能帮助描述不确定性，不能替人决定什么值得追求。

---

## 4. 创造力：不是灵感，而是扩大解空间
{{< reading-note-figure src="/images/critical-thinking-and-creativity-in-ai-era/04-expand-solution-space.svg" alt="不同领域的素材卡片进入组合台，经过发散、酝酿和原型三段后形成多个不同方案，红色批注指出不要过早评判" caption="创造力来自材料、连接和试验；先扩大解空间，再判断哪个方案值得留下。" >}}

James Webb Young 在 *A Technique for Producing Ideas* 中把创意描述为既有元素的新组合，并把过程分为五步：搜集材料、加工材料、暂时放下、等待想法浮现、把想法带回现实检验。它来自广告实践，不是严格的实验模型，却抓住了一个重要事实：创造并非凭空出现，而是材料、连接、酝酿与修改的结果。

### 4.1 发散前，先增加可连接的材料

David Epstein 在 *Range* 中讨论了广度的价值。在规则模糊、反馈延迟的陌生问题里，多领域经验能提供更多类比和心智模型。广度不是“什么都懂一点就够了”，而是能把其他领域的结构迁移到当前问题。

培养这种能力，可以有意识地做三件事：

- **跨域输入**：每月阅读一个本职领域之外的主题，不追求立即有用。
- **结构类比**：不只问“别人怎么做”，还问“哪些问题有相同结构”。排队、缓存、库存和注意力分配都涉及有限资源与等待。
- **强制变换约束**：如果预算只有十分之一、时间只有一天、用户无法阅读，方案会怎样变化？

*Range* 并不反对专业化。在规则稳定、反馈及时的领域，早期专精通常有效；广度更适合规则不清晰、需要迁移和重新定义问题的环境。

### 4.2 把生成与评判暂时分开

创意讨论最常见的失败，是一个想法刚出现就被“做不了”“用户不会要”“以前试过”终止。批判性思维介入得太早，会把还没长成的方案全部剪掉。

发散阶段可以先设数量目标：至少提出 10 个方案，其中必须包含两个反常识方案、两个跨行业类比和一个“不使用 AI”的方案。到收敛阶段，再用目标、约束、证据和可验证性评分。这里不是禁止批评，而是延迟批评。

Tom Kelley 和 David Kelley 在 *Creative Confidence* 中强调，创造力信心来自行动经验。与其等待完整方案，不如制作低成本原型，让真实反馈替代脑内争论。相关研究总体支持创造力可以训练，但效果有限且研究质量不一，不能把任何一次工作坊都当成能力跃迁。

### 4.3 心流支持投入，但不保证创造

Mihaly Csikszentmihalyi 在《心流》中总结了高度投入的常见条件：目标清晰、反馈及时、挑战与能力大致匹配。这样的环境有助于持续加工、学习和执行。

但心流不等于创造力。重复性工作也能进入心流，而创造性成果还必须新颖且适用。创造过程既需要专注，也需要离开问题后的酝酿；既需要顺畅推进，也需要被反例和现实约束打断。

> **创造力训练**：增加材料，制造远距离连接，延迟评判，快速做出可以被现实否定的东西。灵感只是过程中的一个瞬间。

---

## 5. 把两种能力合成问题解决循环
{{< reading-note-figure src="/images/critical-thinking-and-creativity-in-ai-era/05-problem-solving-loop.svg" alt="定义、发散、质疑、验证、更新五个节点组成循环，黄色路径表示创造力扩大选项，红色路径表示批判性思维筛选和修正" caption="创造力负责打开可能性，批判性思维负责校准方向；验证把两者接回现实。" >}}

批判性思维与创造力不是两支彼此对抗的队伍，而是同一循环里的两种动作：创造力让我们看到更多地图，批判性思维检查地图是否对应地形，实验则让现实给出反馈。

### 5.1 五步循环

| 阶段 | 核心问题 | 主要产物 | 常见失败 |
| --- | --- | --- | --- |
| **定义** | 真正要改变什么？ | 目标、所有者、约束、成功标准 | 把预设方案当问题 |
| **发散** | 还有哪些不同路径？ | 多组机制不同的候选方案 | 只生成同一思路的变体 |
| **质疑** | 什么会证明它不成立？ | 假设、反例、风险、信心水平 | 为喜欢的方案寻找支持 |
| **验证** | 最便宜的有效证据是什么？ | 原型、实验、访谈或可结算预测 | 用更多讨论代替现实反馈 |
| **更新** | 结果改变了什么认识？ | 保留、修改或放弃方案的决定 | 把失败解释成执行问题 |

这个循环不是瀑布流程。验证可能暴露问题定义错误，质疑可能迫使团队重新发散，原型也可能发现新的用户目标。成熟的问题解决能力，不是一次走完五步，而是用最低成本尽快完成一轮，再带着证据进入下一轮。

### 5.2 给每一轮设退出条件

“再想想”会让分析无限延长，“先做了再说”又可能跳过判断。解决办法是为每一阶段设退出条件：

- 定义阶段：团队能否用一句话说清目标，而不夹带方案？
- 发散阶段：候选方案是否至少包含三种不同机制？
- 质疑阶段：是否写出了关键假设和放弃条件？
- 验证阶段：是否获得了比内部意见更接近现实的证据？
- 更新阶段：是否记录了哪项认识发生变化，以及下一轮要验证什么？

退出条件把“感觉想清楚了”变成可以检查的工作成果。

---

## 6. AI 应该进入哪一环
{{< reading-note-figure src="/images/critical-thinking-and-creativity-in-ai-era/06-ai-roles.svg" alt="人在五步循环中央掌握目标、价值和责任，AI分别作为地图绘制者、类比生成器、反方审稿人和实验助手接入不同节点" caption="把 AI 当作思维角色，而不是最终裁判；它可以扩展和挑战，不能替人决定价值。" >}}

AI 最有价值的用法，不是替人完成整个循环，而是在不同阶段扮演不同角色。

### 6.1 四种适合 AI 的角色

1. **地图绘制者**：列出利益相关者、可能的根因和不同的问题定义，帮助发现遗漏。
2. **类比生成器**：从其他行业、学科和历史案例中寻找结构相似的问题，扩大解空间。
3. **反方审稿人**：指出关键假设、最强反例、证据缺口和方案可能失败的条件。
4. **实验助手**：把模糊方案改写成可验证假设，设计低成本原型、评价指标和停止条件。

这些角色都只提供候选内容。AI 不知道组织真正愿意承担什么代价，也不能对引用资料的真实性、实验伦理或决策后果负责。

### 6.2 先想后问，避免被第一个答案锚定

使用 AI 前，先独立写下三行：

- 我认为真正的问题是……
- 我目前倾向的解释或方案是……
- 我最不确定的是……

然后再让 AI 提出不同框架。比较自己的版本与 AI 的版本，比直接接受一份完整答案更能暴露盲点，也保留了形成个人判断的过程。

向 AI 提问时，少问“最好的方案是什么”，多问：

- 在这些目标和约束下，有哪些机制不同的方案？
- 哪些证据支持或反对每个方案？请区分事实与推断。
- 如果当前结论是错的，最可能错在哪里？
- 设计一个一周内能推翻关键假设的最小实验。
- 哪些选择涉及价值判断，不能由证据单独决定？

### 6.3 让证据而不是第二个模型裁决

一个 AI 反驳另一个 AI，并不会自动得到真相。多个模型可能共享相似训练材料、叙事习惯和盲点。关键结论仍要回到原始资料、实际用户、运行数据和可重复实验。

对低风险任务，可以抽样核验；对高风险、不可逆或涉及他人权益的任务，需要独立来源、人工复核和明确责任人。AI 可以帮助准备决策，但不应让“生成得像结论”取代决策过程。

---

## 7. 从个人练习到组织机制
{{< reading-note-figure src="/images/critical-thinking-and-creativity-in-ai-era/07-training-system.svg" alt="学生、知识工作者和管理者三条训练路径汇入同一循环，旁边的团队反馈室强调同侪可以指出问题但不能替创作者做决定" caption="能力来自反复经历完整循环，组织则要让质疑、试验和更新成为默认机制。" >}}

批判性思维和创造力都不能靠记住一组原则获得。它们需要在真实问题中反复使用，并得到反馈。

### 7.1 学生：保留无 AI 的第一次尝试

学生可以先独立完成问题定义、解题思路或文章提纲，再用 AI 比较替代方案、寻找反例，最后关闭 AI 重新表达。重点不是禁止工具，而是避免把“看懂答案”误当成“能够独立迁移”。

每周选一道没有标准答案的问题，保存自己的第一版、AI 的建议、最终版本和修改理由。一个月后回看：哪些修改来自证据，哪些只是因为 AI 表达得更流畅？

### 7.2 知识工作者：维护假设与决策记录

对重要任务，保留一页记录：问题定义、关键假设、当前信心、反证条件、验证方法和结果。复盘时不只问项目成功没有，还要问当时的判断是否校准、哪些信息本可更早获得。

日常训练可以很小：会议前写一个反对自己方案的理由；做选择时给出概率；每周找一个跨领域类比；每月复盘一次被证据改变的观点。目标不是显得更谨慎，而是缩短从错误认识到更新认识的时间。

### 7.3 管理者：保护早期想法，也让问题尽早暴露

Ed Catmull 在 *Creativity, Inc.* 中介绍了 Pixar 的 Braintrust：由可信且专业的同侪坦诚指出作品的问题，但不拥有替创作者作决定的权力。它的价值不在于集体审批，而在于让问题尽早暴露，同时保留负责人的判断与所有权。

这种机制不能简单复制。坦诚需要信任和较低的权力压力；保护未成熟想法也不是无限免责，方案最终仍要面对用户、预算和交付约束。管理者要设计的是一个节奏：早期允许粗糙和分歧，中期引入强反馈，后期用现实标准收敛。

团队还可以建立三项默认规则：

- 重要决策先独立写判断，再讨论，避免职位最高或发言最早的人形成锚点。
- 评审时先复述目标与约束，再评价方案，避免各自解决不同问题。
- AI 生成内容必须标出待核验事实、关键假设和责任人，不能以“AI 建议”作为决策依据。

### 7.4 一页问题解决清单

开始之前：

- 我们要改变的现实是什么？这是谁的问题？
- 目标、硬约束和成功标准分别是什么？
- 当前表述是否偷偷夹带了一个方案？

生成方案时：

- 是否有至少三种机制不同的路径？
- 是否使用了跨领域类比和反常识约束？
- 是否暂时把生成与评价分开？

做出判断时：

- 哪些是事实、解释、预测和价值判断？
- 什么证据会让我改变观点？当前信心是多少？
- 最便宜、最快的有效验证是什么？

完成之后：

- 结果改变了哪项认识？
- 哪些能力被 AI 放大，哪些思考被它替代？
- 下一轮应保留、修改还是放弃什么？

AI 时代真正需要培养的，不是与机器比赛谁能更快给出答案，而是在人和机器都能生成大量答案时，仍能选对问题、打开可能性、接受反证，并让现实不断修正自己。

---

**书籍与研究来源**

**问题定义与批判性思维**

- Donald C. Gause & Gerald M. Weinberg. *Are Your Lights On? How to Figure Out What the Problem Really Is*. Dorset House, 1982. [出版社书目](http://www.dorsethouse.com/books/aylo.html)
- Julia Galef. *The Scout Mindset: Why Some People See Things Clearly and Others Don't*. Portfolio, 2021. [Penguin Random House](https://www.penguinrandomhouse.com/books/555240/the-scout-mindset-by-julia-galef/)
- Adam Grant. *Think Again: The Power of Knowing What You Don't Know*. Viking, 2021. [作者官网](https://adamgrant.net/book/think-again/)
- Philip E. Tetlock & Dan Gardner. *Superforecasting: The Art and Science of Prediction*. Crown, 2015. [Penguin Random House](https://www.penguinrandomhouse.com/books/227815/superforecasting-by-philip-e-tetlock-and-dan-gardner/)
- Mellers, B. et al. (2015). [The Psychology of Intelligence Analysis: Drivers of Prediction Accuracy in World Politics](https://stanford.edu/~knutson/nfc/mellers15.pdf). *Journal of Experimental Psychology: Applied*.

**创造力与组织**

- James Webb Young. *A Technique for Producing Ideas*. 1940. [书籍文本](https://assets.ctfassets.net/lwoaet07hh7w/125v7jpAX4C1Q1Gq41p5Md/2d8867d5528ac9adab5373aed36fb73f/WMR_Producing_Ideas_EBook_v1.pdf)
- Tom Kelley & David Kelley. *Creative Confidence: Unleashing the Creative Potential Within Us All*. Crown Business, 2013. [IDEO 介绍](https://www.ideo.com/journal/creative-confidence)
- David Epstein. *Range: Why Generalists Triumph in a Specialized World*. Riverhead Books, 2019. [作者官网](https://davidepstein.com/range/)
- Mihaly Csikszentmihalyi. *Flow: The Psychology of Optimal Experience*. Harper & Row, 1990. [HarperCollins](https://www.harpercollins.com/products/flow-mihaly-csikszentmihalyi)
- Ed Catmull with Amy Wallace. *Creativity, Inc.: Overcoming the Unseen Forces That Stand in the Way of True Inspiration*. Random House, 2014. [扩展版书目](https://www.penguinrandomhouse.com/books/216369/creativity-inc-the-expanded-edition-by-ed-catmull-with-amy-wallace/)
- Sio, U. N. & Ormerod, T. C. (2009). [Does incubation enhance problem solving? A meta-analytic review](https://research.lancaster-university.uk/en/publications/does-incubation-enhance-problem-solving-a-meta-analytic-review/). *Psychological Bulletin*.
- Sio, U. N. & Lortie-Forgues, H. (2024). [The impact of creativity training on creative performance: A meta-analytic review and critical evaluation of 5 decades of creativity training studies](https://eprints.whiterose.ac.uk/id/eprint/209749/). *Psychological Bulletin*.
- Peifer, C. et al. (2022). [A Scoping Review of Flow Research](https://pmc.ncbi.nlm.nih.gov/articles/PMC9022035/). *Frontiers in Psychology*.

**AI、批判性思维与创造力**

- Doshi, A. R. & Hauser, O. P. (2024). [Generative AI enhances individual creativity but reduces the collective diversity of novel content](https://pmc.ncbi.nlm.nih.gov/articles/PMC11244532/). *Science Advances*.
- Lee, H.-P. et al. (2025). [The Impact of Generative AI on Critical Thinking](https://www.microsoft.com/en-us/research/publication/the-impact-of-generative-ai-on-critical-thinking-self-reported-reductions-in-cognitive-effort-and-confidence-effects-from-a-survey-of-knowledge-workers/). *CHI 2025*.
- Bastani, H. et al. (2025). [Generative AI can harm learning](https://pmc.ncbi.nlm.nih.gov/articles/PMC12232635/). *Proceedings of the National Academy of Sciences*.
