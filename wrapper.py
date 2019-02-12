from simulation_exp3 import simulation as sim
import numpy as np
import pdb
import csv

# Update Known (if TRUE players will update BUS payoff
# even when do not take it, just because they know its value).
updateKnown = True

# Print results every modPrint rounds.
modPrint = 1

repetitions = 10

rounds = [30]
players = [20]
cars = [5, 10, 15]
busRewards = [50, 70]

## Includes BUS (last one).
actions = [11]

gammas = np.linspace(0.01, 0.3, 10)

outfile = "mean.csv"

dumpActions = True

def sweep():

    f = open(outfile, "w")
    writer = csv.writer(f, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['avg.cars', 'avg.time'])

    simIdx = 0
    for p in players:
        for c in cars:
            for b in busRewards:
                for r in rounds:
                    for g in gammas:
                        for a in actions:
                            for R in range(1, repetitions):
                                ## pdb.set_trace()
                                simIdx += 1
                                res = sim(simIdx, p, b, c, r, g, a,
                                          updateKnown, modPrint, dumpActions)
                                writer.writerow(res)
if __name__ == "__main__":
    sweep()
