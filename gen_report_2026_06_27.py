#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate reports/日报-2026-06-27.html from template and ledger."""
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
REPORT_DATE = "2026-06-27"
YESTERDAY_DATE = "2026-06-26"
ISSUE = "13"
DATE_CN = "06月27日"

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
# NOTE: matches on REPORT_DATE are already finished by system time, but we still render them as "today focus"
# and append the actual score line for transparency.
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
    "数据分析师": "四场清晰实力差（法国、塞内加尔、西班牙、比利时）按赔率+xG指向正路并命中；佛得角与埃及两场数据最接近，过度相信主队纸面优势，忽视了「首秀球队第三轮体能拐点」与「打平即可出线球队主动降速」的结构信号。",
    "战术分析师": "从阵型克制看，法国边路压制挪威、塞内加尔冲击伊拉克、西班牙破乌拉圭高位、比利时围攻新西兰均符合推演；佛得角与埃及两场因双方同时缺乏进攻锐度、形成低位僵持而被闷平。",
    "伤病观察员": "5/6。准确识别埃及-伊朗双方核心带伤、节奏保守而看平；唯一失误是佛得角，虽列出其防线伤停，但低估了沙特同样缺乏破密集能力导致的互相僵持。",
    "舆情嘴替": "舆论一边倒看好法国、塞内加尔、西班牙、比利时，舆情角色跟随主流并命中四场；佛得角「励志剧本」与埃及「打平即出线」两场的舆情热度被过度解读，实际比赛节奏向防守方倾斜。",
    "风险官": "本轮仅命中埃及-伊朗闷平；对四场深盘/热门看平均未应验，说明在战意明确、实力差距悬殊的场次中，单纯「防闷平」的反调价值有限；但对佛得角与埃及两场的警示仍值得保留。",
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
    "我读了错题本，本次注意了「首秀球队低位奇迹有保质期」「打平即可出线的热门会主动降速」「深盘热门战意明确时仍可走正路」三条教训。<br><br>"
    "<code>assets/世界杯赛程截图.png</code> 为 ESPN FIFA World Cup Schedule 长截图，但截图时间较早，仅覆盖到 6 月 23 日（美国时间）的比赛，"
    "未包含本轮（北京时间 6 月 27 日）G/H/I 组六场。<br><br>"
    "今日读图结论：assets 目录当前无 6/27 比赛专属截图/海报，日报使用 swarm 联网取证数据填充。"
)
template = template.replace("{{VISION_BLOCK}}", vision)

# ---------- 建议站队 ----------
template = template.replace("{{PICK_TEAM}}", "西班牙")
template = template.replace("{{PICK_WHY}}", "五人会诊四票客胜、仅风险官看平；西班牙控球与边路优势明显，乌拉圭残阵背水一战，是今日结构最清晰的正路场次之一。")

# ---------- footer ----------
template = template.replace("{{UPDATED_AT}}", f"{REPORT_DATE} {datetime.now().strftime('%H:%M')} 北京")

out_path = ROOT / "reports" / f"日报-{REPORT_DATE}.html"
out_path.write_text(template, encoding="utf-8")
print(f"report written: {out_path}")
