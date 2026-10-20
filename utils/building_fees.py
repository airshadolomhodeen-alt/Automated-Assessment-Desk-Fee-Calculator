def get_fixed_cost_per_sqm(group: str) -> float:
    """Returns fixed cost of construction per square meter based on Table II.G.1."""
    group_upper = group.upper()
    if group_upper == "GROUP F":
        return 8000.0
    elif group_upper.startswith("GROUP J"):
        return 6000.0
    else:
        return 10000.0

def compute_cumulative_fee(area: float, brackets: list) -> float:
    """Computes cumulative building fee based on bracket limits and rates."""
    total_fee = 0.0
    remaining = area
    prev_limit = 0.0
    for limit, rate in brackets:
        if remaining <= 0:
            break
        bracket_size = limit - prev_limit
        if remaining >= bracket_size:
            total_fee += bracket_size * rate
            remaining -= bracket_size
        else:
            total_fee += remaining * rate
            remaining = 0.0
        prev_limit = limit
    return total_fee

def compute_building_fee(division: str, area: float, is_original: bool = True) -> float:
    """Computes principal building permit fees for Divisions A through J."""
    div = division.upper()
    if div == "A-1":
        if area <= 20.0:
            rate = 2.00 if is_original else 2.40
            return area * rate
        elif area <= 50.0:
            return area * 3.40
        elif area <= 100.0:
            return area * 4.80
        elif area <= 150.0:
            return area * 6.00
        else:
            return area * 7.20
    elif div == "A-2":
        if area <= 20.0:
            rate = 3.00 if is_original else 3.40
            return area * rate
        elif area <= 50.0:
            return area * 5.20
        elif area <= 100.0:
            return area * 8.00
        elif area <= 150.0:
            return area * 8.00
        else:
            return area * 8.40
    elif div in ["B-1", "C-1", "E-1", "E-2", "E-3", "F-1", "G-1", "G-2", "G-3", "G-4", "G-5", "H-1", "H-2", "H-3", "H-4", "I-1", "J-1", "J-2", "J-3"]:
        brackets = [
            (5000, 23.00), (6000, 22.00), (7000, 20.50), (8000, 19.50),
            (9000, 18.00), (10000, 17.00), (15000, 16.00), (20000, 15.00),
            (30000, 14.00), (float('inf'), 12.00)
        ]
        fee = compute_cumulative_fee(area, brackets)
        if div == "J-2":
            fee *= 0.50
        return fee
    elif div in ["C-2", "D-1", "D-2", "D-3"]:
        brackets = [
            (5000, 12.00), (6000, 11.00), (7000, 10.20), (8000, 9.60),
            (9000, 9.00), (10000, 8.40), (15000, 7.20), (20000, 6.60),
            (30000, 6.00), (float('inf'), 5.00)
        ]
        return compute_cumulative_fee(area, brackets)
    else:
        brackets = [(float('inf'), 15.00)]
        return compute_cumulative_fee(area, brackets)
