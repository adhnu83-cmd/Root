import datetime
import random
import os
import time
import difflib
import tkinter as tk
from tkinter import simpledialog, messagebox

TODO_FILE = "root_todos.txt"
NOTES_FILE = "root_notes.txt"
REMIND_FILE = "root_reminders.txt"
HISTORY_FILE = "root_calc_history.txt"
DIARY_FILE = "root_diary.txt"
BACKUP_FILE = "root_auto_backup.txt"

def load_from_file(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

def save_to_file(filename, data_list):
    with open(filename, "w", encoding="utf-8") as f:
        for item in data_list:
            f.write(item + "\n")

todo_list = load_from_file(TODO_FILE)
notes_list = load_from_file(NOTES_FILE)
reminders_list = load_from_file(REMIND_FILE)
calc_history = load_from_file(HISTORY_FILE)
diary_list = load_from_file(DIARY_FILE)

current_mood = "boss"
current_lang = "ml"
current_password = "rootroot"  # ഡിഫോൾട്ട് പാസ്‌വേർഡ്
quiz_score = 0

quiz_data = [
    ("സൗരയൂഥത്തിലെ ഏറ്റവും വലിയ ഗ്രഹം ഏതാണ്?", "വ്യാഴം"),
    ("ഇന്ത്യയുടെ ദേശീയ മൃഗം ഏതാണ്?", "കടുവ"),
    ("പൈത്തൺ എന്താണ്?", "പ്രോഗ്രാമിംഗ് ഭാഷ"),
    ("കേരളത്തിന്റെ തലസ്ഥാനം ഏതാണ്?", "തിരുവനന്തപുരം")
]

def auto_backup_data():
    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        f.write("=== ROOT AUTO BACKUP ===\n")
        f.write(f"Timestamp: {datetime.datetime.now()}\n\n")

def match_command(user_input, valid_commands):
    match = difflib.get_close_matches(user_input, valid_commands, n=1, cutoff=0.6)
    if match:
        return match[0]
    return user_input

class RootAppWithPassword:
    def __init__(self, root):
        self.root = root
        self.root.title("ROOT - Secure App")
        self.root.geometry("400x600")
        self.root.configure(bg="#1e1e1e")

        # ആദ്യം പാസ്‌വേർഡ് ചോദിക്കുന്നു
        if not self.check_password():
            self.root.destroy()
            return

        # Top Title Header
        self.header_label = tk.Label(root, text="ROOT ASSISTANT", bg="#1e1e1e", fg="#00ff66", font=("Arial", 14, "bold"))
        self.header_label.pack(fill=tk.X, pady=10)

        # Bottom Input Box Frame (Fixed at the very bottom)
        self.bottom_frame = tk.Frame(root, bg="#2d2d2d", height=50)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Send Button
        self.send_button = tk.Button(self.bottom_frame, text="Send", bg="#00ff66", fg="#000000", font=("Arial", 10, "bold"), command=self.process_input)
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Typing Entry Box (At the bottom)
        self.entry_box = tk.Entry(self.bottom_frame, bg="#3d3d3d", fg="#ffffff", font=("Arial", 12), insertbackground="white", bd=0)
        self.entry_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=8)
        self.entry_box.bind("<Return>", self.process_input)

        # Chat Display Area
        self.chat_display = tk.Text(root, wrap=tk.WORD, bg="#121212", fg="#ffffff", font=("Arial", 11), bd=0, highlightthickness=0)
        self.chat_display.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)

        self.speak_style("പാസ്‌വേർഡ് ശരിയാണ്! സ്വാഗതം ബോസ്!", "Password correct! Welcome Boss!")

    def check_password(self):
        global current_password
        # Tkinter സിമ്പിൾ ഡയലോഗ് വഴി പാസ്‌വേർഡ് ചോദിക്കുന്നു
        pwd = simpledialog.askstring("Security Check", "Enter Root Password:", show="*")
        if pwd == current_password:
            return True
        else:
            messagebox.showerror("Access Denied", "Wrong Password! Closing App.")
            return False

    def speak_style(self, text, english_text=""):
        global current_mood, current_lang
        msg = english_text if (current_lang == "en" and english_text) else text
        
        self.chat_display.config(state=tk.NORMAL)
        if current_mood == "sir":
            self.chat_display.insert(tk.END, f"\n[ROOT - Sir]: {msg}, Sir.\n")
        elif current_mood == "friend":
            self.chat_display.insert(tk.END, f"\n[ROOT - Friend]: Hey, {msg}!\n")
        elif current_mood == "motivator":
            self.chat_display.insert(tk.END, f"\n[ROOT - Motivator]: {msg} Keep going!\n")
        else:
            self.chat_display.insert(tk.END, f"\n[ROOT - Boss]: {msg}, Boss.\n")
            
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def append_user(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\nYou: {message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def process_input(self, event=None):
        global current_lang, current_mood, quiz_score
        raw_command = self.entry_box.get().strip().lower()
        if not raw_command:
            return

        self.append_user(raw_command)
        self.entry_box.delete(0, tk.END)

        valid_cmds = ['exit', 'quit', 'bye', 'lang en', 'lang ml', 'time', 'health', 'list all', 
                      'add todo', 'show todos', 'add note', 'show notes', 'quiz',
                      'സുഖമാണോ', 'ഹലോ', 'hi', 'hello']

        command = match_command(raw_command, valid_cmds)

        if 'exit' in command or 'quit' in command or 'bye' in command:
            auto_backup_data()
            self.speak_style("ഞാൻ ഓഫാകുകയാണ്!", "Shutting down!")
            self.root.after(1000, self.root.destroy)

        elif command == 'lang en':
            current_lang = "en"
            self.speak_style("Switched language to English.", "Switched language to English.")
        elif command == 'lang ml':
            current_lang = "ml"
            self.speak_style("ഭാഷ മലയാളത്തിലേക്ക് മാറ്റിയിരിക്കുന്നു.", "Language switched to Malayalam.")

        elif command in ['സുഖമാണോ', 'how are you']:
            self.speak_style("ഞാൻ വളരെ സുഖമായിരിക്കുന്നു", "I am doing great")
        elif command in ['ഹലോ', 'hi', 'hello']:
            self.speak_style("ഇന്ന് ഞാൻ നിങ്ങൾക്ക് എന്ത് സഹായമാണ് ചെയ്തു തരേണ്ടത്?", "How can I help you today?")
            
        elif 'സമയം' in command or 'time' in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.speak_style(f"ഇപ്പോൾ സമയം {now} ആണ്", f"Current time is {now}")

        elif 'health' in command or 'സ്റ്റാറ്റസ്' in command:
            self.speak_style("സിസ്റ്റം ഹെൽത്ത്: 100% പെർഫെക്റ്റ്!", "System Health: 100% Perfect!")

        elif 'list all' in command:
            self.speak_style(f"നോട്ട്സ്: {len(notes_list)} | ടോഡോസ്: {len(todo_list)}", f"Notes: {len(notes_list)} | Todos: {len(todo_list)}")

        elif 'add todo' in raw_command:
            todo = raw_command.replace('add todo', '').strip()
            if todo:
                todo_list.append(todo)
                save_to_file(TODO_FILE, todo_list)
                self.speak_style("ജോലി സേവ് ചെയ്തു", "Todo saved")
            else:
                self.speak_style("ജോലി നൽകൂ", "Provide todo")
                
        elif 'show todos' in command:
            if todo_list:
                self.speak_style(', '.join(todo_list), ', '.join(todo_list))
            else:
                self.speak_style("ടു-ഡു ഇല്ല", "No todos")

        elif 'add note' in raw_command:
            note = raw_command.replace('add note', '').strip()
            if note:
                notes_list.append(note)
                save_to_file(NOTES_FILE, notes_list)
                self.speak_style("നോട്ട് സേവ് ചെയ്തു", "Note saved")
            else:
                self.speak_style("നോട്ട് നൽകൂ", "Provide note")
                
        elif 'show notes' in command:
            if notes_list:
                self.speak_style(', '.join(notes_list), ', '.join(notes_list))
            else:
                self.speak_style("നോട്ട്സ് ഇല്ല", "No notes")

        elif 'quiz' in command or 'ക്വിസ്' in command:
            q, a = random.choice(quiz_data)
            self.speak_style(f"ചോദ്യം: {q}", f"Question: {q}")
            ans = simpledialog.askstring("Quiz", q)
            if ans and a.lower() in ans.lower():
                quiz_score += 1
                self.speak_style(f"ശരിയാണ്! സ്കോർ: {quiz_score}", f"Correct! Score: {quiz_score}")
            else:
                self.speak_style(f"തെറ്റാണ്. ശരിയായ ഉത്തരം '{a}' ആണ്.", f"Wrong. Correct answer is '{a}'.")

        elif any(op in raw_command for op in ['+', '-', '*', '/']):
            try:
                result = eval(raw_command)
                calc_history.append(f"{raw_command} = {result}")
                save_to_file(HISTORY_FILE, calc_history)
                self.speak_style(f"ഉത്തരം: {result}", f"Result: {result}")
            except:
                self.speak_style("കണക്ക് തെറ്റാണ്", "Calculation error")
                
        else:
            self.speak_style(f"'{raw_command}' മനസ്സിലായില്ല.", f"'{raw_command}' not understood.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RootAppWithPassword(root)
    root.mainloop()
