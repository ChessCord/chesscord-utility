from time import time
from dotenv import load_dotenv
import os
import requests

import discord
from discord.ext import tasks

from status import get_status, statuses
from utils import StatusView, create_embed

load_dotenv()

message_id = os.getenv("MESSAGE")
channel_id = 876932773208797205
guild_id = 811678377639280670

bot_statuses = {
    "online": "🟢",
    "offline": "⚪",
    "idle": "🟠",
    "dnd": "🔴",
    "do_not_disturb": "🔴"
}


client = discord.Bot(command_prefix="c-u!", intents=discord.Intents().all())


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="this server!"))
    print("Bot is ready")


@tasks.loop(minutes=2)
async def update_status():
    comps, incidents = get_status()
    global message_id
    channel = client.get_channel(channel_id)
    c_str = ""
    for n, d in comps.items():
        c_str += f"{statuses[d['Status']]} {n}\n"
    bot = client.get_guild(guild_id).get_member(811760473422823465)
    c_time = round(time())
    embed = create_embed(
        "Bot Status",
        description=f"Check ChessCord's current status, synced with the [Status Page](https://chesscord.statuspage.io)\n\u200B\nUpdated: <t:{c_time}:R>\n\u200B",
        author=client.user,
        fields=[
            ["Bot Status", bot_statuses[str(bot.status)] + " " + str(bot.status).title() + "\n\u200B\n"],
            ["Components", c_str + "\u200B", True],
            ["Status", "\n".join([dn['Status'].replace('_', ' ').title() for _, dn in comps.items()]), True],
            ["\u200B", "\u200B", True],
            ["Incidents", "\n".join([i for i in incidents.keys()]), True],
            ["Status", "\n".join(["\n".join([j[1] for j in i['Statuses']]) for i in incidents.values()]), True],
            ["Affects", "\n".join(["\n".join([j[0] for j in i['Statuses']]) for i in incidents.values()]), True]
        ]
    )
    view = StatusView()
    if not message_id:
        message = await channel.send(bot_statuses[str(bot.status)] + " Bot Status", embed=embed, view=view)
        message_id = message.id
        with open(".env", "a") as env_file:
            env_file.write(f"MESSAGE={message_id}\n")
        return
    msg = await channel.fetch_message(message_id)
    await msg.edit(bot_statuses[str(bot.status)] + " Bot Status", embed=embed, view=view)


@update_status.before_loop
async def before_some_task():
    await client.wait_until_ready()


@tasks.loop(minutes=5)
async def heartbeat():
    print("Sending heartbeat")
    requests.post(f"https://uptime.betterstack.com/api/v1/heartbeat/{os.getenv('HEARTBEAT')}")


@heartbeat.before_loop
async def heartbeat_is_ready():
    await client.wait_until_ready()
