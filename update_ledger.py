#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update data/ledger.json for 2026-06-18 daily report."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
ledger_path = ROOT / "data" / "ledger.json"

with ledger_path.open("r", encoding="utf-8") as f:
    data = json.load(f)

# ---------- 1. Verify & fill results for Day 7 (Beijing 06/18 early) ----------
day7_results = {
    "葡萄牙": {"away": "刚果（金）", "score": "1-1", "source": "https://english.ahram.org.eg/WorldCup2026/WC2026News/2026/6/17/19_2026-639173328625715322-571.aspx（DR Congo hold Portugal 1-1）"},
    "英格兰": {"away": "克罗地亚", "score": "4-2", "source": "https://www.vietnam.vn/en/nhan-dinh-ty-so-the-vang-uzbekistan-vs-colombia-9h00-ngay-18-6-bang-k-world-cup-2026-mua-the-se-xuat-hien（England 4-2 Croatia）"},
    "加纳": {"away": "巴拿马", "score": "1-0", "source": "https://4score.ru/en/events/ghana-panama-17-06-2026/（Ghana 1-0 Panama FT）"},
    "乌兹别克斯坦": {"away": "哥伦比亚", "score": "1-3", "source": "https://4score.ru/en/events/uzbekistan-kolumbiya-18-06-2026/（Uzbekistan 1-3 Colombia FT）"},
}

# Helper to find a match by home team name (Chinese) and beijing_date 2026-06-18
def find_match(home):
    for m in data["matches"]:
        if m["home"] == home and m.get("beijing_date") == "2026-06-18":
            return m
    return None

for home, info in day7_results.items():
    m = find_match(home)
    if not m:
        print(f"WARN: match not found for {home}")
        continue
    m["score"] = info["score"]
    m["status"] = "finished"
    m["source"] = info["source"]
    # Ensure result_check exists
    if "result_check" not in m:
        m["result_check"] = {}

# ---------- 2. Compute result_check for Day 7 matches ----------
# Portugal: my_swarm final 主队胜, actual draw -> miss; opta group -> n/a; kimi n/a; coin 主队胜 -> miss
m = find_match("葡萄牙")
if m:
    m["result_check"]["my_swarm"] = "miss"
    m["result_check"]["opta"] = "n/a"
    m["result_check"]["kimi_official"] = "n/a"
    m["result_check"]["coin_flip"] = "miss"

# England: my_swarm final 主队胜 -> hit; opta England 55.9% -> hit; coin 平 -> miss
m = find_match("英格兰")
if m:
    m["result_check"]["my_swarm"] = "hit"
    m["result_check"]["opta"] = "hit"
    m["result_check"]["kimi_official"] = "n/a"
    m["result_check"]["coin_flip"] = "miss"

# Ghana: my_swarm final 平 -> actual Ghana win -> miss; opta n/a; coin 客队胜 -> miss
m = find_match("加纳")
if m:
    m["result_check"]["my_swarm"] = "miss"
    m["result_check"]["opta"] = "n/a"
    m["result_check"]["kimi_official"] = "n/a"
    m["result_check"]["coin_flip"] = "miss"

# Uzbekistan: my_swarm final 客队胜 -> hit; opta Colombia win prob -> hit; coin 主队胜 -> miss
m = find_match("乌兹别克斯坦")
if m:
    m["result_check"]["my_swarm"] = "hit"
    m["result_check"]["opta"] = "hit"
    m["result_check"]["kimi_official"] = "n/a"
    m["result_check"]["coin_flip"] = "miss"

# ---------- 3. Recompute tally from all result_check entries ----------
tally = {"my_swarm": {"hit": 0, "miss": 0}, "kimi_official": {"hit": 0, "miss": 0},
         "opta": {"hit": 0, "miss": 0}, "coin_flip": {"hit": 0, "miss": 0}}

for m in data["matches"]:
    rc = m.get("result_check", {})
    for key in tally:
        val = rc.get(key)
        if val == "hit":
            tally[key]["hit"] += 1
        elif val == "miss":
            tally[key]["miss"] += 1
        # n/a ignored

data["tally"] = tally

# ---------- 4. Add Day 8 matches (Beijing 06/19) ----------
day8 = [
    {
        "date": "2026-06-18",
        "home": "捷克",
        "away": "南非",
        "group": "A",
        "beijing_time": "06/19 05:00",
        "beijing_date": "2026-06-19",
        "status": "scheduled",
        "source": "https://www.espn.com/soccer/story/_/id/48939282/2026-fifa-world-cup-fixtures-results-match-schedule-group-stage-knockout-rounds-bracket",
        "predictions": {
            "my_swarm": {"votes": {"数据": "待确认", "战术": "待确认", "伤病": "待确认", "舆情": "待确认", "风险官": "待确认"},
                         "final": "待确认", "split": False},
            "opta": "待确认（Opta/The Analyst 未查到单场概率；小组预测：墨西哥小组第一 47.8%）",
            "kimi_official": "待确认",
            "coin_flip": "主队胜"
        },
        "score_pred": "1-0（赛前主流看捷克小胜；南非首战0-2墨西哥且两张红牌）",
        "key_players": "希克、绍切克（捷克）；姆韦拉、西索尔（南非）",
        "recent_form": "捷克首战1-2遭韩国逆转；南非首战0-2墨西哥、近4场仅2球",
        "stay_up_index": 2,
        "one_liner": " loser几乎出局：捷克能否用欧洲经验碾压残阵南非？"
    },
    {
        "date": "2026-06-18",
        "home": "瑞士",
        "away": "波黑",
        "group": "B",
        "beijing_time": "06/19 08:00",
        "beijing_date": "2026-06-19",
        "status": "scheduled",
        "source": "https://www.espn.com/soccer/story/_/id/48939282/2026-fifa-world-cup-fixtures-results-match-schedule-group-stage-knockout-rounds-bracket",
        "predictions": {
            "my_swarm": {"votes": {"数据": "待确认", "战术": "待确认", "伤病": "待确认", "舆情": "待确认", "风险官": "待确认"},
                         "final": "待确认", "split": False},
            "opta": "瑞士出线概率较高；小组四队首战皆平（Opta/The Analyst 小组预测）",
            "kimi_official": "待确认",
            "coin_flip": "主队胜"
        },
        "score_pred": "1-0（波黑近9场6平，瑞士防线稳健但攻坚效率一般）",
        "key_players": "恩博洛、扎卡、阿坎吉（瑞士）；哲科、德米罗维奇（波黑）",
        "recent_form": "瑞士近6场正式比赛不败；波黑连续5场平局",
        "stay_up_index": 1,
        "one_liner": "B组全平之后的六分战：瑞士经验能否敲开波黑铁桶？"
    },
    {
        "date": "2026-06-18",
        "home": "加拿大",
        "away": "卡塔尔",
        "group": "B",
        "beijing_time": "06/19 11:00",
        "beijing_date": "2026-06-19",
        "status": "scheduled",
        "source": "https://www.espn.com/soccer/story/_/id/48939282/2026-fifa-world-cup-fixtures-results-match-schedule-group-stage-knockout-rounds-bracket",
        "predictions": {
            "my_swarm": {"votes": {"数据": "待确认", "战术": "待确认", "伤病": "待确认", "舆情": "待确认", "风险官": "待确认"},
                         "final": "待确认", "split": False},
            "opta": "加拿大出线概率 42.7%，预计与瑞士争夺小组头名（Opta/The Analyst）",
            "kimi_official": "待确认",
            "coin_flip": "平"
        },
        "score_pred": "2-0（东道主加拿大主场施压，卡塔尔首战被瑞士狂射26脚）",
        "key_players": "戴维斯、戴维（加拿大）；阿菲夫、阿里（卡塔尔）",
        "recent_form": "加拿大近10场不败且7场零封；卡塔尔首战1-1瑞士但xG仅0.76",
        "stay_up_index": 3,
        "one_liner": "东道主冲击世界杯首胜，卡塔尔高位防线能否顶住加拿大速度？"
    },
    {
        "date": "2026-06-19",
        "home": "墨西哥",
        "away": "韩国",
        "group": "A",
        "beijing_time": "06/19 14:00",
        "beijing_date": "2026-06-19",
        "status": "scheduled",
        "source": "https://www.espn.com/soccer/story/_/id/48939282/2026-fifa-world-cup-fixtures-results-match-schedule-group-stage-knockout-rounds-bracket",
        "predictions": {
            "my_swarm": {"votes": {"数据": "待确认", "战术": "待确认", "伤病": "待确认", "舆情": "待确认", "风险官": "待确认"},
                         "final": "待确认", "split": False},
            "opta": "墨西哥小组第一 47.8% / 晋级 52.0%（Opta/The Analyst）",
            "kimi_official": "待确认",
            "coin_flip": "主队胜"
        },
        "score_pred": "2-1（墨西哥主场气势+韩国反击，双方均有进球预期）",
        "key_players": "吉梅内斯、阿尔瓦雷斯（墨西哥）；孙兴慜、李刚仁（韩国）",
        "recent_form": "墨西哥首战2-0南非，2026年9场不败；韩国首战2-1逆转捷克",
        "stay_up_index": 4,
        "one_liner": "小组头名之争：墨西哥东道主加持 vs 韩国亚洲反击风暴"
    }
]

# Avoid duplicates
existing_keys = {(m["home"], m["away"], m.get("beijing_date")) for m in data["matches"]}
for d in day8:
    if (d["home"], d["away"], d["beijing_date"]) not in existing_keys:
        data["matches"].append(d)

# ---------- 5. Update token_account daily_pick to today's suggestion placeholder ----------
# Will be filled after swarm; here leave the previous pick as pending.

with ledger_path.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("ledger updated")
print(json.dumps(data["tally"], ensure_ascii=False, indent=2))
