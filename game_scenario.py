class GameState:
    def __init__(self):
        self.year = 1957
        self.phrase = {
            1957: "First Sputnik",
            1961: "Gagarin flew!",
            1969: "Armstrong got on the moon!",
            1971: "First orbital space station Salute-1",
            1981: "Flight of the Shuttle Columbia",
            1998: "ISS start building",
            2011: "Messenger launch to Mercury",
            2020: "Take the plasma gun! Shoot the garbage!",
        }
        self.can_fire = False

    def get_garbage_delay_tics(self):
        if self.year < 1961:
            return None
        elif self.year < 1969:
            return 20
        elif self.year < 1981:
            return 14
        elif self.year < 1995:
            return 10
        elif self.year < 2010:
            return 8
        elif self.year < 2020:
            return 6
        else:
            self.can_fire = True
            return 2


game_state = GameState()
