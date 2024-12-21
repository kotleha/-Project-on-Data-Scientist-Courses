import pandas as pd

# Замените путь к файлу на актуальный путь к вашему .csv файлу
file_path = '/home/sexxlexx/Desktop/SKILL/dst-3.0_16_1_hh_database.csv'

# Чтение данных с указанием разделителя ";"
df = pd.read_csv(file_path, sep=";")

# Списки категорий для «Занятость» и «График»
employments = ['полная занятость', 'частичная занятость', 'проектная работа', 'волонтёрство', 'стажировка']
charts = ['полный день', 'сменный график', 'гибкий график', 'удаленная работа', 'вахтовый метод']

# Создание признаков-мигалок для «Занятость»
for employment in employments:
    df[employment] = df['Занятость'].apply(lambda x: employment in x if isinstance(x, str) else False)

# Создание признаков-мигалок для «График»
for chart in charts:
    df[chart] = df['График'].apply(lambda x: chart in x if isinstance(x, str) else False)

# Удаляем исходные столбцы «Занятость» и «График»
df = df.drop(['Занятость', 'График'], axis=1)

# Проверяем результат
print("Пример данных после преобразования:")
print(df.head())
