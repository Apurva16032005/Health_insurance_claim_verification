import streamlit as st
import requests
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- SYSTEM CONFIGURATION ---
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="InsurVerify | Enterprise Claims Auditing",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- MODERN ENTERPRISE DESIGN SYSTEM ---
st.markdown("""
<style>
    /* Global Typography & Font Smoothing */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #0f172a;
    }
    
    /* Main Background */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Navbar Styling */
    .navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 28px;
        background: #ffffff;
        border-bottom: 1px solid #e2e8f0;
        margin: -4rem -4rem 1.5rem -4rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }
    .brand-container {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-logo {
        width: 32px;
        height: 32px;
        background: #1e293b;
        color: #ffffff;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 15px;
        letter-spacing: -0.5px;
    }
    .brand-title {
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
        letter-spacing: -0.3px;
    }
    .brand-subtitle {
        font-size: 12px;
        color: #64748b;
        margin: 0;
        font-weight: 400;
    }
    .badge-env {
        background: #f1f5f9;
        color: #475569;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 4px;
        border: 1px solid #cbd5e1;
        letter-spacing: 0.3px;
        text-transform: uppercase;
    }
    
    /* Card Component */
    .saas-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03), 0 2px 6px rgba(0,0,0,0.01);
        margin-bottom: 20px;
    }
    .card-title {
        font-size: 16px;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 4px;
    }
    .card-description {
        font-size: 13px;
        color: #64748b;
        margin-bottom: 18px;
    }
    
    /* Metric Card Component */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px 20px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .metric-label {
        font-size: 12px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748b;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.2;
    }
    .metric-sub {
        font-size: 12px;
        color: #94a3b8;
        margin-top: 4px;
    }
    
    /* Status Badges */
    .risk-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.2px;
    }
    .risk-low {
        background: #f0fdf4;
        color: #15803d;
        border: 1px solid #bbf7d0;
    }
    .risk-med {
        background: #fffbeb;
        color: #b45309;
        border: 1px solid #fde68a;
    }
    .risk-high {
        background: #fef2f2;
        color: #b91c1c;
        border: 1px solid #fecaca;
    }
    
    /* Audit Detail Item */
    .audit-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        margin-top: 14px;
    }
    .audit-item {
        background: #f8fafc;
        border: 1px solid #f1f5f9;
        border-radius: 6px;
        padding: 10px 14px;
    }
    .audit-item-label {
        font-size: 11px;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 500;
        margin-bottom: 2px;
    }
    .audit-item-val {
        font-size: 14px;
        font-weight: 600;
        color: #1e293b;
    }
    
    /* Streamlit Button Overrides */
    .stButton>button {
        border-radius: 6px;
        font-weight: 500;
        font-size: 14px;
        padding: 0.5rem 1rem;
        transition: all 0.15s ease-in-out;
    }
    .stButton>button[kind="primary"] {
        background-color: #2563eb;
        border-color: #2563eb;
        color: #ffffff;
    }
    .stButton>button[kind="primary"]:hover {
        background-color: #1d4ed8;
        border-color: #1d4ed8;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        color: #1e293b !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    /* Form inputs */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 6px;
        border: 1px solid #cbd5e1;
        font-size: 14px;
    }
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 1px #2563eb;
    }
</style>
""", unsafe_allow_html=True)

# --- NAVBAR HEADER ---
def render_navbar(user_role=None):
    col1, col2 = st.columns([5, 1.2])
    with col1:
        st.markdown("""
        <div class="navbar">
            <div class="brand-container">
                <div class="brand-logo">IV</div>
                <div>
                    <p class="brand-title">InsurVerify Enterprise</p>
                    <p class="brand-subtitle">Automated Claims Fraud & Discrepancy Auditing</p>
                </div>
            </div>
            <span class="badge-env">Production v2.4</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if user_role:
            st.write("")
            if st.button("Sign Out", key="nav_logout", use_container_width=True):
                st.session_state['role'] = None
                st.rerun()

# --- LOGIN VIEW ---
def render_login():
    render_navbar()
    
    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Authentication Portal</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-description">Select your access domain to access the verification workspace.</div>', unsafe_allow_html=True)
        
        tab_user, tab_officer = st.tabs(["Policyholder Portal", "Claims Auditor Portal"])
        
        with tab_user:
            st.write("")
            email = st.text_input("Account Email", placeholder="policyholder@domain.com", key="login_user_email")
            pwd = st.text_input("Security PIN / Password", type="password", key="login_user_pwd")
            st.write("")
            if st.button("Sign In as Policyholder", type="primary", use_container_width=True, key="btn_login_user"):
                if email and pwd:
                    st.session_state['role'] = 'User'
                    st.session_state['user_email'] = email
                    st.rerun()
                else:
                    st.error("Please provide both email and password credentials.")
                    
        with tab_officer:
            st.write("")
            officer_id = st.text_input("Auditor Badge / ID", placeholder="EMP-8821", key="login_off_id")
            off_email = st.text_input("Corporate Email", placeholder="auditor@insurance.com", key="login_off_email")
            off_pwd = st.text_input("Master Password", type="password", key="login_off_pwd", help="Default auditor access: admin123")
            st.write("")
            if st.button("Sign In as Auditor", type="primary", use_container_width=True, key="btn_login_off"):
                if officer_id and off_email and off_pwd == "admin123":
                    st.session_state['role'] = 'Officer'
                    st.session_state['officer_id'] = officer_id
                    st.rerun()
                elif not (officer_id and off_email and off_pwd):
                    st.warning("All auditor credential fields are mandatory.")
                else:
                    st.error("Invalid auditor credentials. (Authorized default: 'admin123')")
                    
        st.markdown('</div>', unsafe_allow_html=True)

# --- POLICYHOLDER VIEW ---
def render_policyholder():
    render_navbar(user_role="User")
    
    col_crumb, col_act = st.columns([4, 1])
    with col_crumb:
        st.markdown(f"**Workspace:** Claims Submissions &nbsp;|&nbsp; Logged in as: `{st.session_state.get('user_email', 'user')}`")
    
    st.write("")
    
    col_left, col_right = st.columns([1.6, 1])
    
    with col_left:
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">New Reimbursement Claim Submission</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-description">Upload your itemized medical bill, receipt, or discharge summary for automated verification.</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            p_name = st.text_input("Patient Full Name", placeholder="e.g. John Doe")
            h_name = st.text_input("Medical Facility / Hospital", placeholder="e.g. City General Hospital")
        with c2:
            amt = st.number_input("Total Claimed Amount (INR ₹)", min_value=0.0, step=500.0, format="%.2f")
            desc = st.text_input("Treatment / Diagnostic Summary", placeholder="e.g. Emergency Appendectomy")
            
        st.write("")
        uploaded_files = st.file_uploader(
            "Document Attachments (Bill Receipts, Invoices, Summaries)", 
            type=["jpg", "jpeg", "png", "pdf"],
            accept_multiple_files=True
        )
        
        st.write("")
        submit_btn = st.button("Submit Claim for Automated Audit", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if submit_btn:
            if not uploaded_files or amt <= 0:
                st.warning("Please upload at least one receipt document and specify a valid claim amount.")
            else:
                progress_container = st.container()
                with progress_container:
                    for f in uploaded_files:
                        with st.spinner(f"Auditing {f.name} with Multimodal Verification Engine..."):
                            try:
                                f.seek(0)
                                files_payload = {"file": (f.name, f.getvalue(), f.type)}
                                data_payload = {
                                    "amount": amt,
                                    "user_id": 101,
                                    "description": desc or "Medical Reimbursement",
                                    "hospital_name": h_name or "General Hospital",
                                    "patient_name": p_name or "Policyholder"
                                }
                                
                                res = requests.post(f"{API_URL}/upload-claim", files=files_payload, data=data_payload)
                                if res.status_code == 200:
                                    res_data = res.json()
                                    score = res_data.get("fraud_score", 0.0)
                                    risk_tier = res_data.get("risk_label", "Low")
                                    
                                    badge_class = "risk-high" if score > 0.7 else "risk-med" if score > 0.3 else "risk-low"
                                    
                                    st.markdown(f"""
                                    <div class="metric-card" style="margin-bottom: 12px; border-left: 4px solid {'#dc2626' if score>0.7 else '#d97706' if score>0.3 else '#16a34a'};">
                                        <div style="display:flex; justify-content:space-between; align-items:center;">
                                            <div>
                                                <strong>File:</strong> {f.name} &nbsp;•&nbsp; <strong>Claim Reference:</strong> #{res_data.get('claim_id')}
                                                <div style="font-size: 13px; color: #64748b; margin-top: 3px;">
                                                    Verification completed. Status: {res_data.get('message', 'Processed')}
                                                </div>
                                            </div>
                                            <span class="risk-badge {badge_class}">
                                                {risk_tier.upper()} RISK ({score*100:.1f}%)
                                            </span>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.error(f"Server error ({res.status_code}) processing {f.name}. Please ensure the backend is active.")
                            except Exception as err:
                                st.error(f"Connection failure for {f.name}: {err}")
                                
    with col_right:
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Automated Verification Protocol</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-description">Every submitted bill undergoes automated multi-stage evaluation:</div>', unsafe_allow_html=True)
        
        st.markdown("""
        1. **Forensic Splicing Check (CNN & ELA):**  
           Scans for copy-move edits, pixel resampling, and image manipulation.
           
        2. **Optical Character Recognition (EasyOCR):**  
           Extracts itemized invoice rows, line-item totals, dates, and facility names.
           
        3. **Clinical Context Matching (DistilBERT):**  
           Verifies medical taxonomy and procedure terminology consistency.
           
        4. **Financial Ratio Discrepancy (Benford's Check):**  
           Compares stated reimbursement total against extracted line items.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# --- CLAIMS OFFICER VIEW ---
def render_officer():
    render_navbar(user_role="Officer")
    
    st.markdown(f"**Workspace:** Auditor Console &nbsp;|&nbsp; Inspector: `{st.session_state.get('officer_id', 'EMP-8821')}`")
    st.write("")
    
    # 1. LIVE DATA FETCH
    claims_data = []
    try:
        resp = requests.get(f"{API_URL}/get-pending-claims", timeout=6)
        if resp.status_code == 200:
            claims_data = resp.json()
    except Exception as e:
        st.error(f"Cannot reach backend API at {API_URL}. Ensure FastAPI is running.")
        
    # 2. EXECUTIVE METRICS
    total_claims = len(claims_data)
    total_val = sum(c['input_data']['amount_claimed'] for c in claims_data) if claims_data else 0.0
    critical_count = sum(1 for c in claims_data if c['scores']['final_fraud_score'] > 0.7) if claims_data else 0
    avg_score = (sum(c['scores']['final_fraud_score'] for c in claims_data) / total_claims * 100) if total_claims > 0 else 0.0
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Active Claims in Queue</div>
            <div class="metric-value">{total_claims}</div>
            <div class="metric-sub">Total verified records</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Portfolio Exposure</div>
            <div class="metric-value">₹{total_val:,.2f}</div>
            <div class="metric-sub">Cumulative claimed volume</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Mean Fraud Risk Index</div>
            <div class="metric-value">{avg_score:.1f}%</div>
            <div class="metric-sub">Multimodal model baseline</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Critical Anomaly Flags</div>
            <div class="metric-value" style="color: {'#dc2626' if critical_count>0 else '#15803d'};">{critical_count}</div>
            <div class="metric-sub">Requires manual adjudication</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    
    # 3. TABS: QUEUE VS ANALYTICS
    tab_queue, tab_charts = st.tabs(["Inspection Queue", "Portfolio Risk Analytics"])
    
    with tab_queue:
        if not claims_data:
            st.info("No claims currently awaiting audit in the queue.")
        else:
            for item in claims_data:
                cid = item['claim_id']
                score = item['scores']['final_fraud_score']
                tamper_score = item['scores']['cnn_score']
                hosp = item['input_data']['hospital_name']
                amt_claimed = item['input_data']['amount_claimed']
                created = item['created_at']
                
                tier = "High" if score > 0.7 else "Medium" if score > 0.3 else "Low"
                badge_class = "risk-high" if score > 0.7 else "risk-med" if score > 0.3 else "risk-low"
                
                exp_header = f"Claim #{cid} • {hosp} • ₹{amt_claimed:,.2f} • {tier.upper()} RISK ({score*100:.1f}%)"
                
                with st.expander(exp_header, expanded=(score > 0.7)):
                    c_left, c_right = st.columns([1, 1.4])
                    
                    with c_left:
                        st.markdown("**Submitted Document & Forgery Analysis**")
                        heatmap_url = item.get('details', {}).get('cnn_heatmap')
                        if heatmap_url and "temp_heatmap" not in heatmap_url:
                            st.image(f"{API_URL}{heatmap_url}", caption="Visual Anomaly Map (ELA / Resampling)", use_container_width=True)
                        else:
                            st.image(f"{API_URL}{item['input_data']['file_url']}", caption="Source Document Scan", use_container_width=True)
                            
                    with c_right:
                        st.markdown(f"""
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 12px;">
                            <h4 style="margin:0; font-size: 16px; font-weight:600;">Automated Audit Breakdown</h4>
                            <span class="risk-badge {badge_class}">{tier.upper()} RISK</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        ext_amt = item.get('details', {}).get('extracted_amount')
                        bill_date = item.get('details', {}).get('bill_date') or "Not Detected"
                        gst_no = item.get('details', {}).get('gst_number') or "Unspecified"
                        
                        st.markdown(f"""
                        <div class="audit-grid">
                            <div class="audit-item">
                                <div class="audit-item-label">Claimed Amount</div>
                                <div class="audit-item-val">₹{amt_claimed:,.2f}</div>
                            </div>
                            <div class="audit-item">
                                <div class="audit-item-label">OCR Extracted Total</div>
                                <div class="audit-item-val">₹{float(ext_amt):,.2f}</div>
                            </div>
                            <div class="audit-item">
                                <div class="audit-item-label">Document Date</div>
                                <div class="audit-item-val">{bill_date}</div>
                            </div>
                            <div class="audit-item">
                                <div class="audit-item-label">Facility GSTIN</div>
                                <div class="audit-item-val">{gst_no}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.write("")
                        st.markdown(f"**Visual Splicing Score:** `{tamper_score:.2f}` &nbsp;|&nbsp; **Composite Fraud Score:** `{score:.2f}`")
                        
                        explanation = item.get('xai_explanation', 'No detailed anomalies flagged.')
                        st.markdown(f"""
                        <div style="background:#f1f5f9; border-radius:6px; padding:10px 14px; font-size:13px; color:#334155; margin-top:8px;">
                            <strong>AI Audit Finding:</strong> {explanation}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.write("")
                        pdf_report_url = f"{API_URL}/reports/Fraud_Report_{cid}.pdf"
                        st.link_button("Download Audit Verification Report (PDF)", pdf_report_url, use_container_width=True)
                        
                        st.write("")
                        btn_c1, btn_c2 = st.columns(2)
                        with btn_c1:
                            if st.button("Approve Claim", key=f"app_{cid}", type="primary", use_container_width=True):
                                requests.post(f"{API_URL}/update-decision", json={"claim_id": cid, "status": "Approved", "remarks": "Approved by Officer"})
                                st.success("Claim approved and archived.")
                                time.sleep(0.6)
                                st.rerun()
                        with btn_c2:
                            if st.button("Flag / Reject", key=f"rej_{cid}", use_container_width=True):
                                requests.post(f"{API_URL}/update-decision", json={"claim_id": cid, "status": "Rejected", "remarks": "Rejected: Discrepancy Found"})
                                st.error("Claim flagged for rejection.")
                                time.sleep(0.6)
                                st.rerun()

    with tab_charts:
        if not claims_data:
            st.info("No claims available for aggregate portfolio analytics.")
        else:
            df = pd.DataFrame(claims_data)
            df['Amount'] = df['input_data'].apply(lambda x: x['amount_claimed'])
            df['Hospital'] = df['input_data'].apply(lambda x: x['hospital_name'])
            df['Risk Score'] = df['scores'].apply(lambda x: x['final_fraud_score'])
            df['Risk Level'] = df['details'].apply(lambda x: x.get('risk_label', 'Unknown'))
            
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                st.markdown('<div class="saas-card">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">Portfolio Exposure by Risk Tier</div>', unsafe_allow_html=True)
                fig_pie = px.pie(
                    df, names='Risk Level', values='Amount', hole=0.5,
                    color='Risk Level',
                    color_discrete_map={'High': '#dc2626', 'Medium': '#d97706', 'Low': '#16a34a'}
                )
                fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10), showlegend=True)
                st.plotly_chart(fig_pie, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with c_p2:
                st.markdown('<div class="saas-card">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">Mean Risk Index by Healthcare Facility</div>', unsafe_allow_html=True)
                hosp_df = df.groupby('Hospital')['Risk Score'].mean().reset_index()
                fig_bar = px.bar(
                    hosp_df, x='Risk Score', y='Hospital', orientation='h',
                    range_x=[0, 1],
                    color='Risk Score',
                    color_continuous_scale=['#16a34a', '#eab308', '#dc2626']
                )
                fig_bar.update_layout(margin=dict(t=10, b=10, l=10, r=10), coloraxis_showscale=False)
                st.plotly_chart(fig_bar, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

# --- APPLICATION ROUTING ---
if 'role' not in st.session_state:
    st.session_state['role'] = None

if st.session_state['role'] == 'User':
    render_policyholder()
elif st.session_state['role'] == 'Officer':
    render_officer()
else:
    render_login()
