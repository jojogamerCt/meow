import json
import datetime
import os
from colorama import Fore, Style
from selenium.webdriver.remote.webdriver import WebDriver
import io
from PIL import Image
from logger import Logger
import datetime
from selenium.webdriver.remote.webelement import WebElement
logger = Logger().get_logger()

class ScreenshotHandler:
    def __init__(self, driver: WebDriver):
        self.driver = driver

        # Load the Pokemon info from the JSON file
        with open(os.path.join('commands', 'pokemon_info.json')) as f:
            self.pokemon_info_dict = json.load(f)

    def is_special(self, pokemon_name):
        # Check if the Pokemon is shiny or legendary
        rarity = self.pokemon_info_dict.get(pokemon_name, {}).get('Rarity', '')
        return rarity in ['Legendary', 'Shiny']
        
    def take_screenshot_by_element(self, element :WebElement, pokemon_name:str):
        now = datetime.datetime.now()
        time_string = now.strftime("%I_%M_%S_%p")
        image_binary = element.screenshot_as_png 
        img = Image.open(io.BytesIO(image_binary))

        # Get the absolute path of the root directory
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Create the screenshots directory in the root directory if it doesn't exist
        screenshots_dir = os.path.join(root_dir, 'screenshots')
        os.makedirs(screenshots_dir, exist_ok=True)

        # Save the screenshot
        screenshot_path = os.path.join(screenshots_dir, f"{pokemon_name}_{time_string}.png")
        img.save(screenshot_path)
        logger.info(f'{Fore.YELLOW}Screenshot taken of{Style.RESET_ALL} {Fore.GREEN}{pokemon_name}{Style.RESET_ALL} {Fore.YELLOW}and saved as {screenshot_path}{Style.RESET_ALL}')

    def take_screenshot(self, pokemon_name):
        if self.is_special(pokemon_name):
            now = datetime.datetime.now()
        if self.is_special(pokemon_name):
            # Take a screenshot
            self.driver.save_screenshot(f'{pokemon_name}_{datetime}.png')