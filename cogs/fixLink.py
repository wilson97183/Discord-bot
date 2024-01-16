import re
from typing import List

import discord
import discord_markdown_ast_parser as dmap
from discord.ext import commands
from discord_markdown_ast_parser.parser import NodeType

mix_regex = re.compile(
    r"https?:\/\/(?:www\.)?(?:twitter\.com|x\.com|pixiv\.net)\/(?:([\w]+)\/)?(status|artworks)\/(\d+)(?:[\S]+)?"
)

fx_domain = "https://fxtwitter.com"
ph_domain = "https://www.phixiv.net/artworks"


def getLinks(nodes: List[dmap.Node]) -> List[str]:
    links = []
    for node in nodes:
        match node.node_type:
            case NodeType.CODE_BLOCK | NodeType.SPOILER | NodeType.CODE_INLINE:
                continue
            case NodeType.URL_WITH_PREVIEW if url := mix_regex.fullmatch(node.url):
                links.append(url)
            case _:
                try:
                    links.append(getLinks(node.children))
                except:
                    continue
    fixed_links = []
    for link in links:
        if link.group(2) == "status":
            fixed_links.append(f"{fx_domain}/{link[1]}/status/{link[3]}")

        if link.group(2) == "artworks":
            fixed_links.append(f"{ph_domain}/{link[3]}")

    return fixed_links


async def fixEmbed(message: discord.Message, links: List[str]) -> None:
    permissions = message.channel.permissions_for(message.guild.me)

    if not permissions.send_messages or not permissions.embed_links:
        raise commands.BotMissingPermissions

    if permissions.manage_messages:
        try:
            await message.edit(suppress=True)
        except discord.NotFound:
            return

    await message.channel.send("\n".join(links))


class filLink(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.bot.user:
            return

        links = getLinks(dmap.parse(message.content))

        if not links:
            return

        await fixEmbed(message, links)


async def setup(bot: commands.Bot):
    await bot.add_cog(filLink(bot))
