import requests
import time
import json
from typing import Dict, List, Optional
import asyncio
import aiohttp

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> List[Dict]:
        """List available models"""
        response = self.session.get(f"{self.base_url}/api/tags")
        return response.json().get('models', [])
    
    def generate(self, model: str, prompt: str, **kwargs) -> Dict:
        """Generate response from model"""
        start_time = time.time()
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            **kwargs
        }
        
        response = self.session.post(
            f"{self.base_url}/api/generate",
            json=payload
        )
        
        end_time = time.time()
        result = response.json()
        result['response_time'] = end_time - start_time
        result['status_code'] = response.status_code
        
        return result
    
    async def async_generate(self, session, model: str, prompt: str, **kwargs) -> Dict:
        """Async version for concurrent requests"""
        start_time = time.time()
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            **kwargs
        }
        
        async with session.post(
            f"{self.base_url}/api/generate",
            json=payload
        ) as response:
            result = await response.json()
            end_time = time.time()
            result['response_time'] = end_time - start_time
            result['status_code'] = response.status
            return result
