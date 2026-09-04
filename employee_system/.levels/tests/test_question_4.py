from employee_system.solution import EmployeeSystem


def test_calc_salary_basic():
    hr = EmployeeSystem()
    hr.add_employee("A", "dev", 5)

    # Turno 1: [10, 30] com compensation = 5
    hr.register("A", 10)
    hr.register("A", 30)

    # Promoção para compensation = 10 em timestamp 50
    hr.promote("A", "dev", 10, 50)

    # Turno 2: [50, 80] com compensation = 10
    hr.register("A", 50)
    hr.register("A", 80)

    # Consulta [20, 60):
    # Interseção com turno 1: [20, 30) -> 10 * 5 = 50
    # Interseção com turno 2: [50, 60) -> 10 * 10 = 100
    # Total = 150
    assert hr.calc_salary("A", 20, 60) == 150


def test_calc_salary_shift_intervals_geometry():
    """
    Exhaustively tests all interval intersection geometries:
    - shift completely inside query
    - shift completely encloses query
    - partial overlap left
    - partial overlap right
    - query completely before shift
    - query completely after shift
    - boundary touching (left / right)
    - empty query interval [T, T)
    - exact matching interval
    """
    hr = EmployeeSystem()
    hr.add_employee("emp", "dev", 10)

    # Shift: [20, 80] with compensation = 10
    hr.register("emp", 20)
    hr.register("emp", 80)

    # Shift completely inside query [0, 100) -> 60 * 10 = 600
    assert hr.calc_salary("emp", 0, 100) == 600

    # Query exactly matches shift [20, 80) -> 60 * 10 = 600
    assert hr.calc_salary("emp", 20, 80) == 600

    # Shift completely encloses query [30, 60) -> 30 * 10 = 300
    assert hr.calc_salary("emp", 30, 60) == 300

    # Partial overlap on left: query [50, 100) -> [50, 80) = 30 * 10 = 300
    assert hr.calc_salary("emp", 50, 100) == 300

    # Partial overlap on right: query [0, 50) -> [20, 50) = 30 * 10 = 300
    assert hr.calc_salary("emp", 0, 50) == 300

    # Query completely before shift [0, 15) -> 0
    assert hr.calc_salary("emp", 0, 15) == 0

    # Boundary touching left [0, 20) -> 0
    assert hr.calc_salary("emp", 0, 20) == 0

    # Query completely after shift [90, 120) -> 0
    assert hr.calc_salary("emp", 90, 120) == 0

    # Boundary touching right [80, 100) -> 0
    assert hr.calc_salary("emp", 80, 100) == 0

    # Empty query interval [40, 40) -> 0
    assert hr.calc_salary("emp", 40, 40) == 0

    # Inverted query interval [60, 40) -> 0
    assert hr.calc_salary("emp", 60, 40) == 0


def test_calc_salary_multiple_shifts_and_gaps():
    hr = EmployeeSystem()
    hr.add_employee("worker", "engineer", 10)

    # Shift 1: [10, 30]
    hr.register("worker", 10)
    hr.register("worker", 30)

    # Shift 2: [50, 70]
    hr.register("worker", 50)
    hr.register("worker", 70)

    # Shift 3: [90, 120]
    hr.register("worker", 90)
    hr.register("worker", 120)

    # Query in gap between shift 1 and 2: [35, 45) -> 0
    assert hr.calc_salary("worker", 35, 45) == 0

    # Query spanning shift 1 and 2 across gap: [20, 60)
    # [20, 30) = 10 * 10 = 100
    # [50, 60) = 10 * 10 = 100
    assert hr.calc_salary("worker", 20, 60) == 200

    # Query spanning all 3 shifts: [0, 150)
    # (20 + 20 + 30) * 10 = 700
    assert hr.calc_salary("worker", 0, 150) == 700


def test_calc_salary_multiple_promotions_and_rate_changes():
    hr = EmployeeSystem()
    hr.add_employee("A", "junior", 10)

    # Shift 1: [10, 40] @ rate 10 -> 30 * 10 = 300
    hr.register("A", 10)
    hr.register("A", 40)

    # Promotion 1 to rate 20 at timestamp 50
    assert hr.promote("A", "mid", 20, 50) is True
    # Shift 2: [50, 80] @ rate 20 -> 30 * 20 = 600
    hr.register("A", 50)
    hr.register("A", 80)

    # Promotion 2 to rate 50 at timestamp 100
    assert hr.promote("A", "senior", 50, 100) is True
    # Shift 3: [100, 140] @ rate 50 -> 40 * 50 = 2000
    hr.register("A", 100)
    hr.register("A", 140)

    # Spanning all 3 shifts completely: [0, 200) -> 300 + 600 + 2000 = 2900
    assert hr.calc_salary("A", 0, 200) == 2900

    # Partial overlaps across all 3 rates: [25, 120)
    # Shift 1 [25, 40): 15 * 10 = 150
    # Shift 2 [50, 80): 30 * 20 = 600
    # Shift 3 [100, 120): 20 * 50 = 1000
    # Total = 1750
    assert hr.calc_salary("A", 25, 120) == 1750


def test_calc_salary_delayed_promotion_shift_compensation():
    """
    If employee clocks in before promotion timestamp and leaves after promotion timestamp,
    the entire shift was worked under the old compensation rate.
    The new compensation rate applies starting on the next entry from outside.
    """
    hr = EmployeeSystem()
    hr.add_employee("emp", "dev", 10)

    # Promotion to rate 30 scheduled for T=100
    assert hr.promote("emp", "dev", 30, 100) is True

    # Enters at 80 (before 100)
    hr.register("emp", 80)
    # Exits at 120 (after 100, but entered before 100 -> worked entirely at rate 10)
    hr.register("emp", 120)

    # Enters at 130 (outside -> promo activates! rate is now 30)
    hr.register("emp", 130)
    # Exits at 160 (worked at rate 30)
    hr.register("emp", 160)

    # Full period [80, 160):
    # Shift 1: 40 * 10 = 400
    # Shift 2: 30 * 30 = 900
    # Total = 1300
    assert hr.calc_salary("emp", 80, 160) == 1300

    # Partial period [100, 150):
    # Shift 1 [100, 120): 20 * 10 = 200
    # Shift 2 [130, 150): 20 * 30 = 600
    # Total = 800
    assert hr.calc_salary("emp", 100, 150) == 800


def test_calc_salary_open_shift_not_counted():
    hr = EmployeeSystem()
    hr.add_employee("emp", "dev", 10)

    # Shift 1: [10, 50] @ 10 -> 400
    hr.register("emp", 10)
    hr.register("emp", 50)

    # Open shift starts at 60 (currently inside)
    hr.register("emp", 60)

    # Open shift [60, 100) must NOT be counted
    assert hr.calc_salary("emp", 0, 100) == 400
    assert hr.calc_salary("emp", 60, 100) == 0

    # Once closed at 80, it becomes 400 + (20 * 10) = 600
    hr.register("emp", 80)
    assert hr.calc_salary("emp", 0, 100) == 600


def test_calc_salary_nonexistent_and_zero_worked():
    hr = EmployeeSystem()
    hr.add_employee("emp", "dev", 10)

    # Non-existent employee returns None
    assert hr.calc_salary("Ghost", 0, 100) is None
    assert hr.calc_salary("unknown_id", 10, 20) is None

    # Employee never worked -> returns 0
    assert hr.calc_salary("emp", 0, 100) == 0


def test_calc_salary_isolated_between_employees():
    hr = EmployeeSystem()
    hr.add_employee("A", "developer", 10)
    hr.add_employee("B", "developer", 30)

    hr.register("A", 10)
    hr.register("B", 20)
    hr.register("A", 30)
    hr.register("B", 40)

    assert hr.calc_salary("A", 0, 100) == 200
    assert hr.calc_salary("B", 0, 100) == 600


def test_duplicate_employee_does_not_overwrite_position_or_compensation():
    hr = EmployeeSystem()
    assert hr.add_employee("emp", "developer", 10) is True
    assert hr.add_employee("emp", "manager", 99) is False

    hr.register("emp", 10)
    hr.register("emp", 20)

    assert hr.top_n_employees(1, "developer") == ["emp(10)"]
    assert hr.top_n_employees(1, "manager") == []
    assert hr.calc_salary("emp", 0, 100) == 100
