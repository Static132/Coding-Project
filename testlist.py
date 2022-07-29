def loadlevel(level_list):
    level = level_list
    spawnpoint = []
    for y_axis in range(50,200,50):
        for x_axis in range(50,1000,50):
            spawnpoint.append([x_axis,y_axis])

    for enemy in range(0,len(level)):
        spawnpoint[enemy] = [level[enemy],spawnpoint[enemy]]
    return spawnpoint

#example spawnpoint = [scout,1],[x,y]
scout = 7

level_1 = [
    [scout,1],[scout,1],[scout,1],[scout,1],[scout,1],[scout,1],[scout,1],[scout,1],
    [scout,1],[scout,1],[scout,1],[scout,1],[scout,1],[scout,1],[scout,1],[scout,1],
    [scout,1],[scout,1],[scout,1]
]

print(((loadlevel(level_1)[0])[0])[0])
