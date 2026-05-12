import discord
import os
import json
from dotenv import load_dotenv

# =========================
# LOAD TOKEN
# =========================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# =========================
# INTENTS
# =========================
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# =========================
# CONFIG
# =========================
CONFIG_FILE = "kasper_config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except:
        return {"maintenance": False, "debug": False, "password": "1234"}

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

# =========================
# ADMIN
# =========================
ADMIN_ID = 1503490257960698017

def is_admin(message):
    return message.author.id == ADMIN_ID

# =========================
# READY
# =========================
@client.event
async def on_ready():
    print(f"Bot online as {client.user}")

# =========================
# COMMANDS
# =========================
@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if not is_admin(message):
        return

    cmd = message.content.lower()
    config = load_config()

    if cmd == "!maintenance on":
        config["maintenance"] = True
        save_config(config)
        await message.channel.send("⚠️ Maintenance ENABLED")

    elif cmd == "!maintenance off":
        config["maintenance"] = False
        save_config(config)
        await message.channel.send("✅ Maintenance DISABLED")

    elif cmd == "!debug on":
        config["debug"] = True
        save_config(config)
        await message.channel.send("🐞 Debug ENABLED")

    elif cmd == "!debug off":
        config["debug"] = False
        save_config(config)
        await message.channel.send("✅ Debug DISABLED")

    elif cmd.startswith("!setpass"):
        parts = cmd.split(" ", 1)
        if len(parts) < 2:
            await message.channel.send("❌ No password provided")
            return

        config["password"] = parts[1]
        save_config(config)

        await message.channel.send("🔐 Password updated")

# =========================
# RUN
# =========================
client.run(TOKEN)
