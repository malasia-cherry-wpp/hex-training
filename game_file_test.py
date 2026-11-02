import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output

# 1. Load the Game Data
# We use the slither-ready dataset we built earlier
df = pd.read_csv("../data/firefly_data_game_dataset_v2.csv")
# Create a simple player profile starting as a Class A firefly
player_stats = {'mass': 10.0, 'speed': 5.0}

# 2. Build the Widgets (The GUI)
# Instead of typing a name like in the Pokemon example, we use a dropdown
enemy_dropdown = widgets.Dropdown(
    options=['Class A (Mass 10)', 'Class B (Mass 25)', 'Class C (Mass 50)', 'Class D (Boss - Mass 100)'],
    description='Target:',
    disabled=False,
)

hunt_button = widgets.Button(
    description='Hunt Target!',
    button_style='success',
    tooltip='Attempt to eat the target firefly'
)

output_screen = widgets.Output()

# 3. The Game Logic Function
def on_hunt_click(b):
    with output_screen:
        clear_output()
        
        # Determine target mass from the dropdown selection
        target_selection = enemy_dropdown.value
        if "Class A" in target_selection: target_mass = 10
        elif "Class B" in target_selection: target_mass = 25
        elif "Class C" in target_selection: target_mass = 50
        else: target_mass = 100
            
        # Find a matching enemy in your dataset
        match = df[df['starting_mass'] == target_mass]
        
        if match.empty:
            print("Error: Target not found in the dataset.")
            return
            
        enemy = match.iloc[0]
        
        print(f"--- HUNT INITIATED ---")
        print(f"You (Mass: {player_stats['mass']}, Speed: {player_stats['speed']}) are hunting a {target_selection}.")
        print(f"Enemy Speed is {enemy['movement_speed']}.")
        
        # Slither.io Combat Logic: Speed dictates ability to cut off the enemy
        if player_stats['speed'] >= enemy['movement_speed']:
            print(f"\nSUCCESS! You are fast enough to cut off the enemy's head.")
            # Player grows by consuming the food_value
            player_stats['mass'] += enemy['food_value']
            
            # As player grows, their speed decreases (balancing mechanic)
            if player_stats['mass'] >= 50:
                player_stats['speed'] = 3.0
            elif player_stats['mass'] >= 25:
                player_stats['speed'] = 4.0
                
            print(f"You ate the firefly! Your mass is now {player_stats['mass']}.")
        else:
            print(f"\nFAILURE! The enemy's speed ({enemy['movement_speed']}) is higher than yours.")
            print("They escaped your trap.")

# 4. Connect and Display
hunt_button.on_click(on_hunt_click)
display(widgets.VBox([enemy_dropdown, hunt_button, output_screen]))