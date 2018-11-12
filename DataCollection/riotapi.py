import requests
from datetime import datetime
from riot_constants import EUW, NA
from riot_classes import Account

class RiotApi:
    key:str

    def __init__(self):
        self.update_credentials()

    def update_credentials(self):
        with open("credentials.txt") as f:
            txt = [line for line in f]
            self.key=txt[0]

    def print_key(self):
        print(self.key)

    def get_acc_by_name(self, name:str, region:str):
        name =  name.replace(" ", "%20")
        json = requests.get(f"https://{region}.api.riotgames.com/lol/summoner/v3/summoners/by-name/{name}?api_key={self.key}").json()
        return Account(json["name"], json["accountId"], json["id"], region)        

    def get_rank(self, acc:Account,soloq:bool=True):
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
        json = requests.get(f"https://{acc.region}.api.riotgames.com/lol/match/v3/matchlists/by-account/{acc.acc_id}?api_key={self.key}").json()
        matches = json["matches"]
        while len(matches) < number_of_games:
            json2 = requests.get(f"https://{acc.region}.api.riotgames.com/lol/match/v3/matchlists/by-account/{acc.acc_id}?beginIndex={len(matches)}&api_key={self.key}").json()
            matches.extend(json2["matches"])
        print(matches[len(matches)-1])
        return matches
    
    def get_match(self, id:int, region:str=EUW):
        json = requests.get(f"https://{region}.api.riotgames.com/lol/match/v3/matches/{id}?api_key={self.key}").json()
        return json

    def get_players_by_match(self, id:int, region:str=EUW):
        self.get_match(id, region)

if __name__ == "__main__":
    rapi = RiotApi()
    rapi.update_credentials()
    rapi.print_key() 
    acc1 = rapi.get_acc_by_name("C SideStep", EUW)
    #ts = rapi.get_matchlist(acc1, 500)[0]["timestamp"]
    #ts = str(ts-3628800000)
    #print(datetime.fromtimestamp(int(str(ts)[:-3])))
    print(rapi.get_match(3758727935, EUW))