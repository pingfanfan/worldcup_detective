#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新 2026-07-02 日报对应的 ledger.json 数据"""
import json
import random
from pathlib import Path

ROOT = Path(__file__).parent
ledger_path = ROOT / "data" / "ledger.json"

with open(ledger_path, "r", encoding="utf-8") as f:
    ledger = json.load(f)

# ---- 1. 更新 tally ----
# 07/02 北京已核验三场的 result_check（按最终晋级判定）：
# 英格兰 2-1 刚果（金）：my_swarm hit, opta hit, coin_flip miss
# 比利时 3-2 塞内加尔（AET，90分钟2-2，加时晋级）：my_swarm hit, opta hit, coin_flip miss
# 美国 2-0 波黑：my_swarm hit, opta hit, coin_flip hit
ledger["tally"]["my_swarm"]["hit"] += 3
ledger["tally"]["opta"]["hit"] += 3
ledger["tally"]["coin_flip"]["hit"] += 1
ledger["tally"]["coin_flip"]["miss"] += 2

# ---- 2. 更新 token_account ----
# 把上一个 daily_pick（2026-06-30 德国 vs 巴拉圭，miss）补进历史
prev_pick = ledger["token_account"].get("daily_pick", {})
if prev_pick and prev_pick.get("date"):
    ledger["token_account"]["supported_team_history"].append({
        "date": prev_pick["date"],
        "match": prev_pick["match"],
        "team": prev_pick["team"],
        "status": prev_pick.get("status", "miss")
    })

# 07/01 日报建议站队英格兰，实际英格兰 2-1 胜，status hit
ledger["token_account"]["supported_team_history"].append({
    "date": "2026-07-01",
    "match": "英格兰 vs 刚果（金）",
    "team": "英格兰",
    "status": "hit"
})

# 07/02 日报建议站队西班牙（三场中数据面最稳的热门）
ledger["token_account"]["daily_pick"] = {
    "date": "2026-07-02",
    "match": "西班牙 vs 奥地利",
    "team": "西班牙",
    "status": "pending"
}

# ---- 3. 更新 2026-07-01（北京时间 07/02）三场已结束比赛 ----
matches = ledger["matches"]
for m in matches:
    if m.get("date") == "2026-07-01" and m.get("home") == "英格兰" and m.get("away") == "刚果（金）":
        m["score"] = "2-1"
        m["status"] = "finished"
        m["source"] = "https://www.olympics.com/en/news/fifa-world-cup-2026-england-dr-congo-round-32-score-lineups-live-updates"
        m["result_check"] = {
            "my_swarm": "hit",
            "opta": "hit",
            "kimi_official": "n/a",
            "coin_flip": "miss"
        }
    elif m.get("date") == "2026-07-01" and m.get("home") == "比利时" and m.get("away") == "塞内加尔":
        m["score"] = "3-2（AET，90分钟2-2）"
        m["status"] = "finished"
        m["source"] = "https://www.vavel.com/en-us/soccer/2026/07/01/1264833-belgium-vs-senegal-live-score-2026-world-cup.html"
        m["result_check"] = {
            "my_swarm": "hit",
            "opta": "hit",
            "kimi_official": "n/a",
            "coin_flip": "miss"
        }
    elif m.get("date") == "2026-07-01" and m.get("home") == "美国" and m.get("away") == "波黑":
        m["score"] = "2-0"
        m["status"] = "finished"
        m["source"] = "https://sports.yahoo.com/soccer/article/2026-fifa-world-cup-daily-schedule-every-match-date-kickoff-time-and-venue-for-all-48-teams-234515087.html"
        m["result_check"] = {
            "my_swarm": "hit",
            "opta": "hit",
            "kimi_official": "n/a",
            "coin_flip": "hit"
        }

# ---- 4. 添加 2026-07-02（北京时间 07/03）三场比赛 ----
def coin_flip():
    return random.choice(["主队胜", "平", "客队胜"])

new_matches = [
    {
        "date": "2026-07-02",
        "home": "西班牙",
        "away": "奥地利",
        "group": "1/16",
        "beijing_time": "07/03 03:00",
        "beijing_date": "2026-07-03",
        "status": "scheduled",
        "source": "https://www.espn.com/soccer/story/_/id/48939282/2026-fifa-world-cup-fixtures-results-match-schedule-group-stage-knockout-rounds-bracket",
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
            "opta": "西班牙 68.8% / 奥地利 31.2%（GoalIQ/Opta 模型，赛前单场胜率）",
            "kimi_official": "待确认",
            "coin_flip": coin_flip()
        },
        "score_pred": "2-0（四票主队胜，风险官看平；西班牙小组赛 0 失球、xG 7.93，但尼科·威廉斯与皮诺伤缺收敛比分）",
        "key_players": "拉明·亚马尔、米克尔·奥亚萨瓦尔（西班牙）；马尔科·阿瑙托维奇、马塞尔·萨比策（奥地利）",
        "recent_form": "西班牙小组赛 2 胜 1 平积 7 分，0 失球；奥地利 1 胜 1 平 1 负积 4 分，进 6 失 6",
        "stay_up_index": 5,
        "one_liner": "传控王者 vs 朗尼克高位逼抢：亚马尔能否撕开奥地利防线"
    },
    {
        "date": "2026-07-02",
        "home": "葡萄牙",
        "away": "克罗地亚",
        "group": "1/16",
        "beijing_time": "07/03 07:00",
        "beijing_date": "2026-07-03",
        "status": "scheduled",
        "source": "https://www.espn.com/soccer/story/_/id/48939282/2026-fifa-world-cup-fixtures-results-match-schedule-group-stage-knockout-rounds-bracket",
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
            "opta": "葡萄牙 ~55% / 平 ~25% / 克罗地亚 ~20%（赛前盘口隐含概率汇总）",
            "kimi_official": "待确认",
            "coin_flip": coin_flip()
        },
        "score_pred": "2-1（四票主队胜，风险官看平；C罗 vs 莫德里奇最后一舞，克罗地亚防线老化但加时/点球经验顶级）",
        "key_players": "克里斯蒂亚诺·罗纳尔多、布鲁诺·费尔南德斯（葡萄牙）；卢卡·莫德里奇、约什科·格瓦迪奥尔（克罗地亚）",
        "recent_form": "葡萄牙小组赛 1 胜 2 平积 5 分，进 6 失 1；克罗地亚 2 胜 1 负积 6 分，进 5 失 5",
        "stay_up_index": 4,
        "one_liner": "诸神黄昏：41 岁 C 罗与 40 岁魔笛的淘汰赛最后一舞"
    },
    {
        "date": "2026-07-02",
        "home": "瑞士",
        "away": "阿尔及利亚",
        "group": "1/16",
        "beijing_time": "07/03 11:00",
        "beijing_date": "2026-07-03",
        "status": "scheduled",
        "source": "https://www.espn.com/soccer/story/_/id/48939282/2026-fifa-world-cup-fixtures-results-match-schedule-group-stage-knockout-rounds-bracket",
        "predictions": {
            "my_swarm": {
                "votes": {
                    "数据": "主队胜",
                    "战术": "主队胜",
                    "伤病": "主队胜",
                    "舆情": "主队胜",
                    "风险官": "客队胜"
                },
                "final": "主队胜",
                "split": True
            },
            "opta": "瑞士 49.5% / 阿尔及利亚 23.9% / 平 26.6%（The Analyst Opta 90 分钟胜率）；瑞士晋级 63.75%",
            "kimi_official": "待确认",
            "coin_flip": coin_flip()
        },
        "score_pred": "2-1（四票主队胜，风险官直接押阿尔及利亚客胜；瑞士结构占优但淘汰赛 90 分钟胜率历史偏低）",
        "key_players": "布雷尔·恩博洛、格拉尼特·扎卡（瑞士）；里亚德·马赫雷斯、穆罕默德·阿穆拉（伤疑，阿尔及利亚）",
        "recent_form": "瑞士小组赛 2 胜 1 平积 7 分，进 7 失 3；阿尔及利亚 1 胜 1 平 1 负积 4 分，进 5 失 7",
        "stay_up_index": 3,
        "one_liner": "瑞士军刀 vs 沙漠之狐：前瑞士主帅彼得科维奇反戈旧主"
    }
]

ledger["matches"].extend(new_matches)

with open(ledger_path, "w", encoding="utf-8") as f:
    json.dump(ledger, f, ensure_ascii=False, indent=2)

print("ledger.json 更新完成")
print(f"my_swarm: {ledger['tally']['my_swarm']}")
print(f"opta: {ledger['tally']['opta']}")
print(f"coin_flip: {ledger['tally']['coin_flip']}")
