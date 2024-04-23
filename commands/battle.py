from bs4 import BeautifulSoup
from commands.handlers.action_handler import ActionHandler
from driver import Driver
from validators.response_validator import evaluate_response
from logger import Logger
import time
from validators.action import Action
from selenium.webdriver.common.by import By
from catch_statistics import CatchStatistics
import re
catch_statistics = CatchStatistics()
logger = Logger().get_logger()


class Battle(ActionHandler):
    def __init__(self, driver: Driver):
        super().__init__()
        self.driver = driver
        self.logger = Logger().get_logger()
    
    
    def start(self, command:str):
        self.command = command
        
        self.driver.write(command)
        pokemeow_element_response = self.driver.get_last_element_by_user("PokéMeow", timeout=30)
        action = evaluate_response(pokemeow_element_response)
        
        if action is not Action.PROCEED:
            self.handle_action(action, self.driver, pokemeow_element_response)
            return
        
        logger.info('[Battle] Battle started!')
        # While message not into won battle or lost battle
        while True:
            last_element_html = self.driver.wait_next_message(timeout=20)
            if last_element_html is None:
                logger.error('No response found from PokéMeow while battling...')
                break
            time.sleep(1)
            
            if "won the battle" in last_element_html.text:
                try:
                    # last_element_html.find_element(By.XPATH, ".//button")
                    coins = self.extract_coins(last_element_html.get_attribute('innerHTML'))
                    items = self.extract_items(last_element_html.get_attribute('innerHTML'))
                    catch_statistics.add_battles_won(coins)
                    for item in items:
                        #get item quantity
                        catch_statistics.add_item(item, items[item])
                    # print the items and coins, if no items, print empty
                    if items:
                        logger.info(f'[Battle] Battle won! Coins: {coins}, Items: {items}')
                    else:
                        logger.info(f'[Battle] Battle won! Coins: {coins}')    
                    break
                except Exception as e:
                    logger.error(f"An error occurred while extracting items and coins: {e}")
                    break
            if "lost the battle" in last_element_html.text:
                logger.warning('[Battle] Battle lost!')
                break
            time.sleep(1)
            first_button = last_element_html.find_element(By.XPATH, ".//button")

            
            # Check if the button was found
            if first_button:
                # Click the first button
                logger.info('[Battle] Using the first attack button...')
                first_button.click()
            else:
                logger.info("[Battle] No button found")
    

    def extract_coins(self, html):
        soup = BeautifulSoup(html, 'html.parser')
    
        # Convert all sequences of whitespace characters to a single space
        text = ' '.join(soup.stripped_strings).replace(",", "").replace(" ", "")
        

        # Adjust regex to handle possible formatting issues
        coins_match = re.search(r'(\d+)PokeCoins', text)
        if coins_match:
            coins = int(coins_match.group(1))
        else:
            coins = 0
            
        return coins;
    
    def extract_items(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = {}
        
        div = soup.select_one('div[id^=message-content]')
        
        img_tags = div.find_all('img', alt=True)
        #remove pokecoin from match
        img_tags = [img for img in img_tags if img.get('alt') != ':PokeCoin:']

        for img in img_tags:
            alt_text = img.get('alt', '')
            item_match = re.match(r':([^:]+):', alt_text)
            if item_match:
                item_name = item_match.group(1)
                #Exploring just previous element for quantity information
                quantity_text = img.find_previous(string=re.compile(r'\d+x'))
                
                if quantity_text:
                    # print(f"Quantity text found: {quantity_text}")
                    quantity_match = re.search(r'(\d+)x', quantity_text)
                    if quantity_match:
                        quantity = int(quantity_match.group(1))
                        items[item_name] = items.get(item_name, 0) + quantity
        return items


