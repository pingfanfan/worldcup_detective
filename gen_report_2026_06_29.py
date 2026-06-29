#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate reports/日报-2026-06-29.html from template and ledger."""
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
REPORT_DATE = "2026-06-29"
YESTERDAY_DATE = "2026-06-28"
ISSUE = "15"
DATE_CN = "06月29日"

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
template = template.replace("{{TICKER}}", f"截至 {REPORT_DATE} · 我的小分队 {my_rate} · Opta {opta_rate} · 抛硬币 {coin_rate}")

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

# ---------- 今日焦点 ----------
moon_map = {1: "🌙", 2: "🌙🌙", 3: "🌙🌙🌙", 4: "🌙🌙🌙🌙", 5: "🌙🌙🌙🌙🌙"}
today = [m for m in ledger["matches"] if m.get("beijing_date") == REPORT_DATE]
today.sort(key=lambda m: m.get("beijing_time", ""))

vote_class = {"主队胜": "win", "平": "draw", "客队胜": "lose"}
vote_disp = {"主队胜": "主", "平": "平", "客队胜": "客"}

cards = []
for m in today:
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
    actual_line = f"<b>实际赛果</b> {m['home']} {m['score']} {m['away']}"
    cards.append(f'''<div class="match">
  <div class="head">
    <span class="vs">{m["home"]} vs {m["away"]}<span class="grp">{m["group"]}组</span></span>
    <span class="time">{m["beijing_time"][-5:]}</span>
  </div>
  <div class="stat">
    <span><b>🌙</b><span class="moon">{moon}</span> 熬夜{stay}/5</span>
    <span>比分预测 <b>{score_pred_clean}</b></span>
    <span>{actual_line}</span>
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
    "数据分析师": "按赔率+FIFA排名+xG，加拿大是55–60%的小热门而非深盘；Jonathan David与完整锋线决定上限，预测加拿大1-0或2-1。",
    "战术分析师": "加拿大高位逼抢+边路爆破对南非低位铁桶，Davies存疑削弱破密效率；南非反击有限，预计加拿大控制节奏后2-1小胜。",
    "伤病观察员": "加拿大科内报销、Davies大概率替补、Eustaquio带伤，但锋线完整；南非Zwane停赛、Mokoena复出，防线纪律性强。方向看客胜，比分1-2。",
    "舆情嘴替": "舆论70%站加拿大，最热比分0-1/1-2；也弥漫「南非低位铁桶+Williams爆种」的防冷叙事。综合舆情看加拿大小胜晋级。",
    "风险官": "给出40%翻车概率，看平/闷平。核心逻辑：加拿大伤病+首次离开本土远征、南非光脚不怕穿鞋，淘汰赛可能复制「围攻无果」剧本。",
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
    "我读了错题本，本次注意了「淘汰赛阶段回到硬实力判断」「非洲球队低位防守+门将爆种仍是有效信号」「赔率55–60%小热门需降档但不机械押冷」三条教训。<br><br>"
    "<code>assets/世界杯赛程截图.png</code> 为 6 月 17 日保存的 ESPN 赛程长截图，内容覆盖至小组赛中期，未包含本轮（北京时间 6/28–6/29）的 J/K/L 组末轮与 1/16 决赛对阵；"
    "今日读图未获得新投喂的比赛专属截图/海报，使用 swarm 联网取证与 Fox Sports 官方赛果填充。"
)
template = template.replace("{{VISION_BLOCK}}", vision)

# ---------- 建议站队 ----------
template = template.replace("{{PICK_TEAM}}", "加拿大")
template = template.replace("{{PICK_WHY}}", "五人会诊四票客胜、仅风险官看平；南非进攻产量本届最低，加拿大有David/Larin终结点，东道主硬实力更胜一筹。实际赛果0-1绝杀验证方向。")

# ---------- footer ----------
template = template.replace("{{UPDATED_AT}}", f"{REPORT_DATE} {datetime.now().strftime('%H:%M')} 北京")

out_path = ROOT / "reports" / f"日报-{REPORT_DATE}.html"
out_path.write_text(template, encoding="utf-8")
print(f"report written: {out_path}")
