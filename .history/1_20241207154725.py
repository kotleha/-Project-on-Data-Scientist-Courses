import pandas as pd

# Замените путь к файлу на актуальный путь к вашему .csv файлу
file_path = '/home/sexxlexx/Desktop/SKILL/dst-3.0_16_1_hh_database.csv'

# Чтение данных с указанием разделителя ";"
df = pd.read_csv(file_path, sep=";")

# Списки категорий для «Занятость» и «График»
employment_categories = ['полная занятость', 'частичная занятость', 'проектная работа', 'волонтёрство', 'стажировка']
schedule_categories = ['полный день', 'сменный график', 'гибкий график', 'удаленная работа', 'вахтовый метод']

# Функция для применения One Hot Encoding к столбцам
def apply_one_hot_encoding(df, column_name, categories):
    for category in categories:
        df[f'{column_name}_{category}'] = df[column_name].apply(lambda x: category in x if isinstance(x, str) else False)
    return df

# Применяем One Hot Encoding для «Занятость» и «График»
df = apply_one_hot_encoding(df, 'Занятость', employment_categories)
df = apply_one_hot_encoding(df, 'График', schedule_categories)

# Удаляем исходные столбцы «Занятость» и «График»
df = df.drop(['Занятость', 'График'], axis=1)

# Подсчёт количества людей, которые ищут проектную работу и волонтёрство
project_volunteer_filter = df['Занятость_проектная работа'] & df['Занятость_волонтёрство']
project_and_volunteer_count = df[project_volunteer_filter].shape[0]

# Подсчёт количества людей, которые хотят работать вахтовым методом и с гибким графиком
shift_flexible_filter = df['График_вахтовый метод'] & df['График_гибкий график']
shift_and_flexible_count = df[shift_flexible_filter].shape[0]

# Выводим ответы
print(f"Количество людей, которые ищут проектную работу и волонтёрство: {project_and_volunteer_count}")
print(f"Количество людей, которые хотят работать вахтовым методом и с гибким графиком: {shift_and_flexible_count}")
