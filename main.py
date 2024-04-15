from logger import Logger
from driver import Driver
from dotenv import load_dotenv
load_dotenv()
import os
from helpers.sleep_helper import interruptible_sleep
import configparser
config = configparser.ConfigParser()
import sys


logger = Logger.getInstance().get_logger()
            
if __name__ == "__main__":
    with open('config.ini', 'r', encoding='utf-8') as f:
        config.read_file(f)
    # Start the bot
    driver_path = config.get('settings', 'driver_path')
    version = config.get('settings', 'version')
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    channel = os.getenv('CHANNEL')
    api_key = os.getenv('API_KEY')
    discord_token = os.getenv('DISCORD_TOKEN')
    
    main = Driver(driver_path)
    logger.info(f"🚀 Starting bot, version {version}!")
    logger.info("[Developer info] Keep updated on changes at Github: https://github.com/qqqwda/pokemeow-autoplay")
    logger.info("[Developer info] Keep updated on changes at Github: https://github.com/qqqwda/pokemeow-autoplay")
    
    if os.path.exists("catch_counter.json"):
        os.remove("catch_counter.json")  

    if not (api_key and len(api_key) > 25):
        logger.error("Error: Invalid API key.")
        logger.error("Please get you API key from https://rapidapi.com/qqqwda/api/pokemeow-captcha-solver")
        sys.exit(1)
  
    main.start_driver()
    #  check if discord_token is valid
    if discord_token and len(discord_token) > 25:
        main.inject_token(discord_token)
    else:
        main.navigate_to_page("https://discord.com/login")
        main.login(email,password)
    main.navigate_to_page(channel)
    interruptible_sleep(5)
    main.play()
    