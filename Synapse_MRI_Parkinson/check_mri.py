import sys
import pandas as pd
from pathlib import Path

# =========================
# CONFIG (no arguments)
# =========================
BASE_DIR = Path(r"D:\Datasets\Synapse\Synapse_MRI_Parkinson").resolve()
MRI_ROOT = BASE_DIR / "MRI_data"
DEMO_CSV = BASE_DIR / "BrainLat_Demographic_MRI.csv"

OUT_CSV = BASE_DIR / "mri_modality_availability.csv"

# Detect NIfTI files: .nii or .nii.gz
def has_nifti(folder: Path) -> bool:
    if not folder.exists() or not folder.is_dir():
        return False
    for p in folder.rglob("*"):
        if not p.is_file():
            continue
        name = p.name.lower()
        if name.endswith(".nii") or name.endswith(".nii.gz"):
            return True
    return False

def main():
    if not MRI_ROOT.exists():
        print("ERROR: MRI_data not found at:", MRI_ROOT)
        sys.exit(1)
    if not DEMO_CSV.exists():
        print("ERROR: BrainLat_Demographic_MRI.csv not found at:", DEMO_CSV)
        sys.exit(1)

    demo = pd.read_csv(DEMO_CSV)
    if "MRI_ID" not in demo.columns or "diagnosis" not in demo.columns:
        print("ERROR: demographics CSV must contain columns: MRI_ID, diagnosis")
        print("Found columns:", list(demo.columns))
        sys.exit(1)

    demo["MRI_ID"] = demo["MRI_ID"].astype(str).str.strip()
    demo["diagnosis"] = demo["diagnosis"].astype(str).str.strip()

    # Collect subject dirs that match pattern MRI_data/<SITE>/<SUBJECT>/
    rows = []
    seen = set()

    # site folders are immediate children of MRI_data (AR, CLB, COA, ...)
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

            key = (site, subject)
            if key in seen:
                continue
            seen.add(key)

            anat_dir = subj_dir / "anat"
            dwi_dir = subj_dir / "dwi"
            func_dir = subj_dir / "func"

            rows.append({
                "site": site,
                "subject": subject,
                "has_anat_dir": anat_dir.exists(),
                "has_dwi_dir": dwi_dir.exists(),
                "has_func_dir": func_dir.exists(),
                "has_anat_nifti": has_nifti(anat_dir),
                "has_dwi_nifti": has_nifti(dwi_dir),
                "has_func_nifti": has_nifti(func_dir),
            })

    df = pd.DataFrame(rows)
    df = df.merge(demo[["MRI_ID", "diagnosis"]], left_on="subject", right_on="MRI_ID", how="left")

    # Save full table
    df.to_csv(OUT_CSV, index=False)

    # Summary print
    def count(mask, label):
        sub = df[mask].drop_duplicates(subset=["subject"])
        pd_n = int((sub["diagnosis"] == "PD").sum())
        cn_n = int((sub["diagnosis"] == "CN").sum())
        unk_n = int(sub["diagnosis"].isna().sum())
        total = len(sub)
        print(f"{label:<20} total={total:>4} | PD={pd_n:>3} | CN={cn_n:>3} | UNKNOWN={unk_n:>3}")

    print("=" * 90)
    print("MRI MODALITY AVAILABILITY REPORT (anat / dwi / func)")
    print("Base dir :", BASE_DIR)
    print("MRI root :", MRI_ROOT)
    print("Demo CSV :", DEMO_CSV)
    print("=" * 90)

    # Use nifti-based availability as the meaningful metric
    has_anat = df["has_anat_nifti"]
    has_dwi  = df["has_dwi_nifti"]
    has_func = df["has_func_nifti"]

    count(has_anat, "ANAT (NIfTI)")
    count(has_dwi,  "DWI (NIfTI)")
    count(has_func, "FUNC (NIfTI)")

    print("-" * 90)
    count(has_anat & has_dwi, "ANAT + DWI")
    count(has_anat & has_func, "ANAT + FUNC")
    count(has_dwi & has_func, "DWI + FUNC")
    count(has_anat & has_dwi & has_func, "ANAT + DWI + FUNC")

    print("-" * 90)
    # Also show directory-only (in case folders exist but nifti detection misses something)
    count(df["has_anat_dir"], "ANAT (dir)")
    count(df["has_dwi_dir"],  "DWI (dir)")
    count(df["has_func_dir"], "FUNC (dir)")

    print("=" * 90)
    print("Saved:", OUT_CSV)
    print("=" * 90)

if __name__ == "__main__":
    main()
