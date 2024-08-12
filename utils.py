# HANDLE PLAYING A RECORDED AUTOAMTION FILE
import time
from tkinter import filedialog, messagebox, simpledialog
from pynput import mouse
from pynput.mouse import Button, Controller
import settings
settings.init()

def play():
    file_path = filedialog.askopenfilename(
        title='Select a file',
        filetypes=[('Text files', '*.txt')])

    settings.playing = True
    
    if(file_path):

        try:
            mouse = Controller()

            settings.play_clicks = []
            with open(f'{file_path}', 'r') as file:
                for line in file:
                    parts = line.split()
                    if(len(parts) != 3):
                        raise ValueError(f"Invalid line format: {line.strip()}")
                    
                    x, y, t = map(float, line.split())
                    settings.play_clicks.append((x, y, t))

            if (not settings.play_clicks):
                raise ValueError('No valid data found in the file.')
            
            settings.start_time = settings.play_clicks[0][2]

            clicks_len = len(settings.play_clicks)
            
            while(settings.click_index < clicks_len and not settings.exited):                
                while(not settings.playing):
                    time.sleep(1)

                settings.play_x, settings.play_y, settings.click_time = settings.play_clicks[settings.click_index]

                time.sleep(settings.click_time - settings.start_time)
                mouse.position = (settings.play_x,settings.play_y)
                mouse.click(Button.left, 1)
                settings.start_time = settings.click_time

                settings.click_index+= 1

            settings.playing = False
            settings.click_index = 0
            settings.exited = False

        except ValueError as ve:
            messagebox.showerror('File Error', ve)
        except Exception as e:
            messagebox.showerror('File Error', e)
        
# HANDLE RECORDING AND SAVING AN AUTOMATION FILE
def record():
    messagebox.showinfo('Usage', 'Right click to stop recording!')
    
    file_name = simpledialog.askstring('New File', 'Give the new file a name: \t\t\t\t')

    if(file_name):
        clicks = []

        def handleClick(x,y, button, pressed):
            if button == mouse.Button.right:
                return False
            if pressed:
                clicks.append((x,y, time.time()))
            
        with mouse.Listener(on_click=handleClick) as listener:
            listener.join()

        with open(f'{file_name}.txt', 'w') as file:
            for click in clicks:
                file.write(f"{click[0]} {click[1]} {click[2]}\n")

        messagebox.showinfo('Recording Info', 'Recording finished and saved succesfully!')



def handleKeybClick(e):
    if(e.name == 'ctrl' or e.name == 'right ctrl'):
        settings.playing = not settings.playing
    elif (e.name == 'shift' or e.name == 'right shift'):
        if(settings.click_index > 1):
            settings.click_index -= 1
            settings.start_time = settings.play_clicks[settings.click_index - 1][2]
            settings.play_x = settings.play_clicks[settings.click_index][0]
            settings.play_y = settings.play_clicks[settings.click_index][1]
            settings.click_time = settings.play_clicks[settings.click_index][2]
            
    elif (e.name == 'esc'):
        settings.exited = True
        settings.playing = False
        settings.click_index = 0
        settings.play_clicks = []
        settings.start_time = 0
        settings.click_time = 0
        settings.play_x = 100
        settings.play_y = 100