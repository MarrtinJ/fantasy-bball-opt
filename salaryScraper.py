import argparse
import requests
from datetime import date
from bs4 import BeautifulSoup
import pandas as pd

from variables import team_dictionary2

player_dict = {'Date': [], 'Name': [], 'Team': [], 'Starter': [], 'Position': [], 'Salary': [], 'FPTS': []}

# this script srapes player position, salary, and fantasy point info from rotoguru.com
# which hosts historical info for fantasy sports on various platforms up to 2021
def main():
    # iterates through the dates and times of nba season, scrapes the tables
    # creates a dataframe for a season and exports that dataframe to a csv

    # years and months of a season, alter these years and months to fit the season to scrape for
    cal = {"2019": ['10', '11', '12'], "2020": ['01', '02', '03', '07', '08', '09', '10']}

    for year, mons in cal.items(): 
        for mon in mons:
            for i in range(1, 32):
                # for each day in a month
                day_str = f'{i}'
                day_str = f'0{day_str}' if len(day_str) == 1 else day_str
                url = f'http://rotoguru1.com/cgi-bin/hyday.pl?mon={mon}&day={day_str}&year={year}&game=dk'

                date = f'{year}{mon}{day_str}'
                # print(date, url)
                scrape_page(url, date)

    player_df = pd.DataFrame.from_dict(player_dict)
    print(player_df)

    player_df.to_csv(f'{year}_PlayerPosSalaries.csv', line_terminator='\n', index=False)
    message = f'Saved player position/salary info for {year} to a csv'
    print(message)


def scrape_page(url, date):

    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    # print(soup.prettify())

    # all the information is stored on a single table
    table = soup.find('table', {'border': '0', 'cellspacing': '5'})
    table = table.find_all('tr')
    rows = []
    ignore = ['DNP', 'NA'] # ignore rows that don't include useful info
    for row in table:
        if len(row) == 9:
            cols = row.find_all('td')
            cols = [i.text.strip() for i in cols]
            
            if (cols[-2]) not in ignore:
                rows.append(cols)
    
    for player in rows:
        pos = player[0] 
        name = player[1]
        
        i = name.find('^') # ^ indicates a player started
        if i != -1:
            name = name[:i] + name[i+1:]
            starter = 1
        else:
            starter = 0

        comma = name.find(',')
        first = name[comma+2:]
        last = name[:comma]
        name = f'{first} {last}'
        fpts = player[2] # append to dict
        sal = player[3] # clean data, $ and ,
        comma = sal.find(',')
        if comma == -1:
            continue # player was unlisted, skip row
        sal = sal[1:comma]+sal[comma+1:]
        team = team_dictionary2[player[4]]
        # print(player)
        print(f'Date: {date}, Name: {name}, Team: {team}, Starter: {starter}, Position: {pos}, Salary: {sal}, FPTS: {fpts}')
        player_dict['Date'].append(date)
        player_dict['Name'].append(name)
        player_dict['Team'].append(team)
        player_dict['Starter'].append(starter)
        player_dict['Position'].append(pos)
        player_dict['Salary'].append(sal)
        player_dict['FPTS'].append(fpts)

    
if __name__ == "__main__":
    main()