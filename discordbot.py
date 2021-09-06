import discord
from discord.ext import tasks, commands
from decouple import config
import boardroom as br
import functions as fn

cache = {}
channel_id = int(config('CHANNEL_ID'))
client = discord.Client()

cmd_list = fn.list_cnames(cache)[1]


cname = "creamfinance"
@client.event
async def on_ready():
    channel = client.get_channel(channel_id)
    tester.start()
    await channel.send(fn.cmd_msg())

@tasks.loop(seconds=30)
async def tester():
    print("running tester!")
    channel = client.get_channel(channel_id)
    await channel.send("TESTER MESSAGE!")


ctrl = commands.Bot(command_prefix=".")
@ctrl.command()
async def ping(ctx):
    await channel.send("TESTER MESSAGE 222!")
    
@client.event
async def on_message(message):
    global cmd_list
    ticker = ""
    msg = message.content
    if message.author == client.user:
        return
    
    
    for i in fn.list_cnames(cache)[0]:
        props = br.get_prop_by_cname(i, cache)
        for a in props:
            print(a['currentState'])
    
    
    
    if '$' in msg[0]:
        for tick in cmd_list:
            if msg.startswith(tick):
                ticker = tick
    if msg.startswith('/menu'):
        await message.channel.send(fn.cmd_msg())
    if msg.startswith('/listproto'):
        await message.channel.send(', '.join(fn.list_cnames(cache)[0]))
        
    if msg.startswith('/active'):
        await message.channel.send(', '.join(fn.list_cnames(cache)[0]))
        
        
    if ticker:
        cname = ticker.replace("$", "")
        proto = br.get_single_proto(cname, cache)
        
        props = br.get_prop_by_cname(cname, cache)
        titles = '\n'.join(fn.get_proposal_lists(props, True)[0])
        refid = '\n'.join(fn.get_proposal_lists(props, True)[1])
        title_list, refid_list = fn.get_proposal_lists(props)
        if(msg.startswith(f"{ticker}")):
            try:
                sec_command = msg.split(f"{ticker} ",1)[1]
                if sec_command in title_list:
                    ref = fn.get_prop_by_title(props, sec_command)
                    await message.channel.send(fn.prop_msg(ref))
                if sec_command in refid_list:
                    ref = fn.get_prop_by_ref(props, sec_command)
                    await message.channel.send(fn.prop_msg(ref))
            except:
                pass
        if msg.startswith(f"{ticker} proposals"):
            if msg == (f"{ticker} proposals"):
                await message.channel.send(titles)
                
                
        if msg.startswith(f"{ticker} refid"):
            if msg == (f"{ticker} refid"):
                await message.channel.send(refid)
                
        if msg == (f"{ticker} contract"):
            await message.channel.send(fn.ca_msg(proto))
            
        if msg == f"{ticker} prop ":
            cname = ticker.replace("$", "")
            props = br.get_prop_by_cname(cname, cache)
            titles = '\n'.join(fn.get_proposal_lists(props)[0])
            await message.channel.send(titles)
            
            

        if msg in cmd_list:
            ticker = msg            
            proto['price'] = br.get_price(cname)[cname]['usd']
            await message.channel.send(fn.proto_msg(proto))
        
        

try:
    client.run(config('DISCORD_BOT'))
except KeyboardInterrupt:
    client.close()
    