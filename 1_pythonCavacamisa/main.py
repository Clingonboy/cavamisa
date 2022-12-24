import player
import json
import sys

def print_data(data):
    print("Simulation data:")
    for item, amount in data.items():
        print(" {}: {}".format(item, amount))



# sim1 = player.Simulation()
# sim1.player1.cards = [1, 5, 8, 6, 2, 3, 3, 9, 6, 2, 4, 7, 8, 2, 10, 8, 10, 4, 6, 5]
# sim1.player2.cards = [7, 5, 2, 4, 10, 6, 9, 9, 1, 1, 7, 10, 1, 5, 3, 9, 3, 4, 7, 8]
# sim1.data["Start_card_G1"] = sim1.player1.cards.copy()
# sim1.data["Start_card_G2"] = sim1.player2.cards.copy()
# print_data(sim1.data)
# sim1.start_simulation()
# print_data(sim1.data)
#print(json.dumps(sim.data, indent=4, sort_keys=True))


numero_partite_da_simulare = 1000

score = 0
count = 0
best_sim = None
for x in range(numero_partite_da_simulare):
    test = player.Simulation()
    test.start_simulation()
    count +=1
    print(count)
    if test.data["Total_played_cards"] > score:
        score = test.data["Total_played_cards"]
        print_data(test.data)
        best_sim = test.data.copy()

print(count)
print_data(best_sim)
print("--")
print("--")
