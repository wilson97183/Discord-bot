import random
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Roll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="roll",
        description="roll a random number.",
    )
    @app_commands.describe(range="Range of numbers, if not given than will be 100.")
    async def roll(self, context: Context, range: Optional[int] = None) -> None:
        result = random.randint(1, range) if range else random.randint(1, 100)
        await context.send(f"rolled {result}")

    @commands.hybrid_command(
        name="dice",
        description="roll nDn dice.",
    )
    @app_commands.describe(spec="Roll dice nDn")
    async def dice(self, context: Context, spec: Optional[str] = None) -> None:
        if spec == None:
            msg = f"1D6 rolled {random.randint(1, 6)}"

        else:
            Dice = [4, 6, 8, 10, 12, 20]
            count, dice = spec.lower().split('d', 1)

            try:
                if int(dice) not in Dice:
                    await context.send("please choose a dice in `4`,`6`,`8`,`10`,`12`,`20`")
                    return

                dice = int(dice)
                result = []

                if count == "0":
                    raise
                elif count == "":
                    result.append(str(random.randint(1, dice)))
                else:
                    count = int(count)
                    for i in range(count):
                        result.append(str(random.randint(1, dice)))

                msg = f"roll {count}D{dice} \nresult: {", ".join(result)}"

            except:
                await context.send(
                    "spec shuold be `nDn` or `ndn`, replace `n` by number and `n` should larger then 0"
                )
                return

        await context.send(msg)


async def setup(bot: commands.Bot):
    await bot.add_cog(Roll(bot))
