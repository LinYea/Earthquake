import discord
import random
import os
from discord.ext import commands

class Voice(commands.Cog):

    def __str__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def joina(self, ctx):
        channel = ctx.message.author.voice.voice_channel
        await client.join_voice_channel(channel)

    @commands.command(pass_context=True)
    async def leavea(self, ctx):
        server = ctx.message.server
        voice_client = client.voice.client_in(server)
        await voice_client.disconnect()


def setup(client):
    client.add_cog(Voice(client))