#!/usr/bin/env bash
# 世界杯 AI 球探 · 每日自动运行入口
# 由 launchd（com.user.kimi-scout）每天 08:00 触发。
# 手动测试： /Users/pingfan/projects/kimi/scout/run.sh
set -uo pipefail

SCOUT_DIR="/Users/pingfan/projects/kimi/scout"
KIMI="/Users/pingfan/projects/kimi/.kimi-code/bin/kimi"
BROWSE="$HOME/.claude/skills/gstack/browse/dist/browse"
LOG="$SCOUT_DIR/cron.log"

# 定时任务环境没有登录终端的 PATH，手动补齐常用路径（bun 给 browse 用）。
export PATH="$HOME/.bun/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

cd "$SCOUT_DIR" || exit 1
TODAY=$(date '+%Y-%m-%d')

echo "===== AI 球探开工 $(date '+%Y-%m-%d %H:%M:%S') =====" >> "$LOG"

# 1) Kimi Code 非交互执行当天任务（查赛果/赛程、/swarm 会诊、更新账本、生成日报 HTML）。
#    -p 模式下工具调用走 auto 权限，无需人工确认。截图交给下一步的 browse，更稳。
"$KIMI" -p "请严格按照本目录下的 daily-scout.md 执行今天($TODAY)的任务：联网核验赛果与赛程、用 /swarm 五人会诊、更新 data/ledger.json 与 data/lessons.md、生成 reports/日报-$TODAY.html。截图这步不用做。完成后打印生成的文件路径。" \
  >> "$LOG" 2>&1

# 2) 用 browse 把今天的日报 HTML 渲染成 PNG（这步比让模型自己截稳）。
HTML="$SCOUT_DIR/reports/日报-$TODAY.html"
if [ -f "$HTML" ] && [ -x "$BROWSE" ]; then
  "$BROWSE" viewport 600x900 --scale 2          >> "$LOG" 2>&1
  "$BROWSE" goto "file://$HTML"                  >> "$LOG" 2>&1
  "$BROWSE" wait --load                          >> "$LOG" 2>&1
  "$BROWSE" screenshot "$SCOUT_DIR/reports/日报-$TODAY.png" >> "$LOG" 2>&1
  echo "已截图: reports/日报-$TODAY.png" >> "$LOG"
else
  echo "⚠ 未找到日报 HTML 或 browse，跳过截图: $HTML" >> "$LOG"
fi

# 3) 重新生成网站（读最新账本+历史日报 → docs/）。
python3 "$SCOUT_DIR/build_site.py" >> "$LOG" 2>&1 && echo "已重建网站 docs/" >> "$LOG"

# 4) 提交并推送到 GitHub，触发 Pages 自动发布。
cd "$SCOUT_DIR"
git add -A >> "$LOG" 2>&1
if ! git diff --cached --quiet; then
  git commit -q -m "每日更新：$TODAY 日报" >> "$LOG" 2>&1
  if git push -q origin main >> "$LOG" 2>&1; then
    echo "✅ 已推送到 GitHub，网站将自动更新" >> "$LOG"
  else
    echo "⚠ git push 失败（可能需要重新认证 gh / 网络问题），日报已生成在本地" >> "$LOG"
  fi
else
  echo "今日无改动，跳过提交" >> "$LOG"
fi

echo "===== 完成 $(date '+%Y-%m-%d %H:%M:%S') =====" >> "$LOG"
echo "" >> "$LOG"
