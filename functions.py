
import boardroom as br
from datetime import timedelta, datetime


def cache_reset(cache):
    '''
    Resets cache and updates data returns cache back
    '''
    dt = datetime.now()
    dt_tom = datetime.now() + timedelta(days=1)
    if dt > dt_tom:
        cache = {}
        return cache
    return cache

def list_cnames(cache):
    '''
    Creates lists and returns
    cnames and ticker
    '''
    clist = []
    cmdlist = []
    if 'protocols' in cache:
        temp = cache['protocols']
    else:
        br.get_proto(cache)
        temp = cache['protocols']
    for cname in range(len(temp['all'])):
        ticker = temp['all'][cname]['cname']
        clist.append(ticker)
        cmdlist.append(f"${ticker}")
    return clist, cmdlist

def get_proposal_lists(props, counter=False):
    '''
    Creates lists for proposal data
    returns title_list, refid_list
    '''
    title_list, refid_list = [],[]
    count = 0
    for ref in props:
        count += 1
        if counter:
            title_list.append(f"{count}. {ref['title']}")
            refid_list.append(f"{count}. {ref['refId']}")
        else:
            title_list.append(ref['title'])
            refid_list.append(ref['refId'])
    return title_list, refid_list
        
def get_prop_by_title(props, title):
    '''Get proposal by title name 
    returns dict'''
    for ref in props:
        if ref['title'] == title:
            return ref

def get_prop_by_ref(props, refid):
    '''Get proposal by ref ID 
    returns dict'''
    for ref in props:
        if ref['refId'] == refid:
            return ref
        

def cmd_msg():
    return """
COMMANDS
--------------------
/menu : List of commands
/listproto : list of available protocols
--------------------
$(protocol) : all data from specified protocol
$(protocol) proposals : lists all proposal titles for protocol
$(protocol) refid: lists all proposal ref IDs
$(protocol) contract: get contract address and network
--------------------
$(protocol) (title): gets specific proposal data
$(protocol) (ref ID): gets specific proposal data
"""
def proto_msg(proto):
    return f'''
{proto['name']}
--------------------
Current Price: {proto['price']}
Total Proposals: {proto['totalProposals']}
Total Votes: {proto['totalVotes']}
Unique Voters: {proto['uniqueVoters']}'''

def prop_msg(ref):
    results = ref['results']
    choice = results[0]['choice']
    total = results[0]['total']
    if len(results) <= 1:
        if choice == 0:
            nay = total
            yae = 0
        elif choice == 1:
            yae = ref['results'][0]['total']
            nay = 0
    else:
        nay = total
        yae = results[1]['total']
        
    start_ts = ref['startTimestamp']
    end_ts = ref['endTimestamp']
    dt_start = datetime.fromtimestamp(start_ts)
    dt_end = datetime.fromtimestamp(end_ts)
    bs = ref['startTime']['blockNumber']
    be = ref['endTime']['blockNumber']
    return f'''
{ref['title']}
--------------------
Ref ID: {ref['refId']}
Current State: {ref['currentState']}
Start: {dt_start}
End: {dt_end}

Block Start: {bs}
Block End: {be}

RESULTS
--------------------
NAY : {nay}
YAE : {yae}'''

def ca_msg(proto):
    try: 
        return f'''
Network: {proto['tokens'][0]['network']}
Contract: {proto['tokens'][0]['contractAddress']}'''
    except:
        return f'''No Contract Found'''