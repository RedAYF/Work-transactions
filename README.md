# Work-transactions
### Процесс
1. Пользователь вводит сумму и выбирает валюту в веб-интерфейсе, затем нажимает кнопку «Оплатить».

![Снимок экрана 2024-12-01 170933](https://github.com/user-attachments/assets/79569925-cb19-4e56-8aef-c6d8e68c7c16)

2. Транзакция проходит через несколько этапов:

   Validation Service - проверяет корректность данных транзакции.
  
    Valute Convertor Service - преобразует сумму в требуемую валюту.
  
    Fraud Detection Service - анализирует транзакцию на предмет мошеннических действий.
  
    Logging Service - сохраняет информацию о транзакции в базе данных.

3. После успешного завершения всех этапов пользователю отображается сообщение: «Оплата прошла успешно».

![red1](https://github.com/user-attachments/assets/2ff2e9d8-de57-4621-adf3-d185041abf98)

Структура проекта

  - main.py — основной файл для запуска микросервисов.

  - web_interface.py — файл для инициализации веб-интерфейса.

  - services/validation_service.py — сервис валидации.

  - services/fraud_detection_service.py — сервис для проверки на мошенничество.

  - services/logging_service.py — сервис логирования.

  - services/valute_convertor_service.py — сервис конвертации валют.

  - db.py — файл для инициализации базы данных.
  
  - container_setup.py — скрипт для настройки Docker-контейнеров для Kafka и Redis.
