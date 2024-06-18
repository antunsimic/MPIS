import tkinter as tk
from classes import *

dalekovod = Dalekovod()
#dalekovod.D_polje2.prespoji(2) # Samo za testiranje s razlicitim sabirnicama

def draw_point(canvas, x, y, color='black', radius=3, fill="black"):
    return canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=fill, outline=color)

def draw_line(canvas, x1, y1, x2, y2, color='black'):
    return canvas.create_line(x1, y1, x2, y2, fill=color)

def draw_text(canvas, x, y, text):
    return canvas.create_text(x, y, text=text)

def on_canvas_click(event):
    #draw_point(canvas, event.x, event.y)
    print(f"Mouse clicked at ({event.x}, {event.y})")

def button_click():
    print("Button clicked")
    
# Tu provjeravamo sva stanja zbog bojanja prekidača
def check_color():
    new_color_p1 = 'black' if dalekovod.D_polje2.prekidac.odredi_polozaj() == Stanje.ISKLJUČEN else 'green'
    # Prekidac
    canvas.itemconfig(p11, fill=new_color_p1)
    canvas.itemconfig(p12, fill=new_color_p1)
    canvas.itemconfig(p1_mainline, fill=new_color_p1)
    prekidac1.config(bg=new_color_p1)
    
    ## Za linije oko prekidaca i sabirnica, cabirnickih rastavljaca
    if dalekovod.D_polje2.prekidac.odredi_polozaj() == Stanje.UKLJUČEN:
        if dalekovod.D_polje2.s_rastavljacS1.odredi_polozaj() == Stanje.UKLJUČEN:
            color_s1="green"
        else:
            color_s1="black"
        if dalekovod.D_polje2.s_rastavljacS2.odredi_polozaj() == Stanje.UKLJUČEN:
            color_s2="green"
        else:
            color_s2="black"
    else:
        color_s1="black"
        color_s2="black"
    canvas.itemconfig(line_S1, fill=color_s1)
    canvas.itemconfig(line_S2, fill=color_s2)
    canvas.itemconfig(s2_horisontal, fill=color_s2)
    canvas.itemconfig(s2_vertical, fill=color_s2)
    canvas.itemconfig(s1_horisontal, fill=color_s1)
    canvas.itemconfig(s1_vertical, fill=color_s1)
    canvas.itemconfig(p_s1, fill=color_s1)
    canvas.itemconfig(p_s2, fill=color_s2)
    canvas.itemconfig(sr1, fill=color_s1)
    canvas.itemconfig(sr2, fill=color_s2)   # Za s_rastavljače ali neznam koje promjene oni još vuču
                                            # da bi ih trbali prikazati na GUI-u
    ##
    
    root.after(100, check_color)
          

root = tk.Tk()
root.title('Electrical Schematic')


# Get the width and height of the screen
width = 1700
height = 1000

# Create a canvas that matches the screen size
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()

canvas.bind("<Button-1>", on_canvas_click)

#sabirnica S1
s1_height = 36
line_S1=canvas.create_line(82, s1_height, 1005, s1_height, fill='black')
draw_text(canvas, 46, s1_height, "S1")

#sabirnica S2
s2_height = 70
line_S2=canvas.create_line(82, s2_height, 1005, s2_height, fill='black')
draw_text(canvas, 46, s2_height, "S2")
draw_text(canvas, 1036, 53, "TS D1")


#dalekovodno polje s 2 sabirnice = bez uređaja__________
p_s2=draw_point(canvas, 491, s2_height)
s2_vertical=draw_line(canvas, 491, s2_height, 491, 127)
s2_horisontal=draw_line(canvas, 491, 127, 519, 127)
s1_horisontal=draw_line(canvas, 519, 127, 546, 127)
s1_vertical=draw_line(canvas, 546, 127, 546, s1_height)
p_s1=draw_point(canvas, 546, s1_height)
p1_mainline=draw_line(canvas, 519, 127, 519, 249)


#sabirnički rastavljači na tom dalekovodnom polju
#S2
sr2=draw_line(canvas, 476, 93, 506, 108)
#s2
sr1=draw_line(canvas, 531, 93, 561, 108)

#prekidač na tom polju
p11=draw_line(canvas, 504, 147, 534, 162)
p12=draw_line(canvas, 504, 162, 534, 147)
prekidac1 = tk.Button(root, text="", command=dalekovod.D_polje2.interakcija_prekidac, bg="red" )
prekidac1.place(x=470, y=145, width=17, height=17)


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

check_color()

root.mainloop()
