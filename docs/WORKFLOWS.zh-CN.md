# 新版科研工作流

这一版保留完整科研能力，把默认执行方式改为“给清楚目标和完成条件，按需取用细节”。
模型负责实施选择；科学主张仍须证据支持。入口是
[research-rigor](../skills/research-rigor/SKILL.md)，完整程序在
[research-playbooks](../skills/research-rigor/references/research-playbooks.md)。

## 三条路径

默认记录只有三件套：`python <SKILL_DIR>/scripts/init_research_project.py <project>`。
需要完整控制器时用 `--upgrade` 补齐，保留旧文件；`--mode full-cycle` 可直接建立完整新项目。
引用与数字工具见[论文检查](../skills/research-rigor/references/manuscript-checks.md)，
plugin 安装和封存保护见[宿主设置](CLAUDE_PLUGIN.md)，变更验证见[评测基线](../evals/README.md)。

| 情境 | 可复制的过程 | 决定性检查 |
|---|---|---|
| 集中的方法论文 | 问题与模型一致 → 确认真实增量 → 理论条件与机制 → 公平实验 → 有效边界 → 成稿 → 逐点返修 → 终稿 | 图、公式、代码和基线是否描述同一系统；收益究竟由什么产生 |
| 从零开始的实证论文 | 候选淘汰 → 最近工作反证 → 完整 pilot → 冻结比较 → 覆盖率审计 → 根据证据修改故事 → 成稿与审稿整改 | 生成结果能否一路到有效统计量；实验是否真的施加了预期干预 |
| 理论稿拒稿后重建 | 原文拆解 → 正确性修复 → 创新重新判断 → 一个核心问题 → 独立证据与实际价值 → 决定投稿 | 正确性、创新性、实际价值分别成立，不能互相替代 |

某个项目接收不代表流程每步都正确，也不保证复制后接收。第一轮通过与最终接收不同。
模型预审、正式审稿、编辑决定和作者自己的复盘分别记录。

## 怎样从两篇文献得到一个 idea

按需读取[从文献到 idea](../skills/research-rigor/references/literature-to-idea.md)。
一篇提供新问题、可控机制与瓶颈；另一篇提供可迁移的消元、分解、不变量或优化结构。
先建立公式与物理对象的对应，再推导“易解块消去后还剩什么”，提出具体候选。
接着检查新增变量破坏了哪些条件，把这个障碍转成可验证的贡献。

输出要说明“各自给了什么 → 在哪一步连接 → 哪些是严格推导/近似/代理 →
朴素迁移缺什么 → 最小验证与最近工作”。区分最初灵感和终稿后来补齐的条件、
算法与证据；也区分用户讲述的灵感、文献表中的引用与分析者的合理重建。

```text
用 research-rigor 分析这些论文怎样启发一个具体研究问题。
提取问题来源和方法来源，给出公式对应、可消去的变量与剩余设计变量。
先提出可实施候选，再找迁移障碍、最近竞争方案和最小否证实验。
标清严格等价、条件、下界、近似与代理，不要只罗列风险或泛称“方法加场景”。
```

可在已有笔记中使用[idea 卡](../skills/research-rigor/assets/idea-transfer-card.md)，
不新增强制 Gate，不因一次构思创建整套项目。合成检查题见
[行为检查案例](../evals/literature-to-idea-cases.md)；它们尚未构成模型效果评测。

## 怎样撰写与优化 RP

撰写或优化研究计划时，先读[RP 工作流](../skills/research-rigor/references/research-proposals.md)。
允许推翻重写时，比较真正不同的候选问题；要求保留框架时，在既定方向、RQ 与章节约束内
纠正错误论证并补强方法。两种方式都要交付实际改稿，不能停在批评或计划。

从“实际需求 → 可核查失败 → 机理 → 最近工作 → 剩余问题 → 决定性检验”建立主线，
再接到工作包、资源、个人能力和时间表。文献默认先获取本地原文，区分元数据、摘要、
部分章节和全文阅读；明确要求全读时，不得为了省工作量改成摘要筛选。发现旧文献反例后，
同时重查摘要、对比表、假设、方法和预期贡献，不能只把一句“首次”改得更绕。

```text
用 research-rigor 优化这份 RP，保留原方向、现有 RQ 和章节结构。
先核查最近工作的原文，建立 gap—RQ—方法—证据—里程碑的联系。
检查实际可用信息、约束、预算公平、保证类型和部署成本。
交付修改稿、修改说明与未完成的原文阅读/验证项，不把计划写成已完成成果。
```

需要记录时用[RP 证据映射表](../skills/research-rigor/assets/proposal-evidence-map.md)，
已有记录足够就不另建。检查编译和逐页版式，但不要把编译通过当作科学有效。
另有[合成行为检查题](../evals/research-proposal-cases.md)，未将其声称为已执行的效果评测。

## 审稿人的问题如何转成行动

保留原意见和稿件版本，记录“表面要求 → 背后的有效性风险 → 独立核实 → 决定性证据
→ 正文改动 → 回复锚点 → 剩余限制”。编辑意见可能重复审稿意见，但不能因重复漏掉回复。

例如，要求更多迭代往往是在问计算预算是否公平；要求其他工况可能是在找被耦合参数
掩盖的失效条件；质疑公式可能实际针对摘要越界；“文章太散”可能表明没有一个决定性贡献。
改文字不能代替缺失的证据，增加实验数量也不能代替正确的实验设计。

理论专项检查在[theory-and-claim-audit](../skills/research-rigor/references/theory-and-claim-audit.md)：
支撑/退化情形、混合项与极限、矩阵变换适用范围、上界与双边阶数、代理与目标指标、
局部解与全局界、同模型自验证、稀有事件分辨率、统计获取成本。

## 保留的工具

| 能力 | 工具或记录 |
|---|---|
| 初始化与只补缺失文件 | `init_research_project.py`、`--merge` |
| 持续执行、恢复、证据门、回滚、重开依赖阶段 | `research_cycle.py`、`audit_research_state.py` |
| 文献充分性与最近工作 | `02_NOVELTY_ASSESSMENT.json`、文献账本、最近工作矩阵 |
| 实验矩阵、失败与重设计、统计分母 | experiment/evidence 协议及现有 CSV 模板 |
| 理论合同与全文主张 | theorem contract、paper claim map、manuscript audit |
| 回复信、修改说明、cover letter、漏答检查 | `audit_revision_package.py` 及原有模板 |
| 最终尺寸图表、坐标轴、字体、清稿与标记稿 | figures/layout 与 paper/submission 协议 |
| 外部 AI 预审 | 原稿 hash、原始 review、授权记录与整改闭环 |
| 文件密封与复核 | `seal_artifacts.py` |
| 通用发布前的隐私检查 | `scan_release.py` 与私有 denylist |

## 如何调用

Codex 使用 `$research-rigor`；Claude Code 使用 `/research-rigor`。

整篇推进示例：

```text
在已给出的数据、算力和预算内，把这个研究问题推进到可核验的论文草稿。
先挑战创新性，再跑通最脆弱的实验链；执行和核验完成后写稿。
保留相反结果，明确哪些是探索发现，哪些有独立确认。
沿用已有授权；缺少会改变下一步的决定才问，其他工作继续。
```

返修示例：

```text
对照原投稿版本和完整审稿意见，核实每条批评；执行已授权的补充分析或实验。
同步修改正文、回复、图表和主张对应表，完成可核查的本地返修包。
不要把摘要式记忆当成原始评审，也不要把润色写成新增证据。
```

## 配额与旧项目兼容

新项目默认 `coverage`，不强制凑论文数量。G2 仍检查已核查全文的来源、原文锚点、
最近工作对照、检索充分性和决策理由，并区分独立审查与同一 agent 的原文复核。
这些结构检查不能证明新颖性。

有明确数量要求时仍可设置：

```text
python skills/research-rigor/scripts/init_research_project.py <project> --literature-policy quota --deep-read-min 300 --forensic-neighbor-min 30 --independent-audit-fraction 0.1
```

这些数字是可选示例，不是通用科研标准。旧 state 没有 `mode` 时继续按原配额检查；
`--merge` 保留现有 state。需要迁移时记录原因，不得在结果不利后静默降低门槛。
新项目的 `claim_policy.headline_max` 为 `null`；旧项目未设置该字段时保留原上限。

GPT-6 Astra 与 Opus 5.5 使用同一套科学合同，保留用户已选的模型与工具。
模型适配关注清楚的完成条件和少而有效的约束，不强制最大推理档、不杜撰模型 ID，
也不把 CLI 安装通过说成两种模型均经过研究效果验证。
