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

button_P_polje1 = tk.Button(root, text="P_polje1", command=dalekovod.D_polje1.interakcija_prekidac)
button_P_polje1.place(x = 400, y = 150)

button_RI_polje1 = tk.Button(root, text="RI_polje1", command=dalekovod.D_polje1.interakcija_i_rastavljac)
button_RI_polje1.place(x = 400, y = 250)

button_RU_polje1 = tk.Button(root, text="RU_polje1", command=dalekovod.D_polje1.interakcija_u_rastavljac)
button_RU_polje1.place(x = 400, y = 350)

button_RS_polje1 = tk.Button(root, text="RS_polje1", command=dalekovod.D_polje1.interakcija_s_rastavljac)
button_RS_polje1.place(x = 400, y = 450)

button_P_polje2 = tk.Button(root, text="P_polje2", command=dalekovod.D_polje2.interakcija_prekidac)
button_P_polje2.place(x = 950, y = 155)

button_RI_polje2 = tk.Button(root, text="RI_polje2", command=dalekovod.D_polje2.interakcija_i_rastavljac)
button_RI_polje2.place(x = 950, y = 255)

button_RU_polje2 = tk.Button(root, text="RU_polje2", command=dalekovod.D_polje2.interakcija_u_rastavljac)
button_RU_polje2.place(x = 950, y = 355)

button_RS1_polje2 = tk.Button(root, text="RS1_polje2", command=dalekovod.D_polje2.interakcija_s1_rastavljac)
button_RS1_polje2.place(x = 1150, y = 690)

button_RS2_polje2 = tk.Button(root, text="RS2_polje2", command=dalekovod.D_polje2.interakcija_s2_rastavljac)
button_RS2_polje2.place(x = 1350, y = 690)

# Create a Canvas widget
canvas = tk.Canvas(root, width=1800, height=1800)
canvas.pack()
button1.lift()
button2.lift()
button3.lift()
button4.lift()
button5.lift()
button6.lift()
button_P_polje1.lift()
button_RI_polje1.lift()
button_RU_polje1.lift()
button_RS_polje1.lift()
button_P_polje2.lift()
button_RI_polje2.lift()
button_RU_polje2.lift()
button_RS1_polje2.lift()
button_RS2_polje2.lift()

dp1_line_main = Line(300, 100, 300, 700, dalekovod.D_polje1, 3)
dp1_line_main.draw(canvas)
dp1_line_prekidac = Line(300, 170, 400, 170, dalekovod.D_polje1, 3)
dp1_line_prekidac.draw(canvas)
dp1_line_i_rastavljac = Line(300, 270, 400, 270, dalekovod.D_polje1, 3)
dp1_line_i_rastavljac.draw(canvas)
dp1_line_u_rastavljac = Line(300, 370, 400, 370, dalekovod.D_polje1, 3)
dp1_line_u_rastavljac.draw(canvas)
dp1_line_s_rastavljac = Line(300, 470, 400, 470, dalekovod.D_polje1, 3)
dp1_line_s_rastavljac.draw(canvas)

dp2_line_s1 = Line(1200, 100, 1200, 700, dalekovod.D_polje2, 3)
dp2_line_s1.draw(canvas)
dp2_line_s2 = Line(1400, 100, 1400, 700, dalekovod.D_polje2, 3)
dp2_line_s2.draw(canvas)
dp2_prekidac_s1 = Line(1000, 170, 1200, 170, dalekovod.D_polje2, 3)
dp2_prekidac_s1.draw(canvas)
dp2_prekidac_s2 = Line(1000, 180, 1400, 180, dalekovod.D_polje2, 3)
dp2_prekidac_s2.draw(canvas)
dp2_i_rastavljac_s1 = Line(1000, 270, 1200, 270, dalekovod.D_polje2, 3)
dp2_i_rastavljac_s1.draw(canvas)
dp2_i_rastavljac_s2 = Line(1000, 280, 1400, 280, dalekovod.D_polje2, 3)
dp2_i_rastavljac_s2.draw(canvas)
dp2_u_rastavljac_s1 = Line(1000, 370, 1200, 370, dalekovod.D_polje2, 3)
dp2_u_rastavljac_s1.draw(canvas)
dp2_u_rastavljac_s2 = Line(1000, 380, 1400, 380, dalekovod.D_polje2, 3)
dp2_u_rastavljac_s2.draw(canvas)


# Start the Tkinter event loop
root.mainloop()