from kafka import KafkaProducer
from time import sleep
import json
import csv

# Create a kafka topic and a producer    
kafka_topic = 'machineindus'

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Define the function to load data from CSV
def read_csv(file_path):
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

# Send data to topic
while True:
    data = read_csv("data.csv")
    for line in data:
        # Check if any value in the row is None
        if any(value is None for value in line.values()):
            continue  # Skip the row if any value is None
        
        d = {
            "UDI": int(line.get('UDI')),
            "Product ID": str(line.get('Product ID')),
            "Type": str(line.get('Type')),
            "Air temperature [K]": float(line.get('Air temperature [K]')),
            "Process temperature [K]": float(line.get('Process temperature [K]')),
            "Rotational speed [rpm]": float(line.get('Rotational speed [rpm]')),
            "Torque [Nm]": float(line.get('Torque [Nm]')),
            "Tool wear [min]": int(line.get('Tool wear [min]')),
            "Target": int(line.get('Target'))
        }
        producer.send(kafka_topic, value=d)
        print(d)
        sleep(0.05)
    sleep(60)
