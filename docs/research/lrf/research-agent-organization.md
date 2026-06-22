# LRF 研究智能体组织模型

Status: current_truth
Updated: 2026-06-22

本文定义 LRF 历史研究中各类智能体的职责。核心目标是解决两个问题：

1. worker 不知道该研究哪一段。
2. worker 拿到过多或过少信息后，要么发散评论，要么被暗示答案。

## 不是实时交易团队

本组织模型用于历史研究，不用于实时交易。

- Council 可以看较大的历史范围，但只能提出研究假设和候选窗口。
- Director 可以切片和派任务，但不能把答案塞给 worker。
- Blind worker 只能看到自己的任务边界和 known-at 数据。
- Outcome、win/loss、future path 只属于 freeze 后的 judge / ledger。
- 任何阶段都不得输出 live entry、edge、can-trade 或 Product GO。

## 角色

### Global Research Council

职责：

- 在较大历史范围内观察重复出现的结构现象。
- 提出可能值得研究的 playbook / hypothesis。
- 给出候选窗口和为什么值得验证的低层事实线索。
- 明确可证伪条件和需要哪些数据族验证。

Council 输出的是研究想法，不是交易结论。

最小输出：

```json
{
  "hypothesis_id": "h001",
  "hypothesis_title": "sell-side sweep then reclaim with trade aggression failure",
  "historical_scope": {
    "symbol": "PerpUsdc:ETH-USDC",
    "timeframe": "1h",
    "from": "2026-06-12T16:00:00Z",
    "to": "2026-06-21T00:00:00Z"
  },
  "candidate_windows": [
    {
      "candidate_id": "cand-001",
      "window_start": "2026-06-14T20:30:00Z",
      "window_end": "2026-06-14T22:30:00Z",
      "why_candidate": ["large range expansion", "prior low interaction"]
    }
  ],
  "verification_questions": [
    "Was there a sweep and reclaim known at the decision time?",
    "Did trades show counterparty aggression failure?",
    "Did OI/funding support or contradict the context?"
  ],
  "forbidden_claims": ["edge", "can_trade", "performance", "Product GO"]
}
```

### Research Director

职责：

- 从 Council 的候选中选择具体验证窗口。
- 决定 worker 任务粒度：事件点、短窗口、长窗口、对照窗口或反例窗口。
- 生成 answer-free worker task packet。
- 控制信息隔离：worker 不能看到 Council 想要的结论、future outcome 或其他 worker 的暗示。
- 根据 worker / reviewer 结果安排下一轮：深挖、找反例、扩大样本、修工具或停止。

Director 不直接写市场判断。

### Blind Worker

职责：

- 在 bounded window 内自主请求工具事实。
- 用允许的 rubric 判断结构。
- 输出 `judgment_trace`。
- 明确 counter evidence、missing evidence、confidence 和 recheck condition。

Worker 可以请求更细粒度数据，例如：

- 某 1h bar 的 completed OHLCV facts；
- 某 15 分钟 trades slice；
- 某个 price zone 的 trades facts；
- OI/funding 的低层变化事实。

Worker 不得知道：

- 后续涨跌结果；
- Council 希望它证明什么；
- 哪些样本是“成功图”；
- judge / ledger / performance。

### Falsifier

职责：

- 用同样的 answer-free 边界攻击 hypothesis。
- 找 no-entry、boring、failure、alternative explanation。
- 检查是不是只挑漂亮样本。
- 检查 trades/OI/funding 是否反而削弱假设。

Falsifier 不判断最终赚钱，只判断当前假设是否证据不足或过拟合。

### Reviewer

职责：

- 审 evidence refs 是否存在。
- 审 tool_response 是否真的支持 observed_facts。
- 审 known-at cutoff 是否正确。
- 审 truncated / partial data 是否被误用成 complete evidence。
- 审 worker 是否被 Council/Director 暗示。
- 审是否输出 forbidden claims。

Reviewer 不审市场结果。

### Future Judge / Ledger

职责：

- 只能在 packet、worker output、reviewer audit 冻结后运行。
- 看 outcome、entry、stop、exit、cancel、MAE/MFE、failure/cost/no-entry。
- 产生跨样本统计输入。

Judge / ledger 不解释 smart-money 机制，只执行已定义规则。

## 任务粒度规则

### 不给 worker 全局乱看

全局数据属于 Council / Director。Blind worker 不应该直接拿 8 天、30 天或全市场数据自由发挥。

### 不只给单根 K 线

单根 bar 往往没有足够上下文。默认给 worker 一个 bounded range，例如 30 分钟、2 小时、一个 session 或一个 candidate window。Worker 可在范围内请求单根 bar / trade slice。

### 默认三层粒度

```text
Council: 大范围历史扫描和 hypothesis 生成
Director: candidate window / verification task 切片
Worker: 窗口内 facts 请求和 judgment_trace
```

### 显微镜下钻

Worker 需要更细证据时，通过 tool_request 请求：

- narrower time slice；
- price zone；
- fixed time buckets；
- completed-bar lookup；
- trades adaptive slice；
- OI/funding context slice。

R / broker 只返回 deterministic facts，不补写结论。

## 成功标准

一次组织良好的研究迭代至少应产生：

- hypothesis 或 typed blocker；
- candidate window；
- answer-free worker task；
- tool_requests / tool_responses；
- judgment_trace；
- falsifier 或 reviewer audit；
- next action：继续、找反例、修工具、修 app、扩大样本或停止。

它不需要产生赚钱结论。赚钱结论只能是多轮历史验证之后的候选，不是单轮输出。
