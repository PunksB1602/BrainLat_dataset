import os
from collections import Counter

BASE_DIR = os.path.join(os.path.dirname(__file__), "MRI_data")

def ext_key(filename: str) -> str:
    name = filename.lower()
    if name.endswith(".nii.gz"):
        return ".nii.gz"
    ext = os.path.splitext(name)[1].lower()
    return ext if ext else "[no extension]"

def main():
    counts = Counter()
    total_files = 0

    for root, _, files in os.walk(BASE_DIR):
        for fn in files:
            counts[ext_key(fn)] += 1
            total_files += 1

    print(f"Scanning: {BASE_DIR}\n")
    print(f"Total files: {total_files}\n")

    print("File counts by extension:")
    for ext, n in counts.most_common():
        print(f"  {ext:12s} {n}")

if __name__ == "__main__":
    main()
