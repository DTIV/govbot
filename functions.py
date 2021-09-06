
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
      
def get_active(prop, cache):
    '''
    Gets and updates active proposals
    Returns title and sets to cache 
    '''

    if 'active' in cache:
        if prop['currentState'] == 'active':
            cache['active'].append(prop)
            return prop['title']
        else:
            if prop in cache['active']:
                cache['active'].remove(prop)
                prop['changed_from'] = 'active'
                return prop
    else:
        cache['active'] = []
        if prop['currentState'] == 'active':
            cache['active'].append(prop)
            return prop['title']
        else:
            if prop in cache['active']:
                cache['active'].remove(prop)
                prop['changed_from'] = 'active'
                return prop
    

def get_queued(prop, cache):
    '''
    Gets and updates queded proposals
    Returns title and sets to cache
    '''
    if 'queued' in cache:
        if prop['currentState'] == 'queued':
            cache['queued'].append(prop)
            return prop['title']
        else:
            if prop in cache['queued']:
                cache['queued'].remove(prop)
                prop['changed_from'] = 'queued'
                return prop
    else:
        cache['queued'] = []
        if prop['currentState'] == 'queued':
            cache['queued'].append(prop)
            return prop['title']
        else:
            if prop in cache['queued']:
                cache['queued'].remove(prop)
                prop['changed_from'] = 'queued'
                return prop

def get_canceled(prop, cache):
    '''
    Gets and updates canceled proposals
    Returns title and to cache
    '''
    if 'canceled' in cache:
        if prop['currentState'] == 'canceled':
            cache['canceled'].append(prop)
            return prop['title']
        else:
            if prop in cache['canceled']:
                cache['canceled'].remove(prop)
                prop['changed_from'] = 'canceled'
                return prop
    else:
        cache['canceled'] = []
        if prop['currentState'] == 'canceled':
            cache['canceled'].append(prop)
            return prop['title']
        else:
            if prop in cache['canceled']:
                cache['canceled'].remove(prop)
                prop['changed_from'] = 'canceled'
                return prop

def get_closed(prop, cache):
    '''
    Gets and updated closed proposals 
    Returns title and to cache
    '''
    if 'closed' in cache:
        if prop['currentState'] == 'closed':
            cache['closed'].append(prop)
            return prop['title']
        else:
            if prop in cache['closed']:
                cache['closed'].remove(prop)
                prop['changed_from'] = 'closed'
                return prop
    else:
        cache['closed'] = []
        if prop['currentState'] == 'closed':
            cache['closed'].append(prop)
            return prop['title']
        else:
            if prop in cache['closed']:
                cache['closed'].remove(prop)
                prop['changed_from'] = 'closed'
                return prop

def get_executed(prop, cache):
    '''
    Gets and updates executed proposals 
    Returns title and to cache
    '''
    if 'executed' in cache:
       if prop['currentState'] == 'executed':
           cache['executed'].append(prop)
           return prop['title']
       else:
           if prop in cache['executed']:
               cache['executed'].remove(prop)
               prop['changed_from'] = 'executed'
               return prop
    else:
        cache['executed'] = []
        if prop['currentState'] == 'executed':
            cache['executed'].append(prop)
            return prop['title']
        else:
            if prop in cache['executed']:
                cache['executed'].remove(prop)
                prop['changed_from'] = 'executed'
                return prop



def state_sort(cname_list, cache):
    '''
    Parameters
    ----------
    cname_list : List
    cache : dict

    Returns
    -------
    active : List
    que : List
    canceled : List
    closed : List
    exc : List.

    '''
    active, que, canceled, closed, executed, changed = [],[],[],[],[],[]
    for i in cname_list:
        props = br.get_prop_by_cname(i,cache)
        for prop in props:
            ac = get_active(prop, cache)
            qu = get_queued(prop, cache)
            ca = get_canceled(prop, cache)
            cl = get_closed(prop, cache)
            ex = get_executed(prop, cache)
            if ac:
                if 'changed_from' in ac:
                    changed.append(ac)
                else:
                    active.append(ac)
            if qu:
                if 'changed_from' in qu:
                    changed.append(qu)
                else:
                    que.append(qu)
            if ca:
                if 'changed_from' in ca:
                    changed.append(ca)
                else:
                    canceled.append(ca)
            if cl:
                if 'changed_from' in cl:
                    changed.append(cl)
                else:
                    closed.append(cl)
            if ex:
                if 'changed_from' in ex:
                    changed.append(ex)
                else:
                    executed.append(ex)
    cache['active_list'] = active
    cache['queued_list'] = que
    cache['canceled_list'] = canceled
    cache['closed_list'] = closed
    cache['executed_list'] = executed
    cache['changed_list'] = changed
    
    return active, que, canceled, closed, executed, changed

def cmd_msg():
    return """
COMMANDS
--------------------
/menu : List of commands
/listproto : list of available protocols
--------------------
/active: List of all active proposals
/que: List of all queued proposals
/canceled: List of all canceled proposals
/changed: List of changed proposals that have changed status
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
        return '''No Contract Found'''
    
def chg_msg(change_list):
    temp = []
    if change_list:
        for i in change_list:
            protocol = i['protocol']
            state = i['currentState']
            past = i['changed_from']
            new_str = f"{protocol} protocol changed from {past} to {state}"
            temp.append(new_str)
    else:
        temp.append("No Changed Detected")
    return temp