import tkinter as tk
from tkinter import messagebox
import time
from PIL import Image, ImageTk

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
        self.root.geometry("800x500")
        self.root.configure(bg="#121212")

        self.canvas = tk.Canvas(root, width=780, height=250, highlightthickness=0)
        self.canvas.pack(pady=10)

        for i in range(0, 250, 5):
            color = f'#{int(18 + i/3):02x}{int(18 + i/4):02x}{int(18 + i/2):02x}'
            self.canvas.create_rectangle(0, i, 780, i + 5, fill=color, outline=color)

        self.energy_label = tk.Label(root, text="", font=("Helvetica", 14), fg="red", bg="#121212")
        self.energy_label.pack()

        self.flower_label = tk.Label(root, text="", font=("Helvetica", 14), fg="lime", bg="#121212")
        self.flower_label.pack()

        self.timer_label = tk.Label(root, text="", font=("Helvetica", 12), fg="cyan", bg="#121212")
        self.timer_label.pack()

        self.question_label = tk.Label(root, text="", font=("Helvetica", 14), fg="white", bg="#121212")
        self.question_label.pack(pady=5)

        self.entry = tk.Entry(root, font=("Helvetica", 14), justify="center")
        self.entry.pack(pady=5)

        self.submit_button = tk.Button(root, text="💥 ATTACK 💥", font=("Helvetica", 12, "bold"),
                                       command=self.check_answer, bg="#ff69b4", fg="white", relief="raised", padx=10, pady=5)
        self.submit_button.pack(pady=5)

        self.feedback_label = tk.Label(root, text="", font=("Helvetica", 12), fg="skyblue", bg="#121212")
        self.feedback_label.pack()

        self.reset_game()

    def reset_game(self):
        self.zombie_energy = 20
        self.flower_energy = 5
        self.current_question = 0
        self.canvas.delete("zombie")
        self.canvas.delete("flower")

        self.zombie_parts = []
        self.draw_flower()
        self.draw_zombie()

        self.energy_label.config(text=f"🧛 Zombie Energy: {self.zombie_energy}")
        self.flower_label.config(text=f"🌸 Flower Energy: {self.flower_energy}")
        self.feedback_label.config(text="")
        self.timer_label.config(text="")
        self.entry.config(state="normal")
        self.submit_button.config(state="normal")

        self.update_question()

    def draw_flower(self):
        self.canvas.create_line(65, 190, 65, 250, fill="green", width=6, tags="flower")
        self.canvas.create_oval(55, 220, 75, 230, fill="green", outline="", tags="flower")
        self.canvas.create_oval(60, 230, 80, 240, fill="green", outline="", tags="flower")

        petal_coords = [
            (45, 155, 65, 175),
            (65, 155, 85, 175),
            (55, 145, 75, 165),
            (55, 165, 75, 185),
        ]
        for x0, y0, x1, y1 in petal_coords:
            self.canvas.create_oval(x0, y0, x1, y1, fill="pink", outline="", tags="flower")

        self.canvas.create_oval(55, 155, 75, 175, fill="yellow", outline="", tags="flower")

    def draw_zombie(self):
        x_offset = -280
        parts = []
        parts.append(self.canvas.create_rectangle(580 + x_offset, 150, 630 + x_offset, 200, fill="#7fffd4", outline="", tags="zombie"))  # head
        parts.append(self.canvas.create_oval(590 + x_offset, 160, 595 + x_offset, 165, fill="black", tags="zombie"))  # eye
        parts.append(self.canvas.create_oval(615 + x_offset, 160, 620 + x_offset, 165, fill="black", tags="zombie"))  # eye
        parts.append(self.canvas.create_line(590 + x_offset, 180, 620 + x_offset, 180, fill="black", width=2, tags="zombie"))  # mouth
        parts.append(self.canvas.create_rectangle(590 + x_offset, 200, 620 + x_offset, 250, fill="#7fffd4", outline="", tags="zombie"))  # body
        parts.append(self.canvas.create_line(590 + x_offset, 210, 570 + x_offset, 230, fill="#7fffd4", width=4, tags="zombie"))  # arm
        parts.append(self.canvas.create_line(620 + x_offset, 210, 640 + x_offset, 230, fill="#7fffd4", width=4, tags="zombie"))  # arm
        parts.append(self.canvas.create_line(595 + x_offset, 250, 595 + x_offset, 280, fill="#7fffd4", width=4, tags="zombie"))  # leg
        parts.append(self.canvas.create_line(615 + x_offset, 250, 615 + x_offset, 280, fill="#7fffd4", width=4, tags="zombie"))  # leg
        self.zombie_parts.extend(parts)

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
            self.canvas.move("zombie", -5, 0)
            self.root.update()
            time.sleep(0.02)

    def flower_attack_animation(self):
        for _ in range(3):
            self.canvas.move("flower", 5, 0)
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
            self.canvas.itemconfig("zombie", fill="gray")
            self.energy_label.config(text="💀 Zombie Defeated!")
            self.feedback_label.config(text="🏆 YOU WIN!")
            messagebox.showinfo("Victory", "The giant zombie has been destroyed!")
        else:
            self.canvas.itemconfig("flower", fill="gray")
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
