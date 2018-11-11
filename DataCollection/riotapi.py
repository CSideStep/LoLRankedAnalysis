import requests
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

    def get_id_by_name_region(self, name:str, region:str):
        name =  name.replace(" ", "%20")
        my_request = f"https://{region}.api.riotgames.com/lol/summoner/v3/summoners/by-name/{name}?api_key={self.key}"
        return int(requests.get(my_request).json()["id"])

    def get_id_by_name_euw(self, name:str):
        return self.get_id_by_name_region(name, "euw1")

    def get_id_by_name_na(self, name:str):
        return self.get_id_by_name_region(name, "na1")    

    def get_rank_by_id(self, id:int, region:str="euw1",soloq:bool=True):
        json = requests.get(f"https://{region}.api.riotgames.com/lol/league/v3/positions/by-summoner/{id}?api_key={self.key}").json()
        for queue in json:
            if queue["queueType"] == "RANKED_SOLO_5x5":
                return queue["tier"] + " " + queue["rank"]
        return "unranked I"

    def get_rank_by_name(self, name:str, region:str="euw1",soloq:bool=True):
        id = self.get_id_by_name_region(name, region)
        return self.get_rank_by_id(id, region, soloq)

if __name__ == "__main__":
    rapi = RiotApi()
    rapi.update_credentials()
    rapi.print_key() 
    id = rapi.get_id_by_name_euw("C SideStep")
    print(rapi.get_rank_by_id(id))
    print(rapi.get_rank_by_name("Alien Mazort"))