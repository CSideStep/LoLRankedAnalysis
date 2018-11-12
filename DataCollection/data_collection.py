import riotapi
from riot_classes import Account
from riot_constants import EUW, NA
def main():
    rapi = riotapi.RiotApi()
    
def build_data_base(inital_acc:Account, active_players:int, rapi:riotapi.RiotApi):
    accs = []
    while len(accs) < active_players:
        rapi.get_matchlist()

def append_data_base():
    pass

def loop():
    pass

if __name__ == "__main__":
    main()

