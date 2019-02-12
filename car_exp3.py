from probability import distr, draw
import math
import random
import pdb

nPlayers = 20
nRounds = 3000000
nCars = 5

gamma = 0.07

# Print results every modPrint rounds.
modPrint = 1000

# Actions 0-60 are CAR.
nActions = 62
busActionIdx = nActions - 1

weights = [1.0] * nActions


# Rewards.
rewardMin = 0
rewardMax = 100
rewardBus = 50
rewardCar = 30;
slopeCar = (rewardMax - rewardCar) / 60;
slopeCarMiss = rewardCar / 60;

def distr(weights, gamma=0.0):
    theSum = float(sum(weights))
    return tuple((1.0 - gamma) * (w / theSum) + (gamma / len(weights)) for w in weights)

class Player:
   def __init__(self, name):
      self.name = name
      
      self.gamma = gamma
      self.weights = [1.0] * nActions
      self.probabilityDistribution = distr(self.weights, self.gamma)
      
      self.lastChoice = None
      self.cumulativeReward = 0
      self.bestActionCumulativeReward = 0
      self.weakRegret = 0
      
   def choose(self):
      self.probabilityDistribution = distr(self.weights, self.gamma)
      choice = draw(self.probabilityDistribution)
      self.lastChoice = choice
      return choice
    
   def exp3(self, reward):
      scaledReward = (1.0 * reward - rewardMin) / (rewardMax - rewardMin) # rewards scaled to 0,1
      estimatedReward = scaledReward / self.probabilityDistribution[self.lastChoice]
      self.weights[self.lastChoice] *= math.exp(estimatedReward * self.gamma / nActions) # important that we use estimated reward here!
      self.cumulativeReward += reward
      ## bestActionCumulativeReward += rewardVector[t][bestAction]
      ## weakRegret = (bestActionCumulativeReward - cumulativeReward)
      ## regretBound = (math.e - 1) * gamma * bestActionCumulativeReward + (nActions * math.log(nActions)) / gamma

 

# Test Exp3 using stochastic payoffs for 10 actions.
def simulation():
   
   players = list()

   for r in range(nRounds):
      for p in range(nPlayers):

         ## print('{0} {1}'.format(p, r))
         
         ## Create players for the first time.
         if (r == 0):
            players.append(Player(p))

         player = players[p]
         choice = player.choose()

      ## pdb.set_trace()
      players.sort(key=lambda x: x.lastChoice)

      ## Number of people who chose CAR.
      nCarers = 0
      totCarTime = 0
      for player in players:
         if player.lastChoice == busActionIdx:
            reward = rewardBus
         else:
            nCarers += 1
            time = player.lastChoice
            if time == None:
               pdb.set_trace()
               
            totCarTime += time
            if nCarers <= nCars:
                reward = rewardCar + (slopeCar * time);
            else:
                reward = rewardCar - (slopeCarMiss * time);

         ## pdb.set_trace()
         ## print(reward)
         player.exp3(reward)

      ## Print every X.
      if r % modPrint == 0:
         if nCarers > 0:
            print("round: %d\tnCars: %d\ttime: %.2f" % (r, nCarers, (totCarTime/nCarers)))
         else:
            print('round: %d\tnCars: 0')
      
         
      ## print("nCars: %d\tmaxRegret: %.2f\tweights: (%s)" % (nCarers, (totCarTime/nCarers), ', '.join(["%.3f" % weight for weight in distr(weights)])))
   ##pdb.set_trace()



if __name__ == "__main__":
   simulation()
