"""
User feedback collection module for WhisPay.
Gathers user feedback for evaluation and improvement.
"""

from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
import json
from utils.logger import log
from app.config import settings


class FeedbackCollector:
    """Collects and stores user feedback."""
    
    def __init__(self, storage_path: str = None):
        """
        Initialize feedback collector.
        
        Args:
            storage_path: Path to store feedback
        """
        self.storage_path = Path(storage_path or settings.metrics_export_path) / "feedback"
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.feedback_records: List[Dict] = []
        log.info("Feedback collector initialized")
    
    def collect_session_feedback(
        self,
        user_id: str,
        session_duration: float,
        tasks_completed: int,
        satisfaction_rating: int,
        ease_of_use_rating: int,
        trust_rating: int,
        comments: Optional[str] = None
    ) -> Dict:
        """
        Collect feedback after a session.
        
        Args:
            user_id: User identifier
            session_duration: Session duration in seconds
            tasks_completed: Number of tasks completed
            satisfaction_rating: Overall satisfaction (1-5)
            ease_of_use_rating: Ease of use rating (1-5)
            trust_rating: Trust level rating (1-5)
            comments: Optional user comments
            
        Returns:
            Feedback record
        """
        feedback = {
            'feedback_id': f"FB{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'session_duration_seconds': session_duration,
            'tasks_completed': tasks_completed,
            'ratings': {
                'satisfaction': satisfaction_rating,
                'ease_of_use': ease_of_use_rating,
                'trust': trust_rating
            },
            'comments': comments,
            'type': 'session_feedback'
        }
        
        self.feedback_records.append(feedback)
        self._save_feedback(feedback)
        
        log.info(f"Session feedback collected from user {user_id}")
        return feedback
    
    def collect_feature_feedback(
        self,
        user_id: str,
        feature_name: str,
        usefulness_rating: int,
        worked_as_expected: bool,
        comments: Optional[str] = None
    ) -> Dict:
        """
        Collect feedback on specific feature.
        
        Args:
            user_id: User identifier
            feature_name: Name of feature
            usefulness_rating: Usefulness rating (1-5)
            worked_as_expected: Whether feature worked as expected
            comments: Optional comments
            
        Returns:
            Feedback record
        """
        feedback = {
            'feedback_id': f"FB{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'feature_name': feature_name,
            'usefulness_rating': usefulness_rating,
            'worked_as_expected': worked_as_expected,
            'comments': comments,
            'type': 'feature_feedback'
        }
        
        self.feedback_records.append(feedback)
        self._save_feedback(feedback)
        
        log.info(f"Feature feedback collected: {feature_name}")
        return feedback
    
    def collect_error_feedback(
        self,
        user_id: str,
        error_type: str,
        context: str,
        user_frustrated: bool,
        recovery_successful: bool,
        comments: Optional[str] = None
    ) -> Dict:
        """
        Collect feedback when error occurs.
        
        Args:
            user_id: User identifier
            error_type: Type of error
            context: Context where error occurred
            user_frustrated: Whether user seemed frustrated
            recovery_successful: Whether error was recovered from
            comments: Optional comments
            
        Returns:
            Feedback record
        """
        feedback = {
            'feedback_id': f"FB{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'error_type': error_type,
            'context': context,
            'user_frustrated': user_frustrated,
            'recovery_successful': recovery_successful,
            'comments': comments,
            'type': 'error_feedback'
        }
        
        self.feedback_records.append(feedback)
        self._save_feedback(feedback)
        
        log.info(f"Error feedback collected: {error_type}")
        return feedback
    
    def _save_feedback(self, feedback: Dict):
        """Save feedback to file."""
        if not settings.collect_feedback:
            return
        
        filename = f"feedback_{feedback['feedback_id']}.json"
        filepath = self.storage_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(feedback, f, indent=2)
    
    def get_average_ratings(self) -> Dict:
        """
        Calculate average ratings from all feedback.
        
        Returns:
            Dictionary with average ratings
        """
        session_feedback = [f for f in self.feedback_records if f['type'] == 'session_feedback']
        
        if not session_feedback:
            return {}
        
        total_satisfaction = sum(f['ratings']['satisfaction'] for f in session_feedback)
        total_ease = sum(f['ratings']['ease_of_use'] for f in session_feedback)
        total_trust = sum(f['ratings']['trust'] for f in session_feedback)
        count = len(session_feedback)
        
        return {
            'average_satisfaction': total_satisfaction / count,
            'average_ease_of_use': total_ease / count,
            'average_trust': total_trust / count,
            'total_responses': count
        }
    
    def get_feature_feedback_summary(self) -> Dict:
        """
        Get summary of feature feedback.
        
        Returns:
            Summary by feature
        """
        feature_feedback = [f for f in self.feedback_records if f['type'] == 'feature_feedback']
        
        summary = {}
        for feedback in feature_feedback:
            feature = feedback['feature_name']
            if feature not in summary:
                summary[feature] = {
                    'total_feedback': 0,
                    'total_usefulness': 0,
                    'worked_as_expected_count': 0
                }
            
            summary[feature]['total_feedback'] += 1
            summary[feature]['total_usefulness'] += feedback['usefulness_rating']
            if feedback['worked_as_expected']:
                summary[feature]['worked_as_expected_count'] += 1
        
        # Calculate averages
        for feature, data in summary.items():
            data['average_usefulness'] = data['total_usefulness'] / data['total_feedback']
            data['success_rate'] = data['worked_as_expected_count'] / data['total_feedback']
        
        return summary


# Global feedback collector instance
feedback_collector = FeedbackCollector()
