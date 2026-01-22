# BrainLat Dataset - Multimodal Neuroimaging of Neurodegenerative Diseases

**Synapse Project ID:** syn51549340  
**DOI:** https://doi.org/10.7303/syn51549340  
**License:** CC0 (Public Domain Dedication)

## Overview

The Latin American Brain Health Institute (BrainLat) dataset comprises multimodal neuroimaging data of 780 participants from Latin America. This dataset represents the first regional collection of clinical and cognitive assessments, anatomical MRI, resting-state fMRI, diffusion-weighted MRI (DWI), and high-density resting-state EEG in dementia patients from underrepresented backgrounds.

**Key Features:**
- **Total Participants:** 780 subjects
- **Age Range:** 21-89 years (mean: 62.7 ± 9.5 years)
- **Countries:** 5 Latin American countries (Argentina, Chile, Colombia, Mexico, Peru)
- **Modalities:** T1w anatomical MRI, resting-state fMRI, DWI, high-density EEG
- **Clinical Groups:** AD, bvFTD, MS, PD, and healthy controls

---

## Dataset Composition

### Participants by Diagnosis

| Diagnosis | Full Name | N | Description |
|-----------|-----------|---|-------------|
| **AD** | Alzheimer's Disease | 278 | Neurodegenerative disease affecting memory and cognition |
| **bvFTD** | Behavioral Variant Frontotemporal Dementia | 163 | Dementia affecting behavior and personality |
| **PD** | Parkinson's Disease | 57 | Movement disorder with cognitive symptoms |
| **MS** | Multiple Sclerosis | 32 | Autoimmune disease affecting CNS |
| **CN/HC** | Cognitively Normal / Healthy Controls | 250 | Age-matched healthy participants |
| **Total** | | **780** | |

### Focus of This Download: PD vs CN Classification

This repository contains data for **245 subjects**:
- **Parkinson's Disease (PD):** 56 subjects
- **Cognitively Normal (CN):** 189 subjects

Subjects with AD, bvFTD, and MS were excluded to focus on PD classification.

---

## Recruitment Centers and Site Codes

The dataset was collected through the Multi-Partner Consortium to Expand Dementia Research in Latin America (ReDLat). Each recruitment site has a unique identifier used in subject IDs.

### Site Code Mapping

| Site Code | Country | Institution | Full Name |
|-----------|---------|-------------|-----------|
| **AR** | 🇦🇷 Argentina | CNC-UdeSA | Centro de Neurociencia Cognitiva, Universidad de San Andrés, Buenos Aires |
| **CLB** | 🇨🇱 Chile | GERO | Neurology Department, Geroscience Center for Brain Health and Metabolism, Santiago |
| **CLA** | 🇨🇱 Chile | CICA | Centro de Investigación Clínica Avanzada (CICA), Hospital Clínico Universidad de Chile |
| **COA** | 🇨🇴 Colombia | UV | Universidad del Valle, Cali |
| **COB** | 🇨🇴 Colombia | AI-PUJB | Aging Institute, Pontificia Universidad Javeriana, Bogotá |
| **MXA** | 🇲🇽 Mexico | INCMNM | Geriatrics Dept, Instituto Nacional de Ciencias Médicas y Nutrición Salvador Zubirán, Mexico City |
| **MXB** | 🇲🇽 Mexico | INNN | Instituto Nacional de Neurología y Neurocirugía, Ciudad de México |
| **PE** | 🇵🇪 Peru | UCIDP-IPN | Unit Cognitive Impairment and Dementia Prevention, Peruvian Institute of Neurosciences, Lima |

### Country Codes (ISO Standard)

- **AR:** Argentina
- **CL:** Chile  
- **CO:** Colombia
- **MX:** Mexico
- **PE:** Peru

**Note:** Site codes include both country identifier and site-specific letter:
- **AR** = Argentina site A
- **CLB** = Chile site B (GERO Santiago)
- **COA** = Colombia site A (Universidad del Valle)
- **COB** = Colombia site B (Pontificia Universidad Javeriana)
- **MXA** = Mexico site A (INCMNM)
- **PE** = Peru (single site)

---

## Subject ID Format

Subject IDs follow the format: `sub-[SITE][NUMBER]`

**Examples:**
- `sub-AR00401` - Argentina, subject 401 (PD patient)
- `sub-CLB00044` - Chile site B (GERO), subject 44 (CN)
- `sub-COA00101` - Colombia site A (UV Cali), subject 101 (PD patient)
- `sub-COB069` - Colombia site B (PUJB Bogotá), subject 69 (CN)
- `sub-MXA00014` - Mexico site A, subject 14 (CN)
- `sub-PE00101` - Peru, subject 101 (CN)

### EEG Subject IDs (Resting-State EEG)

EEG subject IDs follow a different format from MRI IDs and are typically:

- **PD EEG IDs:** `sub-40001`, `sub-40004`, ...
- **HC/CN EEG IDs:** `sub-10001`, `sub-100010`, ...

> Do not assume EEG IDs match MRI IDs unless you have an explicit mapping (e.g., `EEG_ID ↔ MRI_ID`).

---

## Data Structure

### Downloaded Data Organization
```text
data/
├── AR/ # Argentina (Buenos Aires)
│ ├── sub-AR00401/
│ │ ├── anat/ # T1-weighted anatomical MRI
│ │ ├── dwi/  # Diffusion-weighted imaging
│ │ └── func/ # Resting-state functional MRI
│ ├── sub-AR00402/
│ └── ...
├── CLB/ # Chile - GERO Santiago
│ ├── sub-CLB00044/
│ └── ...
├── COA/ # Colombia - Universidad del Valle (Cali)
│ ├── sub-COA00101/
│ └── ...
├── COB/ # Colombia - PUJB Bogotá
│ ├── sub-COB069/
│ └── ...
├── MXA/ # Mexico - INCMNM Mexico City
│ ├── sub-MXA00014/
│ └── ...
└── PE/ # Peru (Lima)
  ├── sub-PE00101/
  └── ...
```


### EEG Downloaded Data Organization
```text
EEG_data/
├── 3_PD/
│ ├── AR/ # Parkinson's (Argentina)
│ └── CL/ # Parkinson's (Chile)
└── 5_HC/
  ├── AR/ # Healthy Controls / CN (Argentina)
  └── CL/ # Healthy Controls / CN (Chile)
```

**EEG File Format (EEGLAB):**
- `*.set` (header/metadata)
- `*.fdt` (binary signal data)

---

### MRI Modalities

Each subject folder contains up to three subdirectories:

1. **anat/** - Anatomical MRI
   - T1-weighted structural images
   - Format: NIfTI (.nii.gz)
   - Used for: Brain morphometry, cortical thickness, volumetric analysis

2. **dwi/** - Diffusion-Weighted Imaging
   - Multi-shell diffusion MRI
   - Format: NIfTI + .bval + .bvec files
   - Used for: White matter tractography, microstructural analysis

3. **func/** - Functional MRI
   - Resting-state BOLD fMRI
   - Format: NIfTI (.nii.gz)
   - Used for: Functional connectivity, network analysis

---

## Dataset Statistics

### Downloaded Data Summary (PD + CN Only)

| Folder | CSV Expected | Synapse Available | Downloaded | PD | CN |
|--------|--------------|-------------------|------------|----|----|
| **AR** | 92 | 35 | 35 | 13 | 22 |
| **CLB** | 106 | 106 | 106 | 21 | 85 |
| **COA** | 50 | 50 | 50 | 22 | 28 |
| **COB** | 45 | 45 | 45 | 0 | 45 |
| **MXA** | 2 | 2 | 2 | 0 | 2 |
| **PE** | 7 | 7 | 7 | 0 | 7 |
| **TOTAL** | **302** | **245** | **245** | **56** | **189** |

**Download Status:**  100% Complete (245/245 available subjects downloaded)

### EEG Downloaded Data Summary (PD + CN/HC)
> EEG data are available only for Argentina and Chile sites and represent a partially overlapping cohort with the MRI dataset.

| Folder | Synapse Available | Downloaded | PD | CN/HC |
|--------|-------------------|------------|----|-------|
| **3_PD/AR** | 7  | 7  | 7  | 0  |
| **3_PD/CL** | 22 | 22 | 22 | 0  |
| **5_HC/AR** | 19 | 19 | 0  | 19 |
| **5_HC/CL** | 27 | 27 | 0  | 27 |
| **TOTAL**   | **75** | **75** | **29** | **46** |

**EEG Download Status:** 100% Complete (75/75 available subjects downloaded)

**Note on duplicates (EEG CSVs):**
- PD EEG CSVs contain **duplicate `id_eeg` entries** (6 duplicates), so the **unique PD subject count is 23** (not 29).
- Recommended EEG ML cohort (unique PD+CN): **69 subjects** = **23 PD + 46 CN**.

---

### Demographics by Diagnosis

| Group | N | Age (Mean ± SD) | Male % | Female % |
|-------|---|-----------------|---------|----------|
| **PD** | 57 | 69.7 ± 7.8 | 70.2% | 29.8% |
| **CN** | 247 | 68.0 ± 8.9 | 34.0% | 66.0% |

### Cognitive Assessment Scores

| Group | MoCA (Mean ± SD) | IFS (Mean ± SD) |
|-------|------------------|-----------------|
| **PD** | 23.2 ± 4.0 | 21.7 ± 5.3 |
| **CN** | 26.1 ± 3.0 | 24.8 ± 3.8 |

**Note:**
- **MoCA:** Montreal Cognitive Assessment (max score: 30)
- **IFS:** INECO Frontal Screening (max score: 30)
- Lower scores indicate greater cognitive impairment

---

## Data Files

### CSV Files

1. **BrainLat_Demographic_MRI.csv**
   - Demographics: age, sex, education
   - Clinical diagnosis
   - MRI ID for each subject
   - Total: 762 subjects with MRI data

2. **BrainLat_Cognition_MRI.csv**
   - Cognitive assessment scores (MoCA, IFS, etc.)
   - Neuropsychological test results
   - Total: 765 subjects with cognitive data

3. **EEG CSV Files (6 total)**
   - **Demographics:** `demographics_hc_eeg_data.csv`, `Demographics_PD_EEG_data.csv`
   - **Cognition:** `cognition_hc_eeg_data.csv`, `Cognition_PD_EEG_data.csv`
   - **Records/Modality flags:** `records_hc_eeg_data.csv`, `Records_PD_EEG_data.csv`

These EEG CSVs include:
- `id_eeg`, diagnosis, demographics (age/sex/education), and available cognition scores (MoCA/IFS where present)
- `path` field pointing to EEG file locations
- records/modality flags indicating availability (e.g., EEG, T1, rest, DWI, MF)

### Python Scripts

1. **BrainLat_CSV_Analysis.py**
   - Comprehensive analysis of demographic and cognitive data
   - Filters PD and CN subjects with detailed statistics
   - Validates data quality and completeness
   - Generates research recommendations

2. **synapse_download_pdcn.py**
   - Downloads PD and CN subjects from Synapse
   - Filters out AD, FTD, MS subjects
   - Organizes data by country folders
   - Uses correct country code extraction

3. **verify_download.py**
   - Verifies downloaded data against CSV
   - Checks file existence on disk with os.path.exists()
   - Provides three-stage verification: CSV → Synapse → Local files
   - Confirms 100% download success (245/245 subjects)

4. **BrainLat_EEG_analysis.py**
   - Loads and validates all 6 EEG CSV files
   - Reports missingness, duplicates, and PD vs CN distributions
   - Produces merged subject-level EEG statistics

5. **verify_download_eeg.py**
   - Verifies EEG downloads against Synapse listings and EEG CSV expectations
   - Confirms each subject exists locally with `.set/.fdt` files
   - Reports folder-wise completeness and totals (75/75 verified)

---

## How to Access Additional Data

### MRI Data

The MRI data in this repository was downloaded from the Synapse platform.

**Synapse Project:** https://www.synapse.org/#!Synapse:syn51549340  
**Project DOI:** https://doi.org/10.7303/syn51549340

**To access additional MRI data:**
1. Fill out the data access form: [BrainLat Data Request Form]
2. Or email directly: Guido Roccati (grocatti@udesa.edu.ar)

### EEG Data

EEG data can be accessed directly through the Synapse platform in the data folder.

### Synapse Repository Structure

```text
BrainLat MRI Dataset (Synapse)
├── Argentina_CNC-UdeSA (syn54002190) → AR subjects
├── Chile_GERO (syn54023101) → CLB subjects
├── Colombia_UV (syn54014630) → COA subjects
├── Colombia_AI-PUJB (syn54015826) → COB subjects
├── Mexico_INCMNM (syn54013943) → MXA subjects
└── Peru_UCIDP-IPN (syn54014195) → PE subjects
```


---

## Data Usage and Citation

### Reference

Please cite the following paper when using this dataset:

> Prado P, Medel V, Gonzalez-Gomez R, Sainz-Ballesteros A, Vidal V, Santamaría-García H, Moguilner S, Mejia J, Slachevsky A, Behrens MI, Aguillon D, Lopera F, Parra MA, Matallana D, Maito MA, Garcia AM, Custodio N, Funes AA, Piña-Escudero S, Birba A, Fittipaldi S, Legaz A, Ibañez A (2023). **The BrainLat project, a multimodal neuroimaging dataset of neurodegeneration from underrepresented backgrounds.** *Scientific Data* (accepted).

### Purpose

This dataset was created to:
- Address the need for affordable, scalable biomarkers in regions with larger inequities
- Promote assessment of regional variability in neurodegeneration
- Include underrepresented populations in neuroimaging research
- Enable development of diagnostic tools for neurodegenerative diseases

---

## Technical Specifications

### Data Format
- **Image Format:** NIfTI (.nii.gz)
- **BIDS Compliance:** Partially BIDS-compliant structure
- **Coordinate System:** MNI space (after preprocessing)

### Total Dataset Size
- **MRI (PD+CN only):** ~19.8 GB  
  - 245 subjects (56 PD + 189 CN)
  - Modalities: T1w, DWI, resting-state fMRI

- **EEG (PD+CN/HC):** ~7.94 GB  
  - 75 subjects downloaded
  - 69 unique PD+CN subjects (23 PD + 46 CN)
  - Format: EEGLAB (`.set` / `.fdt`)

- **Combined MRI + EEG:** ~27.74 GB
- **Number of Files:** ~1,800 (varies by modality and site)


### Quality Control
- All subjects have passed site-level quality control
- Imaging parameters harmonized across sites where possible
- Standardized clinical and cognitive assessments

---

## Research Applications

This dataset is suitable for:

1. **Machine Learning Classification**
   - PD vs CN discrimination
   - Multi-class disease classification
   - Feature extraction and selection

2. **Neuroimaging Analysis**
   - Brain morphometry and volumetrics
   - Cortical thickness analysis
   - White matter tractography
   - Functional connectivity patterns

3. **Biomarker Development**
   - Early detection markers for PD
   - Disease progression tracking
   - Regional brain changes in neurodegeneration

4. **Cross-Cultural Studies**
   - Latin American population norms
   - Regional variability assessment
   - Health disparities research

---

## Contact Information

**Dataset Coordinator:**  
Guido Roccati  
Email: grocatti@udesa.edu.ar

**Institution:**  
Latin American Brain Health Institute (BrainLat)  
Universidad de San Andrés, Buenos Aires, Argentina

**Consortium:**  
Multi-Partner Consortium to Expand Dementia Research in Latin America (ReDLat)

---

## License

**BrainLat Dataset © 2023** by Pavel Prado, Vicente Medel, and Agustín Ibañez is licensed under **CC0 (Creative Commons Zero)**.

This dataset is dedicated to the public domain. You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission.

**Attribution (recommended but not required):**  
While not legally required under CC0, please cite the dataset using the reference provided above to support the researchers and acknowledge their contribution.

---

## Acknowledgments

This dataset was made possible through the collaborative efforts of:
- ReDLat consortium members across 5 Latin American countries
- All participating institutions and clinical sites
- Patients and healthy volunteers who contributed their data
- Funding agencies supporting dementia research in Latin America
- **Dataset creators:** Pavel Prado, Vicente Medel, and Agustín Ibañez

---

## Version Information

**Dataset Version:** 1.0  
**Download Date:** January 2026  
**README Version:** 1.0  
**Last Updated:** January 22, 2026

---

## Quick Reference: Site Codes

| Code | Location | PD | CN | Total |
|------|----------|----|----|-------|
| **AR** | Buenos Aires, Argentina | 13 | 22 | 35 |
| **CLB** | Santiago, Chile (GERO) | 21 | 85 | 106 |
| **COA** | Cali, Colombia (UV) | 22 | 28 | 50 |
| **COB** | Bogotá, Colombia (PUJB) | 0 | 45 | 45 |
| **MXA** | Mexico City, Mexico | 0 | 2 | 2 |
| **PE** | Lima, Peru | 0 | 7 | 7 |

**Grand Total:** 56 PD + 189 CN = **245 subjects**

