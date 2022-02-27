import discord
import json
import os

import requests
from discord.ext import commands, tasks
from dotenv import load_dotenv
from itertools import cycle
from function import *


#地震

load_dotenv()
bot = commands.Bot(command_prefix = '-')
status = cycle(['請使用:-help 查看指令','Python好難QQ','努力學習Python中'])
bot.remove_command('help')
data = sets(
    os.getenv("token"), APIToken=os.getenv("APIToken"))


def setup():
    try:
        open(data.checkFile)
    except:
        with open(data.checkFile, "w") as outfile:
            json.dump({}, outfile, ensure_ascii=False, indent=4)
            print("建立 check.json 完成")


@bot.event
async def on_ready():
    print("-"*15)
    print(bot.user.name)
    print(bot.user.id)
    print(bot.user)
    print("-"*15)
    change_status.start()
    setup()
    if data.APIToken:
        earthquake.start()
        print("地震報告啟動")
    else:
        print("請至 https://opendata.cwb.gov.tw/userLogin 獲取中央氣象局TOKEN並放置於 .env 檔案中")


@tasks.loop(seconds=10)
async def earthquake():
    # 大型地震
    API = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization={data.APIToken}&format=JSON&areaName="
    # 小型地震
    API2 = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization={data.APIToken}&format=JSON"

    b = requests.get(API).json()
    s = requests.get(API2).json()
    _API = b["records"]["earthquake"][0]["earthquakeInfo"]["originTime"]
    _API2 = s["records"]["earthquake"][0]["earthquakeInfo"]["originTime"]

    async def goTo(how, now):
        for ch in data.channels:
            await sosIn(bot.get_channel(ch), ({API: b, API2: s}[how]), data)
        with open(data.checkFile, 'w') as outfile:
            json.dump(now, outfile, ensure_ascii=False, indent=4)

    with open(data.checkFile, "r") as file:
        file = json.load(file)
    for i in [API, API2]:
        if not file.get(i):
            file[i] = ""
    if file[API] != _API:
        file[API] = _API
        await goTo(API, file)
    if file[API2] != _API2:
        file[API2] = _API2
        await goTo(API2, file)

#地震


#Command指令
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command()
async def clear(ctx, num:int):
    await ctx.channel.purge(limit = num+1)
    await ctx.send('已清理 {} 則訊息'.format(num))

@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)

@bot.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = bot.voice.client_in(server)
    await voice_client.disconnect()



#Event事件


@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('請使用-help來查詢目前有的指令!')




bot.run(data.token)