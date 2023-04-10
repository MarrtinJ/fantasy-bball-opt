# brute forces best fantasy lineup on any given day using an inverted DFS

import numpy as np
import pandas as pd

df = pd.read_csv('dataset2.csv')
df = df[['Date', 'Name', 'Team', 'Position', 'Salary', 'FPTS']]

# all the unique dates in the dataset
dates = df['Date'].unique()

for x in range(0,2):
  date = dates[x]

  df = df[df['Date']==date]

  Utils = df.copy()
  Utils['Position'] = 'UTIL'
  Utils

  multPositions = df[df['Position'].str.contains("/")]
  multPositions.reset_index(inplace=True, drop=True)

  pos1 = []
  pos2 = []
  for index, row in multPositions.iterrows():
    playerPos1, playerPos2 = row['Position'].split('/')
    copy1 = row.copy()
    copy1['Position'] = playerPos1
    copy2 = row.copy()
    copy2['Position'] = playerPos2
    # print(copy)
    pos1.append(copy1)
    pos2.append(copy2)
    # print(playerPos1, playerPos2)

  pos1 = pd.DataFrame(pos1)
  pos2 = pd.DataFrame(pos2)


  onePosition = df[ df['Position'].str.contains('/')==False ]

  currentPlayers = pd.concat([onePosition, pos1, pos2], ignore_index=True)
  currentPlayers.sort_values(['Name', 'Team', 'Position'], na_position='first', inplace=True, ignore_index=True)

  Gs = currentPlayers[currentPlayers['Position'].isin(['PG', 'SG'])]
  Gs.drop_duplicates(subset='Name', inplace=True)
  Gs.reset_index(inplace=True, drop=True)
  Gs['Position'] = 'G'

  Fs = currentPlayers[currentPlayers['Position'].isin(['SF', 'PF'])]
  Fs.drop_duplicates(subset='Name', inplace=True)
  Fs.reset_index(inplace=True, drop=True)
  Fs['Position'] = 'F'

  currentPlayers = pd.concat([currentPlayers, Gs, Fs, Utils], ignore_index=True)
  currentPlayers.sort_values(['Name', 'Team', 'Position'], na_position='first', inplace=True, ignore_index=True)

  # incr determines if the players are each position are sorted by increasing salary
  incr = True

  PGs = currentPlayers[currentPlayers['Position'] == 'PG']
  PGs.sort_values(by=['Salary'], ascending=incr, inplace=True)

  SGs = currentPlayers[currentPlayers['Position'] == 'SG']
  SGs.sort_values(by=['Salary'], ascending=incr, inplace=True)

  SFs = currentPlayers[currentPlayers['Position'] == 'SF']
  SFs.sort_values(by=['Salary'], ascending=incr, inplace=True)

  PFs = currentPlayers[currentPlayers['Position'] == 'PF']
  PFs.sort_values(by=['Salary'], ascending=incr, inplace=True)

  Cs = currentPlayers[currentPlayers['Position'] == 'C']
  Cs.sort_values(by=['Salary'], ascending=incr, inplace=True)

  Gs = currentPlayers[currentPlayers['Position'] == 'G']
  Gs.sort_values(by=['Salary'], ascending=incr, inplace=True)

  Fs = currentPlayers[currentPlayers['Position'] == 'F']
  Fs.sort_values(by=['Salary'], ascending=incr, inplace=True)

  Utils = currentPlayers[currentPlayers['Position'] == 'UTIL']
  Utils.sort_values(by=['Salary'], ascending=incr, inplace=True)

  # minPrices holds the minimum budget required to keep searching at each position
  #   where the number at index i represents the sum of the least expensive players at position index >= i

  # maxPrices holds the minimum budget required to afford the highest scoring players in the remaining positions
  #   where the number at index i represents the sum of the most expensive players at position index >= i

  l1 = [PGs, SGs, SFs, PFs, Cs, Gs, Fs, Utils]

  minSalaries = []
  maxSalaries = []
  l2 = []
  position_order = []

  l3 = []

  for i in range(8):
    # could also consider sorting by the mean salary of each position
    pos_max = l1[i].Salary.max()
    l2.append((pos_max, l1[i]))

  # sort the positions in descending order by max salary
  l2 = sorted(l2, key=lambda x: x[0], reverse=True)

  cheapest_sum = 0
  expensive_sum = 0
  for i in range(len(l2)):
    # keeping track of the sum of salaries for the most expensive players in each position
    pos_max = l2[i][0]
    expensive_sum += pos_max
    maxSalaries.insert(0, expensive_sum)

    # removing the max sal info, retaining just the dataframe
    l2[i] = l2[i][1]

    l3.append(l2[i].sort_values(by=['FPTS'], ascending=False))

    # keeping track of the sum of salaries for the least expensive players in each position
    pos_min = l2[i].Salary.min()
    cheapest_sum += pos_min
    minSalaries.insert(0, cheapest_sum)

    # keeping track of the sorted order of the positions
    pos = l2[i]['Position'].iloc[0]
    position_order.append(pos)

    print(pos, pos_min, pos_max)

# players[i][j] represents the ith player in the jth position
# players[i] sorted in ascending order by salary

players = []

for i in range(len(l2)):
  players_list = l2[i]['Name'].to_list()
  # print(position_order[i], players_list)
  players.append(players_list)

# players

def getSingleScore(player):
  return currentPlayers[currentPlayers['Name'] == player].iloc[0].FPTS

def getSingleSalary(player):
  return currentPlayers[currentPlayers['Name'] == player].iloc[0].Salary

# getScore takes in a dict of players, returns the fantasy points scored by players
def getScore(players):
  total_score = 0
  for player in players.values():
    player_score = getSingleScore(player)
    # print(player, player_score)
    total_score += player_score
  return total_score

"""# Inverted DFS"""

MAX_POSITION_INDEX = 7

# invertedDFS(players, 0, 0, 50000)
def invertedDFS(players, pos_index, player_index, budget):
  player = players[pos_index][player_index]

  salary = getSingleSalary(player)
  newBudget = budget - salary

  # optimization 1: instead of comparing with 0, compare with sum(min_budget of each remaining position)
  #   can be computed ahead of time for each level
  # if newBudget < 0:
  if pos_index < MAX_POSITION_INDEX and newBudget < minSalaries[pos_index+1]:
    print('out of budget at position {}'.format(pos_index))
    return dict(), np.NINF

  # optimization 3: two separate cases: if I have enough budget to pick the max salary from every remaining level, no need for recursion, just pick best score from every lower level
  # otherwise, do the recursive search in the next block
  if pos_index < MAX_POSITION_INDEX and newBudget > maxSalaries[pos_index+1]:
    print('can afford best players at position {}'.format(pos_index))

    assignment = dict()
    assignment[pos_index] = player
    for i in range(pos_index+1, 8):
      for index, row in l3[i].iterrows():
        if row['Name'] not in assignment.values():
          assignment[i] = row['Name']
          break
    # print(assignment, getScore(assignment))
    return assignment, getScore(assignment)

  if pos_index == MAX_POSITION_INDEX:
    assignment = {pos_index: player}
    # print(pos_index, player_index, player)
    return assignment, getScore(assignment)
  else:
    max_score = 0
    best_lineup = dict()
    for j in range(len(players[pos_index + 1])):
      a, s = invertedDFS(players, pos_index+1, j, newBudget) 
      # optimization 2: if a returns None (a is empty), break out of the current loop
      if not a:
        print('next level returned none')
        break
      if s > max_score and a and player not in a.values(): #duplicate check
        max_score = s
        best_lineup = a
        # print(max_score, best_lineup)
    if best_lineup:
      best_lineup[pos_index]=player
      return best_lineup, max_score + getSingleScore(player)
    else:
      return dict(), np.NINF

invertedDFS(players, 0, 0, 50000)

"""# Test"""

res = ({0: 'Nicolo Melli',
  1: 'Anthony Davis',
  2: 'Josh Hart',
  3: 'Maurice Harkless',
  4: 'Nickeil Alexander-Walker',
  5: 'Kawhi Leonard',
  6: 'LeBron James',
  7: 'Danny Green'}, 289.75)
res

soln = res[0]
soln['Date'] = date
soln['FPTS'] = res[1]

soln_df = pd.DataFrame(soln, index=[0])
soln_df