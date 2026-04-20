import asyncio
import os

class Cell():
    def __init__( self, status="cross", available=True ):
            self.status = status
            self.available = available

    def return_info(self, info):
        match info:
            case "status":
                return self.status
            case "available":
                return self.available
        return None

class Counting_cell():
    def __init__(self):
        self.status = ["blank", "balnk"]
        self.countable = True

########################################### ГРА ######################################################

TURN = 0

PLAYERS = []

PENDING_GAMES_INFO = {}             # у форматі { ( 1гравець, 2гравець ) : [ [черга], [ *стіл* ] ] }
PENDING_GAMES_CAPTURED = {}         # у форматі { ( 1гравець, 2гравець ) : [ полонені1, полонені2 ] }
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
    table_size = len(table)
    result = ""
    printablel = [ "A", "B", "C", "D", "E", "F", "G", "H", "I " ]
    printable = [ "9️⃣", "8️⃣", "7️⃣", "6️⃣", "5️⃣", "4️⃣", "3️⃣", "2️⃣", "1️⃣" ]
    for i in range(8, -1, -1):
        result += printable[i]
    result += "⏹️"
    result += "\n"
    for i in range(table_size):
        for j in range(table_size):
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
        result += f"|{printablel[i]}|\n"
    return result

def _analyze_group(players_tuple, coord, color, visited=None):
    if visited == None:
        visited = []
    visited.append(coord)
    table = PENDING_GAMES_INFO[players_tuple][1]
    coord_lt = (coord[0]-1, coord[1])
    coord_up = (coord[0], coord[1]-1)
    coord_rt = (coord[0]+1, coord[1])
    coord_dn = (coord[0], coord[1]+1)
    result_up = False
    result_lt = False
    result_rt = False
    result_dn = False
    if coord_up[1] >= 0 and not coord_up in visited:
        if table[coord_up[0]][coord_up[1]].return_info("status") == color:
            result_up = _analyze_group(players_tuple, coord_up, color, visited)
        elif table[coord_up[0]][coord_up[1]].return_info("status") == "cross":
            return True
    if coord_lt[0] >= 0 and not coord_lt in visited:
        if table[coord_lt[0]][coord_lt[1]].return_info("status") == color:
            result_lt = _analyze_group(players_tuple, coord_lt, color, visited)
        elif table[coord_lt[0]][coord_lt[1]].return_info("status") == "cross":
            return True
    if coord_rt[0] <= 8 and not coord_rt in visited:
        if table[coord_rt[0]][coord_rt[1]].return_info("status") == color:
            result_rt = _analyze_group(players_tuple, coord_rt, color, visited)
        elif table[coord_rt[0]][coord_rt[1]].return_info("status") == "cross":
            return True
    if coord_dn[1] <= 8 and not coord_dn in visited:
        if table[coord_dn[0]][coord_dn[1]].return_info("status") == color:
            result_dn = _analyze_group(players_tuple, coord_dn, color, visited)
        elif table[coord_dn[0]][coord_dn[1]].return_info("status") == "cross":
            return True
    result = result_lt or result_up or result_rt or result_dn
    return result

def _remove_group(players_tuple, coord, color, p=0, visited=None):
    if visited == None:
        visited = []
    visited.append(coord)
    table = PENDING_GAMES_INFO[players_tuple][1]
    coord_lt = (coord[0]-1, coord[1])
    coord_up = (coord[0], coord[1]-1)
    coord_rt = (coord[0]+1, coord[1])
    coord_dn = (coord[0], coord[1]+1)
    table[coord[0]][coord[1]].status = "cross"
    table[coord[0]][coord[1]].available = True
    if coord_up[1] >= 0 and not coord_up in visited:
        if table[coord_up[0]][coord_up[1]].return_info("status") == color:
            result_up = _remove_group(players_tuple, coord_up, color, p+1, visited)
    if coord_lt[0] >= 0 and not coord_lt in visited:
        if table[coord_lt[0]][coord_lt[1]].return_info("status") == color:
            result_lt = _remove_group(players_tuple, coord_lt, color, p+1, visited)
    if coord_rt[0] <= 8 and not coord_rt in visited:
        if table[coord_rt[0]][coord_rt[1]].return_info("status") == color:
            result_rt = _remove_group(players_tuple, coord_rt, color, p+1, visited)
    if coord_dn[1] <= 8 and not coord_dn in visited:
        if table[coord_dn[0]][coord_dn[1]].return_info("status") == color:
            result_dn = _remove_group(players_tuple, coord_dn, color, p+1, visited)
    result = p + result_lt + result_up + result_rt + result_dn
    return result

def _analyze_table(players_tuple):
    table = PENDING_GAMES_INFO[players_tuple][1]
    captures = PENDING_GAMES_CAPTURED[players_tuple]
    for i in range(len(table)):
        for j in range(len(table)):
            cross_status = table[i][j].return_info("status")
            if cross_status != "cross":
                analyze_result = _analyze_group(players_tuple, (i, j), cross_status)
                if not analyze_result:
                    print(f"found a dead group. deleting it from the desk")
                    color = table[i][j].return_info("status")
                    dead_group = _remove_group(players_tuple, (i, j), cross_status)
                    if color == "black":
                        captures[0] += dead_group
                    else:
                        captures[1] += dead_group
                    print(f"added {dead_group} of stones to captures for {players_tuple[0] if color == "black" else players_tuple[1]}")

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

def Make_move(current_player, destination):                 # назначення у форматі ( число_стовпця, 'буква_рядка' )
    letter = int(ord(destination[1].lower()))-97
    number = int(destination[0])-1
    dest = (letter, number)
    color = ""
    for key in PENDING_GAMES:
        if current_player == key:
            color = "black"
            players_tuple = (key, PENDING_GAMES[key])
        elif current_player == PENDING_GAMES[key]:
            color = "white"
            players_tuple = (key, PENDING_GAMES[key])
    
    turn = PENDING_GAMES_INFO[players_tuple][0]
    if turn[0][0] == "p":
        turn[0] = "white" if turn[0] == "pwhite" else "black"
    if turn[0] == color:
        table = PENDING_GAMES_INFO[players_tuple][1]
        if table[dest[0]][dest[1]].available:
            table[dest[0]][dest[1]].status = color
            table[dest[0]][dest[1]].available = False
            print(f"{current_player} successfully made a move - {color} to the {dest[0]} - {dest[1]}")
            turn[0] = "white" if turn[0] == "black" else "black"
            _analyze_table(players_tuple)
            return f"Ви зробили хід, очікуємо на відповідь гравця {players_tuple[0] if turn[0] == "black" else players_tuple[1]}"
        else:
            print(f"error upon trying to make a move by {current_player}")
            _analyze_table(players_tuple)
            return f"Неможливий хід, спробуйте походити у інше місце"
    else:
        print(f"player tryed to make a move out of order")
        _analyze_table(players_tuple)
        return f"Ще не ваш хід. Дочекайтеся суперника та зробіть хід після нього"

def Pass_turn(player):
    for key in PENDING_GAMES:
        if player == key:
            color = "white"
            players_tuple = (key, PENDING_GAMES[key])
        elif player == PENDING_GAMES[key]:
            color = "black"
            players_tuple = (key, PENDING_GAMES[key])
        else:
            print(f"player {player} can not pass their turn. Did not find their table")
            return f"Неможливо пропустити хід, не граючи жодної гри."
    turn = PENDING_GAMES_INFO[players_tuple][0]
    if turn[0][0] == "p":
        if "p"+color != turn:
            print(f"player {player} can not pass their turn. Not their turn.")
            return f"Неможливо пропустити хід. Ще не ваша черга."
        print(f"player {player} passed his turn, ending the game")
        return Finnish_game(players_tuple)
    else:
        turn[0] = "pwhite" if turn[0] == "black" else "pblack"
        print(f"player {player} passed their turn. Waiting for the opponent's respond.")
        return f"Ви пропустили хід. Далі хід {players_tuple[0] if turn[0] == "black" else players_tuple[1]}"

def Start_game(table_size=9, player1="player1", player2="player2"):
    players_tuple = (player1, player2) 
    PENDING_GAMES_INFO[players_tuple] = [ ["black"], _gen_table(table_size) ]
    PENDING_GAMES_CAPTURED[players_tuple] = [0, 0]
    print(f"added {player1} & {player2}'s game to the dictionary")
    print(players_tuple)
    print(PENDING_GAMES_INFO[players_tuple])
    
def _finnish_game(players_tuple):
    PENDING_GAMES.pop(players_tuple[0])
    PENDING_GAMES_INFO.pop(players_tuple)
    PENDING_GAMES_CAPTURED.pop(players_tuple)
    print(f"the game of {players_tuple[0]} and {players_tuple[1]} has ended. Cleared info of their game.")
    return f"Ви пропустили хід, гру завершено."

