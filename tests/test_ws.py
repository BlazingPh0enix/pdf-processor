import asyncio
import websockets
import pytest
import time
from concurrent.futures import ThreadPoolExecutor

async def websocket_client(messages=100):
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        for i in range(messages):
            await websocket.send(f"Message {i}")
            response = await websocket.recv()
            assert response is not None

async def test_concurrent_websocket_connections():
    num_clients = 50
    tasks = []
    
    start_time = time.time()
    
    for _ in range(num_clients):
        tasks.append(websocket_client())
    
    await asyncio.gather(*tasks)
    
    elapsed = time.time() - start_time
    assert elapsed < 60  # All connections should complete within 60 seconds

@pytest.mark.asyncio
async def test_websocket_long_connection():
    uri = "ws://localhost:8000/ws"
    message_count = 1000
    
    start_time = time.time()
    async with websockets.connect(uri) as websocket:
        for i in range(message_count):
            await websocket.send(f"Message {i}")
            response = await websocket.recv()
            assert response is not None
            
            if i % 100 == 0:  # Check every 100 messages
                current_time = time.time()
                assert current_time - start_time < 30  # Should process 100 messages within 30 seconds
