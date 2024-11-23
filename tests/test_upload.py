import concurrent.futures
import time
from pathlib import Path
import requests

def create_test_file(size_kb):
    path = Path(f"test_file_{size_kb}kb.txt")
    with open(path, 'wb') as f:
        f.write(b'0' * (size_kb * 1024))
    return path

def upload_file(file_path, url='http://localhost:8000/upload'):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        return requests.post(url, files=files)

def test_concurrent_uploads():
    # Create test files of different sizes
    files = [create_test_file(size) for size in [100, 500, 1000]]
    
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(upload_file, file) for file in files * 5]  # Upload each file 5 times
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    elapsed = time.time() - start_time
    
    # Cleanup
    for file in files:
        file.unlink()
    
    # Assertions
    assert all(r.status_code == 200 for r in results)
    assert elapsed < 30  # All uploads should complete within 30 seconds

def test_large_file_upload():
    file = create_test_file(5000)  # 5MB file
    
    start_time = time.time()
    response = upload_file(file)
    elapsed = time.time() - start_time
    
    file.unlink()
    
    assert response.status_code == 200
    assert elapsed < 10  # Single large upload should complete within 10 seconds
