"""
Simulated banking database for WhisPay pilot.
Stores user accounts, transactions, and related data.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from pathlib import Path
from utils.logger import log
from app.config import settings

Base = declarative_base()


class User(Base):
    """User account model."""
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    email = Column(String)
    pin_hash = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    accounts = relationship("Account", back_populates="user")
    beneficiaries = relationship("Beneficiary", back_populates="user")
    reminders = relationship("Reminder", back_populates="user")


class Account(Base):
    """Bank account model."""
    __tablename__ = 'accounts'
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))
    account_type = Column(String)  # savings, current, salary
    balance = Column(Float, default=0.0)
    currency = Column(String, default='INR')
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", foreign_keys="Transaction.from_account_id")


class Beneficiary(Base):
    """Saved beneficiary model."""
    __tablename__ = 'beneficiaries'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.id'))
    name = Column(String, nullable=False)
    account_number = Column(String)
    nickname = Column(String)
    added_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    user = relationship("User", back_populates="beneficiaries")


class Transaction(Base):
    """Transaction model."""
    __tablename__ = 'transactions'
    
    id = Column(String, primary_key=True)
    from_account_id = Column(String, ForeignKey('accounts.id'))
    to_account_id = Column(String)
    to_beneficiary_name = Column(String)
    amount = Column(Float, nullable=False)
    currency = Column(String, default='INR')
    transaction_type = Column(String)  # transfer, deposit, withdrawal
    status = Column(String, default='pending')  # pending, completed, failed
    description = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime)
    
    # Relationships
    from_account = relationship("Account", foreign_keys=[from_account_id], overlaps="transactions")


class Loan(Base):
    """Loan model."""
    __tablename__ = 'loans'
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))
    loan_type = Column(String)  # personal, home, car, education
    amount = Column(Float)
    interest_rate = Column(Float)
    tenure_months = Column(Integer)
    emi = Column(Float)
    status = Column(String)  # pending, approved, rejected, active, closed
    applied_at = Column(DateTime, default=datetime.now)
    approved_at = Column(DateTime)


class Reminder(Base):
    """Payment reminder model."""
    __tablename__ = 'reminders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.id'))
    title = Column(String, nullable=False)
    amount = Column(Float)
    beneficiary_name = Column(String)
    due_date = Column(DateTime)
    frequency = Column(String)  # once, daily, weekly, monthly
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    last_triggered = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="reminders")


class Database:
    """Database manager for WhisPay."""
    
    def __init__(self, db_url: str = None):
        """
        Initialize database connection.
        
        Args:
            db_url: Database URL (uses config if not provided)
        """
        db_url = db_url or settings.database_url
        
        # Create data directory if it doesn't exist
        if db_url.startswith('sqlite'):
            db_path = db_url.replace('sqlite:///', '')
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.engine = create_engine(db_url, echo=settings.database_echo)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Create all tables
        Base.metadata.create_all(self.engine)
        log.info("Database initialized")
    
    def get_session(self):
        """Get database session."""
        return self.SessionLocal()
    
    def create_sample_data(self):
        """Create sample data for testing (idempotent - safe to run multiple times)."""
        session = self.get_session()
        
        try:
            # Check if sample data already exists
            existing_user = session.query(User).filter_by(id="user001").first()
            if existing_user:
                log.info("Sample data already exists, skipping creation")
                return
            
            # Create sample user
            user = User(
                id="user001",
                name="Test User",
                phone="+919876543210",
                email="test@example.com",
                pin_hash="03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"  # hash of "1234"
            )
            session.add(user)
            
            # Create sample account
            account = Account(
                id="acc001",
                user_id="user001",
                account_type="savings",
                balance=50000.0
            )
            session.add(account)
            
            # Create sample beneficiaries
            beneficiaries = [
                Beneficiary(user_id="user001", name="Mom", nickname="Mom", account_number="9876543210"),
                Beneficiary(user_id="user001", name="Dad", nickname="Dad", account_number="9876543211"),
                Beneficiary(user_id="user001", name="Sister", nickname="Sis", account_number="9876543212"),
            ]
            session.add_all(beneficiaries)
            
            session.commit()
            log.info("Sample data created successfully")
            
        except Exception as e:
            session.rollback()
            log.error(f"Error creating sample data: {e}")
        finally:
            session.close()


# Global database instance
db = Database()
