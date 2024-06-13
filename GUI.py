import tkinter as tk
from scenariji import *

# Create the main window
root = tk.Tk()
root.title("Scenariji Kontrole")

# Function to execute scenario functions
def execute_scenario(scenario_func):
    scenario_func()

# Create and place buttons for each scenario
button1 = tk.Button(root, text="Scenarij 1", command=lambda: execute_scenario(scenarij1))
button1.pack(pady=5)

button2 = tk.Button(root, text="Scenarij 2", command=lambda: execute_scenario(scenarij2))
button2.pack(pady=5)

button3 = tk.Button(root, text="Scenarij 3", command=lambda: execute_scenario(scenarij3))
button3.pack(pady=5)

button4 = tk.Button(root, text="Scenarij 4", command=lambda: execute_scenario(scenarij4))
button4.pack(pady=5)

button5 = tk.Button(root, text="Scenarij 5", command=lambda: execute_scenario(scenarij5))
button5.pack(pady=5)

button6 = tk.Button(root, text="Scenarij 6", command=lambda: execute_scenario(scenarij6))
button6.pack(pady=5)

# Start the Tkinter event loop
root.mainloop()