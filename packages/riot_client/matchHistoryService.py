import requests

class MatchHistoryService():

    def __init__ (self, api_key):
        self.api_key = api_key
        self.matchesCache = {}

    def accountByNameEndpoint(self, summoner_name:str, tag_line:str) -> dict:
        get_account_by_name_endpoint = 'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{}/{}'.format(summoner_name, tag_line)
        r = requests.get(get_account_by_name_endpoint, headers = {'x-riot-token': self.api_key})
        return r.json()
    
    def matchesByPuuidEndpoint(self, puuid) -> dict:
        get_matches_by_puuid_endpoint = 'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?queue=420&count=20'.format(puuid)
        r = requests.get(get_matches_by_puuid_endpoint, headers = {'x-riot-token': self.api_key})
        return r.json()
    
    def matchByMatchIdEndpoint(self, matchId) -> dict:
        if matchId in self.matchesCache:
            return self.matchesCache[matchId]
        get_match_from_matchId_endpoint = 'https://americas.api.riotgames.com/lol/match/v5/matches/{}'.format(matchId)
        match = requests.get(get_match_from_matchId_endpoint, headers={'x-riot-token': self.api_key})
        self.matchesCache[matchId] = match.json()
        return self.matchesCache[matchId]
    
    def participantsByMatchIdEndpoint(self, matchId) -> dict:
        get_participants_from_matchId_endpoint = 'https://americas.api.riotgames.com/lol/match/v5/matches/{}'.format(matchId)
        participants = requests.get(get_participants_from_matchId_endpoint, headers={'x-riot-token': self.api_key})
        return participants.json()['info']['participants']
    
    def summonerIdByPuuidEndpoint(self, puuid) -> dict:
        get_summonerId_from_puuid_endpoint = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{}'.format(puuid)
        summoner = requests.get(get_summonerId_from_puuid_endpoint, headers={'x-riot-token': self.api_key})
        return summoner.json()['id']
    
    def rankBySummonerIdEndpoint(self, summonerId) -> dict:
        get_rank_from_summonerId_endpoint = 'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{}'.format(summonerId)
        ranks = requests.get(get_rank_from_summonerId_endpoint, headers={'x-riot-token': self.api_key})
        return ranks.json()  #[1]['tier']    
    #the [1] index was assumed to call RANKED_SOLO queue, however, this is only true if account has recent Normal Games played, otherwise soloq index would be [0]
    #likewise, if the player has only played one type of queue at all, then this queue will be the [0] index
    #this is why the specific check is implemented in ingestions.py
