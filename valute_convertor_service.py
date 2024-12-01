from kafka import KafkaConsumer, KafkaProducer
import redis
import json

class ValuteConverterService:
    def __init__(self, kafka_server, redis_host, redis_port):
        self.producer = KafkaProducer(bootstrap_servers=kafka_server)
        self.consumer = KafkaConsumer('validated_transactions', bootstrap_servers=kafka_server)
        self.redis_client = redis.Redis(host=redis_host, port=redis_port)

    def convert_currency(self, transaction_data):
        from_currency = transaction_data['currency']
        to_currency = 'RUB'
        amount = transaction_data['amount']
        order_id = transaction_data['order_id']

        if from_currency == "USDT":
            rate = float(self.redis_client.get("USDT_RUB") or 1)
            converted_amount = amount * rate
            transaction_data['converted_amount'] = converted_amount
            print(f"Order {order_id}: Converted {amount} {from_currency} to {converted_amount} {to_currency}")
        else:
            transaction_data['converted_amount'] = amount

        self.producer.send('fraud_detection', json.dumps(transaction_data).encode('utf-8'))

    def consume_transactions(self):
        for message in self.consumer:
            transaction_data = json.loads(message.value.decode('utf-8'))
            self.convert_currency(transaction_data)
