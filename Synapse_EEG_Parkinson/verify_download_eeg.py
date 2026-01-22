import os
import pandas as pd

print("="*90)
print("EEG DOWNLOAD VERIFICATION: CSV vs SYNAPSE WEBSITE vs LOCAL DATA (FILES CHECK)")
print("="*90)

# ----------------------------
# 1) LOAD EEG CSVs
# ----------------------------
cog_hc  = pd.read_csv("cognition_hc_eeg_data.csv")
cog_pd  = pd.read_csv("Cognition_PD_EEG_data.csv")
demo_hc = pd.read_csv("demographics_hc_eeg_data.csv")
demo_pd = pd.read_csv("Demographics_PD_EEG_data.csv")
rec_hc  = pd.read_csv("records_hc_eeg_data.csv")
rec_pd  = pd.read_csv("Records_PD_EEG_data.csv")

# ----------------------------
# HELPERS
# ----------------------------
def get_subject_id_col(df):
    for c in ["id", "id EEG", "id_EEG"]:
        if c in df.columns:
            return c
    return None

def normalize_ids(series):
    return series.astype(str).str.strip()

def safe_split_path(path_val):
    if pd.isna(path_val):
        return []
    p = str(path_val).replace("\\", "/").strip()
    parts = [x for x in p.split("/") if x]  # remove empty parts
    return parts

def site_from_path(path_val):
    # e.g., "3_PD/CL" -> "CL", "5_HC/AR" -> "AR"
    parts = safe_split_path(path_val)
    return parts[-1].strip() if parts else None

def folder_group_from_path(path_val):
    # e.g., "3_PD/CL" -> "3_PD", "5_HC/AR" -> "5_HC"
    parts = safe_split_path(path_val)
    return parts[0].strip() if parts else None

def ids_in_df(df):
    id_col = get_subject_id_col(df)
    if id_col is None:
        return set()
    return set(normalize_ids(df[id_col]).dropna().tolist())

def build_master_from_demographics(demo_df):
    id_col = get_subject_id_col(demo_df)
    if id_col is None:
        raise ValueError("No subject id column found in demographics file.")
    out = demo_df.copy()
    out["subject_id"] = normalize_ids(out[id_col])
    out["site"] = out["path"].apply(site_from_path) if "path" in out.columns else None
    out["group_folder"] = out["path"].apply(folder_group_from_path) if "path" in out.columns else None
    # keep diagnosis if exists; if not, set None
    if "diagnosis" not in out.columns:
        out["diagnosis"] = None
    return out[["subject_id", "diagnosis", "site", "group_folder"]].drop_duplicates()

def has_eeg_files(subject_folder):
    # Consider "downloaded" only if we find at least one EEG file
    # (edit extensions if your dataset uses different ones)
    for root, _, files in os.walk(subject_folder):
        for f in files:
            fl = f.lower()
            if fl.endswith(".set") or fl.endswith(".fdt"):
                return True
    return False

# ----------------------------
# MASTER CSV UNIVERSE (DEMOGRAPHICS = truth for folder/site + diagnosis)
# ----------------------------
master_demo = pd.concat(
    [build_master_from_demographics(demo_hc), build_master_from_demographics(demo_pd)],
    ignore_index=True
).drop_duplicates()

csv_ids_demo = set(master_demo["subject_id"].dropna().tolist())
csv_ids_cog  = ids_in_df(cog_hc) | ids_in_df(cog_pd)
csv_ids_rec  = ids_in_df(rec_hc) | ids_in_df(rec_pd)

# ----------------------------
# 2) SYNAPSE WEBSITE SUBJECTS (PASTE FROM YOUR WEBSITE LIST)
# ----------------------------
synapse_subjects = {
    ("3_PD", "AR"): [
        "sub-40001","sub-40006","sub-40008","sub-40010","sub-40011","sub-40012","sub-40013"
    ],
    ("3_PD", "CL"): [
        "sub-40001","sub-40004","sub-40005","sub-40006","sub-40007","sub-40008","sub-40009",
        "sub-40010","sub-40011","sub-40012","sub-40015","sub-40016","sub-40017","sub-40018",
        "sub-40019","sub-40020","sub-40021","sub-40022","sub-40023","sub-40024","sub-40025","sub-40026"
    ],
    ("5_HC", "AR"): [
        "sub-100012","sub-100015","sub-100018","sub-10002","sub-100020","sub-100022","sub-100024",
        "sub-100026","sub-100028","sub-10003","sub-100030","sub-100031","sub-100033","sub-100035",
        "sub-100038","sub-10004","sub-10006","sub-10007","sub-10009"
    ],
    ("5_HC", "CL"): [
        "sub-10001","sub-100010","sub-100011","sub-100013","sub-100014","sub-100016","sub-100017",
        "sub-100019","sub-100021","sub-100023","sub-100025","sub-100027","sub-100029","sub-100032",
        "sub-100034","sub-100036","sub-100037","sub-100039","sub-100040","sub-100041","sub-100042",
        "sub-100043","sub-100044","sub-100045","sub-100046","sub-10005","sub-10008"
    ],
}

# ----------------------------
# 3) LOCAL ROOT (EDIT IF NEEDED)
# ----------------------------
# Expected structure:
#   ./EEG_data/3_PD/AR/sub-40001/...
#   ./EEG_data/5_HC/CL/sub-10001/...
LOCAL_EEG_ROOT = "./EEG_data"

# ----------------------------
# 4) VERIFICATION PER FOLDER
# ----------------------------
all_results = {}

for (group_folder, site), subjects in synapse_subjects.items():
    print(f"\n{'='*90}")
    print(f"FOLDER: {group_folder}/{site}  (Synapse website items: {len(subjects)})")
    print(f"{'='*90}")

    subjects = sorted(set([str(s).strip() for s in subjects if str(s).strip()]))

    # 4.1 CSV expected for this folder/site (from DEMOGRAPHICS)
    csv_expected = master_demo[
        (master_demo["group_folder"] == group_folder) &
        (master_demo["site"] == site)
    ].copy()

    csv_expected_ids = set(csv_expected["subject_id"].dropna().tolist())
    n_csv = len(csv_expected)
    n_csv_pd = int((csv_expected["diagnosis"] == "PD").sum()) if "diagnosis" in csv_expected.columns else 0
    n_csv_cn = int((csv_expected["diagnosis"] == "CN").sum()) if "diagnosis" in csv_expected.columns else 0

    print("\n1) CSV EXPECTED (from DEMOGRAPHICS):")
    print(f"   Total: {n_csv} subjects | PD: {n_csv_pd} | CN: {n_csv_cn}")
    if n_csv:
        print("   IDs:", ", ".join(sorted(csv_expected_ids)))

    # Compare website list vs demographics-expected (strongest check)
    missing_from_demo_expected = [s for s in subjects if s not in csv_expected_ids]
    extra_in_demo_expected = [s for s in sorted(csv_expected_ids) if s not in subjects]

    print("\n   DEMOGRAPHICS vs WEBSITE (folder-level):")
    print(f"   Missing on website but expected by demographics: {len(extra_in_demo_expected)}")
    if extra_in_demo_expected:
        print("   Extra-expected IDs:", ", ".join(extra_in_demo_expected))
    print(f"   Present on website but NOT in demographics-expected: {len(missing_from_demo_expected)}")
    if missing_from_demo_expected:
        print("   Missing-in-demographics IDs:", ", ".join(missing_from_demo_expected))

    # 4.2 Website subjects vs presence across ANY EEG CSV (dem/cog/rec)
    in_demo = [s for s in subjects if s in csv_ids_demo]
    in_cog  = [s for s in subjects if s in csv_ids_cog]
    in_rec  = [s for s in subjects if s in csv_ids_rec]
    missing_all_csv = [s for s in subjects if (s not in csv_ids_demo and s not in csv_ids_cog and s not in csv_ids_rec)]

    print("\n2) WEBSITE vs CSV PRESENCE (any EEG CSV):")
    print(f"   Present in Demographics CSV: {len(in_demo)} / {len(subjects)}")
    print(f"   Present in Cognition CSV:    {len(in_cog)} / {len(subjects)}")
    print(f"   Present in Records CSV:      {len(in_rec)} / {len(subjects)}")
    if missing_all_csv:
        print(f"   [WARN] Missing from ALL EEG CSVs: {len(missing_all_csv)}")
        print("   Missing IDs:", ", ".join(missing_all_csv))
    else:
        print("   [OK] All website IDs appear in at least one EEG CSV")

    # 4.3 Local download verification (checks REAL EEG FILES)
    local_folder = os.path.join(LOCAL_EEG_ROOT, group_folder, site)
    downloaded = []
    not_downloaded = []
    empty_or_no_eeg_files = []

    for s in subjects:
        p = os.path.join(local_folder, s)
        if os.path.isdir(p):
            if has_eeg_files(p):
                downloaded.append(s)
            else:
                empty_or_no_eeg_files.append(s)
                not_downloaded.append(s)
        else:
            not_downloaded.append(s)

    print("\n3) LOCAL DATA VERIFICATION (folder + .set/.fdt files):")
    print(f"   Path: {local_folder}")
    print(f"   Downloaded (has EEG files): {len(downloaded)} / {len(subjects)} (website available)")
    if not_downloaded:
        print(f"   [WARN] NOT Downloaded / incomplete: {len(not_downloaded)}")
        print("   Missing/Incomplete:", ", ".join(not_downloaded))
    else:
        print("   [OK] All website subjects exist locally with EEG files!")

    all_results[(group_folder, site)] = {
        "synapse_total": len(subjects),
        "csv_expected": n_csv,
        "csv_pd": n_csv_pd,
        "csv_cn": n_csv_cn,
        "missing_in_demographics_expected": len(missing_from_demo_expected),
        "extra_in_demographics_expected": len(extra_in_demo_expected),
        "missing_all_csv": len(missing_all_csv),
        "downloaded": len(downloaded),
        "not_downloaded": len(not_downloaded),
    }

# ----------------------------
# 5) FINAL SUMMARY
# ----------------------------
print(f"\n{'='*90}")
print("OVERALL SUMMARY - EEG WEBSITE vs CSV vs LOCAL")
print(f"{'='*90}")

total_syn = sum(v["synapse_total"] for v in all_results.values())
total_csv = sum(v["csv_expected"] for v in all_results.values())
total_dl  = sum(v["downloaded"] for v in all_results.values())
total_miss_local = sum(v["not_downloaded"] for v in all_results.values())
total_miss_csv = sum(v["missing_all_csv"] for v in all_results.values())
total_miss_demo_expected = sum(v["missing_in_demographics_expected"] for v in all_results.values())
total_extra_demo_expected = sum(v["extra_in_demographics_expected"] for v in all_results.values())

print(f"\nWebsite available (Synapse lists):           {total_syn}")
print(f"CSV expected (from DEMOGRAPHICS):           {total_csv}")
print(f"Downloaded locally (has EEG files):         {total_dl} / {total_syn}")
print(f"Missing / incomplete locally:               {total_miss_local}")
print(f"Website IDs missing from ALL EEG CSVs:      {total_miss_csv}")
print(f"Website IDs NOT in demographics-expected:   {total_miss_demo_expected}")
print(f"Demographics-expected IDs missing on site:  {total_extra_demo_expected}")

print(f"\n{'Folder':<10} {'Site':<6} {'Synapse':<8} {'CSV':<6} {'DL':<6} "
      f"{'MissLocal':<10} {'MissAllCSV':<10} {'MissDemo':<9} {'ExtraDemo':<9} Status")
print("-"*90)

for (group_folder, site), v in all_results.items():
    status = "[OK]" if (v["not_downloaded"] == 0 and v["missing_all_csv"] == 0) else "[WARN]"
    print(f"{group_folder:<10} {site:<6} {v['synapse_total']:<8} {v['csv_expected']:<6} {v['downloaded']:<6} "
          f"{v['not_downloaded']:<10} {v['missing_all_csv']:<10} "
          f"{v['missing_in_demographics_expected']:<9} {v['extra_in_demographics_expected']:<9} {status}")

print(f"\n{'='*90}")
print("VERIFICATION COMPLETE")
print(f"{'='*90}")
