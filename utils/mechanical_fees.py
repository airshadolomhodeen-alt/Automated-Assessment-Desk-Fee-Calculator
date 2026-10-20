def compute_mechanical_fees(ref_cold_storage_tons: float,
                            ice_plants_tons: float,
                            ac_up_to_100_tons: float,
                            ac_above_100_tons: float,
                            window_ac_units: int,
                            ventilation_kw: float,
                            escalators_meters: float,
                            elevators_dumbwaiter: int,
                            elevators_construction: int,
                            elevators_passenger: int,
                            elevators_freight: int,
                            elevators_car: int,
                            boiler_kw: float,
                            pressure_water_heaters: int,
                            pumps_kw: float,
                            sprinkler_heads: int,
                            gen_kw: float,
                            gases_outlets: int,
                            gas_meters: int,
                            power_piping_meters: float,
                            other_ice_kw: float,
                            pressure_vessels_cum: float,
                            other_machinery_kw: float,
                            ducts_conveyors_meters: float,
                            weighing_scale_tons: float) -> float:
    total = 0.0
    total += ref_cold_storage_tons * 40.0
    total += ice_plants_tons * 60.0
    total += ac_up_to_100_tons * 90.0
    total += ac_above_100_tons * 40.0
    total += window_ac_units * 60.0
    total += ventilation_kw * 40.0
    
    if escalators_meters > 0:
        if escalators_meters <= 20:
            total += 20.0
        else:
            total += 20.0 + (escalators_meters - 20.0) * 10.0
            
    total += elevators_dumbwaiter * 600.0
    total += elevators_construction * 2000.0
    total += elevators_passenger * 5000.0
    total += elevators_freight * 5000.0
    total += elevators_car * 5000.0
    
    if boiler_kw > 0:
        if boiler_kw <= 7.5:
            b_fee = 500.0
        elif boiler_kw <= 22:
            b_fee = 700.0
        elif boiler_kw <= 37:
            b_fee = 900.0
        elif boiler_kw <= 52:
            b_fee = 1200.0
        elif boiler_kw <= 67:
            b_fee = 1400.0
        elif boiler_kw <= 74:
            b_fee = 1600.0
        else:
            b_fee = 1600.0 + (boiler_kw - 74.0) * 5.0
        total += b_fee
        
    total += pressure_water_heaters * 200.0
    total += pumps_kw * 60.0
    total += sprinkler_heads * 4.0
    
    if gen_kw > 0:
        if gen_kw <= 50:
            total += gen_kw * 25.0
        elif gen_kw <= 100:
            total += 50.0 * 25.0 + (gen_kw - 50.0) * 20.0
        else:
            total += 50.0 * 25.0 + 50.0 * 20.0 + (gen_kw - 100.0) * 3.0
            
    total += gases_outlets * 20.0
    total += gas_meters * 100.0
    total += power_piping_meters * 4.0
    
    if other_ice_kw > 0:
        if other_ice_kw <= 50:
            total += other_ice_kw * 10.0
        elif other_ice_kw <= 100:
            total += 50.0 * 10.0 + (other_ice_kw - 50.0) * 12.0
        else:
            total += 50.0 * 10.0 + 50.0 * 12.0 + (other_ice_kw - 100.0) * 3.0
            
    total += pressure_vessels_cum * 60.0
    total += other_machinery_kw * 60.0
    total += ducts_conveyors_meters * 10.0
    total += weighing_scale_tons * 50.0
    
    return total
