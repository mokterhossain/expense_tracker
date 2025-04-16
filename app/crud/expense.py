from sqlalchemy import select
from app.schemas.expense import ExpenseCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.expense import Expense

async def create_user_expense(db: AsyncSession, expense: ExpenseCreate, user_id: int):
    db_expense = Expense(**expense.dict(), user_id=user_id)
    db.add(db_expense)
    await db.commit()
    await db.refresh(db_expense)
    return db_expense

async def get_user_expenses(db: AsyncSession, user_id: int):
    stmt = select(Expense).where(Expense.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().all()