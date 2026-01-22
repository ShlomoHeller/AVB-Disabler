import sys, os, re
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

TXT = {
    "title": ("AVB Disabler", "משבית AVB"),
    "select_active": ("Please select an active vbmeta file", "אנא בחר קובץ vbmeta פעיל"),
    "option_1": ("Press Enter to choose a file", "לחץ אנטר כדי לבחור קובץ"),
    "option_drag": ("Or drag and drop a file into this window", "או גרור ושחרר קובץ בחלון זה"),
    "active": ("AVB is ACTIVE", "AVB פעיל"),
    "disabled": ("AVB already disabled", "AVB כבר מושבת"),
    "invalid": ("Invalid vbmeta file", "קובץ vbmeta לא חוקי"),
    "ask_disable": ("Do you want to disable AVB?", "האם ברצונך להשבית את ה-BVA?"),
    "press_enter": ("Press Enter to continue", "לחץ אנטר בשביל להמשיך"),
    "success": ("AVB disabled successfully", "AVB הושבת בהצלחה"),
    "file_exists": ("File already exists. Overwrite?", "הקובץ כבר קיים. האם לדרוס?"),
    "saved": ("The disabled vbmeta file was saved to:", "הקובץ vbmeta המושבת נשמר ב:"),
    "not_found": ("File does not exist", "הקובץ לא קיים"),
    "exit": ("Process finished. Press Enter to restart", "התהליך הסתיים. בשביל להמשיך לחץ אנטר"),
}

def fix_he(text):
    words = [w[::-1] if re.search(r'[\u0590-\u05FF]', w) else w for w in text.split()]
    return " ".join(words[::-1])

def bi_print(en, he=""):
    print(f"{en:<55} {fix_he(he):>63}")

def set_terminal_title(title):
    if os.name == 'nt':
        os.system(f"title {title}")

def get_file():
    root = tk.Tk(); root.withdraw()
    path = filedialog.askopenfilename(filetypes=[("vbmeta images", "*.img"), ("All files", "*.*")])
    root.destroy()
    return path

def process_file(path_str):
    if not path_str: return
    path = Path(path_str.strip('"'))
    
    if not path.exists():
        bi_print(*TXT["not_found"])
        return
    
    try:
        data = bytearray(path.read_bytes())
        if data[:4] != b"AVB0":
            return bi_print(*TXT["invalid"])
        
        is_active = not (data[123] & 3)
        bi_print(*TXT["active"] if is_active else TXT["disabled"])
        
        if is_active:
            bi_print(*TXT["ask_disable"])
            bi_print(*TXT["press_enter"])
            if input("> ") == "":
                data[123] |= 3
                base = Path(sys.executable).parent if getattr(sys, "frozen", 0) else Path(__file__).parent
                out_dir = base / "Disabled"
                out_dir.mkdir(exist_ok=True)
                out_path = out_dir / f"{path.stem}_disabled{path.suffix}"
                
                if out_path.exists():
                    bi_print(*TXT["file_exists"])
                    if input("> ") != "": return

                out_path.write_bytes(data)
                bi_print(*TXT["success"])
                bi_print(*TXT["saved"])
                print(f"\n{out_path}")
                
    except Exception as e:
        print(f"Error: {e}")

def main():
    if os.name == 'nt': 
        set_terminal_title("AVB Disabler")
        os.system("color 1F")
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        bi_print(*TXT["title"])
        print("-" * 115)
        bi_print(*TXT["select_active"])
        print()
        bi_print(*TXT["option_1"])
        bi_print(*TXT["option_drag"])
        print("-" * 115)        
        inp = input("> ").strip()
        process_file(inp if inp else get_file())
        print("\n" + "-" * 115)
        bi_print(*TXT["exit"])
        input("> ")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()