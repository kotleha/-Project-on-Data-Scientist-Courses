import pandas as pd
import re

# Замените путь к файлу на актуальный путь к вашему .csv файлу
file_path = '/home/sexxlexx/Desktop/SKILL/dst-3.0_16_1_hh_database.csv'

# Чтение данных с указанием разделителя ";"
df = pd.read_csv(file_path, sep=";")

# Функция для извлечения города, готовности к переезду и командировкам
def extract_features(value):
    # Разбиение строки с использованием регулярных выражений
    parts = re.split(r'\s*,\s*', value)
    
    # 1. Готовность к переезду
    relocation_status = False  # По умолчанию False
    for term in ['готов к переезду', 'хочу переехать', 'готова к переезду']:
        if term in parts[1]:
            relocation_status = True
            break
    
    # 2. Готовность к командировкам
    travel_status = False  # По умолчанию False
    for term in ['готов к командировкам', 'готова к командировкам', 'готов к редким командировкам']:
        if term in parts[-1]:
            travel_status = True
            break

    return pd.Series([relocation_status, travel_status])

# Применяем функцию для извлечения признаков
df[['Готовность к переезду', 'Готовность к командировкам']] = df['Город, переезд, командировки'].apply(extract_features)

# Считаем количество соискателей, которые готовы и к переезду, и к командировкам
both_ready_count = df[(df['Готовность к переезду'] == True) & (df['Готовность к командировкам'] == True)].shape[0]

# Считаем общее количество соискателей
total_count = df.shape[0]

# Рассчитываем процент
percentage = (both_ready_count / total_count) * 100

# Округляем до целого
percentage_rounded = round(percentage)

print(f"Процент соискателей, готовых одновременно и к переезду, и к командировкам: {percentage_rounded}%")