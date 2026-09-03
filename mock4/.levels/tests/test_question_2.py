from mock4.solution import EmployeeSystem


def test_top_n_employees_basic_ranking_and_formatting():
    hr = EmployeeSystem()
    hr.add_employee("A", "developer", 100)
    hr.add_employee("B", "developer", 100)
    hr.add_employee("C", "manager", 200)

    # A works 50
    hr.register("A", 10)
    hr.register("A", 60)

    # B works 80
    hr.register("B", 100)
    hr.register("B", 180)

    # C works 300
    hr.register("C", 10)
    hr.register("C", 310)

    # Developer ranking: B (80) > A (50)
    assert hr.top_n_employees(2, "developer") == [
        "B(80)",
        "A(50)",
    ]

    # Manager ranking: C (300)
    assert hr.top_n_employees(1, "manager") == [
        "C(300)",
    ]


def test_top_n_employees_tie_breaking_order():
    hr = EmployeeSystem()
    hr.add_employee("dev_c", "developer", 100)
    hr.add_employee("dev_a", "developer", 100)
    hr.add_employee("dev_b", "developer", 100)

    # All work exactly 50 hours
    hr.register("dev_c", 0)
    hr.register("dev_c", 50)
    hr.register("dev_a", 0)
    hr.register("dev_a", 50)
    hr.register("dev_b", 0)
    hr.register("dev_b", 50)

    # Tie breaker: employee_id ASC
    assert hr.top_n_employees(3, "developer") == [
        "dev_a(50)",
        "dev_b(50)",
        "dev_c(50)",
    ]


def test_top_n_employees_includes_zero_worked_time():
    hr = EmployeeSystem()
    hr.add_employee("dev2", "developer", 100)
    hr.add_employee("dev1", "developer", 100)
    hr.add_employee("dev3", "developer", 100)

    # dev3 works 20 hours, dev1 and dev2 have 0 hours worked
    hr.register("dev3", 0)
    hr.register("dev3", 20)

    assert hr.top_n_employees(3, "developer") == [
        "dev3(20)",
        "dev1(0)",
        "dev2(0)",
    ]


def test_top_n_employees_unfinished_shift_not_counted():
    hr = EmployeeSystem()
    hr.add_employee("dev1", "developer", 100)
    hr.add_employee("dev2", "developer", 100)

    # dev1 completes a 30 hr shift
    hr.register("dev1", 10)
    hr.register("dev1", 40)

    # dev2 is currently inside on a 1000 hr shift (not completed)
    hr.register("dev2", 0)

    # dev2's unfinished shift counts as 0
    assert hr.top_n_employees(2, "developer") == [
        "dev1(30)",
        "dev2(0)",
    ]


def test_top_n_employees_n_limits_and_edge_cases():
    hr = EmployeeSystem()
    hr.add_employee("dev1", "developer", 100)
    hr.add_employee("dev2", "developer", 100)
    hr.add_employee("dev3", "developer", 100)

    hr.register("dev1", 0)
    hr.register("dev1", 10)
    hr.register("dev2", 0)
    hr.register("dev2", 20)
    hr.register("dev3", 0)
    hr.register("dev3", 30)

    # n is smaller than count
    assert hr.top_n_employees(1, "developer") == ["dev3(30)"]
    assert hr.top_n_employees(2, "developer") == ["dev3(30)", "dev2(20)"]

    # n is larger than total employees with that position
    assert hr.top_n_employees(10, "developer") == [
        "dev3(30)",
        "dev2(20)",
        "dev1(10)",
    ]

    # n == 0 returns empty list
    assert hr.top_n_employees(0, "developer") == []


def test_top_n_employees_position_with_no_employees():
    hr = EmployeeSystem()
    hr.add_employee("dev1", "developer", 100)

    # Unknown or empty position returns empty list
    assert hr.top_n_employees(5, "designer") == []
    assert hr.top_n_employees(5, "nonexistent") == []


def test_top_n_employees_multi_tier_tie_breaking():
    hr = EmployeeSystem()
    # 2 with 100h, 2 with 50h, 2 with 0h
    hr.add_employee("b_100", "qa", 50)
    hr.add_employee("a_100", "qa", 50)
    hr.add_employee("d_50", "qa", 50)
    hr.add_employee("c_50", "qa", 50)
    hr.add_employee("f_0", "qa", 50)
    hr.add_employee("e_0", "qa", 50)

    hr.register("b_100", 0)
    hr.register("b_100", 100)
    hr.register("a_100", 0)
    hr.register("a_100", 100)
    hr.register("d_50", 0)
    hr.register("d_50", 50)
    hr.register("c_50", 0)
    hr.register("c_50", 50)

    assert hr.top_n_employees(6, "qa") == [
        "a_100(100)",
        "b_100(100)",
        "c_50(50)",
        "d_50(50)",
        "e_0(0)",
        "f_0(0)",
    ]
