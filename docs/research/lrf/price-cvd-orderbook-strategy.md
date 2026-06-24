# Price Action + CVD/Delta + Orderbook 第一版战法

Status: current_truth
Updated: 2026-06-24

本文定义 LRF 第一版最小研究战法。它从 `research-thesis.md` 的市场机制假设派生，回答“如何组织研究”，不是实时交易信号。

## 上层 thesis

本战法不自带市场哲学。它接受 `research-thesis.md` 的最高层假设：

```text
市场是拍卖和流动性重新定价过程；短周期机会来自价格位置、主动成交、被动流动性和运动接受/失败之间的相互作用，而不是来自 FVG、OB、liquidity sweep 等名词本身。
```

如果后续工具、worker 或 run 发现这个 thesis 不适用，只能输出 blocker、counterexample 或 docs-change proposal，不能在 active run 中临场改写战法。

## 战法一句话

第一版研究的问题是：

> 当价格出现候选结构动作时，主动成交是否确认或背离该动作；被动流动性是否增强、削弱或反证这个解释。

第一版固定为：

```text
Price Action + CVD/Delta + Orderbook
```

smart-money language 只作为 hypothesis language，不作为自证结论。

换成 ResearchAgents 的执行原则：

```text
structure first
  -> order-flow verifies/refutes
  -> smart-money names hypotheses, not proof
```

## 三层模型

### Layer 0: Price-action base layer

职责：定义价格处在什么结构语境。

这层是地图，不是信号。Worker 必须先说明市场处在高位、低位、range 边界、突破后、扫后收回、冲高失败还是回踩位置，再允许讨论订单流或 smart-money hypothesis。

允许元素：

- range high / range low；
- breakout / breakdown；
- sweep / reclaim；
- displacement；
- acceptance / rejection；
- pullback / retest；
- failed breakout；
- consolidation / compression。

Price action 只回答“价格行为像什么结构”，不回答“是否能交易”。

### Layer 1: Order-flow evidence layer

职责：验证主动成交和被动流动性是否支持价格动作。

这层是现场证据。CVD/delta 代表 aggressive flow，orderbook/book depth 代表 passive liquidity。它们只能支持、反证或降级结构假设，不能直接输出交易结论。

CVD/delta/trades aggression 回答：

- 主动买是否推动上涨；
- 主动卖是否推动下跌；
- 价格和 CVD 是否同步；
- 是否出现 price-CVD divergence；
- 关键 bar/window 附近的 buy/sell/unknown qty；
- volume 是否集中在突破、回踩、失败、扫流动性位置。

Orderbook/book depth/passive liquidity 回答：

- top-N bid/ask depth 是否偏斜；
- spread 是否异常；
- best bid/ask 是否随价格推进而漂移；
- bid/ask depth 是否补出、撤掉或被消耗；
- snapshot count/density 是否足够；
- coverage/truncation 是否允许使用该证据。

Orderbook 初期只能是增强证据、反证证据或 partial evidence。OB 缺失或不稳定不能阻塞整个战法，只能使 passive-liquidity evidence 降级。

### Layer 2: Smart-money structure hypothesis layer

职责：提出可验证叙事，不负责证明叙事。

这层是方法语言/分类框架。FVG、liquidity sweep、displacement、ICT order block candidate 等词只能命名候选 hypothesis。它们不能替代 price-action context 和 order-flow evidence。

第一版保留：

- liquidity sweep candidate；
- sweep reclaim candidate；
- displacement continuation candidate；
- FVG candidate；
- failed breakout / distribution candidate；
- absorption candidate；
- range liquidity context。

第一版暂缓：

- 复杂 ICT order block 确认；
- 多级 FVG 叠加；
- 自动 liquidity map；
- funding/OI 叙事；
- session / killzone 大组合；
- premium/discount 大叙事；
- 任何 stop/target/win/loss/PnL 结论。

## Orderbook 命名边界

`orderbook`、`book_depth`、`passive_liquidity` 指盘口深度和被动流动性。

`ict_order_block_candidate` 指 ICT 结构区候选。

两者不得都缩写成 `OB`。工具、worker 和 reviewer 必须用清楚字段名区分。

## 第一版可用判断

允许输出：

- `hypothesis_supported`
- `hypothesis_contradicted`
- `hypothesis_partial`
- `evidence_insufficient`
- `blocked`

禁止输出：

- `absorption_confirmed`
- `distribution_confirmed`
- `smart_money_action_confirmed`
- `edge`
- `can_trade`
- `Product GO`
- `performance`
- 必涨 / 必跌。

## 典型组合解释

### 主动流确认

- Price：突破、回踩后继续抬高。
- CVD/delta：同步上升。
- Orderbook：ask 被消耗后不明显补，bid 在回踩时不撤。
- 输出：上涨 hypothesis 得到支持，但仍不是交易许可。

### 主动流背离

- Price：价格上涨或高位横住。
- CVD/delta：不涨、走弱或 delta 偏卖。
- Orderbook：上方 ask 反复补，bid 支撑不持续。
- 输出：上涨质量差，假强或派发 hypothesis 增强。

### 吸收假设

- Price：价格跌不动，或扫低后收回。
- CVD/delta：明显负 delta。
- Orderbook：下方 bid 补得住，卖单打进去但价格不破。
- 输出：吸收 hypothesis 增强；必须等待后续价格重新上破或结构收回验证。

### 派发假设

- Price：高位横盘、冲高失败或重心下移。
- CVD/delta：买入很多但价格不涨，或 CVD 走弱。
- Orderbook：上方 ask 压制，bid 被打就撤或变薄。
- 输出：派发 hypothesis 增强；若下沿跌破，反证力度更强。

### 无效区

- Price：横盘无关键位置。
- CVD/delta：杂乱或数据 truncated。
- Orderbook：snapshot density 不足或 partial。
- 输出：`evidence_insufficient`，不能硬编叙事。

## Worker 取证问题

Worker 不应被问“这里会涨吗”。应被问：

- 这个窗口的 price-action context 是什么？
- 主动成交是否支持该价格动作？
- CVD/delta 是否出现 divergence？
- volume 是否集中在关键结构附近？
- orderbook evidence 是 complete、partial、blocked 还是 insufficient？
- passive-liquidity facts 支持、反证还是无法判断该 hypothesis？
- 是否存在 alternative explanation？

Worker 也不应从 FVG、ICT OB、liquidity sweep 这些名词开始找证据。正确顺序必须是：

1. 先定义 price-action context。
2. 再请求 CVD/delta 和 orderbook facts。
3. 最后判断某个 smart-money hypothesis 是否被支持、反证、partial 或 insufficient。

## judgment_trace 最小字段

每个非平凡判断至少记录：

- `blind_task_id`
- `price_action_context`
- `aggressive_flow_state`
- `passive_liquidity_state`
- `smart_money_hypothesis`
- `supporting_facts`
- `contradicting_facts`
- `partial_or_blocked_evidence`
- `alternative_explanations`
- `confidence_label`
- `forbidden_claims_attestation`

没有 deterministic fact refs 的 smart-money 叙事必须降级为 `structure_only_hypothesis` 或 `evidence_insufficient`。
