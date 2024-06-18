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
draw_text(canvas, 1036, 53, "TS D1")


#dalekovodno polje s 2 sabirnice = bez uređaja__________
draw_point(canvas, 491, s2_height)
draw_line(canvas, 491, s2_height, 491, 127)
draw_line(canvas, 491, 127, 546, 127)
draw_line(canvas, 546, 127, 546, s1_height)
draw_point(canvas, 546, s1_height)
draw_line(canvas, 519, 127, 519, 249)


#sabirnički rastavljači na tom dalekovodnom polju
#S2
draw_line(canvas, 476, 93, 506, 108)
#s2
draw_line(canvas, 531, 93, 561, 108)

#prekidač na tom polju
draw_line(canvas, 504, 147, 534, 162)
draw_line(canvas, 504, 162, 534, 147)


#rastavljač uzemljenja
draw_line(canvas, 504, 192, 534, 207)

#spojno polje = bez uređaja__________________
draw_point(canvas, 792, s2_height)
draw_line(canvas, 792, s2_height, 792, 170)
draw_line(canvas, 792, 170, 854, 170)
draw_line(canvas, 854, 170, 854, s1_height)
draw_point(canvas, 854, s1_height)
draw_point(canvas, 823, 170, radius=12, fill="")


#sabirnički rastavljač S2
draw_line(canvas, 777, 93, 807, 108)

#sabirnički rastavljač S1
draw_line(canvas, 839, 93, 869, 108)

#prekidač na spojnom polju
draw_line(canvas, 777, 129, 807, 144)
draw_line(canvas, 777, 144, 807, 129)

#sabirnica na strani gdje ima samo jedna sabrinica______________
s_height=598
draw_line(canvas, 82, s_height, 1005, s_height)
draw_text(canvas, 1036, s_height, "TS D2")

#dalekovodno polje s jednom sabirnicom
draw_line(canvas, 519, s_height, 519, 399)
draw_point(canvas, 519, s_height)

#rastavljač sabirnički
draw_line(canvas, 504, 556, 534, 571)

#prekidač
draw_line(canvas, 504, 514, 534, 529)
draw_line(canvas, 504, 529, 534, 514)

#rastavljač uzemljenja
draw_line(canvas, 504, 460, 534, 475)


#dalekovod ____________________________________________________
draw_line(canvas, 519, 399, 519, 249)
draw_point(canvas, 519, 399)
draw_point(canvas, 519, 249)



root.mainloop()
