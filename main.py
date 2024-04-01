from logger import Logger
from driver import Driver
from dotenv import load_dotenv
load_dotenv()
import os
import time
import sys


DRIVER_PATH = os.getenv('DRIVER_PATH')
logger = Logger.getInstance().get_logger()

if __name__ == "__main__":
    # Start the bot
    
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    channel = os.getenv('CHANNEL')
    api_key = os.getenv('API_KEY')
    
    
    main = Driver(DRIVER_PATH)
    logger.info("🚀 Starting bot!")
    
    if os.path.exists("catch_counter.json"):
        os.remove("catch_counter.json")  

    main.start_driver()
    main.navigate_to_page("https://discord.com/login")
    main.login(email,password)
    main.navigate_to_page(channel)
    time.sleep(5)
    main.play()
    