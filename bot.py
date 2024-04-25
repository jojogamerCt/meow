# bot.py
import random
from helpers.scheduler import Scheduler, Task
from commands.battle import Battle
from commands.fish import Fish
from commands.pokemon import Pokemon
from commands.inventory import Inventory
import os

ENABLE_FISHING = os.getenv('ENABLE_FISHING') == 'True'
ENABLE_BATTLE_NPC = os.getenv('ENABLE_BATTLE_NPC') == 'True'
ENABLE_HUNTING = os.getenv('ENABLE_HUNTING') == 'True'

class Bot:
    
    def __init__(self, driver):
        self.scheduler = Scheduler()
        self.battle = Battle(driver)
        self.fish = Fish(driver)
        self.pokemon = Pokemon(driver)
        
        task_settings = {
            'inventory_task': [True],
            'fishing_task': [ENABLE_FISHING],
            'hunting_task': [ENABLE_HUNTING],
            'battle_task': [ENABLE_BATTLE_NPC],
        }
        
        self.inventory_task = Task(lambda: Inventory.check_inventory(driver), lambda: ( (7*4)*50))
        self.battle_task = Task(lambda: self.battle.start(";b npc 1"), lambda: random.randint(39, 42))
        self.fishing_task = Task(lambda: self.fish.start(";f"), lambda: random.randint(19, 21))
        self.hunting_task = Task(lambda: self.pokemon.start(";p"), lambda: random.randint(7, 11))
        
        self.scheduler.add_task(self.inventory_task)
        self.scheduler.add_task(self.battle_task)
        self.scheduler.add_task(self.fishing_task)
        self.scheduler.add_task(self.hunting_task)
        
        for task_name, settings in task_settings.items():
            if any(settings):
                getattr(self, task_name).enable()
            else:
                getattr(self, task_name).disable()
        

    def enable_task(self, task):
        task.enable()

    def disable_task(self, task):
        task.disable()
    
    def switch_task(self, task):
        if task.enabled:
            self.disable_task(task)
        else:
            self.enable_task(task)
