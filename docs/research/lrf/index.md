# LRF 当前研究入口

Status: current_truth
Updated: 2026-06-20

LRF 当前不是泛泛的 horizontal breakout 研究，也不是单独研究某一个
liquidity、OB 或 FVG 标签是否有效。

当前 accepted framing 是：

> 在关键 liquidity / OB / FVG / 失守区附近，研究价格通过盘整、扎针、扫流动性、
> 假突破和订单流变化完成方向选择的过程，并判断哪些 known-at 迹象能区分真接受与假突破。

## 入口文档

- `research-object.md`：LRF 当前研究对象、因果链和可证伪字段。
- `analysis-workflow.md`：R 面对 owner UI 图表或同一组 app 数据时必须执行的分析顺序。
- `method-stack.md`：docs / workflow / skills / tools 的分工。
- `blocker-taxonomy.md`：研究过程中的 blocker 分类。

## 核心收敛

liquidity、OB、FVG、失守区是研究场景或战场位置。
盘整、扎针、sweep、fake breakout、accept/reject 才是当前 LRF 要研究的再定价过程。

研究问题不是“突破后能不能追”，而是：

- 价格为什么来到这个关键区域？
- 到达后是否发生足够长的盘整或重新定价？
- 盘整内部是否有上沿 / 下沿 sweep、扎针、假突破和回收？
- orderflow / OI / FR / orderbook 是否支持吸收、清算、诱导或重新接受的解释？
- 最后一次 breakout 和前面的 fake breakout 在发生前有什么 known-at 差异？

## 探索S暴露的教训

探索S 对同一类图表的后半段分析有可吸收价值，但过程暴露出 R 的默认行为缺口：

- 不应先临场找局部机会，再让 owner 提醒前因。
- 不应等 owner 提醒才看暴跌、失守区、横盘原因和状态切换点。
- 不应只写漂亮成功机会，必须同时记录假突破、止损、成本和 no-entry。
- 不应把 `06/15 10:50/10:54` 这类状态切换点当作普通突破 K 线一笔带过。

因此，R 的默认职责不是“owner 指哪儿就解释哪儿”，而是主动把 owner 指向的图表现象放回 LRF 因果链：

```text
关键区来源
  -> 回到关键区
  -> 区域内盘整 / 扎针 / sweep
  -> fake breakout 和失败成本
  -> 状态切换候选
  -> known-at 数据验证
```

## 非目标

当前 docs 不证明：

- 该战法有效。
- 可以交易。
- 存在 edge。
- 可以进入 Product GO。
- 可以跳过 failure / cost / no-entry 样本。

