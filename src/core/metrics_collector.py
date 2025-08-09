import time
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import statistics

@dataclass
class PerformanceMetric:
    timestamp: float
    model: str
    prompt_length: int
    response_time: float
    tokens_generated: int
    tokens_per_second: float
    memory_usage: float
    cpu_usage: float
    status_code: int
    error: Optional[str] = None

class MetricsCollector:
    def __init__(self):
        self.metrics: List[PerformanceMetric] = []
        self.start_time = time.time()
    
    def add_metric(self, metric: PerformanceMetric):
        """Add a performance metric"""
        self.metrics.append(metric)
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Calculate summary statistics"""
        if not self.metrics:
            return {}
        
        response_times = [m.response_time for m in self.metrics]
        tokens_per_sec = [m.tokens_per_second for m in self.metrics if m.tokens_per_second > 0]
        
        return {
            'total_requests': len(self.metrics),
            'successful_requests': len([m for m in self.metrics if m.status_code == 200]),
            'failed_requests': len([m for m in self.metrics if m.status_code != 200]),
            'avg_response_time': statistics.mean(response_times),
            'min_response_time': min(response_times),
            'max_response_time': max(response_times),
            'p95_response_time': statistics.quantiles(response_times, n=20)[18],  # 95th percentile
            'p99_response_time': statistics.quantiles(response_times, n=100)[98], # 99th percentile
            'avg_tokens_per_second': statistics.mean(tokens_per_sec) if tokens_per_sec else 0,
            'total_test_duration': time.time() - self.start_time,
            'requests_per_second': len(self.metrics) / (time.time() - self.start_time)
        }
    
    def export_to_csv(self, filename: str):
        """Export metrics to CSV"""
        df = pd.DataFrame([
            {
                'timestamp': m.timestamp,
                'model': m.model,
                'prompt_length': m.prompt_length,
                'response_time': m.response_time,
                'tokens_generated': m.tokens_generated,
                'tokens_per_second': m.tokens_per_second,
                'memory_usage': m.memory_usage,
                'cpu_usage': m.cpu_usage,
                'status_code': m.status_code,
                'error': m.error
            } for m in self.metrics
        ])
        df.to_csv(filename, index=False)
    
    def export_to_json(self, filename: str):
        """Export metrics to JSON"""
        data = {
            'summary': self.get_summary_stats(),
            'metrics': [
                {
                    'timestamp': m.timestamp,
                    'model': m.model,
                    'prompt_length': m.prompt_length,
                    'response_time': m.response_time,
                    'tokens_generated': m.tokens_generated,
                    'tokens_per_second': m.tokens_per_second,
                    'memory_usage': m.memory_usage,
                    'cpu_usage': m.cpu_usage,
                    'status_code': m.status_code,
                    'error': m.error
                } for m in self.metrics
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
