# for dataframe
team_dictionary = {
    'Atlanta Hawks': 'Atl', 'Boston Celtics': 'Bos', 
    'Brooklyn Nets': 'Bkn', 'Charlotte Hornets': 'Cha', 
    'Chicago Bulls': 'Chi', 'Cleveland Cavaliers': 'Cle', 
    'Dallas Mavericks': 'Dal', 'Denver Nuggets': 'Den', 
    'Detroit Pistons': 'Det','Golden State Warriors': 'GSW', 
    'Houston Rockets': 'Hou', 'Indiana Pacers': 'Ind',
    'Los Angeles Lakers': 'LAL', 'Los Angeles Clippers': 'LAC', 
    'Memphis Grizzlies': 'Mem', 'Miami Heat': 'Mia', 
    'Milwaukee Bucks': 'Mil', 'Minnesota Timberwolves': 'Min', 
    'New Orleans Pelicans': 'Nor', 'New York Knicks': 'NYK', 
    'Oklahoma City Thunder': 'OKC', 'Orlando Magic': 'Orl', 
    'Philadelphia 76ers': 'Phi', 'Phoenix Suns': 'Pho', 
    'Portland Trail Blazers': 'Por', 'Sacramento Kings': 'Sac', 
    'San Antonio Spurs': 'SAS', 'Toronto Raptors': 'Tor', 
    'Utah Jazz': 'Uta', 'Washington Wizards': 'Was'
}

# for bbref box-score ids
team_dictionary3 = {
    'Atlanta Hawks': 'Atl', 'Boston Celtics': 'Bos', 
    'Brooklyn Nets': 'Brk', 'Charlotte Hornets': 'Cho', 
    'Chicago Bulls': 'Chi', 'Cleveland Cavaliers': 'Cle', 
    'Dallas Mavericks': 'Dal', 'Denver Nuggets': 'Den', 
    'Detroit Pistons': 'Det','Golden State Warriors': 'GSW', 
    'Houston Rockets': 'Hou', 'Indiana Pacers': 'Ind',
    'Los Angeles Lakers': 'LAL', 'Los Angeles Clippers': 'LAC', 
    'Memphis Grizzlies': 'Mem', 'Miami Heat': 'Mia', 
    'Milwaukee Bucks': 'Mil', 'Minnesota Timberwolves': 'Min', 
    'New Orleans Pelicans': 'Nop', 'New York Knicks': 'NYK', 
    'Oklahoma City Thunder': 'OKC', 'Orlando Magic': 'Orl', 
    'Philadelphia 76ers': 'Phi', 'Phoenix Suns': 'Pho', 
    'Portland Trail Blazers': 'Por', 'Sacramento Kings': 'Sac', 
    'San Antonio Spurs': 'SAS', 'Toronto Raptors': 'Tor', 
    'Utah Jazz': 'Uta', 'Washington Wizards': 'Was'
}

# for rotoguru
team_dictionary2 = {
    'atl': 'Atl', 'bos': 'Bos', 
    'bkn': 'Bkn', 'cha': 'Cha', 
    'chi': 'Chi', 'cle': 'Cle', 
    'dal': 'Dal', 'den': 'Den', 
    'det': 'Det','gsw': 'GSW', 
    'hou': 'Hou', 'ind': 'Ind',
    'lal': 'LAL', 'lac': 'LAC', 
    'mem': 'Mem', 'mia': 'Mia', 
    'mil': 'Mil', 'min': 'Min', 
    'nor': 'Nor', 'nyk': 'NYK', 
    'okc': 'OKC', 'orl': 'Orl', 
    'phi': 'Phi', 'pho': 'Pho', 
    'por': 'Por', 'sac': 'Sac', 
    'sas': 'SAS', 'tor': 'Tor', 
    'uta': 'Uta', 'was': 'Was'
}

month_dictionary = {'Jan': '01', 'Feb': '02',  'Mar': '03', 
'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

# alter the months in this list to match the season you want to scrape for
# have to alter for 2019-2020 season, October listed twice (October 2019 and October 2020)

# 2015-2016
month_list = ['october', 'november', 'december', 'january', 'february', 'march', 'april', 'may', 'june']

# 2019-2020
# month_list = ['october 2019', 'november', 'december', 'january', 'february', 'march', 'july', 'august','september', 'october 2020']

# 2020-2021
# month_list = ['december', 'january', 'february', 'march', 'april', 'may', 'june', 'july']

# 2021-2022
# month_list = ['october', 'november', 'december', 'january', 'february', 'march', 'april', 'may']
