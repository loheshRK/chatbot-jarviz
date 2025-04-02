import os
import google.generativeai as genai
from dotenv import load_dotenv
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    messagebox.showerror("Error", "API key is missing! Please check your .env file.")
    exit(1)

# Configure the Gemini API
genai.configure(api_key=api_key)

# Custom AI personality
AI_PERSONALITY = "You are a friendly and helpful assistant. Always respond in a conversational and engaging tone."

# Initialize model
def initialize_chat():
    global chat_session
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        system_instruction=AI_PERSONALITY,
    )
    chat_session = model.start_chat(history=[])

initialize_chat()

# Save chat history
CHAT_HISTORY_FILE = "chat_history.txt"

def save_chat_history(user_text, bot_response):
    """Save the chat history to a file"""
    with open(CHAT_HISTORY_FILE, "a", encoding="utf-8") as file:
        file.write(f"You: {user_text}\nBot: {bot_response}\n\n")

# GUI Functions
def new_chat():
    """Clear chat and start fresh conversation"""
    chat_box.config(state=tk.NORMAL)
    chat_box.delete(1.0, tk.END)
    initialize_chat()
    chat_box.insert(tk.END, "How can I help you today?\n\n", "bot")
    chat_box.config(state=tk.DISABLED)
    chat_box.yview(tk.END)

def send_message():
    """Handles user input and chatbot response"""
    user_text = entry.get()
    if not user_text.strip():
        return

    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, f"You: {user_text}\n", "user")
    entry.delete(0, tk.END)

    try:
        response = chat_session.send_message(user_text)
        bot_response = response.text
        chat_box.insert(tk.END, f"Jarviz: {bot_response}\n\n", "bot")
        save_chat_history(user_text, bot_response)
    except Exception as e:
        messagebox.showerror("Error", f"Chatbot error: {e}")

    chat_box.config(state=tk.DISABLED)
    chat_box.yview(tk.END)

# GUI Setup
root = tk.Tk()
root.title("Jarviz Chat")
root.geometry("800x600")
root.configure(bg="#161616")

# Main Container
main_frame = tk.Frame(root, bg="#161616")
main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

# Centered Welcome Message
welcome_frame = tk.Frame(main_frame, bg="#161616")
welcome_frame.pack(expand=True, fill=tk.BOTH)

tk.Label(welcome_frame, 
        text="Hi, I'm Jarviz",
        font=("Arial", 24, "bold"),
        bg="#161616",
        fg="#00A7E1").pack(pady=10)



# Chat Area Container
chat_container = tk.Frame(main_frame, bg="#161616")
chat_container.pack(expand=True, fill=tk.BOTH)

# New Chat Button Row
button_frame = tk.Frame(chat_container, bg="#161616")
button_frame.pack(fill=tk.X, pady=10)

tk.Button(button_frame, 
         text="New Chat",
         command=new_chat,
         bg="#2C2C2C",
         fg="white",
         font=("Arial", 10, "bold"),
         relief=tk.FLAT).pack(side=tk.RIGHT)

# Chat Display
chat_box = scrolledtext.ScrolledText(chat_container, 
                                    wrap=tk.WORD,
                                    font=("Arial", 12),
                                    bg="#2C2C2C",
                                    fg="white",
                                    bd=0,
                                    padx=20,
                                    pady=20,
                                    state=tk.DISABLED)
chat_box.pack(expand=True, fill=tk.BOTH)

# Initial Message
chat_box.config(state=tk.NORMAL)
chat_box.insert(tk.END, "How can I help you today?\n\n", "bot")
chat_box.tag_config("user", foreground="#00FF88")
chat_box.tag_config("bot", foreground="#00A7E1")
chat_box.config(state=tk.DISABLED)

# Input Area
input_frame = tk.Frame(main_frame, bg="#161616")
input_frame.pack(fill=tk.X, pady=10)

entry = tk.Entry(input_frame, 
                bg="#2C2C2C",
                fg="white",
                font=("Arial", 12),
                bd=0,
                insertbackground="white")
entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

send_btn = tk.Button(input_frame, 
                    text="→",
                    bg="#00A7E1",
                    fg="white",
                    font=("Arial", 12, "bold"),
                    relief=tk.FLAT,
                    command=send_message)
send_btn.pack(side=tk.RIGHT, padx=2)

entry.bind("<Return>", lambda event: send_message())

# Run the GUI
root.mainloop()