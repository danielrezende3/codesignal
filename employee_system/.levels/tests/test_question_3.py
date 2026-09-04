from employee_system.solution import EmployeeSystem


def test_promote_basic_lifecycle():
    hr = EmployeeSystem()
    hr.add_employee("A", "junior", 100)

    # Promoção agendada para timestamp >= 100
    assert hr.promote("A", "senior", 200, 100) is True
    # Não pode ter duas promoções pendentes ao mesmo tempo
    assert hr.promote("A", "lead", 300, 150) is False

    # Turnos antes de 100 (posição continua junior)
    hr.register("A", 80)
    hr.register("A", 90)  # +10 junior
    assert hr.top_n_employees(1, "junior") == ["A(10)"]
    assert hr.top_n_employees(1, "senior") == []

    # Primeiro registro em ou depois de 100 com funcionário fora do escritório
    hr.register("A", 110)  # Ativa promoção -> vira senior e entra no escritório
    hr.register("A", 150)  # Sai -> +40 como senior

    # Agora A é senior; as 10 horas de junior não entram no ranking de senior
    assert hr.top_n_employees(1, "senior") == ["A(40)"]
    assert hr.top_n_employees(1, "junior") == []
    assert hr.get_worked_time("A") == 50


def test_promote_nonexistent_employee():
    hr = EmployeeSystem()
    assert hr.promote("missing", "lead", 500, 10) is False


def test_promote_delayed_activation_when_inside_office_at_promotion_timestamp():
    """
    Subtle CodeSignal trap:
    If employee enters BEFORE start_timestamp and exits AT OR AFTER start_timestamp,
    the exit does NOT activate the promotion because the employee was inside before registering.
    The promotion only activates on the FIRST entry from outside at or after start_timestamp.
    """
    hr = EmployeeSystem()
    hr.add_employee("emp1", "junior", 50)

    # Schedule promotion for T=100
    assert hr.promote("emp1", "senior", 100, 100) is True

    # Clock in at 80 (outside -> inside) before T=100
    hr.register("emp1", 80)

    # Clock out at 120 (inside -> outside) after T=100.
    # Was inside before registering -> does NOT activate promotion!
    hr.register("emp1", 120)

    # Position is STILL junior after exiting at 120
    assert hr.top_n_employees(1, "junior") == ["emp1(40)"]
    assert hr.top_n_employees(1, "senior") == []

    # Promotion is STILL pending (cannot schedule another pending promotion yet)
    assert hr.promote("emp1", "lead", 200, 150) is False

    # Next register from outside at 130 (130 >= 100) -> ACTIVATES promotion!
    hr.register("emp1", 130)  # Now senior
    hr.register("emp1", 170)  # +40 senior

    # Only the 40 hours worked as senior count in the senior ranking
    assert hr.top_n_employees(1, "senior") == ["emp1(40)"]
    assert hr.top_n_employees(1, "junior") == []


def test_promote_exact_timestamp_boundary():
    hr = EmployeeSystem()
    hr.add_employee("emp", "intern", 20)

    assert hr.promote("emp", "junior", 40, 100) is True

    # Employee is outside and registers at exactly timestamp 100 -> activates immediately
    hr.register("emp", 100)
    hr.register("emp", 150)

    assert hr.top_n_employees(1, "junior") == ["emp(50)"]
    assert hr.top_n_employees(1, "intern") == []


def test_promotion_activates_immediately_on_qualifying_entry():
    hr = EmployeeSystem()
    hr.add_employee("emp", "junior", 20)

    assert hr.promote("emp", "senior", 40, 100) is True
    assert hr.register("emp", 100) == "registered"

    # The position changes on entry, even while the new shift is still open.
    assert hr.top_n_employees(1, "junior") == []
    assert hr.top_n_employees(1, "senior") == ["emp(0)"]

    # Activation also clears the pending promotion immediately.
    assert hr.promote("emp", "lead", 80, 200) is True


def test_pending_promotions_are_independent_per_employee():
    hr = EmployeeSystem()
    hr.add_employee("A", "junior", 20)
    hr.add_employee("B", "analyst", 30)

    assert hr.promote("A", "senior", 40, 100) is True
    assert hr.promote("B", "manager", 60, 100) is True

    hr.register("A", 100)
    hr.register("B", 110)
    hr.register("A", 120)
    hr.register("B", 130)

    assert hr.top_n_employees(1, "senior") == ["A(20)"]
    assert hr.top_n_employees(1, "manager") == ["B(20)"]
    assert hr.top_n_employees(1, "junior") == []
    assert hr.top_n_employees(1, "analyst") == []


def test_subsequent_promotions_after_activation():
    hr = EmployeeSystem()
    hr.add_employee("dev", "junior", 50)

    # 1st promotion scheduled for 50
    assert hr.promote("dev", "mid", 80, 50) is True

    # Cannot schedule 2nd while 1st is pending
    assert hr.promote("dev", "senior", 120, 100) is False

    # Activate 1st promotion at 50
    hr.register("dev", 50)
    hr.register("dev", 70)  # 20 hours as mid

    # Now 1st promotion is active, no pending promotion remains.
    # We can now schedule a 2nd promotion!
    assert hr.promote("dev", "senior", 120, 100) is True

    # Activate 2nd promotion at 100
    hr.register("dev", 100)
    hr.register("dev", 140)  # 40 hours as senior

    assert hr.top_n_employees(1, "senior") == ["dev(40)"]
    assert hr.top_n_employees(1, "mid") == []
    assert hr.top_n_employees(1, "junior") == []


def test_top_n_employees_with_promoted_peers_and_current_position_hours():
    hr = EmployeeSystem()
    hr.add_employee("dev1", "developer", 100)
    hr.add_employee("dev2", "developer", 100)
    hr.add_employee("qa1", "qa", 80)

    # dev1 works 50 hours
    hr.register("dev1", 0)
    hr.register("dev1", 50)

    # dev2 works 30 hours
    hr.register("dev2", 0)
    hr.register("dev2", 30)

    # qa1 works 40 hours as qa
    hr.register("qa1", 0)
    hr.register("qa1", 40)
    assert hr.top_n_employees(1, "qa") == ["qa1(40)"]

    # Promote qa1 to developer at 100
    assert hr.promote("qa1", "developer", 120, 100) is True
    hr.register("qa1", 100)
    hr.register("qa1", 130)  # +30 as developer

    # qa1 is no longer listed in qa
    assert hr.top_n_employees(1, "qa") == []

    # Only time worked as developer is ranked. dev2 wins the 30-hour ID tie.
    assert hr.top_n_employees(3, "developer") == [
        "dev1(50)",
        "dev2(30)",
        "qa1(30)",
    ]
