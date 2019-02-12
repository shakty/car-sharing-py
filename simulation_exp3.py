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
        self.probabilityDistribution = distr(self.weights, self.gamma)

        self.lastAction = None
        self.cumulativeReward = 0
        self.bestActionCumulativeReward = 0
        self.weakRegret = 0

    def choose(self):
        self.probabilityDistribution = distr(self.weights, self.gamma)
        action = draw(self.probabilityDistribution)
        self.lastAction = action
        return action

    def exp3(self, reward, action=None):
        if action == None:
            action = self.lastAction
        else:
            self.cumulativeReward += reward

        # Rewards scaled to 0,1.
        scaledReward = (1.0 * reward - rewardMin) / (rewardMax - rewardMin)
        estimatedReward = scaledReward / self.probabilityDistribution[action]
        # Important that we use estimated reward here!
        self.weights[action] *= math.exp(estimatedReward * self.gamma / self.nActions)


# Exp3 using stochastic payoffs.
def simulation(nPlayers=20, rewardBus=50, nCars=5, nRounds=30, gamma=0.07,
               nActions=62, updateKnown=True, modPrint=1):

    players = list()

    # Actions (last action is bus).
    busActionIdx = nActions - 1

    for r in range(nRounds):
        for p in range(nPlayers):

            ## print('{0} {1}'.format(p, r))

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
            for player in players:
                if player.lastAction == busActionIdx:
                    reward = rewardBus
                else:
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
                    else:
                        reward = rewardCar - (slopeCarMiss * time);

                    

            ## pdb.set_trace()
            ## print(reward)
            
            ## Update reward action taken.
            player.exp3(reward)

            ## Print every X.
    if modPrint and r % modPrint == 0:
        prefix = "bus: %d\tcars: %02d\tgamma: %.2f\tround: %d\t" % \
                 (rewardBus, nCars, gamma, (r+1))
        
        if nCarers > 0:
            print("%snCars: %d\ttime: %.2f" %
                  (prefix, nCarers, (totCarTime/nCarers)))
        else:
            print('round: %d\tnCars: 0')


      ## print("nCars: %d\tmaxRegret: %.2f\tweights: (%s)" % (nCarers, (totCarTime/nCarers), ', '.join(["%.3f" % weight for weight in distr(weights)])))
      ##pdb.set_trace()



if __name__ == "__main__":
    simulation()
