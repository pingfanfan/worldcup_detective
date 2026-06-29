#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update data/ledger.json for 2026-06-29 daily report."""
import json
import random
from pathlib import Path

ROOT = Path(__file__).parent
ledger_path = ROOT / "data" / "ledger.json"

with ledger_path.open("r", encoding="utf-8") as f:
    data = json.load(f)

# Deterministic coin flip
random.seed("2026-06-29-coin-flip")

def coin_flip():
    return random.choice(["主队胜", "平", "客队胜"])

# ---------- Add Round of 32 match (Beijing 2026-06-29) as FINISHED ----------
# Verified result from Fox Sports boxscore: Canada 1-0 South Africa (Eustaquio 90+2')
match = {
    "date": "2026-06-28",
    "home": "南非",
    "away": "加拿大",
    "score": "0-1",
    "group": "32强",
    "beijing_time": "06/29 03:00",
    "beijing_date": "2026-06-29",
    "status": "finished",
    "source": "https://www.foxsports.com/soccer/fifa-world-cup-men-south-africa-vs-canada-jun-28-2026-game-boxscore-607903",
    "predictions": {
        "my_swarm": {
            "votes": {"数据": "客队胜", "战术": "客队胜", "伤病": "客队胜", "舆情": "客队胜", "风险官": "平"},
            "final": "客队胜",
            "split": True
        },
        "opta": "加拿大 55.1% / 平 24.9% / 南非 20.0%（Opta 超级计算机，赛前单场概率）",
        "kimi_official": "待确认",
        "coin_flip": coin_flip()
    },
    "score_pred": "0-1（赛前数据/舆情最热剧本；实际赛果：欧斯塔基奥 90+2' 绝杀）",
    "key_players": "Jonathan David、Stephen Eustáquio（加拿大）；Ronwen Williams、Teboho Mokoena（南非）",
    "recent_form": "南非 1-1-1（0-2 墨西哥、1-1 捷克、1-0 韩国）；加拿大 1-1-1（1-1 波黑、6-0 卡塔尔、1-2 瑞士）",
    "stay_up_index": 5,
    "one_liner": "世界杯史上首场 1/16 决赛：东道主加拿大洛杉矶绝杀南非晋级",
    "result_check": {"my_swarm": "hit", "opta": "hit", "kimi_official": "n/a", "coin_flip": "n/a"}
}

# Resolve coin_flip result_check
score = match["score"]
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
cf = match["predictions"]["coin_flip"]
match["result_check"]["coin_flip"] = "hit" if (actual and cf == actual) else "miss"

# Avoid duplicates
existing_keys = {(m["home"], m["away"], m.get("beijing_date")) for m in data["matches"]}
if (match["home"], match["away"], match["beijing_date"]) not in existing_keys:
    data["matches"].append(match)
    print(f"added: {match['home']} vs {match['away']}")
else:
    print(f"already exists: {match['home']} vs {match['away']}")

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
data["token_account"]["daily_pick"] = {
    "date": "2026-06-29",
    "match": "南非 vs 加拿大",
    "team": "加拿大",
    "status": "hit"
}

# Update supported_team_history if needed
hist = data["token_account"].setdefault("supported_team_history", [])
hist.append({
    "date": "2026-06-29",
    "match": "南非 vs 加拿大",
    "team": "加拿大",
    "status": "hit"
})

with ledger_path.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("ledger updated")
print(json.dumps(data["tally"], ensure_ascii=False, indent=2))
