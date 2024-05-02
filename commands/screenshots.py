import json
import datetime
import os
from selenium.webdriver.remote.webdriver import WebDriver

class ScreenshotHandler:
    def __init__(self, driver: WebDriver):
        self.driver = driver

        # Load the Pokemon info from the JSON file
        with open(os.path.join('data', 'pokemon_info.json')) as f:
            self.pokemon_info_dict = json.load(f)

    def is_special(self, pokemon_name):
        # Check if the Pokemon is shiny or legendary
        rarity = self.pokemon_info_dict.get(pokemon_name, {}).get('Rarity', '')
        return rarity in ['Legendary', 'Shiny']

    def take_screenshot(self, pokemon_name):
        if self.is_special(pokemon_name):
            # Take a screenshot
            self.driver.save_screenshot(f'{pokemon_name}_{datetime}.png')