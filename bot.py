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
# DISCORD INTENTS
# =========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

# =========================
# CONFIG FILE
# =========================
CONFIG_FILE = "kasper_config.json"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

# =========================
# ADMIN ID
# =========================
ADMIN_ID = 1503490257960698017

def is_admin(message):
    return message.author.id == ADMIN_ID

# =========================
# BOT READY
# =========================
@client.event
async def on_ready():
    print(f"Bot online as {client.user}")

# =========================
# MESSAGE HANDLER
# =========================
@client.event
async def on_message(message):

    if message.author == client.user:
        return

    print("MESSAGE:", message.content)

    # admin only
    if not is_admin(message):
        return

    cmd = message.content.lower()

    # =========================
    # MAINTENANCE
    # =========================
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

    # =========================
    # DEBUG
    # =========================
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

    # =========================
    # PASSWORD
    # =========================
    elif cmd.startswith("!setpass"):
        new_pass = cmd.split(" ", 1)[1]

        config = load_config()
        config["password"] = new_pass
        save_config(config)

        await message.channel.send("🔐 Password updated")

# =========================
# START BOT
# =========================
client.run(TOKEN)
