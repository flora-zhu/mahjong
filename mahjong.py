import pandas as pd
import numpy as np
import random
from pathlib import Path

# building the deck
type = []
number = []
tiles = []
honor = []
suites = ['tong', 'tiao', 'wan']
winds = ['dong', 'nan', 'xi', 'bei']
dragons = ['hz', 'bb', 'fc']
flowers = ['1', '2', '3', '4']

for suite in suites:
    for i in range(1, 10):
        for j in range(4):
            tiles.append(suite + str(i))
            type.append(suite)
            number.append(i)
            honor.append(False)
for wind in winds:
    for j in range(4):
        tiles.append(wind)
        type.append(wind)
        number.append(0)
        honor.append(True)
for dragon in dragons:
    for j in range(4):
        tiles.append(dragon)
        type.append(dragon)
        number.append(0)
        honor.append(True)
for flower in flowers:
    for j in range(2):
        tiles.append('flower' + flower)
        type.append('flower')
        number.append(flower)
        honor.append(False)

df_tiles = pd.DataFrame(tiles)
df_tiles['type'] = type
df_tiles['number'] = number
df_tiles['honor'] = honor
indexes = list(range(144))
df_tiles['index'] = indexes

winds = {1: 'dong', 2: 'nan', 3: 'xi', 4: 'bei'} # numbers corresponding to winds
winddirs = []
dirs = []
flowerdfs = []
hands = []
scores = []
flowernums = []
pairnums = []
pongnums = []
kongnums = []
halfchinums = []
chinums = []
misssuitenums = []
tilelist = []
fullhands = pd.DataFrame()

# simulate drawing n=100000 hands
for j in range(100000):
    score = 0
    redraw = 0
    winddir = random.randint(1, 4)
    dir = random.randint(1, 4)
    pairnum = 0
    pongnum = 0
    halfchinum = 0
    nokongs = 0

    # draw hand
    hand = df_tiles.sample(13).sort_index()
    remaining = df_tiles.drop(list(hand.index))
    flower_df = hand[hand['type'] == 'flower']
    hand = hand[hand['type'] != 'flower']

    # redraw for flowers
    while redraw < len(flower_df):
        for i in range(len(flower_df) - redraw):
            redraw_df = remaining.sample(len(flower_df) - redraw).sort_index()
            remaining = remaining.drop(list(redraw_df.index))
            flower_df = pd.concat([flower_df, redraw_df[redraw_df['type'] == 'flower']])
            hand = pd.concat([hand, redraw_df[redraw_df['type'] != 'flower']])
            redraw += len(flower_df) - redraw
    hand = hand.sort_index()
    flower_df = flower_df.sort_index()

    # kongs
    pairs = hand[hand[0].duplicated()]
    pongs = pairs[pairs[0].duplicated()]
    pairs = pairs.drop(list(pongs.index))
    kongs = pongs[pongs[0].duplicated()]
    pongs = pongs.drop(list(kongs.index))
    if len(kongs) != 0:
        nokongs = len(kongs)
        for i in range(nokongs):
            draw = remaining.sample(1)
            if draw.iloc[i]['type'] == 'flower':
                flower_df = pd.concat([flower_df, draw])
                while redraw < len(flower_df):
                    for i in range(len(flower_df) - redraw):
                        redraw_df = remaining.sample(len(flower_df) - redraw).sort_index()
                        remaining = remaining.drop(list(redraw_df.index))
                        flower_df = pd.concat([flower_df, redraw_df[redraw_df['type'] == 'flower']])
                        hand = pd.concat([hand, redraw_df[redraw_df['type'] != 'flower']])
                        redraw += len(flower_df) - redraw
            else:
                hand = pd.concat([hand, draw])
            score += 4
            if kongs.iloc[i]['honor']:
                score += 1
                if kongs.iloc[i]['type'] == winds[dir]:
                    score += 1
                if kongs.iloc[i]['type'] == winds[winddir]:
                    score += 1
            
    honor_pairs = pairs[pairs['honor']]
    honor_pongs = pongs[pongs['honor']]

    #pongs
    for i in range(len(honor_pongs)):
        score += 4
        pongnum += 1
        if len(honor_pongs[honor_pongs['type'] == winds[dir]]) > 0:
            score += 1
        if len(honor_pongs[honor_pongs['type'] == winds[winddir]]) > 0:
            score += 1
    for i in range(len(pongs) - len(honor_pongs)):
        pongnum += 1
        score += 3

    #pairs
    for i in range(len(honor_pairs)):
        pairnum += 1
        score += 3
        if len(honor_pongs[honor_pongs['type'] == winds[dir]]) > 0:
            score += 1
        if len(honor_pongs[honor_pongs['type'] == winds[winddir]]) > 0:
            score += 1
    for i in range(len(pairs) - len(honor_pairs)):
        pairnum += 1
        score += 2

    # flower scoring
    if redraw == 0:
        score += 1
    if len(flower_df[flower_df['number'] == str(dir)]) != 0:
        score += 1
    if len(flower_df[flower_df['number'] == str(winddir)]) != 0:
        score += 1

    # suites
    missingsuites = 0
    for suite in suites:
        if len(hand[hand['type'] == suite]) == 0:
            missingsuites += 1
    score += missingsuites * 4

    # chi
    for suite in suites:
        cursuite = hand[hand['type'] == suite]
        for index in list(cursuite.index):
            row = cursuite.loc[index]
            if len(cursuite[cursuite['number'] == (row['number'] + 1)]) > 0: # full chi is handled by this 
                score += 1
                halfchinum += 1
            elif len(cursuite[cursuite['number'] == (row['number'] + 2)]) > 0:
                score += 1
                halfchinum += 1

    winddirs.append(winddir)
    dirs.append(dir)
    flowerdfs.append(list(flower_df[0]))
    hands.append(list(hand[0]))
    scores.append(score)
    flowernums.append(redraw)
    pairnums.append(pairnum)
    pongnums.append(pongnum)
    kongnums.append(nokongs)
    halfchinums.append(halfchinum)
    misssuitenums.append(missingsuites)

    # create bool row of which tiles are in the hand
    merged = pd.merge(df_tiles, hand, how='left', indicator=True)

    print(j)
    params = pd.DataFrame(merged['_merge'] == 'both').T
    fullhands = pd.concat([fullhands, params])
    if j == 9: # for demonstration purposes
        break

data = pd.DataFrame()
data['hand'] = hands
data['flowers'] = flowerdfs
data['score'] = scores
data['wind'] = winddirs
data['dir'] = dirs
data['flowernum'] = flowernums
data['pairs'] = pairnums
data['pongs'] = pongnums
data['kongs'] = kongnums
data['halfchi'] = halfchinums
data['suites missing'] = misssuitenums
fullhands['score'] = scores

print(data)
print(fullhands)
directory = Path(r'C:\Users\Flora Zhu\Downloads\cs109proj')
directory.mkdir(parents=True, exist_ok=True)
#data.to_csv(directory / 'mahjong_hands_train.csv')
#fullhands.to_csv(directory / 'fullhands_train.csv')
df_tiles.to_csv(directory / 'mahjong_deck.csv')