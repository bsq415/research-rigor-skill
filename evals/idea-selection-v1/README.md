# 实证选题行为回归 v1

这个开发集检验选题流程能否支持具体行动。所有案例均为合成质检研究；没有把私有论文、原始评审或真实项目结果发送给答题模型。

| 用例 | 必须观察的行为 |
|---|---|
| I01 | 给出实际、有决策价值且资源可行的临时候选，并设计区分冻结工具与条件内适配的 pilot |
| I02 | 淘汰已被近邻覆盖的创新声明，提出真正未解决、仍需查重的后续问题 |
| I03 | 区分 continue 与测量通过，修复配对、解析和实际干预，保留未定义和受阻状态 |
| I04 | 放弃统一退化预期，保留有效问题、异质证据、版本与有信息价值的下一检验 |
| I05 | 直接核对分歧的侦察、缺失语料和 pilot 原始状态，分开研究者报告、模拟评审与正式原文 |

本次 v1.0.0 输入在模型生成前冻结并随结果包保留；当前[任务](tasks.json)和 [rubric](rubric.json)为后续运行使用的 v1.0.1。每题四项语义评分，合计 20 分；关键错误单列。主要报告逐项分数，完整通过还要求冻结的任务处置标签。I01 的 supported 指临时提案可用，不能解读为新颖性或结果已经证实。

本次执行的是 v1.0.0，其完整输入保留在结果包；当前 v1.0.1 仅修正 I04 的预期处置标签。它问的是能否继续经修订的研究，两组都合理回答 supported，并满足四项科学标准；v1.0.0 却要求 revise，导致其完整通过计数不适合解释为科学质量。没有改旧评分或伪称重跑，见[结果与问题说明](RESULTS.md)。

这次对比的是 **修改前 skill 与修改后 skill**，不是无 skill 对照。旧上下文来自修改前 `4c28423` 的入口、idea-and-literature 和 research-playbooks；新上下文包含修改后的同三份文本及 empirical-idea-discovery。额外文本长度是处理的一部分，未做等 token 对照。

两组共用模型、推理档、输入、输出格式和字数指令；每次用独立临时会话、关闭工具，按冻结顺序交错运行。独立评分上下文隐藏条件标签，但同一模型评分仍只是临时评分，精确引文检查不证明评分正确。每题仅一次、案例公开且为已知机制设计，不能证明跨域科研收益或未来评审认可。

复跑使用结果包里的 baseline-context.txt 或自行冻结旧版本上下文。不会自动读取私有研究目录，不重写旧十题审计基线，不自动重试失败调用：

```text
python evals/run_idea_selection.py prepare <NEW_RUN_DIR> --baseline-context <OLD_CONTEXT_FILE> --model <MODEL> --effort medium
python evals/run_idea_selection.py run <NEW_RUN_DIR>
python evals/run_idea_selection.py blind <NEW_RUN_DIR>
python evals/run_idea_selection.py judge <NEW_RUN_DIR>
python evals/run_idea_selection.py summarize <NEW_RUN_DIR>
python evals/run_idea_selection.py export <NEW_RUN_DIR> --destination <NEW_EXPORT_DIR>
```

运行会消耗当前登录模型额度。新模型、上下文或任务版本应使用新目录。`prepare` 冻结输入、旧/新上下文与执行脚本哈希；发布包保留答案、逐项理由和校验清单，机器事件日志留在本地。

精确重放 v1.0.0 输入时，给 prepare 增加 `--suite-dir evals/results/idea-selection-20261025-v1`；省略该选项则使用当前修正版开发集。输入可重放不代表服务端采样能逐字重现。
