#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update data/ledger.json for 2026-06-27 daily report."""
import json
import random
from pathlib import Path

ROOT = Path(__file__).parent
ledger_path = ROOT / "data" / "ledger.json"

with ledger_path.open("r", encoding="utf-8") as f:
    data = json.load(f)

# Deterministic coin flip
random.seed("2026-06-27-coin-flip")

def coin_flip():
    return random.choice(["主队胜", "平", "客队胜"])

# ---------- Add Day 13 matches (Beijing 2026-06-27, US 2026-06-26) as FINISHED ----------
day13 = [
    {
        "date": "2026-06-26",
        "home": "挪威",
        "away": "法国",
        "score": "1-4",
        "group": "I",
        "beijing_time": "06/27 03:00",
        "beijing_date": "2026-06-27",
        "status": "finished",
        "source": "https://www.britannica.com/event/2026-FIFA-World-Cup（France won 4-1）",
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
        "score_pred": "1-2（四票客队胜；法国阵容深度与边路优势压制挪威，但已出线轮换/平局即够头名需降档）",
        "key_players": "哈兰德、厄德高（挪威）；姆巴佩、登贝莱（法国）",
        "recent_form": "挪威4-1伊拉克、3-2塞内加尔；法国3-1塞内加尔、3-0伊拉克",
        "stay_up_index": 5,
        "one_liner": "姆哈金靴对决：法国打平即锁头名，挪威必须取胜才能反超",
        "result_check": {"my_swarm": "hit", "opta": "n/a", "kimi_official": "n/a", "coin_flip": "n/a"}
    },
    {
        "date": "2026-06-26",
        "home": "塞内加尔",
        "away": "伊拉克",
        "score": "5-0",
        "group": "I",
        "beijing_time": "06/27 03:00",
        "beijing_date": "2026-06-27",
        "status": "finished",
        "source": "https://www.britannica.com/event/2026-FIFA-World-Cup（Senegal won 5-0）",
        "predictions": {
            "my_swarm": {
                "votes": {"数据": "主队胜", "战术": "主队胜", "伤病": "主队胜", "舆情": "主队胜", "风险官": "平"},
                "final": "主队胜",
                "split": True
            },
            "opta": "待确认（Opta/The Analyst 未查到本场单场概率）",
            "kimi_official": "待确认",
            "coin_flip": coin_flip()
        },
        "score_pred": "2-0（四票主队胜；塞内加尔攻击线 intact，伊拉克防线崩盘，但深盘过热风险官唱平）",
        "key_players": "马内、萨尔、雅克松（塞内加尔）；艾曼·侯赛因（伊拉克）",
        "recent_form": "塞内加尔1-3法国、2-3挪威；伊拉克1-4挪威、0-3法国",
        "stay_up_index": 5,
        "one_liner": "荣誉战中的深盘热门：非洲大象能否大胜挽回尊严",
        "result_check": {"my_swarm": "hit", "opta": "n/a", "kimi_official": "n/a", "coin_flip": "n/a"}
    },
    {
        "date": "2026-06-26",
        "home": "佛得角",
        "away": "沙特阿拉伯",
        "score": "0-0",
        "group": "H",
        "beijing_time": "06/27 08:00",
        "beijing_date": "2026-06-27",
        "status": "finished",
        "source": "https://www.britannica.com/event/2026-FIFA-World-Cup（Match drawn 0-0）",
        "predictions": {
            "my_swarm": {
                "votes": {"数据": "主队胜", "战术": "主队胜", "伤病": "客队胜", "舆情": "主队胜", "风险官": "客队胜"},
                "final": "主队胜",
                "split": True
            },
            "opta": "待确认（Opta/The Analyst 未查到本场单场概率）",
            "kimi_official": "待确认",
            "coin_flip": coin_flip()
        },
        "score_pred": "1-0（三票主队胜；佛得角低位纪律性惊艳，但伤停与沙特必须取胜制造分歧）",
        "key_players": "沃济尼亚、瑞恩·门德斯（佛得角）；奥韦斯、阿尔道萨里（沙特）",
        "recent_form": "佛得角0-0西班牙、2-2乌拉圭；沙特1-1乌拉圭、0-4西班牙",
        "stay_up_index": 3,
        "one_liner": "世界杯新军励志剧本 vs 亚洲铁桶：沙特必须取胜才能保留希望",
        "result_check": {"my_swarm": "miss", "opta": "n/a", "kimi_official": "n/a", "coin_flip": "n/a"}
    },
    {
        "date": "2026-06-26",
        "home": "乌拉圭",
        "away": "西班牙",
        "score": "0-1",
        "group": "H",
        "beijing_time": "06/27 08:00",
        "beijing_date": "2026-06-27",
        "status": "finished",
        "source": "https://www.britannica.com/event/2026-FIFA-World-Cup（Spain won 1-0）",
        "predictions": {
            "my_swarm": {
                "votes": {"数据": "客队胜", "战术": "客队胜", "伤病": "客队胜", "舆情": "客队胜", "风险官": "平"},
                "final": "客队胜",
                "split": True
            },
            "opta": "西班牙 62.4% / 乌拉圭 15.7% / 平 21.9%（Opta/The Analyst）",
            "kimi_official": "待确认",
            "coin_flip": coin_flip()
        },
        "score_pred": "1-2（四票客队胜；西班牙控球与边路优势明显，乌拉圭残阵背水一战）",
        "key_players": "巴尔韦德（乌拉圭）；亚马尔、尼科·威廉姆斯（西班牙）",
        "recent_form": "乌拉圭1-1沙特、2-2佛得角；西班牙0-0佛得角、4-0沙特",
        "stay_up_index": 3,
        "one_liner": "H组头名争夺战：西班牙不败即第一，乌拉圭必须取胜",
        "result_check": {"my_swarm": "hit", "opta": "hit", "kimi_official": "n/a", "coin_flip": "n/a"}
    },
    {
        "date": "2026-06-26",
        "home": "埃及",
        "away": "伊朗",
        "score": "1-1",
        "group": "G",
        "beijing_time": "06/27 11:00",
        "beijing_date": "2026-06-27",
        "status": "finished",
        "source": "https://www.britannica.com/event/2026-FIFA-World-Cup（Match drawn 1-1）",
        "predictions": {
            "my_swarm": {
                "votes": {"数据": "主队胜", "战术": "主队胜", "伤病": "平", "舆情": "主队胜", "风险官": "平"},
                "final": "主队胜",
                "split": True
            },
            "opta": "待确认（Opta/The Analyst 未查到本场单场概率）",
            "kimi_official": "待确认",
            "coin_flip": coin_flip()
        },
        "score_pred": "1-0（三票主队胜；埃及打平即可出线，伊朗必须取胜但破密集乏力，伤病与风险官看平）",
        "key_players": "萨拉赫、马尔穆什（埃及）；塔雷米、贝兰万德（伊朗）",
        "recent_form": "埃及1-1比利时、3-1新西兰；伊朗2-2新西兰、0-0比利时",
        "stay_up_index": 1,
        "one_liner": "G组生死战：埃及保平即晋级，伊朗必须取胜",
        "result_check": {"my_swarm": "miss", "opta": "n/a", "kimi_official": "n/a", "coin_flip": "n/a"}
    },
    {
        "date": "2026-06-26",
        "home": "新西兰",
        "away": "比利时",
        "score": "1-5",
        "group": "G",
        "beijing_time": "06/27 11:00",
        "beijing_date": "2026-06-27",
        "status": "finished",
        "source": "https://www.britannica.com/event/2026-FIFA-World-Cup（Belgium won 5-1）",
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
        "score_pred": "0-2（四票客队胜；比利时阵容深度碾压，但前两轮终结荒+本场深盘触发风险官降档）",
        "key_players": "克里斯·伍德（新西兰）；德布劳内、多库（比利时）",
        "recent_form": "新西兰2-2伊朗、1-3埃及；比利时1-1埃及、0-0伊朗",
        "stay_up_index": 1,
        "one_liner": "欧洲红魔背水一战：必须取胜才能保留出线希望",
        "result_check": {"my_swarm": "hit", "opta": "n/a", "kimi_official": "n/a", "coin_flip": "n/a"}
    }
]

# Resolve coin_flip result_check after generation
for d in day13:
    actual = None
    if d["home"] == "挪威" and d["away"] == "法国":
        actual = "客队胜"
    elif d["home"] == "塞内加尔" and d["away"] == "伊拉克":
        actual = "主队胜"
    elif d["home"] == "佛得角" and d["away"] == "沙特阿拉伯":
        actual = "平"
    elif d["home"] == "乌拉圭" and d["away"] == "西班牙":
        actual = "客队胜"
    elif d["home"] == "埃及" and d["away"] == "伊朗":
        actual = "平"
    elif d["home"] == "新西兰" and d["away"] == "比利时":
        actual = "客队胜"
    cf = d["predictions"]["coin_flip"]
    d["result_check"]["coin_flip"] = "hit" if cf == actual else "miss"

existing_keys = {(m["home"], m["away"], m.get("beijing_date")) for m in data["matches"]}
for d in day13:
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
# Pick Spain (Uruguay vs Spain) for 2026-06-27; actual result Spain won 1-0 -> hit
data["token_account"]["daily_pick"] = {
    "date": "2026-06-27",
    "match": "乌拉圭 vs 西班牙",
    "team": "西班牙",
    "status": "hit"
}
data["token_account"]["supported_team_history"].append({
    "date": "2026-06-27",
    "match": "乌拉圭 vs 西班牙",
    "team": "西班牙",
    "status": "hit"
})

with ledger_path.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("ledger updated")
print(json.dumps(data["tally"], ensure_ascii=False, indent=2))
