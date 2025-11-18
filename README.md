# PV Finder - Packaging Specs Search App

This app allows your team to search and filter PV specifications using a secure interface.

## How to Run Locally:
-------------------
1. Make sure you have Python installed.
2. Install required packages:
   pip install streamlit pandas openpyxl
3. Save your official PV Spec Excel file locally.
4. Run the app:
   streamlit run pv_finder.py
5. Enter the PIN (130125) in the sidebar to upload the Excel file.

## How to Publish on Streamlit Cloud:
----------------------------------
1. Create a GitHub repository and upload pv_finder.py.
2. Go to https://streamlit.io/cloud and sign in.
3. Click "New App" and connect your GitHub repo.
4. Select pv_finder.py and click "Deploy".
5. Configure access as Private and share the link with your team.
6. Only users with the PIN can upload the official database weekly.

## Security:
---------
- Only users with PIN 130125 can upload the official Excel file.
- Without upload, the app shows a warning and disables filters.

**Author: Amanda & Copilot**
