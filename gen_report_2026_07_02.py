#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 2026-07-02 世界杯 AI 球探日报 HTML"""
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
ledger_path = ROOT / "data" / "ledger.json"
template_path = ROOT / "templates" / "report-template.html"
output_path = ROOT / "reports" / "日报-2026-07-02.html"

with open(ledger_path, "r", encoding="utf-8") as f:
    ledger = json.load(f)

with open(template_path, "r", encoding="utf-8") as f:
    html = f.read()

# ---- 战绩 ----
my = ledger["tally"]["my_swarm"]
kimi = ledger["tally"]["kimi_official"]
opta = ledger["tally"]["opta"]
coin = ledger["tally"]["coin_flip"]

my_total = my["hit"] + my["miss"]
kimi_total = kimi["hit"] + kimi["miss"]
opta_total = opta["hit"] + opta["miss"]
coin_total = coin["hit"] + coin["miss"]

my_rate = f"{my['hit']/my_total*100:.1f}%" if my_total else "0.0%"
kimi_rate = f"{kimi['hit']/kimi_total*100:.1f}%" if kimi_total else "0.0%"
opta_rate = f"{opta['hit']/opta_total*100:.1f}%" if opta_total else "0.0%"
coin_rate = f"{coin['hit']/coin_total*100:.1f}%" if coin_total else "0.0%"

# 谁领先（按命中率）
leaders = []
for name, total, hit in [("my", my_total, my["hit"]), ("kimi", kimi_total, kimi["hit"]), ("opta", opta_total, opta["hit"])]:
    if total:
        leaders.append((name, hit/total))
lead = max(leaders, key=lambda x: x[1])[0] if leaders else ""

my_lead = "lead" if lead == "my" else ""
kimi_lead = "lead" if lead == "kimi" else ""
opta_lead = "lead" if lead == "opta" else ""

# ---- 复盘行 ----
recap_rows = """    <div class="row"><span class="sc">英格兰 2-1 刚果（金）</span><span class="hit">小分队 ✅ · Opta ✅</span></div>
    <div class="row"><span class="sc">比利时 3-2 塞内加尔（AET）</span><span class="hit">小分队 ✅ · Opta ✅</span></div>
    <div class="row"><span class="sc">美国 2-0 波黑</span><span class="hit">小分队 ✅ · Opta ✅ · 抛硬币 ✅</span></div>"""

# ---- 比赛卡片 ----
matches = ledger["matches"]
today_matches = [m for m in matches if m.get("date") == "2026-07-02" and m.get("beijing_date") == "2026-07-03"]

def moon(n):
    return "🌙" * n

def vote_class(v):
    if "主" in v or "胜" in v and "客" not in v:
        return "win"
    if "客" in v:
        return "lose"
    return "draw"

def vote_abbr(v):
    if "主" in v:
        return "主"
    if "客" in v:
        return "客"
    return "平"

cards = []
for m in today_matches:
    votes = m["predictions"]["my_swarm"]["votes"]
    final = m["predictions"]["my_swarm"]["final"]
    split = m["predictions"]["my_swarm"]["split"]
    vote_html = "\n".join([
        f'      <div class="vote {vote_class(v)}"><span class="r">{k}</span><span class="v">{vote_abbr(v)}</span></div>'
        for k, v in votes.items()
    ])
    split_html = '<div class="split">⚠ 五人有分歧：风险官' + ("看客胜" if votes.get("风险官") == "客队胜" else "看平") + "，其余四票主队胜</div>" if split else ""
    stay = m.get("stay_up_index", 3)
    card = f"""  <div class="match">
    <div class="head">
      <span class="vs">{m['home']} vs {m['away']}<span class="grp">{m['group']}</span></span>
      <span class="time">{m['beijing_time']}</span>
    </div>
    <div class="stat">
      <span><b>🌙</b><span class="moon">{moon(stay)}</span> 熬夜{stay}/5</span>
      <span>比分预测 <b>{m['score_pred'].split('（')[0]}</b></span>
      <span>关键 <b>{m['key_players'].split('；')[0].replace('（西班牙）','').replace('（葡萄牙）','').replace('（瑞士）','')}</b></span>
    </div>
    <div class="take">{m['one_liner']}。</div>
    <div class="votes">
{vote_html}
    </div>
{split_html}
  </div>"""
    cards.append(card)

match_cards = "\n".join(cards)

# ---- 五人会诊摘要 ----
role_data = "三场全部看主队胜。西班牙 xG 7.93/0 失球、盘口隐含胜率约 75%；葡萄牙 FIFA 第 5、历史交锋 7 胜 1 负；瑞士场均 xG 2.7+，阿尔及利亚 3 场丢 7 球。比分全部守 2-0/2-1，不追大胜。"
role_tactic = "三场全部看主队胜但强调比分收敛。西班牙尼科·威廉斯与皮诺伤缺导致宽度不足；葡萄牙 vs 克罗地亚是今天加时/点球风险最高的一场；瑞士结构占优但淘汰赛 90 分钟追分能力历史偏弱。"
role_injury = "三场全部看主队胜。西班牙边路三人伤停但亚马尔回归、中场完整；葡萄牙无新增伤病；瑞士维德默髋部伤疑但雅凯已证明可顶替。"
role_buzz = "三场全部看主队胜。西班牙‘零封滤镜’仍在但网友担心破密集乏力；葡萄牙 vs 克罗地亚‘诸神黄昏’情怀站克罗地亚、理性站葡萄牙；瑞士黑马叙事缺乏硬数据支撑。"
role_risk = "西班牙看平（翻车概率 35%），葡萄牙看平（38%），瑞士直接看客胜（42%）。核心逻辑：淘汰赛不要把‘晋级概率’等同于‘90 分钟胜率’，65% 以上深盘要降档。"

# ---- 视觉 ----
vision = "assets/ 目录中仍为 6 月 17 日的 ESPN 小组赛赛程截图，覆盖 6/17–6/23 小组赛对阵、时间、场地与转播信息。该图为历史赛程参考，不直接用于今日淘汰赛预测；但其显示的多城长途飞行、不同场地草皮类型提醒体能与适应性在淘汰赛中的权重上升。今日无新图投喂。"

# ---- 站队 ----
pick_team = "西班牙"
pick_why = "三场中数据面最稳的热门：小组赛 0 失球、xG 7.93、FIFA 第 2，奥地利防线 3 场丢 6 球。尽管风险官提醒 75% 隐含胜率存在深盘溢价，但西班牙结构优势最明显，方向最明确。Token Cup 选队优先‘方向明确+深盘不过热’，本场符合条件。"

# ---- 替换 ----
replacements = {
    "{{ISSUE}}": "18",
    "{{DATE_CN}}": "2026 年 7 月 2 日",
    "{{MY_REC}}": f"{my['hit']}-{my['miss']}",
    "{{MY_RATE}}": my_rate,
    "{{MY_LEAD}}": my_lead,
    "{{KIMI_REC}}": f"{kimi['hit']}-{kimi['miss']}",
    "{{KIMI_RATE}}": kimi_rate,
    "{{KIMI_LEAD}}": kimi_lead,
    "{{OPTA_REC}}": f"{opta['hit']}-{opta['miss']}",
    "{{OPTA_RATE}}": opta_rate,
    "{{OPTA_LEAD}}": opta_lead,
    "{{COIN_REC}}": f"{coin['hit']}-{coin['miss']}",
    "{{COIN_RATE}}": coin_rate,
    "{{TICKER}}": f"我的小分队 {my['hit']}-{my['miss']}（{my_rate}）暂领跑；淘汰赛连续命中后命中率回升。",
    "{{RECAP_ROWS}}": recap_rows,
    "{{MATCH_CARDS}}": match_cards,
    "{{ROLE_DATA}}": role_data,
    "{{ROLE_TACTIC}}": role_tactic,
    "{{ROLE_INJURY}}": role_injury,
    "{{ROLE_BUZZ}}": role_buzz,
    "{{ROLE_RISK}}": role_risk,
    "{{VISION_BLOCK}}": vision,
    "{{PICK_TEAM}}": pick_team,
    "{{PICK_WHY}}": pick_why,
    "{{UPDATED_AT}}": datetime.now().strftime("%Y-%m-%d %H:%M 北京"),
}

for k, v in replacements.items():
    html = html.replace(k, v)

# 清理未替换的占位符
import re
html = re.sub(r"\{\{[A-Z_]+\}\}", "", html)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"日报已生成：{output_path}")
