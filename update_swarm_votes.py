#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(__file__).parent
ledger_path = ROOT / "data" / "ledger.json"

with ledger_path.open("r", encoding="utf-8") as f:
    data = json.load(f)

# Votes extracted from swarm files for Day 8 matches (Beijing 2026-06-19)
swarm_votes = {
    "捷克": {
        "votes": {"数据": "主队胜", "战术": "主队胜", "伤病": "主队胜", "舆情": "主队胜", "风险官": "客队胜"},
        "final": "主队胜",
        "split": True,
        "score_pred": "1-0（数据看捷克小胜；战术看2-1；取数据端保守比分）",
    },
    "瑞士": {
        "votes": {"数据": "主队胜", "战术": "主队胜", "伤病": "主队胜", "舆情": "主队胜", "风险官": "客队胜"},
        "final": "主队胜",
        "split": True,
        "score_pred": "1-0（战术/伤病看瑞士零封小胜；数据看2-1；取最可能低比分）",
    },
    "加拿大": {
        "votes": {"数据": "主队胜", "战术": "主队胜", "伤病": "主队胜", "舆情": "主队胜", "风险官": "平"},
        "final": "主队胜",
        "split": True,
        "score_pred": "2-0（数据看2-0；战术/舆情看2-1；综合取主场净胜2球）",
    },
    "墨西哥": {
        "votes": {"数据": "平", "战术": "主队胜", "伤病": "平", "舆情": "平", "风险官": "客队胜"},
        "final": "平",
        "split": True,
        "score_pred": "1-1（数据/伤病/舆情均看平；战术看墨西哥2-1；多数票为平）",
    },
}

for m in data["matches"]:
    home = m["home"]
    if home in swarm_votes and m.get("beijing_date") == "2026-06-19":
        info = swarm_votes[home]
        m["predictions"]["my_swarm"] = {
            "votes": info["votes"],
            "final": info["final"],
            "split": info["split"],
        }
        # Update score_pred only if it was placeholder or to reflect consensus
        m["score_pred"] = info["score_pred"]

# Update token daily pick to a confident home win suggestion
# Based on swarm: Switzerland home win has 4/5 votes and strong data/opta support
data["token_account"]["daily_pick"] = {
    "date": "2026-06-18",
    "match": "瑞士 vs 波黑",
    "team": "瑞士",
    "status": "pending"
}

with ledger_path.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("swarm votes updated")
