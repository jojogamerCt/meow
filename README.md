# PokéMeow autoplay 🚀

This application is designed to automate the process of catching Pokemons in the popular Discord game, PokéMeow. Utilizing Selenium and ChromeDriver.

![image](https://github.com/qqqwda/pokemeow-autoplay/assets/41929135/21d0385d-9bbf-41f5-87ff-47c189131c8f)


## Main Features
   ![Wailord](https://cdn.discordapp.com/emojis/722255594660036609.webp?size=96&quality=lossless) ![Gyarados](https://cdn.discordapp.com/emojis/722263017513025547.webp?size=96&quality=lossless) ![Wailord](https://cdn.discordapp.com/emojis/722273142109896764.webp?size=44&quality=lossless)
- Hunting/Pokemon: `;p`
- Fishing: `;f` 🎣 
- Battle: `;battle npc 1` (Recommend set Wailord lvl. 100) `;team set wailord 1`
- Explore: `;explore grass/fire` 🗺️ (⚠️This feature is only for **Pokémeow patreons!** This is still in beta, might change in the future and **EXPECT BUGS**)
- Captcha solver: captcha solver currently boasts around a 90% accuracy rate 🎯.

## Extra Features


- Inventory check: `;inv` 🎒
- Hatch Egg: `;egg hatch / ;egg hold` ![image](https://github.com/qqqwda/pokemeow-autoplay/assets/41929135/bdbe953b-285d-4b8a-8faf-a02c17e9fa93)
- Lootbox Open: `;lb all` ![image](https://github.com/qqqwda/pokemeow-autoplay/assets/41929135/1e80f3f0-0b75-402e-9ba1-775073bd9b22)
- Quest reroll: `;q r {quest_id}` 🔄 (reroll until is a catching related quest)
- Screenshots: When finding a Shiny/Golden/Legendary it will take a screenshot 📷 and save it in `screenshot` folder (Set to True `ENABLE_RUN_PICTURES` to Enable)

## Future Features

- Research: `;res / ;res ex` 🔍
- Catchbot: `;cb run / ;cb` 
- Release: `;release duplicates` 🗑️
- Daily: `;d`
- Swap: `;swap {pokemon_name}`


## Commands

- Press `Enter` in console to resume program.
- Press `'p'` in console to **PAUSE** program.
- Press `'s'` in console to **SHOW SESSION STATISTICS**.
- Press `'b'` in console to Enable/Disable  **BATTLE** Task: `;battle npc 1`.
- Press `'f'` in console to Enable/Disable **FISHING** Task: `;f`.
- Press `'h'` in console to Enable/Disable **HUNTING/CATCHING** Task. `;p`.
- Press `'e'` in console to Enable/Disable **EXPLORE** Task. `;explore fire/grass`.

## 🚀 [Setup Instructions Video](https://www.youtube.com/watch?v=ZH7YryYCqg4)
<p align="center">
   Click on this image or https://www.youtube.com/watch?v=ZH7YryYCqg4
</p>
<p align="center">
  <a href="https://www.youtube.com/watch?v=ZH7YryYCqg4">
    <img src="https://github.com/qqqwda/pokemeow-autoplay/assets/41929135/72825f7f-f059-4d1c-b8bd-42f55ae51272" width="50%">
  </a>
</p>

## 🚀 Setup Instructions
 Install Python >= 3.9

 Get your API-KEY 🔑: [PokeMeow Captcha Solver](https://rapidapi.com/qqqwda/api/pokemeow-captcha-solver)


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
set ENABLE_AUTO_QUEST_REROLL=True
set ENABLE_FISHING=False
set ENABLE_BATTLE_NPC=False
set ENABLE_HUNTING=True
set ENABLE_EXPLORING=False
set ENABLE_CHROME_HEADLESS=True
set ENABLE_RUN_PICTURES=False
py main.py %0
pause
   ```

- `ENABLE_AUTO_BUY_BALLS` enables `;s b {ball id} {ball amount}`
- `ENABLE_AUTO_RELEASE_DUPLICATES` TODO
- `ENABLE_AUTO_EGG_HATCH` enables `;egg hold` `;egg hatch` when checks inventory
- `ENABLE_AUTO_LOOTBOX_OPEN` enables `;lb all` when it reaches 10 lootboxes or more
- `ENABLE_AUTO_QUEST_REROLL` enables `;quest reroll [id]` (Will reroll until a hunting quest related)
- `ENABLE_FISHING` enables `;f`
- `ENABLE_BATTLE_NPC` enables `;battle npc 1`
- `ENABLE_HUNTING` enables main feature `;p`
- `ENABLE_EXPLORING` enables explore feature `;explore grass/fire`
- `ENABLE_CHROME_HEADLESS` enable this for better performance, if you enable this, the chromedriver will run in headless mode (Recommended)
- `ENABLE_RUN_PICTURES` enable this if you want to save an image of every Legendary, Shiny or Golden that you caught, the image will be saved in `screenshots` folder

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
To run just double click on `run_account_example.bat`  file

Do you want to add another account? 

Create another `run_account_example_2.bat`  file

## Get Discord Token Script
```plaintext
(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()
```

## ⚠️ Disclaimer
Please note, while this bot is designed to automate tasks within PokeMeow, users are encouraged to use it responsibly and in accordance with the game's terms of service. The developer of this bot assumes no responsibility for any bans or penalties that may result from the use of this bot. Users should be aware of PokeMeow's rules and use the bot at their own risk.

