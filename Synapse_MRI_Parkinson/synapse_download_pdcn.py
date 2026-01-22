import pandas as pd
import synapseclient 
import synapseutils 
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Load the PD+CN subject list
demographic = pd.read_csv('BrainLat_Demographic_MRI.csv')
demographic['country'] = demographic['MRI_ID'].str.extract(r'sub-([A-Z]+)')[0]

# Filter for PD and CN only
pd_cn = demographic[demographic['diagnosis'].isin(['PD', 'CN'])]

print("="*80)
print("BRAINLAT PD+CN DOWNLOAD - ALL FOLDERS")
print("="*80)
print(f"\nTotal PD+CN subjects to download: {len(pd_cn)}")
print(f"PD: {(pd_cn['diagnosis'] == 'PD').sum()}")
print(f"CN: {(pd_cn['diagnosis'] == 'CN').sum()}")

# Login to Synapse
print("\nLogging into Synapse...")
syn = synapseclient.Synapse() 
syn.login(authToken="eyJ0eXAiOiJKV1QiLCJraWQiOiJXN05OOldMSlQ6SjVSSzpMN1RMOlQ3TDc6M1ZYNjpKRU9VOjY0NFI6VTNJWDo1S1oyOjdaQ0s6RlBUSCIsImFsZyI6IlJTMjU2In0.eyJhY2Nlc3MiOnsic2NvcGUiOlsidmlldyIsImRvd25sb2FkIl0sIm9pZGNfY2xhaW1zIjp7fX0sInRva2VuX3R5cGUiOiJQRVJTT05BTF9BQ0NFU1NfVE9LRU4iLCJpc3MiOiJodHRwczovL3JlcG8tcHJvZC5wcm9kLnNhZ2ViYXNlLm9yZy9hdXRoL3YxIiwiYXVkIjoiMCIsIm5iZiI6MTc2ODQ0ODU3OSwiaWF0IjoxNzY4NDQ4NTc5LCJqdGkiOiIzMTA0NCIsInN1YiI6IjM1NjUwMDIifQ.ONQ5PPhEvAaBsoyAZr1dnEMFr-dpoCk58c5gfM5PGV_2ZJd564oVV5MLP0q9dnc1qGC3tZCloMDzu_M0j46i-1VriYRRZG0DgfPh3s2GRCKFcw20nDetL28eAC0H9uBe3KNpL8GJ9QZoqmadgsrw1iHXqScOH57Z4HXRmB2blllYNeo9e26UTRpNs7O8QOF-fyKWtzssg-gSex8sFoQt93_r8V8FuBw63HmNBRsd_Ni5YWoM0KBP_4SdGhczkFWnbsc8eEWUVZn-cJHLqoLlONwpOLzy-EuqVfeFee9wFOjcmlC5EaZ83OcpZnVaaxxLe6WEtmiH49u2O5y585V2EQ")
print("Login successful!")

# Synapse folder IDs from the website
folder_ids = {
    'AR': 'syn54002190',  # Argentina
    'CLB': 'syn54023101',  # Chile B
    'COA': 'syn54014630',  # Colombia A
    'COB': 'syn54015826',  # Colombia B
    'PE': 'syn54014195',  # Peru
    'MXA': 'syn54013943',  # Mexico A
}

# Statistics
total_downloaded = 0
total_skipped = 0

# Download from each folder
for country, folder_id in folder_ids.items():
    print("\n" + "="*80)
    print(f"PROCESSING FOLDER: {country}")
    print("="*80)
    
    # Get PD+CN subjects for this country
    pd_cn_country = pd_cn[pd_cn['country'] == country]['MRI_ID'].tolist()
    
    if len(pd_cn_country) == 0:
        print(f"No PD/CN subjects in {country}, skipping...")
        continue
    
    print(f"Expected PD+CN subjects: {len(pd_cn_country)}")
    
    # Get all children in this folder
    try:
        children = list(syn.getChildren(folder_id))
        print(f"Found {len(children)} subjects in Synapse folder")
        
        downloaded_this_folder = 0
        skipped_this_folder = 0
        
        for child in children:
            subject_id = child['name']  # e.g., 'sub-AR00001'
            
            # Check if this subject is in our PD+CN list
            if subject_id in pd_cn_country:
                print(f"  Downloading: {subject_id} (ID: {child['id']})")
                
                # Download with proper folder structure (each subject in its own folder)
                synapseutils.syncFromSynapse(
                    syn, 
                    child['id'], 
                    path=f'./data/{country}/{subject_id}'
                )
                downloaded_this_folder += 1
                total_downloaded += 1
            else:
                print(f" Skipping: {subject_id} (not PD or CN)")
                skipped_this_folder += 1
                total_skipped += 1
        
        print(f"\n{country} Summary: Downloaded {downloaded_this_folder}, Skipped {skipped_this_folder}")
        
    except Exception as e:
        print(f"ERROR processing {country}: {e}")
        continue

# Final summary
print("\n" + "="*80)
print("DOWNLOAD COMPLETE")
print("="*80)
print(f"Total subjects downloaded: {total_downloaded}")
print(f"Total subjects skipped: {total_skipped}")
print(f"\nData saved to: ./data/")
print("Folder structure: ./data/[COUNTRY]/[SUBJECT]/[MODALITY]/files")
