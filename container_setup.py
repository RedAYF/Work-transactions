from testcontainers.redis import RedisContainer
from testcontainers.kafka import KafkaContainer
import redis

class ContainerSetup:
    def __init__(self):
        self.redis_container = RedisContainer()
        self.kafka_container = KafkaContainer()

    def start_containers(self):
        self.redis_container.start()
        redis_port = self.redis_container.get_exposed_port(6379)
        redis_client = redis.Redis(host="localhost", port=redis_port)

        redis_client.set("USDT_RUB", 75)

        self.kafka_container.start()
        kafka_bootstrap_server = self.kafka_container.get_bootstrap_server()

        return {
            "redis_host": "localhost",
            "redis_port": redis_port,
            "kafka_bootstrap_server": kafka_bootstrap_server
        }

    def stop_containers(self):
        self.redis_container.stop()
        self.kafka_container.stop()

