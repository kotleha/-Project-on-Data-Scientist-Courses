import pandas as pd
import re

# Замените путь к файлу на актуальный путь к вашему .csv файлу
file_path = '/home/sexxlexx/Desktop/SKILL/dst-3.0_16_1_hh_database.csv'

# Чтение данных с указанием разделителя ";"
df = pd.read_csv(file_path, sep=";")

# Список городов-миллионников
million_cities = ['Новосибирск', 'Екатеринбург', 'Нижний Новгород', 'Казань', 'Челябинск', 
                  'Омск', 'Самара', 'Ростов-на-Дону', 'Уфа', 'Красноярск', 'Пермь', 'Воронеж', 
                  'Волгоград']

# Функция для извлечения города из строки
def extract_city(value):
    # Разбиение строки с использованием регулярных выражений
    parts = re.split(r'\s*,\s*', value)
    city = parts[0].split('(')[0].strip()  # Убираем возможную информацию о области в скобках
    return city

# Применяем функцию для извлечения города
df['Город'] = df['Город, переезд, командировки'].apply(extract_city)

# Считаем, сколько соискателей живут в Санкт-Петербурге
st_petersburg_count = df[df['Город'] == 'Санкт-Петербург'].shape[0]

# Считаем общее количество соискателей
total_count = df.shape[0]

# Рассчитываем процент
percentage = (st_petersburg_count / total_count) * 100

# Округляем до целого
percentage_rounded = round(percentage)

print(f"Процент соискателей, проживающих в Санкт-Петербурге: {percentage_rounded}%")