def compute_connected_load_fee(kva: float) -> float:
    if kva <= 5.0:
        return 200.0
    elif kva <= 50.0:
        return 200.0 + (kva - 5.0) * 20.0
    elif kva <= 300.0:
        return 1100.0 + (kva - 50.0) * 10.0
    elif kva <= 1500.0:
        return 3600.0 + (kva - 300.0) * 5.0
    elif kva <= 6000.0:
        return 9600.0 + (kva - 1500.0) * 2.50
    else:
        return 20850.0 + (kva - 6000.0) * 1.25

def compute_transformer_generator_fee(kva: float) -> float:
    if kva <= 5.0:
        return 40.0
    elif kva <= 50.0:
        return 40.0 + (kva - 5.0) * 4.0
    elif kva <= 300.0:
        return 220.0 + (kva - 50.0) * 2.0
    elif kva <= 1500.0:
        return 720.0 + (kva - 300.0) * 1.0
    elif kva <= 6000.0:
        return 1920.0 + (kva - 1500.0) * 0.50
    else:
        return 4170.0 + (kva - 6000.0) * 0.25

def compute_electrical_fees(connected_load_kva: float,
                            trans_gen_kva: float,
                            poles: int,
                            guys: int,
                            occupancy_type: str,
                            num_meters: int,
                            num_wiring_permits: int) -> float:
    fee_load = compute_connected_load_fee(connected_load_kva)
    fee_trans = compute_transformer_generator_fee(trans_gen_kva)
    fee_poles = poles * 30.0
    fee_guys = guys * 30.0
    
    occ = occupancy_type.lower()
    if "commercial" in occ or "industrial" in occ:
        meter_fee_per_unit = 60.0
        permit_fee_per_unit = 36.0
    elif "institutional" in occ:
        meter_fee_per_unit = 30.0
        permit_fee_per_unit = 12.0
    else:
        meter_fee_per_unit = 15.0
        permit_fee_per_unit = 15.0
        
    fee_meters = num_meters * meter_fee_per_unit
    fee_permits = num_wiring_permits * permit_fee_per_unit
    
    return fee_load + fee_trans + fee_poles + fee_guys + fee_meters + fee_permits
