"""
Predictive analytics module for WhisPay.
Analyzes spending patterns and provides proactive suggestions.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
from banking.database import db, Transaction, Reminder
from utils.logger import log
from utils.helpers import format_currency
from app.config import settings


class BankingPredictor:
    """Provides predictive banking features."""
    
    def __init__(self):
        """Initialize predictor."""
        self.db = db
        log.info("Banking predictor initialized")
    
    def analyze_spending_patterns(self, user_id: str, days: int = 90) -> Dict:
        """
        Analyze user's spending patterns.
        
        Args:
            user_id: User identifier
            days: Number of days to analyze
            
        Returns:
            Dictionary with spending analysis
        """
        session = self.db.get_session()
        try:
            # Get account
            from banking.operations import BankingOperations
            ops = BankingOperations()
            account = ops.get_user_primary_account(user_id)
            
            if not account:
                return {'success': False, 'error': 'Account not found'}
            
            # Get transactions from last N days
            start_date = datetime.now() - timedelta(days=days)
            transactions = session.query(Transaction).filter(
                Transaction.from_account_id == account.id,
                Transaction.created_at >= start_date,
                Transaction.status == 'completed'
            ).all()
            
            if not transactions:
                return {
                    'success': True,
                    'total_spent': 0,
                    'transaction_count': 0,
                    'message': 'No transactions found in the analyzed period'
                }
            
            # Calculate statistics
            total_spent = sum(txn.amount for txn in transactions)
            avg_transaction = total_spent / len(transactions)
            
            # Group by recipient
            by_recipient = defaultdict(lambda: {'count': 0, 'total': 0})
            for txn in transactions:
                recipient = txn.to_beneficiary_name
                by_recipient[recipient]['count'] += 1
                by_recipient[recipient]['total'] += txn.amount
            
            # Find top recipients
            top_recipients = sorted(
                by_recipient.items(),
                key=lambda x: x[1]['total'],
                reverse=True
            )[:5]
            
            # Group by time period
            monthly_spending = defaultdict(float)
            for txn in transactions:
                month_key = txn.created_at.strftime('%Y-%m')
                monthly_spending[month_key] += txn.amount
            
            result = {
                'success': True,
                'period_days': days,
                'total_spent': total_spent,
                'formatted_total': format_currency(total_spent, '₹'),
                'transaction_count': len(transactions),
                'average_transaction': avg_transaction,
                'formatted_avg': format_currency(avg_transaction, '₹'),
                'top_recipients': [
                    {
                        'name': name,
                        'count': data['count'],
                        'total': data['total'],
                        'formatted_total': format_currency(data['total'], '₹')
                    }
                    for name, data in top_recipients
                ],
                'monthly_breakdown': [
                    {
                        'month': month,
                        'amount': amount,
                        'formatted_amount': format_currency(amount, '₹')
                    }
                    for month, amount in sorted(monthly_spending.items())
                ]
            }
            
            log.info(f"Spending analysis for user {user_id}: {result['formatted_total']} over {days} days")
            return result
            
        except Exception as e:
            log.error(f"Error analyzing spending patterns: {e}")
            return {'success': False, 'error': str(e)}
        finally:
            session.close()
    
    def detect_recurring_transactions(self, user_id: str) -> List[Dict]:
        """
        Detect recurring transaction patterns.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of detected recurring transactions
        """
        session = self.db.get_session()
        try:
            from banking.operations import BankingOperations
            ops = BankingOperations()
            account = ops.get_user_primary_account(user_id)
            
            if not account:
                return []
            
            # Get last 90 days of transactions
            start_date = datetime.now() - timedelta(days=settings.prediction_lookback_days)
            transactions = session.query(Transaction).filter(
                Transaction.from_account_id == account.id,
                Transaction.created_at >= start_date,
                Transaction.status == 'completed'
            ).all()
            
            # Group by recipient and amount
            pattern_key = defaultdict(list)
            for txn in transactions:
                key = (txn.to_beneficiary_name, round(txn.amount, -1))  # Round to nearest 10
                pattern_key[key].append(txn.created_at)
            
            # Find patterns that occur regularly
            recurring = []
            threshold = settings.recurring_transaction_threshold
            
            for (recipient, amount), dates in pattern_key.items():
                if len(dates) >= threshold:
                    # Calculate average interval
                    dates_sorted = sorted(dates)
                    intervals = []
                    for i in range(len(dates_sorted) - 1):
                        delta = (dates_sorted[i+1] - dates_sorted[i]).days
                        intervals.append(delta)
                    
                    if intervals:
                        avg_interval = sum(intervals) / len(intervals)
                        
                        # Determine frequency
                        frequency = 'irregular'
                        if 25 <= avg_interval <= 35:
                            frequency = 'monthly'
                        elif 6 <= avg_interval <= 8:
                            frequency = 'weekly'
                        elif avg_interval <= 2:
                            frequency = 'daily'
                        
                        # Calculate next expected date
                        last_date = dates_sorted[-1]
                        next_expected = last_date + timedelta(days=int(avg_interval))
                        
                        recurring.append({
                            'recipient': recipient,
                            'amount': amount,
                            'formatted_amount': format_currency(amount, '₹'),
                            'frequency': frequency,
                            'occurrence_count': len(dates),
                            'last_transaction': last_date,
                            'next_expected': next_expected,
                            'days_until_next': (next_expected - datetime.now()).days,
                            'avg_interval_days': int(avg_interval)
                        })
            
            # Sort by next expected date
            recurring.sort(key=lambda x: x['next_expected'])
            
            log.info(f"Detected {len(recurring)} recurring transactions for user {user_id}")
            return recurring
            
        except Exception as e:
            log.error(f"Error detecting recurring transactions: {e}")
            return []
        finally:
            session.close()
    
    def get_proactive_suggestions(self, user_id: str) -> List[Dict]:
        """
        Generate proactive suggestions for user.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of suggestions
        """
        suggestions = []
        
        # Check for upcoming recurring transactions
        recurring = self.detect_recurring_transactions(user_id)
        for pattern in recurring:
            if 0 <= pattern['days_until_next'] <= 3:
                suggestions.append({
                    'type': 'recurring_payment',
                    'priority': 'high',
                    'message': (
                        f"You usually transfer {pattern['formatted_amount']} to "
                        f"{pattern['recipient']} around this time. "
                        f"Would you like me to process this transaction?"
                    ),
                    'action': {
                        'type': 'transfer',
                        'recipient': pattern['recipient'],
                        'amount': pattern['amount']
                    }
                })
        
        # Check if it's time for monthly summary
        today = datetime.now()
        if today.day == settings.monthly_summary_day:
            suggestions.append({
                'type': 'monthly_summary',
                'priority': 'medium',
                'message': (
                    "It's the beginning of a new month. "
                    "Would you like a summary of your spending from last month?"
                ),
                'action': {
                    'type': 'get_monthly_summary'
                }
            })
        
        # Check pending reminders
        session = self.db.get_session()
        try:
            upcoming_reminders = session.query(Reminder).filter(
                Reminder.user_id == user_id,
                Reminder.is_active == True,
                Reminder.due_date <= datetime.now() + timedelta(days=2),
                Reminder.due_date >= datetime.now()
            ).all()
            
            for reminder in upcoming_reminders:
                days_until = (reminder.due_date - datetime.now()).days
                suggestions.append({
                    'type': 'reminder',
                    'priority': 'high' if days_until == 0 else 'medium',
                    'message': (
                        f"Reminder: {reminder.title} "
                        f"{'is due today' if days_until == 0 else f'is due in {days_until} days'}. "
                        f"{format_currency(reminder.amount, '₹') if reminder.amount else ''}"
                    ),
                    'action': {
                        'type': 'payment_reminder',
                        'reminder_id': reminder.id
                    }
                })
        finally:
            session.close()
        
        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        suggestions.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        log.info(f"Generated {len(suggestions)} proactive suggestions for user {user_id}")
        return suggestions
    
    def get_monthly_summary(self, user_id: str, month: Optional[int] = None, year: Optional[int] = None) -> Dict:
        """
        Get monthly spending summary.
        
        Args:
            user_id: User identifier
            month: Month (1-12), defaults to last month
            year: Year, defaults to current year
            
        Returns:
            Dictionary with monthly summary
        """
        if month is None or year is None:
            last_month = datetime.now().replace(day=1) - timedelta(days=1)
            month = month or last_month.month
            year = year or last_month.year
        
        # Get transactions for the month
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        session = self.db.get_session()
        try:
            from banking.operations import BankingOperations
            ops = BankingOperations()
            account = ops.get_user_primary_account(user_id)
            
            if not account:
                return {'success': False, 'error': 'Account not found'}
            
            transactions = session.query(Transaction).filter(
                Transaction.from_account_id == account.id,
                Transaction.created_at >= start_date,
                Transaction.created_at < end_date,
                Transaction.status == 'completed'
            ).all()
            
            if not transactions:
                return {
                    'success': True,
                    'month': month,
                    'year': year,
                    'total_spent': 0,
                    'transaction_count': 0,
                    'message': 'No transactions in this period'
                }
            
            total_spent = sum(txn.amount for txn in transactions)
            
            # Group by recipient
            by_recipient = defaultdict(float)
            for txn in transactions:
                by_recipient[txn.to_beneficiary_name] += txn.amount
            
            top_recipients = sorted(
                by_recipient.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            # Group by week
            weekly_spending = defaultdict(float)
            for txn in transactions:
                week_num = txn.created_at.isocalendar()[1]
                weekly_spending[week_num] += txn.amount
            
            result = {
                'success': True,
                'month': month,
                'year': year,
                'month_name': datetime(year, month, 1).strftime('%B'),
                'total_spent': total_spent,
                'formatted_total': format_currency(total_spent, '₹'),
                'transaction_count': len(transactions),
                'average_transaction': total_spent / len(transactions),
                'top_recipients': [
                    {
                        'name': name,
                        'amount': amount,
                        'formatted_amount': format_currency(amount, '₹'),
                        'percentage': (amount / total_spent * 100)
                    }
                    for name, amount in top_recipients
                ],
                'weekly_average': sum(weekly_spending.values()) / len(weekly_spending) if weekly_spending else 0
            }
            
            log.info(f"Monthly summary for user {user_id}: {result['month_name']} {year}")
            return result
            
        except Exception as e:
            log.error(f"Error generating monthly summary: {e}")
            return {'success': False, 'error': str(e)}
        finally:
            session.close()
