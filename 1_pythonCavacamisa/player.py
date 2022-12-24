import random
from datetime import datetime

version = 0.3

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.other = None # The opponent player
        self.sim = None   # The parent simualtion

    def play_card(self):
        self.sim.table.receive_card(self.cards.pop(0))
        self.sim.data["Total_played_cards"] += 1


    def take_cards(self):
        cards_on_table = self.sim.table.cards.copy()
        cards_on_table.reverse()
        self.cards.extend(cards_on_table)
        self.sim.data["Total_taking"] += 1
        self.sim.table.cards = []

    def play(self, in_penal):
        penal = in_penal
        if len(self.cards) < 1:
            self.sim.data["Winner"] = self.other.name
            return "HO PERSO"
        if penal == 0:
            self.play_card()
            self.other.play(self.get_last_table_card())
            return
        if penal > 0:
            self.play_card()
            if self.get_last_table_card() < 4:
                self.other.play(self.get_last_table_card())
                return
            penal -= 1
            if penal == 0 and self.get_last_table_card() > 3:
                self.other.take_cards()
                self.sim.table.cards = []
                self.other.play(0)
                return
            self.play(penal)

    def __str__(self):
        return f"{self.name}"
# class Player

class Table:
    def __init__(self):
        self.cards = []
        self.total_received_cards = 0

    def receive_card(self, value):
        self.cards.insert(0, value)
        self.total_received_cards += 1
# class Table

class Simulation:
    def __init__(self):
        self.player1 = Player("G1")
        self.player2 = Player("G2")
        self.player1.other = self.player2
        self.player2.other = self.player1
        self.player1.sim = self
        self.player2.sim = self
        give_cards_to_player(self.player1, self.player2)
        self.players = [self.player1, self.player2]
        self.table = Table()
        self.data = {}
        self.data["Date"] = get_data_time()
        self.data["Start_card_G1"] = self.player1.cards.copy()
        self.data["Start_card_G2"] = self.player2.cards.copy()
        self.data["Total_played_cards"] = 0
        self.data["Total_taking"] = 0
        self.data["Winner"] = None

    def get_last_table_card(self):
        if len(self.table.cards) > 0:
            return self.table.cards[0]
        else:
            return 0

    def start_simulation(self):
        
        active_player = 0
        penal_cards = 0
        counter = 0

        while len(self.player1.cards) > 0 and len(self.player2.cards) > 0:
            if penal_cards == 0:
                self.players[active_player].play_card()
                counter += 1
                if len(self.player1.cards) == 0:
                    self.data["Winner"] = self.player2.name
                    break
                if len(self.player2.cards) == 0:
                    self.data["Winner"] = self.player1.name
                    break
                if self.get_last_table_card() < 4:
                    penal_cards = self.get_last_table_card()
                active_player = 0 if active_player == 1 else 1
                continue
            if penal_cards > 0:
                while penal_cards > 0:
                    if len(self.player1.cards) == 0:
                        self.data["Winner"] = self.player2.name
                        break
                    if len(self.player2.cards) == 0:
                        self.data["Winner"] = self.player1.name
                        break

                    self.players[active_player].play_card()
                    counter += 1
                    penal_cards -= 1

                    if self.get_last_table_card() < 4:
                        active_player = 0 if active_player == 1 else 1
                        penal_cards = self.get_last_table_card()
                    elif penal_cards == 0:
                        self.players[active_player].other.take_cards()
                        active_player = 0 if active_player == 1 else 1
                        penal_cards = 0
                        
            if len(self.player1.cards) == 0:
                self.data["Winner"] = self.player2.name
                break
            if len(self.player2.cards) == 0:
                self.data["Winner"] = self.player1.name
                break
            if counter > 6000:
                print(self.data)
                break
# class Simulation

def create_cards():
    cards = []
    for x in range (4):
        for y in range(1,11):
            cards.append(y)
    random.shuffle(cards)
    return cards

def give_cards_to_player(p1, p2):
    cards = create_cards()
    p1.cards = cards[:20]
    p2.cards = cards[20:]

def get_data_time():
    now = datetime.now()
    now_str = now.strftime("%Y/%m/%d %H:%M:%S")
    return now_str
