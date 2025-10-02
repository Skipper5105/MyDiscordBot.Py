import discord
import os
import dotenv
import asyncio
from discord.ext import commands
from datetime import datetime


dotenv.load_dotenv()
token = os.getenv('DISCORD_TOKEN')
log_channel_id = 1423345957856083968  # Ersetze mit der ID deines Log-Kanals

# Bot initialisieren
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

# Hilfsfunktion zur Überprüfung der Berechtigungen
async def check_permissions(ctx, required_permission):
    if not ctx.author.guild_permissions.administrator and required_permission:
        await ctx.send("Du benötigst Administratorrechte, um diesen Befehl zu verwenden.")
        return False
    return True


# Funktion zum Senden von Log-Nachrichten
def send_log(channel_id, message):
    channel = bot.get_channel(channel_id)
    if channel:
        try:
            asyncio.run(channel.send(message))
        except Exception as e:
            print(f"Fehler beim Senden der Log-Nachricht: {e}")


# Warnbefehl mit Logging
@bot.command()
async def verwarn(ctx, user: discord.Member, *, reason="Kein Grund angegeben"):
    if not check_permissions(ctx, False):
        return

    await ctx.send(f"{user.mention} wurde verwarnt wegen: {reason}")
    try:
        await user.send(f"Du wurdest auf dem Server {ctx.guild.name} verwarnt wegen: {reason}")
    except discord.errors.Forbidden:
        print(f"Konnte Nachricht an Benutzer senden: {user.id}")

    # Log-Nachricht erstellen
    log_message = f"**Benutzer:** {user.mention}\n**Verwarnungsgrund:** {reason}\n**Server:** {ctx.guild.name}"
    send_log(log_channel_id, log_message)


# Stummschaltungsbefehl mit Logging
@bot.command()
async def stummschalten(ctx, user: discord.Member, duration: int, *, reason="Kein Grund angegeben"):
    if not check_permissions(ctx, False):
        return

    try:
        await user.timeout(duration.seconds)
        await ctx.send(f"{user.mention} wurde für {duration} gestimmt wegen: {reason}")
        await user.send(f"Du wurdest auf dem Server {ctx.guild.name} für {duration} gestimmt wegen: {reason}")
    except discord.errors.Forbidden:
        print(f"Konnte Nachricht an Benutzer senden: {user.id}")

    # Log-Nachricht erstellen
    log_message = f"**Benutzer:** {user.mention}\n**Stummschaltungsdauer:** {duration} Sekunden\n**Grund:** {reason}\n**Server:** {ctx.guild.name}"
    send_log(log_channel_id, log_message)


# Timeout-Befehl mit Logging
@bot.command()
async def timeout(ctx, user: discord.Member, duration: int, *, reason="Kein Grund angegeben"):
    if not check_permissions(ctx, False):
        return

    try:
        await user.timeout(duration.seconds)
        await ctx.send(f"{user.mention} wurde für {duration} gesperrt wegen: {reason}")
        await user.send(f"Du wurdest auf dem Server {ctx.guild.name} für {duration} gesperrt wegen: {reason}")
    except discord.errors.Forbidden:
        print(f"Konnte Nachricht an Benutzer senden: {user.id}")

    # Log-Nachricht erstellen
    log_message = f"**Benutzer:** {user.mention}\n**Sperrdauer:** {duration} Sekunden\n**Grund:** {reason}\n**Server:** {ctx.guild.name}"
    send_log(log_channel_id, log_message)


# Bot starten
bot.run(token)
