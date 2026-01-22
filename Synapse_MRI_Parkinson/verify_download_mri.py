import pandas as pd
import os

# Load CSV
demographic = pd.read_csv('BrainLat_Demographic_MRI.csv')
# Extract country code (handle both 2-letter like AR, PE and 3-letter like CLB, COA, COB, MXA)
demographic['country'] = demographic['MRI_ID'].str.extract(r'sub-([A-Z]+)')[0]

print("="*80)
print("DOWNLOAD VERIFICATION: CSV vs SYNAPSE vs DATA FOLDER")
print("="*80)

# All Synapse website subjects for each folder
synapse_subjects = {
    'AR': [
        'sub-AR00162', 'sub-AR00163', 'sub-AR00164', 'sub-AR00165', 'sub-AR00166',
        'sub-AR00167', 'sub-AR00168', 'sub-AR00169', 'sub-AR00170', 'sub-AR00171',
        'sub-AR00172', 'sub-AR00176', 'sub-AR00180', 'sub-AR00181', 'sub-AR00182',
        'sub-AR00185', 'sub-AR00186', 'sub-AR00187', 'sub-AR00188', 'sub-AR00191',
        'sub-AR00195', 'sub-AR00196',
        'sub-AR00401', 'sub-AR00402', 'sub-AR00403', 'sub-AR00404', 'sub-AR00405',
        'sub-AR00406', 'sub-AR00407', 'sub-AR00408', 'sub-AR00409', 'sub-AR00410',
        'sub-AR00411', 'sub-AR00412', 'sub-AR00413', 'sub-AR00414',
        'sub-AR00506', 'sub-AR00507', 'sub-AR00508', 'sub-AR00509', 'sub-AR00510',
        'sub-AR00511', 'sub-AR00512', 'sub-AR00513', 'sub-AR00514', 'sub-AR00515',
        'sub-AR00516', 'sub-AR00517', 'sub-AR00518', 'sub-AR00519', 'sub-AR00520',
        'sub-AR00522', 'sub-AR00523', 'sub-AR00524', 'sub-AR00525', 'sub-AR00526',
        'sub-AR00527', 'sub-AR00528', 'sub-AR00529', 'sub-AR00530', 'sub-AR00531',
        'sub-AR00532', 'sub-AR00533', 'sub-AR00534', 'sub-AR00535', 'sub-AR00536',
        'sub-AR00537', 'sub-AR00538', 'sub-AR00539', 'sub-AR00540', 'sub-AR00541',
        'sub-AR00542', 'sub-AR00543', 'sub-AR00544', 'sub-AR00545', 'sub-AR00546',
        'sub-AR00547', 'sub-AR00548', 'sub-AR00549', 'sub-AR00550', 'sub-AR00551',
        'sub-AR00552', 'sub-AR00553', 'sub-AR00554', 'sub-AR00555', 'sub-AR00556',
        'sub-AR00557', 'sub-AR00558', 'sub-AR00559', 'sub-AR00560'
    ],
    'CLB': [
        'sub-CLB00002', 'sub-CLB00003', 'sub-CLB00004', 'sub-CLB00005', 'sub-CLB00006',
        'sub-CLB00008', 'sub-CLB00009', 'sub-CLB00010', 'sub-CLB00011', 'sub-CLB00012',
        'sub-CLB00013', 'sub-CLB00014', 'sub-CLB00015', 'sub-CLB00017', 'sub-CLB00019',
        'sub-CLB00021', 'sub-CLB00023', 'sub-CLB00024', 'sub-CLB00025', 'sub-CLB00026',
        'sub-CLB00027', 'sub-CLB00028', 'sub-CLB00029', 'sub-CLB00030', 'sub-CLB00031',
        'sub-CLB00032', 'sub-CLB00033', 'sub-CLB00037', 'sub-CLB00038', 'sub-CLB00039',
        'sub-CLB00040', 'sub-CLB00041', 'sub-CLB00044', 'sub-CLB00045', 'sub-CLB00046',
        'sub-CLB00047', 'sub-CLB00049', 'sub-CLB00050', 'sub-CLB00051', 'sub-CLB00052',
        'sub-CLB00053', 'sub-CLB00054', 'sub-CLB00055', 'sub-CLB00056', 'sub-CLB00057',
        'sub-CLB00061', 'sub-CLB00062', 'sub-CLB00063', 'sub-CLB00066', 'sub-CLB00067',
        'sub-CLB00069', 'sub-CLB00070', 'sub-CLB00071', 'sub-CLB00072', 'sub-CLB00073',
        'sub-CLB00074', 'sub-CLB00075', 'sub-CLB00076', 'sub-CLB00077', 'sub-CLB00078',
        'sub-CLB00079', 'sub-CLB00080', 'sub-CLB00081', 'sub-CLB00082', 'sub-CLB00085',
        'sub-CLB00087', 'sub-CLB00088', 'sub-CLB00090', 'sub-CLB00091', 'sub-CLB00092',
        'sub-CLB00094', 'sub-CLB00095', 'sub-CLB00096', 'sub-CLB00097', 'sub-CLB00098',
        'sub-CLB00099', 'sub-CLB00100', 'sub-CLB00101', 'sub-CLB00102', 'sub-CLB00103',
        'sub-CLB00104', 'sub-CLB00105', 'sub-CLB00106', 'sub-CLB00107', 'sub-CLB00108',
        'sub-CLB00109', 'sub-CLB00110', 'sub-CLB00111', 'sub-CLB00113', 'sub-CLB00114',
        'sub-CLB00115', 'sub-CLB00116', 'sub-CLB00117', 'sub-CLB00118', 'sub-CLB00119',
        'sub-CLB00120', 'sub-CLB00121', 'sub-CLB00122', 'sub-CLB00123', 'sub-CLB00125',
        'sub-CLB00126', 'sub-CLB00127', 'sub-CLB00128', 'sub-CLB00129', 'sub-CLB00130',
        'sub-CLB00132', 'sub-CLB00133', 'sub-CLB00134', 'sub-CLB00135', 'sub-CLB00136',
        'sub-CLB00137', 'sub-CLB00138', 'sub-CLB00139', 'sub-CLB00140', 'sub-CLB00141',
        'sub-CLB00142', 'sub-CLB00143', 'sub-CLB00144', 'sub-CLB00145', 'sub-CLB00146',
        'sub-CLB00148', 'sub-CLB00149', 'sub-CLB00151', 'sub-CLB00152', 'sub-CLB00154',
        'sub-CLB00155', 'sub-CLB00156', 'sub-CLB00157', 'sub-CLB00158', 'sub-CLB00159',
        'sub-CLB00160', 'sub-CLB00161', 'sub-CLB00162', 'sub-CLB00163', 'sub-CLB00164',
        'sub-CLB00165', 'sub-CLB00167', 'sub-CLB00168', 'sub-CLB00170', 'sub-CLB00171',
        'sub-CLB00172', 'sub-CLB00174', 'sub-CLB00175', 'sub-CLB00176', 'sub-CLB00177',
        'sub-CLB00179', 'sub-CLB00180', 'sub-CLB00181', 'sub-CLB00182', 'sub-CLB00184',
        'sub-CLB00186', 'sub-CLB00187', 'sub-CLB00188', 'sub-CLB00189', 'sub-CLB00190',
        'sub-CLB00191', 'sub-CLB00193', 'sub-CLB00194', 'sub-CLB00195', 'sub-CLB00196',
        'sub-CLB00197', 'sub-CLB00198', 'sub-CLB00199', 'sub-CLB00200', 'sub-CLB00201',
        'sub-CLB00202', 'sub-CLB00203', 'sub-CLB00204', 'sub-CLB00205', 'sub-CLB00206',
        'sub-CLB00208', 'sub-CLB00209', 'sub-CLB00210', 'sub-CLB00211', 'sub-CLB00212',
        'sub-CLB00213', 'sub-CLB00214', 'sub-CLB00215', 'sub-CLB00216', 'sub-CLB00217',
        'sub-CLB00218', 'sub-CLB00219', 'sub-CLB00220', 'sub-CLB00221', 'sub-CLB00222',
        'sub-CLB00223', 'sub-CLB00224', 'sub-CLB00225', 'sub-CLB00226', 'sub-CLB00227',
        'sub-CLB00228', 'sub-CLB00229', 'sub-CLB00230', 'sub-CLB00232', 'sub-CLB00233',
        'sub-CLB00234', 'sub-CLB00235', 'sub-CLB00239', 'sub-CLB00240', 'sub-CLB00242',
        'sub-CLB00243', 'sub-CLB00244', 'sub-CLB00246', 'sub-CLB00247', 'sub-CLB00249',
        'sub-CLB00250', 'sub-CLB00251', 'sub-CLB00252', 'sub-CLB00253', 'sub-CLB00254',
        'sub-CLB00255', 'sub-CLB00256', 'sub-CLB00257', 'sub-CLB00258', 'sub-CLB00259',
        'sub-CLB00260', 'sub-CLB00261', 'sub-CLB00262', 'sub-CLB00263', 'sub-CLB00267',
        'sub-CLB00268', 'sub-CLB00272', 'sub-CLB00273',
        'sub-CLB00401', 'sub-CLB00402', 'sub-CLB00403', 'sub-CLB00404', 'sub-CLB00405',
        'sub-CLB00406', 'sub-CLB00408', 'sub-CLB00409', 'sub-CLB00410', 'sub-CLB00411',
        'sub-CLB00412', 'sub-CLB00413', 'sub-CLB00414', 'sub-CLB00415', 'sub-CLB00416',
        'sub-CLB00417', 'sub-CLB00418', 'sub-CLB00419', 'sub-CLB00420', 'sub-CLB00421',
        'sub-CLB00422',
        'sub-CLB01009', 'sub-CLB10001', 'sub-CLB10002', 'sub-CLB10004', 'sub-CLB10005',
        'sub-CLB10006', 'sub-CLB10007', 'sub-CLB10011', 'sub-CLB10012', 'sub-CLB10013',
        'sub-CLB10014', 'sub-CLB10015', 'sub-CLB10016', 'sub-CLB10017'
    ],
    'COA': [
        'sub-COA00001', 'sub-COA00002', 'sub-COA00003', 'sub-COA00004', 'sub-COA00005',
        'sub-COA00006', 'sub-COA00007', 'sub-COA00008', 'sub-COA00009', 'sub-COA00010',
        'sub-COA00011', 'sub-COA00012', 'sub-COA00013', 'sub-COA00014', 'sub-COA00015',
        'sub-COA00016', 'sub-COA00017', 'sub-COA00018', 'sub-COA00020', 'sub-COA00021',
        'sub-COA00022', 'sub-COA00023', 'sub-COA00024', 'sub-COA00025', 'sub-COA00026',
        'sub-COA00027', 'sub-COA00028', 'sub-COA00029', 'sub-COA00101', 'sub-COA00201',
        'sub-COA00301', 'sub-COA00401', 'sub-COA00501', 'sub-COA00601', 'sub-COA00701',
        'sub-COA00801', 'sub-COA00901', 'sub-COA01001', 'sub-COA01101', 'sub-COA01201',
        'sub-COA01301', 'sub-COA01401', 'sub-COA01501', 'sub-COA01601', 'sub-COA01701',
        'sub-COA01801', 'sub-COA01901', 'sub-COA02001', 'sub-COA02101', 'sub-COA02201'
    ],
    'COB': [
        'sub-COB001', 'sub-COB002', 'sub-COB003', 'sub-COB004', 'sub-COB005',
        'sub-COB008', 'sub-COB009', 'sub-COB010', 'sub-COB012', 'sub-COB013',
        'sub-COB014', 'sub-COB016', 'sub-COB019', 'sub-COB020', 'sub-COB021',
        'sub-COB022', 'sub-COB025', 'sub-COB026', 'sub-COB027', 'sub-COB028',
        'sub-COB029', 'sub-COB030', 'sub-COB031', 'sub-COB033', 'sub-COB035',
        'sub-COB038', 'sub-COB039', 'sub-COB040', 'sub-COB042', 'sub-COB043',
        'sub-COB044', 'sub-COB045', 'sub-COB046', 'sub-COB047', 'sub-COB048',
        'sub-COB049', 'sub-COB050', 'sub-COB052', 'sub-COB053', 'sub-COB054',
        'sub-COB055', 'sub-COB056', 'sub-COB057', 'sub-COB059', 'sub-COB060',
        'sub-COB061', 'sub-COB063', 'sub-COB065', 'sub-COB066', 'sub-COB067',
        'sub-COB069', 'sub-COB073', 'sub-COB075', 'sub-COB077', 'sub-COB078',
        'sub-COB082', 'sub-COB083', 'sub-COB084', 'sub-COB085', 'sub-COB086',
        'sub-COB087', 'sub-COB089', 'sub-COB090', 'sub-COB091', 'sub-COB092',
        'sub-COB093', 'sub-COB094', 'sub-COB095', 'sub-COB096', 'sub-COB097',
        'sub-COB098', 'sub-COB099', 'sub-COB101', 'sub-COB102', 'sub-COB103',
        'sub-COB104', 'sub-COB105', 'sub-COB106', 'sub-COB107', 'sub-COB109',
        'sub-COB111', 'sub-COB116', 'sub-COB117', 'sub-COB118', 'sub-COB119',
        'sub-COB120', 'sub-COB121', 'sub-COB122', 'sub-COB123', 'sub-COB125',
        'sub-COB126', 'sub-COB127', 'sub-COB128', 'sub-COB129', 'sub-COB130',
        'sub-COB131', 'sub-COB132', 'sub-COB133', 'sub-COB134', 'sub-COB135',
        'sub-COB136', 'sub-COB137', 'sub-COB138', 'sub-COB139', 'sub-COB140',
        'sub-COB141', 'sub-COB142', 'sub-COB143', 'sub-COB145', 'sub-COB146',
        'sub-COB147', 'sub-COB148', 'sub-COB149', 'sub-COB150', 'sub-COB151',
        'sub-COB152', 'sub-COB153', 'sub-COB154', 'sub-COB155', 'sub-COB156',
        'sub-COB158', 'sub-COB159', 'sub-COB161', 'sub-COB162', 'sub-COB163',
        'sub-COB164', 'sub-COB165', 'sub-COB166', 'sub-COB167', 'sub-COB168',
        'sub-COB169', 'sub-COB170', 'sub-COB171', 'sub-COB172', 'sub-COB173',
        'sub-COB174', 'sub-COB175', 'sub-COB176', 'sub-COB177', 'sub-COB178',
        'sub-COB179', 'sub-COB180', 'sub-COB181', 'sub-COB182', 'sub-COB183',
        'sub-COB184', 'sub-COB185', 'sub-COB186', 'sub-COB187', 'sub-COB188',
        'sub-COB189'
    ],
    'MXA': [
        'sub-MXA00014', 'sub-MXA00017'
    ],
    'PE': [
        'sub-PE00001', 'sub-PE00002', 'sub-PE00003', 'sub-PE00004', 'sub-PE00006',
        'sub-PE00007', 'sub-PE00008', 'sub-PE00009', 'sub-PE00010', 'sub-PE00011',
        'sub-PE00012', 'sub-PE00013', 'sub-PE00014', 'sub-PE00015', 'sub-PE00016',
        'sub-PE00017', 'sub-PE00018', 'sub-PE00019', 'sub-PE00020', 'sub-PE00021',
        'sub-PE00022', 'sub-PE00023', 'sub-PE00024', 'sub-PE00025', 'sub-PE00026',
        'sub-PE00027', 'sub-PE00028', 'sub-PE00029', 'sub-PE00030', 'sub-PE00031',
        'sub-PE00032', 'sub-PE00033', 'sub-PE00034', 'sub-PE00035', 'sub-PE00036',
        'sub-PE00037', 'sub-PE00038', 'sub-PE00039', 'sub-PE00040', 'sub-PE00041',
        'sub-PE00042', 'sub-PE00043', 'sub-PE00044', 'sub-PE00045', 'sub-PE00046',
        'sub-PE00047', 'sub-PE00048', 'sub-PE00049', 'sub-PE00050', 'sub-PE00051',
        'sub-PE00052', 'sub-PE00053', 'sub-PE00054', 'sub-PE00055', 'sub-PE00056',
        'sub-PE00057', 'sub-PE00058', 'sub-PE00059', 'sub-PE00060', 'sub-PE00063',
        'sub-PE00066', 'sub-PE00084', 'sub-PE00086', 'sub-PE00088', 'sub-PE00089',
        'sub-PE00090', 'sub-PE00091', 'sub-PE00092', 'sub-PE00093', 'sub-PE00095',
        'sub-PE00097', 'sub-PE00101', 'sub-PE00103', 'sub-PE00105', 'sub-PE00108',
        'sub-PE00111', 'sub-PE00112', 'sub-PE00114', 'sub-PE00115', 'sub-PE00117',
        'sub-PE00124'
    ]
}

# Downloaded counts from synapse_download_pdcn.py
downloaded_counts = {
    'AR': 35,
    'CLB': 106,
    'COA': 50,
    'COB': 45,
    'MXA': 2,
    'PE': 7
}

# Process each folder
all_results = {}

for country, subjects in synapse_subjects.items():
    print(f"\n{'='*80}")
    print(f"{country} FOLDER VERIFICATION")
    print(f"{'='*80}")
    
    # 1. Get PD+CN subjects from CSV for this country
    csv_pdcn = demographic[(demographic['country'] == country) & 
                           (demographic['diagnosis'].isin(['PD', 'CN']))]
    csv_pd = csv_pdcn[csv_pdcn['diagnosis'] == 'PD']['MRI_ID'].tolist()
    csv_cn = csv_pdcn[csv_pdcn['diagnosis'] == 'CN']['MRI_ID'].tolist()
    
    print(f"\n1. CSV EXPECTED (PD+CN):")
    print(f"   Total: {len(csv_pdcn)} subjects")
    print(f"   PD: {len(csv_pd)} subjects")
    if csv_pd:
        print(f"      {', '.join(sorted(csv_pd))}")
    print(f"   CN: {len(csv_cn)} subjects")
    if csv_cn:
        print(f"      {', '.join(sorted(csv_cn))}")
    
    # 2. Check each Synapse website subject's status in CSV
    available_pdcn = []
    skipped_others = []
    missing_from_csv = []
    
    for subj in sorted(subjects):
        if subj in demographic['MRI_ID'].values:
            dx = demographic[demographic['MRI_ID'] == subj]['diagnosis'].values[0]
            if dx in ['PD', 'CN']:
                available_pdcn.append((subj, dx))
            else:
                skipped_others.append((subj, dx))
        else:
            missing_from_csv.append(subj)
    
    available_pd = [subj for subj, dx in available_pdcn if dx == 'PD']
    available_cn = [subj for subj, dx in available_pdcn if dx == 'CN']
    
    print(f"\n2. SYNAPSE WEBSITE (PD+CN Available):")
    print(f"   Total on website: {len(subjects)} subjects")
    print(f"   Available PD+CN: {len(available_pdcn)} subjects")
    print(f"   PD: {len(available_pd)} subjects")
    if available_pd:
        print(f"      {', '.join(sorted(available_pd))}")
    print(f"   CN: {len(available_cn)} subjects")
    if available_cn:
        print(f"      {', '.join(sorted(available_cn))}")
    print(f"   Skipped (AD/FTD/MS): {len(skipped_others)} subjects")
    print(f"   Missing from CSV: {len(missing_from_csv)} subjects")
    
    # 3. Verify actual downloads in data folder
    data_folder = f'./MRI_data/{country}'
    downloaded = []
    not_downloaded = []
    
    for subj, dx in available_pdcn:
        subject_path = os.path.join(data_folder, subj)
        if os.path.exists(subject_path) and os.path.isdir(subject_path):
            downloaded.append((subj, dx))
        else:
            not_downloaded.append((subj, dx))
    
    downloaded_pd = [subj for subj, dx in downloaded if dx == 'PD']
    downloaded_cn = [subj for subj, dx in downloaded if dx == 'CN']
    
    print(f"\n3. DATA FOLDER VERIFICATION:")
    print(f"   Path: {data_folder}")
    print(f"   Downloaded: {len(downloaded)} / {len(available_pdcn)} available")
    print(f"   PD: {len(downloaded_pd)} subjects")
    if downloaded_pd:
        print(f"      {', '.join(sorted(downloaded_pd))}")
    print(f"   CN: {len(downloaded_cn)} subjects")
    if downloaded_cn:
        print(f"      {', '.join(sorted(downloaded_cn))}")
    
    if not_downloaded:
        print(f"\n   [WARN] NOT Downloaded: {len(not_downloaded)} subjects")
        for subj, dx in not_downloaded:
            print(f"      {subj} ({dx})")
    else:
        print(f"\n   [OK] All available PD+CN subjects downloaded!")
    
    # Store results
    all_results[country] = {
        'csv_total': len(csv_pdcn),
        'csv_pd': len(csv_pd),
        'csv_cn': len(csv_cn),
        'synapse_total': len(subjects),
        'synapse_available': len(available_pdcn),
        'synapse_pd': len(available_pd),
        'synapse_cn': len(available_cn),
        'synapse_skipped': len(skipped_others),
        'synapse_missing': len(missing_from_csv),
        'downloaded_total': len(downloaded),
        'downloaded_pd': len(downloaded_pd),
        'downloaded_cn': len(downloaded_cn),
        'not_downloaded': len(not_downloaded)
    }

# Final Summary
print(f"\n{'='*80}")
print("OVERALL SUMMARY - ALL 6 FOLDERS")
print(f"{'='*80}")

total_csv = sum(r['csv_total'] for r in all_results.values())
total_csv_pd = sum(r['csv_pd'] for r in all_results.values())
total_csv_cn = sum(r['csv_cn'] for r in all_results.values())

total_synapse = sum(r['synapse_total'] for r in all_results.values())
total_available = sum(r['synapse_available'] for r in all_results.values())
total_synapse_pd = sum(r['synapse_pd'] for r in all_results.values())
total_synapse_cn = sum(r['synapse_cn'] for r in all_results.values())
total_skipped = sum(r['synapse_skipped'] for r in all_results.values())
total_missing = sum(r['synapse_missing'] for r in all_results.values())

total_downloaded = sum(r['downloaded_total'] for r in all_results.values())
total_downloaded_pd = sum(r['downloaded_pd'] for r in all_results.values())
total_downloaded_cn = sum(r['downloaded_cn'] for r in all_results.values())
total_not_downloaded = sum(r['not_downloaded'] for r in all_results.values())

print(f"\n1. CSV EXPECTED:")
print(f"   Total PD+CN: {total_csv} subjects")
print(f"   - PD: {total_csv_pd}")
print(f"   - CN: {total_csv_cn}")

print(f"\n2. SYNAPSE WEBSITE:")
print(f"   Total on website: {total_synapse} subjects")
print(f"   Available PD+CN: {total_available} subjects")
print(f"   - PD: {total_synapse_pd}")
print(f"   - CN: {total_synapse_cn}")
print(f"   Skipped (AD/FTD/MS): {total_skipped} subjects")
print(f"   Missing from CSV: {total_missing} subjects")

print(f"\n3. DATA FOLDER:")
print(f"   Downloaded: {total_downloaded} / {total_available} available")
print(f"   - PD: {total_downloaded_pd}")
print(f"   - CN: {total_downloaded_cn}")

if total_not_downloaded > 0:
    print(f"\n   [WARN] NOT Downloaded: {total_not_downloaded} subjects")
    status = "DISCREPANCIES FOUND"
else:
    print(f"\n   [OK] SUCCESS! All available PD+CN subjects downloaded!")
    status = "ALL DOWNLOADS VERIFIED!"

print(f"\n{'='*80}")
print("FOLDER-BY-FOLDER BREAKDOWN")
print(f"{'='*80}")
print(f"{'Folder':<8} {'CSV':<8} {'Synapse':<10} {'Downloaded':<12} {'PD':<6} {'CN':<6} {'Status':<10}")
print("-"*80)
for country, result in all_results.items():
    dl_status = "[OK]" if result['synapse_available'] == result['downloaded_total'] else "[WARN]"
    print(f"{country:<8} {result['csv_total']:<8} {result['synapse_available']:<10} {result['downloaded_total']:<12} "
          f"{result['downloaded_pd']:<6} {result['downloaded_cn']:<6} {dl_status:<10}")

print(f"\n{'='*80}")
print("VERIFICATION COMPLETE")
print(f"{'='*80}")
print(f"Status: {status}")
print(f"Dataset ready for PD vs CN classification: {total_downloaded_pd} PD + {total_downloaded_cn} CN = {total_downloaded} subjects")

