import sqlite3
from datetime import datetime

from apscheduler.triggers.date import DateTrigger


def init_db():
    conn = sqlite3.connect('reminders.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reminders
                 (user_id INTEGER, message TEXT, reminder_time TEXT, repeat_interval TEXT)''')
    conn.commit()
    conn.close()

def add_reminder(user_id, message, reminder_time, repeat_interval=None):
    conn = sqlite3.connect('reminders.db')
    c = conn.cursor()
    c.execute("INSERT INTO reminders (user_id, message, reminder_time, repeat_interval) VALUES (?, ?, ?, ?)",
              (user_id, message, reminder_time, repeat_interval))
    conn.commit()
    conn.close()

def get_reminders(user_id=None):
    conn = sqlite3.connect('reminders.db')
    c = conn.cursor()
    if user_id:
        c.execute("SELECT message, reminder_time, repeat_interval FROM reminders WHERE user_id = ?", (user_id,))
    else:
        c.execute("SELECT user_id, message, reminder_time, repeat_interval FROM reminders")
    reminders = c.fetchall()
    conn.close()
    return reminders

def delete_reminder(user_id, message):
    conn = sqlite3.connect('reminders.db')
    c = conn.cursor()
    c.execute("DELETE FROM reminders WHERE user_id = ? AND message = ?", (user_id, message))
    conn.commit()
    conn.close()

def load_reminders(scheduler, bot):
    all_reminders = get_reminders()
    for user_id, message, reminder_time, repeat_interval in all_reminders:
        reminder_time = datetime.fromisoformat(reminder_time)
        if reminder_time > datetime.now():
            async def reminder_callback(user_id=user_id, message=message):
                user = await bot.fetch_user(user_id)
                await user.send(f'Reminder: {message}')

            scheduler.add_job(reminder_callback, DateTrigger(run_date=reminder_time))

    print(f"Loaded {len(all_reminders)} reminders from the database.")
