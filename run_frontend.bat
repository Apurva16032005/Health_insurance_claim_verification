@echo off
echo Starting Streamlit Dashboard on http://localhost:8501 ...
cd /d "%~dp0frontend"
call ..\backend\venv\Scripts\activate.bat
streamlit run streamlit_app.py
