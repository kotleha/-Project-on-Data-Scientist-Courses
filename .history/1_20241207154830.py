import pandas as pd

# Замените путь к файлу на актуальный путь к вашему .csv файлу
file_path = '/home/sexxlexx/Desktop/SKILL/dst-3.0_16_1_hh_database.csv'

# Чтение данных с указанием разделителя ";"
df = pd.read_csv(file_path, sep=";")

employments = ['полная занятость', 'частичная занятость',
              'проектная работа', 'волонтерство', 'стажировка']
charts = ['полный день', 'сменный график', 
         'гибкий график', 'удаленная работа',
         'вахтовый метод']
for employment, chart in zip(employments, charts):
    df[employment] = df['Занятость'].apply(lambda x: employment in x)
    df[chart] = df['График'].apply(lambda x: chart in x)
df = df.drop('Занятость', axis=1)
df = df.drop('График', axis=1)
print(df[df['проектная работа'] & df['волонтерство']].shape[0])
print(df[df['вахтовый метод'] & df['гибкий график']].shape[0])