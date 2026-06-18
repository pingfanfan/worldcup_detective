#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界杯 AI 球探 · 网站生成器
读取 data/ledger.json 和 reports/ 下的历史日报，生成 GitHub Pages 静态站点到 site/。
每天 run.sh 跑完会调用它，再 git push。
"""
import json, os, re, shutil, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
LEDGER = os.path.join(ROOT, "data", "ledger.json")
REPORTS = os.path.join(ROOT, "reports")

def load_ledger():
    with open(LEDGER, encoding="utf-8") as f:
        return json.load(f)

def pct(hit, miss):
    tot = hit + miss
    return round(hit / tot * 100) if tot else None

def rate_str(d):
    p = pct(d["hit"], d["miss"])
    return f"{p}%" if p is not None else "—"

def fmt_vote(v):
    if not v: return ("draw", "?")
    if "主队胜" in v or v.endswith("胜") and "客" not in v: cls, t = "win", "主"
    elif "客队胜" in v: cls, t = "lose", "客"
    elif "平" in v: cls, t = "draw", "平"
    else: cls, t = "win", v[:1]
    if "主" in v: cls, t = "win", "主"
    if "客" in v: cls, t = "lose", "客"
    return (cls, t)

def build():
    d = load_ledger()
    tally = d["tally"]
    matches = d["matches"]

    # 找历史日报（按日期倒序）
    report_files = sorted(glob.glob(os.path.join(REPORTS, "日报-*.html")), reverse=True)
    report_dates = []
    for rf in report_files:
        m = re.search(r"日报-(\d{4}-\d{2}-\d{2})", os.path.basename(rf))
        if m: report_dates.append(m.group(1))
    latest_date = report_dates[0] if report_dates else None

    # 今日待赛（取最近一个有 scheduled 的日期）
    sched = [m for m in matches if m["status"] == "scheduled"]
    sched_dates = sorted({m.get("beijing_date", "") for m in sched})
    today_bj = sched_dates[0] if sched_dates else None
    today_matches = [m for m in sched if m.get("beijing_date") == today_bj] if today_bj else []

    # 昨夜复盘（最近完赛的几场）
    finished = [m for m in matches if m["status"] == "finished" and m.get("score")]
    recap = finished[-6:][::-1]

    os.makedirs(SITE, exist_ok=True)

    # ---- 记分牌 ----
    board = []
    rows = [("我的小分队", "my_swarm", "me"), ("Opta 超算", "opta", "opta"),
            ("抛硬币", "coin_flip", "coin"), ("Kimi 官方", "kimi_official", "kimi")]
    leader = max(["my_swarm", "opta", "coin_flip"], key=lambda k: pct(tally[k]["hit"], tally[k]["miss"]) or -1)
    for name, key, cls in rows:
        t = tally[key]
        lead = " lead" if key == leader else ""
        rec = f'{t["hit"]}胜{t["miss"]}负' if (t["hit"] + t["miss"]) else "—"
        board.append(f'''<div class="sb {cls}{lead}"><div class="who">{name}</div>
          <div class="rec">{rec}</div><div class="rate">{rate_str(t)}</div></div>''')

    # ---- 今日比赛卡片 ----
    cards = []
    for m in today_matches:
        p = m.get("predictions", {})
        sw = p.get("my_swarm", {})
        votes = sw.get("votes", {}) if isinstance(sw, dict) else {}
        split = sw.get("split") if isinstance(sw, dict) else False
        moon = "🌙" * int(m.get("stay_up_index", 0) or 0)
        vbar = ""
        order = [("数据", "数据"), ("战术", "战术"), ("伤病", "伤病"), ("舆情", "舆情"), ("风险官", "风险")]
        for k, lab in order:
            cls, t = fmt_vote(votes.get(k, ""))
            vbar += f'<div class="vote {cls}"><span class="r">{lab}</span><span class="v">{t}</span></div>'
        split_html = '<div class="split">⚠ 五人有分歧</div>' if split else ''
        opta = p.get("opta", "")
        opta_html = f'<span class="opta-tag">Opta {opta}</span>' if opta and opta != "待确认" else ''
        cards.append(f'''<div class="match">
          <div class="mhead"><span class="vs">{m["home"]} vs {m["away"]}<span class="grp">{m.get("group","")}组</span></span>
            <span class="time">{m.get("beijing_time","")}</span></div>
          <div class="mstat"><span class="moon">{moon}</span> 熬夜{m.get("stay_up_index","?")}/5
            <span class="sep">·</span> 预测 <b>{m.get("score_pred","—")}</b>
            <span class="sep">·</span> {m.get("key_players","")}</div>
          <div class="take">{m.get("one_liner","")}</div>
          <div class="votes">{vbar}</div>{split_html}{opta_html}</div>''')
    if not cards:
        cards.append('<div class="match"><div class="take">今日暂无待赛场次，等下一批赛程。</div></div>')

    # ---- 昨夜复盘 ----
    recap_rows = ""
    for m in recap:
        p = m.get("predictions", {})
        sw = p.get("my_swarm", {})
        rc = m.get("result_check", {})
        my = rc.get("my_swarm", "")
        mark = '<span class="hit">✅</span>' if my == "hit" else ('<span class="miss">🤡</span>' if my == "miss" else '')
        recap_rows += f'<div class="rrow"><span class="sc">{m["home"]} {m["score"]} {m["away"]}</span>{mark}</div>'

    # ---- 历史归档 ----
    archive = ""
    for dt in report_dates:
        archive += f'<a class="arch-item" href="reports/日报-{dt}.html">📋 {dt} 日报</a>'

    pick = d.get("token_account", {}).get("daily_pick", {})
    pick_team = pick.get("team", "—")

    html = TEMPLATE.format(
        title=d["meta"]["title"],
        latest_date=latest_date or "—",
        board="".join(board),
        cards="".join(cards),
        recap_rows=recap_rows or '<div class="rrow"><span class="sc">暂无复盘</span></div>',
        archive=archive or "暂无历史日报",
        pick_team=pick_team,
        n_finished=len([m for m in matches if m["status"] == "finished"]),
        my_rate=rate_str(tally["my_swarm"]),
        opta_rate=rate_str(tally["opta"]),
    )
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    # 拷贝历史日报和图到 site/，让归档链接可点
    out_reports = os.path.join(SITE, "reports")
    os.makedirs(out_reports, exist_ok=True)
    for rf in report_files:
        shutil.copy(rf, out_reports)
    # 日报里引用的 PNG 也带上
    for png in glob.glob(os.path.join(REPORTS, "*.png")):
        shutil.copy(png, out_reports)

    print(f"✅ 站点生成完成 → {SITE}/index.html（{len(report_dates)} 期历史日报）")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="一个用 Kimi Code 搭的世界杯 AI 球探：每天自动联网分析、五人会诊、四方对赌。仅供娱乐与 AI 能力测评。">
<style>
  :root{{--bg:#080c11;--card:#111922;--card2:#0e151d;--line:#1d2935;--ink:#e9f0f7;
    --muted:#7d8b9c;--accent:#22d3a8;--accent2:#3ba3ff;--win:#22d3a8;--draw:#8b95a3;--lose:#ff7a45;--danger:#ff5d6c}}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:radial-gradient(1200px 600px at 50% -10%,#0e1a16 0%,var(--bg) 55%);color:var(--ink);
    font-family:-apple-system,"PingFang SC","Microsoft YaHei",system-ui,sans-serif;line-height:1.6;
    padding:20px 16px 60px;max-width:620px;margin:0 auto}}
  header{{text-align:center;padding:18px 0 8px}}
  header h1{{font-size:23px;letter-spacing:.5px}}
  header .tag{{display:inline-block;font-size:11px;color:var(--accent);border:1px solid var(--accent);
    border-radius:5px;padding:2px 8px;margin-top:8px}}
  header .date{{font-size:12px;color:var(--muted);margin-top:8px}}
  .scoreboard{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:18px 0 8px}}
  .sb{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 6px;text-align:center}}
  .sb.lead{{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent) inset}}
  .sb .who{{font-size:10.5px;color:var(--muted);margin-bottom:3px}}
  .sb .rec{{font-size:15px;font-weight:800}}
  .sb .rate{{font-size:11px;color:var(--accent)}}
  .ticker{{font-size:11.5px;color:var(--muted);text-align:center;margin-bottom:20px}}
  h2{{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:1.5px;
    margin:26px 0 10px;display:flex;align-items:center;gap:8px}}
  h2::before{{content:"";width:3px;height:13px;background:var(--accent);border-radius:2px}}
  .recap{{background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}}
  .rrow{{display:flex;justify-content:space-between;padding:9px 13px;border-bottom:1px solid var(--line);font-size:13.5px}}
  .rrow:last-child{{border-bottom:none}}
  .rrow .sc{{font-variant-numeric:tabular-nums;color:#cdd9e5}}
  .hit{{color:var(--win)}} .miss{{color:var(--danger)}}
  .match{{background:linear-gradient(180deg,var(--card),var(--card2));border:1px solid var(--line);
    border-radius:13px;padding:14px;margin-bottom:11px}}
  .mhead{{display:flex;justify-content:space-between;align-items:center;margin-bottom:7px}}
  .vs{{font-size:16px;font-weight:800}}
  .grp{{font-size:10px;color:var(--muted);border:1px solid var(--line);border-radius:4px;padding:1px 5px;margin-left:6px}}
  .time{{font-size:12px;color:var(--accent2);font-variant-numeric:tabular-nums}}
  .mstat{{font-size:12px;color:#bcc9d6;margin:4px 0 8px}}
  .mstat b{{color:var(--ink)}} .sep{{color:var(--line);margin:0 5px}}
  .moon{{letter-spacing:1px}}
  .take{{font-size:12.5px;color:#cdd9e5;border-left:2px solid var(--accent);padding-left:8px;margin:6px 0}}
  .votes{{display:flex;gap:4px;margin-top:9px}}
  .vote{{flex:1;text-align:center;font-size:9.5px;border-radius:6px;padding:5px 2px;border:1px solid var(--line)}}
  .vote .r{{color:var(--muted);display:block;font-size:9px;margin-bottom:2px}}
  .vote .v{{font-weight:700}}
  .vote.win{{background:rgba(34,211,168,.12);border-color:rgba(34,211,168,.4)}} .vote.win .v{{color:var(--win)}}
  .vote.draw{{background:rgba(139,149,163,.12)}} .vote.draw .v{{color:var(--draw)}}
  .vote.lose{{background:rgba(255,122,69,.12);border-color:rgba(255,122,69,.35)}} .vote.lose .v{{color:var(--lose)}}
  .split{{font-size:10px;color:#ffb454;margin-top:6px}}
  .opta-tag{{display:inline-block;font-size:10px;color:var(--accent2);margin-top:6px;
    border:1px solid rgba(59,163,255,.3);border-radius:4px;padding:1px 6px}}
  .pick{{background:linear-gradient(135deg,#11241d,#0e2a33);border:1px solid var(--accent);
    border-radius:13px;padding:16px;text-align:center;margin:8px 0}}
  .pick .label{{font-size:11px;color:var(--muted)}}
  .pick .team{{font-size:22px;font-weight:800;color:var(--accent);margin:4px 0}}
  .arch{{display:flex;flex-direction:column;gap:7px}}
  .arch-item{{display:block;background:var(--card);border:1px solid var(--line);border-radius:9px;
    padding:11px 14px;color:#cdd9e5;text-decoration:none;font-size:14px;transition:border-color .15s}}
  .arch-item:hover{{border-color:var(--accent)}}
  .about{{background:var(--card);border:1px solid var(--line);border-radius:11px;padding:15px;font-size:13px;color:#bcc9d6;line-height:1.8}}
  .about b{{color:var(--ink)}}
  footer{{margin-top:28px;padding-top:14px;border-top:1px solid var(--line);
    font-size:10.5px;color:var(--muted);text-align:center;line-height:1.9}}
  footer a{{color:var(--accent);text-decoration:none}}
  footer .disc{{color:#5f6c7b}}
</style></head><body>

  <header>
    <h1>⚽ 世界杯 AI 球探</h1>
    <div class="tag">由 Kimi Code 每天自动生成</div>
    <div class="date">最新一期：{latest_date} · 北京时间</div>
  </header>

  <div class="scoreboard">{board}</div>
  <div class="ticker">四方对赌 · 我的小分队命中 {my_rate} vs Opta 超算 {opta_rate} · 已完赛 {n_finished} 场</div>

  <h2>今日焦点（北京时间）</h2>
  {cards}

  <h2>昨夜复盘</h2>
  <div class="recap">{recap_rows}</div>

  <h2>今日建议站队</h2>
  <div class="pick"><div class="label">日报单场建议支持</div><div class="team">{pick_team}</div></div>

  <h2>往期日报</h2>
  <div class="arch">{archive}</div>

  <h2>关于这个项目</h2>
  <div class="about">
    这是一个用 <b>Kimi Code</b> 搭的实验：每天早上自动联网搜集世界杯赛果与赛程，用 <b>/swarm</b> 派五个 AI 球探（数据/战术/伤病/舆情/风险官）并行会诊，再生成这份日报、记一本四方对赌账本（我的小分队 vs Opta 超算 vs 抛硬币 vs Kimi 官方）。
    全程无人值守，连这个网页都是自动更新的。想自己玩一个：<a href="https://kimi.com/code">kimi.com/code</a>，一行命令安装。
  </div>

  <footer>
    数据由 Kimi Code 自动联网搜集并标注来源 · 每日自动更新<br>
    <span class="disc">世界杯分析仅供娱乐与 AI 能力测评，不构成任何投注建议。</span><br>
    <a href="https://github.com/pingfanfan/worldcup_detective">GitHub</a> · <a href="https://kimi.com/code">Kimi Code</a>
  </footer>

</body></html>"""

if __name__ == "__main__":
    build()
