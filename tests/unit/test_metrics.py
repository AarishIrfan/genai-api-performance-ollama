import pytest
import requests
from src.core.metrics_collector import MetricsCollector, PerformanceMetrics
from datetime import datetime

def test_metrics_collector_initialization():
    collector = MetricsCollector()
    assert collector is not None

def test_record_metrics():
    collector = MetricsCollector()
    metrics = PerformanceMetrics(
        latency=0.5,
        tokens_per_second=100,
        memory_usage=1024,
        timestamp=datetime.now()
    )
    
    collector.record_request(metrics)
    summary = collector.get_summary()
    
    assert 'latency' in summary
    assert 'tokens_per_second' in summary
    assert 'memory_usage' in summary
