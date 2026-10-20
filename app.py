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

st.set_page_config(
    page_title="PH Building Permit Fee Calculator (NBCDO MC 03)",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Philippine Building Permit Fee Calculator")
st.markdown("### Strict compliance with NBCDO Memorandum Circular No. 03 (Revised IRR of PD 1096)")

st.sidebar.title("Navigation & Modules")
module = st.sidebar.radio(
    "Select Permit Module:",
    [
        "1. General Building & Valuation",
        "2. Electrical Permit Fees",
        "3. Mechanical Permit Fees",
        "4. Plumbing Permit Fees",
        "5. Electronics Permit Fees",
        "6. Accessories & Structures",
        "7. Other Fees & Permits",
        "8. Certificates & Annual Inspections",
        "📊 Grand Summary & Export"
    ]
)

# Initialize Session State for persistence across modules
if "fees_summary" not in st.session_state:
    st.session_state.fees_summary = {
        "Building Fee": 0.0,
        "Electrical Fee": 0.0,
        "Mechanical Fee": 0.0,
        "Plumbing Fee": 0.0,
        "Electronics Fee": 0.0,
        "Accessories Fee": 0.0,
        "Other Fees": 0.0,
        "Certificate & Inspection Fee": 0.0
    }

# --- MODULE 1: BUILDING FEES ---
if module == "1. General Building & Valuation":
    st.header("Module 1: Bases of Assessment & Building Fees")
    col1, col2 = st.columns(2)
    with col1:
        group_choice = st.selectbox("Occupancy Group", ["Group A-1 (Residential Single)", "Group A-2 (Residential Duplex/Multi)", "Groups B, C, E, F, G, H, I, J-1 (Commercial/Institutional/Industrial)", "Groups C-2, D (Residential Apartments/Assembly/Schools)"])
        floor_area = st.number_input("Total Floor Area (sq. meters)", min_value=0.0, value=75.0, step=1.0)
    with col2:
        is_original = st.checkbox("Original Complete Construction", value=True)
        
    # Map selection to division & group
    if "A-1" in group_choice:
        division = "A-1"
        group = "Group A"
    elif "A-2" in group_choice:
        division = "A-2"
        group = "Group A"
    elif "Commercial/Institutional/Industrial" in group_choice:
        division = "B-1"
        group = "Group B"
    else:
        division = "C-2"
        group = "Group C"
        
    fixed_rate = get_fixed_cost_per_sqm(group)
    estimated_valuation = floor_area * fixed_rate
    building_fee = compute_building_fee(division, floor_area, is_original)
    
    st.info(f"**Fixed Construction Cost per Sq. Meter:** ₱{fixed_rate:,.2f}\n\n**Estimated Total Construction Cost (Valuation):** ₱{estimated_valuation:,.2f}")
    st.success(f"**Calculated Building Permit Fee:** ₱{building_fee:,.2f}")
    
    st.session_state.fees_summary["Building Fee"] = building_fee
    st.session_state["building_valuation"] = estimated_valuation
    st.session_state["floor_area"] = floor_area
    st.session_state["division"] = division

# --- MODULE 2: ELECTRICAL FEES ---
elif module == "2. Electrical Permit Fees":
    st.header("Module 2: Electrical Permit Fees (Section 4)")
    col1, col2 = st.columns(2)
    with col1:
        connected_load = st.number_input("Total Connected Load (kVA)", min_value=0.0, value=15.0)
        trans_gen_kva = st.number_input("Total Transformer / UPS / Generator Capacity (kVA)", min_value=0.0, value=0.0)
        poles = st.number_input("Power Supply Poles", min_value=0, value=0)
        guys = st.number_input("Guying Attachments", min_value=0, value=0)
    with col2:
        occ_type = st.selectbox("Occupancy Type", ["Residential", "Commercial / Industrial", "Institutional"])
        num_meters = st.number_input("Electric Meters", min_value=0, value=1)
        num_permits = st.number_input("Wiring Permits Issuance", min_value=0, value=1)
        
    elec_fee = compute_electrical_fees(connected_load, trans_gen_kva, poles, guys, occ_type, num_meters, num_permits)
    st.success(f"**Calculated Electrical Permit Fee:** ₱{elec_fee:,.2f}")
    st.session_state.fees_summary["Electrical Fee"] = elec_fee
    st.session_state["electrical_fee_raw"] = elec_fee

# --- MODULE 3: MECHANICAL FEES ---
elif module == "3. Mechanical Permit Fees":
    st.header("Module 3: Mechanical Permit Fees (Section 5)")
    col1, col2, col3 = st.columns(3)
    with col1:
        ref_tons = st.number_input("Refrigeration/Cold Storage (tons)", min_value=0.0, value=0.0)
        ice_tons = st.number_input("Ice Plants (tons)", min_value=0.0, value=0.0)
        ac_100 = st.number_input("Centralized AC up to 100 tons", min_value=0.0, value=0.0)
        window_ac = st.number_input("Window Type AC units", min_value=0, value=0)
        vent_kw = st.number_input("Mechanical Ventilation (kW)", min_value=0.0, value=0.0)
    with col2:
        escalator_m = st.number_input("Escalators / Moving Walks (lineal meters)", min_value=0.0, value=0.0)
        elev_pass = st.number_input("Passenger Elevators", min_value=0, value=0)
        elev_freight = st.number_input("Freight Elevators", min_value=0, value=0)
        boiler_kw = st.number_input("Boilers (kW)", min_value=0.0, value=0.0)
        pumps_kw = st.number_input("Water/Sump/Sewage Pumps (kW)", min_value=0.0, value=0.0)
    with col3:
        sprinklers = st.number_input("Automatic Fire Sprinkler Heads", min_value=0, value=0)
        gen_kw = st.number_input("Generating Units (kW)", min_value=0.0, value=0.0)
        pressure_vessels = st.number_input("Pressure Vessels (cu. meters)", min_value=0.0, value=0.0)
        machinery_kw = st.number_input("Other Machineries (kW)", min_value=0.0, value=0.0)
        
    mech_fee = compute_mechanical_fees(
        ref_cold_storage_tons=ref_tons, ice_plants_tons=ice_tons, ac_up_to_100_tons=ac_100,
        ac_above_100_tons=0.0, window_ac_units=window_ac, ventilation_kw=vent_kw,
        escalators_meters=escalator_m, elevators_dumbwaiter=0, elevators_construction=0,
        elevators_passenger=elev_pass, elevators_freight=elev_freight, elevators_car=0,
        boiler_kw=boiler_kw, pressure_water_heaters=0, pumps_kw=pumps_kw,
        sprinkler_heads=sprinklers, gen_kw=gen_kw, gases_outlets=0, gas_meters=0,
        power_piping_meters=0.0, other_ice_kw=0.0, pressure_vessels_cum=pressure_vessels,
        other_machinery_kw=machinery_kw, ducts_conveyors_meters=0.0, weighing_scale_tons=0.0
    )
    st.success(f"**Calculated Mechanical Permit Fee:** ₱{mech_fee:,.2f}")
    st.session_state.fees_summary["Mechanical Fee"] = mech_fee

# --- MODULE 4: PLUMBING FEES ---
elif module == "4. Plumbing Permit Fees":
    st.header("Module 4: Plumbing Permit Fees (Section 6)")
    col1, col2 = st.columns(2)
    with col1:
        std_units = st.number_input("Standard Plumbing Units (1 unit = 1 WC, 2 floor drains, 1 lavatory, 1 sink, 3 faucets, 1 shower)", min_value=0, value=1)
        exc_wc = st.number_input("Excess Water Closets", min_value=0, value=0)
        exc_fd = st.number_input("Excess Floor Drains", min_value=0, value=0)
        exc_lav = st.number_input("Excess Lavatories", min_value=0, value=0)
    with col2:
        urinals = st.number_input("Special Fixtures: Urinals", min_value=0, value=0)
        bathtubs = st.number_input("Special Fixtures: Bathtubs", min_value=0, value=0)
        meters_small = st.number_input("Water Meters (12-25mm Ø)", min_value=0, value=1)
        septic_cum = st.number_input("Septic Tank Digestion Chamber (cu. meters)", min_value=0.0, value=0.0)
        
    special_dict = {"urinal": urinals, "bath_tub": bathtubs}
    plumbing_fee = compute_plumbing_fees(
        standard_units=std_units, excess_water_closets=exc_wc, excess_floor_drains=exc_fd,
        excess_sinks=0, excess_lavatories=exc_lav, excess_faucets=0, excess_shower_heads=0,
        special_fixtures_dict=special_dict, water_meters_12_25mm=meters_small,
        water_meters_above_25mm=0, septic_tank_cum=septic_cum
    )
    st.success(f"**Calculated Plumbing Permit Fee:** ₱{plumbing_fee:,.2f}")
    st.session_state.fees_summary["Plumbing Fee"] = plumbing_fee
    st.session_state["plumbing_units_total"] = std_units + exc_wc + exc_fd + exc_lav

# --- MODULE 5: ELECTRONICS FEES ---
elif module == "5. Electronics Permit Fees":
    st.header("Module 5: Electronics Permit Fees (Section 7)")
    col1, col2 = st.columns(2)
    with col1:
        ports = st.number_input("Switching / PABX / Network Ports", min_value=0, value=0)
        outlets = st.number_input("Electronics & Communications Outlets", min_value=0, value=0)
        terminations = st.number_input("Security / Fire Alarm / CCTV Terminations", min_value=0, value=0)
    with col2:
        towers = st.number_input("Antenna Towers / Masts", min_value=0, value=0)
        signages = st.number_input("Electronic Signages & Displays", min_value=0, value=0)
        other_elec = st.number_input("Other Electronics Devices", min_value=0, value=0)
        
    elec_permit_fee = compute_electronics_fees(
        ports=ports, locations_broadcast=0, atms_vending_medical=0,
        outlets=outlets, terminations=terminations, studios_theaters=0,
        antenna_towers=towers, signages=signages, poles=0, attachments=0, other_devices=other_elec
    )
    st.success(f"**Calculated Electronics Permit Fee:** ₱{elec_permit_fee:,.2f}")
    st.session_state.fees_summary["Electronics Fee"] = elec_permit_fee

# --- MODULE 6: ACCESSORIES & STRUCTURES ---
elif module == "6. Accessories & Structures":
    st.header("Module 6: Accessories of Building / Structure Fees (Section 8)")
    col1, col2 = st.columns(2)
    with col1:
        balcony_sqm = st.number_input("Open Balconies / Terraces / Lanais (sq. meters)", min_value=0.0, value=0.0)
        pool_res = st.number_input("Residential Swimming Pool (cu. meters)", min_value=0.0, value=0.0)
        firewall_sqm = st.number_input("Firewall Construction (sq. meters)", min_value=0.0, value=0.0)
    with col2:
        towers_detached = st.number_input("Self-Supporting Towers (Single Detached)", min_value=0, value=0)
        tanks_above = st.number_input("Above-ground Water Tanks (Group A/B, cu. meters)", min_value=0.0, value=0.0)
        
    principal_rate = 10.0 # Default baseline rate per sqm
    acc_fee = compute_accessories_fees(
        balcony_area=balcony_sqm, principal_rate_per_sqm=principal_rate, height_above_8m_cum=0.0,
        vault_volume=0.0, pool_residential_cum=pool_res, pool_commercial_cum=0.0,
        pool_institutional_cum=0.0, pool_shower_rooms=0, firewall_sqm=firewall_sqm,
        towers_single_detached=towers_detached, towers_comm_up_to_10m=0, towers_comm_excess_m=0.0,
        towers_inst_up_to_10m=0, towers_inst_excess_m=0.0, silos_up_to_10m=0, silos_excess_m=0.0,
        smokestack_up_to_10m=0, smokestack_excess_m=0.0, chimney_up_to_10m=0, chimney_excess_m=0.0,
        fixed_ovens_sqm=0.0, industrial_kiln_cum=0.0, tanks_abovetank_group_ab_cum=tanks_above,
        tanks_abovetank_other_cum=0.0, treatment_tanks_cum=0.0, comm_tanks_above_cum=0.0,
        comm_tanks_under_cum=0.0, booths_permanent_sqm=0.0, booths_temporary_sqm=0.0,
        cemetery_tombs_sqm=0.0, cemetery_semi_mausoleum_sqm=0.0, cemetery_fully_mausoleum_sqm=0.0,
        cemetery_multi_level_sqm=0.0, cemetery_columbarium_sqm=0.0
    )
    st.success(f"**Calculated Accessories Fee:** ₱{acc_fee:,.2f}")
    st.session_state.fees_summary["Accessories Fee"] = acc_fee

# --- MODULE 7: OTHER FEES & PERMITS ---
elif module == "7. Other Fees & Permits":
    st.header("Module 7: Other Fees & Accessory Permits (Section 9 & 10)")
    col1, col2 = st.columns(2)
    with col1:
        line_grade = st.number_input("Line and Grade (lineal meters fronting streets)", min_value=0.0, value=0.0)
        fencing_m = st.number_input("Masonry/Concrete Fencing (lineal meters up to 1.80m)", min_value=0.0, value=0.0)
        repair_cost = st.number_input("Building Repairs Detailed Cost (₱)", min_value=0.0, value=0.0)
    with col2:
        demolition_sqm = st.number_input("Demolition Floor Area (sq. meters)", min_value=0.0, value=0.0)
        pavement_sqm = st.number_input("Pavement Area (sq. meters excess of 20 sqm)", min_value=0.0, value=0.0)
        
    other_fee = compute_other_fees(
        line_grade_m=line_grade, gp_inspection=False, gp_excavation_cum=0.0, gp_permit_issuance=False,
        basement_excavation_cum=0.0, other_excavation_cum=0.0, footing_encroachment_sqm=0.0,
        fencing_masonry_m=fencing_m, fencing_masonry_height_over_18m_m=0.0, fencing_indigenous_m=0.0,
        pavement_up_to_20_sqm=False, pavement_excess_sqm=pavement_sqm, street_occupancy_up_to_20_sqm_months=0,
        street_occupancy_excess_sqm_months=0.0, scaffolding_up_to_10m_months=0, scaffolding_excess_m_months=0.0,
        sign_erection_up_to_4_sqm=0, sign_erection_excess_sqm=0.0, sign_installation_sqm=0.0,
        sign_installation_type="Neon", sign_installation_category="Business", sign_renewal_sqm=0.0,
        sign_renewal_type="Neon", sign_renewal_category="Business", repair_vertical_sqm=0.0,
        repair_horizontal_sqm=0.0, repair_cost=repair_cost, demolition_building_sqm=demolition_sqm,
        demolition_frames_m=0.0, demolition_structures_up_to_10m=0, demolition_structures_excess_m=0.0, moving_sqm=0.0
    )
    st.success(f"**Calculated Other Fees:** ₱{other_fee:,.2f}")
    st.session_state.fees_summary["Other Fees"] = other_fee

# --- MODULE 8: CERTIFICATES & INSPECTIONS ---
elif module == "8. Certificates & Annual Inspections":
    st.header("Module 8: Certificates of Occupancy & Annual Inspection Fees (Sections 10 & 11)")
    valuation = st.session_state.get("building_valuation", 750000.0)
    floor_area = st.session_state.get("floor_area", 75.0)
    division = st.session_state.get("division", "A-1")
    plumbing_units = st.session_state.get("plumbing_units_total", 1)
    elec_fee_raw = st.session_state.get("electrical_fee_raw", 200.0)
    
    occ_cert = compute_occupancy_certificate_fee(division, valuation, floor_area)
    annual_insp = compute_annual_inspection_fees(floor_area, plumbing_units, elec_fee_raw)
    total_cert_insp = occ_cert + annual_insp
    
    st.info(f"**Certificate of Occupancy Fee:** ₱{occ_cert:,.2f}\n\n**Annual Inspection Fees (Building + Plumbing + Electrical):** ₱{annual_insp:,.2f}")
    st.success(f"**Total Certificates & Inspection Fees:** ₱{total_cert_insp:,.2f}")
    st.session_state.fees_summary["Certificate & Inspection Fee"] = total_cert_insp

# --- MODULE 9: GRAND SUMMARY & EXPORT ---
else:
    st.header("📊 Grand Summary & Bill of Fees")
    st.markdown("Comprehensive breakdown of all computed building permit fees and charges in accordance with NBCDO MC No. 03.")
    
    summary_df = pd.DataFrame(list(st.session_state.fees_summary.items()), columns=["Fee Category", "Amount (₱)"])
    summary_df["Amount (₱)"] = summary_df["Amount (₱)"].apply(lambda x: f"₱{x:,.2f}")
    
    grand_total = sum(st.session_state.fees_summary.values())
    
    st.table(summary_df)
    st.markdown(f"### **Grand Total Building Permit Fees: ₱{grand_total:,.2f}**")
    
    # Export CSV button
    csv_data = pd.DataFrame(list(st.session_state.fees_summary.items()), columns=["Fee Category", "Amount (PHP)"])
    csv_data.loc[len(csv_data)] = ["Grand Total", grand_total]
    csv_string = csv_data.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Download Bill of Fees (CSV Report)",
        data=csv_string,
        file_name="ph_building_permit_fee_summary.csv",
        mime="text/csv"
    )
