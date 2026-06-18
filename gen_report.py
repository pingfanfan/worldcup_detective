#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate reports/日报-2026-06-18.html from template and ledger."""
import json
from pathlib import Path

ROOT = Path(__file__).parent

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

# determine leader among non-zero rate
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

# kimi has no results, never lead in this dataset
template = template.replace("{{KIMI_LEAD}}", "")

template = template.replace("{{MY_REC}}", rec_str(tally["my_swarm"]))
template = template.replace("{{MY_RATE}}", my_rate)
template = template.replace("{{KIMI_REC}}", rec_str(tally["kimi_official"]))
template = template.replace("{{KIMI_RATE}}", kimi_rate)
template = template.replace("{{OPTA_REC}}", rec_str(tally["opta"]))
template = template.replace("{{OPTA_RATE}}", opta_rate)
template = template.replace("{{COIN_REC}}", rec_str(tally["coin_flip"]))
template = template.replace("{{COIN_RATE}}", coin_rate)

template = template.replace("{{ISSUE}}", "5")
template = template.replace("{{DATE_CN}}", "06月18日")
template = template.replace("{{TICKER}}", f"截至 2026-06-18 · 我的小分队 {my_rate} · Opta {opta_rate} · 抛硬币 {coin_rate}")

# ---------- 昨夜复盘 ----------
day7 = [m for m in ledger["matches"] if m.get("beijing_date") == "2026-06-18" and m.get("status") == "finished"]
# sort by beijing_time
order = {"01:00": 1, "04:00": 2, "07:00": 3, "10:00": 4}
day7.sort(key=lambda m: order.get(m["beijing_time"][-5:], 99))

def result_tag(val):
    return f'<span class="{ "hit" if val == "hit" else "miss"}">{"✅" if val == "hit" else "❌"}</span>'

recap_rows = []
for m in day7:
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
# day8 matches: beijing_date 2026-06-19
moon_map = {1: "🌙", 2: "🌙🌙", 3: "🌙🌙🌙", 4: "🌙🌙🌙🌙", 5: "🌙🌙🌙🌙🌙"}
day8 = [m for m in ledger["matches"] if m.get("beijing_date") == "2026-06-19"]
day8.sort(key=lambda m: m["beijing_time"])

vote_class = {"主队胜": "win", "平": "draw", "客队胜": "lose"}
vote_disp = {"主队胜": "主", "平": "平", "客队胜": "客"}

cards = []
for m in day8:
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
    "数据分析师": "三场看主队小胜（捷克1-0、瑞士2-1、加拿大2-0），墨西哥看1-1平；依据赔率隐含概率、FIFA排名与首轮xG。",
    "战术分析师": "四场一致看主胜：捷克2-1、瑞士1-0、加拿大2-1、墨西哥2-1；强调定位球与转换效率。",
    "伤病观察员": "捷克/瑞士/加拿大主胜，墨西哥1-1平；南非两中场停赛、墨西哥蒙特斯停赛、戴维斯复出状态待确认是最大变量。",
    "舆情嘴替": "媒体前三场一边倒站主胜，墨西哥vs韩国热梗最多；我逆媒体选墨西哥平局，防东道主中卫停赛。",
    "风险官": "四场全唱反调：捷克/瑞士/墨西哥看客队爆冷，加拿大看平；给出28-35%翻车概率作为反向基准。",
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
    "我读了错题本，本次注意了「豪门开局偏紧」「亚洲/大洋洲球队在北美不怯场」「首秀球队低位防守+门将爆种」三条教训。<br><br>"
    "<code>assets/世界杯赛程截图.png</code> 为 ESPN FIFA World Cup Schedule 长截图：<br>"
    "• 已完成：阿根廷 3-0 阿尔及利亚、奥地利 3-1 约旦、葡萄牙 1-1 刚果（金）；英格兰 4-2 克罗地亚。<br>"
    "• 待开赛（北京时间 6/19）：捷克 05:00、瑞士 08:00、加拿大 11:00、墨西哥 14:00。<br>"
    "• 关键信号：葡萄牙再证豪门偏紧；东道主加拿大承压；韩国/墨西哥头名战存疑。"
)
template = template.replace("{{VISION_BLOCK}}", vision)

# ---------- 建议站队 ----------
template = template.replace("{{PICK_TEAM}}", "瑞士")
template = template.replace("{{PICK_WHY}}", "五人会诊四票主胜，Opta 超算给瑞士胜 61.6%；波黑后防与锋线同时缺人，瑞士主场（洛杉矶）经验与结构占优。")

# ---------- footer ----------
template = template.replace("{{UPDATED_AT}}", "2026-06-18 15:00 北京")

out_path = ROOT / "reports" / "日报-2026-06-18.html"
out_path.write_text(template, encoding="utf-8")
print(f"report written: {out_path}")
