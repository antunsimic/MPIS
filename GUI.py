import tkinter as tk
from scenariji import *
from classes import *

# Create the main window
root = tk.Tk()
root.title("Scenariji Kontrole")
root.geometry("1800x1000")
# root.attributes('-fullscreen', True)

# Function to execute scenario functions
def execute_scenario(scenario_func):
    scenario_func()

# Create and place buttons for each scenario
button1 = tk.Button(root, text="Scenarij 1", command=lambda: execute_scenario(scenarij1))
button1.pack(side='bottom', anchor='w', pady=5)

button2 = tk.Button(root, text="Scenarij 2", command=lambda: execute_scenario(scenarij2))
button2.pack(side='bottom', anchor='w', pady=5)

button3 = tk.Button(root, text="Scenarij 3", command=lambda: execute_scenario(scenarij3))
button3.pack(side='bottom', anchor='w', pady=5)

button4 = tk.Button(root, text="Scenarij 4", command=lambda: execute_scenario(scenarij4))
button4.pack(side='bottom', anchor='w', pady=5)

button5 = tk.Button(root, text="Scenarij 5", command=lambda: execute_scenario(scenarij5))
button5.pack(side='bottom', anchor='w', pady=5)

button6 = tk.Button(root, text="Scenarij 6", command=lambda: execute_scenario(scenarij6))
button6.pack(side='bottom', anchor='w', pady=5)

def initialize_lines():
    global dp1_line_main_id, dp1_line_prekidac_id, dp1_line_i_rastavljac_id, dp1_line_u_rastavljac_id
    dp1_line_main_id = canvas.create_line(300, 100, 300, 700, fill='black', width=3)
    dp1_line_prekidac_id = canvas.create_line(300, 170, 400, 170, fill='black', width=3)
    dp1_line_i_rastavljac_id = canvas.create_line(300, 220, 400, 220, fill='black', width=3)
    dp1_line_u_rastavljac_id = canvas.create_line(300, 270, 400, 270, fill='black', width=3)

def prekidac():
    dalekovod.D_polje1.interakcija_prekidac()
    color = "green" if dalekovod.D_polje1.prekidac.odredi_polozaj else "black"
    # Update line colors using their IDs
    canvas.itemconfig(dp1_line_main_id, fill=color)
    canvas.itemconfig(dp1_line_prekidac_id, fill=color)
    canvas.itemconfig(dp1_line_i_rastavljac_id, fill=color)
    canvas.itemconfig(dp1_line_u_rastavljac_id, fill=color)
   

button_P_polje1 = tk.Button(root, text="P_polje1", command=prekidac)
button_P_polje1.place(x = 400, y = 150)

button_RI_polje1 = tk.Button(root, text="RI_polje1", command=dalekovod.D_polje1.interakcija_i_rastavljac)
button_RI_polje1.place(x = 400, y = 200)

button_RU_polje1 = tk.Button(root, text="RU_polje1", command=dalekovod.D_polje1.interakcija_u_rastavljac)
button_RU_polje1.place(x = 400, y = 250)


# Create a Canvas widget
canvas = tk.Canvas(root, width=1800, height=1800)
canvas.pack()
initialize_lines()
button1.lift()
button2.lift()
button3.lift()
button4.lift()
button5.lift()
button6.lift()
button_P_polje1.lift()
button_RI_polje1.lift()
button_RU_polje1.lift()

dp1_line_main = Line(300, 100, 300, 700, dalekovod.D_polje1, 3, "green")
dp1_line_main.draw(canvas)

dp1_line_prekidac = Line(300, 170, 400, 170, dalekovod.D_polje1, 3, "green")
dp1_line_prekidac.draw(canvas)

dp1_line_i_rastavljac = Line(300, 220, 400, 220, dalekovod.D_polje1, 3, "green")
dp1_line_i_rastavljac.draw(canvas)

dp1_line_u_rastavljac = Line(300, 270, 400, 270, dalekovod.D_polje1, 3, "green")
dp1_line_u_rastavljac.draw(canvas)

# Start the Tkinter event loop
root.mainloop()