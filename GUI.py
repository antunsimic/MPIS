import tkinter as tk
from classes import *
import sys


class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        try:
            if self.text_widget.winfo_exists():  # Check if the widget still exists
                self.text_widget.insert(tk.END, string)
                self.text_widget.see(tk.END)  # Scrolls to the end
        except tk.TclError as e:
            print("Failed to write to the text widget:", e)

    def flush(self):
        pass

dalekovod = Dalekovod()

field_device_mapping = {
'Dalekovodno Polje TS D1': dalekovod.D_polje2,
'Dalekovodno Polje TS D2': dalekovod.D_polje1,
'Spojno Polje TS D1': dalekovod.D_polje2.S_polje
}

device_mapping = {
'prekidač': 'prekidac',
'rastavljač sabirnički': 's_rastavljac',
'rastavljač izlazni': 'i_rastavljac',
'distantna zaštita': 'dist_zastita',
'APU': 'apu',
'nadstrujna zaštita': 'nads_zastita',
'mjerni_pretvornik': 'mjera',
'rastavljač sabirnički S1': 's_rastavljacS1',
'rastavljač sabirnički S2': 's_rastavljacS2',

}



# Function to display signals based on selected options
def display_signals():
    field = field_var.get()
    device = device_var.get()
    signal_type = signal_type_var.get()

    if field == 'Sva polja':
        fields_to_process = field_device_mapping.values()
    else:
        fields_to_process = [field_device_mapping[field]]

    for field_instance in fields_to_process:
        if device == 'Svi uređaji':
            # Process all devices, skipping ones not present in the field instance
            devices_to_process = []
            for dev_key, dev_var in device_mapping.items():
                try:
                    dev_instance = getattr(field_instance, dev_var)
                    devices_to_process.append(dev_instance)
                except AttributeError:
                    # Skip this device if it's not present in the current field instance
                    continue
        else:
            try:
                device_instance = getattr(field_instance, device_mapping[device])
                devices_to_process = [device_instance]
            except AttributeError:
                # Skip this device if it's not present and continue with the next iteration
                continue

        for device_instance in devices_to_process:
            #print(f"Displaying {signal_type} signals for {device_instance.__class__.__name__} in {field}:")
            if signal_type == "Svi":
                field_instance.izlistaj_uredaj(device_instance, "sve")
            else:
                field_instance.izlistaj_uredaj(device_instance, "trenutne")

# Update devices menu based on selected field
def update_devices_menu():
    field = field_var.get()
    device_menu.delete(0, 'end')  # Clear existing options
    if field == 'Svi':
        devices = ['Svi uređaji'] + dalekovod.get_all_devices()
    else:
        devices = ['Svi uređaji'] + dalekovod.get_devices_in_field(field)
    for device in devices:
        device_menu.add_command(label=device, command=tk._setit(device_var, device))



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
    new_color_s2 = 'black' if dalekovod.D_polje2.s_rastavljacS2.odredi_polozaj() == Stanje.ISKLJUČEN else 'green'
    new_color_s1 = 'black' if dalekovod.D_polje2.s_rastavljacS1.odredi_polozaj() == Stanje.ISKLJUČEN else 'green'
    new_color_p1 = 'black' if dalekovod.D_polje2.prekidac.odredi_polozaj() == Stanje.ISKLJUČEN else 'green'
    new_color_u1 = 'black' if dalekovod.D_polje2.u_rastavljac.odredi_polozaj() == Stanje.ISKLJUČEN else 'green'
    new_color_s4 = 'black' if dalekovod.D_polje2.S_polje.s_rastavljacS1.odredi_polozaj() == Stanje.ISKLJUČEN else 'green'
    new_color_s3 = 'black' if dalekovod.D_polje2.S_polje.s_rastavljacS2.odredi_polozaj() == Stanje.ISKLJUČEN else 'green'
    new_color_p2 = 'black' if dalekovod.D_polje2.S_polje.prekidac.odredi_polozaj() == Stanje.ISKLJUČEN else 'green'
    new_color_p3 = 'black' if dalekovod.D_polje1.prekidac.odredi_polozaj() == Stanje.ISKLJUČEN else 'green'
    new_color_s5 = 'black' if dalekovod.D_polje1.s_rastavljac.odredi_polozaj() == Stanje.ISKLJUČEN else 'green'
    new_color_u2 = 'black' if dalekovod.D_polje1.u_rastavljac.odredi_polozaj() == Stanje.ISKLJUČEN else 'green'
    new_color_d = 'black' if dalekovod.stanje == Stanje.ISKLJUČEN else 'green'
    # Prekidac 1
    canvas.itemconfig(p11, fill=new_color_p1)
    canvas.itemconfig(p12, fill=new_color_p1)
    canvas.itemconfig(p1_mainline, fill=new_color_p1)
    prekidac1.config(bg=new_color_p1)
    
    # S2 rastavljac
    s_rastavljacS2.config(bg=new_color_s2)
    canvas.itemconfig(sr2, fill=new_color_s2) 
    canvas.itemconfig(line_S2, fill=new_color_s2)
    canvas.itemconfig(p_s2, fill=new_color_s2)
    canvas.itemconfig(s2_horisontal, fill=new_color_s2)
    canvas.itemconfig(s2_vertical, fill=new_color_s2)
    
    # S1 rastavljac
    s_rastavljacS1.config(bg=new_color_s1)
    canvas.itemconfig(sr1, fill=new_color_s1)
    canvas.itemconfig(p_s1, fill=new_color_s1)
    canvas.itemconfig(line_S1, fill=new_color_s1)
    canvas.itemconfig(s1_horisontal, fill=new_color_s1)
    canvas.itemconfig(s1_vertical, fill=new_color_s1)
    
    # Uzemljenje rastavljac 1
    r_uzemljenja1.config(bg=new_color_u1)   
    canvas.itemconfig(ru1, fill=new_color_u1)
    
    # S3 rastavljac
    s_rastavljacS3.config(bg=new_color_s3)
    canvas.itemconfig(sr3, fill=new_color_s3)
    canvas.itemconfig(spojno_right, fill=new_color_s3)
    
    # S4 rastavljac
    s_rastavljacS4.config(bg=new_color_s4)
    canvas.itemconfig(sr4, fill=new_color_s4)
    canvas.itemconfig(spojno_left, fill=new_color_s4)
    
    # Prekidac 2
    prekidac2.config(bg=new_color_p2)
    canvas.itemconfig(p21, fill=new_color_p2)
    canvas.itemconfig(p22, fill=new_color_p2)
    canvas.itemconfig(spojno_horizontal, fill=new_color_p2)
    canvas.itemconfig(krug, fill=new_color_p2)
    
    # Prekidac 3
    prekidac3.config(bg=new_color_p3)
    canvas.itemconfig(p31, fill=new_color_p3)
    canvas.itemconfig(p32, fill=new_color_p3)
    canvas.itemconfig(dalekovodno1S, fill=new_color_p3)
    
    # S5 rastavljac
    s_rastavljacS5.config(bg=new_color_s5)
    canvas.itemconfig(sr5, fill=new_color_s5)
    canvas.itemconfig(line_S3, fill=new_color_s5)
    canvas.itemconfig(dp, fill=new_color_s5)
    
    # Uzemljenje rastavljac 2
    r_uzemljenja2.config(bg=new_color_u2)
    canvas.itemconfig(ru2, fill=new_color_u2)
    
    #dalekovod
    canvas.itemconfig(dalekovod_line, fill=new_color_d)
    canvas.itemconfig(dd1, fill=new_color_d)
    canvas.itemconfig(dd2, fill=new_color_d)
    
    root.after(100, check_color)

        

root = tk.Tk()
root.title('Jednopolna shema')


# Get the width and height of the screen
width = 1700
height = 1000

# Create a canvas that matches the screen size
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()
 # Create the Text widget for output
output_console = tk.Text(root, height=30, width=100)
output_console.place(x=1116, y=451)

# # Redirect stdout to the text widget
sys.stdout = StdoutRedirector(output_console) #UNCOMMENT

# Menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Signal type menu
signal_type_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Signali", menu=signal_type_menu)
signal_type_var = tk.StringVar()
signal_type_var.set("Trenutni")  # default value
signal_type_menu.add_radiobutton(label="Svi", variable=signal_type_var, value="Svi")
signal_type_menu.add_radiobutton(label="Trenutni", variable=signal_type_var, value="Trenutni")

# Field menu
field_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Polje", menu=field_menu)
field_var = tk.StringVar()
field_var.set("Sva polja")  # default value
fields = ['Sva polja', 'Dalekovodno Polje TS D1', 'Dalekovodno Polje TS D2', 'Spojno Polje TS D1']
for field in fields:
    field_menu.add_radiobutton(label=field, variable=field_var, value=field, command=update_devices_menu)

# Device menu
device_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Uređaj", menu=device_menu)
device_var = tk.StringVar()
device_var.set("Svi uređaji")  # default value
device_menu.add_command(label="Svi uređaji", command=tk._setit(device_var, "Svi uređaji"))

# Button to display selected signals
btn_display = tk.Button(root, text="Izlistaj signale", command=display_signals)
btn_display.place(x=170, y=0)


canvas.bind("<Button-1>", on_canvas_click)

#sabirnica S1
s1_height = 126
line_S1=canvas.create_line(82, s1_height, 1005, s1_height, fill='black')
draw_text(canvas, 46, s1_height, "S1")

#sabirnica S2
s2_height = 160
line_S2=canvas.create_line(82, s2_height, 1005, s2_height, fill='black')
draw_text(canvas, 46, s2_height, "S2")

draw_text(canvas, 1036, 143, "TS D1")

#dalekovodno polje s 2 sabirnice = bez uređaja__________
p_s2=draw_point(canvas, 491, s2_height)
s2_vertical=draw_line(canvas, 491, s2_height, 491, 217)
s2_horisontal=draw_line(canvas, 491, 217, 519, 217)
s1_horisontal=draw_line(canvas, 519, 217, 546, 217)
s1_vertical=draw_line(canvas, 546, 217, 546, s1_height)
p_s1=draw_point(canvas, 546, s1_height)
p1_mainline=draw_line(canvas, 519, 217, 519, 339)


#sabirnički rastavljači na tom dalekovodnom polju
#S2
sr2=draw_line(canvas, 476, 183, 506, 198)
s_rastavljacS2 = tk.Button(root, text="", command=dalekovod.D_polje2.interakcija_s2_rastavljac, bg="red" )
s_rastavljacS2.place(x=445, y=185, width=17, height=17)

#S1
sr1=draw_line(canvas, 531, 183, 561, 198)
s_rastavljacS1 = tk.Button(root, text="", command=dalekovod.D_polje2.interakcija_s1_rastavljac, bg="red" )
s_rastavljacS1.place(x=570, y=185, width=17, height=17)

#prekidač na tom polju
p11=draw_line(canvas, 504, 237, 534, 252)
p12=draw_line(canvas, 504, 252, 534, 237)
prekidac1 = tk.Button(root, text="", command=dalekovod.D_polje2.interakcija_prekidac, bg="red" )
prekidac1.place(x=470, y=235, width=17, height=17)

#rastavljač uzemljenja
ru1=draw_line(canvas, 504, 282, 534, 297)
r_uzemljenja1 = tk.Button(root, text="", command=dalekovod.D_polje2.interakcija_u_rastavljac, bg="red" )
r_uzemljenja1.place(x=470, y=280, width=17, height=17)

#spojno polje = bez uređaja__________________
ps2=draw_point(canvas, 792, s2_height)
ps1=draw_point(canvas, 854, s1_height)
spojno_right=draw_line(canvas, 792, s2_height, 792, 260)
spojno_horizontal=draw_line(canvas, 792, 260, 854, 260)
spojno_left=draw_line(canvas, 854, 260, 854, s1_height)
krug=draw_point(canvas, 823, 260, radius=12, fill="")

#sabirnički rastavljač S2
sr3=draw_line(canvas, 777, 183, 807, 198)
s_rastavljacS3=tk.Button(root, text="", command=dalekovod.D_polje2.S_polje.interakcija_s2_rastavljac, bg="red" )
s_rastavljacS3.place(x=750, y=180, width=17, height=17)

#sabirnički rastavljač S1
sr4=draw_line(canvas, 839, 183, 869, 198)
s_rastavljacS4=tk.Button(root, text="", command=dalekovod.D_polje2.S_polje.interakcija_s1_rastavljac, bg="red" )
s_rastavljacS4.place(x=880, y=180, width=17, height=17)

#prekidač na spojnom polju
p21=draw_line(canvas, 777, 219, 807, 234)
p22=draw_line(canvas, 777, 234, 807, 219)
prekidac2 = tk.Button(root, text="", command=dalekovod.D_polje2.S_polje.interakcija_prekidac, bg="red" )
prekidac2.place(x=750, y=217, width=17, height=17)

#sabirnica na strani gdje ima samo jedna sabrinica______________
s_height=688
line_S3=draw_line(canvas, 82, s_height, 1005, s_height)
draw_text(canvas, 1036, s_height, "TS D2")

#dalekovodno polje s jednom sabirnicom
dalekovodno1S=draw_line(canvas, 519, s_height, 519, 489)
dp=draw_point(canvas, 519, s_height)

#rastavljač sabirnički
sr5=draw_line(canvas, 504, 646, 534, 661)
s_rastavljacS5=tk.Button(root, text="", command=dalekovod.D_polje1.interakcija_s_rastavljac, bg="red" )
s_rastavljacS5.place(x=470, y=644, width=17, height=17)

#prekidač
p31=draw_line(canvas, 504, 604, 534, 619)
p32=draw_line(canvas, 504, 619, 534, 604)
prekidac3 = tk.Button(root, text="", command=dalekovod.D_polje1.interakcija_prekidac, bg="red" )
prekidac3.place(x=470, y=602, width=17, height=17)

#rastavljač uzemljenja
ru2=draw_line(canvas, 504, 550, 534, 565)
r_uzemljenja2=tk.Button(root, text="", command=dalekovod.D_polje1.interakcija_u_rastavljac, bg="red" )
r_uzemljenja2.place(x=470, y=548, width=17, height=17)

#dalekovod ____________________________________________________
dalekovod_line=draw_line(canvas, 519, 489, 519, 339)
dd1=draw_point(canvas, 519, 489)
dd2=draw_point(canvas, 519, 339)

#SCENARIJI
ukljuciS1_dalekovod = tk.Button(root, text="Uključi dalekovod na S1", command=dalekovod.ukljuci1)
ukljuciS1_dalekovod.place(x=1200, y=100, width=150, height=50)

ukljuciS2_dalekovod = tk.Button(root, text="Uključi dalekovod na S2", command=dalekovod.ukljuci2)
ukljuciS2_dalekovod.place(x=1200, y=160, width=150, height=50)

iskljuci_dalekovod = tk.Button(root, text="Isključi dalekovod", command=dalekovod.iskljuci)
iskljuci_dalekovod.place(x=1200, y=220, width=150, height=50)

prespoji_na_S1 = tk.Button(root, text="Prespoji na S1", command=dalekovod.D_polje2.prespoji1)
prespoji_na_S1.place(x=1200, y=280, width=150, height=50)

prespoji_na_S2 = tk.Button(root, text="Prespoji na S2", command=dalekovod.D_polje2.prespoji2)
prespoji_na_S2.place(x=1200, y=340, width=150, height=50)






check_color()


root.mainloop()

