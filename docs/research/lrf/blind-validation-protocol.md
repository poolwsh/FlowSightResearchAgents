# LRF Blind Validation Protocol

Status: current_truth
Updated: 2026-06-20

本文定义 LRF 的盲测、冻结、裁判和 post-reveal comparison 顺序。

## 目标

防止 R 或 subagent 事后看答案写故事。每个 hypothesis 必须先在 answer-free known-at packet 上写出，再冻结，再由独立 judge / evaluator 判定。

## 标准顺序

```text
Client Mirror First
  -> answer-free packet construction
  -> packet freeze
  -> blind hypothesis subagent
  -> blind adversarial subagent
  -> reviewer discipline audit
  -> A/B/Reviewer freeze
  -> deterministic judge / evaluator reveal
  -> post-reveal comparison
  -> failure/cost/no-entry ledger
  -> cross-case research summary
```

不能跳过 freeze 边界。

## 盲包要求

answer-free packet 只能包含 known-at 信息：

- app readback refs；
- projection generation；
- bounded time window；
- key zone / range / sweep candidates；
- entry / stop / exit 字段；
- data family status；
- missing evidence；
- source hashes。

盲包不得包含：

- 后续走势；
- outcome；
- reveal；
- 成功/失败标签；
- judge result；
- post-reveal comparison；
- performance。

## Subagent 分工

### Hypothesis subagent

任务：

- 写 LRF trade hypothesis；
- 定义 entry / invalidation / stop / exit / cancel / no-entry；
- 明确 observed fact 和 hypothesis；
- 标 missing evidence。

### Adversarial subagent

任务：

- 攻击 hypothesis；
- 指出 fake breakout、overclaim、缺数据、成本和 no-entry 风险；
- 不看 reveal；
- 不判结果。

### Reviewer subagent

任务：

- 审 A/B 是否遵守盲测纪律；
- 审 refs 是否来自 packet；
- 审是否有 answer leakage；
- 审是否 overclaim。

Reviewer 不负责市场结果判定。它不是 deterministic judge。

## Judge / evaluator

Judge 优先用 deterministic tool / evaluator。

Judge 只在 packet 和 A/B/Reviewer 输出冻结后运行。

Judge 判定：

- 是否触发 entry；
- 是否 no-entry；
- 是否 stop；
- 是否 exit；
- 是否 cancel；
- 是否 timeout；
- MAE / MFE / cost；
- judge reason。

Judge 不解释 smart-money 机制，只执行已定义规则。

## Post-reveal comparison

post-reveal comparison 只能回答：

- hypothesis 的哪些部分被数据支持、部分支持或不支持；
- adversarial critique 是否指出了真实失败点；
- Reviewer 是否漏掉 overclaim；
- ledger 是否完整；
- 下一轮 packet / tool / protocol 应修什么。

不能回答：

- 是否可以交易；
- 是否有 edge；
- 是否 Product GO；
- 是否 live-ready。
