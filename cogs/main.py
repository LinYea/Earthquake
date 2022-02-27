import discord
from discord.ext import commands

class Main(commands.Cog):
    def __init__(self, client):
        self.client = client
    #調用event函式庫
    @commands.Cog.listener()
    #當機器人完成啟動時
    async def on_ready(self):
        client_channel = self.client.get_channel(int(947506098745774150))
        print('目前登入身份：',self.client.user)
        await client_channel.send(f"我回來惹(*´∀`*)")
        await client_channel.send(f"地震警報已啟動")

    @commands.Cog.listener()
    async def on_member_join(member):
        print(f'{member} has joined server.')

    @commands.Cog.listener()
    async def on_member_remove(member):
        print(f'{member} has left a server.')

def setup(client):
    client.add_cog(Main(client))