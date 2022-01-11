from typing import Optional

import discord
from discord import ButtonStyle
from discord.utils import utcnow
from discord.ui import View


class StatusView(View):
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(discord.ui.Button(
            label="Status Page", 
            url="https://chesscord.statuspage.io/",
            emoji="📊",
            style=ButtonStyle.green
        ))


def create_embed(title: Optional[str] = None,
                 description: Optional[str] = None,
                 author: Optional[discord.User] = None,
                 fields: Optional[list] = None,
                 image: Optional[str] = None,
                 thumbnail: Optional[str] = "https://images.discordapp.net/avatars/811760473422823465/4d2e470acfc0be5ce75fbc23b406c6ce.png?size=1024",
                 color: Optional[hex] = 0xbd6f29) -> discord.Embed:
    if title:
        embed = discord.Embed(title=title, color=color)
    else:
        embed = discord.Embed(color=color)
    if description:
        embed.description = description
    if author:
        embed.set_author(name=author.name, icon_url=author.display_avatar.url)
    if fields:
        for field in fields:
            embed.add_field(name=field[0], value=field[1], inline=field[2] if len(field) > 2 else False)
    if image:
        embed.set_image(url=image)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    embed.timestamp = utcnow()
    return embed
