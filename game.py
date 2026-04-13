import asyncio
import os

class Cell():
    def __init__( self, status="cross", available=True ):
            self.status = status
            self.available = available

    def return_info(self, info):
        match info:
            case "coord":
                return self.coord
            case "status":
                return self.status
            case "available":
                return self.available
        return None


########################################### ГРА ######################################################

TURN = 0

PLAYERS = []

PENDING_GAMES_INFO = {}             # у форматі { ( 1гравець, 2гравець ) : [ [черга], [ *стіл* ] ] }
PENDING_GAMES = {}                  # у форматі { 1гравець : 2гравець },           де 1 гравець - отримувач, чорні,
PENDING_DUEL_REQUESTS = {}          # у форматі { 1гравець : 2гравець }             а 2 гравець - відправник, білі

def _gen_table(table_size=9):
    result = []
    print("\n"+f"generating table {table_size}x{table_size}")
    for i in range(table_size):
        result.append([])
        for j in range(table_size):
            result[i].append(Cell())
    print("\n"+"table generated")
    return result

def Return_table(player):
    found = False
    for key in PENDING_GAMES:
        if key == player:
            found = True
            players_tuple = (key, PENDING_GAMES[key])
            break
        elif PENDING_GAMES[key] == player:
            found = True
            players_tuple = (key, PENDING_GAMES[key])
            break
    if not found:
        print(f"error: did not find the table of the player {player}")
        return f"Не знайдено вашого стола."
        
    table = PENDING_GAMES_INFO[players_tuple][1]
    result = ""
    printable = [ "9️⃣", "8️⃣", "7️⃣", "6️⃣", "5️⃣", "4️⃣", "3️⃣", "2️⃣", "1️⃣" ]
    result += "⏹️"
    for i in range(8, -1, -1):
        result += printable[i]
    result += "\n"
    for i in range(9):
        result += printable[i]
        for j in range(9):
            match table[i][j].return_info("status"):
                case "cross":
                    if (i == 4 and j == 4 or
                        i == 2 and j == 6 or
                        i == 6 and j == 6 or
                        i == 2 and j == 2 or
                        i == 2 and j == 6):
                        result += "➕"
                    else:
                        result += "➕"
                case "white":
                    result += "⚪️"
                case "black":
                    result += "⚫️"
        result += "\n"
    return result

def To_challenge(player1, player2):
    PENDING_DUEL_REQUESTS[player1] = player2 
    print(f"added new duel request to dictionary. players: {player1}, {player2}")
    print("here is the new updated dict:")
    print(PENDING_DUEL_REQUESTS)

def Accept_duel_request(player1, player2):
    if player1 in PENDING_DUEL_REQUESTS and PENDING_DUEL_REQUESTS[player1] == player2:
        PENDING_GAMES[player1] = player2
        print(f"found a pending duel request ({player1} : {player2}), returning to bot")
        return True
    return False

def Check_pending_games():
    print("checking pending games, here is the list:")
    result = "Ігри у процесі:\n"
    for key in PENDING_GAMES:
        result += f"{key} : {PENDING_GAMES[key]}\n"
        print(f"{key} : {PENDING_GAMES[key]}\n")
    return result

def Check_pending_requests():
    print("checking pending duel requests, here is the list:")
    result = "Дійсні запити на дуель:\n"
    for key in PENDING_DUEL_REQUESTS:
        result += f"{key} → {PENDING_DUEL_REQUESTS[key]}\n"
        print(f"{key} → {PENDING_DUEL_REQUESTS[key]}\n")
    return result

def Make_move(current_player, destination):
    dest = (int(destination[0])-1, 9-int(destination[1]))
    color = ""
    for key in PENDING_GAMES:
        if current_player == key:
            color = "black"
            players_tuple = (key, PENDING_GAMES[key])
        elif current_player == PENDING_GAMES[key]:
            color = "white"
            players_tuple = (key, PENDING_GAMES[key])
    
    order = PENDING_GAMES_INFO[players_tuple][0]
    if order[0][0] == "p":
        order[0] = "white" if order[0] == "pwhite" else "black"
    if order[0] == color:
        table = PENDING_GAMES_INFO[players_tuple][1]
        if table[dest[0]][dest[1]].available:
            table[dest[0]][dest[1]].status = color
            table[dest[0]][dest[1]].available = False
            print(f"{current_player} successfully made a move - {color} to the {dest[0]} - {dest[1]}")
            order[0] = "white" if order[0] == "black" else "black"
            return f"Ви зробили хід, очікуємо на відповідь іншого гравця"
        else:
            print(f"error upon trying to make a move by {current_player}")
            return f"Неможливий хід, спробуйте походити у інше місце"
    else:
        print(f"player tryed to make a move out of order")
        return f"Ще не ваш хід. Дочекайтеся суперника та зробіть хід після нього"

    PENDING_GAMES_INFO[players_dict]


def Start_game(table_size=9, player1="player1", player2="player2"):
    players_tuple = (player1, player2) 
    PENDING_GAMES_INFO[players_tuple] = [ ["black"], _gen_table(table_size) ]
    print(f"added {player1} & {player2}'s game to the dictionary")
    print(players_tuple)
    print(PENDING_GAMES_INFO[players_tuple])
    

def _clear_info():
    PLAYERS = []
    TABLE = []
    PENDING_GAMES = {}
    PENDING_DUEL_REQUESTS = {}
    PENDING_GAMES_INFO = {}
