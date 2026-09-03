from mock4.solution import EmployeeSystem


def test_add_employee_success_and_duplicates():
    hr = EmployeeSystem()
    assert hr.add_employee("A", "developer", 100) is True
    assert hr.add_employee("B", "manager", 200) is True

    # Duplicate employee_id must return False
    assert hr.add_employee("A", "developer", 100) is False
    assert hr.add_employee("A", "lead", 300) is False

    # Check that A still exists and operates under initial state
    assert hr.get_worked_time("A") == 0


def test_register_toggle_single_shift():
    hr = EmployeeSystem()
    assert hr.add_employee("A", "developer", 100) is True

    # Initial state: 0 hours worked
    assert hr.get_worked_time("A") == 0

    # Clock in: outside -> inside
    assert hr.register("A", 10) == "registered"
    # Unfinished shift must NOT count towards worked_time
    assert hr.get_worked_time("A") == 0

    # Clock out: inside -> outside
    assert hr.register("A", 50) == "registered"
    # Shift finished: 50 - 10 = 40
    assert hr.get_worked_time("A") == 40


def test_register_multiple_shifts_and_toggle_sequence():
    hr = EmployeeSystem()
    hr.add_employee("emp1", "qa", 50)

    # Shift 1: [10, 20] -> +10 (Total = 10)
    assert hr.register("emp1", 10) == "registered"
    assert hr.register("emp1", 20) == "registered"
    assert hr.get_worked_time("emp1") == 10

    # Shift 2: [30, 50] -> +20 (Total = 30)
    assert hr.register("emp1", 30) == "registered"
    assert hr.get_worked_time("emp1") == 10  # Open shift not counted
    assert hr.register("emp1", 50) == "registered"
    assert hr.get_worked_time("emp1") == 30

    # Shift 3: [100, 150] -> +50 (Total = 80)
    assert hr.register("emp1", 100) == "registered"
    assert hr.get_worked_time("emp1") == 30  # Open shift not counted
    assert hr.register("emp1", 150) == "registered"
    assert hr.get_worked_time("emp1") == 80


def test_get_worked_time_nonexistent_and_zero_shifts():
    hr = EmployeeSystem()
    hr.add_employee("emp1", "qa", 50)

    # Non-existent employee returns None
    assert hr.get_worked_time("missing_emp") is None
    assert hr.get_worked_time("Ghost") is None

    # Employee added but never registered has worked_time 0
    assert hr.get_worked_time("emp1") == 0


def test_zero_duration_shift():
    hr = EmployeeSystem()
    hr.add_employee("emp_instant", "dev", 100)

    # Enters and exits at the exact same timestamp
    assert hr.register("emp_instant", 10) == "registered"
    assert hr.register("emp_instant", 10) == "registered"
    assert hr.get_worked_time("emp_instant") == 0


def test_multiple_independent_employees_interleaved():
    hr = EmployeeSystem()
    hr.add_employee("alice", "dev", 100)
    hr.add_employee("bob", "qa", 80)

    # Alice enters at 10
    assert hr.register("alice", 10) == "registered"
    # Bob enters at 15
    assert hr.register("bob", 15) == "registered"
    # Alice exits at 30 (Alice: 20 hrs)
    assert hr.register("alice", 30) == "registered"
    # Bob exits at 45 (Bob: 30 hrs)
    assert hr.register("bob", 45) == "registered"

    assert hr.get_worked_time("alice") == 20
    assert hr.get_worked_time("bob") == 30


def test_consecutive_back_to_back_shifts():
    hr = EmployeeSystem()
    hr.add_employee("emp", "dev", 100)

    # Shift 1: [10, 40]
    assert hr.register("emp", 10) == "registered"
    assert hr.register("emp", 40) == "registered"
    # Shift 2: [40, 80] immediately after
    assert hr.register("emp", 40) == "registered"
    assert hr.register("emp", 80) == "registered"

    assert hr.get_worked_time("emp") == 70
