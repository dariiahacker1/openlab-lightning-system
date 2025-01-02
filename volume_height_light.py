import json
from openlab_lights import LightService, Color
import time

COLUMNS = 28
ROWS = 3

RED = Color(255)
GREEN = Color(0,255,4)
LIGHTGREEN = Color(114, 255, 2)
GOLD = Color(227,255,0)
ORANGE = Color(255,141,0)

file_path = "volume_data.json"

k = 200 / 30

ls = LightService()
black = Color(r = 0, g = 0, b = 0, w = 0)

try:
    while True:
        ls.turn_off()
    
        with open(file_path, "r") as file:
            for line in file:
                data = json.loads(line)
                volume_level = data.get("VolumeLevel")
        amount = int(volume_level / k) 
        if(amount > 28):
            amount = 28
        for i in range (1, amount):
            if (i < 6):
                ls.set_same_color([i, i + 28, i + 54], GREEN, fade = 0)

            elif (i < 11):
                ls.set_same_color([i, i + 28, i + 54], LIGHTGREEN, fade = 0)
                
            elif (i < 14):
                ls.set_same_color([i, i + 28, i + 54], GOLD, fade = 0)

            elif (i < 18):
                ls.set_same_color([i, i + 28, i + 54], ORANGE, fade = 0)            
            else:
                ls.set_same_color([i, i + 28, i + 54], RED, fade = 0)
            time.sleep(0.05)
        for i in range (amount, 1, -1):

            ls.set_same_color([i, i + 28, i + 54], black, fade = 0)
            time.sleep(0.05) 


        time.sleep(0.2)

finally:
    ls.turn_off()

