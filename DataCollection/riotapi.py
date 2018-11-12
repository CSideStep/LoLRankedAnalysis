import requests
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
            if queue["queueType"] == "RANKED_SOLO_5x5":
                return queue["tier"] + " " + queue["rank"]
        return "unranked I"

    def get_matchlist(self):
        pass

if __name__ == "__main__":
    rapi = RiotApi()
    rapi.update_credentials()
    rapi.print_key() 
    acc1 = rapi.get_acc_by_name("C SideStep", EUW)
    acc2 = rapi.get_acc_by_name("Alien Mazort", EUW)
    print(rapi.get_rank(acc1))
    print(rapi.get_rank(acc2))