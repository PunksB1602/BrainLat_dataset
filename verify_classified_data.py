from pathlib import Path
import pandas as pd

# =========================
# CONFIG (no arguments)
# =========================
MRI_ROOT = Path(r"D:\Datasets\Synapse\MRI_ANAT_CLASSIFIED").resolve()
EEG_ROOT = Path(r"D:\Datasets\Synapse\EEG_CLASSIFIED").resolve()

EEG_EXT = (".set", ".fdt", ".edf", ".bdf")

# -------------------------
# MRI detection (robust)
# -------------------------
def is_mri_image_file(p: Path) -> bool:
    name = p.name.lower()

    # Standard NIfTI
    if name.endswith(".nii") or name.endswith(".nii.gz"):
        return True

    # Legacy/misnamed compressed image (e.g., *_t1w.gz)
    if name.endswith(".gz"):
        if name.endswith(".json.gz"):
            return False
        if any(tag in name for tag in [".bval", ".bvec", ".tsv", "events", "physio"]):
            return False
        return True

    return False

def has_mri_file(anat_dir: Path) -> bool:
    for p in anat_dir.rglob("*"):
        if p.is_file() and is_mri_image_file(p):
            return True
    return False

# -------------------------
# Generic extension check (EEG)
# -------------------------
def has_file_with_ext(root: Path, exts) -> bool:
    for p in root.rglob("*"):
        if p.is_file() and p.name.lower().endswith(exts):
            return True
    return False

def verify_mri():
    rows = []
    for label in ["PD", "CN"]:
        label_dir = MRI_ROOT / label
        if not label_dir.exists():
            continue

        for subj_dir in label_dir.iterdir():
            if not subj_dir.is_dir():
                continue

            anat_dir = subj_dir / "anat"
            ok = anat_dir.exists() and has_mri_file(anat_dir)

            rows.append({
                "label": label,
                "subject": subj_dir.name,
                "has_anat_dir": anat_dir.exists(),
                "has_mri_image": has_mri_file(anat_dir) if anat_dir.exists() else False,
                "status": "OK" if ok else "MISSING"
            })

    df = pd.DataFrame(rows)
    df.to_csv("verify_mri_anat.csv", index=False)

    total = len(df)
    valid = int((df["status"] == "OK").sum())
    missing = int((df["status"] != "OK").sum())

    # PD/CN totals (by unique subject)
    # (Each subject appears once here, so value_counts is fine)
    counts = df["label"].value_counts()
    pd_n = int(counts.get("PD", 0))
    cn_n = int(counts.get("CN", 0))

    print("=" * 80)
    print("MRI VERIFICATION")
    print("=" * 80)
    print(f"Total subjects: {total}  |  PD: {pd_n}  |  CN: {cn_n}")
    print(f"Valid subjects: {valid}")
    print(f"Missing/invalid: {missing}")
    print("Saved: verify_mri_anat.csv")

def verify_eeg():
    rows = []
    for label in ["PD", "CN"]:
        label_dir = EEG_ROOT / label
        if not label_dir.exists():
            continue

        for site_dir in label_dir.iterdir():  # AR / CL
            if not site_dir.is_dir():
                continue

            for subj_dir in site_dir.iterdir():
                if not subj_dir.is_dir():
                    continue

                ok = has_file_with_ext(subj_dir, EEG_EXT)

                rows.append({
                    "label": label,
                    "condition": site_dir.name,   # AR / CL
                    "subject": subj_dir.name,
                    "has_eeg_file": ok,
                    "status": "OK" if ok else "MISSING"
                })

    df = pd.DataFrame(rows)
    df.to_csv("verify_eeg.csv", index=False)

    # Folder counts (each AR/CL folder counted)
    folder_total = len(df)
    folder_valid = int((df["status"] == "OK").sum())
    folder_missing = int((df["status"] != "OK").sum())
    folder_counts = df["label"].value_counts()
    folder_pd = int(folder_counts.get("PD", 0))
    folder_cn = int(folder_counts.get("CN", 0))

    # Unique subject counts (subject ID counted once even if in both AR and CL)
    uniq = df.drop_duplicates(subset=["label", "subject"])
    subj_total = len(uniq)
    subj_counts = uniq["label"].value_counts()
    subj_pd = int(subj_counts.get("PD", 0))
    subj_cn = int(subj_counts.get("CN", 0))

    print("=" * 80)
    print("EEG VERIFICATION")
    print("=" * 80)
    print(f"Folder-count (AR+CL sessions): total={folder_total} | PD={folder_pd} | CN={folder_cn}")
    print(f"Unique subjects (IDs):         total={subj_total} | PD={subj_pd} | CN={subj_cn}")
    print(f"Valid folders: {folder_valid}")
    print(f"Missing/invalid folders: {folder_missing}")
    print("Saved: verify_eeg.csv")


def main():
    if not MRI_ROOT.exists():
        print("ERROR: MRI_ANAT_CLASSIFIED not found:", MRI_ROOT)
        return
    if not EEG_ROOT.exists():
        print("ERROR: EEG_CLASSIFIED not found:", EEG_ROOT)
        return

    verify_mri()
    verify_eeg()

    print("=" * 80)
    print("VERIFICATION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
