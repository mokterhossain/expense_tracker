from app.models.user import User
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.expense import ExpenseCreate, Expense
from app.crud.expense import create_user_expense, get_user_expenses
from app.database import get_db
from app.auth.security import get_current_user

router = APIRouter()

@router.post("/", response_model=Expense)
async def create_expense(
    expense: ExpenseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_user_expense(db=db, expense=expense, user_id=current_user.id)

@router.get("/", response_model=list[Expense])
async def read_expenses(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expenses = await get_user_expenses(db, user_id=current_user.id)
    return expenses