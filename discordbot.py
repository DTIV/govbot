import discord
from discord.ext import tasks
from decouple import config
import boardroom as br
import functions as fn
import random

cache = {}
channel_id = int(config('CHANNEL_ID'))
client = discord.Client()
cmd_list = fn.list_cnames(cache)[1]
cname_list = fn.list_cnames(cache)[0]


@client.event
async def on_ready():
    reseter.start()
    channel = client.get_channel(channel_id)
    print("Bot Starting Up!")
    await channel.send("Bot Starting Up!")
    fn.state_sort(cname_list, cache)
    await channel.send(fn.cmd_msg())
    looper.start()
    checker.start()
    updater.start()
    
    
@tasks.loop(minutes=5)
async def looper():
    channel = client.get_channel(channel_id)
    fn.cache_reset(cache)
    active, que, canceled, closed, executed, changed = fn.state_sort(cname_list, cache)
    if changed: 
        chg = fn.chg_msg(changed)
        await channel.send('\n'.join(chg))
        cache['changed_list'] = []

@tasks.loop(minutes=10)
async def checker():
    channel = client.get_channel(channel_id)
    complete = []
    if 'set_tickers' in cache:
        for sett in cache['set_tickers']:
            ac = fn.get_active_cname(sett, cache)
            qu = fn.get_que_cname(sett, cache)
            can = fn.get_canceled_cname(sett, cache)
            temp = [*ac,*qu,*can]
            complete.append(temp)
    if complete:
        newset = fn.get_random_set(complete)
        if 'content' in newset:
            content = newset['content'][:2000]
            if len(content) < 2000:
                ns = fn.prop_msg(newset)
                await channel.send(f"{newset['protocol']} - SET UPDATE\n {ns}\nCONTENT\n {content}")
        else:
            await channel.send(f"{newset['protocol']} - SET UPDATE\n {fn.prop_msg(newset)}")

@tasks.loop(minutes=60)
async def updater():
    channel = client.get_channel(channel_id)
    choice = random.choice([1,2,3])
    title = "ONE HOUR RANDOM ACTIVE PROPOSAL UPDATE TIME"
    if choice == 1:
        if 'active' in cache:
            newset = fn.get_random_set(cache['active'])
            if 'content' in newset:
                content = newset['content'][:2000]
                if len(content) < 2000:
                    ns = fn.prop_msg(newset)
                    await channel.send(f"{title}\n\n{ns}\nCONTENT\n\n{content}")
            else:
                await channel.send(fn.prop_msg(newset))
    elif(choice==2):
        if 'queued' in cache:
            newset = fn.get_random_set(cache['queued'])
            if 'content' in newset:
                content = newset['content'][:2000]
                if len(content) < 2000:
                    ns = fn.prop_msg(newset)
                    await channel.send(f"{title}\n\n{ns}\nCONTENT\n\n{content}")
            else:
                await channel.send(fn.prop_msg(newset))
    else:
        if 'canceled' in cache:
            newset = fn.get_random_set(cache['canceled'])
            if 'content' in newset:
                content = newset['content'][:2000]
                if len(content) < 2000:
                    ns = fn.prop_msg(newset)
                    await channel.send(f"{title}\n\n{ns}\nCONTENT\n\n{content}")
            else:
                await channel.send(fn.prop_msg(newset))
                
@tasks.loop(hours=24)
async def reseter():
    cache = {}
     
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
                if sec_command == 'active':
                    active = fn.get_active_cname(cname, cache)
                    ac_list = fn.state_msg(active)
                    await message.channel.send("\n".join(ac_list)) 
                if sec_command == 'que':
                    que = fn.get_que_cname(cname, cache)
                    ac_list = fn.state_msg(que)
                    await message.channel.send('\n'.join(ac_list))
                if sec_command == 'canceled':
                    canceled = fn.get_canceled_cname(cname, cache)
                    ac_list = fn.state_msg(canceled)
                    await message.channel.send('\n'.join(ac_list))   
                if sec_command == 'set':
                    fn.cname_set(cname, cache)
                    await message.channel.send(f"{cname} set!")  
                if sec_command == 'clear':
                    fn.cname_clear(cname, cache)
                    await message.channel.send(f"{cname} cleared") 
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
    