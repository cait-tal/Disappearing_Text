from tkinter import *
from tkinter import filedialog
from round_button import RoundedButton
from bs4 import BeautifulSoup
import requests
import random

CREAM_WHITE = "#FEFFE2"
DARK_GREEN = "#5F7A61"
BUTTON_UNCLICK = "#5E8B7E"
BUTTON_CLICK = "#A7C4BC"
BIG_FONT = ("Verdana", 32, "bold")
LITTLE_FONT = ("Verdana", 16, "normal")
PROMPTS = []
CHOSEN_PROMPT = "Start writing!"

class DisappearText:
    def __init__(self):
        # --------------------------Main Window-----------------#
        self.screen = Tk()
        self.screen.title("Disappearing Text")
        self.screen.minsize(500, 600)
        self.screen.geometry("600x700")

        self.canvas = Canvas(self.screen, width=600, height=700, bg=CREAM_WHITE)
        self.canvas.pack()

        self.upper_text = self.canvas.create_text(300, 40, text="", font=LITTLE_FONT, fill=DARK_GREEN, justify="left", width=500)
        self.center_text = self.canvas.create_text(300, 230, text="Disappearing\nText", font=BIG_FONT, fill=DARK_GREEN,
                                         justify="center", width=550)
        self.number_text = self.canvas.create_text(300, 600, text="", font=BIG_FONT, fill=DARK_GREEN, justify="center")
        self.start_button = RoundedButton(master=self.canvas,
                                     text="Start",
                                     radius=50,
                                     btnbackground=BUTTON_UNCLICK,
                                     btnforeground=BUTTON_CLICK,
                                     clicked=self.start)
        self.start_frame = self.canvas.create_window(360, 470, window=self.start_button)
        self.prompt_button = RoundedButton(master=self.canvas,
                                      text="Generate\nPrompt",
                                      radius=50,
                                      btnbackground=BUTTON_UNCLICK,
                                      btnforeground=BUTTON_CLICK,
                                      clicked=self.random_prompt)
        self.prompt_frame = self.canvas.create_window(360, 550, window=self.prompt_button)
        self.info_button = RoundedButton(master=self.canvas,
                                    text="Info",
                                    radius=50,
                                    btnbackground=BUTTON_CLICK,
                                    btnforeground=BUTTON_UNCLICK,
                                    clicked=self.info_page)
        self.info_frame = self.canvas.create_window(360, 650, window=self.info_button)
        self.save_button = RoundedButton(master=self.canvas,
                                         text="Save",
                                         radius=50,
                                         btnbackground=BUTTON_CLICK,
                                         btnforeground=BUTTON_UNCLICK,
                                         clicked=self.save_text,)
        self.save_frame = self.canvas.create_window(360, 650, window=self.save_button, state="hidden")
        self.frames = [self.start_frame, self.prompt_frame, self.info_frame, self.save_frame]
        self.buttons = [self.start_button, self.prompt_button, self.info_button, self.save_button]
        self.typing_box = Text(
            height=15,
            width=15,
            wrap='word',
            font=LITTLE_FONT,
        )
        self.typing_box.pack(side=LEFT, expand=True)
        sb = Scrollbar(self.typing_box)
        sb.pack(side=RIGHT, fill=BOTH)

        self.typing_box.config(yscrollcommand=sb.set)
        sb.config(command=self.typing_box.yview)

        self.type_box_window = self.canvas.create_window(300, 320, window=self.typing_box, height=450, width=500, state="hidden")
        self.game_loop = ""

        self.screen.mainloop()
#--------------------------Starting self.screen----------------------#
    def writing(self, event):
        self.typing_box.unbind_all("<Key>")
        countdown = 5
        timer = 300
        current_text = self.typing_box.get("1.0", END)
        self.start_timer(current_text, countdown, timer)
    def start_timer(self, current_text, countdown, timer):
        if countdown == 0 or timer == 0:
            self.end_game(countdown)
        else:
            if current_text == self.typing_box.get("1.0", END):
                countdown -= 1
            else:
                countdown = 5
            current_text = self.typing_box.get("1.0", END)
            self.canvas.itemconfig(self.number_text, text=countdown)
            self.game_loop = self.screen.after(1000, self.start_timer, current_text, countdown, timer -1)
    def end_game(self, countdown):
        global CHOSEN_PROMPT
        self.screen.after_cancel(self.game_loop)
        self.canvas.itemconfig(self.type_box_window, state="hidden")
        self.typing_box.config(state="disabled")
        self.canvas.itemconfig(self.upper_text, text="")
        CHOSEN_PROMPT = "Start Writing!"
        self.canvas.itemconfig(self.number_text, text="")
        for button in self.buttons[0:2]:
            button.config(state="normal")
        for frame in self.frames[0:2]:
            self.canvas.itemconfig(frame, state="normal")
        if countdown <= 0:
            self.canvas.itemconfig(self.center_text, text="You stopped typing! You lost all of your progress :(", font=BIG_FONT)
        else:
            self.canvas.itemconfig(self.center_text, text="You completed the challenge! Click 'Save' to save your writing.", font=BIG_FONT)
            self.buttons[3].config(state="normal")
            self.canvas.itemconfig(self.frames[3], state="normal")

    def save_text(self):
        file = filedialog.asksaveasfile(mode="w", defaultextension=".txt")
        if file is None:
            return
        text = self.typing_box.get("1.0", END)
        file.write(text)
        file.close()

    def start(self):
        for frame in self.frames:
            self.canvas.itemconfig(frame, state="hidden")
        for button in self.buttons:
            button.config(state="disabled")
        self.typing_box.config(state="normal")
        self.typing_box.delete("1.0", END)
        self.typing_box.bind_all("<Key>", self.writing)
        self.canvas.itemconfig(self.type_box_window, state="normal")
        self.canvas.itemconfig(self.center_text, text="")
        self.canvas.itemconfig(self.upper_text, text=CHOSEN_PROMPT)
    def random_prompt(self):
        global CHOSEN_PROMPT
        if PROMPTS == []:
            html = requests.get("https://education.yourdictionary.com/for-teachers/activities-lesson-plans/100-creative-writing-prompts-for-middle-school.html").text
            soup = BeautifulSoup(html, "html.parser")
            prompt = soup.find_all("li")
            for prompt in prompt[-104:-4]:
                PROMPTS.append(prompt.text)
        CHOSEN_PROMPT = random.choice(PROMPTS)
        self.canvas.itemconfig(self.center_text, text=CHOSEN_PROMPT, font=LITTLE_FONT)

    def info_page(self):
        self.canvas.itemconfig(self.center_text, text="Your goal is to write non-stop for five minutes or risk losing everything you've written. If you fail to write anything within a five second time frame, all of your typed text will be deleted! Keep writing and you will be able to save your progress for another day.", font=LITTLE_FONT)

text_game = DisappearText()
