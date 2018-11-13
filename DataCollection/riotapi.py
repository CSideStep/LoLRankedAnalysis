import requests
from datetime import datetime
from riot_constants import EUW, NA
from riot_classes import Account

class RiotApi:
    key:str
    calls:int=0

    def __init__(self):
        self.update_credentials()

    def update_credentials(self):
        with open("credentials.txt") as f:
            txt = [line for line in f]
            self.key=txt[0]

    def print_key(self):
        print(self.key)

    def get_acc_by_name(self, name:str, region:str):
        self.calls += 1
        name =  name.replace(" ", "%20")
        json = requests.get(f"https://{region}.api.riotgames.com/lol/summoner/v3/summoners/by-name/{name}?api_key={self.key}").json()
        return Account(json["name"], json["accountId"], json["id"], int(json["revisionDate"]/1000), region)        

    def get_rank(self, acc:Account,soloq:bool=True):
        self.calls += 1
        json = requests.get(f"https://{acc.region}.api.riotgames.com/lol/league/v3/positions/by-summoner/{acc.id}?api_key={self.key}").json()
        for queue in json:
            if soloq:
                if queue["queueType"] == "RANKED_SOLO_5x5":
                    return queue["tier"] + " " + queue["rank"]
            else:
                if queue["queueType"] == "RANKED_FLEX_SR":
                    return queue["tier"] + " " + queue["rank"]
        return "unranked I"

    def get_matchlist(self, acc:Account, number_of_games:int):
        self.calls += 1
        if number_of_games < 100:
            json = requests.get(f"https://{acc.region}.api.riotgames.com/lol/match/v3/matchlists/by-account/{acc.acc_id}?endIndex={number_of_games}&api_key={self.key}").json()
        else:
            json = requests.get(f"https://{acc.region}.api.riotgames.com/lol/match/v3/matchlists/by-account/{acc.acc_id}?api_key={self.key}").json()
        matches = json["matches"]
        while len(matches) < number_of_games:
            self.calls += 1
            json2 = requests.get(f"https://{acc.region}.api.riotgames.com/lol/match/v3/matchlists/by-account/{acc.acc_id}?beginIndex={len(matches)}&api_key={self.key}").json()
            matches.extend(json2["matches"])
        return matches
    
    def get_match(self, id:int, region:str=EUW):
        self.calls += 1
        json = requests.get(f"https://{region}.api.riotgames.com/lol/match/v3/matches/{id}?api_key={self.key}").json()
        return json

    

    def get_players_by_match(self, id:int, region:str=EUW, acc:Account=None):
        players = []
        pI = self.get_match(id, region)["participantIdentities"]
        if acc != None:
            players.append(acc)
            for player in pI:
                tmp = player["player"]
                if tmp["accountId"] != acc.acc_id:
                    players.append(Account(tmp["summonerName"], tmp["accountId"], tmp["summonerId"], tmp["revisionDate"], tmp["platformId"]))
        else:
            for player in pI:
                tmp = player["player"]
                players.append(Account(tmp["summonerName"], tmp["accountId"], tmp["summonerId"], tmp["platformId"]))
        return players

if __name__ == "__main__":
    rapi = RiotApi()
    rapi.update_credentials()
    rapi.print_key() 
    acc1 = rapi.get_acc_by_name("C SideStep", EUW)
    print(acc1)
    #ts = str(ts-3628800000)
    #print(datetime.fromtimestamp(int(str(ts)[:-3])))
    #print(rapi.get_match(3758727935, EUW))
    #print(len(rapi.get_players_by_match(3758727935, acc=acc1)))