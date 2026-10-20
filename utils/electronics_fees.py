def compute_electronics_fees(ports: int,
                             locations_broadcast: int,
                             atms_vending_medical: int,
                             outlets: int,
                             terminations: int,
                             studios_theaters: int,
                             antenna_towers: int,
                             signages: int,
                             poles: int,
                             attachments: int,
                             other_devices: int) -> float:
    total = 0.0
    total += ports * 2.40
    total += locations_broadcast * 1000.0
    total += atms_vending_medical * 10.0
    total += outlets * 2.40
    total += terminations * 2.40
    total += studios_theaters * 1000.0
    total += antenna_towers * 1000.0
    total += signages * 50.0
    total += poles * 20.0
    total += attachments * 20.0
    total += other_devices * 50.0
    return total
