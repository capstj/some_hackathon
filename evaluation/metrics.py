"""
Evaluation metrics module for WhisPay.
Tracks and measures system performance and user experience.
"""

from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
import json
from collections import defaultdict
from utils.logger import log
from app.config import settings


class EvaluationMetrics:
    """Tracks and calculates evaluation metrics."""
    
    def __init__(self, export_path: str = None):
        """
        Initialize evaluation metrics.
        
        Args:
            export_path: Path to export metrics
        """
        self.export_path = Path(export_path or settings.metrics_export_path)
        self.export_path.mkdir(parents=True, exist_ok=True)
        
        # Metrics storage
        self.metrics = {
            'intent_recognition': [],
            'response_times': [],
            'authentication_results': [],
            'transaction_results': [],
            'emotion_detections': [],
            'trust_level_changes': [],
            'user_feedback': []
        }
        
        log.info("Evaluation metrics initialized")
    
    def record_intent_recognition(
        self,
        user_input: str,
        detected_intent: str,
        confidence: float,
        correct_intent: Optional[str] = None
    ):
        """
        Record intent recognition result.
        
        Args:
            user_input: User's input text
            detected_intent: Detected intent
            confidence: Confidence score
            correct_intent: Actual correct intent (if known)
        """
        record = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'detected_intent': detected_intent,
            'confidence': confidence,
            'correct_intent': correct_intent,
            'is_correct': detected_intent == correct_intent if correct_intent else None
        }
        
        self.metrics['intent_recognition'].append(record)
        log.info(f"Intent recognition recorded: {detected_intent} ({confidence:.2f})")
    
    def record_response_time(
        self,
        operation: str,
        response_time_ms: float,
        success: bool = True
    ):
        """
        Record system response time.
        
        Args:
            operation: Operation type
            response_time_ms: Response time in milliseconds
            success: Whether operation succeeded
        """
        record = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'response_time_ms': response_time_ms,
            'success': success
        }
        
        self.metrics['response_times'].append(record)
        log.info(f"Response time recorded: {operation} - {response_time_ms:.0f}ms")
    
    def record_authentication(
        self,
        method: str,
        success: bool,
        confidence: Optional[float] = None,
        error_reason: Optional[str] = None
    ):
        """
        Record authentication attempt.
        
        Args:
            method: Authentication method used
            success: Whether authentication succeeded
            confidence: Confidence score if applicable
            error_reason: Reason for failure if applicable
        """
        record = {
            'timestamp': datetime.now().isoformat(),
            'method': method,
            'success': success,
            'confidence': confidence,
            'error_reason': error_reason
        }
        
        self.metrics['authentication_results'].append(record)
        log.info(f"Authentication recorded: {method} - {'Success' if success else 'Failed'}")
    
    def record_transaction(
        self,
        transaction_type: str,
        success: bool,
        amount: Optional[float] = None,
        error_reason: Optional[str] = None
    ):
        """
        Record transaction attempt.
        
        Args:
            transaction_type: Type of transaction
            success: Whether transaction succeeded
            amount: Transaction amount
            error_reason: Reason for failure if applicable
        """
        record = {
            'timestamp': datetime.now().isoformat(),
            'transaction_type': transaction_type,
            'success': success,
            'amount': amount,
            'error_reason': error_reason
        }
        
        self.metrics['transaction_results'].append(record)
        log.info(f"Transaction recorded: {transaction_type} - {'Success' if success else 'Failed'}")
    
    def record_emotion_detection(
        self,
        primary_emotion: str,
        confidence_level: float,
        needs_reassurance: bool
    ):
        """
        Record emotion detection result.
        
        Args:
            primary_emotion: Detected emotion
            confidence_level: User's confidence level
            needs_reassurance: Whether reassurance was needed
        """
        record = {
            'timestamp': datetime.now().isoformat(),
            'primary_emotion': primary_emotion,
            'confidence_level': confidence_level,
            'needs_reassurance': needs_reassurance
        }
        
        self.metrics['emotion_detections'].append(record)
    
    def record_trust_level_change(
        self,
        from_level: str,
        to_level: str,
        reason: str
    ):
        """
        Record trust level change.
        
        Args:
            from_level: Previous trust level
            to_level: New trust level
            reason: Reason for change
        """
        record = {
            'timestamp': datetime.now().isoformat(),
            'from_level': from_level,
            'to_level': to_level,
            'reason': reason
        }
        
        self.metrics['trust_level_changes'].append(record)
        log.info(f"Trust level changed: {from_level} -> {to_level}")
    
    def calculate_intent_accuracy(self) -> Dict:
        """
        Calculate intent recognition accuracy.
        
        Returns:
            Dictionary with accuracy metrics
        """
        records = [r for r in self.metrics['intent_recognition'] if r['is_correct'] is not None]
        
        if not records:
            return {'accuracy': 0.0, 'total_samples': 0}
        
        correct = sum(1 for r in records if r['is_correct'])
        total = len(records)
        accuracy = correct / total
        
        # Calculate per-intent accuracy
        by_intent = defaultdict(lambda: {'correct': 0, 'total': 0})
        for r in records:
            intent = r['detected_intent']
            by_intent[intent]['total'] += 1
            if r['is_correct']:
                by_intent[intent]['correct'] += 1
        
        intent_accuracy = {
            intent: data['correct'] / data['total']
            for intent, data in by_intent.items()
        }
        
        return {
            'overall_accuracy': accuracy,
            'total_samples': total,
            'correct_predictions': correct,
            'by_intent': intent_accuracy
        }
    
    def calculate_response_time_stats(self) -> Dict:
        """
        Calculate response time statistics.
        
        Returns:
            Dictionary with response time stats
        """
        if not self.metrics['response_times']:
            return {}
        
        times = [r['response_time_ms'] for r in self.metrics['response_times']]
        
        return {
            'average_ms': sum(times) / len(times),
            'min_ms': min(times),
            'max_ms': max(times),
            'median_ms': sorted(times)[len(times) // 2],
            'total_operations': len(times)
        }
    
    def calculate_authentication_success_rate(self) -> Dict:
        """
        Calculate authentication success rates.
        
        Returns:
            Dictionary with authentication metrics
        """
        if not self.metrics['authentication_results']:
            return {}
        
        total = len(self.metrics['authentication_results'])
        successful = sum(1 for r in self.metrics['authentication_results'] if r['success'])
        
        # By method
        by_method = defaultdict(lambda: {'success': 0, 'total': 0})
        for r in self.metrics['authentication_results']:
            method = r['method']
            by_method[method]['total'] += 1
            if r['success']:
                by_method[method]['success'] += 1
        
        method_success_rates = {
            method: data['success'] / data['total']
            for method, data in by_method.items()
        }
        
        return {
            'overall_success_rate': successful / total,
            'total_attempts': total,
            'successful_attempts': successful,
            'by_method': method_success_rates
        }
    
    def generate_report(self) -> Dict:
        """
        Generate comprehensive evaluation report.
        
        Returns:
            Complete evaluation report
        """
        report = {
            'generated_at': datetime.now().isoformat(),
            'intent_recognition': self.calculate_intent_accuracy(),
            'response_times': self.calculate_response_time_stats(),
            'authentication': self.calculate_authentication_success_rate(),
            'emotion_detections': {
                'total_detections': len(self.metrics['emotion_detections']),
                'reassurance_needed_count': sum(
                    1 for r in self.metrics['emotion_detections']
                    if r['needs_reassurance']
                )
            },
            'trust_level_changes': {
                'total_changes': len(self.metrics['trust_level_changes'])
            }
        }
        
        return report
    
    def export_metrics(self, filename: Optional[str] = None):
        """
        Export metrics to JSON file.
        
        Args:
            filename: Output filename
        """
        filename = filename or f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.export_path / filename
        
        report = self.generate_report()
        report['raw_metrics'] = self.metrics
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        log.info(f"Metrics exported to {filepath}")
        return filepath


# Global metrics instance
metrics = EvaluationMetrics()
