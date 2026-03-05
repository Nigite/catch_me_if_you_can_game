import math
import random
import tkinter as tk


class CatchMeGame:
    """
    A simple evasion game built with Tkinter.
    The button evades the user's cursor, with difficulty scaling per level.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Catch Me If You Can!")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.current_level = 1
        self.max_level = 5
        self.trigger_distances = {
            1: 50,
            2: 75,
            3: 90,
            4: 135,
            5: 190
        }
        
        self._setup_ui()
        self._bind_events()

    def _setup_ui(self):
        """Initializes the labels and the evasive button."""
        self.level_label = tk.Label(
            self.root, 
            text=f"Level: {self.current_level} / {self.max_level}", 
            font=("Arial", 16, "bold")
        )

        self.level_label.pack(pady=10)
        self.catch_button = tk.Button(
            self.root, 
            text="Catch Me!", 
            font=("Arial", 14, "bold"),
            bg="lightblue",
            command=self._on_button_click
        )
        
        self.root.update_idletasks()
        self.catch_button.place(x=250, y=200)

    def _bind_events(self):
        """Binds window events to their respective handler methods."""
        self.root.bind('<Motion>', self._on_mouse_motion)

    def _on_mouse_motion(self, event):
        """Calculates distance between cursor and button on every mouse movement."""
        if self.current_level > self.max_level:
            return 

        mouse_x = event.x
        mouse_y = event.y

        btn_x = self.catch_button.winfo_x()
        btn_y = self.catch_button.winfo_y()
        btn_w = self.catch_button.winfo_width()
        btn_h = self.catch_button.winfo_height()

        center_x = btn_x + (btn_w / 2)
        center_y = btn_y + (btn_h / 2)

        distance = math.sqrt((mouse_x - center_x)**2 + (mouse_y - center_y)**2)

        current_threshold = self.trigger_distances[self.current_level]
        
        if distance < current_threshold:
            self._teleport_button(btn_w, btn_h)

    def _teleport_button(self, btn_w, btn_h):
        """Moves the button to a random coordinate within the window boundaries."""
        max_x = self.root.winfo_width() - btn_w
        max_y = self.root.winfo_height() - btn_h
        if max_x <= 0 or max_y <= 0:
            return

        new_x = random.randint(0, max_x)
        new_y = random.randint(50, max_y)  
        self.catch_button.place(x=new_x, y=new_y)

    def _on_button_click(self):
        """Handles the logic for progressing to the next level."""
        if self.current_level < self.max_level:
            self.current_level += 1
            self.level_label.config(text=f"Level: {self.current_level} / {self.max_level}")
            new_font_size = max(6, 20 - (self.current_level * 2))
            
            self.catch_button.config(
                text=f"Catch me! Lvl {self.current_level}!", 
                font=("Arial", new_font_size, "bold"),
                bg="salmon"
            )
            
            self.root.update_idletasks()
            self._teleport_button(self.catch_button.winfo_width(), self.catch_button.winfo_height())
        else:
            self._win_game()

    def _win_game(self):
        """Handles the victory state."""
        self.current_level += 1
        self.level_label.config(text="IMPOSSIBLE! YOU BEAT LEVEL 5!", fg="green")
        
        self.catch_button.config(
            text="Play Again?", 
            font=("Arial", 16, "bold"),
            bg="lightgreen", 
            command=self._restart_game
        )
        
        self.catch_button.place(x=230, y=200)

    def _restart_game(self):
        """Resets all UI and state variables back to Level 1."""
        self.current_level = 1
        
        self.level_label.config(
            text=f"Level: {self.current_level} / {self.max_level}", 
            fg="black"
        )
        
        self.catch_button.config(
            text="Catch Me!", 
            font=("Arial", 14, "bold"),
            bg="lightblue",
            command=self._on_button_click
        )
        
        self.root.update_idletasks()
        self.catch_button.place(x=250, y=200)

if __name__ == "__main__":
    main_window = tk.Tk()
    game_instance = CatchMeGame(main_window)
    main_window.mainloop()