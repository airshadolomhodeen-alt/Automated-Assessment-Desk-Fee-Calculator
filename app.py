import streamlit as st
import pandas as pd
from utils.building_fees import compute_building_fee, get_fixed_cost_per_sqm
from utils.electrical_fees import compute_electrical_fees
from utils.mechanical_fees import compute_mechanical_fees
from utils.plumbing_fees import compute_plumbing_fees
from utils.electronics_fees import compute_electronics_fees
from utils.accessories_fees import compute_accessories_fees
from utils.other_fees import compute_other_fees
from utils.certificates_fees import compute_occupancy_certificate_fee, compute_annual_inspection_fees

# Set page config
st.set_page_config(
    page_title="Building Permit Fees Assessment Utility | BEZA / LGU",
    page_icon="🏛️",
    layout="wide"
)

# Custom CSS for Government Desktop Theme & Order of Payment Modal
st.markdown("""
<style>
    .stApp {
        background-color: #eef2f5;
    }

    .gov-navbar {
        background-color: #0b1a30;
        padding: 12px 20px;
        border-radius: 8px;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    
    .bpfau-banner {
        background: linear-gradient(135deg, #1b365d 0%, #2a4b7c 100%);
        border: 2px solid #002b49;
        border-radius: 6px;
        padding: 16px;
        color: white;
        text-align: center;
        box-shadow: 0px 3px 6px rgba(0,0,0,0.15);
        margin-bottom: 15px;
    }
    .bpfau-banner h4 {
        margin: 0;
        font-size: 13px;
        letter-spacing: 1.5px;
        color: #d1e8ff;
        text-transform: uppercase;
    }
    .bpfau-banner h2 {
        margin: 4px 0;
        font-size: 20px;
        font-weight: 800;
        color: #ffffff;
    }
    .bpfau-banner p {
        margin: 0;
        font-size: 12px;
        font-style: italic;
        color: #ffd700;
    }

    .section-title-bar {
        background-color: #0056b3;
        color: white;
        padding: 8px 15px;
        font-weight: bold;
        font-size: 14px;
        border-radius: 4px;
        margin-bottom: 15px;
        text-align: center;
        letter-spacing: 0.5px;
    }

    .op-receipt {
        background-color: #ffffff;
        border: 1px solid #111;
        padding: 20px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 13px;
        color: #000;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    }
    .op-header {
        text-align: center;
        font-weight: bold;
        text-transform: uppercase;
        border-bottom: 1px dashed #000;
        padding-bottom: 10px;
        margin-bottom: 10px;
    }
    .op-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 4px;
    }
    .op-total {
        border-top: 1px dashed #000;
        border-bottom: 2px double #000;
        padding: 6px 0;
        font-weight: bold;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Top Bar
st.markdown("""
<div class="gov-navbar">
    <div style="font-size: 18px; font-weight: bold;">
        🏛️ OBO Building Permit System &nbsp;|&nbsp; <span style="font-size: 14px; color: #a2c4c9;">Assessment Desk</span>
    </div>
    <div style="font-size: 13px; font-weight: 500; background: #162c4d; padding: 6px 12px; border-radius: 20px;">
        NBCDO MC No. 03 (Series of 2016) / PD 1096
    </div>
</div>
""", unsafe_allow_html=True)

# LGU & BEZA Header
st.markdown("""
<div class="bpfau-banner">
    <h4>Republic of the Philippines</h4>
    <h2>OFFICE OF THE BUILDING OFFICIAL / BEZA DESK</h2>
    <p>"Automated Assessment Desk & Official Order of Payment Generator"</p>
</div>
""", unsafe_allow_html=True)

# Mode Selector in Sidebar
authority_mode = st.sidebar.selectbox(
    "Jurisdiction / Authority Mode",
    ["Standard LGU (80% Local / 20% National)", "BEZA Economic Zone (Direct Ecozone Assessment)"]
)

st.markdown("""
<div class="section-title-bar">
    BUILDING PERMIT FEES and OTHER CHARGES - ASSESSMENT UTILITY
</div>
""", unsafe_allow_html=True)

# Navigation Tabs
tabs = st.tabs([
    "🏢 Building & Occupancy", 
    "⚡ Electrical Fees", 
    "🚰 Plumbing Fees", 
    "🔍 Inspection & Certs",
    "📄 Official Order of Payment (OP)"
])

# Session state initialization
if "fees" not in st.session_state:
    st.session_state.fees = {
        "Electrical Installation Fee": 230.00,
        "Plumbing Installation Fee": 94.00,
        "Building Occupancy Fee": 100.00,
        "Building Inspection Fee": 983.00,
        "Certification Fee": 250.00
    }

# --- TAB 1: BUILDING & OCCUPANCY ---
with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        floor_area = st.number_input("Total Floor Area (SqM)", min_value=1.0, value=500.0)
        cost_val = st.number_input("Building Valuation / Cost (₱)", min_value=0.0, value=0.0)
    with col2:
        occ_fee = st.number_input("Certificate of Occupancy Fee (₱)", min_value=0.0, value=100.0)
        st.session_state.fees["Building Occupancy Fee"] = occ_fee

# --- TAB 2: ELECTRICAL ---
with tabs[1]:
    col1, col2 = st.columns(2)
    with col1:
        elec_inst = st.number_input("Electrical Installation Fee (₱)", min_value=0.0, value=230.0)
        st.session_state.fees["Electrical Installation Fee"] = elec_inst

# --- TAB 3: PLUMBING ---
with tabs[2]:
    col1, col2 = st.columns(2)
    with col1:
        plumb_units = st.number_input("Plumbing Units Count", min_value=1, value=2)
        plumb_inst = st.number_input("Plumbing Installation Fee (₱)", min_value=0.0, value=94.0)
        st.session_state.fees["Plumbing Installation Fee"] = plumb_inst

# --- TAB 4: INSPECTIONS & CERTS ---
with tabs[3]:
    col1, col2 = st.columns(2)
    with col1:
        bldg_insp = st.number_input("Building Annual Inspection Fee (₱)", min_value=0.0, value=983.0)
        cert_fee = st.number_input("Certification Fee (5 x ₱50) (₱)", min_value=0.0, value=250.0)
        st.session_state.fees["Building Inspection Fee"] = bldg_insp
        st.session_state.fees["Certification Fee"] = cert_fee

# --- TAB 5: OFFICIAL ORDER OF PAYMENT ---
with tabs[4]:
    col_left, col_right = st.columns([1.1, 1])
    
    total_assessment = sum(st.session_state.fees.values())
    
    with col_left:
        st.subheader("Assessed Fee Items")
        for item, amount in st.session_state.fees.items():
            st.write(f"• **{item}**: ₱{amount:,.2f}")
        st.markdown(f"### **Total Permit Fee: ₱{total_assessment:,.2f}**")
        
    with col_right:
        if "BEZA" in authority_mode:
            local_share = total_assessment * 1.00
            nat_share = 0.00
            header_title = "BANGSAMORO ECONOMIC ZONE AUTHORITY"
            treasurer_note = "Please pay at the BEZA Finance / Cashier Office."
        else:
            local_share = total_assessment * 0.80
            nat_share = total_assessment * 0.20
            header_title = "OFFICE OF THE BUILDING OFFICIAL"
            treasurer_note = "Please pay at the Municipal Treasurer's Office."

        st.markdown(f"""
        <div class="op-receipt">
            <div class="op-header">
                {header_title}<br>
                ORDER OF PAYMENT
            </div>
            <div class="op-row"><span>Ctrl No:</span> <span>2610201826</span></div>
            <div class="op-row"><span>Date:</span> <span>10/20/2026</span></div>
            <div class="op-row"><span>Units:</span> <span>1</span></div>
            <hr style="border-top: 1px dashed #000; margin: 8px 0;">
            <div class="op-row"><span>Electrical Installation Fee</span> <span>{st.session_state.fees['Electrical Installation Fee']:.2f}</span></div>
            <div class="op-row"><span>Plumbing Installation Fee</span> <span>{st.session_state.fees['Plumbing Installation Fee']:.2f}</span></div>
            <div class="op-row"><span>Building Occupancy Fee</span> <span>{st.session_state.fees['Building Occupancy Fee']:.2f}</span></div>
            <div class="op-row"><span>Building Inspection Fee</span> <span>{st.session_state.fees['Building Inspection Fee']:.2f}</span></div>
            <div class="op-row"><span>Certification Fee</span> <span>{st.session_state.fees['Certification Fee']:.2f}</span></div>
            
            <div class="op-total">
                <div class="op-row"><span>Total Assessment</span> <span>{total_assessment:,.2f}</span></div>
            </div>
            
            <div style="margin-top: 10px;">
                <div class="op-row"><span>Local Gov't Share (80%)</span> <span>{local_share:,.2f}</span></div>
                <div class="op-row"><span>National Gov't Share (20%)</span> <span>{nat_share:,.2f}</span></div>
            </div>
            
            <div style="margin-top: 15px; font-size: 11px;">
                <strong>Assessed by:</strong><br>
                ENGR. AIRSAD R. OLOMODIN, PhD, PECE<br>
                Building Official / Economic Zone Engineer
            </div>
            <div style="margin-top: 10px; font-size: 11px; font-style: italic;">
                Note: {treasurer_note}
            </div>
            <div style="margin-top: 10px;">
                OR No: ___________________
            </div>
        </div>
        """, unsafe_allow_html=True)
