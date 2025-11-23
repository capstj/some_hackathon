"""
Banking operations module for WhisPay.
Handles all banking transactions and account operations.
"""

from typing import Optional, Dict, List, Tuple
from datetime import datetime, timedelta
import secrets
from banking.database import db, User, Account, Transaction, Beneficiary, Loan, Reminder
from utils.logger import log
from utils.helpers import format_currency
from app.config import settings


class BankingOperations:
    """Handles banking operations."""
    
    def __init__(self):
        """Initialize banking operations."""
        self.db = db
        log.info("Banking operations initialized")
    
    def get_user(self, user_id: str) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User identifier
            
        Returns:
            User object or None
        """
        session = self.db.get_session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            return user
        finally:
            session.close()
    
    def get_account(self, account_id: str) -> Optional[Account]:
        """
        Get account by ID.
        
        Args:
            account_id: Account identifier
            
        Returns:
            Account object or None
        """
        session = self.db.get_session()
        try:
            account = session.query(Account).filter_by(id=account_id).first()
            return account
        finally:
            session.close()
    
    def get_user_primary_account(self, user_id: str) -> Optional[Account]:
        """
        Get user's primary account.
        
        Args:
            user_id: User identifier
            
        Returns:
            Account object or None
        """
        session = self.db.get_session()
        try:
            account = session.query(Account).filter_by(
                user_id=user_id,
                is_active=True
            ).first()
            return account
        finally:
            session.close()
    
    def check_balance(self, user_id: str, account_type: Optional[str] = None) -> Dict:
        """
        Check account balance.
        
        Args:
            user_id: User identifier
            account_type: Specific account type or None for primary
            
        Returns:
            Dictionary with balance information
        """
        session = self.db.get_session()
        try:
            if account_type:
                account = session.query(Account).filter_by(
                    user_id=user_id,
                    account_type=account_type,
                    is_active=True
                ).first()
            else:
                account = self.get_user_primary_account(user_id)
            
            if not account:
                log.warning(f"No account found for user {user_id}")
                return {
                    'success': False,
                    'error': 'Account not found'
                }
            
            result = {
                'success': True,
                'account_id': account.id,
                'account_type': account.account_type,
                'balance': account.balance,
                'currency': account.currency,
                'formatted_balance': format_currency(account.balance, '₹')
            }
            
            log.info(f"Balance check for user {user_id}: {result['formatted_balance']}")
            return result
            
        except Exception as e:
            log.error(f"Error checking balance: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            session.close()
    
    def transfer_money(
        self,
        user_id: str,
        recipient: str,
        amount: float,
        description: Optional[str] = None
    ) -> Dict:
        """
        Transfer money to a beneficiary.
        
        Args:
            user_id: User identifier
            recipient: Beneficiary name or account number
            amount: Amount to transfer
            description: Transaction description
            
        Returns:
            Dictionary with transaction result
        """
        session = self.db.get_session()
        try:
            # Get user's account
            account = self.get_user_primary_account(user_id)
            if not account:
                return {
                    'success': False,
                    'error': 'Account not found'
                }
            
            # Check sufficient balance
            if account.balance < amount:
                log.warning(f"Insufficient balance for user {user_id}")
                return {
                    'success': False,
                    'error': 'Insufficient balance',
                    'current_balance': account.balance
                }
            
            # Find beneficiary
            beneficiary = session.query(Beneficiary).filter(
                Beneficiary.user_id == user_id
            ).filter(
                (Beneficiary.name.ilike(f'%{recipient}%')) |
                (Beneficiary.nickname.ilike(f'%{recipient}%'))
            ).first()
            
            beneficiary_name = beneficiary.name if beneficiary else recipient
            to_account = beneficiary.account_number if beneficiary else "external"
            
            # Create transaction
            transaction_id = f"TXN{secrets.token_hex(8).upper()}"
            transaction = Transaction(
                id=transaction_id,
                from_account_id=account.id,
                to_account_id=to_account,
                to_beneficiary_name=beneficiary_name,
                amount=amount,
                transaction_type='transfer',
                status='completed',
                description=description or f'Transfer to {beneficiary_name}',
                completed_at=datetime.now()
            )
            
            # Update balance
            account.balance -= amount
            
            session.add(transaction)
            session.commit()
            
            result = {
                'success': True,
                'transaction_id': transaction_id,
                'amount': amount,
                'formatted_amount': format_currency(amount, '₹'),
                'recipient': beneficiary_name,
                'new_balance': account.balance,
                'formatted_balance': format_currency(account.balance, '₹'),
                'timestamp': transaction.completed_at
            }
            
            log.info(f"Transfer successful: {result['formatted_amount']} to {beneficiary_name}")
            return result
            
        except Exception as e:
            session.rollback()
            log.error(f"Error transferring money: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            session.close()
    
    def get_transaction_history(
        self,
        user_id: str,
        limit: int = 10,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """
        Get transaction history.
        
        Args:
            user_id: User identifier
            limit: Maximum number of transactions
            start_date: Start date filter
            end_date: End date filter
            
        Returns:
            Dictionary with transactions
        """
        session = self.db.get_session()
        try:
            account = self.get_user_primary_account(user_id)
            if not account:
                return {
                    'success': False,
                    'error': 'Account not found'
                }
            
            query = session.query(Transaction).filter_by(from_account_id=account.id)
            
            if start_date:
                query = query.filter(Transaction.created_at >= start_date)
            if end_date:
                query = query.filter(Transaction.created_at <= end_date)
            
            transactions = query.order_by(Transaction.created_at.desc()).limit(limit).all()
            
            transaction_list = []
            for txn in transactions:
                transaction_list.append({
                    'id': txn.id,
                    'recipient': txn.to_beneficiary_name,
                    'amount': txn.amount,
                    'formatted_amount': format_currency(txn.amount, '₹'),
                    'type': txn.transaction_type,
                    'status': txn.status,
                    'date': txn.created_at,
                    'description': txn.description
                })
            
            result = {
                'success': True,
                'count': len(transaction_list),
                'transactions': transaction_list
            }
            
            log.info(f"Retrieved {len(transaction_list)} transactions for user {user_id}")
            return result
            
        except Exception as e:
            log.error(f"Error getting transaction history: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            session.close()
    
    def inquire_loan(self, user_id: str, loan_type: str, amount: Optional[float] = None) -> Dict:
        """
        Get loan information and eligibility.
        
        Args:
            user_id: User identifier
            loan_type: Type of loan
            amount: Desired loan amount
            
        Returns:
            Dictionary with loan information
        """
        # Simulated loan rates and terms
        loan_info = {
            'personal': {
                'min_amount': 50000,
                'max_amount': 1000000,
                'interest_rate': 10.5,
                'max_tenure': 60
            },
            'home': {
                'min_amount': 500000,
                'max_amount': 10000000,
                'interest_rate': 8.5,
                'max_tenure': 240
            },
            'car': {
                'min_amount': 100000,
                'max_amount': 2000000,
                'interest_rate': 9.0,
                'max_tenure': 84
            },
            'education': {
                'min_amount': 100000,
                'max_amount': 5000000,
                'interest_rate': 9.5,
                'max_tenure': 120
            }
        }
        
        if loan_type not in loan_info:
            return {
                'success': False,
                'error': 'Invalid loan type'
            }
        
        info = loan_info[loan_type]
        
        result = {
            'success': True,
            'loan_type': loan_type,
            'interest_rate': info['interest_rate'],
            'min_amount': info['min_amount'],
            'max_amount': info['max_amount'],
            'max_tenure_months': info['max_tenure']
        }
        
        # Calculate EMI if amount provided
        if amount:
            tenure = 36  # Default 3 years
            monthly_rate = info['interest_rate'] / (12 * 100)
            emi = (amount * monthly_rate * (1 + monthly_rate)**tenure) / ((1 + monthly_rate)**tenure - 1)
            
            result['amount'] = amount
            result['formatted_amount'] = format_currency(amount, '₹')
            result['tenure_months'] = tenure
            result['emi'] = round(emi, 2)
            result['formatted_emi'] = format_currency(emi, '₹')
            result['total_payable'] = round(emi * tenure, 2)
            result['formatted_total'] = format_currency(emi * tenure, '₹')
        
        log.info(f"Loan inquiry: {loan_type} for user {user_id}")
        return result
    
    def set_reminder(
        self,
        user_id: str,
        title: str,
        amount: Optional[float] = None,
        beneficiary: Optional[str] = None,
        due_date: Optional[datetime] = None,
        frequency: str = 'once'
    ) -> Dict:
        """
        Set payment reminder.
        
        Args:
            user_id: User identifier
            title: Reminder title
            amount: Payment amount
            beneficiary: Beneficiary name
            due_date: Due date
            frequency: Reminder frequency
            
        Returns:
            Dictionary with reminder result
        """
        session = self.db.get_session()
        try:
            reminder = Reminder(
                user_id=user_id,
                title=title,
                amount=amount,
                beneficiary_name=beneficiary,
                due_date=due_date or datetime.now() + timedelta(days=1),
                frequency=frequency
            )
            
            session.add(reminder)
            session.commit()
            
            result = {
                'success': True,
                'reminder_id': reminder.id,
                'title': title,
                'amount': amount,
                'formatted_amount': format_currency(amount, '₹') if amount else None,
                'beneficiary': beneficiary,
                'due_date': reminder.due_date,
                'frequency': frequency
            }
            
            log.info(f"Reminder set for user {user_id}: {title}")
            return result
            
        except Exception as e:
            session.rollback()
            log.error(f"Error setting reminder: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            session.close()
    
    def get_beneficiaries(self, user_id: str) -> List[Dict]:
        """
        Get user's saved beneficiaries.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of beneficiaries
        """
        session = self.db.get_session()
        try:
            beneficiaries = session.query(Beneficiary).filter_by(user_id=user_id).all()
            
            result = [
                {
                    'id': b.id,
                    'name': b.name,
                    'nickname': b.nickname,
                    'account_number': b.account_number
                }
                for b in beneficiaries
            ]
            
            return result
            
        finally:
            session.close()
