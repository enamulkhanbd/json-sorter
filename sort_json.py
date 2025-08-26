import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# ----------------------------
# Recursive sort function
# ----------------------------
def sort_dict(d):
    if isinstance(d, dict):
        return {k: sort_dict(d[k]) for k in sorted(d.keys())}
    elif isinstance(d, list):
        return [sort_dict(i) for i in d]
    else:
        return d

# ----------------------------
# Browse JSON/TXT file
# ----------------------------
def open_file():
    file_path = filedialog.askopenfilename(
        title="Select JSON or TXT file",
        filetypes=[("JSON/TXT files", "*.json *.txt"), ("All files", "*.*")]
    )
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

# ----------------------------
# Convert & Save (Prettier-like)
# ----------------------------
def convert_file():
    try:
        file_path = entry_file.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file first.")
            return

        # Load JSON
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Sort recursively
        sorted_data = sort_dict(data)

        # Prefill Save As dialog with original filename
        default_name = os.path.basename(file_path)
        save_path = filedialog.asksaveasfilename(
            title="Save Sorted & Beautified JSON",
            initialfile=default_name,
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if save_path:
            # Beautify JSON like Prettier
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(
                    json.dumps(
                        sorted_data,
                        indent=2,            # Prettier-like indentation
                        ensure_ascii=False,  # Keep Unicode characters
                        separators=(',', ': ') # Consistent spacing
                    ) + "\n"                 # Add newline at the end (Prettier style)
                )

            messagebox.showinfo("Success", f"Sorted & Beautified JSON saved to:\n{save_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ----------------------------
# UI Setup (Centered)
# ----------------------------
root = tk.Tk()
root.title("JSON Sorter & Beautifier")

# Window size
window_width = 500
window_height = 150

# Center window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.resizable(False, False)

# Frame
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# Label
label = tk.Label(frame, text="Select JSON/TXT file:")
label.grid(row=0, column=0, sticky="w")

# Entry
entry_file = tk.Entry(frame, width=50)
entry_file.grid(row=1, column=0, padx=5, pady=5)

# Browse button
btn_browse = tk.Button(frame, text="Browse", command=open_file)
btn_browse.grid(row=1, column=1, padx=5)

# Convert & Save button
btn_convert = tk.Button(frame, text="Convert & Save", command=convert_file, bg="lightblue")
btn_convert.grid(row=2, column=0, columnspan=2, pady=10)

# Run the Tkinter main loop
root.mainloop()
