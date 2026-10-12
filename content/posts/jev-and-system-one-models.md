---
title: "别把 System One 模型叫成 Jev"
date: 2026-10-09T00:00:00+08:00
tags:
  - "人工智能"
  - "大模型"
  - "命名"
draft: false
article_style: reading-notes
---

最近在讨论里常听到"我们要接入 Jev"。多数时候，这句话说的并不是它字面上的意思。Jev 是一个具体模型的名字，大家真正想表达的往往是"接入一类模型"。名字用错，看起来只是措辞问题，落到对外沟通、合作关系和能力预期上，就会变成实际问题。

## 1. Jev 是 TypeSafe AI 的模型名
{{< reading-note-figure src="/images/jev-and-system-one-models/01-jev-model-name.svg" alt="模型名片写着 Jev、出品方 TypeSafe AI 和所属类别 System One 模型，红笔更正 JEV 与 Type Safe 两种误写" caption="Jev 是一家公司的一个具体模型，写作 Jev 和 TypeSafe。" >}}

Jev 是 TypeSafe AI 发布的模型。两个写法值得留意：

- 模型名写作 **Jev**，只有首字母大写，不是 JEV。
- 公司名写作 **TypeSafe**，一个词，不是 Type Safe。

TypeSafe 把 Jev 归入它提出的 **System One Models**。官方的定义是："a new class of frontier models built to make fast, structured decisions that software can use directly." 也就是一类新的前沿模型，用来做快速、结构化、可以被软件直接消费的决策。

注意这句定义里的措辞：System One Models 是 "a new class"——一类模型；Jev 是这一类里的一个具体模型。

---

## 2. System One 是一类模型的名字
{{< reading-note-figure src="/images/jev-and-system-one-models/02-class-vs-instance.svg" alt="System One 模型类别的大圈里包含 Jev 和其他团队的同类模型，右侧对比常见 LLM 逐 token 输出字符串与 System One 模型并行输出带概率的结构化值" caption="System One 是类别，Jev 只是其中之一；这一类的特征是并行采样和结构化输出。" >}}

"System One" 这个名字取自卡尼曼《思考，快与慢》里的系统 1 与系统 2（我之前写过一篇[读书笔记](/posts/thinking-fast-and-slow/)）。系统 1 快速、直觉、不费力；系统 2 缓慢、审慎、逐步推理。按这个比喻，常见的大语言模型逐 token 生成，更像系统 2；System One 模型追求的是系统 1 式的"一眼给出判断"。

从官方介绍看，这类模型和常见 LLM 的区别主要在两点：

- **生成方式不同**：LLM 逐个生成 token，每个 token 依赖上一个；System One 模型采用并行采样，一次查询产出全部输出。
- **输出形态不同**：LLM 输出字符串，需要下游再解析；System One 模型直接输出带类型的结构化值，并附带校准过的概率和置信度。

这些是范式层面的特征，并不专属于某一家公司。别的团队完全可以训练、部署具备同样特征的模型——它们可以是 System One 模型，但不是 Jev。

---

## 3. 大厂与创业公司怎么称呼这类模型
{{< reading-note-figure src="/images/jev-and-system-one-models/03-naming-landscape.svg" alt="两列对比：左侧沿用 System One 命名的 TypeSafe、Google、Kev；右侧换用 Decision model / Decisions 命名的 Microsoft、OpenAI、Amazon、Cloudflare、Fastino、Together AI、StartLux" caption="大厂集体绕开 System One，改用更朴素的 Decision model；只有 Google 和沿袭 TypeSafe 契约的开源项目保留 System One 这一说法。" >}}

从 Jev 发布到现在不到一个月，同范式的模型几乎每周都有一款。观察下来，命名出现了两种明显的阵营：

**沿用"System One 模型"的少数**

- **TypeSafe AI** 自己造的词 Jev / System One Models，仍是品类来源。
- **Google DeepMind** 的开源 DiffusionGemma 在官方 Codelabs 里被明写为 "The Discriminative model is a System One model"，是目前唯一跟进这一命名的大厂。
- 开源项目 **Kev**（Jared Palmer）直接声明 API 沿用 TypeSafe 的 System One 契约。

**换用"Decision model / Decisions"的多数**

- **Microsoft Foundry** 10 月 9 日上线 **Microsoft-Decision-1**，官方描述是 "fast decision-making" 和 "decision-scoring model"，发布文中没有出现 System One。
- **OpenAI** 10 月 6 日在 DevDay 上公测 **Decisions API**，底层是 GPT-6 Luna，宣传语是 "Let your app choose the right model, tool, or action in near real-time"，同样绕开了 System One 这一标签。
- **Amazon** 10 月 1 日发布 **Strands Decider 2B**，被 TechCrunch 直接称为"Jev clone"，官方口径是 "AI decision model"。
- **Cloudflare** 10 月 1 日把 **Clef / Clef-Flash** 开源到 Hugging Face，官方博客称之为 "decision models"，引用 Jev 时才提到 System One。
- 创业公司阵营也以 Decision 为主：**Fastino** 的 GLiNER2.5-Decide / GLiDE、**Together AI** 的 Tev1、**Bespoke Labs** 的 Nimble，都用 "decision model" / "open-weight decision model" 的说法。
- 国内目前能查到的开源代表是 **StartLux-Decision**（上海 StartLux，9 月 30 日发布），自我定位是"决策模型"。

两个观察：

- **"System One" 更像 TypeSafe 的品类命名权**。大厂发同类产品时集体避开这个词，改用更朴素的 "decision model"，Microsoft 和 OpenAI 的发布文里甚至不出现 System One。这既避免被动给对手背书，也降低了与卡尼曼术语绑定的解释成本。
- **"Jev" 已经在被用作泛指**。Amazon 的发布被业界直接写成 "Jev clone"，国内外中文媒体多以"类 Jev 模型"/"Jev 的开源替代"概括。这正是上一节担心的地方——越是流通的泛指，越会把具体供应商和品类特征混在一起。

---

## 4. 为什么"接入 Jev"不准确
{{< reading-note-figure src="/images/jev-and-system-one-models/04-four-misreadings.svg" alt="一句“我们接入了 Jev”分别引出合作关系、能力预期、品牌合规、内部沟通四种误读" caption="没有真正调用 TypeSafe 的 Jev 时，这句话会在四个方向上被误读。" >}}

类比一下就清楚了："接入 GPT-5"和"接入大语言模型"是两回事。前者指明了供应商和具体模型，后者只说明了模型类别。

"接入 Jev"同理。只有在真正调用 TypeSafe 提供的 Jev 时，这个说法才准确。如果接入的是其他团队训练或部署的同类模型，继续说"接入 Jev"会带来几类问题：

- **合作关系被误读**：听到"接入 Jev"的人会默认我们和 TypeSafe 有合作，客户、合作方甚至内部其他团队都可能据此做判断。
- **能力预期错位**：Jev 公开的评测结果和特性，不能直接套用到另一个模型上。名字一样，预期就会一样，落差最终由交付方承担。
- **品牌与合规风险**：在对外材料里使用别家公司的模型名描述自己的接入，存在不必要的商标和宣传合规风险。
- **内部沟通含混**：采购、成本结算、技术排障都需要知道"到底接的是谁的模型"，泛化的名字会让这些环节反复确认。

---

## 5. 建议的说法
{{< reading-note-figure src="/images/jev-and-system-one-models/05-naming-decision.svg" alt="判断树：调用 TypeSafe 的 Jev 时说接入 Jev，否则正式场合说接入 System One 模型、口头沟通可说接入类 Jev 模型" caption="先确认接的是谁的模型，再选名字；正式文档优先用类别名。" >}}

按实际情况选择名字：

| 实际情况 | 推荐说法 |
| --- | --- |
| 真正调用 TypeSafe AI 的 Jev | 接入 Jev（TypeSafe AI） |
| 接入同范式的其他模型（正式场合） | 接入 System One 模型（或 Decision 模型） |
| 接入同范式的其他模型（对方熟悉 Jev 时） | 接入类 Jev 模型 |

其中"System One 模型（或 Decision 模型）"描述的是模型类别，适合写进文档、方案和对外材料。两种叫法现阶段并存，下一节专门展开到底该选哪个。"类 Jev 模型"借 Jev 的知名度帮助对方快速理解形态，适合口头沟通，但正式文档里仍建议优先用类别名。

另外两个细节：

- 书写时用 Jev 而不是 JEV，用 TypeSafe 而不是 Type Safe。
- 调用接口时，模型 id 一律照服务方给出的原样填写，不要用"Jev"之类的通用叫法代替。

---

## 6. System One 模型还是 Decision 模型
{{< reading-note-figure src="/images/jev-and-system-one-models/06-which-name.svg" alt="左右两张对照卡：System One 模型优点是继承 TypeSafe 品类命名、绑定卡尼曼比喻、品类讨论稳定，缺点是带供应商暗示、要额外解释、名字不描述能力；Decision 模型优点是大厂通用名、自带语义、更中性，缺点是和决策树决策引擎易混、短期多种变体、失去卡尼曼比喻；底部提示并存期先写一个、括号补另一个" caption="两种叫法各有得失，技术讨论用 System One 模型，对外沟通用 Decision 模型；别再用 Jev 做泛指。" >}}

两种叫法都是一个月内才扩散开的，没必要押宝其中一个。它们各有适用场景。

**System One 模型**

- **优点**：和 TypeSafe 发布 Jev 时提出的概念绑定，一句话就能把这类模型与卡尼曼《思考，快与慢》里的"系统 1"挂钩，解释范式特征时自带隐喻；在学术、品类分析、架构讨论里更稳定。
- **缺点**：承认了 TypeSafe 对品类的命名权，大厂集体避开这个词说明它带有供应商暗示；名字本身不描述模型做什么，对不熟悉卡尼曼的读者需要再解释一遍。

**Decision 模型**

- **优点**：大厂（Microsoft/OpenAI/Amazon/Cloudflare 等）事实上形成的通用名，和产品 API 的叫法保持一致；"决策"两个字自带语义，不认识 Jev 也能大致猜到用途；更中性，不绑定任何一家公司。
- **缺点**：覆盖面太宽，容易和传统规则引擎、决策树、强化学习里的 decision 混淆；行业里短期还没统一叫法，有 Decision model / Decisions API / Decider / Decide 多种变体；失去了与卡尼曼比喻的连接，谈范式特征时得多说一句。

因此我自己的用法分三挡：

- **对外写作、产品沟通、客户介绍**：用"决策模型"或"Decision 模型"，跟进大厂叫法，自带语义，解释成本最低。
- **技术分析、架构讨论、品类/学术对比**：保留"System One 模型"，卡尼曼的隐喻能帮读者快速对齐范式特征。
- **两者并存阶段**：第一次出现时写"决策模型（System One 模型）"或反过来，让读者两种名字都能对上号。

不管用哪个，都不要再用"Jev"做泛指。

---

## 7. 小结
{{< reading-note-figure src="/images/jev-and-system-one-models/07-name-is-a-claim.svg" alt="“接入 Jev”的标签指向“用的是 TypeSafe AI 的模型”这一声明，不是则改用类别名，名字决定合作、预期和成本能否说清" caption="说出模型名就是一次声明，名字准确，后续的事情才说得清。" >}}

Jev 是 TypeSafe AI 的一个模型，System One 是一类模型。说"接入 Jev"，就是在声明我们用的是 TypeSafe 的模型；如果不是，就应该说"接入 System One 模型（或 Decision 模型）"，或者在非正式场合说"接入类 Jev 模型"。名字准确，后面的合作、预期和成本才说得清楚。

---

**事实来源**

- [Introducing System One Models & Jev — TypeSafe AI](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- [Building a Harness with Jev — LangChain](https://www.langchain.com/blog/building-a-harness-with-jev)
- [How System One Models Like Jev Change Enterprise AI Architecture — Kai Waehner](https://www.kai-waehner.de/blog/2026/09/28/how-system-one-models-like-jev-change-enterprise-ai-architecture/)
- [Microsoft-Decision-1: Our model for fast decision-making — Microsoft](https://commandline.microsoft.com/microsoft-decision-1-model-foundry/)
- [Decisions API is now available in Public Beta — OpenAI Community](https://community.openai.com/t/decisions-api-is-now-available-in-public-beta/1403877)
- [Amazon releases its own Jev clone as the AI decision model race turns into a pile-up — Startup Fortune](https://startupfortune.com/amazon-releases-its-own-jev-clone-as-the-ai-decision-model-race-turns-into-a-pile-up/)
- [Clef and Clef-flash: open-source decision models — Cloudflare](https://blog.cloudflare.com/clef-decision-models/)
- [Getting started with Discriminative (Jev / DiffusionGemma) — Google Codelabs](https://codelabs.developers.google.com/codelabs/discriminative-models)
- [Jev, an AI for making quick decisions, has been a viral hit — Fortune](https://fortune.com/2026/10/08/jev-an-ai-for-making-quick-decisions-has-been-a-viral-hit-in-silicon-valley-but-openai-is-hot-on-its-heels/)
- [Jev 被请下王座，StartLux 中国开源决策模型冲上第一 — 36Kr](https://36kr.com/p/4009510615027849)
