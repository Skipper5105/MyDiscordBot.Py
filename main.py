import discord  # Importiere discord.py
import os  # Importiere os
import dotenv  # Importiere dotenv
import asyncio
# Für die Spotify Intergration
import yt_dlp  # Importiere yt-dlp
from discord.ext import commands  # Importiere commands von discord.ext
import datetime  # Importiere datetime

dotenv.load_dotenv()  # Lade die Umgebungsvariablen aus der .env-Datei
token = os.getenv('DISCORD_TOKEN')  # Hole den Discord-Token aus der .env-Datei
log_channel_id = 1423345957856083968  # Ersetze mit der ID deines Log-Kanals

# Bot initialisieren
intents = discord.Intents.default()  # Erstelle ein Intents-Objekt
intents.members = True  # Aktiviere die Mitglieder-Intents
intents.message_content = True  # Aktiviere die Nachrichten-Intents
bot = commands.Bot(
    command_prefix="!", intents=intents
)  # Erstelle einen Bot-Objekt mit dem Befehlspräfix "!" und den Intents


# Client-Klasse definieren
class MyClient(discord.Client):

    async def on_ready(
            self):  # Methode, die aufgerufen wird, wenn der Bot bereit ist
        print(f'Logged on as {self.user}!'
              )  # Gib eine Nachricht aus, dass der Bot bereit ist


# Hilfsfunktion zur Überprüfung der Berechtigungen
async def check_permissions(
        ctx,
        required_permission):  # Funktion zur Überprüfung der Berechtigungen
    if not ctx.author.guild_permissions.administrator and required_permission:  # Wenn der Autor kein Administrator ist und die Berechtigung erforderlich ist
        await ctx.send(
            "Du benötigst Administratorrechte, um diesen Befehl zu verwenden."
        )  # Sende eine Nachricht, dass der Autor keine Administratorrechte hat
        return False  # Gib False zurück
    return True  # Gib True zurück


# Funktion zum Senden von Log-Nachrichten
async def send_log(channel_id, message):
    channel = bot.get_channel(channel_id)
    if channel:
        try:
            await channel.send(message)
        except Exception as e:
            print(f"Fehler beim Senden der Log-Nachricht: {e}")


# Clear Chat Command
@bot.command()
async def clear(ctx, amount: int = 100):
    if not await check_permissions(ctx, True):
        return

    try:
        deleted = await ctx.channel.purge(limit=amount + 1)
        confirmation = await ctx.send(
            f"✅ {len(deleted) - 1} Nachrichten wurden gelöscht.")
        await asyncio.sleep(3)
        await confirmation.delete()
    except discord.errors.Forbidden:
        await ctx.send("❌ Ich habe keine Berechtigung, Nachrichten zu löschen."
                       )
    except Exception as e:
        await ctx.send(f"❌ Fehler beim Löschen der Nachrichten: {e}")


# Warnbefehl mit Logging
@bot.command()
async def verwarn(ctx, user: discord.Member, *, reason="Kein Grund angegeben"):
    if not await check_permissions(ctx, False):
        return

    await ctx.send(f"{user.mention} wurde verwarnt wegen: {reason}")
    try:
        await user.send(
            f"Du wurdest auf dem Server {ctx.guild.name} verwarnt wegen: {reason}"
        )
    except discord.errors.Forbidden:
        print(f"Konnte Nachricht an Benutzer senden: {user.id}")

    # Log-Nachricht erstellen
    log_message = f"**Benutzer:** {user.mention}\n**Verwarnungsgrund:** {reason}\n**Server:** {ctx.guild.name}"
    await send_log(log_channel_id, log_message)


# Stummschaltungsbefehl mit Logging
@bot.command()
async def stummschalten(ctx,
                        user: discord.Member,
                        duration: int,
                        *,
                        reason="Kein Grund angegeben"):
    if not await check_permissions(ctx, False):
        return

    try:
        from datetime import timedelta
        await user.timeout(timedelta(seconds=duration))
        await ctx.send(
            f"{user.mention} wurde für {duration} Sekunden gestimmt wegen: {reason}"
        )
        await user.send(
            f"Du wurdest auf dem Server {ctx.guild.name} für {duration} Sekunden gestimmt wegen: {reason}"
        )
    except discord.errors.Forbidden:
        print(f"Konnte Nachricht an Benutzer senden: {user.id}")

    # Log-Nachricht erstellen
    log_message = f"**Benutzer:** {user.mention}\n**Stummschaltungsdauer:** {duration} Sekunden\n**Grund:** {reason}\n**Server:** {ctx.guild.name}"
    await send_log(log_channel_id, log_message)


# Timeout-Befehl mit Logging
@bot.command()
async def timeout(ctx,
                  user: discord.Member,
                  duration: int,
                  *,
                  reason="Kein Grund angegeben"):
    if not await check_permissions(ctx, False):
        return

    try:
        from datetime import timedelta
        await user.timeout(timedelta(seconds=duration))
        await ctx.send(
            f"{user.mention} wurde für {duration} Sekunden gesperrt wegen: {reason}"
        )
        await user.send(
            f"Du wurdest auf dem Server {ctx.guild.name} für {duration} Sekunden gesperrt wegen: {reason}"
        )
    except discord.errors.Forbidden:
        print(f"Konnte Nachricht an Benutzer senden: {user.id}")

    # Log-Nachricht erstellen
    log_message = f"**Benutzer:** {user.mention}\n**Sperrdauer:** {duration} Sekunden\n**Grund:** {reason}\n**Server:** {ctx.guild.name}"
    await send_log(log_channel_id, log_message)


# Bot starten
bot.run(token)
