from prometheus_client import start_http_server, Counter
import time

requests = Counter('http_requests_total', 'Total HTTP requests made')

def generate_metrics():
    while True:
        requests.inc()  # Increment the counter
        time.sleep(5)

if __name__ == "__main__":
    start_http_server(8000)  # Expose metrics at http://localhost:8000
    generate_metrics()
