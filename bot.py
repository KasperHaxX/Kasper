import json

CONFIG_FILE = "kasper_config.json"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)
      if cmd == "!maintenance on":
    config = load_config()
    config["maintenance"] = True
    save_config(config)
    await message.channel.send("⚠️ Maintenance ENABLED")

elif cmd == "!maintenance off":
    config = load_config()
    config["maintenance"] = False
    save_config(config)
    await message.channel.send("✅ Maintenance DISABLED")

elif cmd == "!debug on":
    config = load_config()
    config["debug"] = True
    save_config(config)
    await message.channel.send("🐞 Debug ENABLED")

elif cmd == "!debug off":
    config = load_config()
    config["debug"] = False
    save_config(config)
    await message.channel.send("✅ Debug DISABLED")

elif cmd.startswith("!setpass"):
    new_pass = cmd.split(" ", 1)[1]
    config = load_config()
    config["password"] = new_pass
    save_config(config)
    await message.channel.send("🔐 Password updated")

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# simple control state
MAINTENANCE_MODE = False
BANNED_USERS = []

ADMIN_ID = 1503460348286468268  # your Discord ID

def is_admin(message):
    return message.author.id == ADMIN_ID

@client.event
async def on_ready():
    print(f"Bot online as {client.user}")

@client.event
async def on_message(message):
    global MAINTENANCE_MODE, BANNED_USERS

    if message.author == client.user:
        return

    if not is_admin(message):
        return  # only you can control system

    cmd = message.content.lower()

    # 🔧 maintenance control
    if cmd == "!maintenance on":
        MAINTENANCE_MODE = True
        await message.channel.send("⚠️ Maintenance ENABLED")

    elif cmd == "!maintenance off":
        MAINTENANCE_MODE = False
        await message.channel.send("✅ Maintenance DISABLED")

    # ⛔ ban system
    elif cmd.startswith("!ban"):
        user = cmd.split(" ", 1)[1]
        BANNED_USERS.append(user.lower())
        await message.channel.send(f"⛔ Banned {user}")

    elif cmd.startswith("!unban"):
        user = cmd.split(" ", 1)[1]
        BANNED_USERS.remove(user.lower())
        await message.channel.send(f"✅ Unbanned {user}")

client.run(TOKEN)
