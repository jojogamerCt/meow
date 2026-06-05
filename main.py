from instances.bot_instance import bot, logger, driver, catch_statistics, settings
import os
from helpers.sleep_helper import interruptible_sleep
import threading
import sys
bat_file_name = None



def try_login(driver):
    if len(sys.argv) > 1:
        bat_file_name = [sys.argv[1]]
    
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    channel = os.getenv('CHANNEL')
    api_key = os.getenv('API_KEY')
    discord_token = os.getenv('DISCORD_TOKEN')

    driver.start_driver()
    #  check if discord_token is valid
    if discord_token and len(discord_token) > 25:
        if not driver.inject_token(discord_token):
            driver.navigate_to_page("https://discord.com/login")
            driver.login(email,password) 
    else:
        driver.navigate_to_page("https://discord.com/login")
        driver.login(email,password)
    # Check if channel URL is a template placeholder
    if not channel or channel.endswith("/channel") or "id/channel" in channel:
        logger.error("❌ ERROR: Your CHANNEL URL in the bat file is invalid or still using a placeholder!")
        logger.error("It should end with a channel ID number, for example: https://discord.com/channels/1512492330857533442/1512492330857533445")
        logger.error("Please edit your run_account.bat file and set a valid channel URL.")
        driver.quit_driver()
        sys.exit(1)

    driver.navigate_to_page(channel)
    interruptible_sleep(5)
    
     
if __name__ == "__main__":
    try_login(driver)
    driver.validate()
    driver.print_initial_message()
    threading.Thread(target=bot.scheduler.run).start()
