#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate reports/日报-2026-07-08.html from template and ledger."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).parent
REPORT_DATE = "2026-07-08"
YESTERDAY_DATE = "2026-07-07"
ISSUE = "24"
DATE_CN = "07月08日"

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
today = [m for m in ledger["matches"] if m.get("beijing_date") == REPORT_DATE and m.get("status") == "scheduled"]
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
    cards.append(f'''<div class="match">
  <div class="head">
    <span class="vs">{m["home"]} vs {m["away"]}<span class="grp">{m["group"]}组</span></span>
    <span class="time">{m["beijing_time"][-5:]}</span>
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
    "数据分析师": "阿根廷 Opta 69.6% 主胜，FIFA 排名与 xG 全面占优，但 120 分钟消耗和埃及反击让比分守稳 2-1；瑞士 vs 哥伦比亚为均势局，Dimers/市场略看好哥伦比亚，平局概率近 30%，看哥伦比亚 1-0 小胜。",
    "战术分析师": "阿根廷 4-3-3/4-4-2 切换，梅西自由人 vs 埃及 4-2-3-1 低位铁桶，埃及左路防线残缺是通道；瑞士 4-2-3-1 组织纪律 vs 哥伦比亚 4-3-3 迪亚斯左路爆破，Manzambi 缺阵削弱瑞士转换。",
    "伤病观察员": "阿根廷梅西、恩佐、Medina、冈萨雷斯均带疲劳/小伤；埃及 Fatouh/Abdelmonem 带伤，Salah 腿筋存疑。瑞士 Manzambi 膝伤缺阵、Aebischer/Jaquez 肌肉成疑；哥伦比亚 Córdoba 报销、J罗状态成谜。",
    "舆情嘴替": "社媒把阿根廷 vs 埃及刷成‘梅西第八球纪录夜 vs Salah 复仇’，深盘情绪溢价高；瑞士‘破咒+Manzambi 流量’对阵哥伦比亚铁桶+迪亚斯，机构客胜 2.26 说明情绪未一边倒。",
    "风险官": "阿根廷 69.6% 深盘+最短轮转+疲劳，45% 翻车概率，投平；哥伦比亚小热但 Córdoba 报销、J罗 0 球 0 助、进攻只剩迪亚斯，40% 翻车概率，投瑞士 1-0。",
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
    "我读了错题本，本次注意了「淘汰赛比分守稳不追大胜」「深盘 65%+ 热门需主动降档」「出席≠状态」「东道主淘汰赛光环已被证伪」四条教训。<br><br>"
    "<code>assets/</code> 目录没有今天（7 月 8 日）比赛专属图片；现有 <code>assets/世界杯赛程截图.png</code> 为 6 月 17–23 日 ESPN 赛程长截图，未覆盖今日两场。<br><br>"
    "今日读图结论：无新图，日报使用 swarm 联网取证数据填充。"
)
template = template.replace("{{VISION_BLOCK}}", vision)

# ---------- 建议站队 ----------
template = template.replace("{{PICK_TEAM}}", "阿根廷")
template = template.replace("{{PICK_WHY}}", "五人会诊四票看好阿根廷（数据/战术/伤病/舆情主胜，仅风险官看平）；Opta 给出 69.6% 90 分钟胜率，埃及后防多人带伤且阿根廷阵容深度可缓冲疲劳，是今日信心最高的一场。")

# ---------- footer ----------
beijing_now = datetime.now(timezone.utc) + timedelta(hours=8)
template = template.replace("{{UPDATED_AT}}", beijing_now.strftime("%Y-%m-%d %H:%M 北京"))

out_path = ROOT / "reports" / f"日报-{REPORT_DATE}.html"
out_path.write_text(template, encoding="utf-8")
print(f"report written: {out_path}")
