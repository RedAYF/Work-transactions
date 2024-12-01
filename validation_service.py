from kafka import KafkaConsumer, KafkaProducer
import json

class ValidationService:
    def __init__(self, kafka_server):
        self.producer = KafkaProducer(bootstrap_servers=kafka_server)
        self.consumer = KafkaConsumer('transaction_validation', bootstrap_servers=kafka_server,
                                      auto_offset_reset='earliest')

    def validate_transaction(self, transaction_data):
        print("Validating transaction:", transaction_data)
        if transaction_data.get('amount') > 0:
            print("Transaction is valid, sending to 'validated_transactions' topic")
            self.producer.send('validated_transactions', json.dumps(transaction_data).encode('utf-8'))
        else:
            print("Invalid transaction data")

    def consume_transactions(self):
        print("ValidationService: Consuming messages from 'transaction_validation'")
        for message in self.consumer:
            transaction_data = json.loads(message.value.decode('utf-8'))
            print("Received transaction in ValidationService:", transaction_data)
            self.validate_transaction(transaction_data)

