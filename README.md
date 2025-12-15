# QRT Challenge:  Overall Survival Prediction for patients diagnosed with Myeloid Leukemia 

This repository contains a machine learning pipeline designed to predict the overall survival (OS) of patients with Acute Myeloid Leukemia (AML). The project integrates clinical, molecular, and complex cytogenetic data to build robust survival models, developed as part of a QRT Data Challenge.

## 📖 Project Overview

The goal of this project is to predict the risk scores and survival time for patients using a dataset comprising:

  * **Clinical Data:** Blood counts (WBC, HB, PLT, etc.)
  * **Molecular Data:** Gene mutations (e.g., *NPM1*, *FLT3*, *TP53*), Variant Allele Frequencies (VAF), and protein changes.
  * **Cytogenetics:** International System for Human Cytogenomic Nomenclature (ISCN) strings detailing chromosomal abnormalities.

The pipeline focuses heavily on **feature engineering**—specifically parsing unstructured text data from cytogenetics and molecular reports—to feed into survival analysis models.

## 🚀 Key Features & Methodology

### 1\. Advanced Data Parsing (`parsing.py`)

A custom parser was built to extract structured features from unstructured medical text:

  * **Cytogenetics:** Regex-based parsing of ISCN strings to identify:
      * **Complex Karyotypes:** Automatically flags high-risk patients with $\ge 3$ chromosomal abnormalities.
      * **Structural Variants:** Extracts specific translocations `t(v;v)` and inversions `inv(v)`.
      * **Numerical Changes:** Identifies gains (`+8`) or losses (`-7`) of chromosomes.
  * **Molecular Hotspots:** Extracts numeric amino acid positions from protein change strings (e.g., `p.R882H` $\to$ `882`).

### 2\. Feature Engineering

  * **VAF Weighting:** Gene mutations are weighted by their maximum Variant Allele Frequency (VAF) per patient to capture clonal dominance.
  * **Biological Interactions:** explicit interaction terms for clinically significant pairs, such as:
      * *NPM1* mutated + *FLT3* Wildtype (Good Prognosis)
      * *TP53* mutated + Complex Karyotype (Poor Prognosis)
  * **Clinical Transformations:** Log-transformation of skewed variables (WBC, Blast counts) and iterative imputation (MICE/KNN) for missing values.

### 3\. Models Implemented

The project compares several survival analysis techniques using `scikit-survival`:

  * **Cox Penalized Regression (CoxNet):** A linear baseline using Elastic Net regularization (L1/L2 penalty) to handle high-dimensional sparse data.
  * **Random Survival Forests (RSF):** A non-linear ensemble method effectively capturing complex interactions between genetic mutations.
  * **Gradient Boosting Survival Analysis (GBSA):** A boosting approach optimizing Cox Partial Likelihood.
  * **Ensemble:** A weighted average of RSF and GBSA predictions to maximize the Concordance Index (C-Index).

## 📂 Repository Structure

```text
.
├── data/                       # Dataset folder
│   ├── X_train/                # Training clinical & molecular files
│   ├── X_test/                 # Test clinical & molecular files
│   └── target_train.csv        # Survival labels (OS_YEARS, OS_STATUS)
├── submission/                 # Output folder for prediction CSVs
├── parsing.py                  # Core logic for ISCN and molecular string parsing
├── cox_penalized.ipynb         # Workflow for CoxNet model training & validation
└── random_survival_forest.ipynb # Workflow for RSF, GBSA, and Ensemble generation
```

## 🛠️ Setup & Usage

### Prerequisites

The project requires Python 3.10+ and the following libraries:

```bash
pip install numpy pandas matplotlib scikit-learn scikit-survival
```

### Running the Pipeline

1.  **Data Placement:** Ensure the raw CSV files are placed in the `data/` directory structure as shown above.
2.  **Baseline Model:** Run `cox_penalized.ipynb` to train the linear model and generate baseline submissions.
3.  **Advanced Models:** Run `random_survival_forest.ipynb` to:
      * Perform advanced imputation.
      * Train Random Survival Forest and Gradient Boosting models.
      * Generate the final ensemble submission file (`submission_ensemble_full_data.csv`).

## 📊 Results

The models are evaluated using the **Concordance Index (C-Index)** via Interval-Censored Probability Weighted (IPCW) scoring.

  * **Cox Penalized:** \~73.4%. (Validation)
  * **Random Survival Forest:** \~76.1%+ (Validation)
  * **Gradient Boosting Survival** \~74.4%+ (Validation)
  * **Ensemble Strategy:** Combines the strengths of RSF and GBSA for optimal generalization on the test set.

## 📜 License

This project is under [MIT](MIT.txt) license
