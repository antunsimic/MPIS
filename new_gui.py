import tkinter as tk
from classes import *

dalekovod = Dalekovod()
def check_color():
    new_color = 'black' if dalekovod.D_polje1.prekidac.odredi_polozaj() == Stanje.ISKLJUČEN else 'green'
    canvas.itemconfig(line_D1, fill=new_color)
    root.after(100, check_color)

root = tk.Tk()
root.title("Color Change GUI")
root.geometry("1300x800")

# Pack the canvas at the top, allowing it to expand and fill both x and y
canvas = tk.Canvas(root, width=1300, height=750)
canvas.pack(side='top', fill='both', expand=True)

# Initial line color is green
line_D1 = canvas.create_line(50, 50, 150, 50, fill='green', width=3)

# Pack the button at the bottom
button_prekidacD1 = tk.Button(root, text="PrekidacD1", command=dalekovod.D_polje1.interakcija_prekidac)
button_prekidacD1.place(x=150, y=40)
# button_prekidacD1.lift()

check_color()

root.mainloop()
