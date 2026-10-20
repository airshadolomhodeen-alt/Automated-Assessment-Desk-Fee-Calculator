def compute_plumbing_fees(standard_units: int,
                          excess_water_closets: int,
                          excess_floor_drains: int,
                          excess_sinks: int,
                          excess_lavatories: int,
                          excess_faucets: int,
                          excess_shower_heads: int,
                          special_fixtures_dict: dict,
                          water_meters_12_25mm: int,
                          water_meters_above_25mm: int,
                          septic_tank_cum: float) -> float:
    total = standard_units * 24.00
    
    total += excess_water_closets * 7.00
    total += excess_floor_drains * 3.00
    total += excess_sinks * 3.00
    total += excess_lavatories * 7.00
    total += excess_faucets * 2.00
    total += excess_shower_heads * 2.00
    
    rates = {
        "slop_sink": 7.0,
        "urinal": 4.0,
        "bath_tub": 7.0,
        "grease_trap": 7.0,
        "garage_trap": 7.0,
        "bidet": 4.0,
        "dental_cuspidor": 4.0,
        "gas_water_heater": 4.0,
        "drinking_fountain": 2.0,
        "bar_sink": 4.0,
        "laundry_sink": 4.0,
        "lab_sink": 4.0,
        "fixed_sterilizer": 2.0
    }
    
    for k, count in special_fixtures_dict.items():
        if k in rates:
            total += count * rates[k]
            
    total += water_meters_12_25mm * 8.00
    total += water_meters_above_25mm * 10.00
    
    if septic_tank_cum > 0:
        if septic_tank_cum <= 5.0:
            total += 24.00
        else:
            total += 24.00 + (septic_tank_cum - 5.0) * 7.00
            
    return total
