# LRF 市场机制假设

Status: current_truth
Updated: 2026-06-24

本文定义 LRF 第一版研究体系的最高层假设。它回答“为什么这些变量值得研究”，不是交易哲学口号，也不是交易许可。

## 一句话 thesis

```text
市场是拍卖和流动性重新定价过程；短周期机会来自价格位置、主动成交、被动流动性和运动接受/失败之间的相互作用，而不是来自 FVG、OB、liquidity sweep 等名词本身。
```

Owner-facing 的短表达是：

```text
结构告诉你去哪看；
订单流告诉你有没有真买卖；
聪明钱告诉你这类机会叫什么。
```

## 研究对象的因果边界

第一版 LRF 研究承认以下机制假设：

- 价格运动是 realized auction path。它显示市场在哪里接受、拒绝、突破、失败、扫流动性或重新定价。
- CVD/delta/trades aggression 是主动成交证据。它只能说明某段窗口里主动买卖是否配合价格运动，不能单独证明未来方向。
- Orderbook/book depth/passive liquidity 是被动流动性证据。它只能说明某段窗口里可见深度、补单、撤单、消耗、spread 和 best bid/ask 漂移状态，不能单独证明吸收或派发。
- Smart-money language 是 hypothesis naming layer。FVG、liquidity sweep、ICT order block candidate、displacement、acceptance/rejection 等词只负责命名可研究叙事，不负责证明叙事。

因此，研究必须先问：

1. 价格在什么结构位置？
2. 主动成交是否支持、背离或削弱该价格动作？
3. 被动流动性是否支持、反证、partial 或 blocked？
4. 这些事实是否足以命名某个 smart-money hypothesis？
5. 反例、boring case、failure case 是否会推翻这个 hypothesis？

## 不允许的反向推理

以下推理方式被禁止：

- 看到 FVG 就寻找所有理由证明 FVG 有效；
- 看到 CVD divergence 就直接写吸收或派发；
- 看到 orderbook 墙就直接写压制、承接、吸收确认；
- 看到一个漂亮 case 就声明 edge、can-trade、performance 或 Product GO；
- 让工具、worker、单次 run 反过来改写 research thesis 或 framework。

如果工具、worker 或 run 发现 thesis / framework 不适用，只能输出 blocker、counterexample 或 docs-change proposal。是否改变 current truth，必须回到 owner/C review 的 docs 层处理。

## 第一版研究取舍

保留：

- price-action location；
- range high / range low；
- sweep / reclaim；
- displacement；
- acceptance / rejection；
- CVD/delta；
- trades aggression；
- volume concentration；
- orderbook low-level passive liquidity；
- minimal smart-money hypothesis language。

暂缓：

- 复杂 ICT order block 确认；
- 多级 FVG 叠加；
- 自动 liquidity map；
- funding/OI；
- session / killzone 大组合；
- 任何 live trading 或 performance 结论。

## 权威位置

本文在 LRF docs 中拥有最高研究语义权威：

```text
research thesis
  -> research framework
  -> skills / rubrics / workflows
  -> tools / deterministic facts
  -> runs / evidence artifacts
```

下层只能实现、验证、阻塞或反证上层；不能在执行中临场改写上层。
