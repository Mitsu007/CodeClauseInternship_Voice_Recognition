import tkinter as tk
from tkinter import filedialog, messagebox
import speech_recognition as sr
import os

class VoiceNotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Notes Application")
        
        self.current_file = None
        
        # UI Components
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text="Create New File", command=self.create_new_file, width=20).pack(pady=10)
        tk.Button(self.root, text="Open File", command=self.open_file, width=20).pack(pady=10)
        tk.Button(self.root, text="Save File", command=self.save_file, width=20).pack(pady=10)
        tk.Button(self.root, text="Start Voice Input", command=self.start_voice_input, width=20).pack(pady=10)
        
        self.text_area = tk.Text(self.root, wrap=tk.WORD, width=70, height=15)
        self.text_area.pack(pady=10)
        
        self.status_label = tk.Label(self.root, text="No file selected", fg="blue")
        self.status_label.pack(pady=5)

    def start_voice_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            messagebox.showinfo("Info", "Listening... Please speak now.")
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                self.text_area.insert(tk.END, text + "\n")
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Could not understand the audio.")
            except sr.RequestError:
                messagebox.showerror("Error", "Network error. Please check your connection.")

    def create_new_file(self):
        self.text_area.delete("1.0", tk.END)
        self.current_file = None
        self.update_status("New file created.")

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.current_file = file_path
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, content)
            self.update_status(f"Opened file: {os.path.basename(file_path)}")

    def save_file(self):
        if not self.current_file:
            self.current_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.text_area.get("1.0", tk.END).strip())
            self.update_status(f"File saved: {os.path.basename(self.current_file)}")
        else:
            messagebox.showwarning("Warning", "File not saved.")

    def update_status(self, message):
        self.status_label.config(text=message)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceNotesApp(root)
    app.run()