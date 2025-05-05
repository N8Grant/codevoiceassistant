import tkinter as tk
import itertools
import threading
import queue
from config import END_PHRASE


class ListeningOverlay:
    def __init__(self):
        self.root = None
        self.label = None
        self.text_display = None
        self.spinner = itertools.cycle(
            ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        )
        self.running = False
        self.queue = queue.Queue()
        self.thread = None
        self.manual_end = False

    def show(self):
        def run():
            self.root = tk.Tk()
            self.root.overrideredirect(True)
            self.root.attributes("-topmost", True)
            self.root.geometry("800x300+300+200")
            self.root.configure(bg="black")
            self.root.attributes("-alpha", 0.85)

            frame = tk.Frame(self.root, bg="black")
            frame.place(relx=0.5, rely=0.4, anchor="center")

            self.label = tk.Label(
                frame,
                text=f"🎤 Listening...\nSay '{END_PHRASE}' to finish.",
                fg="white",
                bg="black",
                font=("Helvetica", 24),
            )
            self.label.pack(pady=10)

            self.text_display = tk.Label(
                frame,
                text="",
                fg="lightgreen",
                bg="black",
                font=("Helvetica", 16),
                wraplength=800,
                justify="center",
            )
            self.text_display.pack()

            done_button = tk.Button(
                frame,
                text="✅ Done",
                command=self._done_clicked,
                font=("Helvetica", 14),
                bg="green",
                fg="white",
                padx=20,
                pady=10,
            )
            done_button.pack(pady=(10, 0))

            self.running = True
            self._animate_spinner()
            self._process_queue()
            self.root.mainloop()

            # Clean shutdown
            try:
                self.root.destroy()
            except Exception:
                pass
            self.root = None
            self.running = False

        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()

    def _animate_spinner(self):
        if not self.running or not self.label or not self.label.winfo_exists():
            return
        spinner_char = next(self.spinner)
        try:
            self.label.config(
                text=f"🎤 Listening {spinner_char}\nSay '{END_PHRASE}' to finish or click ✅"
            )
            self.root.after(150, self._animate_spinner)
        except tk.TclError:
            pass

    def _done_clicked(self):
        self.queue.put(("manual_end", None))

    def _process_queue(self):
        try:
            while True:
                msg, _ = self.queue.get_nowait()
                if msg == "manual_end":
                    self.manual_end = True
                    if self.root:
                        self.root.quit()
                elif msg == "quit" and self.root:
                    self.root.quit()
        except queue.Empty:
            pass

        if self.running:
            self.root.after(100, self._process_queue)

    def update_transcript(self, partial_text):
        if self.text_display:
            self.queue.put(("update_text", partial_text))

    def hide(self):
        self.running = False
        if self.root:
            self.queue.put(("quit", None))
