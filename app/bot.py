# FILE: EncarScraper/app/bot.py
# FINAL ROBUST VERSION for Two-Stage Pipeline

import discord
import subprocess
import os
import logging
import sys
import json
from dotenv import load_dotenv

load_dotenv()

from .config import *

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)-8s [BOT] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

def is_process_running(pid_file):
    """Checks if a process is running based on its PID file."""
    return os.path.exists(pid_file)

@bot.event
async def on_ready():
    logger.info(f'Bot logged in as {bot.user}')
    os.makedirs(DATA_DIR, exist_ok=True)
    for f in [STOP_SIGNAL_FILE, DISCOVERY_PID_FILE, ENRICHMENT_PID_FILE, ENRICHMENT_STATUS_FILE]:
        if os.path.exists(f):
            logger.warning(f"Found a stale file, removing it: {f}")
            os.remove(f)

@bot.event
async def on_message(message):
    if message.author == bot.user or not message.content.startswith('!'):
        return

    command = message.content.split()[0].lower()
    is_running = is_process_running(DISCOVERY_PID_FILE) or is_process_running(ENRICHMENT_PID_FILE)

    if command == '!discover':
        if is_running:
            await message.channel.send("❌ **Error:** A scraper process is already running.")
            return
        await message.channel.send("✅ **Command received:** Starting the **Discovery** process. This may take a few minutes. Use `!status` to check for completion.")
        subprocess.Popen([sys.executable, "-m", "app.discover"])

    elif command == '!enrich':
        if is_running:
            await message.channel.send("❌ **Error:** A scraper process is already running.")
            return
        if not os.path.exists(DISCOVERED_LISTINGS_FILE):
            await message.channel.send("🟡 **Warning:** Discovery data not found. Please run `!discover` first.")
            return
        await message.channel.send("✅ **Command received:** Starting the **Enrichment** process. Use `!status` for detailed progress.")
        subprocess.Popen([sys.executable, "-m", "app.enrich"])

    elif command == '!stop':
        if not is_running:
            await message.channel.send("❌ **Error:** No scraper processes are currently running.")
            return
        logger.info("Received !stop command. Creating stop signal file.")
        await message.channel.send("🟡 **Command received:** Sending stop signal. The current process will halt gracefully.")
        with open(STOP_SIGNAL_FILE, "w") as f:
            f.write("stop")
            
    elif command == '!status':
        if is_process_running(DISCOVERY_PID_FILE):
            await message.channel.send("🔵 **Status:** The **Discovery** process is **RUNNING**.")
        elif is_process_running(ENRICHMENT_PID_FILE):
            try:
                with open(ENRICHMENT_STATUS_FILE, 'r') as f:
                    status = json.load(f)
                
                if status['status'] == 'Running':
                    s = f"S: {status['processed']:,}"
                    f = f"F: {status['failed']:,}"
                    ni = f"NI: {status['partial_counts'].get('no_inspection', 0):,}"
                    nr = f"NR: {status['partial_counts'].get('no_record', 0):,}"
                    nd = f"ND: {status['partial_counts'].get('no_diagnosis', 0):,}"
                    
                    msg = (f"🟢 **Status: Enrichment is RUNNING**\n```"
                           f"Progress: {status['processed']:,} / {status['total']:,} ({status['progress']})\n"
                           f"Speed: {status['speed']} | ETA: {status['eta']}\n"
                           f"--------------------------------------------------\n"
                           f"{s} | {f} | {ni} | {nr} | {nd}```")
                    await message.channel.send(msg)
                elif status['status'] in ['Complete', 'Stopped', 'Crashed']:
                    partial_str = "\n".join([f"- No {k.replace('no_', '')}: {v:,}" for k,v in status['partial_counts'].items() if v > 0])
                    partial_section = f"\nPartially Processed:\n{partial_str}" if any(status['partial_counts'].values()) else ""
                    msg = (f"🏁 **Status: Enrichment {status['status']}**\n```"
                           f"Successful: {status['processed']:,}\n"
                           f"Failed:     {status['failed']:,}{partial_section}\n\n"
                           f"Total Duration:  {status['duration']}```")
                    await message.channel.send(msg)
                else: # Initializing or other state
                     await message.channel.send(f"🟢 **Status:** The **Enrichment** process is **{status.get('status', 'RUNNING')}**...")

            except (FileNotFoundError, json.JSONDecodeError):
                await message.channel.send("🟢 **Status:** The **Enrichment** process is **INITIALIZING**...")
        else:
            await message.channel.send("⚫ **Status:** The scraper is **NOT RUNNING**.")
    
    else:
        await message.channel.send(f"❓ **Unknown command.** Available: `!discover`, `!enrich`, `!stop`, `!status`")

def run_bot():
    if not DISCORD_BOT_TOKEN:
        logger.critical("FATAL: DISCORD_BOT_TOKEN is not set in your .env file!")
        sys.exit("Bot token not found.")
    
    logger.info("Starting the Discord bot listener...")
    try:
        bot.run(DISCORD_BOT_TOKEN)
    except Exception as e:
        logger.critical(f"An unrecoverable error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    run_bot()