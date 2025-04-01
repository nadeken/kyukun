import os
import discord
from discord.ext import commands
from collections import deque
from dotenv import load_dotenv

# トークンの読み込み
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Botの初期化と設定
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# タスク管理のキュー
should_queue = deque()
wantto_queue = deque()

# 起動時のstdout出力
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# inqコマンド タスクを追加
@bot.command()
async def inq(ctx, category: str, *, task: str):
    if category == "should":
        should_queue.append(task)
        await ctx.send(f":white_check_mark: `{task}` をやるべきことに追加したよ！")
    elif category == "wantto":
        wantto_queue.append(task)
        await ctx.send(f":white_check_mark: `{task}` をやりたいことに追加したよ！")
    else:
        await ctx.send(":warning: `/inq should [タスク名]` または `/inq wantto [タスク名]` の形式で入力してね！")

# listコマンド タスクすべてを表示
@bot.command()
async def list(ctx):
    should_tasks = "\n".join(f"- {task}" for task in should_queue) if should_queue else "なし"
    wantto_tasks = "\n".join(f"- {task}" for task in wantto_queue) if wantto_queue else "なし"
    
    response = (
        "**:pencil: やるべきこと:**\n" + should_tasks + "\n\n"
        "**:video_game: やりたいこと:**\n" + wantto_tasks
    )
    
    await ctx.send(response)

# doneコマンド タスクを終了（削除）
@bot.command()
async def done(ctx):
    if should_queue:
        finished_task = should_queue.popleft()
        await ctx.send(f":white_check_mark: `{finished_task}` を完了！次のタスクへ進もう！")
    elif wantto_queue:
        finished_task = wantto_queue.popleft()
        await ctx.send(f":white_check_mark: `{finished_task}` を完了！")
    else:
        await ctx.send(":tada: 今日は寝なさい!")

# peekコマンド 次にやることを表示
@bot.command()
async def peek(ctx):
    if should_queue:
        await ctx.send(f":mag_right: **次にやるべきこと:** `{should_queue[0]}`")
    elif wantto_queue:
        await ctx.send(f":mag_right: **次にやりたいこと:** `{wantto_queue[0]}`")
    else:
        await ctx.send(":tada: 今やるべきことはないよ！ゆっくり休もう！")

# Botを実行
bot.run(TOKEN)

