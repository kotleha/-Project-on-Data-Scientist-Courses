import pandas as pd
import re

# Замените путь к файлу на актуальный путь к вашему .csv файлу
file_path = '/home/sexxlexx/Desktop/SKILL/dst-3.0_16_1_hh_database.csv'

# Чтение данных с указанием разделителя ";"
df = pd.read_csv(file_path, sep=";")

# Подсчитываем количество соискателей из Санкт-Петербурга
spb_count = df[df['Город'] == 'Санкт-Петербург'].shape[0]

# Подсчитываем общее количество соискателей
total_count = df.shape[0]

# Рассчитываем процент соискателей из Санкт-Петербурга
percentage_spb = (spb_count / total_count) * 100

# Округляем результат до целого
percentage_spb = round(percentage_spb)

# Выводим результат
print(f"Процент соискателей из Санкт-Петербурга: {percentage_spb}%")