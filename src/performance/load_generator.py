import asyncio
import aiohttp
import time
from typing import List, Dict, Callable
from concurrent.futures import ThreadPoolExecutor
import threading
from src.core.ollama_client import OllamaClient
from src.core.metrics_collector import MetricsCollector, PerformanceMetric

class LoadGenerator:
    def __init__(self, ollama_client: OllamaClient, metrics_collector: MetricsCollector):
        self.client = ollama_client
        self.metrics = metrics_collector
        self.results = []
    
    def constant_load_test(self, 
                          model: str, 
                          prompts: List[str], 
                          users: int = 10, 
                          duration: int = 60):
        """Constant load test with specified number of users"""
        print(f"🚀 Starting constant load test: {users} users for {duration}s")
        
        def worker():
            start_time = time.time()
            while time.time() - start_time < duration:
                for prompt in prompts:
                    try:
                        result = self.client.generate(model, prompt)
                        
                        metric = PerformanceMetric(
                            timestamp=time.time(),
                            model=model,
                            prompt_length=len(prompt),
                            response_time=result.get('response_time', 0),
                            tokens_generated=len(result.get('response', '').split()),
                            tokens_per_second=len(result.get('response', '').split()) / result.get('response_time', 1),
                            memory_usage=0,  # TODO: Implement memory monitoring
                            cpu_usage=0,     # TODO: Implement CPU monitoring
                            status_code=result.get('status_code', 500)
                        )
                        
                        self.metrics.add_metric(metric)
                        
                    except Exception as e:
                        metric = PerformanceMetric(
                            timestamp=time.time(),
                            model=model,
                            prompt_length=len(prompt),
                            response_time=0,
                            tokens_generated=0,
                            tokens_per_second=0,
                            memory_usage=0,
                            cpu_usage=0,
                            status_code=500,
                            error=str(e)
                        )
                        self.metrics.add_metric(metric)
        
        # Create threads for concurrent users
        threads = []
        for _ in range(users):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        return self.metrics.get_summary_stats()
