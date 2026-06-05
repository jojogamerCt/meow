from commands.shop import Shop
from logger import Logger
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from captcha_service import CaptchaService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import SessionNotCreatedException
import random
import json
import colorama
from colorama import Fore, Back, Style
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import os
from selenium.common.exceptions import TimeoutException
import configparser
from catch_statistics import CatchStatistics
import chromedriver_autoinstaller
from helpers.sleep_helper import interruptible_sleep
load_dotenv()
config = configparser.ConfigParser()
from settings import Settings
from selenium.common.exceptions import WebDriverException
settings = Settings()
    
catch_statistics = CatchStatistics()


ENABLE_AUTO_BUY_BALLS = os.getenv('ENABLE_AUTO_BUY_BALLS') == 'True'
ENABLE_AUTO_RELEASE_DUPLICATES = os.getenv('ENABLE_AUTO_RELEASE_DUPLICATES') == 'True'
ENABLE_AUTO_EGG_HATCH = os.getenv('ENABLE_AUTO_EGG_HATCH') == 'True'
ENABLE_AUTO_LOOTBOX = os.getenv('ENABLE_AUTO_LOOTBOX_OPEN') == 'True'
ENABLE_FISHING = os.getenv('ENABLE_FISHING') == 'True'
ENABLE_BATTLE_NPC = os.getenv('ENABLE_BATTLE_NPC') == 'True'
ENABLE_HUNTING = os.getenv('ENABLE_HUNTING') == 'True'
ENABLE_AUTO_QUEST_REROLL = os.getenv('ENABLE_AUTO_QUEST_REROLL') == 'True'
ENABLE_RUN_PICTURES = os.getenv('ENABLE_RUN_PICTURES') == 'True'
ENABLE_CHROME_HEADLESS = os.getenv('ENABLE_CHROME_HEADLESS') == 'True'

logger = Logger().get_logger()
captcha_service = CaptchaService()

# Get the JSON string from the .ini
pokeball_for_pokemon = settings.pokemon_pokeball_mapping
rarity_pokeball_mapping = settings.rarity_pokeball_mapping
rarity_emoji = settings.rarity_emoji
fishing_ball = settings.fishing_ball
hunt_item_ball = settings.hunt_item_ball
fish_shiny_golden_ball = settings.fishing_shiny_golden_ball



class Driver:
    def __init__(self, driver_path):
        # Instance logger
        
        load_dotenv()
        self.driver_path = driver_path
        self.driver = None
        
    def start_driver(self):
        # Set up Chrome options
        options = Options()
        options.add_argument("--log-level=3")
        #Open the browser 1000x1000
        options.add_argument("--window-size=1000,1000")
        # Disable notifications
        options.add_argument("--disable-notifications")
        # Disable infobars
        options.add_argument("--disable-infobars")
        
        #make the driver lightweight
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--mute-audio")
        
        options.headless = ENABLE_CHROME_HEADLESS

        try:
            self.driver = webdriver.Chrome(executable_path=self.driver_path, options=options)
            
        except SessionNotCreatedException:
            logger.error("Error: The version of ChromeDriver is not compatible with your installed version of Google Chrome.")
            logger.error("Please update Google Chrome to the latest version or install a compatible version of ChromeDriver.")
            raise  # re-raise the exception after handling it
        except:
            logger.warning(f"Driver not found in path: {self.driver_path}")
            logger.warning(f"or version incompatible")
            logger.warning(f"Downloading compatible version...")
            chromedriver_autoinstaller.install()
            self.driver = webdriver.Chrome(options=options)
    
    def navigate_to_page(self, url):
        if self.driver is not None:
            self.driver.get(url)
        else:
            logger.info("Driver not started. Call start_driver first.")

    def quit_driver(self):
        if self.driver is not None:
            self.driver.quit()
        else:
            logger.info("Driver not started. Nothing to quit.")
            
    def inject_token(self, token) -> bool:
        logger.info("Loging with token!")
        # Open Discord login page
        self.driver.get("https://discord.com/login")

        # Inject token using JavaScript
        script = f"""
            const token = "{token}";
            setInterval(() => {{
                document.body.appendChild(document.createElement('iframe')).contentWindow.localStorage.token = `"${{token}}"`;
            }}, 50);
            setTimeout(() => {{
                location.reload();
            }}, 2500);
        """
        self.driver.execute_script(script)

        # Wait for the login process to complete
        # Wait for the URL to match 'https://discord.com/channels/@me'
        WebDriverWait(self.driver, 15).until(lambda d: d.current_url == 'https://discord.com/channels/@me')

        # Verify if login was successful (you can add your own logic here)
        if self.driver.current_url == "https://discord.com/channels/@me":
            logger.info("Login successful!")
            logger.info("Login successful!")
            logger.info("Login successful!")
            return True
        else:
            logger.error("Login with token failed.")
            logger.error("Login with token failed.")
            logger.error("Login with token failed.")
            return False
        
    def login(self, email, password):
        logger.info("Logging in using Email and Password...")
        
        for attempt in range(3):
            try:
                interruptible_sleep(5)
                
                email_field = self.driver.find_element(By.XPATH, "//input[@name='email']")
                email_field.send_keys(Keys.CONTROL + 'a')
                email_field.send_keys(Keys.DELETE)
                interruptible_sleep(1)
                email_field.send_keys(email)
                
                interruptible_sleep(1)
                
                password_field = self.driver.find_element(By.XPATH, "//input[@name='password']")
                password_field.send_keys(Keys.CONTROL + 'a')
                password_field.send_keys(Keys.DELETE)
                interruptible_sleep(1)
                password_field.send_keys(password)
                
                #Random number between 1 and 5
                sleep_time = random.randint(1, 5)
                interruptible_sleep(sleep_time)
                self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
                
                # Wait for the URL to match 'https://discord.com/channels/@me'
                WebDriverWait(self.driver, 15).until(lambda d: d.current_url == 'https://discord.com/channels/@me')

                # If the login was successful, print a message and break the loop
                logger.info('Login successful')
                break
            except Exception as e:
                logger.info(f'Login attempt {attempt + 1} failed')
        else:
            logger.error('All login attempts failed')
                
    def write(self, msg):
        # span = self.driver.find_element(By.XPATH, "//span[contains(@class='emptyText'])")
        span = self.driver.find_element(By.XPATH, "//span[contains(@class, 'emptyText')]")

        ActionChains(self.driver).send_keys_to_element(span, Keys.BACK_SPACE*20).send_keys_to_element(span, msg).perform()
        ActionChains(self.driver).send_keys_to_element(span, Keys.ENTER).perform()
    
    def click_next_button(self):
        try:
            # Wait until the 'Next' buttons are present (timeout after 10 seconds)
            wait = WebDriverWait(self.driver, 10)
            next_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'img[alt="arrow_forward"]')))

            # Select the last 'Next' button from the list
            if next_buttons:
                last_button = next_buttons[-1]
                # Scroll the last element into view
                self.driver.execute_script("arguments[0].scrollIntoView(true);", last_button)

                # Additional wait to handle dynamic content such as pop-ups or notifications
                time.sleep(1)  # Adjust sleep time based on observed behavior of the web page

                # Perform the click using ActionChains for better precision
                ActionChains(self.driver).move_to_element(last_button).click().perform()
                return True  # Return True indicating the action was successfully completed
            else:
                print("No 'Next' button found.")
                return False  # Return False if no buttons are found
        except TimeoutException:
            print("Timeout: 'Next' buttons not found or not clickable.")
            return False  # Return False indicating the action failed due to timeout
        except WebDriverException as e:
            print(f"Web driver error: {e}")
            return False  # Return False indicating the action failed due to a WebDriver issue
        except Exception as e:
            print(f"General error: {e}")
            return False  # Return False indicating the action failed due to some other error
       
    def get_last_message_from_user(self, username):
        try:
            # Fetch all message elements
            messages = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'messageListItem')]")

            # Iterate over messages in reverse to find the last message from the user
            for message in reversed(messages):
                user_elements = message.find_elements(By.XPATH, ".//span[contains(@class, 'username')]")
                if user_elements:
                    user_element = user_elements[-1]
                    if username in user_element.text:
                        # Find the message content
                        return message

            logger.info(f"Message from {username} not found.")
            return None

        except NoSuchElementException:
            logger.info("Error: Unable to locate element.")
            return None
        
    def get_captcha(self):
        try:
            div_element = self.get_last_message_from_user("PokéMeow")
            
            # Find the first a element within the div element
            a_element = div_element.find_elements(By.TAG_NAME, "a")[-1]

            # Now you can get the href attribute or do whatever you need with the a element
            href = a_element.get_attribute("href")
            
            img_path = captcha_service.download_captcha(href)
            
            return captcha_service.send_image(img_path)
        except StaleElementReferenceException:
            logger.error("StaleElementReferenceException occurred. Retrying...")
            time.sleep(1)
            return self.get_captcha()
      
    def get_last_element_by_user(self, username, timeout=30) -> WebElement:
        try:
            # Wait for a new message from the user to appear
            WebDriverWait(self.driver, timeout).until(
                lambda driver: self.check_for_new_message(username)
            )
            
            # Fetch all message elements
            messages = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'messageListItem')]")

            # Iterate over messages in reverse to find the last message from the user
            for message in reversed(messages):
                user_elements = message.find_elements(By.XPATH, ".//span[contains(@class, 'username')]")
                if user_elements:
                    user_element = user_elements[-1]
                    if username in user_element.text:
                        # Return the message element
                        return message

            logger.error(f"Message from {username} not found.")
            return None

        except TimeoutException:
            logger.error(f"Message from {username} not found. Timeout exceeded.")
            return None

        except NoSuchElementException:
            logger.error("Error: Unable to locate element.")
            return None

    def check_for_new_message(self, username):
        # Fetch all message elements
        messages = self.driver.find_elements(By.XPATH, "//li[contains(@class, 'messageListItem')]")

        # Check if the last message is from the user
        if messages:
            try:
                last_message = messages[-1]
                user_elements = last_message.find_elements(By.XPATH, ".//span[contains(@class, 'username')]")
                for user_element in user_elements:
                    if username in user_element.text:
                        return True
                return False
            except StaleElementReferenceException:
                return False

        return False
    
    def wait_for_element_text_to_change(self, element, timeout=15, check_every=1) -> WebElement:
        try:
            # Store the initial text of the element
            initial_text = element.text

            # Wait for the text of the element to change
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    # If the text of the element has changed, return the new text
                    if element.text != initial_text:
                        return element
                except StaleElementReferenceException:
                    # If the element is no longer attached to the DOM, return None
                    logger.error("Element is no longer attached to the DOM")
                    return None

                # Wait before checking the text of the element again
                time.sleep(check_every)

            # If the timeout is reached without the text of the element changing, return None
            logger.warning("Timeout reached without text change")
            return None

        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return None
      
    def solve_captcha(self, element):
        
        #Download the captcha image and send it to the API
        catch_statistics.add_captcha_encounter()
        number = self.get_captcha()
        
        if number is None:
            # If the captcha number is None, try again
            logger.error("Captcha number is None. Trying again...")
            time.sleep(3)
            number = self.get_captcha()
        
        # Write the captcha number in the chat
        logger.info(f"🔢 Captcha response: {number}")
        self.write(number)
        
        # Waits 120 seconds for the captcha to be solved
        pokemeow_last_message = self.wait_for_element_text_to_change(element, timeout=120)
        
        if "Thank you" in pokemeow_last_message.text:
            logger.warning('Captcha solved, continuing...')
            return
        else:
            logger.error('Captcha failed, trying again!')
            new_captcha_element = self.get_last_message_from_user("PokéMeow")
            self.solve_captcha(new_captcha_element)
    
    def get_next_ball(self, current_ball):
        
        balls_priority = {
            "masterball": 5,
            "premierball": 4,
            "ultraball": 3,
            "greatball": 2,
            "pokeball": 1
        }

        # Get the priority of the current ball
        current_priority = balls_priority.get(current_ball)

        # If the current ball is not in the dictionary or it's a Pokeball, return None
        if current_priority is None or current_priority == 1:
            return None

        # Find the ball with the next highest priority
        for ball, priority in sorted(balls_priority.items(), key=lambda item: item[1], reverse=True):
            if priority < current_priority:
                return ball
    
    def click_on_ball(self, ball, delay=1):
        # Attempt to find the specific ball first.
        try:
            time.sleep(delay)
            last_element_html = self.get_last_element_by_user("PokéMeow")
            balls = last_element_html.find_elements("css selector",f'img[alt="{ball}"]')
            if balls:
                # If the specific ball is found, click on the last occurrence of that ball.
                balls[-1].click()
            else:
                next_ball = self.get_next_ball(ball)
                logger.warning(f"{ball} not found. Trying {next_ball}")
                if next_ball is None:
                    logger.error("No more balls to try.")
                    return False
                self.click_on_ball(next_ball)
                
        except Exception as e:
            logger.log(f"An error occurred: {e}")
    
    def buy_balls(self, inventory):
        interruptible_sleep(5)
        # Initialize pokecoin count to 0
        budget = 0

        # Iterate over the inventory list
        for item in inventory:
            # Check if the item name is pokecoin
            if item["name"] == "pokecoin":
                # Update pokecoin count
                budget = item["count"]
                if budget > 200000:
                    budget = 200000
                break
            
        commands = Shop.generate_purchase_commands(budget)
        if not commands:
            logger.info("❌Not Enought budget to buy balls.")
            return
        
        for command in commands:
            #Wait 3 scs before writing next command
            logger.info(f'💰 {command}')
            self.write(command)
            interruptible_sleep(5.5)

    def wait_next_message(self, timeout=10):
        # Define the XPath
        xpath = f"//li[contains(@class, 'messageListItem')]"

        # Get the last message that currently matches the XPath
        old_messages = self.driver.find_elements(By.XPATH, xpath)
        old_last_message = old_messages[-1] if old_messages else None

        # Wait for a new message to appear
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: self.driver.find_elements(By.XPATH, xpath)[-1] != old_last_message
            )
            # Get the last message that matches the XPath after waiting
            new_messages = self.driver.find_elements(By.XPATH, xpath)
            # Return the new message
            return new_messages[-1]
        except TimeoutException:
            return None

    def refresh(self):
        logger.info("Refreshing the page...")
        self.driver.refresh()
        # Wait for the element to be visible, not just present
        element_locator = (By.XPATH, "//span[contains(@class, 'emptyText')]")
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(element_locator))
        logger.info("Page refreshed successfully.")
        
        
    def print_initial_message(self):
        logger.warning(f"{Fore.GREEN}Autplay Settings:{Style.RESET_ALL}")
        logger.warning("[Autplay settings] AutoBuy enabled: " + str(ENABLE_AUTO_BUY_BALLS))
        logger.warning("[Autplay settings] AutoLootbox enabled: " + str(ENABLE_AUTO_LOOTBOX))
        logger.warning("[Autplay settings] AutoRelease enabled: " + str(ENABLE_AUTO_RELEASE_DUPLICATES))
        logger.warning("[Autplay settings] AutoQuestReroll enabled: " + str(ENABLE_AUTO_QUEST_REROLL))
        logger.warning("[Autplay settings] AutoEgg enabled: " + str(ENABLE_AUTO_EGG_HATCH))
        logger.warning("[Autplay settings] [FISHING] enabled: " + str(ENABLE_FISHING))
        logger.warning("[Autplay settings] [BATTLE] enabled: " + str(ENABLE_BATTLE_NPC))
        logger.warning("[Autplay settings] [HUNTING] enabled: " + str(ENABLE_HUNTING))
        logger.warning("[Autplay settings] RunPictures enabled: " + str(ENABLE_RUN_PICTURES))
        logger.warning(f"{Fore.GREEN}Autplay Advice:{Style.RESET_ALL}")
        logger.warning("[Autplay Advice] you can pause the bot by pressing 'p' in the console")
        logger.warning("[Autplay Advice] you can see statistics by pressing 's' in the console")
        logger.warning("[Autplay Advice] you can resume the bot by pressing 'enter' in the console")
        logger.warning("[Autplay Advice] you can stop the bot by pressing 'ctrl + c' in the console")
        logger.warning("[Autplay Advice] you ENABLE/DISABLE [BATTLE] by pressing 'b' in the console")
        logger.warning("[Autplay Advice] you ENABLE/DISABLE [FISHING] by pressing 'f' in the console")
        logger.warning("[Autplay Advice] you ENABLE/DISABLE [HUNTING] by pressing 'h' in the console")
        logger.warning(f"[Autplay Advice] you ENABLE/DISABLE [EXPLORE] by pressing 'e' in the console {Fore.RED}(Only for Pokémeow patreons!){Style.RESET_ALL}")
        logger.warning(f"{Fore.GREEN}Config.ini Settings:{Style.RESET_ALL}")
        logger.warning('[config.ini] Default ball for Fishing: %s', fishing_ball)
        logger.warning('[config.ini] Default ball for Pokemons with Held Items: %s', hunt_item_ball)
        logger.warning('[config.ini] Default ball for Shinies or Golden while Fishing: %s', fish_shiny_golden_ball)
        logger.warning("="*60 + "\n")      
        API_KEY = os.getenv('API_KEY')
        welcome_message = f"""
        {Fore.LIGHTMAGENTA_EX}
              __  __                      
             |  \/  |  ___  ___ __      __
             | |\/| | / _ \/ _ \\ \ /\ / /
             | |  | ||  __/ (_) |\ V  V / 
             |_|  |_| \___|\___/  \_/\_/  
                                          
               _   _  _              _               
              / \ | || |  ___  _ __ | |  __ _  _   _ 
             / _ \| || | / _ \| '__|| | / _` || | | |
            / ___ \| || || (_) || |   | || (_| || |_| |
           /_/   \_\_||_| \___/ |_|   |_| \__,_| \__, |
                                                 |___/ {Style.RESET_ALL}  Version: {settings.version}

        """
        print(welcome_message)
        logger.info("[Developer info] Keep updated on changes at Github: https://github.com/jojogamerCt/meow")
        logger.info("[Developer info] Keep updated on changes at Github: https://github.com/jojogamerCt/meow")
        print("\n")
        
        API_KEY = os.getenv('API_KEY') or ""
        predict_url = settings.predict_captcha_url
        is_local = "localhost" in predict_url or "127.0.0.1" in predict_url

        if is_local:
            logger.info("ℹ️ Using local captcha solver, skipping API_KEY length validation.")
        else:
            #Check that api key len is up to 20
            if len(API_KEY) < 20:
                logger.error("API_KEY not found or invalid. Please add your API_KEY in the .env or bat file !")
                logger.error("Quitting driver !")
                self.driver.quit()
                return
    
    def validate(self):
        pokemeow_last_message = self.get_last_message_from_user("PokéMeow")
        
        if pokemeow_last_message is None:
            return
        
        if "A wild Captcha appeared!" in pokemeow_last_message.text:
            logger.warning('Captcha detected!')
            self.solve_captcha(pokemeow_last_message)
