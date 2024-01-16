import random
from typing import Literal, Optional

import discord
from discord import Interaction, app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Guild(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # @commands.hybrid_command(name="get", description="get cmd")
    # @app_commands.describe()
    # async def get(self, context: Context, scope: Optional[str]) -> None:
    #     guild = None if scope == None else discord.Object(guild=context.guild)
    #     tree = context.bot.tree.get_commands(guild=guild)
    #     cmd = []
    #     for item in tree:
    #         cmd.append(item.__dict__['name'])
    #     await context.send(f"{cmd}")

    @app_commands.command(name="ping", description="ping bot")
    @app_commands.describe()
    async def ping(self, interaction: Interaction) -> None:
        await interaction.response.send_message("ping")

    @app_commands.command(name="pong", description="pong")
    @app_commands.describe()
    async def pong(self, interaction: Interaction) -> None:
        await interaction.response.send_message("pong")

    @app_commands.command(name="pong_pong", description="pong pong")
    @app_commands.describe()
    async def pong_pong(self, interaction: Interaction) -> None:
        await interaction.response.send_message("pong_pong")


guild_server = 674988057170149376
guild_live = 954026833748299776


async def setup(bot: commands.Bot):
    await bot.add_cog(Guild(bot), guilds=[discord.Object(id=674988057170149376)])
