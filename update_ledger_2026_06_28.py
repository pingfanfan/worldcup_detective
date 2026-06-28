#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update data/ledger.json for 2026-06-28 daily report."""
import json
import random
from pathlib import Path

ROOT = Path(__file__).parent
ledger_path = ROOT / "data" / "ledger.json"

with ledger_path.open("r", encoding="utf-8") as f:
    data = json.load(f)

# Deterministic coin flip
random.seed("2026-06-28-coin-flip")

def coin_flip():
    return random.choice(["主队胜", "平", "客队胜"])

# ---------- Add Day 14 matches (Beijing 2026-06-28, US 2026-06-27) as FINISHED ----------
day14 = [
    {
        "date": "2026-06-27",
        "home": "巴拿马",
        "away": "英格兰",
        "score": "0-2",
        "group": "L",
        "beijing_time": "06/28 05:00",
        "beijing_date": "2026-06-28",
        "status": "finished",
        "source": "https://www.espn.com/soccer/match/_/gameId/760485/england-panama",
        "predictions": {
            "my_swarm": {
                "votes": {"数据": "客队胜", "战术": "客队胜", "伤病": "客队胜", "舆情": "客队胜", "风险官": "平"},
                "final": "客队胜",
                "split": True
            },
            "opta": "待确认（Opta/The Analyst 未查到本场单场概率）",
            "kimi_official": "待确认",
            "coin_flip": coin_flip()
        },
        "score_pred": "0-2（四票客队胜；英格兰实力碾压，但轮换与破密集效率存疑，风险官看平）",
        "key_players": "贝林厄姆、凯恩（英格兰）；卡拉斯基利亚（巴拿马伤疑）",
        "recent_form": "巴拿马两战皆负0进球；英格兰4分领跑L组，上轮0-0加纳",
        "stay_up_index": 5,
        "one_liner": "2018年6-1往事重演？英格兰轮换后能否锁定L组头名",
        "result_check": {"my_swarm": "hit", "opta": "n/a", "kimi_official": "n/a", "coin_flip": "n/a"}
    },
    {
        "date": "2026-06-27",
        "home": "克罗地亚",
        "away": "加纳",
        "score": "2-1",
        "group": "L",
        "beijing_time": "06/28 05:00",
        "beijing_date": "2026-06-28",
        "status": "finished",
        "source": "https://www.espn.com/soccer/match/_/gameId/760480/ghana-croatia",
        "predictions": {
            "my_swarm": {
                "votes": {"数据": "主队胜", "战术": "平", "伤病": "主队胜", "舆情": "主队胜", "风险官": "平"},
                "final": "主队胜",
                "split": True
            },
            "opta": "待确认（Opta/The Analyst 未查到本场单场概率）",
            "kimi_official": "待确认",
            "coin_flip": coin_flip()
        },
        "score_pred": "2-1（三票主队胜；克罗地亚必须取胜，加纳打平即可，风险官/战术看闷平）",
        "key_players": "莫德里奇、佩里西奇、弗拉希奇（克罗地亚）；帕尔特伊、伊尼亚基·威廉姆斯（加纳）",
        "recent_form": "克罗地亚1-0巴拿马、2-4英格兰；加纳1-0巴拿马、0-0英格兰",
        "stay_up_index": 5,
        "one_liner": "格子军团生死战：老江湖经验 vs 黑星低位反击",
        "result_check": {"my_swarm": "hit", "opta": "n/a", "kimi_official": "n/a", "coin_flip": "n/a"}
    },
    {
        "date": "2026-06-27",
        "home": "哥伦比亚",
        "away": "葡萄牙",
        "score": "0-0",
        "group": "K",
        "beijing_time": "06/28 07:30",
        "beijing_date": "2026-06-28",
        "status": "finished",
        "source": "https://www.foxsports.com/soccer/fifa-world-cup-men-colombia-vs-portugal-jun-27-2026-game-boxscore-647684",
        "predictions": {
            "my_swarm": {
                "votes": {"数据": "客队胜", "战术": "平", "伤病": "平", "舆情": "平", "风险官": "平"},
                "final": "平",
                "split": True
            },
            "opta": "待确认（Opta/The Analyst 未查到本场单场概率）",
            "kimi_official": "待确认",
            "coin_flip": coin_flip()
        },
        "score_pred": "0-0（三票平局；哥伦比亚打平即锁头名，葡萄牙破密集乏力，数据端跟盘看客胜）",
        "key_players": "J罗、路易斯·迪亚斯（哥伦比亚）；C罗、B费（葡萄牙）",
        "recent_form": "哥伦比亚两连胜且零封；葡萄牙1-1刚果金、5-0乌兹别克",
        "stay_up_index": 4,
        "one_liner": "K组头名之争：哥伦比亚低位守平，葡萄牙轮换后攻坚再哑火",
        "result_check": {"my_swarm": "hit", "opta": "n/a", "kimi_official": "n/a", "coin_flip": "n/a"}
    },
    {
        "date": "2026-06-27",
        "home": "刚果（金）",
        "away": "乌兹别克斯坦",
        "score": "3-1",
        "group": "K",
        "beijing_time": "06/28 07:30",
        "beijing_date": "2026-06-28",
        "status": "finished",
        "source": "https://www.foxsports.com/soccer/fifa-world-cup-men-dr-congo-vs-uzbekistan-jun-27-2026-game-boxscore-647685",
        "predictions": {
            "my_swarm": {
                "votes": {"数据": "主队胜", "战术": "主队胜", "伤病": "主队胜", "舆情": "主队胜", "风险官": "客队胜"},
                "final": "主队胜",
                "split": True
            },
            "opta": "待确认（Opta/The Analyst 未查到本场单场概率）",
            "kimi_official": "待确认",
            "coin_flip": coin_flip()
        },
        "score_pred": "2-1（四票主队胜；刚果金身体+战意占优，乌兹别克两战丢8球，风险官唱反调）",
        "key_players": "维萨、巴坎布、姆本巴（刚果金）；法伊祖拉耶夫、肖穆罗多夫（乌兹别克）",
        "recent_form": "刚果金1-1葡萄牙、0-1哥伦比亚；乌兹别克1-3哥伦比亚、0-5葡萄牙",
        "stay_up_index": 4,
        "one_liner": "非洲铁桶变主攻：刚果金必须取胜才能争夺最佳第三",
        "result_check": {"my_swarm": "hit", "opta": "n/a", "kimi_official": "n/a", "coin_flip": "n/a"}
    },
    {
        "date": "2026-06-27",
        "home": "阿尔及利亚",
        "away": "奥地利",
        "score": "3-3",
        "group": "J",
        "beijing_time": "06/28 10:00",
        "beijing_date": "2026-06-28",
        "status": "finished",
        "source": "https://www.foxsports.com/soccer/fifa-world-cup-men-algeria-vs-austria-jun-27-2026-game-boxscore-647687",
        "predictions": {
            "my_swarm": {
                "votes": {"数据": "平", "战术": "客队胜", "伤病": "客队胜", "舆情": "平", "风险官": "平"},
                "final": "平",
                "split": True
            },
            "opta": "待确认（Opta/The Analyst 未查到本场单场概率）",
            "kimi_official": "待确认",
            "coin_flip": coin_flip()
        },
        "score_pred": "1-1（三票平局；奥地利打平即出线，阿尔及利亚必须取胜，最终戏剧性平局）",
        "key_players": "马赫雷斯、古伊里（阿尔及利亚）；萨比策、阿瑙托维奇（奥地利）",
        "recent_form": "阿尔及利亚0-3阿根廷、2-1约旦；奥地利3-1约旦、0-2阿根廷",
        "stay_up_index": 3,
        "one_liner": "J组生死战：奥地利保平即晋级，阿尔及利亚背水一战",
        "result_check": {"my_swarm": "hit", "opta": "n/a", "kimi_official": "n/a", "coin_flip": "n/a"}
    },
    {
        "date": "2026-06-27",
        "home": "约旦",
        "away": "阿根廷",
        "score": "1-3",
        "group": "J",
        "beijing_time": "06/28 10:00",
        "beijing_date": "2026-06-28",
        "status": "finished",
        "source": "https://www.foxsports.com/soccer/fifa-world-cup-men-jordan-vs-argentina-jun-27-2026-game-boxscore-647686",
        "predictions": {
            "my_swarm": {
                "votes": {"数据": "客队胜", "战术": "客队胜", "伤病": "客队胜", "舆情": "客队胜", "风险官": "平"},
                "final": "客队胜",
                "split": True
            },
            "opta": "待确认（Opta/The Analyst 未查到本场单场概率）",
            "kimi_official": "待确认",
            "coin_flip": coin_flip()
        },
        "score_pred": "1-3（四票客队胜；阿根廷轮换仍实力碾压，约旦荣誉战难挡卫冕冠军）",
        "key_players": "穆萨·塔马里（约旦）；梅西、劳塔罗、洛塞尔索（阿根廷）",
        "recent_form": "约旦0-2奥地利、1-2阿尔及利亚；阿根廷3-0阿尔及利亚、2-0奥地利",
        "stay_up_index": 3,
        "one_liner": "卫冕冠军轮换出战，约旦世界杯首秀能否留下进球",
        "result_check": {"my_swarm": "hit", "opta": "n/a", "kimi_official": "n/a", "coin_flip": "n/a"}
    }
]

# Resolve coin_flip result_check
for d in day14:
    home = d["home"]
    score = d["score"]
    try:
        home_goals, away_goals = map(int, score.split("-"))
        if home_goals > away_goals:
            actual = "主队胜"
        elif home_goals < away_goals:
            actual = "客队胜"
        else:
            actual = "平"
    except Exception:
        actual = None
    cf = d["predictions"]["coin_flip"]
    d["result_check"]["coin_flip"] = "hit" if (actual and cf == actual) else "miss"

existing_keys = {(m["home"], m["away"], m.get("beijing_date")) for m in data["matches"]}
for d in day14:
    if (d["home"], d["away"], d["beijing_date"]) not in existing_keys:
        data["matches"].append(d)
        print(f"added: {d['home']} vs {d['away']}")
    else:
        print(f"already exists: {d['home']} vs {d['away']}")

# ---------- Recompute tally from all result_check entries ----------
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

# ---------- Update token_account daily_pick ----------
# Since group stage is done, next pick would be Round of 32; leave as the last successful pick note.
# We keep the 2026-06-27 Spain hit as the latest daily_pick.

with ledger_path.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("ledger updated")
print(json.dumps(data["tally"], ensure_ascii=False, indent=2))
