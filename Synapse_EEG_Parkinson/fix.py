import os
import mne

# Base directory for the EEG data (accounting for the EEG_data subfolder)
base_dir = r"D:\Datasets\Synapse\Synapse_EEG_Parkinson\EEG_data"

print("============================================================")
print("1. FIXING TYPO FOR sub-40015")
print("============================================================")
typo_set = os.path.join(base_dir, r"3_PD\CL\sub-40015\eeg\s00415_ch_pd_reject.set")
correct_set = os.path.join(base_dir, r"3_PD\CL\sub-40015\eeg\s40015_ch_pd_reject.set")

if os.path.exists(typo_set):
    os.rename(typo_set, correct_set)
    print(f" Fixed: Renamed {os.path.basename(typo_set)} -> {os.path.basename(correct_set)}")
elif os.path.exists(correct_set):
    print(" Already fixed.")
else:
    print(f" Could not find file to rename at: {typo_set}")

print("\n============================================================")
print("2. TESTING UNPAIRED HC .SET FILES FOR EMBEDDED DATA")
print("============================================================")

hc_cl_dir = os.path.join(base_dir, r"5_HC\CL")
unpaired_hc_subjects = [
    "sub-100013", "sub-100019", "sub-100023", "sub-100025", "sub-100027",
    "sub-100032", "sub-100036", "sub-100039", "sub-100040", "sub-100041",
    "sub-100042", "sub-100044", "sub-100045", "sub-100046"
]

embedded_count = 0
missing_count = 0

for sub in unpaired_hc_subjects:
    set_file = os.path.join(hc_cl_dir, sub, "eeg", f"s6_{sub}_rs_eeg.set")
    
    if os.path.exists(set_file):
        try:
            # verbose='error' keeps the console clean from MNE warnings
            raw = mne.io.read_raw_eeglab(set_file, preload=False, verbose='error')
            print(f" {sub}: SUCCESS (Data is embedded)")
            embedded_count += 1
        except Exception as e:
            print(f" {sub}: FAILED - {e}")
            missing_count += 1
    else:
        print(f" {sub}: File not found at {set_file}")

print("\n============================================================")
print(f"RESULTS: {embedded_count} Embedded | {missing_count} Genuinely Missing")
print("============================================================")