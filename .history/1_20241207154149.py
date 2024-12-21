import pandas as pd

# Замените путь к файлу на актуальный путь к вашему .csv файлу
file_path = '/home/sexxlexx/Desktop/SKILL/dst-3.0_16_1_hh_database.csv'

# Чтение данных с указанием разделителя ";"
df = pd.read_csv(file_path, sep=";")

# Список всех возможных категорий для «Занятость» и «График»
employment_categories = ['полная занятость', 'частичная занятость', 'проектная работа', 'волонтёрство', 'стажировка']
schedule_categories = ['полный день', 'сменный график', 'гибкий график', 'удаленная работа', 'вахтовый метод']

# Функция для выполнения One Hot Encoding
def create_one_hot_columns(df, column_name, categories):
    for category in categories:
        df[category] = df[column_name].apply(lambda x: category in str(x))
    return df

# Применяем One Hot Encoding для «Занятость»
df = create_one_hot_columns(df, 'Занятость', employment_categories)

# Применяем One Hot Encoding для «График»
df = create_one_hot_columns(df, 'График', schedule_categories)

# Удаляем исходные столбцы «Занятость» и «График»
df = df.drop(['Занятость', 'График'], axis=1)

# Пример сложного анализа: подытожим по выбранным категориям
def count_condition(df, condition):
    return len(df[condition])

# Подсчитаем людей, которые ищут проектную работу и волонтёрство (оба столбца True)
project_and_volunteer = count_condition(df, (df['проектная работа'] == True) & (df['волонтёрство'] == True))

# Подсчитаем людей, которые хотят работать вахтовым методом и с гибким графиком (оба столбца True)
shift_and_flexible = count_condition(df, (df['вахтовый метод'] == True) & (df['гибкий график'] == True))

# Выводим результаты
print(f"Количество людей, которые ищут проектную работу и волонтёрство: {project_and_volunteer}")
print(f"Количество людей, которые хотят работать вахтовым методом и с гибким графиком: {shift_and_flexible}")

# Сохраняем обновлённый DataFrame в новый CSV файл
df.to_csv('/home/sexxlexx/Desktop/SKILL/processed_hh_database.csv', index=False)