# memory_profiler.py
## The below script is a memory profiler, that runs our app and estimates the hardware requirements needed, so that we can ascertain the necessary memory resources before deploying into production.

from memory_profiler import profile
from app import app

@profile
def run_app():
    app.config['TESTING'] = True
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

if __name__ == "__main__":
    run_app()

    
  
  