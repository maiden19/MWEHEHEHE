import tkinter as tk
from tkinter import messagebox
import time
from PIL import Image, ImageTk
import pygame

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("C:/MY USTP FILES/EN EN/background/background_music.mp3")
pygame.mixer.music.play(-1)

questions = [
    {"sentence": "The flower ___ the zombie.", "answer": "kills"},
    {"sentence": "The zombie has ___ energy.", "answer": "20"},
    {"sentence": "Words can ___ a zombie.", "answer": "kill"},
    {"sentence": "Typing speed is very ___.", "answer": "important"},
    {"sentence": "Grammar can ___ communication.", "answer": "improve"},
    {"sentence": "Zombies ___ at night.", "answer": "walk"},
    {"sentence": "The flower is very ___.", "answer": "strong"},
    {"sentence": "We must ___ fast.", "answer": "type"},
    {"sentence": "The zombie ___ scared.", "answer": "looks"},
    {"sentence": "The flower is ___ to attack.", "answer": "ready"},
    {"sentence": "English ___ used worldwide.", "answer": "is"},
    {"sentence": "You should ___ every question.", "answer": "answer"},
    {"sentence": "This game is ___ fun.", "answer": "really"},
    {"sentence": "Zombies can't ___ properly.", "answer": "think"},
    {"sentence": "Grammar rules must be ___.", "answer": "followed"},
    {"sentence": "Flowers can ___ damage.", "answer": "cause"},
    {"sentence": "The zombie is very ___.", "answer": "slow"},
    {"sentence": "Use the right ___.", "answer": "word"},
    {"sentence": "Zombies are not very ___.", "answer": "smart"},
    {"sentence": "The flower ___ brightly.", "answer": "glows"},
]

class ZombieGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 GRAMMAR GLADIATORS 🌸")
        self.root.geometry("1200x900")
        self.root.resizable(False, False)

        # Load background image
        bg_image = Image.open("C:/MY USTP FILES/EN EN/background/background_zombie.png").resize((1000, 1000))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Load flower and zombie images
        self.flower_img = ImageTk.PhotoImage(Image.open("C:/MY USTP FILES/EN EN/background/flower.png").resize((200, 200)))
        self.zombie_img = ImageTk.PhotoImage(Image.open("C:/MY USTP FILES/EN EN/background/zombies.png").resize((200, 200)))

        # Canvas
        self.canvas = tk.Canvas(root, width=5000, height=500, highlightthickness=0)
        self.canvas.pack()
        self.canvas_bg = self.canvas.create_image(0, 0, image=self.bg_photo, anchor='nw')

        self.energy_label = tk.Label(root, text="", font=("Helvetica", 14), fg="red", bg="#D3D3D3")
        self.energy_label.pack()

        self.flower_label = tk.Label(root, text="", font=("Helvetica", 14), fg="green", bg="#D3D3D3")
        self.flower_label.pack()

        self.timer_label = tk.Label(root, text="", font=("Helvetica", 12), fg="blue", bg="#D3D3D3")
        self.timer_label.pack()

        self.question_label = tk.Label(root, text="", font=("Helvetica", 14), fg="black", bg="#D3D3D3")
        self.question_label.pack(pady=5)

        self.entry = tk.Entry(root, font=("Helvetica", 14), justify="center")
        self.entry.pack(pady=5)

        self.submit_button = tk.Button(root, text="💥 ATTACK 💥", font=("Helvetica", 12, "bold"),
                                       command=self.check_answer, bg="#ff69b4", fg="white", relief="raised", padx=10, pady=5)
        self.submit_button.pack(pady=5)

        self.feedback_label = tk.Label(root, text="", font=("Helvetica", 12), fg="blue", bg="green")
        self.feedback_label.pack()

        self.reset_game()

    def reset_game(self):
        self.zombie_energy = 20
        self.flower_energy = 5
        self.current_question = 0
        self.canvas.delete("zombie")
        self.canvas.delete("flower")

        self.zombie_sprite = self.canvas.create_image(700, 220, image=self.zombie_img, anchor="center", tags="zombie")
        self.flower_sprite = self.canvas.create_image(85, 220, image=self.flower_img, anchor="center", tags="flower")

        self.energy_label.config(text=f"🧛 Zombie Energy: {self.zombie_energy}")
        self.flower_label.config(text=f"🌸 Flower Energy: {self.flower_energy}")
        self.feedback_label.config(text="")
        self.timer_label.config(text="")
        self.entry.config(state="normal")
        self.submit_button.config(state="normal")

        self.update_question()

    def update_question(self):
        if self.current_question < len(questions):
            q = questions[self.current_question]
            self.question_label.config(text=q["sentence"])
            self.entry.delete(0, tk.END)
            self.start_time = time.time()
        else:
            self.end_game(victory=True)

    def move_zombie_closer(self):
        for _ in range(10):
            self.canvas.move("zombie", -12, 0)
            self.root.update()
            time.sleep(0.02)

    def flower_attack_animation(self):
        for _ in range(3):
            self.canvas.move("flower", 9, 0)
            self.root.update()
            time.sleep(0.05)
        for _ in range(3):
            self.canvas.move("flower", -5, 0)
            self.root.update()
            time.sleep(0.05)

    def zombie_wobble(self):
        for dx in (-5, 5) * 2:
            self.canvas.move("zombie", dx, 0)
            self.root.update()
            time.sleep(0.05)

    def check_answer(self):
        user_input = self.entry.get().strip().lower()
        correct_answer = questions[self.current_question]["answer"].lower()
        elapsed = time.time() - self.start_time
        self.timer_label.config(text=f"⏱ Typing Time: {elapsed:.2f}s")

        if user_input == correct_answer:
            self.feedback_label.config(text="✅ Correct! Flower hits zombie.")
            self.flower_attack_animation()
            self.zombie_energy -= 5
            self.energy_label.config(text=f"🧛 Zombie Energy: {self.zombie_energy}")
            if self.zombie_energy <= 0:
                self.end_game(victory=True)
            else:
                self.current_question += 1
                self.update_question()
        else:
            self.flower_energy -= 1
            self.flower_label.config(text=f"🌸 Flower Energy: {self.flower_energy}")
            self.feedback_label.config(text="❌ Incorrect! Zombie moves closer.")
            self.zombie_wobble()
            self.move_zombie_closer()
            if self.flower_energy <= 0:
                self.end_game(victory=False)
            else:
                self.current_question += 1
                self.update_question()

    def end_game(self, victory):
        if victory:
            self.canvas.itemconfig("zombie", image="")  # Hide zombie image
            self.energy_label.config(text="💀 Zombie Defeated!")
            self.feedback_label.config(text="🏆 YOU WIN!")
            messagebox.showinfo("Victory", "The giant zombie has been destroyed!")
        else:
            self.canvas.itemconfig("flower", image="")  # Hide flower image
            self.flower_label.config(text="💀 Flower Eaten!")
            self.feedback_label.config(text="👽 The zombie ate the flower. GAME OVER.")
            messagebox.showwarning("Defeat", "The flower has been eaten by the zombie.")

        self.entry.config(state="disabled")
        self.submit_button.config(state="disabled")

        play_again = messagebox.askyesno("Play Again?", "Do you want to play again?")
        if play_again:
            self.reset_game()
        else:
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = ZombieGame(root)
    root.mainloop()
    pygame.mixer.music.stop()