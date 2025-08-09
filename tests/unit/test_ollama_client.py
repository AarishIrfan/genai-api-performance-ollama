import pytest
import requests
from src.core.ollama_client import OllamaClient

def test_ollama_client_initialization():
    client = OllamaClient(base_url="http://localhost:5000", model_name="llama2")
    assert client.base_url == "http://localhost:5000"
    assert client.model_name == "llama2"
    assert client.timeout == 30

@pytest.mark.asyncio
async def test_generate_success(mocker):
    client = OllamaClient(base_url="http://localhost:5000", model_name="llama2")
    mocker.patch('requests.post')
    
    # Test successful generation
    await client.generate("test prompt")
    requests.post.assert_called_once_with(
        "http://localhost:5000/generate",
        json={"prompt": "test prompt"},
        timeout=30
    )

def test_health_check(mocker):
    client = OllamaClient(base_url="http://localhost:5000", model_name="llama2")
    mocker.patch('requests.get')
    
    # Test health check
    client.health_check()
    requests.get.assert_called_once_with("http://localhost:5000/health")
