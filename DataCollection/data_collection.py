import riotapi
from riot_classes import Account
from riot_constants import EUW, NA, WEEK
from time import sleep
from datetime import datetime
def main():
    rapi = riotapi.RiotApi()
    acc1 = rapi.get_acc_by_name("C SideStep", EUW)
    build_data_base(acc1, 50, rapi)

def isActive(player:Account, threshold:int=WEEK):
        return datetime.timestamp(datetime.now())-player.revisionDate <= threshold

def build_data_base(inital_acc:Account, active_players:int, rapi:riotapi.RiotApi, threshold:int=WEEK, path:str="data.csv"):
    print("started building process")
    accs = [inital_acc]
    matches = rapi.get_matchlist(inital_acc, 100)
    print("waiting")
    sleep(120)
    for match in matches:
            print("next match")
            players = rapi.get_players_by_match(match["gameId"], acc=inital_acc)
            accs.append(filter(isActive, players))
            if len(accs) >= active_players:
                    break        
    with open(path, "a") as f:
        for acc in accs:
            f.write(f"{acc.name},{acc.acc_id},{acc.id},{acc.revisionDate},{acc.region}")
def append_data_base():
    pass

def loop():
    pass

if __name__ == "__main__":
    main()

