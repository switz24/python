import discord
from discord.ext import commands

import discord

if not discord.opus.is_loaded():
    discord.opus.load_opus("/opt/homebrew/lib/libopus.dylib")

import qrcode

import yt_dlp as youtube_dl
import asyncio
import aiohttp

import random

#delete these three lines to set up as your own or als add a Token.py file with your token and text channel id
from Token import Token_Here
from Token import Text_Channel_ID_Here
from Token import Giphy_Api_Key_Here
from Token import Guild_ID_Here

# initialize music queue mapping (avoid undefined variable)
music_queue = {}
music_queue[Guild_ID_Here] = []


Token = Token_Here

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

Text_Channel_ID = Text_Channel_ID_Here



#login message
@bot.event
async def on_ready():
    print(f'{bot.user} has logged in!')
    channel = bot.get_channel(Text_Channel_ID)
    if on_ready:
        await channel.send('Bot ist online!')


#channel beigetreten
@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None:
        channel = bot.get_channel(Text_Channel_ID)
        await channel.send(f' @everyone {member.name} hat {after.channel.name} betreten!')





#swift command
@bot.command()
async def swift(ctx):
    optionen = ["https://images.cults3d.com/btBHMytOpO4iGbDXmn_2TxJEERM=/516x516/filters:no_upscale()/https://fbi.cults3d.com/uploaders/24075535/illustration-file/f9b1b9e6-c376-481b-9d71-99ae25988ee5/neanderthal_skull_jointed_04.jpg", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSNaa0Cwa8uX1R5jGgEdzAmH_GNpMQRcpr4NryUBnYpfQ&s=10", "https://i.ytimg.com/vi/W3DbRkbBnK4/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLD6M7OCGM4zUl2IFLOcjlKgjKxKfw", "https://media.tenor.com/YrwTZRhN610AAAAM/igorlights-hadmyback.gif", "https://media.tenor.com/6RvxIPV9F1kAAAAM/dayni.gif"]
    swift_message = random.choice(optionen)
    await ctx.send(f"{swift_message}")


#Sprachbchat joinen
@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("Du bist in keinem Voice-Channel!")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()

    await ctx.send(f"Bereit für Wiedergabe in {channel.name}")


@bot.command()
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("Der Bot ist in keinem Voice-Channel.")


#qr code
@bot.command()
async def qr (ctx, *, text):
    img = qrcode.make(text)
    img.save("qrcode.png")
    send = discord.File("qrcode.png")
    await ctx.send("Hier ist dein QR-Code:", file=send)

#music play
@bot.command()
async def play(ctx, url):
    if ctx.author.voice is None:
        await ctx.send("Du bist in keinem Voice-Channel!")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        await channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['url']
        dauer = info.get('duration') or 0

    ctx.voice_client.stop()
    ctx.voice_client.play(discord.FFmpegPCMAudio(url2), after=lambda e: print(f'Player error: {e}') if e else None)
   
    await asyncio.sleep (dauer)
    
    guild_id = ctx.guild.id
    if music_queue.get(guild_id):
        naechster = music_queue[guild_id].pop(0)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info2 = ydl.extract_info(naechster['url'], download=False)
            url3 = info2['url']

        ctx.voice_client.play(
            discord.FFmpegPCMAudio(url3),
            after=lambda e: print(f'Player error: {e}') if e else None
        )
        await ctx.send(f"Spiele jetzt: {info2.get('title', 'Unbekannt')}")

    


@bot.command()
async def stop(ctx):
    if ctx.voice_client is not None:
        ctx.voice_client.stop()
        await ctx.send("Die Wiedergabe wurde gestoppt.")
    else:
        await ctx.send("Der Bot ist in keinem Voice-Channel.")


@bot.command()
async def pause(ctx):
    if ctx.voice_client is not None and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Die Wiedergabe wurde pausiert.")
    else:
        await ctx.send("Der Bot spielt gerade nichts ab.")
@bot.command()
async def resume(ctx):
    if ctx.voice_client is not None and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Die Wiedergabe wurde fortgesetzt.")
    else:
        await ctx.send("Der Bot ist nicht pausiert.")


#queue aber noch nicht implementiert
@bot.command()
async def queue(ctx, url):
    if ctx.voice_client is None:
        await ctx.send("Der Bot ist in keinem Voice-Channel.")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['url']
        title = info.get('title', 'Unbekannter Titel')

    guild_id = ctx.guild.id
    if guild_id not in music_queue:
        music_queue[guild_id] = []

    music_queue[guild_id].append({'url': url2, 'title': title})
    await ctx.send(f"Zum Queue hinzugefügt: {title}")
            
@bot.command()
async def show_queue(ctx):
    guild_id = ctx.guild.id
    if guild_id not in music_queue or not music_queue[guild_id]:
        await ctx.send("Die Queue ist leer")
        return

    queue_list = "\n".join([f"{i+1}. {item['title']}" for i, item in enumerate(music_queue[guild_id])])
    await ctx.send(f"Warteschlange:\n{queue_list}")


#kick & ban/unban
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, nutzer: discord.Member, *, reason: str = None):
    try:
        await nutzer.kick(reason=reason)
        await ctx.send(f"Der User {nutzer.id} wurde erfolgreich gekickt")
    except Exception as e:
        await ctx.send(f"Fehler beim Kicken: {e}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, *, nutzer: discord.Member):
    await nutzer.ban()
    await ctx.send(f"der User {nutzer.id} wurde gebannt")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, nutzer: discord.User):
    await ctx.guild.unban(nutzer)
    await ctx.send(f"der User{nutzer.id} wurde entbannt")

#channel erstellen und löschen
@bot.command()
async def channel (ctx, *, naawme: str = "ticket"):
    await ctx.guild.create_text_channel(naawme)
    await ctx.send(f"Der Kanal \"{naawme}\" wurde erstellt.")

@bot.command()
async def channel_delete(ctx, *, naawme: str = "ticket"):
    channel = discord.utils.get(ctx.guild.text_channels, name=naawme)
    if channel is None:
        await ctx.send(f"Der Kanal \"{naawme}\" wurde nicht gefunden.")
        return

    await channel.delete()
    await ctx.send(f"Der Kanal \"{naawme}\" wurde gelöscht.")


@bot.command()
async def vc(ctx, *, naawme: str = "ticket"):
    await ctx.guild.create_voice_channel(naawme)
    await ctx.send(f"Der Voice Channel \"{naawme}\" wurde erstellt ")


@bot.command()
async def vc_delete(ctx, *, naawme: str = "ticket"):
    vc = discord.utils.get(ctx.guild.voice_channels, name=naawme)
    if vc is None:
     await ctx.send(f"Der Vc  \"{naawme}\" wurde nicht gefunden")
     return

    await vc.delete()
    await ctx.send(f" Der Vc  \"{naawme}\" wurde gelöscht")


#help
@bot.command()
async def h(ctx):
   await ctx.send (f"{h_message}")

h_message = "Hier sind die verfügbaren Befehle:\n- `!join`: Tritt dem Voice-Channel bei\n- `!leave`: Verlässt den Voice-Channel\n- `!qr <text>`: Erstellt einen QR-Code mit dem angegebenen Text\n- `!play <url>`: Spielt Musik aus einer URL ab\n- `!stop`: Stoppt die Wiedergabe\n- `!pause`: Pausiert die Wiedergabe\n- `!resume`: Setzt die Wiedergabe fort"

#cat
@bot.command()
async def cat(ctx):
    await ctx.send("https://cataas.com/cat/gif")


#gif
@bot.command()
async def gif(ctx, *, text):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.giphy.com/v1/gifs/search?api_key={Giphy_Api_Key_Here}&q={text}&limit=1") as response:
            data = await response.json()
            if data['data']:
                gif_url = data['data'][0]['images']['original']['url']
                await ctx.send(gif_url)
            else:
                await ctx.send("Kein GIF gefunden.")



@bot.event
async def on_member_join(ctx, member = True):
    await ctx.send(f"Willst du auf die Insel kommen?")



bot.run(Token)
