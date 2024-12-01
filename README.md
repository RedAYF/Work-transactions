# BUD-transactions


## Мы все любим пиво, но очень обожаем его - наш любимый BUD



### Представители любителя пиво BUD:

![image](https://github.com/user-attachments/assets/cc2b7cba-ac9d-4e9a-83a5-802585b61e12)

![image](https://github.com/user-attachments/assets/c7698257-2937-4c9e-9efd-1471e2647620)

![image](https://github.com/user-attachments/assets/b1248a54-c5b4-4f12-8edf-9c0dac23c07f)


### Процесс
1. Пользователь вводит сумму на пиво и выбирает валюту в веб-интерфейсе, затем нажимает кнопку «Оплатить».

![Снимок экрана 2024-12-01 170933](https://github.com/user-attachments/assets/094fbae7-dab4-49d3-b2cf-e441cdc47835)

2. Транзакция проходит через несколько этапов:

 - Validation Service - проверяет корректность данных транзакции.
  
 - Valute Convertor Service - преобразует сумму в требуемую валюту.
  
 - Fraud Detection Service - анализирует транзакцию на предмет мошеннических действий.
  
 - Logging Service - сохраняет информацию о транзакции в базе данных.

3. После успешного завершения всех этапов пользователю отображается сообщение: «Оплата прошла успешно».

![Снимок экрана 2024-12-01 172415](https://github.com/user-attachments/assets/50f5e38c-7eb2-45ca-992c-bcc087f42fd1)

Структура проекта

  - main.py — основной файл для запуска микросервисов.

  - web_interface.py — файл для инициализации веб-интерфейса.

  - services/validation_service.py — сервис валидации.

  - services/fraud_detection_service.py — сервис для проверки на мошенничество.

  - services/logging_service.py — сервис логирования.

  - services/valute_convertor_service.py — сервис конвертации валют.

  - db.py — файл для инициализации базы данных.
  
  - container_setup.py — скрипт для настройки Docker-контейнеров для Kafka и Redis.
