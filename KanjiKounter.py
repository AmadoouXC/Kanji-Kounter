import tkinter as tk
from tkinter import filedialog
import os
import ebooklib
from ebooklib import epub
from collections import Counter
import re

def load_epub(file_path):
    book = epub.read_epub(file_path)
    text = ""

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            text += item.get_content().decode("utf-8")

    return text

def find_kanji(text):
    kanji_pattern = r'[\u4e00-\u9faf]'
    kanji_list = re.findall(kanji_pattern, text)
    return kanji_list

def analyze_kanji(kanji_list):
    kanji_counter = Counter(kanji_list)
    return kanji_counter

def analyze_and_display(epub_file_path):
    text = load_epub(epub_file_path)
    kanji_list = find_kanji(text)
    kanji_counter = analyze_kanji(kanji_list)

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Total Kanji characters: {len(kanji_list)}\n")
    result_text.insert(tk.END, f"Number of unique Kanji characters: {len(kanji_counter)}\n")
    result_text.insert(tk.END, "Kanji character frequency:\n")

    for kanji, count in kanji_counter.most_common():
        result_text.insert(tk.END, f"{kanji}: {count}\n")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("EPUB Files", "*.epub")])
    if file_path:
        epub_path_entry.delete(0, tk.END)
        epub_path_entry.insert(tk.END, file_path)

def analyze_button_click():
    epub_file_path = epub_path_entry.get()
    if os.path.exists(epub_file_path):
        analyze_and_display(epub_file_path)
    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Invalid EPUB file path.")

root = tk.Tk()
root.title("Kanji Kounter")
root.geometry("600x200")
root.configure(bg="#36393F")

text_color = "#FFFFFF"
button_bg = "#202225"
button_fg = "#FFFFFF"

frame = tk.Frame(root, bg="#36393F")
frame.pack(expand=True, fill=tk.BOTH)

epub_path_entry = tk.Entry(frame, width=50, bg=button_bg, fg=text_color, insertbackground=text_color)
epub_path_entry.pack(padx=5, pady=5, side=tk.LEFT)

browse_button = tk.Button(frame, text="Browse", command=browse_file, bg=button_bg, fg=button_fg)
browse_button.pack(padx=5, pady=5, side=tk.LEFT)

analyze_button = tk.Button(frame, text="Analyze", command=analyze_button_click, bg=button_bg, fg=button_fg)
analyze_button.pack(padx=5, pady=5, side=tk.LEFT)

result_text = tk.Text(root, width=60, height=10, wrap=tk.WORD, bg=button_bg, fg=text_color)
result_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

root.mainloop()
