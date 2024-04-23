from bs4 import BeautifulSoup
from commands.handlers.action_handler import ActionHandler
from driver import Driver
from helpers.sleep_helper import interruptible_sleep
from validators.response_validator import evaluate_response
from logger import Logger
import time
from validators.action import Action
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from settings import Settings
import json
import re
from catch_statistics import CatchStatistics
settings = Settings()
from helpers.handle_exception import handle_on_start_exceptions

logger = Logger().get_logger()
catch_statistics = CatchStatistics()

# Get the JSON string from the .ini
pokeball_for_pokemon = settings.pokemon_pokeball_mapping
rarity_pokeball_mapping = settings.rarity_pokeball_mapping
rarity_emoji = settings.rarity_emoji
fishing_ball = settings.fishing_ball
hunt_item_ball = settings.hunt_item_ball
fish_shiny_golden_ball = settings.fishing_shiny_golden_ball

class Fish(ActionHandler):
    def __init__(self, driver: Driver):
        super().__init__()
        self.driver = driver
        self.logger = Logger().get_logger()
    
    @handle_on_start_exceptions
    def start(self, command:str):
        self.command = command
        self.driver.write(command)
        pokemeow_element_response = self.driver.get_last_element_by_user("PokéMeow", timeout=30)
        action = evaluate_response(pokemeow_element_response)
        
        if action is Action.SKIP:
            interruptible_sleep(2)
            return
        
        if action is not Action.PROCEED:
            self.handle_action(action, self.driver, pokemeow_element_response)
            return
        
        li_element = self.driver.wait_for_element_text_to_change(pokemeow_element_response, check_every=0.2)
        
        if li_element is None:
            logger.error('No response from PokéMeow while fishing...')
            return
        
        try:

            # Try to pull rod
            button = li_element.find_element(By.TAG_NAME, "button")
            time.sleep(0.5)
            button.click()
            
            encounter_element = self.driver.wait_for_element_text_to_change(li_element, check_every=1)
            
            if "The Pokemon got away" in encounter_element.text:
                logger.info(f'🎣 [ESCAPED!] The Pokemon got away.')
                return
            
            spawn_info = self.get_spawn_info(encounter_element.get_attribute('outerHTML'))
            
            #IF shiny or golden fish, catch it
            if spawn_info["Shiny"] or spawn_info["Golden"]:
                self.driver.click_on_ball(fish_shiny_golden_ball)
            else:
                if spawn_info["Name"] in pokeball_for_pokemon:
                    ball = pokeball_for_pokemon[spawn_info["Name"]]
                    logger.info(f"🔴 Pokemon '{spawn_info['Name']}' found in the dictionary. Using {ball}...")
                    self.driver.click_on_ball(ball)
                else:
                    self.driver.click_on_ball(fishing_ball)
            
            catch_status_element = self.driver.wait_for_element_text_to_change(pokemeow_element_response)
            
            if catch_status_element is None:
                logger.error('No response from PokéMeow while fishing...')
                return
            
            self.get_catch_result(spawn_info, 0, catch_status_element)
            return
        except NoSuchElementException as e:
            
            logger.info(f'🎣 [ESCAPED!] No fish found.')
            return


    def get_spawn_info(self, element):
        # Parse the HTML content
        pokemon_info = {}
        soup = BeautifulSoup(element, "html.parser")
        # print(soup)
        pokemon_description = soup.select_one("div[class*='embedDescription']")

        pokemon_info["Item"] = data = soup.find('img', {'aria-label': ':held_item:'}) is not None

        if pokemon_description:
            # Find all strong elements within the description
            strong_elements = pokemon_description.find_all("strong")


            if strong_elements:
                # Get the last strong element
                last_strong_element = strong_elements[-1]

                # Extract Pokémon name
                pokemon_info["Name"] = last_strong_element.get_text(strip=True)
                    
                pokemon_info["Shiny"] = False
                pokemon_info["Golden"] = False
                
                if "shiny" in pokemon_info["Name"].lower():
                    pokemon_info["Shiny"] = True
                    
                if "golden" in pokemon_info["Name"].lower():
                    pokemon_info["Golden"] = True
        # print(pokemon_info)
        
        return pokemon_info
    
    
    def get_catch_result(self, pokemon_info, count, element):
        if isinstance(pokemon_info, str):
            pokemon_info = json.loads(pokemon_info)

        soup = BeautifulSoup(element.get_attribute('outerHTML'), "html.parser")
        pokemon_was_catched = soup.find_all(string=lambda text: '✅' in text)

        # Get the Pokemon name and rarity from pokemon_info
        pokemon_name = pokemon_info.get('Name')
        pokemon_rarity = pokemon_info.get('Rarity')
        has_item = pokemon_info.get('Item')
        emoji = rarity_emoji.get(pokemon_rarity, '')

        if pokemon_was_catched:
            footer_text = soup.find('div', class_='embedFooter_c26cec').get_text(strip=True)
            footer_text = soup.select_one('div[class*=embedFooter]').get_text(strip=True)
            fishing_tokens_match = re.search(r'earned (\d+) Fishing Token', footer_text)

            # Initialize fishing_tokens to 0, then update if found in the text
            fishing_tokens = 0
            if fishing_tokens_match:
                fishing_tokens = int(fishing_tokens_match.group(1))

            # Log the catch result with the number of Fishing Tokens earned
            #Print if shiny or golden fish, if golden print a golden emoji 🟡 if shiny print a shiny emoji
            catch_statistics.add_fish_encounter(fishing_tokens)
            if pokemon_info["Shiny"]:
                logger.info(f'🎣 [CATCHED!] {emoji} {pokemon_name} | Fishing Tokens: {fishing_tokens}'
                            f' | Shiny: ✨')
                return {'caught': True, 'fishing_tokens': fishing_tokens}
            elif pokemon_info["Golden"]:
                logger.info(f'🎣 [CATCHED!] {emoji} {pokemon_name} | Fishing Tokens: {fishing_tokens}'
                            f' | Golden: 🟡')
                return {'caught': True, 'fishing_tokens': fishing_tokens}
            
            # If the Pokémon was caught, log and return that information
            logger.info(f'🎣 [CATCHED!] Pokemon: {pokemon_name} | Fishing Tokens: {fishing_tokens}')
            return {'caught': True, 'fishing_tokens': fishing_tokens}
        else:
            # If the Pokémon was not caught, log and return that information
            logger.info(f'🎣 [ESCAPED!] Pokemon: {pokemon_name}')
            catch_statistics.add_fish_encounter(0)
            return {'caught': False, 'fishing_tokens': 0}