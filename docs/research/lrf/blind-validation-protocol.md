# LRF Blind Validation Protocol

Status: current_truth
Updated: 2026-06-22

本文定义 LRF 历史研究中的盲测、信息隔离、freeze、reviewer 和 post-reveal 顺序。

## 目标

防止 R 或 subagent 事后看答案写故事。每个 hypothesis 必须先在 answer-free known-at 环境中形成判断 trace，再冻结，再由后续 judge / ledger 看 outcome。

## 标准顺序

```text
source binding / source manifest
  -> Global Research Council hypothesis draft
  -> Director task packet
  -> answer-free runtime contract
  -> worker tool requests and judgment traces
  -> falsifier / negative sample challenge
  -> reviewer discipline audit
  -> freeze
  -> deterministic judge / evaluator reveal
  -> post-reveal comparison
  -> failure / cost / no-entry ledger
  -> cross-case research summary
```

不得跳过 freeze 边界。

## Answer-free 不是不给数据

Answer-free 的意思是不给答案，不是不给历史数据。

允许给 worker：

- bounded historical window；
- app-owned source refs；
- allowed tool registry；
- allowed rubric registry；
- known-at policy；
- missing data family notes；
- source hashes；
- candidate task objective。

禁止给 worker：

- future path；
- outcome；
- success/failure label；
- judge result；
- performance；
- edge / can-trade；
- Council 对该窗口的倾向性结论；
- 其他 worker 的判断结果。

## Council 与 worker 的隔离

Council 可以讨论“哪些方法可能赚钱”，但必须把输出降级为可证伪 hypothesis 和 verification tasks。Blind worker 只能看到清洗后的任务包。

错误做法：

```text
Council: 这里很可能是成功的 sell-side sweep long。
Worker: 请证明这里是成功 long。
```

正确做法：

```text
Director task:
  判断 2026-06-14T20:30Z 到 22:30Z 是否存在
  sell-side sweep -> reclaim -> displacement 的结构条件。
  只使用 cutoff 前 facts。
  输出支持、反证、缺失证据和 confidence。
```

## Worker 分工

### Hypothesis / structure worker

- 请求 facts；
- 判断结构；
- 输出 `judgment_trace`；
- 可在证据足够时形成 trade hypothesis fields；
- 不看 outcome。

### Falsifier worker

- 找反证；
- 找 no-entry / boring / failure；
- 检查规则是否过宽；
- 检查数据族是否反向支持。

### Reviewer worker

- 审 blind discipline；
- 审 refs、cutoff、partial/truncated；
- 审 overclaim；
- 审 Council/Director 是否暗示。

Reviewer 不是 deterministic judge。

## Judge / evaluator

Judge / evaluator 只能在 freeze 后运行。它可以回答：

- entry 是否触发；
- stop / exit / cancel / timeout 是否发生；
- MAE / MFE / cost；
- no-entry 是否成立；
- failure reason。

Judge 不回答：

- 是否可以实盘交易；
- 是否已经有 edge；
- 是否 Product GO；
- 是否 live-ready。

## Post-reveal comparison

Post-reveal comparison 只能用于诊断：

- hypothesis 哪些条件有用；
- falsifier 是否抓住真实失败点；
- reviewer 是否漏掉纪律问题；
- ledger 是否完整；
- 下一轮该修 tool、rubric、Director 切片，还是放弃 hypothesis。

它不能把单次结果升级为赚钱结论。
