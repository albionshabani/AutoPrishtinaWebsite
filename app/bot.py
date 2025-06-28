# FILE: EncarScraper/app/bot.py
# FINAL VERSION

import discord
import subprocess
import os
import logging
import sys

from .config import DISCORD_BOT_TOKEN, STOP_SIGNAL_FILE, DATA_DIR

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)-8s [BOT] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
scraper_process = None

@bot.event
async def on_ready():
    logger.info(f'Bot logged in as {bot.user}')
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(STOP_SIGNAL_FILE):
        logger.warning("Found a stale stop signal file. Removing it.")
        os.remove(STOP_SIGNAL_FILE)

@bot.event
async def on_message(message):
    global scraper_process
    if message.author == bot.user or not message.content.startswith('!'):
        return

    command = message.content.split()[0].lower()

    if command == '!run':
        if scraper_process and scraper_process.poll() is None:
            await message.channel.send("❌ **Error:** A scraper process is already running.")
            return
        await message.channel.send("✅ **Command received:** Starting the Encar scraper worker...")
        logger.info("Received !run command. Starting scraper process.")
        scraper_process = subprocess.Popen([sys.executable, "-m", "app.main"])
        
    elif command == '!stop':
        if not scraper_process or scraper_process.poll() is not None:
            await message.channel.send("❌ **Error:** The scraper is not currently running.")
            return
        logger.info("Received !stop command. Creating stop signal file.")
        await message.channel.send("🟡 **Command received:** Sending stop signal. The scraper will halt gracefully after the current batch.")
        with open(STOP_SIGNAL_FILE, "w") as f:
            f.write("stop")
            
    elif command == '!status':
        if scraper_process and scraper_process.poll() is None:
            await message.channel.send("🟢 **Status:** The scraper is **RUNNING**.")
        else:
            await message.channel.send("⚫ **Status:** The scraper is **NOT RUNNING**.")
            if scraper_process: scraper_process = None
    
    else:
        await message.channel.send(f"❓ **Unknown command.** Available: `!run`, `!stop`, `!status`")

def run_bot():
    if not DISCORD_BOT_TOKEN or "YOUR_BOT_TOKEN_HERE" in DISCORD_BOT_TOKEN:
        logger.critical("FATAL: DISCORD_BOT_TOKEN is not configured in app/config.py!")
        raise ValueError("DISCORD_BOT_TOKEN is not set!")
    
    logger.info("Starting the Discord bot listener...")
    bot.run(DISCORD_BOT_TOKEN)

***REMOVED***
    run_bot()