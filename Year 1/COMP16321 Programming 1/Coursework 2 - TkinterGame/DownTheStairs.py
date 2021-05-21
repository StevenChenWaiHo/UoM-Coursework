# Screen Resolution 1920x1080
# Assets Source:
# Character: https://laredgames.itch.io/char-ice
# Tiles: https://craftpix.net/freebies/free-medieval-tileset-pixel-art-pack/
# Buttons: https://pngtree.com/freepng/set-red-game-buttons-with--style-for-casual-games-app--development_5004166.html
# Calculator: Windows Built-in Calculator

from tkinter import Tk, PhotoImage, Canvas, Label, Button, Entry, filedialog
import time
from random import randint
from math import ceil
import os

# Window Size
Height = 900
Width = 800
GUI_Size = 50  # Make Room for Top GUI

# Configure Window

Window = Tk()

ws = Window.winfo_screenwidth()  # width of the screen
hs = Window.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for the Tk root window
ws = (ws / 2) - (Width / 2)
hs = (hs / 2) - (Height / 2) - 40

backgroundColour = "#c5efef"

Window.geometry('%dx%d+%d+%d' % (Width, Height, ws, hs))
Window.title("Down The Stairs")
Window.resizable(width=False, height=False)
canvas = Canvas(Window, width=Width, height=Height, bg=backgroundColour)
canvas.pack()
refresh_rate = 0.001
Screen = 0  # Screen Displaying 0:Menu | 1:ChooseGame | 2:Game | 3:Leaderboard | 4:Settings | -1:Exit

#  ==========================================================================Change Difficulty (HERE)=============================================================================================

init_scroll_speed = 1.0  # Proportional to Difficulty
spike_ratio = 6  # Inversely Proportional to Difficulty
Tile_lv = 9  # Inversely Proportional to Difficulty
g = 0.05  # Proportional to Difficulty
max_x_v = 4.0  # Inversely Proportional to Difficulty

#  ===============================================================================================================================================================================================
# Variable Needs to be defined without using Game_Init()
KeySettings = ["a", "d", "p", "Escape", "c"]  # [Left,Right,Pause,Boss,Cheat]
KeySet_flag = -1
button_flag = [0, 0]  # 1 when Key is pressed [Left,Right]
cheatCode = 0  # Press c Three times to Activate/Deactivate Cheat
pressed = 0
ScrollSpeed_E, SpikeRatio_E, Tile_lv_E, g_btn_E, max_x_v_E = 0, 0, 0, 0, 0
folder = ""


# Quick Sort
def sep(a, s, h):
    pivot = a[s][0]
    tmp_l = s
    s += 1
    while True:
        while s <= h and int(a[h][0]) <= int(pivot):
            h -= 1
        while s <= h and int(a[s][0]) >= int(pivot):
            s += 1
        if s <= h:
            a[s], a[h] = a[h], a[s]
        else:
            break
    a[tmp_l], a[h] = a[h], a[tmp_l]
    return h


def sort(a, s, h):
    if s >= h:
        return

    pivot = sep(a, s, h)

    sort(a, s, pivot - 1)
    sort(a, pivot + 1, h)
    return a


# Sort and Output Leaderboard
def updateLeaderboard():
    global score, Leaderboard, Cheat_History
    if score > int(Leaderboard[len(Leaderboard) - 1][0]) and Cheat_History == 0:
        tmp = [[0, ""]] * (len(Leaderboard) + 1)  # Create a Larger Array for new score
        for record in range(len(Leaderboard)):  # Copy Leaderboard to Tmp List
            tmp[record] = Leaderboard[record]
        tmp[record] = [score, Name_Input.get()]
        sort(tmp, 0, len(Leaderboard) - 1)  # Sort the Leaderboard
        for record in range(len(Leaderboard)):
            Leaderboard[record] = tmp[record]
    Leaderboard_File = open("Leaderboard.txt", "w")
    for record, player in Leaderboard:
        Leaderboard_File.write(str(record) + ": " + player + "\n")
    Leaderboard_File.close()


# Keyboard Binds
def keypress(event):
    global Height, Width, x_v, max_x_v, Screen, KeySettings, KeySet_flag, button_flag, Game_Init_flag, cheatCode, Cheat_History, Cheat_flag, Boss_flag, Fake_Screen, Fake_Screen_img
    if Game_Init_flag == 0 and Screen == 2:
        if event.keysym == KeySettings[0] and pause_flag == 0:
            if button_flag[0] == 0:
                if button_flag[1] == 0:  # Move when Right is not Pressed
                    x_v = -max_x_v
                else:  # Stop when Right is Pressed
                    x_v = 0
            button_flag[0] = 1
        if event.keysym == KeySettings[1] and pause_flag == 0:
            if button_flag[1] == 0:
                if button_flag[0] == 0:  # Move when Left is not Pressed
                    x_v = max_x_v
                else:
                    x_v = 0  # Stop when Left is Pressed
            button_flag[1] = 1
        if event.keysym == KeySettings[2] and Boss_flag == 0:  # Pause Button
            pause()
        if event.keysym == KeySettings[4]:  # Activate Cheat
            if game_over_flag == 0:
                cheatCode += 1
                if cheatCode == 3:
                    cheatCode = 0
                    if Cheat_flag == 0:
                        canvas.config(bg="red")
                        Cheat_History = 1
                        Cheat_flag = 1
                        Window.update()
                    else:
                        canvas.config(bg=backgroundColour)
                        Cheat_flag = 0
                        Window.update()
    if event.keysym == KeySettings[3]:  # Boss Button
        if Boss_flag == 0:
            Window.title("Calculator")
            Fake_Screen = Label(Window, image=Fake_Screen_img)
            Fake_Screen.place(x=0, y=0)
            Boss_flag = 1
        else:
            Window.title("Down The Stairs")
            Fake_Screen.destroy()  # Destroy Fake Screen
            Boss_flag = 0
        if pause_flag == 0 and Game_Init_flag == 0:
            pause()
    if Screen == 4:  # Change Key Setting
        if KeySet_flag != -1:
            KeySettings[KeySet_flag] = event.keysym
            KeySet_flag = -1


def keyrelease(event):
    global x_v, max_x_v, button_flag, Game_Init_flag
    if Game_Init_flag == 0:
        if event.keysym == KeySettings[0] and pause_flag == 0:
            button_flag[0] = 0
            if button_flag[1] == 0:  # Stop when Right is Pressed
                x_v = 0
            else:  # Move when Right is not Pressed
                x_v = max_x_v
        if event.keysym == KeySettings[1] and pause_flag == 0:
            button_flag[1] = 0
            if button_flag[0] == 0:  # Stop when Left is Pressed
                x_v = 0
            else:
                x_v = -max_x_v  # Move when Left is not Pressed


# Keyboard Bind
Window.bind_all('<KeyPress>', keypress)
Window.bind_all('<KeyRelease>', keyrelease)


# Hide_All Assets
def Hide_All():
    global Tiles
    # Hide Game Assets
    canvas.itemconfig(character, state="hidden")
    canvas.itemconfig(Top_Banner, state="hidden")
    canvas.itemconfig(Bot_Banner, state="hidden")
    Scoreboard.place_forget()
    Highscore_Label.place_forget()
    Pause_btn.place_forget()
    canvas.itemconfig(Top_Spikes, state="hidden")
    CountDown.place_forget()
    Any_Label.place_forget()
    Any_Label2.place_forget()
    Submit_btn.place_forget()
    Play_btn.place_forget()
    Save_btn.place_forget()
    Exit_btn.place_forget()
    Name_Input.place_forget()
    for t in range(len(Tiles)):
        canvas.itemconfigure(Tiles[t], state='hidden')


def Display_All():
    global Tiles
    # Reveal Game Assets
    canvas.config(bg=backgroundColour)
    canvas.itemconfig(character, state="normal")
    canvas.itemconfig(Top_Banner, state="normal")
    canvas.itemconfig(Bot_Banner, state="normal")
    Scoreboard.place(x=0, y=0)
    Highscore_Label.place(x=0, y=Height - GUI_Size)
    Pause_btn.place(x=Width - 50, y=0)
    canvas.itemconfig(Top_Spikes, state="normal")
    for t in range(len(Tiles)):
        canvas.itemconfigure(Tiles[t], state='normal')


# Count Down
def CountDown_Func():
    global Width, Height, Screen, pause_flag, Boss_flag
    CountDown.place(x=Width / 2 - 20, y=Height / 2 - 50)
    if Boss_flag == 0:
        for count in reversed(range(1, 4)):
            if Screen != 2:  # Stop if Exit Button is pressed
                Window.update()
                break
            CountDown.config(text=count)
            Window.update()
            if Boss_flag == 1:  # Stop if Boss Key is pressed
                break
            else:
                time.sleep(1)
    if Screen != 0 and Boss_flag == 0:  # Stop if Exit Button is pressed // !!
        CountDown.config(text="START")
        CountDown.place(x=Width / 2 - 105, y=Height / 2 - 50)
        Window.update()
        time.sleep(1)
    CountDown.place_forget()
    if Boss_flag == 1:
        pause()


# Pause Button
def pause():
    global pause_flag, pause_btn_flag, game_over_flag, button_flag, Boss_flag, x_v, Fake_Screen
    if game_over_flag == 0 and Screen == 2:
        if pause_btn_flag == 0:
            pause_btn_flag = 1
            if pause_flag == 0 or Boss_flag == 1:
                button_flag = [0, 0]  # Reset Button
                CountDown.config(text="Pause")
                CountDown.place(x=Width / 2 - 100, y=Height / 2)
                pause_flag = 1
                pause_btn_flag = 0
            else:
                if Boss_flag == 1:
                    canvas.delete(Fake_Screen)
                    Boss_flag = 0
                x_v = 0
                Pause_btn.config(image=Pause_btn_img)
                pause_flag = 0
                CountDown.place(x=Width / 2 - 10, y=Height / 2)
                CountDown_Func()
                pause_btn_flag = 0


# Save Button
def save():
    global folder, Width, Height, GUI_Size, x, y, max_x_v, x_v, g, y_v, pointer, spike_ratio, score, Highscore, sprite_stage, scroll_speed, Tile_lv, pause_flag, game_over_flag, Game_Init_flag, Cheat_History, Game_Play_flag, Tiles, Tile_Type
    # Ask For Save Folder
    folder = filedialog.askdirectory(initialdir=os.getcwd() + "/Saves", title='Create Save')
    if bool(folder):
        # Save Game Data
        game_data_file = open(folder + "/Data.txt", "w")
        game_data_file.write("\n".join(
            [str(Width), str(Height), str(GUI_Size), str(x), str(y), str(max_x_v), str(x_v), str(g), str(y_v), str(pointer), str(spike_ratio),
             str(score), str(Highscore), str(sprite_stage), str(scroll_speed), str(Tile_lv), str(pause_flag),
             str(game_over_flag), str(Game_Init_flag), str(Game_Play_flag), str(Cheat_History)]))
        game_data_file.close()
        # Save Tile Data
        tile_data_file = open(folder + "/Tiles.txt", "w")
        for t in range(len(Tiles)):
            tile_data_file.write(
                str(canvas.coords(Tiles[t])[0]) + " " + str(canvas.coords(Tiles[t])[1]) + " " + str(
                    Tile_Type[t]) + "\n")
        tile_data_file.close()


def No_Save():
    global choice, folder
    choice = -1
    Change_Screen(1)
    if bool(folder):
        # Create Popup Error Msg
        popup = Tk()
        pressed = 0

        def popupDestroy():
            global pressed
            popup.destroy()
            pressed = 1

        popup.title("Error")
        popup.geometry('%dx%d+%d+%d' % (250, 100, ws + Width / 2 - 125, hs + Height / 2 - 50))

        Label(popup, text="No Save in Directory: \n" + folder, anchor="center", wraplength=240).pack()
        Button(popup, text="Ok", command=popupDestroy).pack()
        popup.attributes("-topmost", True)
        while pressed == 0:
            popup.update()


# Load Button
def Load():
    global folder, pressed, choice, Screen, Width, Height, ws, hs, GUI_Size, x, y, max_x_v, x_v, g, y_v, pointer, spike_ratio, score, Highscore, sprite_stage, scroll_speed, Tile_lv, pause_flag, game_over_flag, Game_Init_flag, Game_Play_flag, Cheat_History, Tiles, Tile_Type
    Window.update()
    try:
        # Ask For Save Folder
        folder = filedialog.askdirectory(initialdir=os.getcwd() + "/Saves", title='Load Save')
    except FileNotFoundError:
        choice = -1
        Change_Screen(1)
    except TypeError:
        choice = -1
        Change_Screen(1)
    else:
        try:
            # Load Game File
            game_data = open(folder + "/Data.txt", "r").readlines()
        except FileNotFoundError:
            No_Save()
        except TypeError:
            No_Save()
        else:
            try:
                # Load Tile File
                tile_data = open(folder + "/Tiles.txt", "r").readlines()
            except FileNotFoundError:
                No_Save()
            except TypeError:
                No_Save()
            else:
                for i in range(len(game_data)):
                    game_data[i] = game_data[i].strip("\n")
                Width, Height, GUI_Size, x, y, max_x_v, x_v, g, y_v = int(game_data[0]), int(game_data[1]), int(
                    game_data[2]), float(
                    game_data[3]), float(game_data[4]), float(game_data[5]), float(game_data[6]), float(game_data[7]), float(game_data[8])
                pointer, spike_ratio, score, sprite_stage, scroll_speed, Tile_lv, pause_flag, game_over_flag, Game_Init_flag, Game_Play_flag, Cheat_History = int(game_data[9]), int(game_data[10]), int(game_data[11]), int(
                    game_data[13]), float(game_data[14]), int(game_data[15]), int(game_data[16]), int(game_data[17]), int(game_data[18]), int(game_data[19]), int(game_data[20])
                if score > Highscore:
                    Highscore_Label.config(text="Highscore: " + str(score))
                    Highscore_Label.config(fg="red")
                else:
                    Highscore = int(game_data[12])

                for t in range(len(tile_data)):
                    tile_data[t] = tile_data[t].split(" ")
                    tile_data[t][2] = tile_data[t][2].strip("\n")
                for t in range(len(Tiles)):
                    canvas.delete(Tiles[t])  # Destroy old Assets
                Tiles = [0] * Tile_lv  # Create New Circular Array depending on New Tile_Lv
                Tile_Type = [0] * Tile_lv
                for t in range(Tile_lv):
                    if int(tile_data[t][2]) == 0:
                        img = Spike_Tile_img
                    else:
                        img = Tile_img
                    Tiles[t] = canvas.create_image(tile_data[t][0], tile_data[t][1], image=img)
                    Tile_Type[t] = tile_data[t][2]

                # Update Assets
                if float(y_v) == float(scroll_speed):  # Change Character Model depending velocity
                    if x_v > 0:
                        canvas.itemconfig(character, image=R_run_img[sprite_stage])
                    elif x_v < 0:
                        canvas.itemconfig(character, image=L_run_img[sprite_stage])
                    else:
                        canvas.itemconfig(character, image=Idle_img)
                else:
                    if x_v > 0:
                        canvas.itemconfig(character, image=R_fall_img)
                    elif x_v < 0:
                        canvas.itemconfig(character, image=L_fall_img)
                    else:
                        canvas.itemconfig(character, image=fall_img)

                if score > 0:  # Change Scoreboard txt
                    Scoreboard.config(text="Score: " + str(score))
                Window.update()

# Submit Button
def Submit_Game():
    global score, Submit_flag, Exit_flag, Leaderboard, Screen, Name_Input
    Submit_flag = 1
    if score > int(Leaderboard[len(Leaderboard) - 1][0]) and Cheat_History == 0:
        if not 0 < len(Name_Input.get()) <= 20:
            Submit_flag = 0
            Any_Label2.config(text="Name can only be 1 to 20 Characters Long")
            Any_Label2.place(x=Width / 2 - 130, y=Height / 2 + 70)
            Window.update()
        else:
            updateLeaderboard()
            Screen = 0
    else:
        Screen = 0


# Game Over Function
def Game_Over():
    global game_over_flag, Height, Record_Break_flag, Submit_flag, Cheat_History, clear
    game_over_flag = 1
    Pause_btn.place_forget()
    CountDown.config(text="GAME OVER", bg="white")

    if score > int(Leaderboard[len(Leaderboard) - 1][0]) and Cheat_History == 0:
        Any_Label.config(text="You Have Beaten a Person on Leaderboard\nPlease Input Your Name")
        CountDown.place(x=Width / 2 - 195, y=Height / 2 - 190)
        Any_Label.place(x=Width / 2 - 250, y=Height / 2 - 80)
        if clear == 0:
            Name_Input.delete("0", "end")
            clear = 1
        Name_Input.place(x=Width / 2 - 110, y=Height / 2 + 40)
        Submit_btn.place(x=Width / 2 + 90, y=Height / 2 + 28)
        Record_Break_flag = 1
    else:
        CountDown.place(x=Width / 2 - 190, y=Height / 2 - 40)
        Exit_btn.config(bg=backgroundColour, activebackground=backgroundColour)
        Exit_btn.place(x=Width / 2 - 10, y=Height / 2 + 60)


def Load_Settings():
    global KeySettings, init_scroll_speed, spike_ratio, Tile_lv, g, max_x_v, refresh_rate
    try:
        Settings_File_l = open("Settings.txt", "r").readlines()
    except FileNotFoundError:
        Settings_File_l = open("Settings.txt", "w")
        Settings_File_l.write(
            "scroll speed = 1.0\nspike_ratio = 6\nTile_lv = 9\ng = 0.05\nmax_x_v = 4.0\nrefresh_rate = 0.001\nKeySettings = a, d, p, Escape, c")
        Settings_File_l.close()
        Settings_File_l = open("Settings.txt", "r").readlines()
    for i in range(len(Settings_File_l)):
        Settings_File_l[i] = Settings_File_l[i].strip("\n")
        Settings_File_l[i] = Settings_File_l[i].split(" = ")
    Settings_File_l[6][1] = Settings_File_l[6][1].split(", ")
    KeySettings = [Settings_File_l[6][1][0], Settings_File_l[6][1][1], Settings_File_l[6][1][2],
                   Settings_File_l[6][1][3], Settings_File_l[6][1][4]]
    init_scroll_speed, spike_ratio, Tile_lv, g, max_x_v, refresh_rate = float(Settings_File_l[0][1]), int(
        Settings_File_l[1][1]), int(Settings_File_l[2][1]), float(Settings_File_l[3][1]), float(
        Settings_File_l[4][1]), float(Settings_File_l[5][1])


def Update_Settings():
    global KeySettings, init_scroll_speed, spike_ratio, Tile_lv, g, max_x_v, refresh_rate, ScrollSpeed_E, SpikeRatio_E, Tile_lv_E, g_btn_E, max_x_v_E
    error = ""
    # Check For Error
    GameSettings = [ScrollSpeed_E.get(), SpikeRatio_E.get(), Tile_lv_E.get(), g_btn_E.get(), max_x_v_E.get()]
    ScrollSpeed_E.destroy()
    SpikeRatio_E.destroy()
    Tile_lv_E.destroy()
    g_btn_E.destroy()
    max_x_v_E.destroy()
    try:
        tmp = float(GameSettings[0])
        if tmp > 0:
            init_scroll_speed = tmp
        else:
            error = error + "Scroll Speed must be positive\n"
    except ValueError:
        error = error + "Scroll Speed\n"
    try:
        tmp = int(GameSettings[1])
        if tmp >= 0:
            spike_ratio = tmp
        else:
            error = error + "Spike Ratio cannot be negative\n"
    except ValueError:
        error = error + "Spike Ratio must be integer\n"
    try:
        tmp = int(GameSettings[2])
        if tmp >= 3:
            Tile_lv = tmp
        else:
            error = error + "Tile Levels too small\n"
    except ValueError:
        error = error + "Tile Levels must be integer\n"
    try:
        tmp = float(GameSettings[3])
        if tmp > 0:
            g = tmp
        else:
            error = error + "Downward Acceleration must be positive\n"
    except ValueError:
        error = error + "Downward Acceleration\n"
    try:
        tmp = float(GameSettings[4])
        if tmp > 0:
            max_x_v = tmp
        else:
            error = error + "Max Horizontal Speed must be positive\n"
    except ValueError:
        error = error + "Max Horizontal Speed\n"

    if bool(error):
        # Create Popup Error Msg
        popup = Tk()
        pressed = 0

        def popupDestroy():
            global pressed
            popup.destroy()
            pressed = 1

        popup.title("Error")
        popup.geometry('%dx%d+%d+%d' % (250, 200, ws + Width / 2 - 125, hs + Height / 2 - 100))

        Label(popup, text="\nError in Settings: \n\n" + error, anchor="center", wraplength=240).pack()
        Button(popup, text="Ok", command=popupDestroy).pack()
        popup.attributes("-topmost", True)
    Settings_File_l = open("Settings.txt", "w")
    Settings_File_l.write("scroll speed = " + str(init_scroll_speed) + "\n")
    Settings_File_l.write("spike_ratio = " + str(spike_ratio) + "\n")
    Settings_File_l.write("Tile_lv = " + str(Tile_lv) + "\n")
    Settings_File_l.write("g = " + str(g) + "\n")
    Settings_File_l.write("max_x_v = " + str(max_x_v) + "\n")
    Settings_File_l.write("refresh_rate = " + str(refresh_rate) + "\n")
    Settings_File_l.write("KeySettings = " + ", ".join(KeySettings) + "\n")
    Settings_File_l.close()


def Load_Game_Assets(Width_l, GUI_Size_l):
    # @Load Settings
    Load_Settings()
    # @Load Images
    # Character Assets
    R_run_img_l = [PhotoImage(file="Assets/R_Run_0.gif"), PhotoImage(file="Assets/R_Run_1.gif"),
                   PhotoImage(file="Assets/R_Run_2.gif"),
                   PhotoImage(file="Assets/R_Run_3.gif")]
    L_run_img_l = [PhotoImage(file="Assets/L_Run_0.gif"), PhotoImage(file="Assets/L_Run_1.gif"),
                   PhotoImage(file="Assets/L_Run_2.gif"),
                   PhotoImage(file="Assets/L_Run_3.gif")]
    Idle_img_l = PhotoImage(file="Assets/Idle.gif")
    R_fall_img_l = PhotoImage(file="Assets/Fall_R.gif")
    L_fall_img_l = PhotoImage(file="Assets/Fall_L.gif")
    fall_img_l = PhotoImage(file="Assets/Fall.gif")
    character_l = canvas.create_image(0, 0, image=Idle_img_l)

    # @GUI
    # Top Banner
    Top_Banner_l = canvas.create_rectangle(0, 0, Width_l, GUI_Size_l, fill="Black")

    # Bot Banner
    Bot_Banner_l = canvas.create_rectangle(0, Height - GUI_Size, Width_l, Height, fill="Black")

    # ScoreBoard
    Scoreboard_l = Label(Window, text="Score: 0", font=("Arial", 30), bg="black", fg="white")

    # Leaderboard
    Highscore_Label_l = Label(Window, text="Highest Score: 100", font=("Arial", 30), bg="black", fg="white")

    # Buttons and CountDown Label
    Pause_btn_img_l = PhotoImage(file="Assets/Pause.gif")
    Pause_btn_l = Button(Window, image=Pause_btn_img_l, command=pause, highlightthickness=0, border=0, bg="black",
                         activebackground="black")

    Play_btn_img_l = PhotoImage(file="Assets/Play.gif")
    Play_btn_l = Button(Window, image=Play_btn_img_l, command=pause, highlightthickness=0, border=0, bg="black",
                        activebackground="black")

    Save_btn_img_l = PhotoImage(file="Assets/Save.gif")
    Save_btn_l = Button(Window, image=Save_btn_img_l, command=save, highlightthickness=0, border=0, bg="black",
                        activebackground="black")

    CountDown_l = Label(Window, text="Pause", font=("Arial", 50), bg="white", fg="black", borderwidth=2, relief="solid")

    Any_Label_l = Label(Window, text="", font=("Arial", 20), bg="white", fg="black", borderwidth=1,
                        relief="solid")
    Any_Label_l.place_forget()
    Any_Label2_l = Label(Window, text="", font=("Arial", 10), bg="white", fg="red")

    Submit_btn_img_l = PhotoImage(file="Assets/Submit.gif")
    Submit_btn_l = Button(Window, image=Submit_btn_img_l, command=Submit_Game, highlightthickness=0, border=0,
                          bg=backgroundColour,
                          activebackground=backgroundColour)

    Exit_btn_img_l = PhotoImage(file="Assets/Exit.gif")
    Exit_btn_l = Button(Window, image=Exit_btn_img_l, command=lambda: Change_Screen(0), highlightthickness=0, border=0,
                        bg=backgroundColour,
                        activebackground=backgroundColour)

    # Top Spikes
    Top_Spikes_img_l = PhotoImage(file="Assets/Long_Spikes.gif")
    Top_Spikes_l = canvas.create_image(Width / 2, GUI_Size + 25, image=Top_Spikes_img_l)

    # Name Input
    Name_Input_l = Entry(Window)
    Name_Input_l.place_forget()

    # @Create Tiles
    Tile_img_l = PhotoImage(file="Assets/Large_Tile.gif")
    Spike_Tile_img_l = PhotoImage(file="Assets/Spike_Tile.gif")  # Create SpikesTile

    # Fake Screen
    Fake_Screen_img_l = PhotoImage(file="Assets/Fake_Screen.gif")
    Fake_Screen_l = canvas.create_image(0, 0, image=Fake_Screen_img_l)
    canvas.delete(Fake_Screen_l)

    return character_l, R_run_img_l, L_run_img_l, R_fall_img_l, L_fall_img_l, fall_img_l, Idle_img_l, Play_btn_l, Play_btn_img_l, Pause_btn_l, Pause_btn_img_l, Save_btn_l, Save_btn_img_l, CountDown_l, Any_Label_l, Any_Label2_l, Submit_btn_l, Submit_btn_img_l, Exit_btn_l, Exit_btn_img_l, Top_Banner_l, Bot_Banner_l, Top_Spikes_l, Top_Spikes_img_l, Scoreboard_l, Highscore_Label_l, Tile_img_l, Spike_Tile_img_l, Name_Input_l, Fake_Screen_l, Fake_Screen_img_l,


def Game_Init():
    global Height, GUI_Size, Tile_lv, Game_Init_flag, Game_Play_flag, Record_Break_flag, Exit_flag, init_scroll_speed
    # Character Position and Velocity Initialize
    x_l = randint(Width / 2 - 3, Width / 2 + 300)
    y_l = 400
    x_v_l = 0
    y_v_l = 0

    # Pause Button flag
    pause_flag_l = 0
    pause_btn_flag_l = 0
    # Submit Button flag
    Submit_flag_l = 0

    # Create Score
    score_l = -5  # First 5 Tile not counted
    Scoreboard.config(text="Score: 0")
    try:
        # Load Leaderboard
        Leaderboard_File_l = open("Leaderboard.txt", "r").readlines()
    except FileNotFoundError:
        Leaderboard_File_l = open("Leaderboard.txt", "w")
        for record in range(10):
            Leaderboard_File_l.write("0: Empty\n")
        Leaderboard_File_l.close()
        Leaderboard_File_l = open("Leaderboard.txt", "r").read()
    i = 0
    Leaderboard_l = [""] * len(Leaderboard_File_l)
    for record_l in Leaderboard_File_l:
        record_l = record_l.strip("\n")
        Leaderboard_l[i] = record_l.split(": ")
        for j in range(len(Leaderboard_l[i]) - 2):
            Leaderboard_l[i][1] = Leaderboard_l[i][1] + Leaderboard_l[i].pop()
        i += 1
    Highscore_l = int(Leaderboard_l[0][0])
    Highscore_Label.config(text="Highscore: " + str(Highscore_l))
    Highscore_Label.config(fg="white")

    # Game Over flag
    game_over_flag_l = 0
    # Sprite Stage
    sprite_stage_l = 0
    # Initialize Tiles
    Tiles_l = [0] * Tile_lv  # Create Circular Array for Tiles
    pointer_l = 0  # Points at Highest Tile
    Tile_Type_l = [1] * Tile_lv
    for i in range(0, Tile_lv):
        Tile_Type_l[i] = randint(0, spike_ratio)
        if Tile_Type_l[i] > 0:
            img = Tile_img
        else:
            img = Spike_Tile_img
        rand_num = randint(0, Width)
        if Tile_Type_l[i] == 0:
            if i > 1:
                # Ensure Consecutive Spiky Tiles are not too close
                while (60 <= abs(rand_num - canvas.coords(Tiles_l[(i - 1) % Tile_lv])[0]) <= 300 and Tile_Type_l[
                    i] == 0) or \
                        (60 <= abs(rand_num - canvas.coords(Tiles_l[(i - 2) % Tile_lv])[0]) <= 300 and Tile_Type_l[
                            i] == 0):
                    rand_num = randint(0, Width)
        Tiles_l[i] = canvas.create_image(rand_num, i * (Height - GUI_Size * 2) / Tile_lv + GUI_Size, image=img)
        canvas.tag_lower(Tiles_l[i])
        closestTile = ceil(
            (canvas.coords(Tiles_l[pointer_l])[1] - y_l) * Tile_lv / -(Height - GUI_Size * 2))  # Find Closest Tile:
        # Create Safe Tile
        if i == closestTile:
            Tile_Type_l[closestTile] = 1  # Start Tile must not be Spiky
            canvas.itemconfig(Tiles_l[closestTile], image=Tile_img)
            x_l = canvas.coords(Tiles_l[closestTile])[0]

    scroll_speed_l = init_scroll_speed
    Game_Init_flag_l = 1
    Game_Play_flag_l = 1
    Record_Break_flag_l = 0
    Cheat_flag_l = 0
    Cheat_History_l = 0
    Boss_flag_l = 0
    clear_l = 0
    Exit_flag_l = 0

    return x_l, y_l, x_v_l, y_v_l, scroll_speed_l, sprite_stage_l, score_l, Leaderboard_l, Highscore_l, pointer_l, game_over_flag_l, pause_flag_l, pause_btn_flag_l, Submit_flag_l, Game_Init_flag_l, Game_Play_flag_l, Record_Break_flag_l, Cheat_flag_l, Cheat_History_l, Boss_flag_l, Exit_flag_l, Tiles_l, Tile_Type_l, clear_l


def Game_Update(Width_l, Height_l, GUI_Size_l, x_l, y_l, x_v_l, y_v_l, pointer_l,
                spike_ratio_l, score_l,
                sprite_stage_l, scroll_speed_l, Tile_lv_l,
                pause_flag_l, game_over_flag_l, Game_Init_flag_l, Game_Play_flag_l, Tiles_l, Tile_Type_l, Cheat_flag_l,
                Cheat_History_l):
    global Highscore, Record_Break_flag
    if Game_Init_flag_l == 1:
        canvas.itemconfig(character, image=fall_img)  # Starting Sequence
        x_v_l = 0
        y_v_l = 0
    if game_over_flag_l == 0:
        if pause_flag_l == 1:  # When Pause_Btn is Pressed
            Pause_btn.place_forget()
            Play_btn.place(x=Width_l - 150, y=1)
            Exit_btn.config(bg="black", activebackground="black")
            Save_btn.place(x=Width_l - 100, y=1)
            Save_btn.config(bg="black", activebackground="black")
            Exit_btn.place(x=Width_l - 50, y=1)
        else:
            Exit_btn.place_forget()
            Play_btn.place_forget()
            Save_btn.place_forget()
            Pause_btn.place(x=Width_l - 50, y=1)

    if 0 <= x_l + x_v_l <= Width_l and Game_Init_flag_l == 0 and game_over_flag_l == 0 and pause_flag_l == 0 and Boss_flag == 0:
        x_l += x_v_l

    # Move Tiles
    if pause_flag_l == 0 and Boss_flag == 0:
        for j in range(len(Tiles_l)):
            canvas.move(Tiles_l[j], 0, -scroll_speed_l)

    # Tiles Detection
    closestTile_l = (pointer_l - 1) % len(Tiles_l)
    if not y_l > canvas.coords(Tiles_l[(pointer_l - 1) % Tile_lv_l])[1]:
        closestTile_l = ceil(
            (canvas.coords(Tiles_l[pointer_l])[1] - y_l) * Tile_lv_l / -(Height - GUI_Size * 2))  # Find Closest Tile
    # Check if Tile is Directly Below
    if canvas.coords(Tiles_l[(pointer_l + closestTile_l) % Tile_lv_l])[0] - 150 <= x_l <= \
            canvas.coords(Tiles_l[(pointer_l + closestTile_l) % Tile_lv_l])[0] + 150 and \
            canvas.coords(Tiles_l[(pointer_l + closestTile_l) % Tile_lv_l])[1] - 30 <= y_l <= \
            canvas.coords(Tiles_l[(pointer_l + closestTile_l) % Tile_lv_l])[1] + 3:
        y_v_l = scroll_speed_l
        y_l = canvas.coords(Tiles_l[(pointer_l + closestTile_l) % Tile_lv_l])[1] - 20
        Game_Init_flag_l = 0
        # Game Over when hit Spiky Tile
        if Tile_Type_l[(pointer_l + closestTile_l) % Tile_lv_l] == 0 and Cheat_flag_l == 0:
            game_over_flag_l = 1

    elif Game_Init_flag_l == 0 and game_over_flag_l == 0 and pause_flag_l == 0 and Boss_flag == 0:
        if Cheat_flag_l == 0:
            y_v_l += g
        else:
            y_v_l = 0  # Active Cheat
        y_l += y_v_l

    # Move Character
    if game_over_flag_l == 0 or GUI_Size_l < y_l < Height - GUI_Size_l and pause_flag_l == 0 and Boss_flag == 0:
        canvas.coords(character, x_l, y_l)

    # Destroy Highest Tile and Create Lowest
    if canvas.coords(Tiles_l[pointer_l])[1] < GUI_Size_l:
        Tile_Type_l[pointer_l] = randint(0, spike_ratio_l)
        if Tile_Type_l[pointer_l] > 0:
            img_l = Tile_img
        else:
            img_l = Spike_Tile_img
        rand_num = randint(0, Width)
        # Ensure Consecutive Spiky Tiles are not too close
        if Tile_Type_l[pointer_l] == 0:
            while (60 <= abs(rand_num - canvas.coords(Tiles_l[(pointer_l - 1) % Tile_lv_l])[0]) <= 300 and Tile_Type[
                pointer_l] == 0) or \
                    (60 <= abs(rand_num - canvas.coords(Tiles_l[(pointer_l - 2) % Tile_lv_l])[0]) <= 300 and Tile_Type[
                        pointer_l] != 0):
                rand_num = randint(0, Width)
        canvas.coords(Tiles_l[pointer_l], rand_num,
                      canvas.coords(Tiles_l[(pointer_l - 1) % Tile_lv_l])[1] + (
                              Height - GUI_Size * 2) / Tile_lv_l)  # Reuse Tiles
        canvas.itemconfig(Tiles_l[pointer_l], image=img_l)
        pointer_l = (pointer_l + 1) % len(Tiles_l)
        if game_over_flag_l == 0 and Game_Init_flag_l == 0:
            score_l += 1
        if score_l > 0:  # Change Scoreboard txt
            Scoreboard.config(text="Score: " + str(score_l))
            if game_over_flag_l == 0:
                scroll_speed_l = round(scroll_speed_l + 0.01, 2)

    # Make Highscore as score if not Cheated
    if score_l > Highscore and Cheat_History_l == 0:
        Highscore_Label.config(text="Highscore: " + str(score))
        Highscore_Label.config(fg="red")

    if Cheat_History_l == 1:
        Highscore_Label.config(text="Highscore: " + str(Highscore))
        Highscore_Label.config(fg="white")

    if Game_Play_flag_l == 1 and game_over_flag_l == 0:
        Pause_btn.place_forget()
        CountDown_Func()
        Game_Play_flag_l = 0

    # Game Over when hit Top or Bottom
    if y_l < GUI_Size_l or y_l > Height - GUI_Size_l + 50:
        game_over_flag_l = 1

    # Jump to Game Over Sequence
    if game_over_flag_l == 1:
        Game_Over()

    if game_over_flag_l == 0 and Game_Init_flag_l == 0 and pause_flag_l == 0 and Boss_flag == 0:
        if y_v_l == scroll_speed_l:  # Change Character Model depending velocity
            if x_v_l > 0:
                canvas.itemconfig(character, image=R_run_img[sprite_stage_l])
            elif x_v_l < 0:
                canvas.itemconfig(character, image=L_run_img[sprite_stage_l])
            else:
                canvas.itemconfig(character, image=Idle_img)
        else:
            if x_v_l > 0:
                canvas.itemconfig(character, image=R_fall_img)
            elif x_v_l < 0:
                canvas.itemconfig(character, image=L_fall_img)
            else:
                canvas.itemconfig(character, image=fall_img)
    sprite_stage_l = (sprite_stage_l + 1) % 4
    Window.update()

    return Width_l, Height_l, x_l, y_l, y_v_l, pointer_l, score_l, sprite_stage_l, scroll_speed_l, game_over_flag_l, Game_Init_flag_l, Game_Play_flag_l, Tiles_l, Tile_Type_l


# @ Switching Screen
def Change_Screen(ScreenNo):
    global Screen
    Screen = ScreenNo


# Choose New Game
def Choose_New():
    global choice, Screen
    Change_Screen(2)
    choice = 0


# Choose Load Game
def Choose_Load():
    global choice, Screen
    Change_Screen(2)
    choice = 1
    Load()


# Game Choose Screen
def To_Choice():
    global Screen, choice
    Screen = 1
    NewGame_l = Label(Window, text="New Game", font=("Arial", 30), bg=backgroundColour, fg="black")
    NewGame_l.place(x=Width / 2 - 180, y=350)
    Play_btn_img_l = PhotoImage(file="Assets/Play.gif")
    Play_btn_l = Button(Window, image=Play_btn_img_l, command=Choose_New, highlightthickness=0, border=0,
                        bg=backgroundColour,
                        activebackground=backgroundColour)
    Play_btn_l.place(x=Width / 2 + 80, y=352)

    LoadGame_l = Label(Window, text="Load Game", font=("Arial", 30), bg=backgroundColour, fg="black")
    LoadGame_l.place(x=Width / 2 - 183, y=450)
    Save_btn_img_l = PhotoImage(file="Assets/Save.gif")
    Save_btn_l = Button(Window, image=Save_btn_img_l, command=Choose_Load, highlightthickness=0, border=0,
                        bg=backgroundColour,
                        activebackground=backgroundColour)
    Save_btn_l.place(x=Width / 2 + 80, y=452)

    Exit_btn_img_l = PhotoImage(file="Assets/Exit.gif")
    Exit_btn_l = Button(Window, image=Exit_btn_img_l, command=lambda: Change_Screen(0), highlightthickness=0, border=0,
                        bg=backgroundColour,
                        activebackground=backgroundColour)
    Exit_btn_l.place(x=Width - 50, y=Height - 50)
    while Screen == 1:
        Window.update()
    if Screen != 1:
        NewGame_l.destroy()
        Play_btn_l.destroy()
        LoadGame_l.destroy()
        Save_btn_l.destroy()
        Exit_btn_l.destroy()
    return choice


# Leaderboard Screen
def To_Leaderboard():
    global Screen
    Screen = 3
    Title_l = Label(Window, text="Top 10", font=("Arial", 60), bg=backgroundColour, fg="black")
    Title_l.place(x=Width / 2 - 125, y=50)
    Exit_btn_img_l = PhotoImage(file="Assets/Exit.gif")
    Exit_btn_l = Button(Window, image=Exit_btn_img_l, command=lambda: Change_Screen(0), highlightthickness=0, border=0,
                        bg=backgroundColour,
                        activebackground=backgroundColour)
    Exit_btn_l.place(x=Width - 50, y=Height - 50)
    try:
        # Load Leaderboard
        Leaderboard_File_l = open("Leaderboard.txt", "r").read()
    except FileNotFoundError:
        Leaderboard_File_l = open("Leaderboard.txt", "w")
        for _ in (range(10)):
            Leaderboard_File_l.write("0: Empty\n")
        Leaderboard_File_l.close()
        Leaderboard_File_l = open("Leaderboard.txt", "r").read()
    # Make Screen Neater
    Leaderboard_File_l = "\n" + Leaderboard_File_l
    Leaderboard_l = Label(Window, padx=3, pady=3, width=25, text=Leaderboard_File_l, font=("Arial", 30),
                          bg=backgroundColour, fg="black", borderwidth=1, justify="center", relief="solid",
                          anchor="center")
    Leaderboard_l.place(x=Width / 2 - 280, y=220)
    while Screen == 3:
        Window.update()
    if Screen != 3:
        Title_l.destroy()
        Leaderboard_l.destroy()
        Exit_btn_l.destroy()


# Set Key are pressed
def SetKey(Key):
    global KeySet_flag
    KeySet_flag = Key


# Setting Screen
def To_Settings():
    global Screen, KeySettings, KeySet_flag, ScrollSpeed_E, SpikeRatio_E, Tile_lv_E, g_btn_E, max_x_v_E
    Screen = 4

    Title_l = Label(Window, text="Settings", font=("Arial", 60), bg=backgroundColour, fg="black")
    Title_l.place(x=Width / 2 - 150, y=50)

    # Key Settings
    KeySettings_Title_l = Label(Window, text="Key Settings:", font=("Arial", 25, "bold"), bg=backgroundColour,
                                fg="black")
    KeySettings_Title_l.place(x=50, y=200)

    Left_btn_Title_l = Label(Window, text="Left", font=("Arial", 25), bg=backgroundColour, fg="black")
    Left_btn_Title_l.place(x=110, y=300)
    Left_btn_l = Button(Window, width=10, text=KeySettings[0], command=lambda: SetKey(0), highlightthickness=0,
                        bg=backgroundColour)
    Left_btn_l.place(x=110, y=350)

    Right_btn_Title_l = Label(Window, text="Right", font=("Arial", 25), bg=backgroundColour, fg="black")
    Right_btn_Title_l.place(x=240, y=300)
    Right_btn_l = Button(Window, width=10, text=KeySettings[1], command=lambda: SetKey(1), highlightthickness=0,
                         bg=backgroundColour)
    Right_btn_l.place(x=240, y=350)

    Pause_btn_Title_l = Label(Window, text="Pause", font=("Arial", 25), bg=backgroundColour, fg="black")
    Pause_btn_Title_l.place(x=370, y=300)
    Pause_btn_l = Button(Window, width=10, text=KeySettings[2], command=lambda: SetKey(2), highlightthickness=0,
                         bg=backgroundColour)
    Pause_btn_l.place(x=370, y=350)

    Boss_btn_Title_l = Label(Window, text="Boss", font=("Arial", 25), bg=backgroundColour, fg="black")
    Boss_btn_Title_l.place(x=500, y=300)
    Boss_btn_l = Button(Window, width=10, text=KeySettings[3], command=lambda: SetKey(3), highlightthickness=0,
                        bg=backgroundColour)
    Boss_btn_l.place(x=500, y=350)

    Cheat_btn_Title_l = Label(Window, text="Cheat", font=("Arial", 25), bg=backgroundColour, fg="black")
    Cheat_btn_Title_l.place(x=620, y=300)
    Cheat_btn_l = Button(Window, width=10, text=KeySettings[4], command=lambda: SetKey(4), highlightthickness=0,
                         bg=backgroundColour)
    Cheat_btn_l.place(x=620, y=350)

    # Game Settings
    GameSettings_Title_l = Label(Window, text="Game Performance Settings:", font=("Arial", 25, "bold"),
                                 bg=backgroundColour, fg="black")
    GameSettings_Title_l.place(x=50, y=450)

    ScrollSpeed_Title_l = Label(Window, text="Scroll Speed", font=("Arial", 25), bg=backgroundColour, fg="black")
    ScrollSpeed_Title_l.place(x=110, y=550)
    ScrollSpeed_E = Entry(Window, width=10, justify="center")
    ScrollSpeed_E.insert(0, init_scroll_speed)
    ScrollSpeed_E.place(x=170, y=600)

    SpikeRatio_Title_l = Label(Window, text="Spike Ratio", font=("Arial", 25), bg=backgroundColour, fg="black")
    SpikeRatio_Title_l.place(x=350, y=550)
    SpikeRatio_E = Entry(Window, width=10, justify="center")
    SpikeRatio_E.insert(0, spike_ratio)
    SpikeRatio_E.place(x=400, y=600)

    Tile_lv_Title_l = Label(Window, text="Tile Levels", font=("Arial", 25), bg=backgroundColour, fg="black")
    Tile_lv_Title_l.place(x=570, y=550)
    Tile_lv_E = Entry(Window, width=10, justify="center")
    Tile_lv_E.insert(0, Tile_lv)
    Tile_lv_E.place(x=600, y=600)

    g_btn_Title_l = Label(Window, text="Downward Acceleration", font=("Arial", 25), bg=backgroundColour, fg="black")
    g_btn_Title_l.place(x=60, y=650)
    g_btn_E = Entry(Window, width=10, justify="center")
    g_btn_E.insert(0, g)
    g_btn_E.place(x=200, y=700)

    max_x_v_Title_l = Label(Window, text="Max Horizontal Speed", font=("Arial", 25), bg=backgroundColour, fg="black")
    max_x_v_Title_l.place(x=460, y=650)
    max_x_v_E = Entry(Window, width=10, justify="center")
    max_x_v_E.insert(0, max_x_v)
    max_x_v_E.place(x=580, y=700)

    Save_btn_img_l = PhotoImage(file="Assets/Save.gif")
    Save_btn_l = Button(Window, image=Save_btn_img_l, command=lambda: Change_Screen(0), highlightthickness=0, border=0,
                        bg=backgroundColour)
    Save_btn_l.place(x=Width - 50, y=Height - 50)
    while Screen == 4:
        Left_btn_l.configure(bg=backgroundColour)
        Right_btn_l.configure(bg=backgroundColour)
        Pause_btn_l.configure(bg=backgroundColour)
        Boss_btn_l.configure(bg=backgroundColour)
        Cheat_btn_l.configure(bg=backgroundColour)
        Left_btn_l.configure(text=KeySettings[0])
        Right_btn_l.configure(text=KeySettings[1])
        Pause_btn_l.configure(text=KeySettings[2])
        Boss_btn_l.configure(text=KeySettings[3])
        Cheat_btn_l.configure(text=KeySettings[4])
        if KeySet_flag == 0:
            Left_btn_l.configure(bg="SkyBlue2")
        elif KeySet_flag == 1:
            Right_btn_l.configure(bg="SkyBlue2")
        elif KeySet_flag == 2:
            Pause_btn_l.configure(bg="SkyBlue2")
        elif KeySet_flag == 3:
            Boss_btn_l.configure(bg="SkyBlue2")
        elif KeySet_flag == 4:
            Cheat_btn_l.configure(bg="SkyBlue2")
        Window.update()
    if Screen != 4:
        Title_l.destroy()
        KeySettings_Title_l.destroy()
        Left_btn_Title_l.destroy()
        Left_btn_l.destroy()
        Right_btn_Title_l.destroy()
        Right_btn_l.destroy()
        Pause_btn_Title_l.destroy()
        Pause_btn_l.destroy()
        Boss_btn_Title_l.destroy()
        Boss_btn_l.destroy()
        Cheat_btn_Title_l.destroy()
        Cheat_btn_l.destroy()
        GameSettings_Title_l.destroy()
        ScrollSpeed_Title_l.destroy()
        SpikeRatio_Title_l.destroy()
        Tile_lv_Title_l.destroy()
        g_btn_Title_l.destroy()
        max_x_v_Title_l.destroy()
        Save_btn_l.destroy()
    Update_Settings()


# Menu Screen
def To_Menu():
    global Screen
    Screen = 0
    Background_img_l = PhotoImage(file="Assets/Background_Menu.gif")
    Background_l = Label(Window, image=Background_img_l)
    Background_l.place(x=0, y=0)
    Title_l = Label(Window, text="Down The Stairs", font=("Arial", 60), bg=backgroundColour, fg="black")
    Title_l.place(x=Width / 2 - 295, y=150)

    Play_btn_img_l = PhotoImage(file="Assets/Play.gif")
    Play_btn_l = Button(Window, image=Play_btn_img_l, command=lambda: Change_Screen(1), highlightthickness=0, border=0,
                        bg=backgroundColour,
                        activebackground=backgroundColour)
    Play_btn_l.place(x=Width / 2 - 20, y=Height / 2)

    Leaderboard_btn_img_l = PhotoImage(file="Assets/Leaderboard.gif")
    Leaderboard_btn_l = Button(Window, image=Leaderboard_btn_img_l, command=lambda: Change_Screen(3),
                               highlightthickness=0,
                               border=0,
                               bg=backgroundColour,
                               activebackground=backgroundColour)
    Leaderboard_btn_l.place(x=Width / 2 - 20, y=Height / 2 + 60)

    Settings_btn_img_l = PhotoImage(file="Assets/Settings.gif")
    Settings_btn_l = Button(Window, image=Settings_btn_img_l, command=lambda: Change_Screen(4), highlightthickness=0,
                            border=0,
                            bg=backgroundColour,
                            activebackground=backgroundColour)
    Settings_btn_l.place(x=Width / 2 - 20, y=Height / 2 + 120)

    Exit_btn_img_l = PhotoImage(file="Assets/Exit.gif")
    Exit_btn_l = Button(Window, image=Exit_btn_img_l, command=Exit_Screen, highlightthickness=0, border=0,
                        bg=backgroundColour,
                        activebackground=backgroundColour)
    Exit_btn_l.place(x=Width - 50, y=Height - 50)
    while Screen == 0:
        Window.update()
    if Screen != 0:
        Background_l.destroy()
        Title_l.destroy()
        Play_btn_l.destroy()
        Leaderboard_btn_l.destroy()
        Settings_btn_l.destroy()
        Exit_btn_l.destroy()


def Exit_Screen():
    global Screen
    Screen = -1


# Load Game Assets
character, R_run_img, L_run_img, R_fall_img, L_fall_img, fall_img, Idle_img, Play_btn, Play_btn_img, Pause_btn, Pause_btn_img, Save_btn, Save_btn_im, CountDown, Any_Label, Any_Label2, Submit_btn, Submit_btn_img, Exit_btn, Exit_btn_img, Top_Banner, Bot_Banner, Top_Spikes, Top_Spikes_img, Scoreboard, Highscore_Label, Tile_img, Spike_Tile_img, Name_Input, Fake_Screen, Fake_Screen_img = Load_Game_Assets(
    Width, GUI_Size)
x, y, x_v, y_v, scroll_speed, sprite_stage, score, Leaderboard, Highscore, pointer, game_over_flag, pause_flag, pause_btn_flag, Submit_flag, Game_Init_flag, Game_Play_flag, Record_Break_flag, Cheat_flag, Cheat_History, Boss_flag, Exit_flag, Tiles, Tile_Type, clear = Game_Init()

Hide_All()

choice = -1

while Screen != -1:
    if Screen == 0:
        To_Menu()
    elif Screen == 1:
        x, y, x_v, y_v, scroll_speed, sprite_stage, score, Leaderboard, Highscore, pointer, game_over_flag, pause_flag, pause_btn_flag, Submit_flag, Game_Init_flag, Game_Play_flag, Record_Break_flag, Cheat_flag, Cheat_History, Boss_flag, Exit_flag, Tiles, Tile_Type, clear = Game_Init()
        Hide_All()
        choice = To_Choice()
        if Screen == 2:
            Display_All()
            while Screen == 2:
                Width, Height, x, y, y_v, pointer, score, sprite_stage, scroll_speed, game_over_flag, Game_Init_flag, Game_Play_flag, Tiles, Tile_Type = Game_Update(
                    Width, Height, GUI_Size, x, y, x_v, y_v, pointer, spike_ratio, score, sprite_stage,
                    scroll_speed, Tile_lv, pause_flag, game_over_flag, Game_Init_flag, Game_Play_flag, Tiles, Tile_Type,
                    Cheat_flag,
                    Cheat_History)
                time.sleep(refresh_rate)
        Hide_All()
        canvas.config(bg=backgroundColour)
    elif Screen == 3:
        To_Leaderboard()
    elif Screen == 4:
        To_Settings()
