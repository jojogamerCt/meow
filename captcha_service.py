import os
import requests
from logger import Logger
from dotenv import load_dotenv
import configparser
import time
logger = Logger().get_logger()
load_dotenv()
from datetime import datetime

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
        max_attempts = 5
        timeout = 10  # Adjust the timeout based on your network speed and reliability
        # Create the directory if it doesn't exist
        if not os.path.exists("captchas"):
            os.makedirs("captchas")

                # Generate a unique ID for the image
        now = datetime.now()
        image_id = now.strftime("%d%m%Y%H%M%S%f")
        
        for attempt in range(max_attempts):
            try:
                response = requests.get(image_url, timeout=timeout)
                if response.status_code == 200:
                    with open(f"captchas/{image_id}.png", "wb") as file:
                        file.write(response.content)
                        
                    return f"captchas/{image_id}.png"
                else:
                    logger.error(f"Failed to download captcha, status code: {response.status_code}")
            except requests.exceptions.Timeout:
                logger.error(f"Timeout when trying to download captcha, attempt {attempt + 1}/{max_attempts}")
            except requests.exceptions.ConnectionError:
                logger.error(f"Connection error when trying to download captcha, attempt {attempt + 1}/{max_attempts}")

            time.sleep(1)  # Wait a second before retrying

        return None  # Return None if all attempts fail

    
    @staticmethod 
    def send_image(image_path):
        try:
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
        except Exception as e:
            logger.error(f"❌ Exception while sending image: {e}")
            return None