from pydantic import BaseModel


class GroupedSalarySchema(BaseModel):
    id: int
    name: str
    from_date: str
    to_date: str
    empl_count: int
    is_approved: bool
    salaries_amount: float
    group_id: int
    advances: float
    bonuses: float
    fines: float
    final_salary: float


class GroupedSalaryListSchema(BaseModel):
    results: list[GroupedSalarySchema]


class SalaryEmployeeSchema(BaseModel):
    id: int
    employee_id: int
    full_name: str
    salary: float
    advances: float
    bonuses: float
    fines: float
    final_salary: float


class SalaryEmployeeListSchema(BaseModel):
    results: list[SalaryEmployeeSchema]
