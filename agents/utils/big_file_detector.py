# agents/utils/big_file_detector.py

import os

def find_big_files(folder, min_mb=100):
    bigs = []
    min_bytes = min_mb * 1024 * 1024
    for root, _, files in os.walk(folder):
        for f in files:
            path = os.path.join(root, f)
            try:
                size = os.path.getsize(path)
                if size > min_bytes:
                    bigs.append((path, round(size/1024/1024, 2)))
            except Exception:
                continue
    return bigs
