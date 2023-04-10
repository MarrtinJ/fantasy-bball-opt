import argparse
import requests
from datetime import date
from bs4 import BeautifulSoup
import pandas as pd

def main():
    # ideas:
    #   take in a player name or url, scrape the last 10 games
    #   given a date, look at all games played on that day

    parser = argparse.ArgumentParser()
    parser.add_argument("First", help="player first name", type=str)
    parser.add_argument("Last", help="player last name", type=str)
    args = parser.parse_args()
    print("Player Name: {} {}".format(args.First, args.Last))

    today = date.today()
    dateStr = today.strftime("%m_%d_%Y")
    # print(dateStr)

    # all the html content of the website
    url = 'https://www.basketball-reference.com/players/c/curryst01/gamelog/2022'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    # selecting the table itself
    content = soup.find('div', id = 'content')
    table_div = content.find('div', id = 'all_pgl_basic')
    table = content.find('div', id = 'div_pgl_basic')

    # need to decide which features to include
    stats = ['date_game', 'opp_id', 'pts', 'fg3', 'trb', 'ast', 'stl', 'blk', 'tov']
    order = ['Last', 'First', 'Date', 'Opp', '3PM', ' REB', 'AST', 'STL', 'BLK', 'TOV', 'PTS']
    data = []

    # selecting the bulk of the data
    t_body = table.find('tbody')
    t_rows = t_body.find_all('tr')

    # iterating through first 10 rows (the 10 most recent games)
    for row in t_rows:
        line = [args.Last, args.First]
        # line = []
        for cell in row.find_all('td'):
            if cell['data-stat'] in stats:
                # only scrape necessary cells
                line.append(cell.text)
                # print("{}: {}".format(cell['data-stat'], cell.text))
        if len(line) == len(stats) + 2:
            # if a player is inactive, the length of the row won't match what is desired
            data.append(line)

    data = sorted(data, reverse=True) # most recent games first
    # print(*data, sep='\n')

    df = pd.DataFrame(data, columns=order)
    print(df)

    filename = 'data/'+dateStr+'_'+args.First+args.Last
    print(filename)
    # df.to_csv(filename, index=False)
    
if __name__ == "__main__":
    main()