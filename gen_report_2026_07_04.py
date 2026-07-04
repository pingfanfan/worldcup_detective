#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate reports/日报-2026-07-04.html from template and ledger."""
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
REPORT_DATE = "2026-07-04"
YESTERDAY_DATE = "2026-07-03"
ISSUE = "20"
DATE_CN = "07月04日"

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

# ---------- 今日焦点（已完成） ----------
moon_map = {1: "🌙", 2: "🌙🌙", 3: "🌙🌙🌙", 4: "🌙🌙🌙🌙", 5: "🌙🌙🌙🌙🌙"}
today = [m for m in ledger["matches"] if m.get("beijing_date") == REPORT_DATE and m.get("status") == "finished"]
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
    actual_score = m.get("score", "")
    cards.append(f'''<div class="match">
  <div class="head">
    <span class="vs">{m["home"]} vs {m["away"]}<span class="grp">{m["group"]}</span></span>
    <span class="time">{m["beijing_time"][-5:]} · 赛果 {actual_score}</span>
  </div>
  <div class="stat">
    <span><b>🌙</b><span class="moon">{moon}</span> 熬夜{stay}/5</span>
    <span>赛前预测 <b>{score_pred_clean}</b></span>
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
    "数据分析师": "三场方向 2/3（阿根廷、哥伦比亚最终方向对；埃及 90 分钟客胜错），比分 0/3；xG 与盘口均指向热门，但淘汰赛门将爆种+点球尾部压缩了实际比分。",
    "战术分析师": "哥伦比亚 1-0 剧本完全命中；阿根廷方向对但 2-0 被拖入加时；澳大利亚把埃及拖入点球超出预期。核心教训：淘汰赛必须区分「90 分钟」与「最终晋级」口径。",
    "伤病观察员": "萨拉赫带伤首发但状态打折，埃及攻坚效率骤降；佛得角 Arcanjo 缺阵但 Cabral 复出进球；加纳 Kudus 整届缺阵。伤病出席≠状态满格。",
    "舆情嘴替": "赛前中文论坛看澳埃僵持、阿根廷小胜、哥伦比亚 1-0；赛后 Vozinha 封神、梅西世界杯第 20 球、埃及首进 16 强成最热话题。",
    "风险官": "阿根廷 90 分钟闷平反向基准完全应验；澳大利亚拖入点球部分应验但结果押澳大利亚落空；哥伦比亚 1-0 直接解决战斗反向落空。反向基准应识别结构脆弱性而非机械押冷。",
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
    "我读了错题本，本次注意了「淘汰赛 90 分钟与最终晋级口径要分开」「深盘 65%+ 需降档不追大胜」「低位铁桶+门将爆种压缩比分」三条教训。<br><br>"
    "<code>assets/世界杯赛程截图.png</code> 为 ESPN 赛程长截图，内容未覆盖 7/4 当日三场；assets 目录今日无新投喂图片。<br><br>"
    "今日读图结论：无新图可分析，日报使用 swarm 联网核验数据与赛后统计填充。"
)
template = template.replace("{{VISION_BLOCK}}", vision)

# ---------- 建议站队 ----------
template = template.replace("{{PICK_TEAM}}", "今日无新开赛事")
template = template.replace("{{PICK_WHY}}", "北京时间 7 月 4 日三场 1/16 决赛已全部结束；1/8 决赛将于 7 月 5 日开打，建议待明日日报给出 Token Cup 站队。")

# ---------- footer ----------
template = template.replace("{{UPDATED_AT}}", f"{REPORT_DATE} {datetime.now().strftime('%H:%M')} 北京")

out_path = ROOT / "reports" / f"日报-{REPORT_DATE}.html"
out_path.write_text(template, encoding="utf-8")
print(f"report written: {out_path}")
