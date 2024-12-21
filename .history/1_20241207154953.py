import pandas as pd

# Замените путь к файлу на актуальный путь к вашему .csv файлу
file_path = '/home/sexxlexx/Desktop/SKILL/dst-3.0_16_1_hh_database.csv'

# Чтение данных с указанием разделителя ";"
df = pd.read_csv(file_path, sep=";")

# Список всех возможных категорий для «Занятость» и «График»
employment_categories = ['полная занятость', 'частичная занятость', 'проектная работа', 'волонтёрство', 'стажировка']
schedule_categories = ['полный день', 'сменный график', 'гибкий график', 'удаленная работа', 'вахтовый метод']

# Функция для применения One Hot Encoding с улучшенной логикой
def create_one_hot_columns(df, column_name, categories):
    for category in categories:
        # Применяем векторизованный метод, чтобы ускорить обработку
        df[f'{column_name}_{category}'] = df[column_name].str.contains(category, na=False)
    return df

# Применяем One Hot Encoding для «Занятость» и «График»
df = create_one_hot_columns(df, 'Занятость', employment_categories)
df = create_one_hot_columns(df, 'График', schedule_categories)

# Удаляем исходные столбцы «Занятость» и «График»
df = df.drop(['Занятость', 'График'], axis=1)

# Применяем фильтрацию для подсчёта нужных комбинаций
project_and_volunteer_count = df[(df['Занятость_проектная работа']) & (df['Занятость_волонтёрство'])].shape[0]
shift_and_flexible_count = df[(df['График_вахтовый метод']) & (df['График_гибкий график'])].shape[0]

# Выводим результаты
print(f"Количество людей, которые ищут проектную работу и волонтёрство: {project_and_volunteer_count}")
print(f"Количество людей, которые хотят работать вахтовым методом и с гибким графиком: {shift_and_flexible_count}")

# Если нужно, выводим обновлённый DataFrame
# print(df)
