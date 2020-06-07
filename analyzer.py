from experience_points import ExperienceTable
from experience_points import ExperienceTableRow
from experience_points import ExperiencePoints

import jsonpickle

def readData(fileName):
    file = open(fileName, "r")
    dataText = file.read()
    data = jsonpickle.decode(dataText)

    return data

def insertIntoRanking(ranking, monsterName, comparisonValue):
    for index, tup in enumerate(ranking):
        if tup[1] < comparisonValue:
            ranking.insert(index, (monsterName, comparisonValue))
            return
    ranking.append((monsterName, comparisonValue))

def rankMostStatsPerExp(ranking, data):
    expLimit = 50000
    for monster in data:
        currStats = 0
        for i in range(len(monster.table.speed)):
            attackRow = monster.table.attack[i]
            speedRow = monster.table.speed[i]
            hpRow = monster.table.hp[i]
            mpRow = monster.table.mp[i]
            defRow = monster.table.defense[i]
            intellRow = monster.table.intelligence[i]

            currExp = int(attackRow.experience_required)
            if currExp > expLimit:
                break
            currStats += int(attackRow.amount)
            currStats += int(speedRow.amount)
            currStats += int(hpRow.amount)
            currStats += int(mpRow.amount)
            currStats += int(defRow.amount)
            currStats += int(intellRow.amount)
        insertIntoRanking(ranking, monster.monster_name, currStats)

def addToQueue(queue, toAdd):
    for index, element in enumerate(queue):
        if toAdd[1] < element[1]:
            queue.insert(index, toAdd)
            return
    queue.append(toAdd)

# startingStats: [hp,mp,att,def,spd,int]
def findBestPath(monsterTable, startingLevel, startingStats, expLimit=0):
    # Thinking of leveling up/reincarnating as paths
    # Lv1 -> Lv2 -> ... -> Lv10 -> Lv11 -> Lv12
    # or Lv1 -> Lv2 -> ... -> Lv10 -> Lv1 -> Lv2
    # The cost is the amount of exp required,
    # the value is the amount of stats acquired.
    # If ]cost(B) is lower than cost(A) while value(B) is higher than value(A),
    # we can safely assume that path B is better than path A
    queue = []
    maxValue = -1
    maxCost = 0
    bestPath = [-1] 
    bestStats = [-1,-1,-1,-1,-1,-1]
    #path(levels/reincarnations), cost(exp required), value([hp,mp,att,def,spd,int])
    addToQueue(queue,([startingLevel], 0, startingStats))
    while len(queue) > 0:
        next = queue.pop(0)
        currPath = next[0]
        currCost = next[1]
        currStats = next[2]
        lastPath = currPath[-1]
        # reincarnate if we can and should
        # should: if we are in the midst of testing a reincarnation (len(queue) == 1),
        #         we should not have to reincarnate during the testing phase
        #         because we have already validated beforehand that any level under the current level
        #         should be leveled up for max stats
        if lastPath >= 10 and len(queue) == 0:
            reincarnatedStats = []
            for stat in currStats:
                newStat = round(0.8 * stat)
                if newStat > 500:
                    newStat = 500
                reincarnatedStats.append(newStat)
            newCost = currCost
            newPath = currPath.copy()
            newPath.append(1)
            addToQueue(queue, (newPath, newCost, reincarnatedStats))
        # normal leveling
        if lastPath == 99:
            continue
        nextStats = currStats.copy()
        nextPathIndex = lastPath - 1
        nextCost = int(monsterTable.hp[nextPathIndex].experience_required)
        if nextPathIndex > 0:
            nextCost -= int(monsterTable.hp[nextPathIndex-1].experience_required)
        nextCost += currCost
        if expLimit == 0:
            shouldStop = False
            # stop when we know when to reincarnate
            if len(queue) == 0:
                for index, path in enumerate(reversed(currPath)):
                    if path == 1 and index != len(currPath)-1:
                        shouldStop = True
                        break
            if shouldStop:
                continue
        elif nextCost > expLimit:
            continue

        nextStats[0] = min(999, nextStats[0] + int(monsterTable.hp[nextPathIndex].amount))
        nextStats[1] = min(999, nextStats[1] + int(monsterTable.mp[nextPathIndex].amount))
        nextStats[2] = min(999, nextStats[2] + int(monsterTable.attack[nextPathIndex].amount))
        nextStats[3] = min(999, nextStats[3] + int(monsterTable.defense[nextPathIndex].amount))
        nextStats[4] = min(999, nextStats[4] + int(monsterTable.speed[nextPathIndex].amount))
        nextStats[5] = min(999, nextStats[5] + int(monsterTable.intelligence[nextPathIndex].amount))
        nextValue = sum(nextStats)

        # we know this cannot be the best path
        if nextCost > maxCost and nextValue < maxValue:
            continue

        nextPath = currPath.copy()
        nextPath.append(lastPath+1)
        # since we order the queue by least cost,
        # it should be fine to assume
        # that this is the best so far
        if nextValue > maxValue:
            maxValue = nextValue
            maxCost = nextCost
            bestPath = nextPath
            bestStats = nextStats

            if maxValue == 999*6:
                continue

        addToQueue(queue, (nextPath, nextCost, nextStats))
    return bestPath, bestStats

def rankMostStatsPerExpWithReincarnation(ranking, data):
    for monster in data:
        path, stats = findBestPath(monster.table, 1, [500,500,500,500,500,500])
        print(monster.monster_name)
        print(*path)
        print(*stats)
        print()
            



        

#data = readData("monsters.txt")
#ranking = []
#subdata = data[-2:-1]
#rankMostStatsPerExpWithReincarnation(ranking, data)