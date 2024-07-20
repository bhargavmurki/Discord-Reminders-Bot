import re
from datetime import datetime, timedelta
from apscheduler.triggers.date import DateTrigger
from discord.ext import commands
from database import add_reminder, get_reminders, delete_reminder

def parse_time_interval(time_str):
    pattern = re.compile(r'^(\d+)([smhd])$')
    match = pattern.match(time_str)
    if match:
        value, unit = match.groups()
        value = int(value)
        now = datetime.now()
        if unit == 's':
            return now + timedelta(seconds=value)
        elif unit == 'm':
            return now + timedelta(minutes=value)
        elif unit == 'h':
            return now + timedelta(hours=value)
        elif unit == 'd':
            return now + timedelta(days=value)
    return None

class ReminderCog(commands.Cog):
    def __init__(self, bot, scheduler):
        self.bot = bot
        self.scheduler = scheduler

    @commands.command(name='set_reminder')
    async def set_reminder(self, ctx, time: str, *, message: str):
        user_id = ctx.author.id
        next_time = parse_time_interval(time)
        if next_time is None:
            await ctx.send("Invalid time format! Use 'Xs' for seconds, 'Xm' for minutes, 'Xh' for hours, or 'Xd' for days.")
            return

        add_reminder(user_id, message, next_time.isoformat())

        async def reminder_callback():
            await ctx.send(f'Reminder for {ctx.author.mention}: {message}')

        self.scheduler.add_job(reminder_callback, DateTrigger(run_date=next_time))
        await ctx.send(f'Reminder set for {time} later.')

    @commands.command(name='list_reminders')
    async def list_reminders(self, ctx):
        user_id = ctx.author.id
        user_reminders = get_reminders(user_id)

        if user_reminders:
            response = "Your reminders:\n"
            for idx, (message, reminder_time, repeat_interval) in enumerate(user_reminders, start=1):
                reminder_time = datetime.fromisoformat(reminder_time)
                formatted_time = reminder_time.strftime("%a %b %d at %I:%M %p")
                repeat_text = f" (repeats every {repeat_interval})" if repeat_interval else ""
                response += f"{idx}. {message} (at {formatted_time}){repeat_text}\n"
            await ctx.send(response)
        else:
            await ctx.send("You have no reminders set.")

    @commands.command(name='delete_reminder')
    async def delete_reminder(self, ctx, index: int):
        user_id = ctx.author.id
        user_reminders = get_reminders(user_id)

        if 0 < index <= len(user_reminders):
            message = user_reminders[index - 1][0]
            delete_reminder(user_id, message)
            await ctx.send(f'Reminder "{message}" deleted.')
        else:
            await ctx.send("Invalid reminder index.")
