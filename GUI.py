#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 19:51:11 2024

@author: antun
"""

import tkinter as tk

def draw_point(canvas, x, y, color='black', radius=3, fill="black"):
    return canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=fill, outline=color)

def draw_line(canvas, x1, y1, x2, y2, color='black'):
    return canvas.create_line(x1, y1, x2, y2, fill=color)

def draw_text(canvas, x, y, text):
    return canvas.create_text(x, y, text=text)

def on_canvas_click(event):
    draw_point(canvas, event.x, event.y)
    print(f"Mouse clicked at ({event.x}, {event.y})")
          
          


root = tk.Tk()
root.title('Electrical Schematic')


# Get the width and height of the screen
width = 1700
height = 1000

# Set the window to full screen
#root.attributes('-fullscreen', True)

# Create a canvas that matches the screen size
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()


canvas.bind("<Button-1>", on_canvas_click)


#sabirnica S1
s1_height = 36
draw_line(canvas, 82, s1_height, 1005, s1_height)
draw_text(canvas, 46, s1_height, "S1")

#sabirnica S2
s2_height = 70
draw_line(canvas, 82, s2_height, 1005, s2_height)
draw_text(canvas, 46, s2_height, "S2")


#dalekovodno polje s 2 sabirnice = bez uređaja
draw_point(canvas, 491, s2_height)
draw_line(canvas, 491, s2_height, 491, 127)
draw_line(canvas, 491, 127, 546, 127)
draw_line(canvas, 546, 127, 546, s1_height)
draw_point(canvas, 546, s1_height)
draw_line(canvas, 519, 127, 519, 249)


#spojno polje = bez uređaja
draw_point(canvas, 792, s2_height)
draw_line(canvas, 792, s2_height, 792, 150)
draw_line(canvas, 792, 150, 854, 150)
draw_line(canvas, 854, 150, 854, s1_height)
draw_point(canvas, 854, s1_height)
draw_point(canvas, 823, 150, radius=12, fill="")


#sabirnica na strani gdje ima samo jedna sabrinica
s_height=558
draw_line(canvas, 82, s_height, 1005, s_height)


#dalekovodno polje s jednom sabirnicom
draw_line(canvas, 519, s_height, 519, 399)
draw_point(canvas, 519, s_height)


#dalekovod
draw_line(canvas, 519, 399, 519, 249)


root.mainloop()
