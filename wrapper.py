from simulation_exp3 import simulation as sim
import numpy as np

# Update Known (if TRUE players will update BUS payoff
# even when do not take it, just because they know its value).
updateKnown = True

# Print results every modPrint rounds.
modPrint = 1

rounds = [30]
players = [20]
cars = [5, 10, 15]
busRewards = [50, 70]

## Includes BUS (last one).
actions = [11]

gammas = np.linspace(0.01, 0.3, 10)

def sweep():
    for p in players:
        for c in cars:
            for b in busRewards:
                for r in rounds:
                    for g in gammas:
                        for a in actions:
                            sim(p, b, c, r, g, a, updateKnown, modPrint)
              

if __name__ == "__main__":
    sweep()
