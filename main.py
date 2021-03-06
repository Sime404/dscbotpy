import asyncio
import discord
from discord import Member
from discord.ext import commands, tasks
from random import choice
import requests
import json
import os
from keep_alive import keep_alive
import pyshorteners


client = commands.Bot(command_prefix='Sime404')

status = ['spotify ! ', 'commands!', 'music for you !',
          'my fire mix', 'youtube videos', 'cards', 'with fire', 'with others', 'a game', 'tricks', 'UNO', 'it my way !',
          'anything but music', '.help', 'with other bots'] 
          
waves = [
    '***waving you back ๐***', 'why did you wake me up ? ๐ฅฑ',
    'pls, let me sleep ๐ค', '๐ค am sleeping, do not disturb',
    'wanna let me play some music for you ? ๐ถ', 'whatssup ? dude !! ;)'
]

die = [
    'what wrong have I done to you ?', 'why do you want to kill me ?',
    '**sabotage** activated !!', '***omae wa mou shindeiru*** ๐',
    'I have such a small life, you want that too ?', '***DEAD***',
    '**RIP** me', 'you are accused of `Attempt To Murder`'
]

# good_morning = [
#     '**Good morning to you. May every step you make be filled with happiness, love, and peace.**',
#     '**May this morning offer you new hope for life! May you be happy and enjoy every moment of it. Good morning!**',
#     '**Good morning! May your day be filled with positive things and full of blessings. Believe in yourself.**',
#     '**Good Morning my love! I hope my good morning text will bring a smile on your face at the very beginning of the day. I love you so much.**',
#     '**Every morning is a new blessing, a second chance that life gives you because youโre so worth it. Have a great day ahead. Good morning!**',
#     '**Get up early in the morning and donโt forget to say thank you to God for giving you another day! Good morning!**',
#     '**Good morning, my friend! Life gives us new opportunities every day, so hoping today will be full of good luck and prosperity for you!**',
#     '**Good Morning, dear! May everything you dreamed about last night comes true!**',
#     '**Good morning. I hope you have a wonderful day.**',
#     '**Life never gives you a second chance. So, enjoy every bit of it. Why not start with this beautiful morning. Good morning!**',
#     '**Life is full of uncertainties. But there will always be a sunrise after every sunset. Good morning!**'
# ]

good_night = [
    '**good night, have sweet dreams**',
    '**Hey there, just dropped by to say hello. Hope that you had a wonderful day! Good Night!**',
    '**I couldnโt fall asleep unless I told you how much I miss you โ love you and goodnight!**',
    '**Today has been a non-stop, hectic, crazy day, and I wish I had gotten time to see youโฆ so Iโm thinking about U before I fall asleep. Goodnight, sleep tight!**',
    '**We are together for a very long time now, and I just wanna let you know that I love you more than ever now. Good Night**',
    '**I donโt know what Iโd do without you. You mean everything to me. Good Night.**',
    '**One day I wish my dream would come true, And Iโd wake up next to you. Till then Good Night!**',
    '**When I sleep, it is a call to you and when I dream it is a wait for U. Good Night.**',
    '**Sleep tight and good night as I wish you the best of dreams with all of my might.**',
    ' **I know I will have sweet dreams tonight, my only nightmares are when U are away from me. Have a lovely night.**',
    '**While the moon is shining in the sky, you are the brightest star of my night. Good Night.**'
]


# love_words = ['i love you', 'love', 'luv', 'lub', 'โค']

# love_reply = ['love you too โค๏ธ', 'love you 2 โค๏ธ', 'โค๏ธ you too...']


@client.event
async def on_ready():
    change_status.start()
    print('Bot is Online !')


@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='welcome')
    await channel.send(
        f'Welcome {member.mention}!  Ready to jam out? See `.help` command for details!'
    )


@client.command(
    name='ping', help='this command will return you with Latency !')
async def ping(ctx):
    await ctx.send(
        f'**pinged !** Latency is : {round(client.latency * 1000)}ms')


@client.command(name='hello', help='this command will wave you back !')
async def waving(ctx):
  await ctx.send(choice(waves))

# ------------------------------------------------------------------
# url shortner


@client.command(name='short', help='shortens long urls !')
async def shorten(ctx, link):
  s = pyshorteners.Shortener()
  x = s.tinyurl.short(link)
  await ctx.send(x)
# ------------------------------------------------------------------
# die


@client.command(name='die', help='the command to kill')
async def dead(ctx):
  await ctx.send(choice(die))
# -------------------------------------------------------------------
#  good morning


@client.command(name='gm', help='this command will greet you with good morning wishes!')
async def generate_quote(ctx):
    url = "https://ajith-messages.p.rapidapi.com/getMsgs"

    querystring = {"category": "good morning"}

    headers = {
        'x-rapidapi-key': "8c9a184bdfmsh7ddc8d04557787ep1b8dddjsn003f75efff88",
        'x-rapidapi-host': "ajith-messages.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    json_data = json.loads(response.text)
    final_text = json_data["Message"]
    await ctx.send(final_text)
# -------------------------------------------------------------------
#  good night


@client.command(
    name='gn',
    help='this command will greet you with good night wishes!')
async def gn(ctx):
    await ctx.send(choice(good_night))
# -------------------------------------------------------------------
# bday text


@client.command(name='bday', help='this command will generate some quotes')
async def generate_quote(ctx, member: discord.Member):
    url = "https://ajith-messages.p.rapidapi.com/getMsgs"

    querystring = {"category": "birthday"}

    headers = {
        'x-rapidapi-key': "8c9a184bdfmsh7ddc8d04557787ep1b8dddjsn003f75efff88",
        'x-rapidapi-host': "ajith-messages.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    json_data = json.loads(response.text)
    bday_text = json_data["Message"]
    await ctx.message.delete()
    await ctx.send(f'{bday_text} ๐ซ๐๐ {member.mention}')
# -------------------------------------------------------------------
# status


@tasks.loop(minutes=30)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))
# -----------------------------------------------------------
# motivational quote generator


def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + ' -' + json_data[0]['a']
    return quote


@client.command(name='quotes', help='this command will send some quotes')
async def send_msg(ctx):
    quote = get_quote()
    await ctx.send(quote)
# -----------------------------------------------------------
# clear command


@client.command(name='clear', help='this command will clear msgs')
# @commands.has_role('mod')
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)
# ----------------------------------------------------
# weather report


@client.command(name='weather', help='this command will send weather report')
async def send_weather(ctx, *, city):
    response = requests.get(
        'https://api.openweathermap.org/data/2.5/weather?q={}&appid=bc3f1439402bf0089ab54926b9e2ad71&units=metric'.format(
            city)
    )
    json_data = json.loads(response.text)

    location = json_data['name']
    temp = json_data['main']['temp']
    wind_speed = json_data['wind']['speed']
    feels_like = json_data['main']['feels_like']
    max_temp = json_data['main']['temp_max']
    min_temp = json_data['main']['temp_min']
    humidity = json_data['main']['humidity']
    cloudiness = json_data['clouds']['all']
    description = json_data['weather'][0]['description']
    weather = (
        '```Location: {}\nTemperature : {}ยฐ C \nWind Speed : {} m/s\nMax Temp: {}ยฐ C\nMin Temp: {}ยฐ C\nFeels like: {}ยฐ C'
        '\nCloudiness: {}%\nHumidity: {}\nWeather Description: {}```'
            .format(location, temp, wind_speed, max_temp, min_temp, feels_like, cloudiness, humidity, description))

    await ctx.send(weather)
    # msg.add_reaction(':fire:')
# -------------------------------------------------------------
# error-handlers


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("`sorry, I don't have info about this`")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("`sorry, you don't have permission for this command`")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("`sorry, you are missing some arguments`")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("`sorry, no such command found`")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("`sorry, no such user found or, you haven't mentioned the user`")
    else:
        raise error
# -------------------------------------------------------------------
# love calculator


@client.command(name='lovecalculator', help='calculate your love luck')
async def love_calculator(ctx, male, female):

  url = "https://love-calculator.p.rapidapi.com/getPercentage"
  querystring = {"fname": {male}, "sname": {female}}

  headers = {
      'x-rapidapi-key': "8c9a184bdfmsh7ddc8d04557787ep1b8dddjsn003f75efff88",
      'x-rapidapi-host': "love-calculator.p.rapidapi.com"
  }

  response = requests.request("GET", url, headers=headers, params=querystring)
  data = json.loads(response.text)
  percentage = data['percentage']
  remarks = data['result']

  result = ('Love percentage: โค๏ธ ** {}** % โค๏ธ \nremarks: {}').format(percentage, remarks)
  await ctx.send(result)

# --------------------------------------------------------------------------------


@client.event
async def on_message(message):
    user = message.author

    if 'fuck' in message.content or 'Fuck' in message.content or 'fucked' in message.content:
        await message.channel.send(
            f"**{user}** please, don't bad mouth anyone...use of ***F*** words is strictly banned, **warning given**"
        )

    await client.process_commands(message)


@client.event
async def on_message(message):
    if 'Hello! Your submission to /r/IllegalLifeProTips has been automatically removed for not complying with the following rule.' in message.content:
        await message.delete()
        await message.channel.send(" ```I deleted this post because it was deleted from the subReddit``` ")
    else:
        await client.process_commands(message)
# -------------------------------------------------------------------
# @client.command()
# async def send_msg(ctx):
#   msg = message.content
#   if any(word in msg for word in love_words):
#     await ctx.send(choice(love_reply))
# -------------------------------------------------------------------
# fetch dp


@client.command(name='dp', help='fetch dp of user')
async def dp(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    userAvatar = member.avatar_url
    await ctx.send(userAvatar)
# -------------------------------------------------------------------
# slap command


@client.command(name='slap', help='slaps someone [only mods]')
@commands.has_role('mod')
async def slap(ctx, members: commands.Greedy[discord.Member], *, reason='no reason'):
    slapped = ", ".join(x.name for x in members)
    await ctx.send('**{}** just got slapped for {}'.format(slapped, reason))
    try:
        await members.send('you were slapped for {}'.format(reason))  # send personal msgs
    except AttributeError:
        print('some error occurred')
          
          
# -------------------------------------------------------------
# The below code warns user.
@client.command(name='warn', help='will warn a member [only for admins]')
@commands.has_role("admin")
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    await member.send(f"Hello, we are from **{ctx.message.guild.name}** , You are being warned for {reason}")
    await ctx.send(f'Warned {member.mention} for {reason}')

          
# ----------------------------------------------------------------------------------------------
# The below code kicks user.
@client.command(name='kick', help='will kick a member [only for admins]')
@commands.has_role("admin")
@commands.has_permissions(kick_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'kicked {member.mention} for {reason}')



# -------------------------------------------------------------------
# The below code bans user.


@client.command(name='ban', help='will ban a member [only for admins]')
@commands.has_role("admin")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention} for {reason}')
# -------------------------------------------------------------------
# The below code unbans user.


@client.command(name='unban', help="unban's a banned member [only for admins]")
@commands.has_role("admin")
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return
# -------------------------------------------------------------------
# locks channel


@client.command(name='lock', help='locks a channel [only mods]')
@commands.has_role("mod")
@commands.has_permissions(manage_channels=True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(ctx.channel.mention + " ***is now in lockdown ๐***")

# -------------------------------------------------------------------
# unlocks channel


@client.command(name='unlock', help='unlocks a channel [only mods]')
@commands.has_role("mod")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " ***has been unlocked ๐***")

# -------------------------------------------------------------------
# user's position in server 


@commands.guild_only()
@client.command(name='position', help='returns server position')
async def position(ctx, *, member: Member = None):
    member = member or ctx.author
    if member.joined_at is None:
        await ctx.send("Could not locate your join date.")
        return
    pos = sum(m.joined_at < member.joined_at for m in ctx.guild.members if m.joined_at is not None)
    await ctx.send(f"You are member #{pos}")

# -------------------------------------------------------------------
# date of joining disord


@client.command(name='joind', help='date of joining discord')
async def userinfo(ctx, member: discord.Member):
    created_at = member.created_at.strftime("Date of joining Discord: %b %d, %Y")
    await ctx.send(created_at)

          
# --------------------------------------------------------------
# reveals joining date of user on the server


@client.command(name='serverjoind', help='reveals date of joining server')
async def serverjoind(ctx, member: discord.Member):
    server_joined_on = member.joined_at.strftime("%b %d, %Y")

    await ctx.send(f"{member.mention} joined this server on **{server_joined_on}**")


# -------------------------------------------------------------------
# confession-box


@client.command(name="confess", help="confess someone in confession_box")
# @commands.has_permissions(manage_messages=True)
async def confess(ctx, member: discord.Member, *, your_text):
    active_channel = ['confession-box']
    # if ctx.channel.id == 'channel_id':
    if str(ctx.message.channel) in active_channel:
        if your_text is None:
            await ctx.send("What do you want to say?")
            return
        await ctx.message.delete()
        await member.send(your_text)
        await ctx.channel.send("**Someone confessed something! ๐**")


    else:
        await ctx.send(f"Sorry, this command is only accessible in **{active_channel}**")
# -------------------------------------------------------------------
#random-password


@client.command(name="password", help="generate random password")
async def password(ctx, length):

    response = requests.get(
        f"https://randompasswordgeneratorapi.herokuapp.com/password-generate/{length}")

    json_data = json.loads(response.text)
    my_password = json_data["password"]

    await ctx.message.author.send(f"Your new {length} digit password is: **{my_password}** \n _Don't share your password with anyone_")
    await ctx.message.delete()
# -------------------------------------------------------------------



keep_alive()

client.run(os.getenv('Sime404'))
