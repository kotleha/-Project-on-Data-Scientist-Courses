import pandas as pd

# Замените путь к файлу на актуальный путь к вашему .csv файлу
file_path = '/home/sexxlexx/Desktop/SKILL/dst-3.0_16_1_hh_database.csv'

# Чтение данных с указанием разделителя ";"
df = pd.read_csv(file_path, sep=";")

# Функция для извлечения города
def get_city(arg):
    million_cities = ['Новосибирск', 'Екатеринбург', 'Нижний Новгород', 
                      'Казань', 'Челябинск', 'Омск', 'Самара', 'Ростов-на-Дону', 
                      'Уфа', 'Красноярск', 'Пермь', 'Воронеж', 'Волгоград']
    
    city = arg.split(' , ')[0]
    
    # Определяем город
    if (city == 'Москва') or (city == 'Санкт-Петербург'):
        return city
    elif city in million_cities:
        return 'город миллионник'
    else:
        return 'другие'

# Функция для определения готовности к переезду
def get_ready_to_move(arg):
    if ('не готов к переезду' in arg) or ('не готова к переезду' in arg):
        return False
    elif 'хочу' in arg:
        return True
    else:
        return True

# Функция для определения готовности к командировкам
def get_ready_for_bisiness_trips(arg):
    if ('командировка' in arg):
        if ('не готов к командировкам' in arg) or ('не готова к командировкам' in arg):
            return False
        else: 
            return True
    else:
        return False

# Применяем функции для создания новых столбцов
df['Город'] = df['Город, переезд, командировки'].apply(get_city)
df['Готовность к переезду'] = df['Город, переезд, командировки'].apply(get_ready_to_move)
df['Готовность к командировкам'] = df['Город, переезд, командировки'].apply(get_ready_for_bisiness_trips)

# Удаляем исходный столбец
df = df.drop('Город, переезд, командировки', axis=1)

# Считаем процент соискателей из Санкт-Петербурга
st_petersburg_percentage = round(df['Город'].value_counts(normalize=True).get('Санкт-Петербург', 0) * 100)

# Считаем процент соискателей, готовых одновременно и к переезду, и к командировкам
ready_for_both_percentage = round(
    df[(df['Готовность к переезду'] == True) & (df['Готовность к командировкам'] == True)].shape[0] 
    / df.shape[0] * 100
)

# Выводим результаты
print(f"Процент соискателей, живущих в Санкт-Петербурге: {st_petersburg_percentage}%")
print(f"Процент соискателей, готовых одновременно к переезду и командировкам: {ready_for_both_percentage}%")
# Выводим результат
print(df.head())