#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate reports/日报-2026-07-10.html from template and ledger."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).parent
REPORT_DATE = "2026-07-10"
RECAP_BEIJING_DATE = "2026-07-10"  # 昨夜复盘：法国 vs 摩洛哥
MATCH_BEIJING_DATE = "2026-07-11"  # 今日焦点：西班牙 vs 比利时
ISSUE = "26"
DATE_CN = "2026年7月10日"

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
template = template.replace("{{TICKER}}", f"昨夜1/4决赛揭幕：法国2-0摩洛哥，姆巴佩、登贝莱建功")

# ---------- 昨夜复盘 ----------
yesterday = [m for m in ledger["matches"] if m.get("beijing_date") == RECAP_BEIJING_DATE and m.get("status") == "finished"]
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
    # 处理点球/加时备注
    score_display = m["score"]
    recap_rows.append(f'<div class="row"><span class="sc">{m["home"]} {score_display} {m["away"]}</span><span>{" · ".join(parts)}</span></div>')

template = template.replace("{{RECAP_ROWS}}", "\n".join(recap_rows))

# ---------- 今日焦点 ----------
moon_map = {1: "🌙", 2: "🌙🌙", 3: "🌙🌙🌙", 4: "🌙🌙🌙🌙", 5: "🌙🌙🌙🌙🌙"}
today = [m for m in ledger["matches"] if m.get("beijing_date") == MATCH_BEIJING_DATE and m.get("status") == "scheduled"]
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
        split_html = '<div class="split">⚠ 五人有分歧：风险官看客胜</div>'
    stay = m.get("stay_up_index", 1)
    moon = moon_map.get(stay, "🌙" * stay)
    score_pred_clean = m.get("score_pred", "").split("（")[0]
    cards.append(f'''<div class="match">
  <div class="head">
    <span class="vs">{m["home"]} vs {m["away"]}<span class="grp">{m["group"]} 决赛</span></span>
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
    "数据分析师": "Opta 西班牙 59.3% / 市场隐含约 62%，轻微热度溢价但未入深盘；西班牙 xGA 0.30/场+近 11 场 H2H 9 胜 2 平；比利时 4-1 美国存在门将送礼与空门水分。方向西班牙，比分 2-0。",
    "战术分析师": "西班牙 4-3-3 控球折磨 vs 比利时 4-2-3-1 中低位转换；Rodri/Pedri 控制中场，但 Onana 缺阵让比利时绞杀能力下降；多库/Trossard 对波罗身后是最大威胁。方向西班牙，比分 2-1，翻车概率 30%。",
    "伤病观察员": "西班牙 Pino 锁骨报销、Nico Williams 内收肌 doubtful，但核心中轴完整；比利时 Onana ACL 报销、Debast 腿伤疑、De Bruyne/Lukaku 状态受限。伤病天平倾向西班牙，比分 1-0/2-1。",
    "舆情嘴替": "论坛西班牙'零封滤镜'拉满，机构一面倒推荐 Spain win to nil；但'比利时 4-1 美国是卖高还是买涨'吵翻，Onana 报销后 Vanaken 上位反而被玩梗。舆论总体站西班牙，比分 1-0。",
    "风险官": "西班牙 59.3% 胜率+5 场零封已被市场定价过热，左路 Pino/Williams 伤缺削弱破密集效率；比利时 4-1 美国有送礼成分但次核状态在线。1986 年 1/4 决赛比利时曾点球淘汰西班牙。看客胜，比分 0-1，翻车概率约 40%。",
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
    "我读了错题本，本次注意了「淘汰赛 55%–65% 小热门必须设防」「90 分钟+点球结构压缩热门优势」「比利时核心'替补'不等于'断电'」三条教训。<br><br>"
    "<code>assets/</code> 目录今天没有新投喂的图片（仅有早期赛程截图）。如需读图，请将赛程/战术/海报图片拖入 assets/ 文件夹。<br><br>"
    "今日读图结论：无新图，日报使用 swarm 联网取证数据填充。"
)
template = template.replace("{{VISION_BLOCK}}", vision)

# ---------- 建议站队 ----------
template = template.replace("{{PICK_TEAM}}", "西班牙")
template = template.replace("{{PICK_WHY}}", "五人会诊四票主胜、仅风险官看客胜；Opta 给出 59.3% 90 分钟胜率，比利时中场屏障 Onana ACL 报销+Debast 伤疑，西班牙控制流核心 intact。但本场处于 55%–65% 小热门区间，比分守稳 1-0，预留加时/点球尾部概率。")

# ---------- footer ----------
beijing_now = datetime.now(timezone.utc) + timedelta(hours=8)
template = template.replace("{{UPDATED_AT}}", beijing_now.strftime("%Y-%m-%d %H:%M 北京"))

out_path = ROOT / "reports" / f"日报-{REPORT_DATE}.html"
out_path.write_text(template, encoding="utf-8")
print(f"report written: {out_path}")
