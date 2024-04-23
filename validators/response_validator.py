
from selenium.webdriver.remote.webelement import WebElement
from helpers.sleep_helper import interruptible_sleep
from logger import Logger
from validators.action import Action
logger = Logger().get_logger()
    
def evaluate_response(pokemeow_element_response:WebElement) -> Action:
    
    if pokemeow_element_response is None:
        logger.error('No response from PokéMeow, trying again...')
        return Action.RETRY
    
    if "A wild Captcha appeared!" in pokemeow_element_response.text:
        logger.warning('A wild Captcha appeared!')
        return Action.SOLVE_CAPTCHA
        
    if "Please wait" in pokemeow_element_response.text:
        logger.info('Please wait...')
        interruptible_sleep(1.5)
        return Action.RETRY
    
    if "Please catch the" in pokemeow_element_response.text:
        logger.error('Please catch the Pokemon you spawned first!')
        return Action.CATCH_AGAIN
    
    if "You can now catch" in pokemeow_element_response.text:
        logger.info('You can now catch Pokemon again.')
        interruptible_sleep(3)
        return Action.RETRY
    
    if "Not even a nibble" in pokemeow_element_response.text:
        logger.info('🎣 [ESCAPED!] Not even a nibble...')
        return Action.SKIP
    
    if "reached your daily catch" in pokemeow_element_response.text:
        logger.warning('You reached your daily catch limit. Stopping the bot...')
        logger.warning('You reached your daily catch limit. Stopping the bot...')
        logger.warning('You reached your daily catch limit. Stopping the bot...')
        return Action.PAUSE
       
    return Action.PROCEED