import tkinter as tk
import utils
from  constants import *
import keyboard

window = tk.Tk()

# WINDOW CONFIG
window.title(APP_NAME)
x = (window.winfo_screenwidth()//2)-(WIDTH//2)
y = (window.winfo_screenheight()//2)-(HEIGHT//2)
window.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
window.iconbitmap(default=APP_LOGO_PATH)
window.resizable(False, False)
window.configure(bg=APP_BG)
# ====================================
pause = tk.BooleanVar(value=True)

# HEADING
heading = tk.Label(text=APP_NAME, 
                   bg="#333", 
                   fg="#fafafa", 
                   padx=10, 
                   pady=5,
                   width=WIDTH,
                   font=("Verdana"))
heading.pack()
# =====================================

# ICONS 
playIco = tk.PhotoImage(file='./icons/play.png').subsample(12,12)
recIco = tk.PhotoImage(file='./icons/record.png').subsample(12,12)

# CONTAINERS
btnContainer = tk.Frame(window, 
                        bg=APP_BG)
infoContainer = tk.Frame(window,
                         bg=APP_BG)


playBtn = tk.Button(btnContainer,
                    text="Play", 
                    padx=10, 
                    pady=5,
                    image=playIco,
                    compound="left",
                    command=utils.play)

recBtn = tk.Button(btnContainer,
                    text="Record",
                    padx=10,
                    pady=5,
                    image=recIco,
                    compound="left",
                    command=utils.record)

tutorialLabel = tk.Label(infoContainer, text='By MetaMorphica Digital <3')
# =====================================

# PACK 
playBtn.pack(side="left", padx=10)
recBtn.pack(side="left", padx=10)
tutorialLabel.pack(padx=10, pady=5)
btnContainer.pack(expand=True)
infoContainer.pack(expand=True)
# =====================================

keyboard.on_press(utils.handleKeybClick)

window.mainloop()