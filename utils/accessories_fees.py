def compute_accessories_fees(balcony_area: float,
                             principal_rate_per_sqm: float,
                             height_above_8m_cum: float,
                             vault_volume: float,
                             pool_residential_cum: float,
                             pool_commercial_cum: float,
                             pool_institutional_cum: float,
                             pool_shower_rooms: int,
                             firewall_sqm: float,
                             towers_single_detached: int,
                             towers_comm_up_to_10m: int,
                             towers_comm_excess_m: float,
                             towers_inst_up_to_10m: int,
                             towers_inst_excess_m: float,
                             silos_up_to_10m: int,
                             silos_excess_m: float,
                             smokestack_up_to_10m: int,
                             smokestack_excess_m: float,
                             chimney_up_to_10m: int,
                             chimney_excess_m: float,
                             fixed_ovens_sqm: float,
                             industrial_kiln_cum: float,
                             tanks_abovetank_group_ab_cum: float,
                             tanks_abovetank_other_cum: float,
                             treatment_tanks_cum: float,
                             comm_tanks_above_cum: float,
                             comm_tanks_under_cum: float,
                             booths_permanent_sqm: float,
                             booths_temporary_sqm: float,
                             cemetery_tombs_sqm: float,
                             cemetery_semi_mausoleum_sqm: float,
                             cemetery_fully_mausoleum_sqm: float,
                             cemetery_multi_level_sqm: float,
                             cemetery_columbarium_sqm: float) -> float:
    total = 0.0
    total += balcony_area * (principal_rate_per_sqm * 0.50)
    total += height_above_8m_cum * 0.25
    
    if vault_volume > 0:
        if vault_volume <= 20.0:
            total += 20.0
        else:
            total += 20.0 + (vault_volume - 20.0) * 8.0
            
    total += pool_residential_cum * 3.0
    total += pool_commercial_cum * 10.0
    total += pool_institutional_cum * 6.0
    total += pool_shower_rooms * 24.0
    
    if firewall_sqm > 0:
        fw_fee = firewall_sqm * 3.0
        total += max(fw_fee, 48.0)
        
    total += towers_single_detached * 500.0
    if towers_comm_up_to_10m > 0:
        total += towers_comm_up_to_10m * (2400.0 + towers_comm_excess_m * 120.0)
    if towers_inst_up_to_10m > 0:
        total += towers_inst_up_to_10m * (1800.0 + towers_inst_excess_m * 120.0)
        
    if silos_up_to_10m > 0:
        total += silos_up_to_10m * (150.0 + silos_excess_m * 12.0)
        
    if smokestack_up_to_10m > 0:
        total += smokestack_up_to_10m * (240.0 + smokestack_excess_m * 12.0)
    if chimney_up_to_10m > 0:
        total += chimney_up_to_10m * (48.0 + chimney_excess_m * 2.0)
        
    total += fixed_ovens_sqm * 48.0
    total += industrial_kiln_cum * 12.0
    
    if tanks_abovetank_group_ab_cum > 0:
        if tanks_abovetank_group_ab_cum <= 2.0:
            total += tanks_abovetank_group_ab_cum * 12.0
        else:
            total += 2.0 * 12.0 + (tanks_abovetank_group_ab_cum - 2.0) * 12.0
            
    if tanks_abovetank_other_cum > 0:
        if tanks_abovetank_other_cum <= 10.0:
            total += 480.0
        else:
            total += 480.0 + (tanks_abovetank_other_cum - 10.0) * 24.0
            
    total += treatment_tanks_cum * 7.0
    
    if comm_tanks_above_cum > 0:
        if comm_tanks_above_cum <= 10.0:
            total += 480.0
        else:
            total += 480.0 + (comm_tanks_above_cum - 10.0) * 24.0
            
    if comm_tanks_under_cum > 0:
        if comm_tanks_under_cum <= 20.0:
            total += 540.0
        else:
            total += 540.0 + (comm_tanks_under_cum - 20.0) * 24.0
            
    total += booths_permanent_sqm * 10.0
    total += booths_temporary_sqm * 5.0
    
    total += cemetery_tombs_sqm * 5.0
    total += cemetery_semi_mausoleum_sqm * 5.0
    total += cemetery_fully_mausoleum_sqm * 12.0
    total += cemetery_multi_level_sqm * 5.0
    total += cemetery_columbarium_sqm * 18.0
    
    return total
