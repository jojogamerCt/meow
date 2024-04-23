from driver import Driver
from helpers.sleep_helper import interruptible_sleep
from logger import Logger
from settings import Settings
from catch_statistics import CatchStatistics
settings = Settings()
catch_statistics = CatchStatistics()
logger = Logger().get_logger()

class Lootbox:
    @staticmethod
    def actions(driver: Driver, inventory):
        logger.info(f"[Lootbox actions] You have {Lootbox.get_lootbox_amount(inventory)} lootbox...")
        if Lootbox.get_lootbox_amount(inventory) >= 10:
            logger.info(f"Opening {Lootbox.get_lootbox_amount(inventory)} lootbox...")
            driver.write(";lb all")
            # lootbox_response = driver.get_last_element_by_user("PokéMeow", timeout=30)
        
    @staticmethod
    def get_lootbox_amount(inventory) -> int:
        return next((item['count'] for item in inventory if item['name'] == 'lootbox'), None)