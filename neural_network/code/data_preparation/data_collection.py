import requests
from bs4 import BeautifulSoup
import json
import os

base_url = "https://www.vlr.gg"




def get_dates_page(page_number):
    soup = BeautifulSoup(requests.get(f'{base_url}/matches/results?page={page_number}').text, 'html.parser')
    return parse_dates(soup)

def parse_dates(soup):
    history = {}
    dates = soup.find_all('div', class_='wf-label mod-large')

    for date in dates:
        date_text = date.text.strip()
        matches = [{'link': base_url + match.get('href', ''),
                    'teams': [team.find('div', class_='text-of').text.strip() for team in match.find_all('div', class_='match-item-vs-team-name') if team.find('div', class_='text-of')]}
                   for match in date.find_next_sibling('div').find_all('a', class_='match-item')]

        if matches:
            history[date_text] = matches

    return history





def get_match_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    player_elements = soup.find_all('div', class_='player-name')
    players = [player.text.strip() for player in player_elements]

    print(f"Players from {url}: {players}")  # Debugging

    return players

def parse_matches(soup):
    matches = []
    match_list = soup.find_all('a', class_='match-item')
    for match in match_list:
        teams = [team.find('div', class_='text-of').text.strip() for team in match.find_all('div', class_='match-item-vs-team-name') if team.find('div', class_='text-of')]
        matches.append({'link': base_url + match.get('href', ''), 'teams': teams, 'text': ' vs '.join(teams)})

    return matches




def save_json(data, filename):
    with open(os.path.join('/Users/soren/Projects/Valorant/neural_network/data/raw', filename), 'w') as file:
        json.dump(data, file)

def save_csv(data, filename):
    with open(os.path.join('/Users/soren/Projects/Valorant/neural_network/data/raw', filename), 'w') as file:
        file.write('Date,Team1,Team2,Link\n')
        for date, matches in data.items():
            for match in matches:
                file.write(f"{date},{match['teams'][0]},{match['teams'][1]},{match['link']}\n")

def save_players_csv(players, filename):
    with open(os.path.join('/Users/soren/Projects/Valorant/neural_network/data/raw', filename), 'w') as file:
        file.write('Player\n')
        for player in players:
            file.write(f"{player}\n")







dates = get_dates_page(1)

save_json(dates, 'data.json')
save_csv(dates, 'data.csv')


players = get_match_page('https://www.vlr.gg/match/231556/100-thieves-vs-liquid-ignition-series')
save_json(players, 'players.json')
save_players_csv(players, 'players.csv')

