from bs4 import BeautifulSoup
from driver import Driver
from helpers.sleep_helper import interruptible_sleep
from logger import Logger
from settings import Settings
from catch_statistics import CatchStatistics
settings = Settings()
catch_statistics = CatchStatistics()
logger = Logger().get_logger()


class Quest:
    @staticmethod
    def actions(driver: Driver, inventory):
        #Check quests
        logger.info("[Quest] Checking quests...")
        driver.write(";q")
        quests_element = driver.get_last_element_by_user("PokéMeow")
        
        if quests_element.text == "Please wait":
            interruptible_sleep(4.5)
            logger.info("[Quest] Please wait...")
            Quest.actions(driver, inventory)
            return
        # get html content of quests
        quests_list = Quest.get_quests_list(quests_element)
        reroll_count = next((item['count'] for item in inventory if item['name'] == 'questreset'), None)
        interruptible_sleep(4)
        if reroll_count and reroll_count > 0:
            for reroll in range(reroll_count):
                for quest in quests_list:
                    for key, value in quest.items():
                        if value != "dexcaught":
                            logger.info(f"[Quest] Rerolling quest {key}...")
                            quests_element = Quest.reroll_quest(driver, key)
                            interruptible_sleep(6)
                            if quests_element is None:
                                break
                            quests_list = Quest.get_quests_list(quests_element)
                            break
            

        
        logger.info(f"[Quest] Quests: {quests_list}")
        

    @staticmethod
    def get_quests_list(quests_element):
        import re
         # Function to check if a tag contains a partial class name
        def contains_partial_class(partial):
            return re.compile(".*" + partial + ".*")
    
        quests_html = quests_element.get_attribute('outerHTML')
        soup = BeautifulSoup(quests_html, 'html.parser')
        # get div container  with class gridContainer
        quests_container = soup.find('div', class_=contains_partial_class("gridContainer"))
        # Find all quest descriptions using a more specific selector if possible
        quests = quests_container.find_all('strong')
        quest_data = []

        # Extract quest number and emoji description
        for quest in quests:
            quest_number_str = quest.span.text.strip()
            match = re.search(r'\d+', quest_number_str)
            quest_number = int(match.group()) if match else 1

            emoji_img = quest.find_next("img", class_="emoji")  # Directly find the next emoji image
            if emoji_img and 'alt' in emoji_img.attrs:
                emoji = emoji_img['alt'].strip(':')
                quest_data.append({quest_number: emoji})
            else:
                print(f"DEBUG: Emoji image not found or missing 'alt' attribute in quest {quest_number_str}")

        return quest_data

        
    @staticmethod
    def reroll_quest(driver: Driver, quest_number: int):
        driver.write(f";q r {quest_number}")
        quests_element = driver.get_last_element_by_user("PokéMeow")
        if "Please wait" in quests_element.text:
            interruptible_sleep(3.5)
            logger.info("[Quest Reroll] Please wait...")
            return Quest.reroll_quest(driver, quest_number)
        
        if "You don't have any quest reset" in quests_element.text:
            logger.info("[Quest Reroll] You don't have any quest reset...")
            return None

        return quests_element