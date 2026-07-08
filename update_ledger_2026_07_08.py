#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update ledger for 2026-07-08 report."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
LEDGER = ROOT / "data" / "ledger.json"

with LEDGER.open("r", encoding="utf-8") as f:
    ledger = json.load(f)

# ---- 1. yesterday matches (beijing 2026-07-07) results and result_check ----
yesterday_results = {
    ("葡萄牙", "西班牙"): {
        "score": "0-1",
        "source": "https://www.espn.com/soccer/match/_/gameId/760506/spain-portugal",
        "result_check": {"my_swarm": "hit", "opta": "hit", "kimi_official": "n/a", "coin_flip": "hit"},
    },
    ("美国", "比利时"): {
        "score": "1-4",
        "source": "https://www.espn.com/soccer/match/_/gameId/760507/belgium-united-states",
        "result_check": {"my_swarm": "miss", "opta": "n/a", "kimi_official": "n/a", "coin_flip": "miss"},
    },
}

for m in ledger["matches"]:
    key = (m.get("home"), m.get("away"))
    if key in yesterday_results and m.get("beijing_date") == "2026-07-07":
        info = yesterday_results[key]
        m["status"] = "finished"
        m["score"] = info["score"]
        m["source"] = info["source"]
        m["result_check"] = info["result_check"]

# ---- 2. update tally ----
ledger["tally"]["my_swarm"]["hit"] = 66    # Portugal hit
ledger["tally"]["opta"]["hit"] = 38        # Portugal hit
ledger["tally"]["coin_flip"]["hit"] = 30   # Portugal hit
ledger["tally"]["coin_flip"]["miss"] = 52  # USA miss

# ---- 3. token account ----
token = ledger["token_account"]
# close yesterday pick (Spain)
token["supported_team_history"].append({
    "date": "2026-07-07",
    "match": "葡萄牙 vs 西班牙",
    "team": "西班牙",
    "status": "hit"
})
token["daily_pick"] = {
    "date": "2026-07-08",
    "match": "阿根廷 vs 埃及",
    "team": "阿根廷",
    "status": "pending"
}

# ---- 4. add today's matches (beijing 2026-07-08) ----
new_matches = [
    {
        "date": "2026-07-07",
        "home": "阿根廷",
        "away": "埃及",
        "score": "",
        "group": "1/8",
        "beijing_time": "07/08 00:00",
        "beijing_date": "2026-07-08",
        "status": "scheduled",
        "source": "https://www.espn.com/soccer/story/_/id/48939282/2026-fifa-world-cup-fixtures-results-match-schedule-group-stage-knockout-rounds-bracket",
        "predictions": {
            "my_swarm": {
                "votes": {"数据": "主队胜", "战术": "主队胜", "伤病": "主队胜", "舆情": "主队胜", "风险官": "平"},
                "final": "主队胜",
                "split": True,
            },
            "opta": "阿根廷 69.6% / 平局 18.9% / 埃及 11.5%（Opta/The Analyst，来源：https://theanalyst.com/articles/argentina-vs-egypt-prediction-world-cup-2026-match-preview）",
            "kimi_official": "待确认",
            "coin_flip": "主队胜",
        },
        "score_pred": "2-1（四票看阿根廷小胜，风险官看平）",
        "key_players": "梅西、阿尔瓦雷斯（阿根廷）；萨拉赫、马尔穆什（埃及）",
        "recent_form": "阿根廷小组赛3-0阿尔及利亚、2-0奥地利、3-1约旦，1/32决赛加时3-2佛得角；埃及小组赛1-1比利时、3-1新西兰、1-1伊朗，1/32决赛点球淘汰澳大利亚",
        "stay_up_index": 5,
        "one_liner": "梅西第八球纪录之夜？阿根廷刚踢满120分钟疲劳+埃及低位铁桶，卫冕冠军难大胜",
    },
    {
        "date": "2026-07-07",
        "home": "瑞士",
        "away": "哥伦比亚",
        "score": "",
        "group": "1/8",
        "beijing_time": "07/08 04:00",
        "beijing_date": "2026-07-08",
        "status": "scheduled",
        "source": "https://www.espn.com/soccer/story/_/id/48939282/2026-fifa-world-cup-fixtures-results-match-schedule-group-stage-knockout-rounds-bracket",
        "predictions": {
            "my_swarm": {
                "votes": {"数据": "客队胜", "战术": "客队胜", "伤病": "客队胜", "舆情": "客队胜", "风险官": "主队胜"},
                "final": "客队胜",
                "split": True,
            },
            "opta": "哥伦比亚 41.9% / 瑞士 29.4% / 平局 28.0%（Opta/The Analyst，来源：https://theanalyst.com/articles/switzerland-vs-colombia-prediction-world-cup-2026-match-preview）",
            "kimi_official": "待确认",
            "coin_flip": "客队胜",
        },
        "score_pred": "1-0（四票看哥伦比亚小胜，风险官反向看瑞士）",
        "key_players": "恩博洛、扎卡（瑞士）；路易斯·迪亚斯、J罗（哥伦比亚）",
        "recent_form": "瑞士小组赛1-1卡塔尔、4-1波黑、2-1加拿大，1/32决赛2-0阿尔及利亚；哥伦比亚小组赛3-1乌兹别克斯坦、1-0刚果（金）、0-0葡萄牙，1/32决赛1-0加纳",
        "stay_up_index": 4,
        "one_liner": "哥伦比亚防线本届仅丢1球但主力中锋科尔多瓦报销，瑞士缺Manzambi，低比分消耗战看迪亚斯",
    },
]

ledger["matches"].extend(new_matches)

# ---- 5. write back ----
with LEDGER.open("w", encoding="utf-8") as f:
    json.dump(ledger, f, ensure_ascii=False, indent=2)

print("ledger updated")
