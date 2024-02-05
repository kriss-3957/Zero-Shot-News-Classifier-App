# memory_profiler.py
## The below script is a memory profiler, that runs our app and estimates the hardware requirements needed, so that we can ascertain the necessary memory resources before deploying into production.
## Many free demployment platforms like Vercel, zeet etc, have memory restrictions of 300 mb or so.
## Since we're using a Zero Shot model, utilizing a HuggingFace pipeline directly, these can be very memory intensive required gegabytes of memory space

## Run the below script in the CLI with the mprof command to generate a memory profile data file:
### mprof run hardware_reqs.py

## To generate a plot of the memory usage with peak memory load use the below CLI command :
### mprof plot


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

    
  
  
