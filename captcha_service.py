import os
import uuid
from selenium.webdriver.common.by import By
import requests
from logger import Logger
from dotenv import load_dotenv
import configparser
import time
logger = Logger.getInstance().get_logger()
load_dotenv()


config = configparser.ConfigParser()

# Open the file with the 'utf-8' encoding and read it with config.read_file
with open('config.ini', 'r', encoding='utf-8') as f:
    config.read_file(f)

predict_captcha_url = config.get('settings', 'predict_captcha_url')
API_KEY = os.getenv('API_KEY')

class CaptchaService:
    
    @staticmethod 
    def download_captcha(href):
        image_url = href

        # Create the directory if it doesn't exist
        if not os.path.exists("captchas"):
            os.makedirs("captchas")

        # Generate a unique ID for the image
        image_id = uuid.uuid4()

        # Send a HTTP request to the URL of the image
        response = requests.get(image_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Open the file in write mode, write the contents of the response to it, and close it
            with open(f"captchas/image_{image_id}.png", "wb") as file:
                file.write(response.content)
                # Get the list of files in the captchas directory
            files = os.listdir("captchas")
            
            return f"captchas/image_{image_id}.png"
        
        return None
    
    @staticmethod 
    def send_image(image_path):
        url = predict_captcha_url
        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": "pokemeow-captcha-solver.p.rapidapi.com"
        }

        with open(image_path, "rb") as image_file:
            files = {"file": image_file}
            retry_delay = 5  # 5 seconds delay between retries
            for attempt in range(5):  # Retry up to 3 times
                logger.info(f"🚀 Sending image to RapidApi, attempt {attempt+1}...")
                try:
                    response = requests.post(url, files=files, headers=headers, timeout=35)
                    if response.status_code == 200:
                        logger.info("✅ Image sent successfully!")
                        return response.json()["number"]
                    else:
                        logger.error(f"❌ Failed to send image, status code: {response.status_code}")
                        logger.error(f"❌ Message: {response.text}")
                except requests.exceptions.Timeout:
                    logger.error("⏰ Request timed out, retrying...")
                except requests.exceptions.ConnectionError:
                    logger.error("🔌 Connection error, retrying...")
                except requests.exceptions.RequestException as e:
                    logger.error(f"🚫 Request error: {e}, retrying...")
                
                if attempt < 2:  # Avoid sleep after the last attempt
                    time.sleep(retry_delay)

        logger.info("❌ Failed to send image after 3 attempts")
        return None