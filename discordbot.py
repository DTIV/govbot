import discord
from discord.ext import tasks
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
    cname_list = fn.list_cnames(cache)[0]
    fn.state_sort(cname_list, cache)
    
    channel = client.get_channel(channel_id)
    tester.start()
    await channel.send(fn.cmd_msg())


@tasks.loop(seconds=30)
async def tester():
    print("running tester!")

    
@client.event
async def on_message(message):
    global cmd_list
    if message.author == client.user:
        return
    
    
    ticker = ""
    msg = message.content
    cname_list = fn.list_cnames(cache)[0]
    
    
    

    
    

    
    
    
    
                
                
    if msg.startswith('/menu'):
        await message.channel.send(fn.cmd_msg())
    if msg.startswith('/listproto'):
        await message.channel.send(', '.join(cname_list))
        
    if msg.startswith('/active'):
        if 'active_list' in cache:
            await message.channel.send('\n'.join(cache['active_list']))
        else:
            fn.state_sort(cname_list, cache)
            await message.channel.send('\n'.join(cache['active_list']))
    if msg.startswith('/que'):
        if 'queued_list' in cache:
            await message.channel.send('\n'.join(cache['queued_list']))
        else:
            fn.state_sort(cname_list, cache)
            await message.channel.send('\n'.join(cache['queued_list']))
    if msg.startswith('/canceled'):
        if 'canceled_list' in cache:
            await message.channel.send('\n'.join(cache['canceled_list']))
        else:
            fn.state_sort(cname_list, cache)
            await message.channel.send('\n'.join(cache['canceled_list']))
    if msg.startswith('/changed'):
        if 'changed_list' in cache:
            await message.channel.send('\n'.join(cache['changed_list']))
        else:
            fn.state_sort(cname_list, cache)
            await message.channel.send('\n'.join(fn.chg_msg(cache['changed_list'])))
            
    if '$' in msg[0]:
        for tick in cmd_list:
            if msg.startswith(tick):
                ticker = tick  
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
            
        if msg in cmd_list:
            ticker = msg            
            proto['price'] = br.get_price(cname)[cname]['usd']
            await message.channel.send(fn.proto_msg(proto))
        
        

try:
    client.run(config('DISCORD_BOT'))
except KeyboardInterrupt:
    client.close()
    