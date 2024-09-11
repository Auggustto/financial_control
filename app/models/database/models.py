from sqlalchemy import Integer, String, Column, DateTime, Boolean, ForeignKey, func, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.database.base import Base
from collections import Counter

def format_datetime(value):
    if value:
        return value.strftime("%d/%m/%Y %H:%M:%S")
    return None

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False)
    email = Column(String(30), unique=True, nullable=False, index=True) 
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True)

    accounts = relationship("Accounts", back_populates="user")
    transactions = relationship("Transactions", back_populates="user")
    budgets = relationship("Budgets", back_populates="user")
    notifications = relationship("Notifications", back_populates="user")

    def as_dict(self):
        status_count = Counter(task.status for task in self.tasks)

        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
            "tasks": [task.as_dict() for task in self.tasks],
            "accounts": [account.as_dict() for account in self.accounts],
            "status_count": dict(status_count)
        }

class Accounts(Base):
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    name = Column(String(100), nullable=False)
    balance = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transactions", back_populates="account")

    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "balance": self.balance,
            "created_at": format_datetime(self.created_at),
            "updated_at": format_datetime(self.updated_at),
        }

class CategoryType(Enum):
    EXPENSE = 1
    INCOME = 2

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    category = Column(String(50), unique=True)
    type = Column(Enum(CategoryType), nullable=False)

    transactions = relationship("Transactions", back_populates="category")
    budgets = relationship("Budgets", back_populates="category")

    def as_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "type": self.type.name
        }

class TransactionType(Enum):
    EXPENSE = 1
    INCOME = 2

class Transactions(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    amount = Column(Float, nullable=False, default=0.0)
    description = Column(String, unique=False)
    transaction_date = Column(DateTime, nullable=False, default=func.now(), index=True)
    type = Column(Enum(TransactionType), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="transactions")
    account = relationship("Accounts", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "account_id": self.account_id,
            "category_id": self.category_id,
            "amount": self.amount,
            "description": self.description,
            "transaction_date": format_datetime(self.transaction_date),
            "type": self.type.name,
            "created_at": format_datetime(self.created_at),
            "updated_at": format_datetime(self.updated_at),
        }

class Budgets(Base):
    __tablename__ = 'budgets'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    amount = Column(Float, nullable=False, default=0.0)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="budgets")

    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "amount": self.amount,
            "start_date": format_datetime(self.start_date),
            "end_date": format_datetime(self.end_date),
            "created_at": format_datetime(self.created_at),
            "updated_at": format_datetime(self.updated_at),
        }

class Notifications(Base):
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    message = Column(String(200), nullable=False)
    read = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    
    user = relationship("User", back_populates="notifications")

    def as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "message": self.message,
            "read": self.read,
            "created_at": format_datetime(self.created_at),
        }
