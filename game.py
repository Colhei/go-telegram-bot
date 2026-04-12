class Cell():
    def __init__( self, status="cross", color="blank", available=True ):
            self.status = status
            self.color = color
            self.available = available

        def return_info(self, info):
            match info:
                case "coord":
                    return self.coord
                case "color":
                    return self.color
                case "status":
                    return self.status
                case "available":
                    return self.available
                case _ :
                    return None


########################################### ГРА ######################################################

table = []

def Start_game():
    pass

def _gen_table():

