#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update data/ledger.json for 2026-06-30 report."""
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
ledger_path = ROOT / "data" / "ledger.json"

with ledger_path.open("r", encoding="utf-8") as f:
    ledger = json.load(f)

# ---------- 1. update tally based on 2026-06-29 Beijing match (South Africa 0-1 Canada) ----------
# my_swarm hit, opta hit, coin_flip miss
ledger["tally"]["my_swarm"]["hit"] = 46
ledger["tally"]["opta"]["hit"] = 18
ledger["tally"]["coin_flip"]["miss"] = 41

# ---------- 2. update token_account daily pick ----------
ledger["token_account"]["daily_pick"] = {
    "date": "2026-06-30",
    "match": "德国 vs 巴拉圭",
    "team": "德国",
    "status": "pending"
}

# ---------- 3. append today's matches ----------
today_matches = [
    {
        "date": "2026-06-29",
        "home": "巴西",
        "away": "日本",
        "group": "1/16",
        "beijing_time": "06/30 01:00",
        "beijing_date": "2026-06-30",
        "status": "scheduled",
        "source": "https://sports.yahoo.com/articles/2026-world-cup-tv-schedule-140319091.html",
        "predictions": {
            "my_swarm": {
                "votes": {
                    "数据": "主队胜",
                    "战术": "主队胜",
                    "伤病": "主队胜",
                    "舆情": "主队胜",
                    "风险官": "平"
                },
                "final": "主队胜",
                "split": True
            },
            "opta": "待确认（Opta 超级计算机赛前预测巴西 2-1 日本，来源：vietnam.vn）",
            "kimi_official": "待确认",
            "coin_flip": "待确认"
        },
        "score_pred": "2-1（四票主胜，风险官看平；数据端巴西隐含胜率约 55%，淘汰赛低比分常态）",
        "key_players": "Vinícius Júnior（巴西）、Ritsu Dōan（日本）",
        "recent_form": "巴西小组赛 1-1 摩洛哥、3-0 海地、3-0 苏格兰；日本 2-2 荷兰、4-0 突尼斯、1-1 瑞典",
        "stay_up_index": 5,
        "one_liner": "淘汰赛首战：维尼修斯连续三场进球 vs 日本近 10 场连续进球，高温休斯顿谁能破局"
    },
    {
        "date": "2026-06-29",
        "home": "德国",
        "away": "巴拉圭",
        "group": "1/16",
        "beijing_time": "06/30 04:30",
        "beijing_date": "2026-06-30",
        "status": "scheduled",
        "source": "https://sports.yahoo.com/articles/2026-world-cup-tv-schedule-140319091.html",
        "predictions": {
            "my_swarm": {
                "votes": {
                    "数据": "主队胜",
                    "战术": "主队胜",
                    "伤病": "主队胜",
                    "舆情": "主队胜",
                    "风险官": "平"
                },
                "final": "主队胜",
                "split": True
            },
            "opta": "待确认（Opta 超级计算机赛前预测德国 2-0 巴拉圭，来源：vietnam.vn）",
            "kimi_official": "待确认",
            "coin_flip": "待确认"
        },
        "score_pred": "2-0（四票主胜，风险官看平；德国隐含胜率约 70%，但 Schlotterbeck 报销需降档）",
        "key_players": "Jamal Musiala（德国）、Miguel Almirón（巴拉圭）",
        "recent_form": "德国小组赛 7-1 库拉索、2-1 科特迪瓦、1-2 厄瓜多尔；巴拉圭 1-4 美国、1-0 土耳其、0-0 澳大利亚",
        "stay_up_index": 5,
        "one_liner": "日耳曼战车轮挑战南美铁桶：穆西亚拉-维尔茨能否敲开巴拉圭低位防线"
    },
    {
        "date": "2026-06-29",
        "home": "荷兰",
        "away": "摩洛哥",
        "group": "1/16",
        "beijing_time": "06/30 09:00",
        "beijing_date": "2026-06-30",
        "status": "scheduled",
        "source": "https://sports.yahoo.com/articles/2026-world-cup-tv-schedule-140319091.html",
        "predictions": {
            "my_swarm": {
                "votes": {
                    "数据": "平",
                    "战术": "主队胜",
                    "伤病": "主队胜",
                    "舆情": "主队胜",
                    "风险官": "客队胜"
                },
                "final": "主队胜",
                "split": True
            },
            "opta": "待确认",
            "kimi_official": "待确认",
            "coin_flip": "待确认"
        },
        "score_pred": "2-1（三票主胜、一票平、一票客胜；荷兰 vs 摩洛哥历来进球局，但荷兰连续无零封是隐患）",
        "key_players": "Cody Gakpo（荷兰）、Achraf Hakimi（摩洛哥）",
        "recent_form": "荷兰小组赛 2-2 日本、5-1 瑞典、3-1 突尼斯；摩洛哥 1-1 巴西、1-0 苏格兰、4-2 海地",
        "stay_up_index": 3,
        "one_liner": "F 组第一 vs C 组第二：橙衣军团火力全开 vs 阿特拉斯雄狮 2022 四强班底"
    }
]

ledger["matches"].extend(today_matches)

# ---------- 4. write back ----------
with ledger_path.open("w", encoding="utf-8") as f:
    json.dump(ledger, f, ensure_ascii=False, indent=2)

print(f"ledger updated: {ledger_path}")
print(f"tally: my_swarm {ledger['tally']['my_swarm']}, opta {ledger['tally']['opta']}, coin_flip {ledger['tally']['coin_flip']}")
