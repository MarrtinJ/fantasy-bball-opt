import argparse
import requests
import re
from datetime import date
from bs4 import BeautifulSoup
import pandas as pd

from variables import team_dictionary, month_dictionary, month_list

def main():
    # getSeasonStats('https://www.basketball-reference.com/leagues/NBA_2019_games.html')
    getSeasonStats('https://www.basketball-reference.com/leagues/NBA_2020_games.html')
    # getSeasonStats('https://www.basketball-reference.com/leagues/NBA_2021_games.html')


def getSeasonStats(season_url):
    # general  idea:
    #   create a list that stores links to the games held during each month of a given season
    #   iterate through the list of months, visit each page
    #       create a list of links to the box scores of all games played during that month
    #   iterate through the box scores, gather information

    base_url = 'https://www.basketball-reference.com'

    html_text = requests.get(season_url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    # scrape the season
    season = soup.find('h1').text
    season = season.strip().split(' ')
    season = season[0]

    print(f'Scraping {season} Season')

    # scrape the links to the games played during each month of that season
    month_links = []

    body = soup.find('body')
    links = body.find_all('a', href = True)
    for link in links:
        if link.text.lower() in month_list:
            # store month and respective url as a tuple
            month_link = (link.text, f"{base_url}{link['href']}")
            # print(month_link)
            month_links.append(month_link)
    
    # dictionary of lists holding the months, urls, indexes
    pages_dict = {'Month': [], 'Url': [], 'Index': []}
    box_score_links = []
    all_dates = []

    # iterate through all the month links, scrape the urls to each games box-score
    for month, link in month_links:
        # visit each months link, get data        
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find_all('tbody')

        page_box_score_links = []
        page_dates = []
        # find all box score links, date of game played
        box_scores = table[0].find_all('a', href=True)
        for i in box_scores:
            if i.text.strip() == 'Box Score':
                page_box_score_links.append(f"{base_url}{i['href']}")
            if ',' in i.text.strip(): # contains date
                date = i.text.strip()
                date = date.split(', ')
                year = date[2]
                date = date[1].split(' ')
                # for formatting purposes
                day = f'0{date[1]}' if len(date[1]) ==1 else date[1]

                mon = month_dictionary[date[0]]
                date = f'{year}{mon}{day}'
                page_dates.append(date)
        
        if len(page_box_score_links) == 0 or len(box_scores)/len(page_box_score_links) != 4:
            # error checking just in case
            print('case 1')
            pages_dict['Url'].append(link)
            pages_dict['Month'].append(month)
            # keep track of the index to be able to pause/continue scraping at any given point
            pages_dict['Index'].append(len(page_box_score_links))
        else: # if len(page_box_score_links) != 0
            # print('Case 2')
            # print(f'Month: {month}\tNumGames: {len(page_box_score_links)}')
            pages_dict['Url'].append(link)
            pages_dict['Month'].append(month)
            pages_dict['Index'].append(None)
        box_score_links.append(page_box_score_links)
        all_dates.append(page_dates)


    df_columns = ['Date', 'Name', 'Team', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA',
               '3P%','FT', 'FTA', 'FT%', 'ORB', 
               'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', '+-' ]
    stat_df = pd.DataFrame(columns = df_columns)
    
    count = 0
    for l, d in zip(box_score_links, all_dates):
        for link, date in zip(l, d):
            # if count == 30:
            #     break

            print(f'\nScraping {link}\tDate: {date}')

            # scrape first table (away team)
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            table1 = soup.find('table', {'class': "sortable stats_table"})
            # filtering out just the team name
            team1 = table1.text.split('\n')[1]
            parenthesis = team1.find('(') 
            team1 = team1[:parenthesis - 1]

            # scrape second table (home team)
            table2 = soup.find_all('table', {'class': 'sortable stats_table'})
            team2 = table2[8].text.split('\n')[1]
            parenthesis = team2.find('(')
            team2 = team2[:parenthesis - 1]

            print(f'{team1} vs {team2}')

            # a dictionary to form a dataframe from
            player_dict = {'Date': [], 'Name': [], 'Team': [], 'MP': [],
                'FG': [], 'FGA': [], 'FG%': [],
                '3P': [], '3PA': [], '3P%': [],
                'FT': [], 'FTA': [], 'FT%': [],
                'ORB': [], 'DRB': [], 'TRB': [],
                'AST': [], 'STL': [], 'BLK': [],
                'TOV': [], 'PF': [], 'PTS': [], '+-': []}

            # # filtering out players
            table1 = table1.find('tbody')
            table1 = table1.find_all('tr')
            rows = []
            for row in table1:
                # scraping individual player statline
                name = row.find('th').text.strip("'.")
                # name = re.sub("'.", '', name)
                cols = row.find_all('td')
                cols = [i.text.strip() for i in cols]
                cols.append(name)
                rows.append(cols)

            # cleaning the data
            for player in rows:
                if len(player) < 21:
                    # filter out rows in the table that don't include player info
                    if player[0] != 'Reserves':
                        print(f'Missing info? {player}')
                    continue
                else:
                    player = [0 if i == '' else i for i in player]
                    colon = player[0].find(':')
                    time = f'{player[0][:colon]}.{player[0][colon + 1:]}'
                    print(player)

                    # adding a new row to the dataframe to be created
                    player_dict['Date'].append(date)
                    player_dict['Name'].append(player[-1])
                    player_dict['Team'].append(team_dictionary[team1])
                    player_dict['MP'].append(time)
                    player_dict['FG'].append(player[1])
                    player_dict['FGA'].append(player[2])
                    player_dict['FG%'].append(player[3])
                    player_dict['3P'].append(player[4])
                    player_dict['3PA'].append(player[5])
                    player_dict['3P%'].append(player[6])
                    player_dict['FT'].append(player[7])
                    player_dict['FTA'].append(player[8])
                    player_dict['FT%'].append(player[9])
                    player_dict['ORB'].append(player[10])
                    player_dict['DRB'].append(player[11])
                    player_dict['TRB'].append(player[12])
                    player_dict['AST'].append(player[13])
                    player_dict['STL'].append(player[14])
                    player_dict['BLK'].append(player[15])
                    player_dict['TOV'].append(player[16])
                    player_dict['PF'].append(player[17])
                    player_dict['PTS'].append(player[18])
                    player_dict['+-'].append(player[19])
            
            # scraping second table
            table2 = table2[8].find('tbody')
            table2 = table2.find_all('tr')
            
            # get all info from the tables
            rows = []
            for row in table2:
                # name = row.find_all('th')[0]
                name = row.find('th').text.strip("'.")
                # name = re.sub("'.", '', name)
                cols = row.find_all('td')
                cols = [i.text.strip() for i in cols]
                cols.append(name)
                rows.append(cols)

            for player in rows:
                if len(player) < 21:
                    # filter out rows in the table that don't include player info
                    # or are missing information / formatted incorrectly
                    if player[0] != 'Reserves':
                        print(f'missing info? {player}')                 
                    continue
                else:
                    player = [0 if i == '' else i for i in player] # fill in empty cells
                    colon = player[0].find(':')
                    time = f'{player[0][:colon]}.{player[0][colon + 1:]}'
                    print(player)

                    # adding a new row to the dataframe to be created
                    player_dict['Date'].append(date)
                    player_dict['Name'].append(player[-1])
                    player_dict['Team'].append(team_dictionary[team2])
                    player_dict['MP'].append(time)
                    player_dict['FG'].append(player[1])
                    player_dict['FGA'].append(player[2])
                    player_dict['FG%'].append(player[3])
                    player_dict['3P'].append(player[4])
                    player_dict['3PA'].append(player[5])
                    player_dict['3P%'].append(player[6])
                    player_dict['FT'].append(player[7])
                    player_dict['FTA'].append(player[8])
                    player_dict['FT%'].append(player[9])
                    player_dict['ORB'].append(player[10])
                    player_dict['DRB'].append(player[11])
                    player_dict['TRB'].append(player[12])
                    player_dict['AST'].append(player[13])
                    player_dict['STL'].append(player[14])
                    player_dict['BLK'].append(player[15])
                    player_dict['TOV'].append(player[16])
                    player_dict['PF'].append(player[17])
                    player_dict['PTS'].append(player[18])
                    player_dict['+-'].append(player[19])

            # create the player dataframe
            player_df = pd.DataFrame.from_dict(player_dict)
            # print(player_df)

            # concatenate overall dataframe with player dataframe
            stat_df = pd.concat((stat_df, player_df), axis=0, ignore_index=True)
            count += 1
    print(stat_df)

    stat_df.to_csv(f'{season}BoxScores.csv', line_terminator='\n', index=False)
    message = f'Saved game stats for the {season} season to a csv'
    print(message)

if __name__ == "__main__":
    main()