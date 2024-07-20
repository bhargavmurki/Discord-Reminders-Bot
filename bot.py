import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from cogs.reminders import ReminderCog
from database import init_db, load_reminders
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)
scheduler = AsyncIOScheduler()

async def load_cogs():
    await bot.add_cog(ReminderCog(bot, scheduler))
    print("ReminderCog loaded")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    init_db()
    load_reminders(scheduler, bot)
    scheduler.start()

    await load_cogs()

bot.run(TOKEN)
