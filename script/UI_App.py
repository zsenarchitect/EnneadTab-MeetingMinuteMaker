

import MeetingMinutesMaker as MMM
import AI_Logic
import tkinter as tk


class App:
    def __init__(self):
        self.solution = AI_Logic.Logic_Solution()
        self.window = tk.Tk()
        self.window.title(MMM.EXE_NAME)
        self.is_thinking = False
        self.x = 900
        self.y = 700

        self.window_width = 550
        self.window_height = 120
        # 100x100 size window, location 700, 500. No space between + and numbers
        self.window.geometry("{}x{}+{}+{}".format(self.window_width,
                                                  self.window_height,
                                                  self.x,
                                                  self.y))

        self.main_label_bubble = tk.Label(self.window, text="Ennead Meeting Minute Maker!", font=(
            "Comic Sans MS", 18), borderwidth=3, relief="solid")
        # pady ====> pad in Y direction
        self.main_label_bubble.pack(pady=15)

        self.window.after(1, self.update)

    def update(self):
        self.window.after(1000, self.check_job)

    def check_job(self):
        if not self.is_thinking and self.solution.has_new_job():
            self.is_thinking = True
            self.main_label_bubble.configure(text="Thinking...")
            self.solution.main()
            self.is_thinking = False
            self.main_label_bubble.configure(text="Ready to work.")
            print("done!")
           
        self.window.after(1, self.update)

    def run(self):
        self.window.mainloop()

