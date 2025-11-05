# analyzer/rules/selection_of_unseen_units/update_vision_data.py

import requests
from bs4 import BeautifulSoup
import json
import os
import re

LIQUIPEDIA_URL = "https://liquipedia.net/starcraft2/Vision"
CONFIG_FILE_NAME = "selection_of_unseen_units_v1.0.json"

def fetch_and_parse_vision_data():
    response = requests.get(LIQUIPEDIA_URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    vision_data = {
        "comment": "Unit and building vision ranges for StarCraft II. Default building vision is 9.",
        "units": {},
        "buildings": {"default": 9}
    }

    content_div = soup.find('div', class_='mw-parser-output')
    if not content_div:
        print("Could not find content div on Liquipedia page.")
        return vision_data

    # Find all tables with the 'wikitable' class
    wikitables = content_div.find_all('table', class_=lambda x: x and 'wikitable' in x.split())

    if not wikitables:
        print("No wikitables found.")
        return vision_data

    # The first wikitable on the page contains the main vision data
    main_table = wikitables[0]
    rows = main_table.find_all('tr')

    for row in rows[1:]: # Skip header row
        cols = row.find_all('td')
        if len(cols) >= 3: # Unit, Race, Vision
            unit_name_tag = cols[0].find('a')
            vision_range_text = cols[2].get_text(strip=True)

            if unit_name_tag and vision_range_text:
                unit_name = unit_name_tag.get_text(strip=True)
                # Clean up unit names (e.g., remove parenthesized info, spaces)
                clean_unit_name = re.sub(r'\s*\([^)]*\)', '', unit_name).replace(' ', '').strip()

                # Extract numerical part of vision range
                match = re.search(r'\d+(\.\d+)?', vision_range_text)
                if match:
                    try:
                        vision_range = float(match.group(0))
                        if clean_unit_name:
                            vision_data['units'][clean_unit_name] = vision_range
                    except ValueError:
                        pass # Ignore if not a valid number
    return vision_data

def update_config_file(new_vision_data):
    CONFIG_FILE_NAME = "selection_of_unseen_units_v1.0.json"
    config_path = os.path.join(os.path.dirname(__file__), CONFIG_FILE_NAME)
    with open(config_path, 'w') as f:
        json.dump(new_vision_data, f, indent=2)
    print(f"Updated {CONFIG_FILE_NAME} with new vision data.")

if __name__ == "__main__":
    print(f"Fetching vision data from {LIQUIPEDIA_URL}...")
    new_data = fetch_and_parse_vision_data()
    if new_data['units']:
        update_config_file(new_data)
    else:
        print("No unit vision data found. Config file not updated.")
