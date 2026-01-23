import shutil
from pathlib import Path

# =========================
# CONFIG (no arguments)
# =========================
BASE_DIR = Path(r"D:\Datasets\Synapse\Synapse_EEG_Parkinson").resolve()
EEG_ROOT = BASE_DIR / "EEG_data"
OUT_ROOT = BASE_DIR / "EEG_CLASSIFIED"

# Map source folder -> target label
MAP = {
    "3_PD": "PD",
    "5_HC": "CN"   # treat HC as control (CN)
}

def main():
    if not EEG_ROOT.exists():
        print("ERROR: EEG_data not found:", EEG_ROOT)
        return

    (OUT_ROOT / "PD").mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "CN").mkdir(parents=True, exist_ok=True)

    copied_pd = 0
    copied_cn = 0
    skipped = 0

    for src_group, label in MAP.items():
        group_dir = EEG_ROOT / src_group
        if not group_dir.exists():
            print("WARNING: missing folder:", group_dir)
            continue

        for cond_dir in group_dir.iterdir():  # AR, CL, etc.
            if not cond_dir.is_dir():
                continue
            condition = cond_dir.name

            for subj_dir in cond_dir.iterdir():  # sub-xxxxx
                if not subj_dir.is_dir():
                    continue

                subject = subj_dir.name
                dest = OUT_ROOT / label / condition / subject

                if dest.exists():
                    continue

                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(subj_dir, dest)

                if label == "PD":
                    copied_pd += 1
                else:
                    copied_cn += 1

    print("=" * 90)
    print("EEG PD/CN CLASSIFICATION COPY COMPLETE")
    print("Source :", EEG_ROOT)
    print("Target :", OUT_ROOT)
    print("-" * 90)
    print("Copied PD:", copied_pd)
    print("Copied CN:", copied_cn)
    print("Skipped:", skipped)
    print("=" * 90)

if __name__ == "__main__":
    main()
