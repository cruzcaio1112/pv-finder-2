import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="PV Finder", layout="wide", page_icon="📦")

# --- CORES ---
PEPSICO_BLUE = "#004C97"
PEPSICO_LIGHT_BLUE = "#00A3E0"
BACKGROUND_COLOR = "#F8FAFC"

# --- CSS ---
st.markdown(f"""
    <style>
        body {{ background-color: {BACKGROUND_COLOR}; }}
        .main-title {{ font-size: 40px; font-weight: bold; color: {PEPSICO_BLUE}; }}
        .subtitle {{ font-size: 18px; color: #555; }}
        .upload-box {{ background-color: #E8F1FA; padding: 15px; border-radius: 8px; margin-top: 10px; }}
        .stButton>button {{ background-color: {PEPSICO_LIGHT_BLUE}; color: white; font-weight: bold; border-radius: 8px; }}
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO ---
st.markdown('<div class="main-title">PV Finder <span style="font-size:18px; color:#004C97;">Packaging Specs</span></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Type any fragment of PV number, description or notes. Update the base weekly via upload (Admin).</div>', unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR ADMIN ---
st.sidebar.header("Admin – Weekly Upload")
pin_input = st.sidebar.text_input("Enter PIN", type="password")
uploaded_file = None
df = None

if pin_input == "130125":
    uploaded_file = st.sidebar.file_uploader("Upload official PV Spec Excel file", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        st.sidebar.success("✅ Base loaded successfully!")
        last_update = datetime.now().strftime("%d-%m-%Y %H:%M")
else:
    last_update = "No data loaded yet"

# --- INFO ---
st.write(f"**Last updated:** {last_update}")
st.markdown('<div class="upload-box">Upload the official Excel file to start. Only Admin can upload using PIN.</div>', unsafe_allow_html=True)

# --- Se não houver dados, mostra aviso ---
if df is None:
    st.warning("⚠ No data loaded. Please upload the official file using PIN.")
    st.stop()

# --- BOTÕES ---
col1, col2, col3 = st.columns([1,1,1])
with col1: st.button("Reset")
with col2: st.button("Save Defaults")
with col3: st.button("Load Defaults")

# --- GLOBAL SEARCH ---
global_search = st.text_input("🔍 Global search (fragment across ALL columns)", placeholder="e.g., Doritos, C2, X-Dock, P000...")
filtered_df = df.copy()
if global_search:
    filtered_df = filtered_df[filtered_df.apply(lambda row: row.astype(str).str.contains(global_search, case=False).any(), axis=1)]

# --- FILTROS BÁSICOS COM TEXTO ---
st.subheader("Basic column filters")
col_filters = st.columns(6)
with col_filters[0]:
    pv_text = st.text_input("PVNumber contains")
    pv_select = st.multiselect("PVNumber options", options=sorted(df["PVNumber"].dropna().unique()))
with col_filters[1]:
    status_text = st.text_input("PVStatus contains")
    status_select = st.multiselect("PVStatus options", options=sorted(df["PVStatus"].dropna().unique()))
with col_filters[2]:
    doc_text = st.text_input("DocumentType contains")
    doc_select = st.multiselect("DocumentType options", options=sorted(df["DocumentType"].dropna().unique()))
with col_filters[3]:
    sales_text = st.text_input("SalesClass contains")
    sales_select = st.multiselect("SalesClass options", options=sorted(df["SalesClass"].dropna().unique()))
with col_filters[4]:
    shape_text = st.text_input("Shape contains")
    shape_select = st.multiselect("Shape options", options=sorted(df["Shape"].dropna().unique()))
with col_filters[5]:
    size_text = st.text_input("Size contains")
    size_select = st.multiselect("Size options", options=sorted(df["Size"].dropna().unique()))

# --- APLICA FILTROS ---
if pv_text:
    filtered_df = filtered_df[filtered_df["PVNumber"].str.contains(pv_text, case=False, na=False)]
if pv_select:
    filtered_df = filtered_df[filtered_df["PVNumber"].isin(pv_select)]
if status_text:
    filtered_df = filtered_df[filtered_df["PVStatus"].str.contains(status_text, case=False, na=False)]
if status_select:
    filtered_df = filtered_df[filtered_df["PVStatus"].isin(status_select)]
if doc_text:
    filtered_df = filtered_df[filtered_df["DocumentType"].str.contains(doc_text, case=False, na=False)]
if doc_select:
    filtered_df = filtered_df[filtered_df["DocumentType"].isin(doc_select)]
if sales_text:
    filtered_df = filtered_df[filtered_df["SalesClass"].str.contains(sales_text, case=False, na=False)]
if sales_select:
    filtered_df = filtered_df[filtered_df["SalesClass"].isin(sales_select)]
if shape_text:
    filtered_df = filtered_df[filtered_df["Shape"].str.contains(shape_text, case=False, na=False)]
if shape_select:
    filtered_df = filtered_df[filtered_df["Shape"].isin(shape_select)]
if size_text:
    filtered_df = filtered_df[filtered_df["Size"].str.contains(size_text, case=False, na=False)]
if size_select:
    filtered_df = filtered_df[filtered_df["Size"].isin(size_select)]

# --- FILTROS AVANÇADOS ---
with st.expander("Advanced filters"):
    min_code = st.number_input("Code Date min", min_value=0, value=0)
    max_code = st.number_input("Code Date max", min_value=0, value=240)
    only_latest = st.checkbox("Show only latest per PVNumber")

    if min_code or max_code:
        if "CodeDate" in filtered_df.columns:
            filtered_df = filtered_df[(filtered_df["CodeDate"] >= min_code) & (filtered_df["CodeDate"] <= max_code)]

    if only_latest:
        filtered_df = filtered_df.sort_values("CodeDate").drop_duplicates(subset=["PVNumber"], keep="last")

# --- RESULTADOS ---
st.subheader("📋 Filtered Results")
st.dataframe(filtered_df)

# --- DOWNLOAD ---
st.download_button("Download Filtered Results", data=filtered_df.to_csv(index=False), file_name="filtered_pv_specs.csv", mime="text/csv")
