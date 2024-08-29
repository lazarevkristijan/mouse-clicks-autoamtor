# HANDLE PLAYING A RECORDED AUTOAMTION FILE
import time
from tkinter import filedialog, messagebox, simpledialog
from pynput import mouse
from pynput.mouse import Button, Controller
import os
from constants import CONFIG_LAST_OPEN
import threading
from win10toast import ToastNotifier
toaster = ToastNotifier()
import pyautogui
import settings
settings.init()
from constants import TOASTER_SETTINGS, BTN_DEAFULT_COLOR,BTN_HOVER_COLOR
def play(*lastOpenPath):
    lastOpenPath = ''.join(lastOpenPath)
    
    try:
        resetSettings()
        settings.playing = True
        settings.paused = False

        mouse = Controller()            
        settings.play_clicks = []
        
        if(not lastOpenPath):
            file_path = filedialog.askopenfilename(
                title='Select a file',
                filetypes=[('Text files', '*.txt')])

        if(lastOpenPath or file_path):
            with open(f'{lastOpenPath if lastOpenPath else file_path}', 'r') as file:
                for line in file:
                    parts = line.split()
                    if(len(parts) != 4):
                        raise ValueError(f"Invalid line format: {line.strip()}")
                    
                    x, y, t, c = map(float, line.split())
                    settings.play_clicks.append((x, y, t, c))

            if (not settings.play_clicks):
                raise ValueError('No valid data found in the file.')  

            if(not lastOpenPath):
                with open(CONFIG_LAST_OPEN, 'w') as file:
                    file.write(file_path)
            
            settings.start_time = settings.play_clicks[0][2]
            clicks_len = len(settings.play_clicks)

            while(not settings.exited and settings.click_index < clicks_len ):                                 
                settings.play_x, settings.play_y, settings.click_time, settings.play_c = settings.play_clicks[settings.click_index]
                time.sleep(settings.click_time - settings.start_time)

                # CHECK IF PAUSED
                while(settings.paused and settings.playing):
                    time.sleep(1)

                if(settings.exited):
                    break
                mouse.position = (settings.play_x, settings.play_y)
                mouseToClick = Button.left if settings.play_c == 1 else Button.right if settings.play_c == 2 else None
                if(not mouseToClick):
                    raise ValueError('Recording has invalid mouse clicks')
                else:
                    mouse.click(mouseToClick, 1)

                settings.start_time = settings.click_time
                settings.click_index += 1

            resetSettings()
            
            
    except ValueError as ve:
        messagebox.showerror('File Error', ve)
    except Exception as e:
        messagebox.showerror('File Error', e)
              
# HANDLE RECORDING AND SAVING AN AUTOMATION FILE
def record():
    messagebox.showinfo('Usage', 'Scroll up/down to stop recording!')
    
    file_name = simpledialog.askstring('New File', 'Give the new file a name: \t\t\t\t')

    if(file_name):
        clicks = []

        def stopRecording(_x, _y, _dx, dy):
            if (dy < 0 or dy > 0):
                return False
        
        def addClick(x, y, button, pressed):
            if pressed:
                btnClicked = 1 if button == mouse.Button.left else 2 if button == mouse.Button.right else None
                if(not btnClicked):
                    toaster.show_toast(title='Error', 
                               msg='Invalid button pressed, click not saved!', 
                               **TOASTER_SETTINGS)
                else:
                    clicks.append((x,y, time.time(), btnClicked))
        
        with mouse.Listener(on_click=addClick,on_scroll=stopRecording) as listener:
            listener.join()

        with open(f'{file_name}.txt', 'w') as file:
            for click in clicks:
                file.write(f"{click[0]} {click[1]} {click[2]} {click[3]}\n")

        toaster.show_toast(title='Info', 
                            msg='Recording finished and saved succesfully.', 
                            **TOASTER_SETTINGS)

def handleKeybClick(e):
    if(e.name == '7'):
        if(len(settings.play_clicks) != 0 and settings.playing):
            settings.paused = not settings.paused
            toaster.show_toast(title='Info', 
                               msg=f'Program is {'paused' if not settings.paused else 'resumed'}!', 
                               **TOASTER_SETTINGS)
        else:
            toaster.show_toast(title='Warning', 
                               msg='Program is not running!', 
                               **TOASTER_SETTINGS)

        
    elif (e.name == '8'):
        if(settings.click_index > 1 and settings.playing):
            settings.click_index -= 1
            settings.start_time = settings.play_clicks[settings.click_index - 1][2]
            settings.play_x = settings.play_clicks[settings.click_index][0]
            settings.play_y = settings.play_clicks[settings.click_index][1]
            settings.click_time = settings.play_clicks[settings.click_index][2]
            settings.play_c = settings.play_clicks[settings.click_index][3]
            toaster.show_toast(title='Info', 
                    msg='Went back 1 click!', 
                    **TOASTER_SETTINGS)
        elif(not settings.playing):
            toaster.show_toast(title='Error', 
                            msg='Program is not running!', 
                            **TOASTER_SETTINGS)
        elif(not settings.click_index > 1):
            toaster.show_toast(title='Error', 
                            msg='Beginning reached, cannot go back further!', 
                            **TOASTER_SETTINGS)
            

    elif(e.name == '9'):
        if(os.path.exists(CONFIG_LAST_OPEN)):
            if(not settings.playing and len(settings.play_clicks) == 0 and settings.paused):
                resetSettings()
                with open(CONFIG_LAST_OPEN, 'r') as file:
                    threading.Thread(target=play, args=(file.read())).start()
                    toaster.show_toast(title='Info',
                                        msg='Rerun last program!', 
                                        **TOASTER_SETTINGS)
            else:
                toaster.show_toast(title='Error', 
                                    msg='Already running a program!', 
                                    **TOASTER_SETTINGS)

        else:
            messagebox.showwarning('Warning', 'There is no last open file configuration.')
            toaster.show_toast(title='Error', 
                                msg='Error rerunning last program!', 
                                **TOASTER_SETTINGS)


    elif (e.name == 'esc'):
        if(settings.playing):
            settings.exited = True
            settings.playing = False
            settings.paused = True
            settings.play_clicks = []
            toaster.show_toast(title='Info', 
                                msg='Exited program!', 
                                **TOASTER_SETTINGS)
        else:
            toaster.show_toast(title='Info',
                                msg='Program is not running!',
                                **TOASTER_SETTINGS)            
    elif (e.name == '6'):
        pyautogui.scroll(-500)

    elif(e.name == '5'):
        pyautogui.scroll(-1)

    elif(e.name == '4'):
        pyautogui.scroll(1)

def resetSettings():
    settings.click_index = 0
    settings.playing = False
    settings.paused = True
    settings.play_clicks = []
    settings.exited = False


def handleButtonEnter(e):
    e.widget.config(bg=BTN_HOVER_COLOR, cursor='hand2')

def handleButtonLeave(e):
    e.widget.config(bg=BTN_DEAFULT_COLOR)
