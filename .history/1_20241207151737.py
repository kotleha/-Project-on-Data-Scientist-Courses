import pandas as pd
import numpy as np
import re

# Замените путь к файлу на актуальный путь к вашему .csv файлу
file_path = '/home/sexxlexx/Desktop/SKILL/dst-3.0_16_1_hh_database.csv'

# Чтение данных с указанием разделителя ";"
df = pd.read_csv(file_path, sep=";")

# Список городов-миллионников
million_cities = ['Новосибирск', 'Екатеринбург', 'Нижний Новгород', 'Казань', 'Челябинск', 
                  'Омск', 'Самара', 'Ростов-на-Дону', 'Уфа', 'Красноярск', 'Пермь', 'Воронеж', 
                  'Волгоград']

# Функция для извлечения города, готовности к переезду и командировкам
def extract_features(value):
    # Разбиение строки с использованием регулярных выражений
    parts = re.split(r'\s*,\s*', value)
    
    # 1. Извлекаем город
    city = parts[0].split('(')[0].strip()  # Убираем возможную информацию о области в скобках
    
    # Определяем категорию города
    if city == 'Москва':
        city_category = 'Москва'
    elif city == 'Санкт-Петербург':
        city_category = 'Санкт-Петербург'
    elif city in million_cities:
        city_category = 'город-миллионник'
    else:
        city_category = 'другие'
    
    # 2. Готовность к переезду
    relocation_status = False  # По умолчанию False
    for term in ['готов к переезду', 'хочу переехать', 'готова к переезду']:
        if term in parts[1]:
            relocation_status = True
            break
    
    # 3. Готовность к командировкам
    travel_status = False  # По умолчанию False
    for term in ['готов к командировкам', 'готова к командировкам', 'готов к редким командировкам']:
        if term in parts[-1]:
            travel_status = True
            break
    
    return pd.Series([city_category, relocation_status, travel_status])

# Применяем функцию для извлечения признаков
df[['Город', 'Готовность к переезду', 'Готовность к командировкам']] = df['Город, переезд, командировки'].apply(extract_features)

# Удаляем столбец «Город, переезд, командировки»
df = df.drop('Город, переезд, командировки', axis=1)

# Выводим результат
print(df.head())
