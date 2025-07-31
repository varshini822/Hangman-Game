import tkinter as tk
from tkinter import messagebox
import random

WORDS = ['elephant', 'giraffe', 'kangaroo', 'dolphin', 'penguin', 'alligator', 'chimpanzee', 'rhinoceros']

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Advanced Hangman Game")
        self.root.geometry("500x600")
        self.root.config(bg="#f5f5f5")
        self.word = random.choice(WORDS).lower()
        self.guessed = []
        self.attempts = 6

        self.setup_gui()
        self.update_display()
        self.draw_hangman()

    def setup_gui(self):
        tk.Label(self.root, text="🎯 Hangman", font=("Verdana", 30, "bold"), bg="#f5f5f5", fg="#333").pack(pady=10)

        self.canvas = tk.Canvas(self.root, width=250, height=250, bg="#ffffff", highlightthickness=2, highlightbackground="#ccc")
        self.canvas.pack(pady=10)

        self.word_label = tk.Label(self.root, font=("Courier", 24, "bold"), bg="#f5f5f5")
        self.word_label.pack(pady=10)

        input_frame = tk.Frame(self.root, bg="#f5f5f5")
        input_frame.pack()

        self.guess_entry = tk.Entry(input_frame, font=("Arial", 18), width=5, justify='center')
        self.guess_entry.grid(row=0, column=0, padx=5)
        self.guess_entry.bind("<Return>", self.check_guess)

        self.guess_button = tk.Button(input_frame, text="Guess", command=self.check_guess, font=("Arial", 14), bg="#4caf50", fg="white")
        self.guess_button.grid(row=0, column=1)

        self.status_label = tk.Label(self.root, text=f"Attempts Left: {self.attempts}", font=("Arial", 16), fg="red", bg="#f5f5f5")
        self.status_label.pack(pady=10)

        self.guessed_label = tk.Label(self.root, text="Guessed Letters: ", font=("Arial", 14), bg="#f5f5f5")
        self.guessed_label.pack(pady=5)

        self.restart_button = tk.Button(self.root, text="🔁 Play Again", command=self.reset_game, font=("Arial", 14), bg="#2196f3", fg="white")
        self.restart_button.pack(pady=10)
        self.restart_button.config(state=tk.DISABLED)

    def update_display(self):
        display = " ".join([letter if letter in self.guessed else "_" for letter in self.word])
        self.word_label.config(text=display)
        self.status_label.config(text=f"Attempts Left: {self.attempts}")
        self.guessed_label.config(text="Guessed Letters: " + ", ".join(self.guessed).upper())

    def check_guess(self, event=None):
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)

        if not guess or len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a single alphabet letter.")
            return

        if guess in self.guessed:
            messagebox.showinfo("Already Guessed", f"You already guessed '{guess}'.")
            return

        self.guessed.append(guess)

        if guess not in self.word:
            self.attempts -= 1

        self.update_display()
        self.draw_hangman()

        if all(letter in self.guessed for letter in self.word):
            messagebox.showinfo("🎉 You Win!", f"The word was '{self.word}'. Well done!")
            self.end_game()
        elif self.attempts == 0:
            messagebox.showerror("💀 Game Over", f"You lost! The word was '{self.word}'.")
            self.end_game()

    def draw_hangman(self):
        self.canvas.delete("all")
        self.canvas.create_line(20, 230, 180, 230)  # Base
        self.canvas.create_line(50, 230, 50, 20)    # Pole
        self.canvas.create_line(50, 20, 150, 20)    # Beam
        self.canvas.create_line(150, 20, 150, 50)   # Rope

        parts = 6 - self.attempts

        if parts >= 1:
            self.canvas.create_oval(130, 50, 170, 90)  # Head
        if parts >= 2:
            self.canvas.create_line(150, 90, 150, 150)  # Body
        if parts >= 3:
            self.canvas.create_line(150, 100, 120, 130)  # Left Arm
        if parts >= 4:
            self.canvas.create_line(150, 100, 180, 130)  # Right Arm
        if parts >= 5:
            self.canvas.create_line(150, 150, 130, 190)  # Left Leg
        if parts >= 6:
            self.canvas.create_line(150, 150, 170, 190)  # Right Leg

    def end_game(self):
        self.guess_entry.config(state=tk.DISABLED)
        self.guess_button.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.NORMAL)

    def reset_game(self):
        self.word = random.choice(WORDS).lower()
        self.guessed = []
        self.attempts = 6
        self.guess_entry.config(state=tk.NORMAL)
        self.guess_button.config(state=tk.NORMAL)
        self.restart_button.config(state=tk.DISABLED)
        self.update_display()
        self.draw_hangman()

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
