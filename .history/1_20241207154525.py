import pandas as pd

# Замените путь к файлу на актуальный путь к вашему .csv файлу
file_path = '/home/sexxlexx/Desktop/SKILL/dst-3.0_16_1_hh_database.csv'

# Чтение данных с указанием разделителя ";"
df = pd.read_csv(file_path, sep=";")

# Список всех возможных категорий для «Занятость»
employment_categories = ['полная занятость', 'частичная занятость', 'проектная работа', 'волонтёрство', 'стажировка']
# Список всех возможных категорий для «График»
schedule_categories = ['полный день', 'сменный график', 'гибкий график', 'удаленная работа', 'вахтовый метод']

# Функция для выполнения One Hot Encoding
def create_one_hot_columns(df, column_name, categories):
    for category in categories:
        df[category] = df[column_name].apply(lambda x: category in x if isinstance(x, str) else False)
    return df

# Применяем One Hot Encoding для «Занятость»
df = create_one_hot_columns(df, 'Занятость', employment_categories)

# Применяем One Hot Encoding для «График»
df = create_one_hot_columns(df, 'График', schedule_categories)

# Удаляем исходные столбцы «Занятость» и «График»
df = df.drop(['Занятость', 'График'], axis=1)

# Преобразуем значения в True/False для корректного сравнения
for category in employment_categories + schedule_categories:
    df[category] = df[category].astype(bool)

# Подсчитываем количество людей, которые ищут проектную работу и волонтёрство (оба столбца True)
project_and_volunteer = df[(df['проектная работа'] == True) & (df['волонтёрство'] == True)]

# Подсчитываем количество людей, которые хотят работать вахтовым методом и с гибким графиком (оба столбца True)
shift_and_flexible = df[(df['вахтовый метод'] == True) & (df['гибкий график'] == True)]

# Выводим ответы
print(f"Количество людей, которые ищут проектную работу и волонтёрство: {len(project_and_volunteer)}")
print(f"Количество людей, которые хотят работать вахтовым методом и с гибким графиком: {len(shift_and_flexible)}")
