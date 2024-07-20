# _**Discord Reminders Bot**_

A Discord bot designed for setting and managing reminders. Users can create one-time or recurring reminders, list all their reminders, and delete specific reminders.

## Features

- **Set Reminders**: Create reminders that trigger after a specified amount of time.
- **List Reminders**: View all active reminders set by the user.
- **Delete Reminders**: Remove specific reminders.
- **Recurring Reminders**: Optionally set reminders to repeat at specified intervals.

## Installation

### Prerequisites

- Python 3.10 or higher
- `pip` (Python package installer)
- A Discord bot token (create one on the [Discord Developer Portal](https://discord.com/developers/applications))

### Clone the Repository

```bash
git clone https://github.com/yourusername/RemindersBot.git
cd RemindersBot
```

### Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### Create .env File

1. Create a new file named `.env` in the project root.
2. Add your Discord bot token to the `.env` file:

``` 
DISCORD_TOKEN=your_token_here
```

### Configure the Bot
Ensure the bot has the necessary permissions:

1. Go to the [Discord Developer Portal](https://discord.com/developers/). 
2. Select your application. 
3. Navigate to the "Bot" section. 
4. Enable the "MESSAGE CONTENT INTENT" under Privileged Gateway Intents.

### Run the Bot

```bash
python bot.py
```

## Usage

- **Set Reminder**: `!set_reminder <time> <message>`

    Example: !set_reminder 5s Take a break

    Description: Sets a reminder that will notify you after the specified time. Time format is Xs (seconds), Xm (minutes), Xh (hours), or Xd (days).

- **List Reminders**: `!list_reminders`

    Description: Lists all the reminders you have set, including their time and any repeat intervals.

- **Delete Reminder**: `!delete_reminder <reminder_id>`

    Example: `!delete_reminder 1`
    Description: Deletes a specific reminder by its index from the list of reminders.


### File Structure
    
```bash
    RemindersBot/
├── bot.py            # Main script to run the bot
├── cogs/
│   └── reminders.py  # Contains the ReminderCog class with command logic
├── database.py       # Contains database initialization and operations
├── requirements.txt  # Python package dependencies
└── .env              # Environment file containing the bot token
```


