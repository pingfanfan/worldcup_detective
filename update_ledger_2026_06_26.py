#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update data/ledger.json for 2026-06-26 daily report."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
ledger_path = ROOT / "data" / "ledger.json"

with ledger_path.open("r", encoding="utf-8") as f:
    data = json.load(f)

# ---------- 1. Add Day 12 matches (Beijing 2026-06-26, US 2026-06-25) as FINISHED ----------
day12 = [
    {
        "date": "2026-06-25",
        "home": "库拉索",
        "away": "科特迪瓦",
        "score": "0-2",
        "group": "E",
        "beijing_time": "06/26 04:00",
        "beijing_date": "2026-06-26",
        "status": "finished",
        "source": "https://www.footballdatabase.eu/en/match/overview/3331510-curacao-cote_d_ivoire",
        "predictions": {
            "my_swarm": {
                "votes": {"数据": "客队胜", "战术": "客队胜", "伤病": "客队胜", "舆情": "客队胜", "风险官": "平"},
                "final": "客队胜",
                "split": True
            },
            "opta": "待确认（Opta/The Analyst 未查到本场单场概率）",
            "kimi_official": "待确认",
            "coin_flip": "平"
        },
        "score_pred": "0-2（四票客队胜；风险官提醒科特迪瓦平局即安全可能保守）",
        "key_players": "Eloy Room（库拉索）；Amad Diallo（科特迪瓦）",
        "recent_form": "库拉索1-7德国、0-0厄瓜多尔；科特迪瓦1-0厄瓜多尔、1-2德国",
        "stay_up_index": 4,
        "one_liner": "加勒比新军背水一战，非洲大象赢球即出线",
        "result_check": {"my_swarm": "hit", "opta": "n/a", "kimi_official": "n/a", "coin_flip": "miss"}
    },
    {
        "date": "2026-06-25",
        "home": "厄瓜多尔",
        "away": "德国",
        "score": "2-1",
        "group": "E",
        "beijing_time": "06/26 04:00",
        "beijing_date": "2026-06-26",
        "status": "finished",
        "source": "https://www.foxsports.com/soccer/fifa-world-cup-men-ecuador-vs-germany-jun-25-2026-game-boxscore-647670",
        "predictions": {
            "my_swarm": {
                "votes": {"数据": "客队胜", "战术": "主队胜", "伤病": "主队胜", "舆情": "主队胜", "风险官": "主队胜"},
                "final": "主队胜",
                "split": True
            },
            "opta": "待确认（Opta/The Analyst 未查到本场单场概率）",
            "kimi_official": "待确认",
            "coin_flip": "客队胜"
        },
        "score_pred": "2-1（四票主队胜；数据跟盘看德国，但战意/轮换警示充分）",
        "key_players": "恩纳·瓦伦西亚、凯塞多（厄瓜多尔）；维尔茨、穆西亚拉（德国）",
        "recent_form": "厄瓜多尔0-1科特迪瓦、0-0库拉索必须胜；德国7-1库拉索、2-1科特迪瓦已出线",
        "stay_up_index": 4,
        "one_liner": "南美背水一战 vs 已出线日耳曼轮换，本轮最大冷门温床",
        "result_check": {"my_swarm": "hit", "opta": "n/a", "kimi_official": "n/a", "coin_flip": "miss"}
    },
    {
        "date": "2026-06-25",
        "home": "日本",
        "away": "瑞典",
        "score": "1-1",
        "group": "F",
        "beijing_time": "06/26 07:00",
        "beijing_date": "2026-06-26",
        "status": "finished",
        "source": "https://www.foxsports.com/soccer/fifa-world-cup-men-japan-vs-sweden-jun-25-2026-game-boxscore-647673",
        "predictions": {
            "my_swarm": {
                "votes": {"数据": "主队胜", "战术": "平", "伤病": "平", "舆情": "平", "风险官": "平"},
                "final": "平",
                "split": True
            },
            "opta": "待确认（Opta/The Analyst 未查到本场单场概率）",
            "kimi_official": "待确认",
            "coin_flip": "主队胜"
        },
        "score_pred": "1-1（四票平局；日本打平即出线，瑞典必须取胜）",
        "key_players": "上田绮世、堂安律（日本）；伊萨克、哲凯赖什（瑞典）",
        "recent_form": "日本4-0突尼斯、2-2荷兰；瑞典5-1突尼斯、1-5荷兰",
        "stay_up_index": 4,
        "one_liner": "蓝武士保平出线，北欧海盗必须强攻",
        "result_check": {"my_swarm": "hit", "opta": "n/a", "kimi_official": "n/a", "coin_flip": "miss"}
    },
    {
        "date": "2026-06-25",
        "home": "突尼斯",
        "away": "荷兰",
        "score": "1-3",
        "group": "F",
        "beijing_time": "06/26 07:00",
        "beijing_date": "2026-06-26",
        "status": "finished",
        "source": "https://www.foxsports.com/soccer/fifa-world-cup-men-tunisia-vs-netherlands-jun-25-2026-game-boxscore-647672",
        "predictions": {
            "my_swarm": {
                "votes": {"数据": "客队胜", "战术": "客队胜", "伤病": "客队胜", "舆情": "客队胜", "风险官": "平"},
                "final": "客队胜",
                "split": True
            },
            "opta": "待确认（Opta/The Analyst 未查到本场单场概率）",
            "kimi_official": "待确认",
            "coin_flip": "客队胜"
        },
        "score_pred": "1-3（四票客队胜；荷兰争小组第一，突尼斯已出局）",
        "key_players": "汉尼拔·梅布里（突尼斯）；加克波、德佩（荷兰）",
        "recent_form": "突尼斯1-5瑞典、0-4日本已出局；荷兰2-2日本、5-1瑞典",
        "stay_up_index": 3,
        "one_liner": "荷兰深盘争头名，突尼斯荣誉战能否避免三连败",
        "result_check": {"my_swarm": "hit", "opta": "n/a", "kimi_official": "n/a", "coin_flip": "hit"}
    },
    {
        "date": "2026-06-25",
        "home": "巴拉圭",
        "away": "澳大利亚",
        "score": "0-0",
        "group": "D",
        "beijing_time": "06/26 10:00",
        "beijing_date": "2026-06-26",
        "status": "finished",
        "source": "https://www.foxsports.com/soccer/fifa-world-cup-men-paraguay-vs-australia-jun-25-2026-game-boxscore-647675",
        "predictions": {
            "my_swarm": {
                "votes": {"数据": "平", "战术": "平", "伤病": "平", "舆情": "平", "风险官": "主队胜"},
                "final": "平",
                "split": True
            },
            "opta": "待确认（Opta/The Analyst 未查到本场单场概率）",
            "kimi_official": "待确认",
            "coin_flip": "主队胜"
        },
        "score_pred": "0-0（四票平局；澳大利亚守平即出线，巴拉圭缺阿尔米隆）",
        "key_players": "恩西索（巴拉圭）；马修·瑞恩、苏塔尔（澳大利亚）",
        "recent_form": "巴拉圭1-4美国、1-0土耳其必须胜；澳大利亚2-0土耳其、0-2美国",
        "stay_up_index": 2,
        "one_liner": "袋鼠打平即出线，巴拉圭为南美荣誉背水一战",
        "result_check": {"my_swarm": "hit", "opta": "n/a", "kimi_official": "n/a", "coin_flip": "miss"}
    },
    {
        "date": "2026-06-25",
        "home": "土耳其",
        "away": "美国",
        "score": "3-2",
        "group": "D",
        "beijing_time": "06/26 10:00",
        "beijing_date": "2026-06-26",
        "status": "finished",
        "source": "https://www.foxsports.com/soccer/fifa-world-cup-men-turkey-vs-united-states-jun-25-2026-game-boxscore-647674",
        "predictions": {
            "my_swarm": {
                "votes": {"数据": "客队胜", "战术": "主队胜", "伤病": "主队胜", "舆情": "主队胜", "风险官": "主队胜"},
                "final": "主队胜",
                "split": True
            },
            "opta": "待确认（Opta/The Analyst 未查到本场单场概率）",
            "kimi_official": "待确认",
            "coin_flip": "平"
        },
        "score_pred": "2-1（四票主队胜；美国已出线轮换，土耳其荣誉战全力）",
        "key_players": "居莱尔、恰尔汗奥卢（土耳其）；巴洛贡、雷纳（美国）",
        "recent_form": "土耳其0-2澳大利亚、0-1巴拉圭已出局；美国4-1巴拉圭、2-0澳大利亚已出线",
        "stay_up_index": 1,
        "one_liner": "星条旗轮换练兵，星月军团荣誉战全力一搏",
        "result_check": {"my_swarm": "hit", "opta": "n/a", "kimi_official": "n/a", "coin_flip": "miss"}
    }
]

existing_keys = {(m["home"], m["away"], m.get("beijing_date")) for m in data["matches"]}
for d in day12:
    if (d["home"], d["away"], d["beijing_date"]) not in existing_keys:
        data["matches"].append(d)
        print(f"added: {d['home']} vs {d['away']}")
    else:
        print(f"already exists: {d['home']} vs {d['away']}")

# ---------- 2. Recompute tally from all result_check entries ----------
tally = {
    "my_swarm": {"hit": 0, "miss": 0},
    "kimi_official": {"hit": 0, "miss": 0},
    "opta": {"hit": 0, "miss": 0},
    "coin_flip": {"hit": 0, "miss": 0},
}

for m in data["matches"]:
    rc = m.get("result_check", {})
    for key in tally:
        val = rc.get(key)
        if val == "hit":
            tally[key]["hit"] += 1
        elif val == "miss":
            tally[key]["miss"] += 1

data["tally"] = tally

# ---------- 3. Update token_account daily_pick ----------
# Pick Netherlands (highest confidence clear win) for 2026-06-26
data["token_account"]["daily_pick"] = {
    "date": "2026-06-26",
    "match": "突尼斯 vs 荷兰",
    "team": "荷兰",
    "status": "hit"
}
data["token_account"]["supported_team_history"].append({
    "date": "2026-06-26",
    "match": "突尼斯 vs 荷兰",
    "team": "荷兰",
    "status": "hit"
})

with ledger_path.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("ledger updated")
print(json.dumps(data["tally"], ensure_ascii=False, indent=2))
