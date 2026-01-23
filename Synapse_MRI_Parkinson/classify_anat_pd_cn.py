import shutil
from pathlib import Path
import pandas as pd

# =========================
# CONFIG (no arguments)
# =========================
BASE_DIR = Path(r"D:\Datasets\Synapse\Synapse_MRI_Parkinson").resolve()
ANAT_ROOT = BASE_DIR / "MRI_ANAT"
DEMO_CSV  = BASE_DIR / "BrainLat_Demographic_MRI.csv"
OUT_ROOT  = BASE_DIR / "MRI_ANAT_CLASSIFIED"

def main():
    if not ANAT_ROOT.exists():
        print("ERROR: MRI_ANAT not found:", ANAT_ROOT)
        return
    if not DEMO_CSV.exists():
        print("ERROR: Demographics CSV not found:", DEMO_CSV)
        return

    demo = pd.read_csv(DEMO_CSV)
    if "MRI_ID" not in demo.columns or "diagnosis" not in demo.columns:
        print("ERROR: BrainLat_Demographic_MRI.csv must contain MRI_ID and diagnosis")
        print("Found:", list(demo.columns))
        return

    demo["MRI_ID"] = demo["MRI_ID"].astype(str).str.strip()
    demo["diagnosis"] = demo["diagnosis"].astype(str).str.strip()

    label_map = dict(zip(demo["MRI_ID"], demo["diagnosis"]))

    (OUT_ROOT / "PD").mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "CN").mkdir(parents=True, exist_ok=True)

    copied_pd = 0
    copied_cn = 0
    skipped_no_label = 0
    skipped_not_found = 0

    for site_dir in ANAT_ROOT.iterdir():
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
                skipped_not_found += 1
                continue

            label = label_map.get(subject, None)
            if label not in ("PD", "CN"):
                skipped_no_label += 1
                continue

            dest_subject_name = f"{site}_{subject}"  # avoid collisions across sites
            dest = OUT_ROOT / label / dest_subject_name / "anat"

            if dest.exists():
                # already copied
                continue

            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(anat_dir, dest)

            if label == "PD":
                copied_pd += 1
            else:
                copied_cn += 1

    print("=" * 90)
    print("ANAT PD/CN CLASSIFICATION COPY COMPLETE")
    print("Source :", ANAT_ROOT)
    print("Target :", OUT_ROOT)
    print("-" * 90)
    print("Copied PD:", copied_pd)
    print("Copied CN:", copied_cn)
    print("Skipped (no label / not PD-CN):", skipped_no_label)
    print("Skipped (no anat folder found):", skipped_not_found)
    print("=" * 90)

if __name__ == "__main__":
    main()
