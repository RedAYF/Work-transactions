from kafka import KafkaConsumer, KafkaProducer
import json
import sqlite3

class LoggingService:
    def __init__(self, kafka_server, db_name):
        self.consumer = KafkaConsumer('logged_transactions', bootstrap_servers=kafka_server)
        self.producer = KafkaProducer(bootstrap_servers=kafka_server)
        self.db_name = db_name

    def log_transaction(self, transaction_data):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (user_id, order_id, amount, status) VALUES (?, ?, ?, ?)",
            (transaction_data['user_id'], transaction_data['order_id'], transaction_data['converted_amount'],
             transaction_data['status'])
        )
        conn.commit()
        conn.close()
        print("Transaction logged:", transaction_data)

        transaction_data['message'] = "Transaction completed successfully"
        self.producer.send('transaction_complete', json.dumps(transaction_data).encode('utf-8'))

    def consume_transactions(self):
        print("LoggingService: Consuming messages from 'logged_transactions'")
        for message in self.consumer:
            transaction_data = json.loads(message.value.decode('utf-8'))
            self.log_transaction(transaction_data)
