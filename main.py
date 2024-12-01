import threading
from services.validation_service import ValidationService
from services.fraud_detection_service import FraudDetectionService
from services.logging_service import LoggingService
from services.valute_convertor_service import ValuteConverterService
from db import initialize_db
from config import DB_NAME
from container_setup import ContainerSetup

def start_services(container_setup):
    container_info = container_setup.start_containers()
    kafka_server = container_info["kafka_bootstrap_server"]
    redis_host = container_info["redis_host"]
    redis_port = container_info["redis_port"]

    with open("kafka_config.txt", "w") as f:
        f.write(kafka_server)

    initialize_db()

    validation_service = ValidationService(kafka_server)
    fraud_detection_service = FraudDetectionService(kafka_server)
    logging_service = LoggingService(kafka_server, DB_NAME)
    valute_convertor_service = ValuteConverterService(kafka_server, redis_host, redis_port)

    threading.Thread(target=validation_service.consume_transactions, daemon=True).start()
    threading.Thread(target=valute_convertor_service.consume_transactions, daemon=True).start()
    threading.Thread(target=fraud_detection_service.consume_transactions, daemon=True).start()
    threading.Thread(target=logging_service.consume_transactions, daemon=True).start()

    print("All services started and consuming transactions...")

if __name__ == "__main__":
    container_setup = ContainerSetup()
    try:
        start_services(container_setup)
        while True:
            pass
    except KeyboardInterrupt:
        print("Service stopped.")
    finally:
        container_setup.stop_containers()


