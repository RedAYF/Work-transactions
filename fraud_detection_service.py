from kafka import KafkaConsumer, KafkaProducer
import json


class FraudDetectionService:
    def __init__(self, kafka_server):
        self.producer = KafkaProducer(bootstrap_servers=kafka_server)
        self.consumer = KafkaConsumer('fraud_detection', bootstrap_servers=kafka_server,
                                      auto_offset_reset='earliest')

    def check_fraud(self, transaction_data):
        print("Checking fraud for transaction:", transaction_data)
        if transaction_data.get('amount') > 10000:
            transaction_data['status'] = 'fraud'
            print("Transaction marked as fraud")
        else:
            transaction_data['status'] = 'approved'
            print("Transaction approved")

        self.producer.send('logged_transactions', json.dumps(transaction_data).encode('utf-8'))

    def consume_transactions(self):
        print("FraudDetectionService: Consuming messages from 'validated_transactions'")
        for message in self.consumer:
            transaction_data = json.loads(message.value.decode('utf-8'))
            print("Received transaction in FraudDetectionService:", transaction_data)
            self.check_fraud(transaction_data)

