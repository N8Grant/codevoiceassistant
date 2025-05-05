import tkinter as tk

def show_confirmation(original: str, refined: str = None):
    # Use existing root or create (but keep it hidden)
    root = tk._default_root
    if not root:
        root = tk.Tk()
        root.withdraw()

    popup = tk.Toplevel(root)
    popup.title("Prompt Captured")
    popup.geometry("800x400+400+200")
    popup.configure(bg="white")
    popup.attributes("-topmost", True)

    def close_popup():
        popup.destroy()

    if refined and original != refined:
        label = tk.Label(popup, text="✨ LLM-refined prompt", font=("Helvetica", 14, "bold"), bg="white", fg="green")
        label.pack(pady=(20, 5))

        refined_box = tk.Text(popup, height=6, wrap="word", font=("Helvetica", 12))
        refined_box.pack(padx=20, fill="both", expand=True)
        refined_box.insert("1.0", refined)
        refined_box.configure(state="disabled")

        separator = tk.Label(popup, text="🔁 Original spoken input", font=("Helvetica", 12, "italic"), bg="white", fg="gray")
        separator.pack(pady=(10, 5))

        original_box = tk.Text(popup, height=4, wrap="word", font=("Helvetica", 11))
        original_box.pack(padx=20, pady=(0, 10), fill="both", expand=False)
        original_box.insert("1.0", original)
        original_box.configure(state="disabled")
    else:
        label = tk.Label(popup, text="✅ Prompt copied to clipboard", font=("Helvetica", 14), bg="white", fg="green")
        label.pack(pady=(20, 10))

        text_box = tk.Text(popup, height=10, wrap="word", font=("Helvetica", 12))
        text_box.pack(padx=20, pady=(0, 20), fill="both", expand=True)
        text_box.insert("1.0", original)
        text_box.configure(state="disabled")

    close_btn = tk.Button(popup, text="Continue", command=close_popup,
                          font=("Helvetica", 12), bg="#4CAF50", fg="white", padx=20, pady=10)
    close_btn.pack(pady=10)

    # This keeps only the popup active until user closes it
    popup.grab_set()
    popup.wait_window()
