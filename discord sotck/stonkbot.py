import discord
from discord.ext import commands
import yfinance as yf
from simple import get_model

token = ''

client = discord.Client(intents = discord.Intents.all())
channel = 1069711820698419322
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())


def valid(a):
    error = []
    ticker = yf.Ticker(str(a[0]))
    try:
        ticker.info
    except:
        error.append("I dont know this ticker, please provide a valid ticker.")

    try:
        val = int(a[1])
    except:
        error.append("You need to provide a valid value for future steps.")

    valid_time_step = ['1m', '2m', '5m', '15m']
    if(a[2] not in valid_time_step):
        error.append("Provide valid interval")
    else:
        pass
    
    return error

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith('$rst'):
        a = message.content.split()[1:] #remove $rst

        #check for valid results
        val = valid(a)
        if(not val):
            msg = await message.channel.send("Getting data, please wait\nHere is a cat while you wait.")
            msg2 = await message.channel.send("https://cdn.discordapp.com/attachments/1118993194097574009/1140019545738858526/desktop-wallpaper-13o-animal-ears-blush-catgirl-cat-smile-chibi-cropped-hololive-nekomata-okayu-purple-hair-short-hair-sketch-white-nekomata-okayu.jpg")


            ticker = a[0]
            future_steps = int(a[1])
            interval = a[2]

            get_model(ticker,future_steps,interval)

            await msg.delete()
            await msg2.delete()


            file = discord.File(r'graphs\\'+ticker+'.png', filename=(ticker+'.png'))
            embed = discord.Embed()
            embed.set_image(url="attachment://"+(ticker+'.png'))
            await message.channel.send(file=file, embed=embed)

        else:
            await message.channel.send("\n".join(val))

if __name__ == "__main__":
    bot.run(token)
