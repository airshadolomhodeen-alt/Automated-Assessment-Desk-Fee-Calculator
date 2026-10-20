def compute_other_fees(line_grade_m: float,
                       gp_inspection: bool,
                       gp_excavation_cum: float,
                       gp_permit_issuance: bool,
                       basement_excavation_cum: float,
                       other_excavation_cum: float,
                       footing_encroachment_sqm: float,
                       fencing_masonry_m: float,
                       fencing_masonry_height_over_18m_m: float,
                       fencing_indigenous_m: float,
                       pavement_up_to_20_sqm: bool,
                       pavement_excess_sqm: float,
                       street_occupancy_up_to_20_sqm_months: int,
                       street_occupancy_excess_sqm_months: float,
                       scaffolding_up_to_10m_months: int,
                       scaffolding_excess_m_months: float,
                       sign_erection_up_to_4_sqm: int,
                       sign_erection_excess_sqm: float,
                       sign_installation_sqm: float,
                       sign_installation_type: str,
                       sign_installation_category: str,
                       sign_renewal_sqm: float,
                       sign_renewal_type: str,
                       sign_renewal_category: str,
                       repair_vertical_sqm: float,
                       repair_horizontal_sqm: float,
                       repair_cost: float,
                       demolition_building_sqm: float,
                       demolition_frames_m: float,
                       demolition_structures_up_to_10m: int,
                       demolition_structures_excess_m: float,
                       moving_sqm: float) -> float:
    total = 0.0
    
    if line_grade_m > 0:
        if line_grade_m <= 10.0:
            total += 24.0
        else:
            total += 24.0 + (line_grade_m - 10.0) * 2.40
            
    if gp_inspection:
        total += 200.0
    if gp_permit_issuance:
        total += 50.0
    total += gp_excavation_cum * 3.0
    total += basement_excavation_cum * 4.0
    total += other_excavation_cum * 3.0
    total += footing_encroachment_sqm * 250.0
    
    total += fencing_masonry_m * 3.0
    total += fencing_masonry_height_over_18m_m * 4.0
    total += fencing_indigenous_m * 2.40
    
    if pavement_up_to_20_sqm:
        total += 24.0
    total += pavement_excess_sqm * 3.0
    
    total += street_occupancy_up_to_20_sqm_months * 240.0
    total += street_occupancy_excess_sqm_months * 12.0
    
    total += scaffolding_up_to_10m_months * 150.0
    total += scaffolding_excess_m_months * 12.0
    
    if sign_erection_up_to_4_sqm > 0:
        total += sign_erection_up_to_4_sqm * 120.0
    total += sign_erection_excess_sqm * 24.0
    
    inst_rates = {
        ("Business", "Neon"): 36.0, ("Advertising", "Neon"): 52.0,
        ("Business", "Illuminated"): 24.0, ("Advertising", "Illuminated"): 36.0,
        ("Business", "Others"): 15.0, ("Advertising", "Others"): 24.0,
        ("Business", "Painted-on"): 9.60, ("Advertising", "Painted-on"): 18.0
    }
    rate_inst = inst_rates.get((sign_installation_category, sign_installation_type), 15.0)
    total += sign_installation_sqm * rate_inst
    
    renewal_config = {
        ("Business", "Neon"): (36.0, 124.0), ("Advertising", "Neon"): (46.0, 200.0),
        ("Business", "Illuminated"): (18.0, 72.0), ("Advertising", "Illuminated"): (38.0, 150.0),
        ("Business", "Others"): (12.0, 40.0), ("Advertising", "Others"): (20.0, 110.0),
        ("Business", "Painted-on"): (8.0, 30.0), ("Advertising", "Painted-on"): (12.0, 100.0)
    }
    r_rate, r_min = renewal_config.get((sign_renewal_category, sign_renewal_type), (12.0, 40.0))
    calc_renewal = sign_renewal_sqm * r_rate
    total += max(calc_renewal, r_min) if sign_renewal_sqm > 0 else 0.0
    
    total += repair_vertical_sqm * 5.0
    total += repair_horizontal_sqm * 5.0
    if repair_cost > 5000.0:
        total += repair_cost * 0.01
        
    total += demolition_building_sqm * 3.0
    total += demolition_frames_m * 4.0
    if demolition_structures_up_to_10m > 0:
        total += demolition_structures_up_to_10m * (800.0 + demolition_structures_excess_m * 50.0)
    total += moving_sqm * 3.0
    
    return total
