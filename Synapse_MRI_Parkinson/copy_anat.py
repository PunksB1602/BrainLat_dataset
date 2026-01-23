import shutil
from pathlib import Path

# =========================
# CONFIG (edit only if needed)
# =========================
BASE_DIR = Path(r"D:\Datasets\Synapse\Synapse_MRI_Parkinson").resolve()
MRI_ROOT = BASE_DIR / "MRI_data"
OUT_ROOT = BASE_DIR / "MRI_ANAT"

def main():
    OUT_ROOT.mkdir(exist_ok=True)

    copied = 0
    skipped = 0

    for site_dir in MRI_ROOT.iterdir():
        if not site_dir.is_dir():
            continue
        site = site_dir.name

        for subj_dir in site_dir.iterdir():
            if not subj_dir.is_dir():
                continue
            subject = subj_dir.name
            if not subject.lower().startswith("sub-"):
                continue

            anat_dir = subj_dir / "anat"
            if not anat_dir.exists():
                skipped += 1
                continue

            dest = OUT_ROOT / site / subject / "anat"
            if dest.exists():
                # already copied
                continue

            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(anat_dir, dest)

            copied += 1

    print("=" * 80)
    print("ANAT COPY COMPLETE")
    print("Source :", MRI_ROOT)
    print("Target :", OUT_ROOT)
    print("Subjects copied :", copied)
    print("Subjects skipped (no anat) :", skipped)
    print("=" * 80)

if __name__ == "__main__":
    main()
