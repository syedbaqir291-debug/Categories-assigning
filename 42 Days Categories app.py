import streamlit as st
import pandas as pd
import re
from io import BytesIO

st.title("Cancer Disease Categorization App - OMAC Developer")
st.write("Upload an Excel file → Select Sheet → Select Disease Column → Get Categorized Output")

# -----------------------------
# Function to categorize disease
# -----------------------------
def categorize_disease(disease):
    if not isinstance(disease, str):
        return "Not categorized"
    
    d = disease.lower().strip()

    # --- Gastrointestinal malignancies ---
    if (re.search(r"gall bladder|gallbladder|gall-bladder|bile duct|bile|gi cancer|gi cancers|gi|gastrointestinal|"
                  r"stomach|gastric|oesoph|esoph|intestin|pancreas|liver", d)):
        return "Gastrointestinal malignancies"

    # --- Haematological malignancies ---
    if (re.search(r"acute leukaemia|acute leukemia|acute myeloid leukemia|acute myeloid leukaemia|aml|hodgkin|"
                  r"non-hodgkin|neuroblastoma|chronic leukaemia", d)):
        return "Haematological malignancies"

    # --- Gynecological Tumors ---
    if (re.search(r"ovarian|germ cell|endometrial|cervical", d)):
        return "Gynecological Tumors"

    # --- Urological Tumors ---
    if (re.search(r"renal|kidney| bladder|bladder cancer|prostate", d)):
        return "Urological Tumors"

    # --- Neurological malignancies ---
    if (re.search(r"brain|cranial|spinal", d)):
        return "Neurological malignancies"

    # --- Breast cancer ---
    if "breast" in d:
        return "Breast cancer"

    # --- Pulmonary malignancies ---
    if "lung" in d:
        return "Pulmonary malignancies"

    # --- Head & Neck cancers ---
    if (re.search(r"oral|orophary|nasophary|head & neck|head and neck", d)):
        return "Head and neck cancers"

    # --- Thyroid cancers ---
    if "thyroid" in d:
        return "Thyroid cancers"

    # --- Sarcoma ---
    if (re.search(r"sarcoma|ewing", d)):
        return "Sarcoma"

    # --- Retinoblastoma ---
    if "retinoblastoma" in d:
        return "Retinoblastoma"

    # --- Non-specific / Wilms ---
    if (re.search(r"wilms|wilms tumour|wilm’s|skin cancer|unknown primary|unknown|rare", d)):
        return "Non-specific"

    return "Not categorized"


# -----------------------------
# Step 1: Upload Excel
# -----------------------------
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    sheet_name = st.selectbox("Select Sheet", xls.sheet_names)

    df = pd.read_excel(uploaded_file, sheet_name=sheet_name)

    st.write("Preview of Data:", df.head())

    # ---------------------------
    # Step 2: Select Disease Column
    # ---------------------------
    disease_col = st.selectbox("Select Column Containing Disease", df.columns)

    if st.button("Assign Categories"):
        # Insert category column next to disease column
        col_index = df.columns.get_loc(disease_col)
        df.insert(col_index + 1, "Cancer Category", df[disease_col].apply(categorize_disease))

        st.success("Categories Assigned Successfully!")
        st.write(df.head())

        # ---------------------------
        # Step 3: Download Updated Excel
        # ---------------------------
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)

        st.download_button(
            label="Download Updated Excel",
            data=output.getvalue(),
            file_name="Updated_Categorized_File.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
