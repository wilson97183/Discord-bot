import json
import os
import random
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/assets/foodType.json"):
    commands.Bot.logger.error("'foodType.json' not found")
else:
    with open(
        f"{os.path.realpath(os.path.dirname(__file__))}/assets/foodType.json",mode='a+', encoding='UTF-8'
    ) as file:
        foodType = json.load(file)


class Food(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_group(
        name="吃什麼",
        description="想不到吃什麼的時候就執行, 子命令有`add` `remove`",
    )
    async def rndRestaurant(self, context: Context) -> None:
        result = foodType["item"][random.randrange(len(foodType["item"]))]
        await context.send(f"{result["name"]}")

    @rndRestaurant.command(
        name="add",
        description="新增項目到清單"
    )
    async def rndRestaurant_add(self, context: Context, item: str) -> None:

        await context.send(f"加入 ")

async def setup(bot: commands.Bot):
    await bot.add_cog(Food(bot))
