import streamlit as st
import pandas as pd
import datetime
import base64
import os
import streamlit.components.v1 as components
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

# Function to load and encode image to base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    return ""

logo_path = "BEZA-LOGO-Copy-300x300.png"
logo_base64 = get_base64_image(logo_path)
logo_data_uri = f"data:image/png;base64,{logo_base64}" if logo_base64 else ""

# Custom CSS for Government Desktop Theme
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

# LGU Banner with Native Streamlit Columns for Perfect Logo Alignment
st.markdown("""
<div class="bpfau-banner">
    <h4 style="margin: 0; font-size: 13px; letter-spacing: 1.5px; color: #d1e8ff; text-transform: uppercase;">Republic of the Philippines</h4>
    <h2 style="margin: 4px 0; font-size: 20px; font-weight: 800; color: #ffffff;">OFFICE OF THE BUILDING OFFICIAL / BEZA DESK</h2>
    <p style="margin: 0; font-size: 12px; font-style: italic; color: #ffd700;">"Automated Assessment Desk & Printable Order of Payment Generator"</p>
</div>
""", unsafe_allow_html=True)

if logo_base64:
    col_logo, col_banner_text = st.columns([1, 6])
    with col_logo:
        st.image(logo_path, width=90)
    with col_banner_text:
        st.empty()

# Initialize Session State Database & Records
if "applicants_db" not in st.session_state:
    st.session_state.applicants_db = [
        {
            "tracking_no": "OBO-20261020-001",
            "applicant": "Airsad R. Olomodin",
            "project": "Commercial Warehouse Building",
            "stage": "Building Permit Stage",
            "total_fee": 2222.00,
            "date": "10/20/2026",
            "status": "Pending Payment"
        }
    ]

if "fees" not in st.session_state:
    st.session_state.fees = {
        "Building Permit Fee": 360.00,
        "Electrical Installation Fee": 230.00,
        "Mechanical Installation Fee": 0.00,
        "Plumbing Installation Fee": 94.00,
        "Electronics Permit Fee": 0.00,
        "Accessories Fee": 0.00,
        "Other Permits Fee": 0.00
    }

if "post_fees" not in st.session_state:
    st.session_state.post_fees = {
        "Building Occupancy Certificate Fee": 1000.00,
        "Annual Inspection Fee": 983.00,
        "Certification Fee": 250.00
    }

# Sidebar Navigation
st.sidebar.markdown("### ⚙️ System Controls")
portal_mode = st.sidebar.radio(
    "Portal View",
    [
        "📋 Assessment Desk (Building Permit)", 
        "🔍 Occupancy & Post-Construction", 
        "📊 OBO Admin Registry (Manager View)"
    ]
)

authority_mode = st.sidebar.selectbox(
    "Jurisdiction / Authority Mode",
    ["Standard LGU (80% Local / 20% National)", "BEZA Economic Zone (Direct Ecozone Assessment)"]
)

# --- VIEW 1: ASSESSMENT DESK (BUILDING PERMIT) ---
if portal_mode == "📋 Assessment Desk (Building Permit)":
    st.markdown("""
    <div class="section-title-bar">
        STAGE 1: BUILDING PERMIT APPLICATION & UPFRONT FEE ASSESSMENT
    </div>
    """, unsafe_allow_html=True)

    col_meta1, col_meta2, col_meta3 = st.columns(3)
    with col_meta1:
        applicant_name = st.text_input("Applicant / Owner Name", value="Airsad R. Olomodin")
    with col_meta2:
        project_title = st.text_input("Project Name / Description", value="Commercial Warehouse Building")
    with col_meta3:
        tracking_no = st.text_input("Tracking Number", value=f"OBO-{datetime.datetime.now().strftime('%Y%m%d')}-0142")

    tabs = st.tabs([
        "🏢 Building Fees", 
        "⚡ Electrical Fees", 
        "🔧 Mechanical Fees", 
        "🚰 Plumbing Fees", 
        "📡 Electronics Fees", 
        "🏗️ Accessories", 
        "📋 Other Fees", 
        "📄 Printable Order of Payment"
    ])

    with tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            group_choice = st.selectbox("Occupancy Group", ["Group A-1 (Residential Single)", "Group A-2 (Residential Duplex/Multi)", "Groups B, C, E, F, G, H, I, J-1 (Commercial/Institutional)", "Groups C-2, D (Apartments/Schools)"])
            floor_area = st.number_input("Total Floor Area (SqM)", min_value=1.0, value=75.0)
            is_original = st.checkbox("Original Complete Construction", value=True)
        with col2:
            division = "A-1" if "A-1" in group_choice else ("A-2" if "A-2" in group_choice else ("B-1" if "Commercial" in group_choice else "C-2"))
            group = "Group A" if "Group A" in group_choice else "Group B"
            fixed_rate = get_fixed_cost_per_sqm(group)
            building_fee = compute_building_fee(division, floor_area, is_original)
            st.info(f"**Fixed Cost Rate:** ₱{fixed_rate:,.2f}/sqm\n\n**Estimated Valuation:** ₱{floor_area * fixed_rate:,.2f}")
            st.success(f"**Computed Building Fee:** ₱{building_fee:,.2f}")
            st.session_state.fees["Building Permit Fee"] = building_fee
            st.session_state["building_valuation"] = floor_area * fixed_rate
            st.session_state["floor_area"] = floor_area

    with tabs[1]:
        col1, col2 = st.columns(2)
        with col1:
            connected_load = st.number_input("Total Connected Load (kVA)", min_value=0.0, value=15.0)
            trans_kva = st.number_input("Transformer / Generator Capacity (kVA)", min_value=0.0, value=0.0)
            occ_type = st.selectbox("Occupancy Type", ["Residential", "Commercial / Industrial", "Institutional"])
            num_meters = st.number_input("Electric Meters Count", min_value=0, value=1)
        with col2:
            try:
                elec_fee = compute_electrical_fees(connected_load, trans_kva, 0, 0, occ_type, num_meters, 1)
            except Exception:
                elec_fee = 230.00
            st.success(f"**Computed Electrical Fee:** ₱{elec_fee:,.2f}")
            st.session_state.fees["Electrical Installation Fee"] = elec_fee

    with tabs[2]:
        col1, col2 = st.columns(2)
        with col1:
            ref_tons = st.number_input("Refrigeration / AC (tons)", min_value=0.0, value=0.0)
        with col2:
            try:
                mech_fee = compute_mechanical_fees(ref_tons, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0.0, 0, 0.0, 0, 0.0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
            except Exception:
                mech_fee = 0.0
            st.success(f"**Computed Mechanical Fee:** ₱{mech_fee:,.2f}")
            st.session_state.fees["Mechanical Installation Fee"] = mech_fee

    with tabs[3]:
        col1, col2 = st.columns(2)
        with col1:
            std_units = st.number_input("Standard Plumbing Units", min_value=0, value=1)
            excess_wc = st.number_input("Excess Water Closets", min_value=0, value=0)
        with col2:
            try:
                plumbing_fee = compute_plumbing_fees(std_units, excess_wc, 0, 0, 0, 0, 0, {}, 1, 0, 0.0)
            except Exception:
                plumbing_fee = 94.00
            st.success(f"**Computed Plumbing Fee:** ₱{plumbing_fee:,.2f}")
            st.session_state.fees["Plumbing Installation Fee"] = plumbing_fee

    with tabs[4]:
        col1, col2 = st.columns(2)
        with col1:
            outlets = st.number_input("Electronics Outlets", min_value=0, value=0)
        with col2:
            try:
                elec_perm_fee = compute_electronics_fees(0, 0, 0, outlets, 0, 0, 0, 0, 0, 0, 0)
            except Exception:
                elec_perm_fee = 0.0
            st.success(f"**Computed Electronics Fee:** ₱{elec_perm_fee:,.2f}")
            st.session_state.fees["Electronics Permit Fee"] = elec_perm_fee

    with tabs[5]:
        col1, col2 = st.columns(2)
        with col1:
            balcony = st.number_input("Balcony / Terrace Area (sq. meters)", min_value=0.0, value=0.0)
        with col2:
            try:
                acc_fee = compute_accessories_fees(balcony, 10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0, 0, 0.0, 0, 0.0, 0, 0.0, 0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
            except Exception:
                acc_fee = 0.0
            st.success(f"**Computed Accessories Fee:** ₱{acc_fee:,.2f}")
            st.session_state.fees["Accessories Fee"] = acc_fee

    with tabs[6]:
        col1, col2 = st.columns(2)
        with col1:
            demolition = st.number_input("Demolition Floor Area (sq. meters)", min_value=0.0, value=0.0)
        with col2:
            try:
                other_fee = compute_other_fees(0.0, False, 0.0, False, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, False, 0.0, 0, 0.0, 0, 0.0, 0, 0.0, 0.0, "Neon", "Business", 0.0, "Neon", "Business", 0.0, 0.0, 0.0, demolition, 0.0, 0, 0.0, 0.0)
            except Exception:
                other_fee = 0.0
            st.success(f"**Computed Other Permits Fee:** ₱{other_fee:,.2f}")
            st.session_state.fees["Other Permits Fee"] = other_fee

    with tabs[7]:
        col_left, col_right = st.columns([1.1, 1])
        total_assessment = sum(st.session_state.fees.values())
        
        with col_left:
            st.subheader("Assessed Fee Summary")
            for item, amount in st.session_state.fees.items():
                if amount > 0:
                    st.write(f"• **{item}**: ₱{amount:,.2f}")
            st.markdown(f"### **Total Assessment: ₱{total_assessment:,.2f}**")
            
            if st.button("💾 Save Application to OBO Registry"):
                new_record = {
                    "tracking_no": tracking_no,
                    "applicant": applicant_name,
                    "project": project_title,
                    "stage": "Building Permit Stage",
                    "total_fee": total_assessment,
                    "date": datetime.datetime.now().strftime("%m/%d/%Y"),
                    "status": "Pending Payment"
                }
                existing_idx = next((i for i, item in enumerate(st.session_state.applicants_db) if item["tracking_no"] == tracking_no), None)
                if existing_idx is not None:
                    st.session_state.applicants_db[existing_idx] = new_record
                else:
                    st.session_state.applicants_db.append(new_record)
                st.success(f"Application {tracking_no} successfully saved to OBO Registry!")

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

            receipt_rows = ""
            for item, amount in st.session_state.fees.items():
                if amount > 0:
                    receipt_rows += f'<div class="op-row"><span>{item}</span> <span>{amount:,.2f}</span></div>\n'

            receipt_html = f"""
            <html>
            <head>
            <style>
                body {{ background: #f4f4f4; padding: 10px; font-family: 'Courier New', Courier, monospace; }}
                .op-receipt {{
                    position: relative;
                    background-color: #ffffff;
                    border: 1px solid #111;
                    padding: 20px;
                    font-size: 13px;
                    color: #000;
                    max-width: 450px;
                    margin: auto;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .op-watermark {{
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    width: 280px;
                    height: 280px;
                    opacity: 0.10;
                    z-index: 0;
                    pointer-events: none;
                }}
                .op-content {{
                    position: relative;
                    z-index: 1;
                }}
                .op-header {{
                    text-align: center;
                    font-weight: bold;
                    text-transform: uppercase;
                    border-bottom: 1px dashed #000;
                    padding-bottom: 10px;
                    margin-bottom: 10px;
                }}
                .op-row {{
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 4px;
                }}
                .op-total {{
                    border-top: 1px dashed #000;
                    border-bottom: 2px double #000;
                    padding: 6px 0;
                    font-weight: bold;
                    margin-top: 10px;
                }}
                .print-btn {{
                    display: block;
                    width: 100%;
                    background: #0056b3;
                    color: white;
                    border: none;
                    padding: 10px;
                    font-size: 14px;
                    font-weight: bold;
                    cursor: pointer;
                    margin-top: 15px;
                    border-radius: 4px;
                }}
                .print-btn:hover {{ background: #003d82; }}
                @media print {{
                    body {{ background: #fff; padding: 0; }}
                    .print-btn {{ display: none; }}
                    .op-receipt {{ border: none; box-shadow: none; width: 100%; }}
                }}
            </style>
            </head>
            <body>
            <div class="op-receipt">
                <img src="{logo_data_uri}" class="op-watermark">
                <div class="op-content">
                    <div class="op-header">
                        {header_title}<br>
                        BUILDING PERMIT ORDER OF PAYMENT
                    </div>
                    <div class="op-row"><span>Tracking No:</span> <span>{tracking_no}</span></div>
                    <div class="op-row"><span>Applicant:</span> <span>{applicant_name}</span></div>
                    <div class="op-row"><span>Date:</span> <span>{datetime.datetime.now().strftime("%m/%d/%Y")}</span></div>
                    <hr style="border-top: 1px dashed #000; margin: 8px 0;">
                    {receipt_rows}
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
                    <button class="print-btn" onclick="window.print()">🖨️ Print Order of Payment</button>
                </div>
            </div>
            </body>
            </html>
            """
            components.html(receipt_html, height=540, scrolling=True)

# --- VIEW 2: OCCUPANCY & POST-CONSTRUCTION ---
elif portal_mode == "🔍 Occupancy & Post-Construction":
    st.markdown("""
    <div class="section-title-bar">
        STAGE 2: OCCUPANCY CERTIFICATE & POST-CONSTRUCTION INSPECTION DESK
    </div>
    """, unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        lookup_track = st.text_input("Enter Project Tracking Number", value="OBO-20261020-001")
        st.info("Loaded project from registry for completion assessment.")
        
        valuation = st.session_state.get("building_valuation", 750000.0)
        floor_area_val = st.session_state.get("floor_area", 75.0)
        elec_base = st.session_state.fees.get("Electrical Installation Fee", 230.00)
        
        occ_cert = compute_occupancy_certificate_fee("A-1", valuation, floor_area_val)
        bldg_insp = compute_annual_inspection_fees(floor_area_val, 2, elec_base)
        cert_fee = st.number_input("Certification Fee (₱)", min_value=0.0, value=250.00)
        
        st.session_state.post_fees["Building Occupancy Certificate Fee"] = occ_cert
        st.session_state.post_fees["Annual Inspection Fee"] = bldg_insp
        st.session_state.post_fees["Certification Fee"] = cert_fee

        total_post = sum(st.session_state.post_fees.values())
        st.success(f"**Occupancy Certificate Fee:** ₱{occ_cert:,.2f}\n\n**Annual Inspection Fee:** ₱{bldg_insp:,.2f}\n\n### **Total Post-Construction Fee: ₱{total_post:,.2f}**")

    with col_s2:
        if "BEZA" in authority_mode:
            p_local = total_post * 1.00
            p_nat = 0.00
            p_header = "BANGSAMORO ECONOMIC ZONE AUTHORITY"
            p_note = "Please pay at the BEZA Finance / Cashier Office."
        else:
            p_local = total_post * 0.80
            p_nat = total_post * 0.20
            p_header = "OFFICE OF THE BUILDING OFFICIAL"
            p_note = "Please pay at the Municipal Treasurer's Office."

        post_rows = ""
        for item, amount in st.session_state.post_fees.items():
            post_rows += f'<div class="op-row"><span>{item}</span> <span>{amount:,.2f}</span></div>\n'

        post_receipt_html = f"""
        <html>
        <head>
        <style>
            body {{ background: #f4f4f4; padding: 10px; font-family: 'Courier New', Courier, monospace; }}
            .op-receipt {{
                position: relative;
                background-color: #ffffff;
                border: 1px solid #111;
                padding: 20px;
                font-size: 13px;
                color: #000;
                max-width: 450px;
                margin: auto;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .op-watermark {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 280px;
                height: 280px;
                opacity: 0.10;
                z-index: 0;
                pointer-events: none;
            }}
            .op-content {{
                position: relative;
                z-index: 1;
            }}
            .op-header {{
                text-align: center;
                font-weight: bold;
                text-transform: uppercase;
                border-bottom: 1px dashed #000;
                padding-bottom: 10px;
                margin-bottom: 10px;
            }}
            .op-row {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 4px;
            }}
            .op-total {{
                border-top: 1px dashed #000;
                border-bottom: 2px double #000;
                padding: 6px 0;
                font-weight: bold;
                margin-top: 10px;
            }}
            .print-btn {{
                display: block;
                width: 100%;
                background: #0056b3;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                cursor: pointer;
                margin-top: 15px;
                border-radius: 4px;
            }}
            .print-btn:hover {{ background: #003d82; }}
            @media print {{
                body {{ background: #fff; padding: 0; }}
                .print-btn {{ display: none; }}
                .op-receipt {{ border: none; box-shadow: none; width: 100%; }}
            }}
        </style>
        </head>
        <body>
        <div class="op-receipt">
            <img src="{logo_data_uri}" class="op-watermark">
            <div class="op-content">
                <div class="op-header">
                    {p_header}<br>
                    OCCUPANCY & INSPECTION ORDER OF PAYMENT
                </div>
                <div class="op-row"><span>Tracking No:</span> <span>{lookup_track}</span></div>
                <div class="op-row"><span>Status:</span> <span style="color: green; font-weight: bold;">PROJECT COMPLETED</span></div>
                <hr style="border-top: 1px dashed #000; margin: 8px 0;">
                {post_rows}
                <div class="op-total">
                    <div class="op-row"><span>Total Assessment</span> <span>{total_post:,.2f}</span></div>
                </div>
                <div style="margin-top: 10px;">
                    <div class="op-row"><span>Local Gov't Share (80%)</span> <span>{p_local:,.2f}</span></div>
                    <div class="op-row"><span>National Gov't Share (20%)</span> <span>{p_nat:,.2f}</span></div>
                </div>
                <div style="margin-top: 15px; font-size: 11px;">
                    <strong>Approved by:</strong><br>
                    ENGR. AIRSAD R. OLOMODIN, PhD, PECE<br>
                    Building Official / Economic Zone Engineer
                </div>
                <div style="margin-top: 10px; font-size: 11px; font-style: italic;">
                    Note: {p_note}
                </div>
                <div style="margin-top: 10px;">
                    OR No: ___________________
                </div>
                <button class="print-btn" onclick="window.print()">🖨️ Print Occupancy Order of Payment</button>
            </div>
        </div>
        </body>
        </html>
        """
        components.html(post_receipt_html, height=520, scrolling=True)

# --- VIEW 3: OBO ADMIN REGISTRY (MANAGER VIEW) ---
else:
    st.markdown("""
    <div class="section-title-bar">
        OBO ADMIN REGISTRY & APPLICANT TRACKING DATABASE
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📁 Saved Applications & Project Records")
    df_db = pd.DataFrame(st.session_state.applicants_db)
    
    if not df_db.empty:
        st.dataframe(df_db, use_container_width=True)
        
        st.markdown("### 🔍 Record Management & Status Update")
        selected_track = st.selectbox("Select Tracking Number to Manage", df_db["tracking_no"].tolist())
        
        record = next((item for item in st.session_state.applicants_db if item["tracking_no"] == selected_track), None)
        
        if record:
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.info(f"**Applicant:** {record['applicant']}\n\n**Project:** {record['project']}\n\n**Total Fee:** ₱{record['total_fee']:,.2f}")
            with col_m2:
                new_status = st.selectbox("Update Application Status", ["Pending Payment", "Paid / Permit Issued", "Construction Complete", "Occupancy Certified"], index=["Pending Payment", "Paid / Permit Issued", "Construction Complete", "Occupancy Certified"].index(record["status"]))
                if st.button("Update Status"):
                    record["status"] = new_status
                    st.success(f"Status for {selected_track} updated to **{new_status}**!")
                    st.rerun()
    else:
        st.info("No applicant records found in registry.")
