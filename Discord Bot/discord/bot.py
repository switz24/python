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


#music

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

    ctx.voice_client.stop()
    ctx.voice_client.play(discord.FFmpegPCMAudio(url2), after=lambda e: print(f'Player error: {e}') if e else None)

    await ctx.send(f"Spiele jetzt: {info['title']}")


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




bot.run(Token)
