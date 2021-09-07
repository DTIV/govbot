import json
from requests import get

def get_price(cname):
   cg_url = f"https://api.coingecko.com/api/v3/simple/price?ids={cname}&vs_currencies=usd"
   price = get(cg_url).json()
   return price

def get_proto(cache):
    '''
    Get all protocols of boardroom
    '''
    temp = {}
    if 'protocols' in cache:
        return cache
    else:
        url = "https://api.boardroom.info/v1/protocols"
        protocols = get(url).json()
        temp['all'] = protocols['data']
        cache['protocols'] = temp
    return protocols['data']

def get_single_proto(cname, cache):
    '''
    Get all proposals for a protocol
    '''
    if 'protocols' in cache:
        if f'{cname}' in cache['protocols']:
            return cache['protocols'][cname]
        else:
            url = "https://api.boardroom.info/v1/protocols/" + cname
            protocol = get(url).json()
            cache['protocols'][cname] = protocol['data']
            return protocol['data']
    else:
        get_proto(cache)
        url = "https://api.boardroom.info/v1/protocols/" + cname
        protocol = get(url).json()
        cache['protocols'][cname] = protocol['data']
        return protocol['data']

def get_prop(cache):
    '''
    Get proposals across all protocols
    '''
    temp={}
    if 'proposals' in cache:
        return cache
    else:
        url = "https://api.boardroom.info/v1/proposals"
        prop = get(url).json()
        temp['all'] = prop['data']
        cache['proposals'] = temp
    return prop

def get_prop_by_cname(cname, cache):
    '''
    Get all proposals for a protocol
    '''
    if 'proposals' in cache:
        if f"{cname}" in cache['proposals']:
            return cache['proposals'][cname]
        else:
            url = "https://api.boardroom.info/v1/protocols/"+cname+"/proposals"
            prop = get(url).json()
            cache['proposals'][cname] = prop['data']
            return prop['data']
    else:
        get_prop(cache)
        url = "https://api.boardroom.info/v1/protocols/"+cname+"/proposals"
        prop = get(url).json()
        cache['proposals'][cname] = prop['data']
        return prop['data']

def get_prop_by_refid(refid, cache):
    '''
    Get a single proposal
    '''
    url = "https://api.boardroom.info/v1/proposals/"+refid
    prop = get(url).json()
    return prop['data']

def get_voters(cache):
    '''
    Get voters across all protocols
    '''
    temp = {}
    if 'voters' in cache:
        return cache
    else:
        url = "https://api.boardroom.info/v1/voters"
        votes = get(url).json()
        temp['all'] = votes['data']
        cache['voters'] = temp
    return votes

def get_prop_votes(refid, cache):
    url = "https://api.boardroom.info/v1/proposals/"+refid+"/votes"
    prop = get(url).json()
    name = prop['data'][0]['protocol']
    temp_cache = {}
    temp_cache[name] = prop['data']
    cache['proposal_refid'] = temp_cache
    return prop

def get_voters_cname(cname, cache):
    '''
    Get all voters for a protocol
    '''
    if 'voters' in cache:
        if f"{cname}" in cache['voters']:
            return cache['voters'][cname]
        else:
            url = "https://api.boardroom.info/v1/protocols/"+cname+"/voters"
            votes = get(url).json()
            cache['voters'][cname] = votes['data']
            return votes['data']
    else:
        get_voters(cache)
        url = "https://api.boardroom.info/v1/protocols/"+cname+"/voters"
        votes = get(url).json()
        cache['voters'][cname] = votes['data']
        return votes['data']
        
def get_voters_votes(addr, cache):
    '''
    Get votes by voter
    '''
    temp_cache = {}
    url = "https://api.boardroom.info/v1/voters"+addr
    votes = get(url).json()
    name = votes['data']['name']
    temp_cache[name] = votes['data']
    cache['voters_vote'] = temp_cache
    return votes

def get_voters_addr(addr, cache):
    '''
    Get details for a specific voter
    '''
    temp_cache = {}
    url = "https://api.boardroom.info/v1/voters"+addr
    votes = get(url).json()
    name = votes['data']['name']
    temp_cache[name] = votes['data']
    cache['votes_addr'] = temp_cache
    return votes

def get_stats(cache):
    '''
    Get global platform stats
    '''
    url = "https://api.boardroom.info/v1/stats"
    stats = get(url).json()
    cache['stats'] = stats['data']
    return stats
     