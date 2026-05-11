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
