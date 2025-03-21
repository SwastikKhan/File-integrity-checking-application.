import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox

# (Optional) This line helps Replit use its built-in X server:
if os.getenv("REPL_ID"):
    os.environ["DISPLAY"] = ":0"

def calculate_file_hash(filepath):
    hash_sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def select_files():
    file_paths = filedialog.askopenfilenames(title="Select Files")
    file_list = list(file_paths)
    if file_list:
        file_label.config(text="\n".join(file_list))
    return file_list

def compute_baseline():
    files = select_files()
    if not files:
        messagebox.showerror("Error", "No files selected!")
        return
    with open("baseline.txt", "w") as baseline_file:
        for filepath in files:
            file_hash = calculate_file_hash(filepath)
            baseline_file.write(f"{filepath}|{file_hash}\n")
    messagebox.showinfo("Success", "Baseline computed and saved!")

def check_integrity():
    if not os.path.exists("baseline.txt"):
        messagebox.showerror("Error", "Baseline not found! Compute baseline first.")
        return
    with open("baseline.txt", "r") as baseline_file:
        baseline_data = {}
        for line in baseline_file:
            path, hash_val = line.strip().split("|")
            baseline_data[path] = hash_val
    changes = []
    for filepath, old_hash in baseline_data.items():
        if os.path.exists(filepath):
            current_hash = calculate_file_hash(filepath)
            if current_hash != old_hash:
                changes.append(f"Modified: {filepath}")
        else:
            changes.append(f"Deleted: {filepath}")
    if changes:
        messagebox.showwarning("Integrity Alert", "\n".join(changes))
    else:
        messagebox.showinfo("Integrity Check", "All files are unchanged.")

# Set up the GUI
root = tk.Tk()
root.title("File Integrity Checker")

file_label = tk.Label(root, text="No files selected", wraplength=400)
file_label.pack(pady=10)

baseline_button = tk.Button(root, text="Compute Baseline", command=compute_baseline)
baseline_button.pack(pady=5)

check_button = tk.Button(root, text="Check Integrity", command=check_integrity)
check_button.pack(pady=5)

root.mainloop()
