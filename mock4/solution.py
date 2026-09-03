class EmployeeSystem:
    def __init__(self):
        pass

    # Level 1
    def add_employee(self, employee_id: str, position: str, compensation: int) -> bool:
        raise NotImplementedError("Level 1: add_employee não implementado")

    def register(self, employee_id: str, timestamp: int) -> str:
        raise NotImplementedError("Level 1: register não implementado")

    def get_worked_time(self, employee_id: str) -> int | None:
        raise NotImplementedError("Level 1: get_worked_time não implementado")

    # Level 2
    def top_n_employees(self, n: int, position: str) -> list[str]:
        raise NotImplementedError("Level 2: top_n_employees não implementado")

    # Level 3
    def promote(
        self,
        employee_id: str,
        new_position: str,
        new_compensation: int,
        start_timestamp: int,
    ) -> bool:
        raise NotImplementedError("Level 3: promote não implementado")

    # Level 4
    def calc_salary(
        self, employee_id: str, start_timestamp: int, end_timestamp: int
    ) -> int | None:
        raise NotImplementedError("Level 4: calc_salary não implementado")
