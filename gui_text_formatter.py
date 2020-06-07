def formatReincarnateTimingMessage(levelList, expLimit=0):
    currLvl = 0
    allTimings = ""
    maxLvl = levelList[-1]
    print(*levelList)
    for level in levelList:
        if level < currLvl:
            allTimings += str(currLvl) + " "
        currLvl = level
    if allTimings == 0:
        return '転生せずレベル{}まで育てるのがベストです！！'.format(maxLvl)
    if expLimit == 0:
        return '次はレベル{}で転生するのが良さそうです'.format(allTimings)
    return '以下のタイミングで転生すると効率が良いです\n{}\n最終的にはレベル{}になります'.format(allTimings, maxLvl)
