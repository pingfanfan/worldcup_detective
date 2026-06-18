# ⚽ 世界杯 AI 球探 · worldcup detective

一个用 [Kimi Code](https://kimi.com/code) 搭的实验：**每天自动联网分析世界杯，派五个 AI 球探并行会诊，记一本四方对赌账本，并把结果发布成一个网页。**

> 网站（GitHub Pages）：https://pingfanfan.github.io/worldcup_detective/
>
> 世界杯分析仅供娱乐与 AI 能力测评，**不构成任何投注建议**。

## 它是怎么跑的

```
每天 08:00（本地 launchd 定时）
  └─ run.sh
       ├─ Kimi Code 非交互执行 daily-scout.md：
       │    联网核验赛果/赛程 → /swarm 五人会诊 → 更新账本 → 生成当日日报 HTML
       ├─ build_site.py：读账本+历史日报 → 生成 site/ 静态站点
       └─ git push → GitHub Pages 自动发布
```

- **五人会诊（/swarm）**：数据分析师 / 战术分析师 / 伤病观察员 / 舆情嘴替 / 风险官，各自独立联网取证、各写一份分析、各投一票，有分歧会标出来。
- **四方对赌**：我的小分队 vs Opta 超算 vs 抛硬币 vs Kimi 官方，逐场对账记命中率。
- **错题本**：每天把猜错的场次和教训写进 `data/lessons.md`，第二天分析前先读，带记忆地复盘。
- **视觉理解**：把赛程截图丢进去，Kimi 直接读图核验数据。

## 目录

| 路径 | 说明 |
|---|---|
| `daily-scout.md` | 每日任务说明书（喂给 Kimi Code 的指令） |
| `run.sh` | 每日入口脚本（launchd 触发） |
| `build_site.py` | 网站生成器 → `site/` |
| `data/ledger.json` | 四方对赌战绩账本（网站数据源） |
| `data/swarm/` | 五人会诊的当日分析原文 |
| `reports/` | 历次日报 HTML/PNG |
| `site/` | GitHub Pages 发布目录 |

## 自己玩一个

装 [Kimi Code](https://kimi.com/code)（一行命令），把 `daily-scout.md` 改成你想分析的东西，挂个定时任务就行。

---
由 Kimi Code 自动生成与维护。
