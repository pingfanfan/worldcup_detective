#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate reports/日报-2026-07-13.html (semifinal rest-day preview)."""
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
REPORT_DATE = "2026-07-13"
YESTERDAY_DATE = "2026-07-12"
ISSUE = "29"
DATE_CN = "07月13日"

with (ROOT / "data" / "ledger.json").open("r", encoding="utf-8") as f:
    ledger = json.load(f)

template = (ROOT / "templates" / "report-template.html").read_text(encoding="utf-8")

# ---------- helpers ----------
def rate(rec):
    total = rec["hit"] + rec["miss"]
    if total == 0:
        return "N/A"
    return f"{rec['hit']/total*100:.1f}%"

def rec_str(rec):
    return f"{rec['hit']}胜{rec['miss']}负"

# ---------- scoreboard ----------
tally = ledger["tally"]
my_rate = rate(tally["my_swarm"])
kimi_rate = rate(tally["kimi_official"])
opta_rate = rate(tally["opta"])
coin_rate = rate(tally["coin_flip"])

candidates = {
    "my_swarm": (tally["my_swarm"]["hit"], tally["my_swarm"]["miss"]),
    "opta": (tally["opta"]["hit"], tally["opta"]["miss"]),
    "coin_flip": (tally["coin_flip"]["hit"], tally["coin_flip"]["miss"]),
}
leader = None
best = -1
for k, (h, m) in candidates.items():
    if h + m == 0:
        continue
    r = h / (h + m)
    if r > best:
        best = r
        leader = k

lead_classes = {
    "my_swarm": "{{MY_LEAD}}",
    "opta": "{{OPTA_LEAD}}",
    "coin_flip": "{{COIN_LEAD}}",
}
for k, placeholder in lead_classes.items():
    template = template.replace(placeholder, "lead" if leader == k else "")
template = template.replace("{{KIMI_LEAD}}", "")

template = template.replace("{{MY_REC}}", rec_str(tally["my_swarm"]))
template = template.replace("{{MY_RATE}}", my_rate)
template = template.replace("{{KIMI_REC}}", rec_str(tally["kimi_official"]))
template = template.replace("{{KIMI_RATE}}", kimi_rate)
template = template.replace("{{OPTA_REC}}", rec_str(tally["opta"]))
template = template.replace("{{OPTA_RATE}}", opta_rate)
template = template.replace("{{COIN_REC}}", rec_str(tally["coin_flip"]))
template = template.replace("{{COIN_RATE}}", coin_rate)

template = template.replace("{{ISSUE}}", ISSUE)
template = template.replace("{{DATE_CN}}", DATE_CN)
template = template.replace("{{TICKER}}", f"截至 {REPORT_DATE} · 半决赛间歇日 · 我的小分队 {my_rate} · Opta {opta_rate} · 抛硬币 {coin_rate}")

# ---------- 昨夜复盘 ----------
yesterday = [m for m in ledger["matches"] if m.get("beijing_date") == YESTERDAY_DATE and m.get("status") == "finished"]
yesterday.sort(key=lambda m: m.get("beijing_time", ""))

def result_tag(val):
    return f'<span class="{"hit" if val == "hit" else "miss"}">{"✅" if val == "hit" else "❌"}</span>'

recap_rows = []
for m in yesterday:
    rc = m.get("result_check", {})
    parts = []
    if "my_swarm" in rc:
        parts.append(f"小分队 {result_tag(rc['my_swarm'])}")
    if "opta" in rc and rc["opta"] != "n/a":
        parts.append(f"Opta {result_tag(rc['opta'])}")
    if "kimi_official" in rc and rc["kimi_official"] != "n/a":
        parts.append(f"Kimi {result_tag(rc['kimi_official'])}")
    if "coin_flip" in rc:
        parts.append(f"抛硬币 {result_tag(rc['coin_flip'])}")
    recap_rows.append(f'<div class="row"><span class="sc">{m["home"]} {m["score"]} {m["away"]}</span><span>{" · ".join(parts)}</span></div>')

template = template.replace("{{RECAP_ROWS}}", "\n".join(recap_rows))

# ---------- 今日焦点：半决赛前瞻 ----------
# Today has no matches; preview the two semifinals (Beijing 7/15 & 7/16)
semis = [m for m in ledger["matches"] if m.get("group") == "半决赛" and m.get("status") == "scheduled"]
semis.sort(key=lambda m: m.get("beijing_time", ""))

moon_map = {1: "🌙", 2: "🌙🌙", 3: "🌙🌙🌙", 4: "🌙🌙🌙🌙", 5: "🌙🌙🌙🌙🌙"}
vote_class = {"主队胜": "win", "平": "draw", "客队胜": "lose"}
vote_disp = {"主队胜": "主", "平": "平", "客队胜": "客"}

cards = []
cards.append('<div class="match"><div class="take" style="border-left-color:var(--accent2)">今日北京时间无比赛（半决赛间歇日）。下场焦点为 7/15 与 7/16 凌晨两场半决赛，五人会诊已提前给出投票。</div></div>')

for m in semis:
    pred = m["predictions"]["my_swarm"]
    votes = pred["votes"]
    vote_bars = []
    for role in ["数据", "战术", "伤病", "舆情", "风险官"]:
        v = votes.get(role, "待确认")
        cls = vote_class.get(v, "")
        d = vote_disp.get(v, v)
        vote_bars.append(f'<div class="vote {cls}"><span class="r">{role}</span><span class="v">{d}</span></div>')
    votes_html = "\n    ".join(vote_bars)
    split_html = ""
    if pred.get("split"):
        split_html = '<div class="split">⚠ 五人有分歧：风险官唱反调/存在不同意见</div>'
    stay = m.get("stay_up_index", 1)
    moon = moon_map.get(stay, "🌙" * stay)
    score_pred_clean = m.get("score_pred", "").split("（")[0]
    date_label = m["beijing_time"][:5]  # e.g. 07/15
    cards.append(f'''<div class="match">
  <div class="head">
    <span class="vs">{m["home"]} vs {m["away"]}<span class="grp">{m["group"]}</span></span>
    <span class="time">{date_label} {m["beijing_time"][-5:]}</span>
  </div>
  <div class="stat">
    <span><b>🌙</b><span class="moon">{moon}</span> 熬夜{stay}/5</span>
    <span>比分预测 <b>{score_pred_clean}</b></span>
    <span>关键 <b>{m.get("key_players", "")}</b></span>
  </div>
  <div class="take">{m.get("one_liner", "")}</div>
  <div class="votes">
    {votes_html}
  </div>
  {split_html}
</div>''')

template = template.replace("{{MATCH_CARDS}}", "\n".join(cards))

# ---------- 五人会诊摘要 ----------
role_summary = {
    "数据分析师": "法国 vs 西班牙看法国胜：FIFA #1、6 战 6 胜进 16 失 2，市场隐含胜率 58%–61%；英格兰 vs 阿根廷看英格兰胜：90 分钟盘小幅领先（39% vs 33%），但平局概率 33% 显著，已提示加时/点球尾部。",
    "战术分析师": "法国 vs 西班牙看平：控制 vs 转换的教科书对决，半决赛双方都不敢大举压上，90 分钟平局概率高；英格兰 vs 阿根廷看英格兰胜：阿根廷菱形中场堆中路，英格兰边路宽度+贝林厄姆后插上会在 60 分钟后压垮疲劳阿根廷。",
    "伤病观察员": "法国 vs 西班牙看法国胜：楚阿梅尼可替代、姆巴佩无碍；西班牙尼科·威廉斯/皮诺缺阵、罗德里 ACL 后负荷管理；英格兰 vs 阿根廷看阿根廷胜：赖斯是英格兰不可替代节拍器且带伤+病毒，阿根廷阵容相对齐整。",
    "舆情嘴替": "法国 vs 西班牙看法国胜：舆论 8 成奶法国，西班牙左路缺爆点、亚马尔非满血；英格兰 vs 阿根廷看平：双方都是疲兵，论坛热梗『谁累谁先死』，常规时间大概率 1-1 或 0-0。",
    "风险官": "法国 vs 西班牙看西班牙胜：法国 60% 晋级概率存在大热溢价，西班牙控球消耗+低位防守能把比赛拖住；英格兰 vs 阿根廷看阿根廷胜：英格兰 -135 晋级赔率忽略防线裂缝与阿根廷冠军属性，低比分+加时/点球尾部概率极高。",
}
for role, text in role_summary.items():
    ph = "{{ROLE_" + {
        "数据分析师": "DATA",
        "战术分析师": "TACTIC",
        "伤病观察员": "INJURY",
        "舆情嘴替": "BUZZ",
        "风险官": "RISK",
    }[role] + "}}"
    template = template.replace(ph, text)

# ---------- 今日读图 ----------
vision = (
    "我读了错题本，本次注意了「半决赛阶段回到硬实力/对位/伤停/体能」「55%–65% 小热门仍需设防」「方向看正路、比分守稳、预留加时/点球尾部」三条教训。<br><br>"
    "今日 <code>assets/</code> 目录无新投喂图片（除旧有的 <code>世界杯赛程截图.png</code> 外）。"
    "今天是半决赛间歇日，无比赛截图可读；已用 swarm 五人会诊联网取证填充两场半决赛前瞻。"
)
template = template.replace("{{VISION_BLOCK}}", vision)

# ---------- 建议站队 ----------
template = template.replace("{{PICK_TEAM}}", "法国（7/15 03:00 vs 西班牙）")
template = template.replace("{{PICK_WHY}}", "半决赛五人会诊 3/5 看法国胜，Opta 超算给法国 57.7% 晋级概率；西班牙边路深度受损+罗德里负荷管理，法国多休息一天且转换效率本届最高。")

# ---------- footer ----------
template = template.replace("{{UPDATED_AT}}", f"{REPORT_DATE} {datetime.now().strftime('%H:%M')} 北京")

out_path = ROOT / "reports" / f"日报-{REPORT_DATE}.html"
out_path.write_text(template, encoding="utf-8")
print(f"report written: {out_path}")
