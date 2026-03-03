import shutil
import csv
from pathlib import Path

# =========================
# CONFIG
# =========================
BASE_DIR = Path(r"D:\Datasets\Synapse\Synapse_EEG_Parkinson").resolve()
EEG_ROOT = BASE_DIR / "EEG_data"
OUT_ROOT = BASE_DIR / "EEG_CLASSIFIED"
OUT_CSV  = OUT_ROOT / "eeg_paired_subjects.csv"

# Map source folder name -> diagnosis label and region key
MAP = {
    "3_PD": "PD",
    "5_HC": "CN",
}

# ── Helpers ──────────────────────────────────────────────────────────────────

def has_paired_eeg(subj_dir: Path) -> tuple[bool, str, str]:
    """Return (paired, set_file, fdt_file) for a subject folder."""
    set_files = {}
    fdt_files = {}
    for f in subj_dir.rglob("*.set"):
        set_files[f.stem.lower()] = f
    for f in subj_dir.rglob("*.fdt"):
        fdt_files[f.stem.lower()] = f
    common = set(set_files) & set(fdt_files)
    if common:
        stem = sorted(common)[0]
        return True, set_files[stem].name, fdt_files[stem].name
    return False, "", ""


def load_csv_index(path: Path, key_col: str = "id EEG") -> dict:
    """Load a CSV keyed by (country_code, id_eeg) using the 'path' column.
    e.g. path='3_PD/AR' -> country='AR', combined key ('AR', 'sub-40001').
    """
    index = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sid     = row[key_col].strip()
            country = row.get("path", "").strip().split("/")[-1].strip()
            k = (country, sid)
            if k not in index:
                index[k] = row
    return index


def load_csvs() -> tuple[dict, dict, dict, dict]:
    """Load demographics + cognition for HC and PD."""
    dem_hc  = load_csv_index(BASE_DIR / "demographics_hc_eeg_data.csv")
    dem_pd  = load_csv_index(BASE_DIR / "Demographics_PD_EEG_data.csv")
    cog_hc  = load_csv_index(BASE_DIR / "cognition_hc_eeg_data.csv")
    cog_pd  = load_csv_index(BASE_DIR / "Cognition_PD_EEG_data.csv")
    return dem_hc, dem_pd, cog_hc, cog_pd


def get_demo(subject_id: str, country: str, label: str, dem_hc: dict, dem_pd: dict) -> dict:
    src = dem_pd if label == "PD" else dem_hc
    return src.get((country, subject_id), {})


def get_cog(subject_id: str, country: str, label: str, cog_hc: dict, cog_pd: dict) -> dict:
    src = cog_pd if label == "PD" else cog_hc
    return src.get((country, subject_id), {})


def safe(d: dict, key: str, default: str = "") -> str:
    return str(d.get(key, default)).strip() if d else default


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if not EEG_ROOT.exists():
        print("ERROR: EEG_data not found:", EEG_ROOT)
        return

    dem_hc, dem_pd, cog_hc, cog_pd = load_csvs()

    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    records       = []   # for the output CSV
    copied_pd     = 0
    copied_cn     = 0
    skipped_no_pair = 0
    skipped_exists  = 0

    for src_group, label in MAP.items():
        group_dir = EEG_ROOT / src_group
        if not group_dir.exists():
            print("WARNING: missing folder:", group_dir)
            continue

        for cond_dir in sorted(group_dir.iterdir()):   # AR, CL …
            if not cond_dir.is_dir():
                continue
            condition = cond_dir.name

            for subj_dir in sorted(cond_dir.iterdir()):  # sub-xxxxx
                if not subj_dir.is_dir():
                    continue

                subject = subj_dir.name

                # ── Only proceed if both .set AND .fdt exist ──────────────
                paired, set_file, fdt_file = has_paired_eeg(subj_dir)
                if not paired:
                    print(f"  [SKIP - no pair] {label}/{condition}/{subject}")
                    skipped_no_pair += 1
                    continue

                # ── Copy to EEG_CLASSIFIED ────────────────────────────────
                dest = OUT_ROOT / label / condition / subject
                if dest.exists():
                    skipped_exists += 1
                else:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copytree(subj_dir, dest)
                    if label == "PD":
                        copied_pd += 1
                    else:
                        copied_cn += 1

                # ── Collect metadata for CSV ───────────────────────────────
                demo = get_demo(subject, condition, label, dem_hc, dem_pd)
                cog  = get_cog (subject, condition, label, cog_hc, cog_pd)

                sex_raw = safe(demo, "sex")
                sex_str = "Male" if sex_raw == "1" else ("Female" if sex_raw == "0" else sex_raw)

                lat_raw = safe(demo, "laterality")
                lat_str = "Right" if lat_raw == "1" else ("Left" if lat_raw == "0" else lat_raw)

                records.append({
                    # Identification
                    "subject_id"                  : subject,
                    "diagnosis"                   : label,
                    "country"                     : condition,
                    "set_file"                    : set_file,
                    "fdt_file"                    : fdt_file,
                    # Demographics
                    "sex"                         : sex_str,
                    "age"                         : safe(demo, "Age"),
                    "years_education"             : safe(demo, "years_education"),
                    "laterality"                  : lat_str,
                    # Cognition – MoCA
                    "moca_total"                  : safe(cog, "moca_total"),
                    "moca_visuospatial"           : safe(cog, "moca_visuospatial"),
                    "moca_recog"                  : safe(cog, "moca_recog"),
                    "moca_attention"              : safe(cog, "moca_attention"),
                    "moca_language"               : safe(cog, "moca_language"),
                    "moca_abstraction"            : safe(cog, "moca_abstraction"),
                    "moca_memory"                 : safe(cog, "moca_memory"),
                    "moca_orientation"            : safe(cog, "moca_orientation"),
                    # Cognition – IFS
                    "ifs_total_score"             : safe(cog, "ifs_total_score"),
                    "ifs_motor_series"            : safe(cog, "ifs_motor_series"),
                    "ifs_conflicting_instructions": safe(cog, "ifs_conflicting_instructions"),
                    "ifs_motor_inhibition"        : safe(cog, "ifs_motor_inhibition"),
                    "ifs_digits"                  : safe(cog, "ifs_digits"),
                    "ifs_months"                  : safe(cog, "ifs_months"),
                    "ifs_visual_wm"               : safe(cog, "ifs_visual_wm"),
                    "ifs_proverb"                 : safe(cog, "ifs_proverb"),
                    "ifs_verbal_inhibition"       : safe(cog, "ifs_verbal_inhibition"),
                    # Cognition – Mini-SEA
                    "mini_sea_fer"                : safe(cog, "mini_sea_fer"),
                    "mini_sea_tom"                : safe(cog, "mini_sea_tom"),
                    "emotion_recog"               : safe(cog, "emotion recog"),
                    # MMSE (PD only)
                    "mmse"                        : safe(cog, "MMSE"),
                })

    # ── Write CSV ─────────────────────────────────────────────────────────────
    fieldnames = list(records[0].keys()) if records else []
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    # ── Summary ───────────────────────────────────────────────────────────────
    pd_count = sum(1 for r in records if r["diagnosis"] == "PD")
    cn_count = sum(1 for r in records if r["diagnosis"] == "CN")
    ar_count = sum(1 for r in records if r["country"] == "AR")
    cl_count = sum(1 for r in records if r["country"] == "CL")

    print("=" * 90)
    print("EEG PD/CN CLASSIFICATION — PAIRED FILES ONLY")
    print(f"Source : {EEG_ROOT}")
    print(f"Target : {OUT_ROOT}")
    print(f"CSV    : {OUT_CSV}")
    print("-" * 90)
    print(f"  Total subjects with paired .set+.fdt : {len(records)}")
    print(f"    PD : {pd_count}   |   CN : {cn_count}")
    print(f"    AR : {ar_count}   |   CL : {cl_count}")
    print(f"  Copied  PD : {copied_pd}   |   Copied  CN : {copied_cn}")
    print(f"  Skipped (no pair)        : {skipped_no_pair}")
    print(f"  Skipped (already exists) : {skipped_exists}")
    print("=" * 90)
    print(f"\nCSV saved -> {OUT_CSV}")


if __name__ == "__main__":
    main()
