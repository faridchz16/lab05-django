import os
import glob
from pathlib import Path

def find_recent_images():
    search_paths = [
        r"C:\Users\farid\Downloads",
        r"C:\Users\farid\AppData\Local\Temp",
        r"C:\Users\farid\AppData\Local\Temp\opencode",
        r"E:\OpenCode\Lab05"
    ]
    
    for p in search_paths:
        if os.path.exists(p):
            print(f"Searching in {p}...")
            for ext in ('*.jpg', '*.jpeg', '*.png', '*.webp'):
                for f in glob.glob(os.path.join(p, "**", ext), recursive=True):
                    stat = os.path.getmtime(f)
                    print(f"  {f} (mtime: {stat})")

if __name__ == '__main__':
    find_recent_images()
