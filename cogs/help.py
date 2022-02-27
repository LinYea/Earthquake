import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Commands
    @commands.command(pass_context=True)
    async def help(self, ctx):

        sms=discord.Embed(title="指令列表", 
        url="https://cdn.discordapp.com/attachments/896664897046315008/946396645002727424/9LAUtPMJxhqx8H2KAv-oipyMnAwFErAUyhUwsz-aNiM.jpg", 
        color = discord.Colour.red())

        sms.set_author(name='幫助')
        sms.add_field(name="-help", value="查詢指令", inline=True)
        sms.add_field(name="-clear", value="清除訊息", inline=True)
    
        await ctx.send(embed=sms)


def setup(client):
    client.add_cog(Help(client))