from logger import Logger
from driver import Driver
from dotenv import load_dotenv
load_dotenv()
import os
from helpers.sleep_helper import interruptible_sleep
import configparser
config = configparser.ConfigParser()



logger = Logger.getInstance().get_logger()
            
if __name__ == "__main__":
    with open('config.ini', 'r', encoding='utf-8') as f:
        config.read_file(f)
    # Start the bot
    driver_path = config.get('settings', 'driver_path')
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    channel = os.getenv('CHANNEL')
    api_key = os.getenv('API_KEY')
    discord_token = os.getenv('DISCORD_TOKEN')
    
    main = Driver(driver_path)
    logger.info("🚀 Starting bot!")
    
    if os.path.exists("catch_counter.json"):
        os.remove("catch_counter.json")  

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
    