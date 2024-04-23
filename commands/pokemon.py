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
from commands.inventory import Inventory
settings = Settings()

logger = Logger().get_logger()
catch_statistics = CatchStatistics()

# Get the JSON string from the .ini
pokeball_for_pokemon = settings.pokemon_pokeball_mapping
rarity_pokeball_mapping = settings.rarity_pokeball_mapping
rarity_emoji = settings.rarity_emoji
fishing_ball = settings.fishing_ball
hunt_item_ball = settings.hunt_item_ball
fish_shiny_golden_ball = settings.fishing_shiny_golden_ball
class Pokemon(ActionHandler):
    def __init__(self, driver: Driver):
        super().__init__()
        self.driver = driver
        self.logger = Logger().get_logger()
        self.encounter_counter = 0
        
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
        
        spawn_json = self.get_spawn_info(pokemeow_element_response)
        spawn_info = json.loads(spawn_json)
        
        rarity = spawn_info["Rarity"]
        ball = rarity_pokeball_mapping.get(rarity)
        has_item = spawn_info["Item"]
        if has_item and rarity not in "Legendary" and rarity not in "Shiny":
            self.driver.click_on_ball(hunt_item_ball)
        else:
            if spawn_info["Name"] in pokeball_for_pokemon:
                ball = pokeball_for_pokemon[spawn_info["Name"]]
                logger.info(f"🔴 Pokemon '{spawn_info['Name']}' found in the dictionary. Using {ball}...")
                self.driver.click_on_ball(ball)
            else:
                self.driver.click_on_ball(ball)
                
        self.encounter_counter += 1
        catch_status_element = self.driver.wait_for_element_text_to_change(pokemeow_element_response)
        self.get_catch_result(spawn_json, self.encounter_counter, catch_status_element)
        
        if spawn_info["Balls"]["Pokeballs"] <= 1 or spawn_info["Balls"]["Greatballs"] <= 1:
                    inventory = Inventory.check_inventory(self.driver)
                    self.driver.buy_balls(inventory)
    
    
    def get_spawn_info(self, element):
        
        pokemon_info = {}
        
        # Parse the HTML content
        soup = BeautifulSoup(element.get_attribute('outerHTML'), "html.parser")
        # Find the element containing the Pokémon description
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
                
        # span = soup.find('span', {'class': 'embedFooterText_dc937f'}) 
        span = soup.select_one("span[class*='embedFooterText']")

        text = span.get_text()
        # Use a regular expression to find the rarity
        rarity = re.search(r'(.+?)\s*\(', span.get_text())

        # Check if a match was found
        if rarity:
            # Get the first group of the match
            rarity = rarity.group(1).strip()
            pokemon_info["Rarity"] = rarity

        # Use a regular expression to find all occurrences of 'word: number'
        matches = re.findall(r'(\w+)\s*:\s*([\d,]+)', text)

        # Convert the matches to a dictionary
        data = {k: int(v.replace(',', '')) for k, v in matches}
        pokemon_info["Balls"] = data
        
        # Convert the dictionary to a JSON string
        json_data = json.dumps(pokemon_info)

        # Convert dictionary to JSON
        pokemon_json = json.dumps(pokemon_info, indent=4)
        catch_statistics.add_hunt_encounter()
        return pokemon_json
    
    def pause(self):
        catch_statistics.print_statistics()
        from instances.bot_instance import bot
        
        bot.disable_task(bot.hunting_task)
        logger.warning('[Hunting] Action Hunt is disabled.')
        logger.warning('[Hunting] Action Hunt is disabled.')
        logger.warning('[Hunting] Action Hunt is disabled.')
    
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
        # Check if any element contains the ✅ emoji
        if pokemon_was_catched:
            
            span = soup.find('span', class_=lambda value: value and 'embedFooterText' in value)

            # Get the text of the span
            text = span.get_text()

            # Use a regular expression to find the earned coins
            earned_coins = re.search(r'earned ([\d,]+) PokeCoins', text)
            
            # Assuming earned_coins is the result of a re.match or re.search operation
            if earned_coins is not None:
                earned_coins = int(earned_coins.group(1).replace(',', ''))
            else:
                logger.error("Failed to parse earned coins.")
                # Handle the error appropriately, e.g., by setting a default value or raising an exception
                earned_coins = 0


            if has_item:
                # Looking for the span that contains the text indicating the item received
                item_received_span = soup.find('span', string=lambda text: 'retrieved a' in text if text else False)        

                # Extracting the text of the next strong tag which should contain the name of the item received
                if item_received_span:
                    item_received = item_received_span.find_next('strong').text
                else:
                    item_received = "Unknown Item"
                    
                #TODO If shiny or legendary print log text in purple using colorama Fore.LIGHTMAGENTA_EX
                
                logger.info(f'🍚 [{count}] [CATCHED!] Rarity: {pokemon_rarity} {emoji} | Pokemon: {pokemon_name} | Earned Coins: {earned_coins} | Item: {item_received}')
                catch_statistics.add_catch(pokemon_rarity, earned_coins, item_received)
                return
            
            # Print the Pokemon name, rarity, and earned coins in one line
            logger.info(f'🍚 [{count}] [CATCHED!] Rarity: {pokemon_rarity} {emoji} | Pokemon: {pokemon_name} | Earned Coins: {earned_coins}')
            catch_statistics.add_catch(pokemon_rarity, earned_coins)
            return
        else:
            logger.info(f'🍚 [{count}] [ESCAPED!] Rarity: {pokemon_rarity} {emoji} | Pokemon: {pokemon_name}')
            return