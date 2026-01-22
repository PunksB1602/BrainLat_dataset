import pandas as pd
import synapseclient
import synapseutils
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Load EEG subject lists (PD and CN)
pd_records = pd.read_csv('Records_PD_EEG_data.csv')
cn_records = pd.read_csv('records_hc_eeg_data.csv')

# Clean subject IDs
pd_records['id_EEG'] = pd_records['id_EEG'].astype(str).str.strip()
cn_records['id_EEG'] = cn_records['id_EEG'].astype(str).str.strip()

# Extract country from path (e.g. 3_PD/AR → AR, 5_HC/CL → CL)
pd_records['country'] = pd_records['path'].astype(str).str.replace("\\", "/").str.split("/").str[-1]
cn_records['country'] = cn_records['path'].astype(str).str.replace("\\", "/").str.split("/").str[-1]

# Keep only PD/CN subjects with EEG available
pd_list = pd_records[(pd_records['diagnosis'] == 'PD') & (pd_records['eeg'] == 1)]
cn_list = cn_records[(cn_records['diagnosis'] == 'CN') & (cn_records['eeg'] == 1)]

print("="*80)
print("BRAINLAT EEG DOWNLOAD - PD + CN")
print("="*80)
print(f"\nTotal PD+CN EEG subjects: {len(pd_list) + len(cn_list)}")
print(f"PD: {len(pd_list)}")
print(f"CN: {len(cn_list)}")

# Login to Synapse
print("\nLogging into Synapse...")
syn = synapseclient.Synapse()
syn.login(authToken="eyJ0eXAiOiJKV1QiLCJraWQiOiJXN05OOldMSlQ6SjVSSzpMN1RMOlQ3TDc6M1ZYNjpKRU9VOjY0NFI6VTNJWDo1S1oyOjdaQ0s6RlBUSCIsImFsZyI6IlJTMjU2In0.eyJhY2Nlc3MiOnsic2NvcGUiOlsidmlldyIsImRvd25sb2FkIl0sIm9pZGNfY2xhaW1zIjp7fX0sInRva2VuX3R5cGUiOiJQRVJTT05BTF9BQ0NFU1NfVE9LRU4iLCJpc3MiOiJodHRwczovL3JlcG8tcHJvZC5wcm9kLnNhZ2ViYXNlLm9yZy9hdXRoL3YxIiwiYXVkIjoiMCIsIm5iZiI6MTc2OTA4NTc5NiwiaWF0IjoxNzY5MDg1Nzk2LCJqdGkiOiIzMTM4NCIsInN1YiI6IjM1NjUwMDIifQ.fyDALbB6l_QnWi36Eb9kZG-tQQPvTfH57uoXX6PO9-mQqMt9GKlEA7Ls7ZZe3jmxXwIuDf28WFc9A6CxeNr3vHA53plFlKpFUZuJG8A2bgIbGWYSqCW0T26dwCY_GBMle78x50gXP5X4dJxSxUZAX66Uy2tvDHRIFyaoLSC7VJ0TuIVOFjzHe0lLtBxxVvWpLc74RAzf61R-TeaH3uol0gQGs3bW4F7yAwlCbC5vLH3EN4_NODQ2hFwjhiYQyTVboAa7imB_2s3wPxk5nziTWoy7qkPOPweHl5TIH3JzxiQSojrtFwb21f_rnyVW6ctWDQI5NKR3Pf1avLT55YJ1ig")
print("Login successful!")

# Synapse EEG folder IDs (from website)
folder_ids = {
    ('PD', 'AR'): 'syn53622405',
    ('PD', 'CL'): 'syn53619554',
    ('CN', 'AR'): 'syn53497914',
    ('CN', 'CL'): 'syn53497784',
}

# Statistics
total_downloaded = 0
total_skipped = 0

# Download from each EEG folder
for (group, country), folder_id in folder_ids.items():
    print("\n" + "="*80)
    print(f"PROCESSING EEG FOLDER: {group} / {country}")
    print("="*80)

    # Get expected subjects from CSV
    if group == 'PD':
        expected = pd_list[pd_list['country'] == country]['id_EEG'].tolist()
    else:
        expected = cn_list[cn_list['country'] == country]['id_EEG'].tolist()

    if len(expected) == 0:
        print(f"No subjects in {group}/{country}, skipping...")
        continue

    print(f"Expected subjects: {len(expected)}")

    try:
        children = list(syn.getChildren(folder_id))
        print(f"Found {len(children)} subjects in Synapse folder")

        downloaded_this_folder = 0
        skipped_this_folder = 0

        for child in children:
            subject_id = str(child['name']).strip()

            # Download only subjects present in CSV list
            if subject_id in expected:
                print(f"  Downloading: {subject_id} (ID: {child['id']})")

                synapseutils.syncFromSynapse(
                    syn,
                    child['id'],
                    path=f'./EEG_data/{group}/{country}/{subject_id}'
                )

                downloaded_this_folder += 1
                total_downloaded += 1
            else:
                print(f" Skipping: {subject_id}")
                skipped_this_folder += 1
                total_skipped += 1

        print(f"\n{group}/{country} Summary: Downloaded {downloaded_this_folder}, Skipped {skipped_this_folder}")

    except Exception as e:
        print(f"ERROR processing {group}/{country}: {e}")
        continue

# Final summary
print("\n" + "="*80)
print("EEG DOWNLOAD COMPLETE")
print("="*80)
print(f"Total subjects downloaded: {total_downloaded}")
print(f"Total subjects skipped: {total_skipped}")
print(f"\nData saved to: ./EEG_data/")
print("Folder structure: ./EEG_data/[PD|CN]/[AR|CL]/[SUBJECT]/files")
