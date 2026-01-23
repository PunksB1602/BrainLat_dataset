"""
EEG Dataset - Comprehensive CSV Analysis (NO SAVING)
====================================================
Single robust analysis script for the 6 EEG-related CSV files you shared.
Prints a report similar in spirit/structure to your earlier BrainLat script:
- file structure + integrity
- diagnosis distributions
- PD vs CN focus (demographics + cognition)
- recruitment sites (from `path`)
- completeness analysis
- validation checks (ranges, unexpected values)
- final summary + recommendations

Expected files in same folder:
  cognition_hc_eeg_data.csv
  Cognition_PD_EEG_data.csv
  demographics_hc_eeg_data.csv
  Demographics_PD_EEG_data.csv
  records_hc_eeg_data.csv
  Records_PD_EEG_data.csv
"""

import os
import re
import pandas as pd
import numpy as np
from datetime import datetime

# Display settings
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 140)
pd.set_option("display.float_format", "{:.2f}".format)

def print_section(title, width=100):
    print(f"\n{'='*width}")
    print(f"{title.center(width)}")
    print(f"{'='*width}")

def print_subsection(title):
    print(f"\n{title}")
    print("-" * len(title))

# -----------------------------------------------------------------------------
# Helpers: robust loading + normalization
# -----------------------------------------------------------------------------
def normalize_colname(c: str) -> str:
    c = str(c).strip().replace("\ufeff", "")
    c = re.sub(r"\s+", "_", c)          # spaces -> _
    c = c.replace("/", "_")
    c = re.sub(r"[^0-9a-zA-Z_]+", "", c)
    c = c.strip("_").lower()

    # normalize a few known variants
    if c in {"ideeg", "id_eeg", "id__eeg", "id_eeg_"}:
        return "id_eeg"
    if c in {"id_mri", "mri_id"}:
        return "id_mri"
    return c

def normalize_id(x):
    if pd.isna(x):
        return np.nan
    s = str(x).strip()
    # remove internal whitespace to fix " sub-40005  "
    s = re.sub(r"\s+", "", s)
    return s

def safe_read_csv(path):
    try:
        return pd.read_csv(path)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin1")

def coerce_numeric(df, cols):
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def add_country_from_path(df, path_col="path"):
    """Extract country/site code from path like '5_HC/AR' or '3_PD/CL'."""
    if path_col not in df.columns:
        df["country"] = np.nan
        return df

    def _extract(p):
        if pd.isna(p):
            return np.nan
        p = str(p).strip()
        last = p.split("/")[-1]
        last = re.sub(r"[^A-Za-z]+", "", last)
        return last.upper() if last else np.nan

    df["country"] = df[path_col].apply(_extract)
    return df

def print_basic_profile(df, keycol=None):
    print(f"   Rows: {len(df):,}")
    print(f"   Columns: {len(df.columns)}")
    print(f"   Column names: {', '.join(df.columns)}")

    print(f"\n   Data Types:")
    for col, dtype in df.dtypes.items():
        print(f"      {col:<28} {dtype}")

    print(f"\n   Missing Values:")
    missing = df.isnull().sum()
    for col, count in missing.items():
        pct = (count / len(df) * 100) if len(df) else 0
        print(f"      {col:<28} {count:>5} ({pct:>5.1f}%)")

    if keycol and keycol in df.columns:
        print(f"\n   Duplicate {keycol}: {df[keycol].duplicated().sum()}")
        print(f"   Unique subjects: {df[keycol].nunique(dropna=True)}")

# -----------------------------------------------------------------------------
# LOAD DATA
# -----------------------------------------------------------------------------
print_section("EEG DATASET - COMPREHENSIVE CSV ANALYSIS", 100)
print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

FILES = {
    "cog_hc": "cognition_hc_eeg_data.csv",
    "cog_pd": "Cognition_PD_EEG_data.csv",
    "demo_hc": "demographics_hc_eeg_data.csv",
    "demo_pd": "Demographics_PD_EEG_data.csv",
    "rec_hc": "records_hc_eeg_data.csv",
    "rec_pd": "Records_PD_EEG_data.csv",
}

dfs = {}
for k, f in FILES.items():
    if not os.path.exists(f):
        raise FileNotFoundError(f"ERROR: Missing file '{f}' in current folder.")
    df = safe_read_csv(f)
    df.columns = [normalize_colname(c) for c in df.columns]

    # standardize id_eeg where possible
    if "id_eeg" in df.columns:
        df["id_eeg"] = df["id_eeg"].apply(normalize_id)
    elif "id" in df.columns:
        # in your cognition/demographics files, "id EEG" becomes id_eeg already,
        # but as fallback, if there's only "id" and it looks like sub-xxxxx, use it.
        df["id_eeg"] = df["id"].apply(normalize_id)

    # standardize diagnosis
    if "diagnosis" in df.columns:
        df["diagnosis"] = df["diagnosis"].astype(str).str.strip().str.upper().replace({"NAN": np.nan})

    df = add_country_from_path(df, "path")

    # numeric coercions (if present)
    df = coerce_numeric(
        df,
        cols=[
            "age", "years_education", "sex", "laterality",
            "moca_total", "ifs_total_score", "mmse",
            "t1", "rest", "dwi", "mf", "eeg"
        ],
    )

    dfs[k] = df

print("\nSuccessfully loaded all 6 CSV files")

# -----------------------------------------------------------------------------
# PART 1: FILE STRUCTURE & DATA INTEGRITY
# -----------------------------------------------------------------------------
print_section("PART 1: FILE STRUCTURE & DATA INTEGRITY")

print_subsection("1.1 Cognition HC (cognition_hc_eeg_data.csv)")
print_basic_profile(dfs["cog_hc"], keycol="id_eeg")

print_subsection("1.2 Cognition PD (Cognition_PD_EEG_data.csv)")
print_basic_profile(dfs["cog_pd"], keycol="id_eeg")

print_subsection("1.3 Demographics HC (demographics_hc_eeg_data.csv)")
print_basic_profile(dfs["demo_hc"], keycol="id_eeg")

print_subsection("1.4 Demographics PD (Demographics_PD_EEG_data.csv)")
print_basic_profile(dfs["demo_pd"], keycol="id_eeg")

print_subsection("1.5 Records HC (records_hc_eeg_data.csv)")
print_basic_profile(dfs["rec_hc"], keycol="id_eeg")

print_subsection("1.6 Records PD (Records_PD_EEG_data.csv)")
print_basic_profile(dfs["rec_pd"], keycol="id_eeg")

# -----------------------------------------------------------------------------
# PART 2: DIAGNOSIS DISTRIBUTION
# -----------------------------------------------------------------------------
print_section("PART 2: DIAGNOSIS DISTRIBUTION")

def print_diag_dist(df, label):
    print_subsection(label)
    if "diagnosis" not in df.columns:
        print("   No 'diagnosis' column.")
        return
    vc = df["diagnosis"].value_counts(dropna=False).sort_index()
    total = len(df)
    print(f"\n   Total rows: {total}")
    for dx, count in vc.items():
        pct = (count / total * 100) if total else 0
        print(f"   {str(dx):<10} {count:>4} ({pct:>5.1f}%)")

print_diag_dist(dfs["demo_hc"], "2.1 Demographics HC")
print_diag_dist(dfs["demo_pd"], "2.2 Demographics PD")
print_diag_dist(dfs["cog_hc"],  "2.3 Cognition HC")
print_diag_dist(dfs["cog_pd"],  "2.4 Cognition PD")
print_diag_dist(dfs["rec_hc"],  "2.5 Records HC")
print_diag_dist(dfs["rec_pd"],  "2.6 Records PD")

# -----------------------------------------------------------------------------
# PART 3: PD vs CN FOCUS (merged analysis)
# -----------------------------------------------------------------------------
print_section("PART 3: PD vs CN CLASSIFICATION DATASET (EEG)")

# Build combined tables
demo = pd.concat([dfs["demo_hc"], dfs["demo_pd"]], ignore_index=True, sort=False)
cog  = pd.concat([dfs["cog_hc"],  dfs["cog_pd"]],  ignore_index=True, sort=False)
rec  = pd.concat([dfs["rec_hc"],  dfs["rec_pd"]],  ignore_index=True, sort=False)

# Collapse duplicates by id_eeg: keep first non-null per column
def first_nonnull(s):
    s = s.dropna()
    return s.iloc[0] if len(s) else np.nan

def collapse_by_id(df, name):
    if "id_eeg" not in df.columns:
        raise ValueError(f"{name}: missing id_eeg")
    df = df.copy()
    df["id_eeg"] = df["id_eeg"].apply(normalize_id)
    agg = {c: first_nonnull for c in df.columns if c != "id_eeg"}
    out = df.groupby("id_eeg", as_index=False).agg(agg)
    return out

demo_u = collapse_by_id(demo, "demographics")
cog_u  = collapse_by_id(cog,  "cognition")
rec_u  = collapse_by_id(rec,  "records")

# Merge
merged = demo_u.merge(cog_u, on="id_eeg", how="outer", suffixes=("_demo", "_cog"))
merged = merged.merge(rec_u, on="id_eeg", how="outer", suffixes=("", "_rec"))

# Unify diagnosis across possible columns (diagnosis, diagnosis_demo, diagnosis_cog, etc.)
diag_cols = [c for c in merged.columns if c.startswith("diagnosis")]
def unify_diagnosis(row):
    vals = []
    for c in diag_cols:
        v = row.get(c, np.nan)
        if pd.notna(v):
            vv = str(v).strip().upper()
            if vv and vv != "NAN":
                vals.append(vv)
    vals = list(dict.fromkeys(vals))
    if len(vals) == 0:
        return np.nan
    if len(vals) == 1:
        return vals[0]
    return "MISMATCH:" + "|".join(vals)

merged["diagnosis_unified"] = merged.apply(unify_diagnosis, axis=1)

# Focus PD/CN only
pd_cn = merged[merged["diagnosis_unified"].isin(["PD", "CN"])].copy()
n_pd = (pd_cn["diagnosis_unified"] == "PD").sum()
n_cn = (pd_cn["diagnosis_unified"] == "CN").sum()

print(f"\n   Target Population: {len(pd_cn)} subjects")
print(f"   - Parkinson's Disease (PD): {n_pd} subjects")
print(f"   - Cognitively Normal (CN): {n_cn} subjects")
if n_pd > 0:
    print(f"   - Class ratio: 1:{n_cn/n_pd:.2f} (PD:CN)")

mismatch_n = pd_cn["diagnosis_unified"].astype(str).str.startswith("MISMATCH:").sum()
print(f"   - Diagnosis mismatches inside PD/CN subset: {mismatch_n}")

# 3.1 Demographics comparison
print_subsection("3.1 Demographics Comparison (PD vs CN)")
for dx in ["PD", "CN"]:
    dx_data = pd_cn[pd_cn["diagnosis_unified"] == dx]
    n_total = len(dx_data)

    age = dx_data["age"].dropna() if "age" in dx_data.columns else pd.Series([], dtype=float)
    edu = dx_data["years_education"].dropna() if "years_education" in dx_data.columns else pd.Series([], dtype=float)
    sex = dx_data["sex"].dropna() if "sex" in dx_data.columns else pd.Series([], dtype=float)

    n_male = int((sex == 1).sum()) if len(sex) else 0

    print(f"\n   {dx}:")
    print(f"      Sample size: {n_total} subjects")
    if len(age):
        print(f"      Age: {age.mean():.1f} ± {age.std():.1f} years (range: {age.min():.0f}-{age.max():.0f})")
    else:
        print(f"      Age: No data available")

    if len(sex):
        print(f"      Sex: {n_male} male ({n_male/n_total*100:.1f}%), {n_total-n_male} female ({(n_total-n_male)/n_total*100:.1f}%)")
    else:
        print(f"      Sex: No data available")

    if len(edu):
        print(f"      Education: {edu.mean():.1f} ± {edu.std():.1f} years (N={len(edu)})")
    else:
        print(f"      Education: No data available")

# 3.2 Cognitive scores
print_subsection("3.2 Cognitive Scores (PD vs CN)")

def print_score(dx, col, label, max_score=None, cutoff=None):
    dx_data = pd_cn[pd_cn["diagnosis_unified"] == dx]
    if col not in dx_data.columns:
        print(f"      {dx}: {label}: column missing")
        return
    s = pd.to_numeric(dx_data[col], errors="coerce").dropna()
    if len(s) == 0:
        print(f"      {dx}: {label}: No data available")
        return
    rng = f"range: {s.min():.0f}-{s.max():.0f}"
    extra = []
    if max_score is not None:
        extra.append(f"Max: {max_score}")
    if cutoff is not None:
        extra.append(f"Cutoff: <{cutoff}")
    extra_txt = ("; " + ", ".join(extra)) if extra else ""
    print(f"      {dx}: {s.mean():.1f} ± {s.std():.1f} (N={len(s)}, {rng}){extra_txt}")

print("\n   MoCA Scores (Max: 30, Cutoff: <26 indicates impairment):")
for dx in ["PD", "CN"]:
    print_score(dx, "moca_total", "MoCA", max_score=30, cutoff=26)

print("\n   IFS Scores (Max: 30, Cutoff: <25 indicates frontal impairment):")
for dx in ["PD", "CN"]:
    print_score(dx, "ifs_total_score", "IFS", max_score=30, cutoff=25)

if "mmse" in pd_cn.columns:
    print("\n   MMSE Scores (Max: 30):")
    for dx in ["PD", "CN"]:
        print_score(dx, "mmse", "MMSE", max_score=30, cutoff=None)

# 3.3 Recruitment sites
print_subsection("3.3 Recruitment Sites (PD+CN, from path -> country)")
if "country" in pd_cn.columns:
    site_dist = pd_cn.groupby(["country", "diagnosis_unified"]).size().unstack(fill_value=0)
    site_dist["Total"] = site_dist.sum(axis=1)
    site_dist.loc["TOTAL"] = site_dist.sum()
    print("\n" + str(site_dist))
else:
    print("   No country info available (missing 'path' column).")

# -----------------------------------------------------------------------------
# PART 4: DATA COMPLETENESS
# -----------------------------------------------------------------------------
print_section("PART 4: DATA COMPLETENESS ANALYSIS")

print_subsection("4.1 Available Data for PD+CN Subjects")
print(f"\n   Total PD+CN subjects: {len(pd_cn)}")

demo_cols = [c for c in ["age", "sex", "years_education"] if c in pd_cn.columns]
cog_cols  = [c for c in ["moca_total", "ifs_total_score"] if c in pd_cn.columns]

has_demo = pd_cn[demo_cols].notna().all(axis=1).sum() if demo_cols else 0
has_moca = pd_cn["moca_total"].notna().sum() if "moca_total" in pd_cn.columns else 0
has_ifs  = pd_cn["ifs_total_score"].notna().sum() if "ifs_total_score" in pd_cn.columns else 0
has_both_cog = pd_cn[["moca_total", "ifs_total_score"]].notna().all(axis=1).sum() if all(c in pd_cn.columns for c in ["moca_total","ifs_total_score"]) else 0
has_all_core = pd_cn[demo_cols + ["moca_total","ifs_total_score"]].notna().all(axis=1).sum() if (demo_cols and all(c in pd_cn.columns for c in ["moca_total","ifs_total_score"])) else 0

n_total = len(pd_cn) if len(pd_cn) else 1

print(f"\n   Demographics only:")
if demo_cols:
    print(f"      Complete ({', '.join([c.title() for c in demo_cols])}): {has_demo} / {len(pd_cn)} ({has_demo/n_total*100:.1f}%)")
else:
    print("      Demographics columns missing")

print(f"\n   Cognitive scores:")
if "moca_total" in pd_cn.columns:
    print(f"      With MoCA: {has_moca} / {len(pd_cn)} ({has_moca/n_total*100:.1f}%)")
if "ifs_total_score" in pd_cn.columns:
    print(f"      With IFS: {has_ifs} / {len(pd_cn)} ({has_ifs/n_total*100:.1f}%)")
if all(c in pd_cn.columns for c in ["moca_total","ifs_total_score"]):
    print(f"      With both MoCA & IFS: {has_both_cog} / {len(pd_cn)} ({has_both_cog/n_total*100:.1f}%)")

print(f"\n   Complete cases:")
if demo_cols and all(c in pd_cn.columns for c in ["moca_total","ifs_total_score"]):
    print(f"      All core data (Demo + MoCA + IFS): {has_all_core} / {len(pd_cn)} ({has_all_core/n_total*100:.1f}%)")
else:
    print("      Core completeness can't be computed (missing columns)")

print_subsection("4.2 Completeness by Diagnosis")
for dx in ["PD", "CN"]:
    dx_data = pd_cn[pd_cn["diagnosis_unified"] == dx]
    n = len(dx_data) if len(dx_data) else 1
    if demo_cols and all(c in dx_data.columns for c in ["moca_total","ifs_total_score"]):
        complete = dx_data[demo_cols + ["moca_total","ifs_total_score"]].notna().all(axis=1).sum()
        print(f"\n   {dx}:")
        print(f"      Total: {len(dx_data)}")
        print(f"      Complete: {complete} ({complete/n*100:.1f}%)")
        print(f"      Missing core data: {len(dx_data) - complete} subjects")
    else:
        print(f"\n   {dx}: Total {len(dx_data)} (core completeness not computable)")

# -----------------------------------------------------------------------------
# PART 5: VALIDATION & QUALITY CHECKS
# -----------------------------------------------------------------------------
print_section("PART 5: DATA VALIDATION")

print_subsection("5.1 Quality Checks")

# Age checks
if "age" in merged.columns:
    age_issues = merged[(merged["age"] < 20) | (merged["age"] > 100)]
    print(f"   -> Suspicious age values (<20 or >100): {len(age_issues)}")
else:
    print("   -> Age column not found in merged data")

# Sex values
if "sex" in merged.columns:
    sex_vals = sorted([v for v in merged["sex"].dropna().unique()])
    print(f"   -> Sex values: {sex_vals} (0=Female, 1=Male expected)")
    if not set(sex_vals).issubset({0, 1}):
        print("      Warning: Unexpected sex values found")
else:
    print("   -> Sex column not found")

# Education range
if "years_education" in merged.columns:
    edu = merged["years_education"].dropna()
    if len(edu):
        print(f"   -> Education range: {edu.min():.0f} - {edu.max():.0f} years")
    else:
        print("   -> Education present but all missing")
else:
    print("   -> years_education column not found")

# MoCA validity
if "moca_total" in merged.columns:
    moca = merged["moca_total"].dropna()
    moca_invalid = ((moca < 0) | (moca > 30)).sum() if len(moca) else 0
    print(f"   -> MoCA scores out of range (0-30): {moca_invalid}")
else:
    print("   -> moca_total column not found")

# IFS validity
if "ifs_total_score" in merged.columns:
    ifs = merged["ifs_total_score"].dropna()
    ifs_invalid = ((ifs < 0) | (ifs > 30)).sum() if len(ifs) else 0
    print(f"   -> IFS scores out of range (0-30): {ifs_invalid}")
else:
    print("   -> ifs_total_score column not found")

# MMSE validity (if exists)
if "mmse" in merged.columns:
    mmse = merged["mmse"].dropna()
    mmse_invalid = ((mmse < 0) | (mmse > 30)).sum() if len(mmse) else 0
    print(f"   -> MMSE scores out of range (0-30): {mmse_invalid}")

# Records flags sanity
print_subsection("5.2 Records sanity (0/1 flags)")
for col in ["t1", "rest", "dwi", "eeg"]:
    if col in merged.columns:
        vals = sorted([v for v in merged[col].dropna().unique()])
        ok = set(vals).issubset({0, 1})
        print(f"   -> {col.upper():<4} unique values: {vals} (0/1 expected) OK={ok}")

if "mf" in merged.columns:
    vals = sorted([v for v in merged["mf"].dropna().unique()])
    print(f"   -> MF unique values: {vals} (often 0 or 3 in your files)")

print_subsection("5.3 Data Integrity Summary")
print(f"   -> Demographics rows: {len(demo):,} (collapsed to {len(demo_u):,} unique id_eeg)")
print(f"   -> Cognition rows:    {len(cog):,} (collapsed to {len(cog_u):,} unique id_eeg)")
print(f"   -> Records rows:      {len(rec):,} (collapsed to {len(rec_u):,} unique id_eeg)")
print(f"   -> Master merged:     {len(merged):,} unique id_eeg")
print(f"   -> PD subjects (merged PD+CN): {n_pd}")
print(f"   -> CN subjects (merged PD+CN): {n_cn}")

# -----------------------------------------------------------------------------
# PART 6: SUMMARY & RECOMMENDATIONS
# -----------------------------------------------------------------------------
print_section("PART 6: SUMMARY & RECOMMENDATIONS")

print_subsection("6.1 Dataset Summary")
diag_vc = merged["diagnosis_unified"].value_counts(dropna=False) if "diagnosis_unified" in merged.columns else pd.Series(dtype=int)
pd_n = int(diag_vc.get("PD", 0))
cn_n = int(diag_vc.get("CN", 0))
mismatch_total = merged["diagnosis_unified"].astype(str).str.startswith("MISMATCH:").sum()

print(f"""
   EEG + Cognition + Demographics + Records Dataset
   ───────────────────────────────────────────────
   Total unique subjects (id_eeg): {len(merged)}
   Diagnoses (unified): PD={pd_n}, CN={cn_n}, mismatched_labels={mismatch_total}

   PD Classification Subset:
   ───────────────────────────────────────────────
   Target subjects (PD+CN): {len(pd_cn)} ({n_pd} PD + {n_cn} CN)
""")

print_subsection("6.2 Recommendations for PD vs CN EEG Pipeline")
print("""
   1. Fix label integrity first:
      -> Investigate any 'MISMATCH:' diagnosis_unified subjects (if any).
      -> Ensure the same id_eeg has consistent diagnosis across demographics/cognition/records.

   2. Use core covariates:
      -> Age, sex, years_education should be used as confounds/covariates.

   3. Cognition as auxiliary signal:
      -> MoCA & IFS are strong clinical correlates; decide whether to:
         (a) use them as extra features, or
         (b) use them only for stratification / sanity checks.

   4. Multi-site effects:
      -> Include 'country' (from path) as covariate or do site-wise validation.

   5. Modality availability:
      -> Use records (T1/Rest/DWI/MF/eeg) to define which subjects qualify
         for EEG-only vs multimodal experiments.
""")

print_section("ANALYSIS COMPLETE", 100)
