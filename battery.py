"""
Author: David De La Cruz
Date: March 2nd, 2025
File: battery.py
Description: A script I made to help me monitor and be more aware of my laptop's battery.
"""


from playsound import playsound
import psutil
import tkinter as tk
from tkinter import ttk
import random


def setCustomizations():
    # Helper function to help hide a lot of the customizations going on
    global high_battery_color, medium_battery_color, low_battery_color, window_color, font_type, number_color, charging_color, unplugged_color
    global low_battery_interval, medium_battery_interval, big_font_size, small_font_size
    high_battery_color, medium_battery_color, low_battery_color = "#024096", "#bd9100", "#960202"
    window_color = "#000000" 
    number_color = "#FFFFFF"
    charging_color = "#00ff00"
    unplugged_color = "#ff0000"
    font_type = "Courier New CE"
    low_battery_interval = (0, 25)
    medium_battery_interval = (25, 40)
    big_font_size, small_font_size = 48, 24

    # How to choose colors? 
    # --> Go to Google and search "color picker", it has a built in color picker that also shows the current color's hex values


def get_random_color():
    color = "#"
    for _ in range(6):
        num = random.randint(0, 15)    # Get random number valid for base 16 (hexadecimal)
        color_val = str(hex(num))[2:]  # Note: hex(num) will return 0x..., so we convert to string and get everything after the "0x"
        color += color_val

    return color


def progress_bar_color(value):
    global low_battery_interval
    global medium_battery_interval
    global s
    if low_battery_interval[0] < value <= low_battery_interval[1]:
        return "red.Horizontal.TProgressbar"
    elif medium_battery_interval[0] < value <= medium_battery_interval[1]:
        return "yellow.Horizontal.TProgressbar"
    elif medium_battery_interval[1] < value < 100:
        return "green.Horizontal.TProgressbar"
    else:
        # When battery at 100%, regardless of charging status, update bar to random colors
        # This is useful for when I need to have laptop plugged in and am playing a game,
        # I don't want to get my ears constantly blasted while playing something
        random_color = get_random_color()
        s.configure("white.Horizontal.TProgressbar", background=random_color, troughcolor=window_color)
        return "white.Horizontal.TProgressbar"

    

def play_alert(charging, color):
    """
    ** >> READ << **
    When using `playsound` it will play the audio file at the MAXIMUM volume that you're sound mixer is currently at!
    Personally, I just use OBS to record some sound I want, play it with maximum volume to see how loud it is, then
    use editing software to further edit the sound as I want.
    """
    global loop_count  # 1 loop currently occurs every 5 seconds
    global forceable

    if (color == "yellow.Horizontal.TProgressbar" or color == "red.Horizontal.TProgressbar") and charging == "Not Charging":

        # Play yellow alert sound every 105 seconds (1:45 mins)
        if color == "yellow.Horizontal.TProgressbar" and loop_count % 15 == 0:
            playsound("Path_to_audio_file", block=False)
        
        # Play red alert
        elif color == "red.Horizontal.TProgressbar":
            # Allow red alert's condition to be true first time red is reached so I immediately know
            if forceable:
                loop_count = 0 # This makes it so that the next condition is True
                forceable = False 
            
            # Play red alert every 25 seconds
            if loop_count % 5 == 0:
                playsound("Path_to_audio_file", block=False)
        
        loop_count += 1

    # Reset loop count and force-ability if we're charging
    else:
        loop_count = 0
        forceable = True

# ----------------------------------------------------------------------------------------------------------------

# Initialize variables
high_battery_color, medium_battery_color, low_battery_color, window_color, font_type, number_color, charging_color, unplugged_color = "", "", "", "", "", "", "", ""
low_battery_interval = ()
medium_battery_interval = ()
big_font_size, small_font_size = -1, -1

# Set Customizations
setCustomizations()

# Create the main window
root = tk.Tk()
root.title("Battery Monitor")
root.configure(bg=window_color)
root.attributes('-topmost', 1)  # Always on top
root.resizable(False, False)  # Can't resize
root.option_add('*tearOff', False)  # Remove the dashed line thing of each menu 

# Style for colors and customizations
s = ttk.Style()
s.theme_use('default')
s.configure("TProgressbar", thickness=50)
s.configure("red.Horizontal.TProgressbar", background=low_battery_color, troughcolor=window_color)
s.configure("yellow.Horizontal.TProgressbar", background=medium_battery_color, troughcolor=window_color)
s.configure("green.Horizontal.TProgressbar", background=high_battery_color, troughcolor=window_color)
s.configure("white.Horizontal.TProgressbar", background="#FFFFFF", troughcolor=window_color)

# Create battery level text
percentage_label = tk.Label(root, text="null", font=(font_type, big_font_size))
percentage_label.pack()

# Create charging status text
charging_label = tk.Label(root, text="null", font=(font_type, small_font_size))
charging_label.pack()

# Create a progress bar
progress_bar = ttk.Progressbar(root, style="red.Horizontal.TProgressbar", orient="horizontal", length=250, mode="determinate")
progress_bar.pack(pady=15)

# Get battery
battery = psutil.sensors_battery()
percent = str(battery.percent)    

# Get plugged status
plugged = battery.power_plugged
plugged_color = charging_color if plugged else unplugged_color
plugged = ">> Charging <<" if plugged else "Not Charging"

# Update the progress bar and labels
progress_bar["value"] = int(percent)
prog_bar_color = progress_bar_color(int(percent))
progress_bar["style"] = prog_bar_color
percent_text = f'{percent}%'
percentage_label.config(text=percent_text, fg=number_color, bg=window_color)
charging_label.config(text=plugged, fg=plugged_color, bg=window_color)

loop_count = 0
forceable = True
play_alert(plugged, prog_bar_color)


def main_loop():
    battery = psutil.sensors_battery()

    # Percentage values
    percent = str(battery.percent)    
    percent_text = f'{percent}%'

    # Charging status
    plugged = battery.power_plugged
    plugged_color = charging_color if plugged else unplugged_color
    plugged = ">> Charging <<" if plugged else "Not Charging"

    # Update the progress bar and labels
    progress_bar["value"] = int(percent)
    prog_bar_color = progress_bar_color(int(percent))
    progress_bar["style"] = prog_bar_color
    percentage_label.config(text=percent_text)
    charging_label.config(text=plugged, fg=plugged_color)

    # Play Alert if Necessary
    play_alert(plugged, prog_bar_color)

    root.after(5000, main_loop)  # Loop every 5 seeconds

# Start the main event loop
root.after(5000, main_loop)  # Loop every 5 seeconds
root.mainloop()