import os
import sys
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context, Greedy


class Owner(commands.Cog, name="owner"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="get", description="get cmd")
    @app_commands.describe()
    async def get(self, context: Context, scope: Optional[str]) -> None:
        guild = None if scope == None else context.guild
        tree = context.bot.tree.get_commands(guild=guild)
        cmd = []
        for item in tree:
            cmd.append(item.__dict__['name'])
        await context.send(f"{cmd}")

    # ----
    # slash command sync control

    @commands.hybrid_group(name="sync", description="Synchonizes slash commands.")
    @commands.is_owner()
    async def sync(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="You need to specify a subcommand.\n\n**Subcommands:**\n`update` - Update slash command\n`remove` - slash command",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @sync.command(
        name="update",
        description="Synchonizes slash commands.",
    )
    @commands.is_owner()
    async def sync_update(self, context: Context, option: Literal['global', 'guild']) -> None:
        if option == "global":
            synced = await context.bot.tree.sync(guild=None)
        elif option == "guild":
            context.bot.tree.copy_global_to(guild=context.guild)
            synced = await context.bot.tree.sync(guild=context.guild)

        desc = f"{option} slash commands have been synchronized."

        for i in synced:
            print(i, end=', ')
        print()

        self.bot.logger.info(f"sync {option} command-update")
        await context.send(f"sycnde {len(synced)} commands.")
        embed = discord.Embed(description=desc, color=0xBEBEFE)
        await context.send(embed=embed)

    @sync.command(
        name="remove",
        description="Unsynchonizes the slash commands.",
    )
    @commands.is_owner()
    async def sync_remove(self, context: Context, option: Literal['global', 'guild']) -> None:
        if option == "global":
            context.bot.tree.clear_commands(guild=None)
            await context.bot.tree.sync()
        elif option == "guild":
            context.bot.tree.clear_commands(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)

        desc = f"{option} slash commands have been synchronized."

        self.bot.logger.info(f"sync {option} command-remove")
        embed = discord.Embed(description=desc, color=0xBEBEFE)
        await context.send(embed=embed)

    #
    # ---- origin sync command ----
    #
    # @commands.hybrid_command(
    #     name="sync",
    #     description="Synchonizes slash commands.",
    # )
    # @commands.is_owner()
    # async def sync(self, context: Context, option: Literal['global', 'guild']) -> None:
    #     if option == "global":
    #         synced = await context.bot.tree.sync()
    #     elif option == "guild":
    #         synced = await context.bot.tree.sync(guild=context.guild)

    #     desc = f"{option} slash commands have been synchronized."

    #     for i in synced:
    #         print(i, end=', ')
    #     print()

    #     # self.bot.logger.info(f"sync {option} command")
    #     # await context.send(f"sycnde {len(synced)} commands.")
    #     embed = discord.Embed(description=desc, color=0xBEBEFE)
    #     await context.send(embed=embed)

    # @commands.hybrid_command(
    #     name="unsync",
    #     description="Unsynchonizes the slash commands.",
    # )
    # @app_commands.describe(option="The to sync.")
    # @commands.is_owner()
    # async def unsync(self, context: Context, option: Literal['global', 'guild']) -> None:
    #     if option == "global":
    #         context.bot.tree.clear_commands()
    #         await context.bot.tree.sync()
    #     elif option == "guild":
    #         context.bot.tree.clear_commands(guild=context.guild)
    #         await context.bot.tree.sync(guild=context.guild)

    #     desc = "{option} slash commands have been unsynchronized."
    #     embed = discord.Embed(description=desc, color=0xBEBEFE)
    #     await context.send(embed=embed)
    #
    # -----------------

    # ------
    # control cog extensions load, re/unload

    @commands.hybrid_command(
        name="load",
        description="Load a cog",
    )
    # @app_commands.describe(cog="The name of the cog to load")
    @commands.is_owner()
    async def load(self, context: Context, cog: str) -> None:
        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(description=f"Could not load the `{cog}` cog.", color=0xE02B2B)
            await context.send(embed=embed)
            return
        embed = discord.Embed(description=f"Successfully loaded the `{cog}` cog.", color=0xBEBEFE)
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="reload",
        description="Reloads a cog.",
    )
    # @app_commands.describe(cog="The name of the cog to reload")
    @commands.is_owner()
    async def reload(self, context: Context, cog: str) -> None:
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(description=f"Could not reload the `{cog}` cog.", color=0xE02B2B)
            await context.send(embed=embed)
            return
        embed = discord.Embed(description=f"Successfully reloaded the `{cog}` cog.", color=0xBEBEFE)
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="unload",
        description="Unloads a cog.",
    )
    # @app_commands.describe(cog="The name of the cog to unload")
    @commands.is_owner()
    async def unload(self, context: Context, cog: str) -> None:
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(description=f"Could not unload the `{cog}` cog.", color=0xE02B2B)
            await context.send(embed=embed)
            return
        embed = discord.Embed(description=f"Successfully unloaded the `{cog}` cog.", color=0xBEBEFE)
        await context.send(embed=embed)

    # --------
    # control bot on/offline

    @commands.hybrid_command(
        name="restart",
        description="Make the bot restart.",
    )
    @commands.is_owner()
    async def restart(self, context: Context) -> None:
        embed = discord.Embed(description="Restarting bot...")
        await context.send(embed=embed)
        os.execv(sys.executable, ['python'] + sys.argv)

    @commands.hybrid_command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @commands.is_owner()
    async def shutdown(self, context: Context) -> None:
        embed = discord.Embed(description="Shutting down. Bye! :wave:", color=0xBEBEFE)
        self.bot.logger.info("Shutting down by command.")

        await context.send(embed=embed)
        await self.bot.close()

    # ---------------------------------------------------
    # use bot to repeat message

    @commands.hybrid_command(
        name="say",
        description="The bot will say anything you want.",
    )
    # @app_commands.describe(message="The message that should be repeated by the bot")
    @commands.is_owner()
    async def say(self, context: Context, *, message: str) -> None:
        await context.send(message)

    @commands.hybrid_command(
        name="embed",
        description="The bot will say anything you want, but within embeds.",
    )
    # @app_commands.describe(message="The message that should be repeated by the bot")
    @commands.is_owner()
    async def embed(self, context: Context, *, message: str) -> None:
        embed = discord.Embed(description=message, color=0xBEBEFE)
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Owner(bot))
