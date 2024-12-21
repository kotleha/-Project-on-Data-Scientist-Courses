import pandas as pd

# Замените путь к файлу на актуальный путь к вашему .csv файлу
file_path = '/home/sexxlexx/Desktop/SKILL/dst-3.0_16_1_hh_database.csv'

# Чтение данных с указанием разделителя ";"
df = pd.read_csv(file_path, sep=";")

# Преобразование признаков "Занятость" и "График" в One Hot Encoding
# Создаем списки возможных категорий для "Занятость" и "График"
employment_categories = ['полная занятость', 'частичная занятость', 'проектная работа', 'волонтёрство', 'стажировка']
schedule_categories = ['полный день', 'сменный график', 'гибкий график', 'удалённая работа', 'вахтовый метод']

# Функция для применения One Hot Encoding
def apply_one_hot_encoding(df, column_name, categories):
    for category in categories:
        df[category] = df[column_name].apply(lambda x: category in str(x).lower())
    return df

# Применяем One Hot Encoding к столбцам "Занятость" и "График"
df = apply_one_hot_encoding(df, 'Занятость', employment_categories)
df = apply_one_hot_encoding(df, 'График', schedule_categories)

# Удаляем исходные столбцы "Занятость" и "График"
df = df.drop(['Занятость', 'График'], axis=1)

# Ответ на контрольные вопросы:
# Сколько людей ищут проектную работу и волонтёрство (в обоих столбцах стоит True)?
project_volunteer_count = df[(df['проектная работа'] == True) & (df['волонтёрство'] == True)].shape[0]

# Сколько людей хотят работать вахтовым методом и с гибким графиком (в обоих столбцах стоит True)?
shift_vahda_count = df[(df['вахтовый метод'] == True) & (df['гибкий график'] == True)].shape[0]

# Выводим результаты
print(f"Количество людей, ищущих проектную работу и волонтёрство: {project_volunteer_count}")
print(f"Количество людей, ищущих работу вахтовым методом и с гибким графиком: {shift_vahda_count}")
