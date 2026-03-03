import os

root = r"D:\Datasets\Synapse\Synapse_EEG_Parkinson\EEG_data"
counts = {'.fdt': 0, '.set': 0}

paired_folders = []
unpaired_folders = []

for dirpath, _, filenames in os.walk(root):
    set_files  = {os.path.splitext(f)[0] for f in filenames if f.lower().endswith('.set')}
    fdt_files  = {os.path.splitext(f)[0] for f in filenames if f.lower().endswith('.fdt')}

    counts['.set'] += len(set_files)
    counts['.fdt'] += len(fdt_files)

    paired   = set_files & fdt_files          # names present in both
    only_set = set_files - fdt_files          # .set without .fdt
    only_fdt = fdt_files - set_files          # .fdt without .set

    rel = os.path.relpath(dirpath, root)

    if paired:
        for name in sorted(paired):
            paired_folders.append((rel, name))

    if only_set:
        for name in sorted(only_set):
            unpaired_folders.append((rel, name + '.set', 'missing .fdt'))

    if only_fdt:
        for name in sorted(only_fdt):
            unpaired_folders.append((rel, name + '.fdt', 'missing .set'))

# ── Summary counts ────────────────────────────────────────────────────────────
print("=" * 60)
print(f"  .fdt files : {counts['.fdt']}")
print(f"  .set files : {counts['.set']}")
print(f"  Total      : {sum(counts.values())}")
print("=" * 60)

# ── Paired folders ────────────────────────────────────────────────────────────
print(f"\n[PAIRED]  ({len(paired_folders)} pairs found)")
print("-" * 60)
for folder, name in paired_folders:
    print(f"  {folder}  ->  {name}(.set + .fdt)")

# ── Unpaired folders ──────────────────────────────────────────────────────────
print(f"\n[UNPAIRED]  ({len(unpaired_folders)} files without a pair)")
print("-" * 60)
if unpaired_folders:
    for folder, fname, reason in unpaired_folders:
        print(f"  {folder}  ->  {fname}  ({reason})")
else:
    print("  None — all files are paired!")
