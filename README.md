# PokéMeow autoplay 🚀

This Python application is designed to automate the process of catching Pokemons in the popular Discord game, PokéMeow. Utilizing Selenium and ChromeDriver.

![image](https://github.com/qqqwda/pokemeow-autoplay/assets/41929135/c09acb38-34a6-4e68-9a18-08e211e89e61)


# [🎥 DEMO](https://www.youtube.com/watch?v=gJrNCuFWc-g&ab_channel=Crossedelboom)

## ⚠️ Disclaimer
Please note, while this bot is designed to automate tasks within PokeMeow, users are encouraged to use it responsibly and in accordance with the game's terms of service. The developer of this bot assumes no responsibility for any bans or penalties that may result from the use of this bot. Users should be aware of PokeMeow's rules and use the bot at their own risk.


## Updates 📢
- **Captcha Solving Endpoint 🧩**: An update has been made to include an endpoint for Captcha Solving. This feature is now fully operational!
- **New Captcha Solver API ✨**: We are excited to introduce a new API for captcha solving! You can find it here: [PokeMeow Captcha Solver](https://rapidapi.com/qqqwda/api/pokemeow-captcha-solver). Please note that this service might operate with some delay.

## Captcha Solver Accuracy and Latency ⚙️🕒
The captcha solver currently boasts around a 90% accuracy rate 🎯. However, expect some low latency due to hosting conditions 🐢. We are continuously working to improve this service for a smoother experience.

## 🚀 Setup Instructions

1. **Install Python 3.10:** Ensure you have Python 3.10 installed on your system. You can download it from the official Python website. 📥
2. **Clone the Repository:** Clone this repository to your local machine or download the source code. 📂
3. **Check Chrome Version:** Before installing ChromeDriver, it's important to check your current version of Google Chrome to ensure compatibility. Open Google Chrome, click on the three dots in the upper right corner to open the menu, then go to "Help" > "About Google Chrome". Your Chrome version will be displayed here. 🔍
4. **Download ChromeDriver:** Depending on your Chrome version, download the corresponding ChromeDriver.
   - For Chrome Version 121 or higher: [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/)
   - For Chrome Version lower than 121: [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
   - Paste / Replace the `chromedriver.exe` inside the `'webdrivers\Chrome'` folder. 📦
5. **Install Dependencies:** Run `pip install -r requirements.txt` in your terminal to install the necessary dependencies. 🛠️
6. **Configure Environment Variables:** Setup your environment variables by creating a `.env` file in the root directory. Include your Discord and PokeMeow credentials, channel URL, Pokemon catching strategy dictionary, ChromeDriver path, and the URL for the captcha prediction service. ⚙️


    Get the API-KEY 🔑: [PokeMeow Captcha Solver](https://rapidapi.com/qqqwda/api/pokemeow-captcha-solver)


    Edit the `run_account_example.bat` (You can use Email and Password or Discord token):

    ```plaintext
    pip install -r requirements.txt
   set SESSION_NAME=account1
   set EMAIL=email1@gmail.com
   set PASSWORD=strongpassword
   set CHANNEL=https://discord.com/channels/id/channel
   set API_KEY=RAPID-API-KEY
   set DISCORD_TOKEN=DISCORD-TOKEN
   set ENABLE_AUTO_BUY_BALLS=True
   set ENABLE_AUTO_RELEASE_DUPLICATES=False
   set ENABLE_AUTO_EGG_HATCH=True
   set ENABLE_AUTO_LOOTBOX_OPEN=True
   set ENABLE_FISHING=False
   set ENABLE_BATTLE_NPC=False
   py main.py
   pause
    ```
   Setup your settings `config.ini`
    ```plaintext
   [settings]
   rarity_emoji={
       "Legendary": "🔮", 
       "Shiny": "✨", 
       "Super": "★", 
       "Super Rare": "★ ★", 
       "Rare": "★", 
       "Uncommon": "♦",
       "Common": "●"
        }
   
   rarity_pokeball_mapping={
       "Legendary": "masterball",
       "Shiny": "masterball",
       "Super": "ultraball",
       "Super Rare": "ultraball", 
       "Rare": "greatball", 
       "Uncommon": "pokeball", 
       "Common": "pokeball"
       }
   
   pokemon_pokeball_mapping = {
       "Shieldon": "greatball",
       "Machoke": "greatball",
       "Magikarp": "greatball"
       }
   
   fishing_ball = greatball
   
   hunt_item_ball = ultraball
   
   fishing_shiny_golden_ball = masterball
   
   driver_path = webdrivers\Chrome\chromedriver.exe
   
   predict_captcha_url=https://pokemeow-captcha-solver.p.rapidapi.com/predict
    ```

## 📬 Contact

For support, questions, or collaboration, feel free to contact me on Discord:

- Discord: cursedelboom
