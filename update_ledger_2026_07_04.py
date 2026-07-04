#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update data/ledger.json for 2026-07-04 report."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
ledger_path = ROOT / "data" / "ledger.json"

with ledger_path.open("r", encoding="utf-8") as f:
    ledger = json.load(f)

# ---------- verified results ----------
# Beijing 07-03 matches (update source to post-match report)
results_0703 = {
    ("西班牙", "奥地利"): {
        "score": "3-0",
        "source": "https://indianexpress.com/article/sports/football/spain-vs-austria-national-football-teams-live-score-fifa-world-cup-2026-round-of-32-match-timeline-lineups-commentary-updates-10768436/",
    },
    ("葡萄牙", "克罗地亚"): {
        "score": "2-1",
        "source": "https://indianexpress.com/article/sports/football/portugal-vs-croatia-fifa-world-cup-2026-live-score-round-of-16-qualifier-football-match-lineups-commentary-updates-10768843/",
    },
    ("瑞士", "阿尔及利亚"): {
        "score": "2-0",
        "source": "https://www.vavel.com/en-us/soccer/2026/07/03/1264892-switzerland-vs-algeria-live-score-2026-fifa-world-cup.html",
    },
}

# Beijing 07-04 matches
results_0704 = {
    ("澳大利亚", "埃及"): {
        "score": "1-1（点球 2-4，埃及晋级）",
        "source": "https://olympics.com/en/news/fifa-world-cup-2026-australia-vs-egypt-round-of-32-score-lineups-live-updates",
        "result_check": {"my_swarm": "hit", "opta": "hit", "kimi_official": "n/a", "coin_flip": "hit"},
    },
    ("阿根廷", "佛得角"): {
        "score": "3-2（AET，90分钟 1-1）",
        "source": "https://indianexpress.com/article/sports/football/argentina-vs-cape-verde-fifa-world-cup-2026-live-score-round-of-16-qualifier-football-match-lineups-commentary-updates-10770403/",
        "result_check": {"my_swarm": "hit", "opta": "hit", "kimi_official": "n/a", "coin_flip": "hit"},
    },
    ("哥伦比亚", "加纳"): {
        "score": "1-0",
        "source": "https://www.espn.com.au/football/match/_/gameId/760501/ghana-colombia",
        "result_check": {"my_swarm": "hit", "opta": "hit", "kimi_official": "n/a", "coin_flip": "miss"},
    },
}

# update matches
for m in ledger["matches"]:
    key = (m.get("home"), m.get("away"))
    if key in results_0703 and m.get("beijing_date") == "2026-07-03":
        m["score"] = results_0703[key]["score"]
        m["source"] = results_0703[key]["source"]
        m["status"] = "finished"
    if key in results_0704 and m.get("beijing_date") == "2026-07-04":
        m["score"] = results_0704[key]["score"]
        m["source"] = results_0704[key]["source"]
        m["status"] = "finished"
        m["result_check"] = results_0704[key]["result_check"]

# ---------- update tally ----------
# current tally from ledger; add results from 07-02, 07-03, 07-04
# (07-02 and 07-03 result_check already exist but were not yet added to tally)
additions = {
    "my_swarm": {"hit": 9, "miss": 0},
    "kimi_official": {"hit": 0, "miss": 0},
    "opta": {"hit": 9, "miss": 0},
    "coin_flip": {"hit": 4, "miss": 5},
}
for col, delta in additions.items():
    ledger["tally"][col]["hit"] += delta["hit"]
    ledger["tally"][col]["miss"] += delta["miss"]

# ---------- token account ----------
# yesterday's pick (2026-07-03): Argentina vs Cape Verde, team Argentina
token_history = ledger["token_account"]["supported_team_history"]
daily_pick = ledger["token_account"]["daily_pick"]
if daily_pick.get("date") == "2026-07-03" and daily_pick.get("status") == "pending":
    daily_pick["status"] = "hit"
    token_history.append({
        "date": "2026-07-03",
        "match": "阿根廷 vs 佛得角",
        "team": "阿根廷",
        "status": "hit"
    })
# no new pending pick because today's matches are finished

with ledger_path.open("w", encoding="utf-8") as f:
    json.dump(ledger, f, ensure_ascii=False, indent=2)

print("ledger updated")
print("tally:", ledger["tally"])
