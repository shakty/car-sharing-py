from probability import distr, draw
import math
import random
import pdb

# Rewards.
rewardMin = 0
rewardMax = 100
rewardCar = 30;

slopeCar = (rewardMax - rewardCar) / 60;
slopeCarMiss = rewardCar / 60;

def distr(weights, gamma=0.0):
    theSum = float(sum(weights))
    return tuple((1.0 - gamma) * (w / theSum) + (gamma / len(weights)) for w in weights)

class Player:
    def __init__(self, name, gamma, nActions):
        self.name = name

        self.nActions = nActions
        self.gamma = gamma
        self.weights = [1.0] * self.nActions
        ## Will be init with the first choice.
        self.probabilityDistribution = [None] * self.nActions

        self.lastAction = None
        self.cumulativeReward = 0
        self.bestActionCumulativeReward = 0
        self.weakRegret = 0

    def choose(self):
        pdb.set_trace()
        self.probabilityDistribution = distr(self.weights, self.gamma)
        action = draw(self.probabilityDistribution)
        self.lastAction = action
        return action

    def exp3(self, reward, action=None):
        if action == None:
            action = self.lastAction
        else:
            self.cumulativeReward += reward

        ## Rewards scaled to 0,1. (if not scaled it gets Inf very quickly).
        scaledReward = (1.0 * reward - rewardMin) / (rewardMax - rewardMin)
        estimatedReward = scaledReward / self.probabilityDistribution[action]
        # Important that we use estimated reward here!
        self.weights[action] *= math.exp(estimatedReward * self.gamma / self.nActions)


# Exp3 using stochastic payoffs.
def simulation(simIdx = 0, nPlayers=20, rewardBus=50, nCars=5, nRounds=30,
               gamma=0.07, nActions=62, updateKnown=True, modPrint=1,
               dump=False):

    ## pdb.set_trace()
    carLevel = 1.0 * nCars/nPlayers * 100

    if dump:
        f = open("results.csv", "a")
        ## Matches names in behavioral dataset.
        condition = "noinfo_car%d_p%d30" % (carLevel, rewardBus)
        prefixDump = '"%d","%s",%d,%d,%d,%.2f' % (simIdx, condition, carLevel,
                                                rewardBus, rewardCar, gamma)

    if modPrint:
        prefix = "%03d - bus: %d\tcars: %02d\tgamma: %.2f\t" % \
                 (simIdx, rewardBus, nCars, gamma)

    players = list()

    # Actions (last action is bus).
    busActionIdx = nActions - 1

    for r in range(nRounds):
        ## 1-based round.
        r1 = r + 1
        for p in range(nPlayers):

            ## Create players for the first time.
            if (r == 0):
                players.append(Player(p, gamma, nActions))

            player = players[p]
            action = player.choose()

            ## pdb.set_trace()
            players.sort(key=lambda x: x.lastAction)

            ## Number of people who chose CAR.
            nCarers = 0
            totCarTime = 0

        ## After all decisions have been made.    
        for player in players:
            if player.lastAction == busActionIdx:
                reward = rewardBus
                gotBus = 1
            else:
                gotBus = 0
                if updateKnown:
                    ## Update BUS anyway because
                    ## player knows its value.
                    player.exp3(rewardBus, busActionIdx)

                nCarers += 1
                time = player.lastAction

                if time == None:
                    pdb.set_trace()

                totCarTime += time
                if nCarers <= nCars:
                    reward = rewardCar + (slopeCar * time);
                    gotCar = 1
                else:
                    reward = rewardCar - (slopeCarMiss * time);
                    gotCar = 0

            if dump:
                if gotBus == 1:
                    decision = "bus"
                    time = 0
                    gotCar = 0
                else:
                    decision = "car"

                row = '%s,"%d_%d",%d,"%s",%d,%d,%d\n' \
                      % (prefixDump, simIdx, player.name, r1,
                         decision, player.lastAction, gotCar, reward)
                ## pdb.set_trace()
                f.write(row)

            ## Update reward action taken.
            player.exp3(reward)

    avgTime = (totCarTime / nCarers) if nCarers > 0 else -1

    ## Print every X.
    if modPrint and r % modPrint == 0:
        print("%sround: %d\tnCars: %d\ttime: %.2f" %
              (prefix, r1, nCarers, avgTime))


    return (nCarers, avgTime)


if __name__ == "__main__":
    simulation()
