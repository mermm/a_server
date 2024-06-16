import redis
import random
from datetime import datetime, timedelta

# Подключение к Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Примерные данные
severity_levels = ["INFO", "WARNING", "ERROR"]
descriptions = [
    "User logged in",
    "User logged out",
    "File uploaded",
    "File deleted",
    "Error while processing request",
    "Warning: Disk space low"
]

# Функция для создания случайной даты в диапазоне
def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

# Генерация логов
num_logs = 100  # Количество логов для добавления
start_date = datetime.now() - timedelta(days=30)  # Начало диапазона (30 дней назад)
end_date = datetime.now()  # Конец диапазона (сегодня)

for i in range(num_logs):
    log_id = i + 1
    severity = random.choice(severity_levels)
    date = random_date(start_date, end_date).strftime('%Y-%m-%d %H:%M:%S')
    description = random.choice(descriptions)
    
    log_entry = {
        "id": log_id,
        "severity": severity,
        "date": date,
        "description": description
    }
    
    # Сохранение лога в Redis (в данном примере используется хеш)
    r.hmset(f"log:{log_id}", log_entry)

print(f"{num_logs} logs have been added to Redis.")
