import math

def compute_occupancy_certificate_fee(division: str, valuation: float, area: float = 0.0) -> float:
    div = division.upper()
    if div in ["A-1", "A-2"]:
        if valuation <= 150000.0:
            return 100.0
        elif valuation <= 400000.0:
            return 200.0
        elif valuation <= 850000.0:
            return 400.0
        elif valuation <= 1200000.0:
            return 800.0
        else:
            excess_millions = (valuation - 1200000.0) / 1000000.0
            return 800.0 + math.ceil(excess_millions) * 800.0
    elif div in ["B-1", "E-1", "E-2", "E-3", "F-1", "G-1", "G-2", "G-3", "G-4", "G-5", "H-1", "H-2", "H-3", "H-4", "I-1"]:
        if valuation <= 150000.0:
            return 200.0
        elif valuation <= 400000.0:
            return 400.0
        elif valuation <= 850000.0:
            return 800.0
        elif valuation <= 1200000.0:
            return 1000.0
        else:
            excess_millions = (valuation - 1200000.0) / 1000000.0
            return 1000.0 + math.ceil(excess_millions) * 1000.0
    elif div in ["C-1", "C-2", "D-1", "D-2", "D-3"]:
        if valuation <= 150000.0:
            return 150.0
        elif valuation <= 400000.0:
            return 250.0
        elif valuation <= 850000.0:
            return 600.0
        elif valuation <= 1200000.0:
            return 900.0
        else:
            excess_millions = (valuation - 1200000.0) / 1000000.0
            return 900.0 + math.ceil(excess_millions) * 900.0
    elif div.startswith("J-1"):
        if area <= 20.0:
            return 50.0
        elif area <= 500.0:
            return 240.0
        elif area <= 1000.0:
            return 360.0
        elif area <= 5000.0:
            return 480.0
        elif area <= 10000.0:
            return 1200.0
        else:
            return 2400.0
    elif div.startswith("J-2"):
        return 800.0
    return 200.0

def compute_annual_inspection_fees(area: float, plumbing_units: int, electrical_permit_fee: float) -> float:
    bldg_insp = 0.0
    if area <= 100.0:
        bldg_insp = 120.0
    elif area <= 200.0:
        bldg_insp = 240.0
    elif area <= 350.0:
        bldg_insp = 480.0
    elif area <= 500.0:
        bldg_insp = 720.0
    elif area <= 750.0:
        bldg_insp = 960.0
    elif area <= 1000.0:
        bldg_insp = 1200.0
    else:
        excess_thousands = (area - 1000.0) / 1000.0
        bldg_insp = 1200.0 + math.ceil(excess_thousands) * 1200.0
        
    plumbing_insp = plumbing_units * 60.0
    electrical_insp = electrical_permit_fee
    
    return bldg_insp + plumbing_insp + electrical_insp
