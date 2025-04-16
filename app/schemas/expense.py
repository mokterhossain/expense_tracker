from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class ExpenseCategory(str, Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    HOUSING = "Housing"
    ENTERTAINMENT = "Entertainment"
    OTHER = "Other"

class ExpenseBase(BaseModel):
    amount: float
    category: ExpenseCategory
    description: str

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int
    date: datetime
    user_id: int

    class Config:
        orm_mode = True