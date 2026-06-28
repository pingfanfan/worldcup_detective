#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate reports/日报-2026-06-28.html from template and ledger."""
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
REPORT_DATE = "2026-06-28"
YESTERDAY_DATE = "2026-06-27"
ISSUE = "14"
DATE_CN = "06月28日"

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
    "数据分析师": "6 中 5。四票实力差（英格兰、克罗地亚、刚果金、阿根廷）按赔率+xG命中；阿尔及利亚-奥地利按赔率与xG持平看平命中；唯一漏判是哥伦比亚-葡萄牙，低估了‘打平即锁头名’带来的结构性保守。",
    "战术分析师": "4/6。命中英格兰客胜、哥伦比亚闷平、刚果金主胜、阿根廷客胜；漏判克罗地亚2-1加纳（看平）与阿尔及利亚3-3奥地利（看客胜）。 Croatia 定位球/二点效率、Algeria 反击爆发超出战术推演。",
    "伤病观察员": "5/6。命中英格兰、克罗地亚、哥伦比亚闷平、刚果金、阿根廷；漏判阿尔及利亚-奥地利——低估了 Amoura 缺阵后 Mahrez 等人的进攻上限，也高估了奥地利带伤防线的稳定性。",
    "舆情嘴替": "6/6 全中。舆论热度与盘口结构成为核心信号：英格兰/克罗地亚/刚果金/阿根廷跟随主流；哥伦比亚-葡萄牙 public 投注 94% 站葡萄牙，过热后看平；阿尔及利亚- Austria 舆论一边倒押奥地利，看平/对攻。",
    "风险官": "2/6，命中哥伦比亚闷平与阿尔及利亚-奥地利平局。反调在英格兰、克罗地亚、刚果金、阿根廷四场未应验，说明当热门战意明确、对手无实质威胁时，机械押冷价值有限；但识别结构脆弱性（65%+深盘、已出线轮换）仍有效。",
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
    "我读了错题本，本次注意了「第三轮算分战要优先看结构信号」「深盘热门仍需降档」「已出线豪门轮换不等于放水」三条教训。<br><br>"
    "<code>assets/世界杯赛程截图.png</code> 为 6 月 17 日保存的 ESPN 赛程长截图，未覆盖本轮（北京时间 6/28）J/K/L 组六场；"
    "本轮使用 swarm 联网取证与 ESPN/Fox Sports 官方赛果填充。<br><br>"
    "今日读图结论：assets 目录当前无 6/28 比赛专属截图/海报；小组赛已收官，明日进入 1/16 决赛阶段。"
)
template = template.replace("{{VISION_BLOCK}}", vision)

# ---------- 建议站队 ----------
template = template.replace("{{PICK_TEAM}}", "小组赛收官 · 淘汰赛再选")
template = template.replace("{{PICK_WHY}}", "J/K/L 组第三轮已全部结束，我的小分队 6/6 全中。下一轮 1/16 决赛将于北京时间 6/29 开打（南非 vs 加拿大），明日将根据对阵形势、黄牌停赛与体能数据重新选队。")

# ---------- footer ----------
template = template.replace("{{UPDATED_AT}}", f"{REPORT_DATE} {datetime.now().strftime('%H:%M')} 北京")

out_path = ROOT / "reports" / f"日报-{REPORT_DATE}.html"
out_path.write_text(template, encoding="utf-8")
print(f"report written: {out_path}")
