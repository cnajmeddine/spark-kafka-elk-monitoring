from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_logs():
    logs = [
        {"level": "INFO", "message": "This is an info log"},
        {"level": "ERROR", "message": "This is an error log"}
    ]
    while True:
        for log in logs:
            producer.send('logs-topic', log)
            print(f"Sent log: {log}")
            time.sleep(1)

if __name__ == "__main__":
    generate_logs()
