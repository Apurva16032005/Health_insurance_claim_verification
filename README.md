# Health Insurance Claim Verification System

An intelligent multimodal AI system designed to detect fraudulent, tampered, or inconsistent health insurance claims. The application analyzes submitted medical bills and receipts to evaluate authenticity using visual forensics, OCR text extraction, clinical NLP, and a calibrated Random Forest risk-scoring classifier.

---

## Key Highlights

- **Multimodal Verification Pipeline:** Built an AI-powered insurance claim verification pipeline using Python, EasyOCR, NLP, and DistilBERT to extract and analyze unstructured medical bills and identify anomalous claims and inconsistent line items.
- **Calibrated Risk Classifier (88% F1-Score):** Trained a Random Forest classifier on a synthetic multimodal dataset of 10,000 medical claim records to categorize claims into Low, Medium, and High risk based on visual & financial anomalies, achieving an 88% F1 score on the test set.
- **End-to-End Application:** Developed a FastAPI backend with MySQL and an interactive Streamlit UI to integrate claim processing, risk scoring, and automated diagnostic reports into an end-to-end application.

---

## System Architecture & Pipeline

1. **Document Ingestion & Forensics:**
   - **Visual Forgery Detection (CNN):** Evaluates image tampering, copy-move edits, and splicing.
   - **Error Level Analysis (ELA) & Metadata:** Analyzes compression discrepancies and inspects EXIF metadata for digital manipulation.
   - **Perceptual Hash Deduplication (pHash):** Flags identical or previously submitted receipts to prevent duplicate claims.

2. **OCR & Text Extraction:**
   - **EasyOCR Pipeline:** Preprocesses scanned documents to extract line items, hospital names, dates, and total amounts.
   - **Financial Anomaly & Benford's Law Check:** Validates numerical distributions and compares user-claimed amounts against OCR-extracted bill totals.

3. **Clinical Context (NLP):**
   - **DistilBERT Embeddings:** Generates contextual embeddings from bill text.
   - **Medical Entity Extraction:** Identifies diagnoses, treatments, and clinical terminology to verify document authenticity.

4. **Risk Classification & Fusion:**
   - **Random Forest Classifier:** Combines visual tampering scores, metadata flags, financial deviation ratios, and keyword densities.
   - **Multi-Tier Risk Assessment:** Triages claims into **Low Risk**, **Medium Risk**, and **High Risk**.
   - **Automated Diagnostic Reports:** Generates downloadable summary reports with anomaly breakdowns.

---

## Project Structure

```
├── backend/
│   ├── app.py                # FastAPI application endpoints
│   ├── train_model.py        # Model training & synthetic data generation (88% F1)
│   ├── requirements.txt      # Backend Python dependencies
│   ├── models/
│   │   ├── cnn_model.py      # Forgery detection (EfficientNet)
│   │   ├── ml_model.py       # Random Forest inference loader
│   │   ├── multimodal.py     # Multimodal risk fusion
│   │   ├── nlp_model.py      # DistilBERT clinical NLP
│   │   └── ocr.py            # EasyOCR extraction
│   └── utils/
│       ├── combine_features.py  # Feature vector aggregator
│       ├── dedup.py             # Image hashing & deduplication
│       ├── extract_fields.py    # Key entity parser
│       ├── forensics.py         # ELA & metadata forensics
│       ├── preprocess.py        # Image pre-processing for OCR
│       ├── report_gen.py        # Diagnostic PDF report generator
│       └── validation_rules.py  # Benford's Law & rule validations
├── frontend/
│   ├── streamlit_app.py      # Streamlit web dashboard
│   └── dashboard_mockup.png  # UI preview
├── data/
│   └── bills/                # Sample test bills
└── README.md
```

---

## Setup & Installation

### 1. Prerequisites
- Python 3.10+
- MySQL Server

### 2. Virtual Environment Setup
```bash
# Clone the repository
git clone https://github.com/Apurva16032005/Health_insurance_claim_verification.git
cd Health_insurance_claim_verification

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
pip install streamlit
```

### 4. Train the Classifier (Optional)
To train the Random Forest model and regenerate `backend/models/ml_model.pkl`:
```bash
python backend/train_model.py
```

### 5. Running the Application

**Start the FastAPI Backend:**
```bash
cd backend
uvicorn app:app --reload
```
Backend API will be available at `http://localhost:8000`.

**Start the Streamlit Dashboard:**
```bash
cd frontend
streamlit run streamlit_app.py
```
Dashboard will open in your browser at `http://localhost:8501`.
