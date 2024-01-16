import random
from typing import Literal, Optional

import discord
from discord import Interaction, app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     self.bot.logger.info(f'{__name__} ready')

    # @commands.hybrid_command()
    # async def sync_(self, context: Context, option: Literal['global', 'guild']) -> None:
    #     if option == "global":
    #         synced = await context.bot.tree.sync()
    #     elif option == "guild":
    #         synced = await context.bot.tree.sync(guild=context.guild)

    #     desc = f"{option} slash commands have been synchronized.\n update{len(synced)} item"

    #     for i in synced:
    #         print(i, end=', ')
    #     print()

    #     # self.bot.logger.info("sync {option} command")
    #     # await context.send(f"sycnde {len(synced)} commands.")
    #     embed = discord.Embed(description=desc, color=0xE02B2B)
    #     await context.send(embed=embed)

    # @app_commands.command(name="ping", description="ping bot")
    # async def ping(self, interaction: Interaction) -> None:
    #     await interaction.response.send_message("pong")

    # @commands.hybrid_command(
    #     name="roll_main",
    #     description="roll a random number.",
    # )
    # @app_commands.describe()
    # async def roll_main(self, context: Context):
    #     await context.send(f"rolled {random.randint(1,100)} by {context.command}")

    # 關鍵字觸發
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.bot.user:
            return
        if message.content == "吃什麼":
            await message.channel.send("command not available now")


async def setup(bot: commands.Bot):
    await bot.add_cog(Main(bot))
