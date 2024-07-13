import tkinter as tk
from tkinter import messagebox
import re
import math
import os

# Define the full path to the common passwords file
common_passwords_path = 'C:/Users/moham/OneDrive/Desktop/common_passwords.txt'

# Load common passwords
try:
    with open(common_passwords_path, 'r') as file:
        common_passwords = set(file.read().splitlines())
except FileNotFoundError:
    messagebox.showerror("File Not Found", f"The file {common_passwords_path} does not exist.")
    common_passwords = set()

# Function to check the strength of the password
def check_password_strength(password):
    length = len(password)
    complexity = 0
    feedback = []

    # Check length
    if length < 8:
        feedback.append("Password is too short, should be at least 8 characters.")
    else:
        complexity += 1
    
    # Check for uppercase, lowercase, digits, and special characters
    if re.search("[a-z]", password):
        complexity += 1
    else:
        feedback.append("Add lowercase letters for more strength.")
    
    if re.search("[A-Z]", password):
        complexity += 1
    else:
        feedback.append("Add uppercase letters for more strength.")
    
    if re.search("[0-9]", password):
        complexity += 1
    else:
        feedback.append("Add digits for more strength.")
    
    if re.search("[@#$%^&+=]", password):
        complexity += 1
    else:
        feedback.append("Add special characters (e.g., @#$%^&+=) for more strength.")
    
    # Check against common passwords
    if password in common_passwords:
        feedback.append("Password is too common.")
        complexity = 0
    
    # Entropy calculation
    pool = 0
    if re.search("[a-z]", password):
        pool += 26
    if re.search("[A-Z]", password):
        pool += 26
    if re.search("[0-9]", password):
        pool += 10
    if re.search("[@#$%^&+=]", password):
        pool += len("@#$%^&+=")
    
    entropy = length * math.log2(pool) if pool else 0

    # Evaluate overall strength
    if complexity == 0:
        strength = "Very Weak"
        color = "red"
    elif complexity == 1:
        strength = "Weak"
        color = "orange"
    elif complexity == 2:
        strength = "Moderate"
        color = "yellow"
    elif complexity == 3:
        strength = "Good"
        color = "lightgreen"
    elif complexity == 4:
        strength = "Strong"
        color = "green"
    elif complexity == 5:
        strength = "Very Strong"
        color = "darkgreen"
    
    return strength, color, feedback, entropy

# Function to display the strength of the password
def show_strength():
    password = entry.get()
    strength, color, feedback, entropy = check_password_strength(password)
    
    strength_text.set(f"Strength: {strength}")
    strength_label.config(fg=color)
    
    feedback_text.set("\n".join(feedback))
    entropy_text.set(f"Entropy: {entropy:.2f} bits")

# Initialize Tkinter window
root = tk.Tk()
root.title("Password Strength Checker")

# Create GUI components
tk.Label(root, text="Enter Password:").pack(pady=10)

entry = tk.Entry(root, show="*")
entry.pack(pady=10)

strength_text = tk.StringVar()
strength_label = tk.Label(root, textvariable=strength_text, font=("Helvetica", 12))
strength_label.pack(pady=10)

feedback_text = tk.StringVar()
feedback_label = tk.Label(root, textvariable=feedback_text, font=("Helvetica", 10), fg="red")
feedback_label.pack(pady=10)

entropy_text = tk.StringVar()
entropy_label = tk.Label(root, textvariable=entropy_text, font=("Helvetica", 10))
entropy_label.pack(pady=10)

check_button = tk.Button(root, text="Check Strength", command=show_strength)
check_button.pack(pady=10)

# Run the GUI loop
root.mainloop()
