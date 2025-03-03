# Battery_Script

## Purpose
To help me monitor my battery and be more aware of its level through sound, changing colors, and text.

## Description
- Uses libraries `tkinter`, `psutil`, `random`, and `playsound` to accomplish its tasks.
- Creates a *(relatively)* small window that constantly shows the status of the battery through a percentage text, and a progress bar with variable color.

## Why?
- My laptop's battery has degraded to a point where if it reaches the threshold for the Windows OS to tell me "it's time to plug in", it'll immedaitely die. 
- Yes, I need to buy a new battery, but for now I decided this would be a good way to help me with my problem.
- The battery icon for Windows (in the bottom right corner) is not at all descriptive of what the battery percentage currently is, and for moments where I'm busy I don't have time to constantly hover over it to see its percentage.
- As far as the sound aspect goes, it helps for when I'm away from my laptop but have headphones in (happens often), and am not able to see my battery percentage. I'll hear the alert, and be able to know where my battery is roughly at, and how urgently I should return to plug it in.