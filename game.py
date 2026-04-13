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

TABLE = []

PENDING_GAMES = {}                  # у форматі { 1гравець : 2гравець },           де 1 гравець - отримувач, чорні,
PENDING_DUEL_REQUESTS = {}          # у форматі { 1гравець : 2гравець }             а 2 гравець - відправник, білі

def _gen_table(table_size=9):
    print("\n"+f"generating table {table_size}x{table_size}")
    for i in range(table_size):
        TABLE.append([])
        for j in range(table_size):
            TABLE[i].append(Cell())
    print("\n"+"table generated")

def Print_table():
    result = ""
    printable = [ "9️⃣", "8️⃣", "7️⃣", "6️⃣", "5️⃣", "4️⃣", "3️⃣", "2️⃣", "1️⃣" ]
    result += "⏹️"
    for i in range(8, -1, -1):
        result += printable[i]
    result += "\n"
    for i in range(9):
        result += printable[i]
        for j in range(9):
            match TABLE[i][j].return_info("status"):
                case "cross":
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

def Make_move(current_player):
    pass

def Start_game(table_size=9, player1="player1", player2="player2"):
    _gen_table(table_size)
    PLAYERS.append(player1)
    PLAYERS.append(player2)

def _clear_info():
    PLAYERS = []
    TABLE = []
    TURN = 0
    PENDING_GAMES = {}
    PENDING_DUELS = {}
