import pandas as pd

# Путь к файлам
resume_file_path = '/home/sexlexx/Desktop/-Project-on-Data-Scientist-Courses/dst-3.0_16_1_hh_database.csv'
exchange_file_path = '/home/sexlexx/Desktop/-Project-on-Data-Scientist-Courses/ExchangeRates.csv'

# Загрузка данных
df = pd.read_csv(resume_file_path, sep=";")
df_exchange = pd.read_csv(exchange_file_path)

# Задача 1: Обработка столбца "Пол, возраст"
def extract_gender(value):
    if 'Мужчина' in value:
        return 'М'
    elif 'Женщина' in value:
        return 'Ж'
    return None

def extract_age(value):
    try:
        return int(value.split(',')[1].strip().split(' ')[0])
    except:
        return None

df['Пол'] = df['Пол, возраст'].apply(extract_gender)
df['Возраст'] = df['Пол, возраст'].apply(extract_age)
df.drop(columns=['Пол, возраст'], inplace=True)

# Задача 2: Обработка столбца "Образование и ВУЗ"
def classify_education(education_str):
    if pd.isna(education_str) or not isinstance(education_str, str):
        return 'неизвестно'
    first_words = ' '.join(education_str.split()[:3])
    if 'Высшее образование' in first_words:
        return 'высшее'
    elif 'Неоконченное высшее образование' in first_words:
        return 'неоконченное высшее'
    elif 'Среднее специальное образование' in first_words:
        return 'среднее специальное'
    elif 'Среднее образование' in first_words:
        return 'среднее'
    return 'неизвестно'

df['Образование'] = df['Образование и ВУЗ'].apply(classify_education)
df.drop(columns=['Образование и ВУЗ'], inplace=True)

# Задача 3: Обработка столбца "Опыт работы"
def get_experience(arg):
    if pd.isna(arg) or arg == 'Не указано':
        return None
    year_words = ['год', 'года', 'лет']
    month_words = ['месяц', 'месяца', 'месяцев']
    arg_splitted = arg.split(' ')
    years = 0
    months = 0
    for index, item in enumerate(arg_splitted):
        if item in year_words:
            years = int(arg_splitted[index - 1])
        if item in month_words:
            months = int(arg_splitted[index - 1])
    return years * 12 + months

df['Опыт работы (месяц)'] = df['Опыт работы'].apply(get_experience)
df.drop(columns=['Опыт работы'], inplace=True)

# Задача 4: Обработка столбца "Город, переезд, командировки"
million_cities = ['Новосибирск', 'Екатеринбург', 'Нижний Новгород', 'Казань', 'Челябинск',
                  'Омск', 'Самара', 'Ростов-на-Дону', 'Уфа', 'Красноярск', 'Пермь', 'Воронеж', 'Волгоград']

def get_city(value):
    city = value.split(' , ')[0]
    if city in ['Москва', 'Санкт-Петербург']:
        return city
    elif city in million_cities:
        return 'город-миллионник'
    else:
        return 'другие'

def get_ready_to_move(value):
    return 'готов' in value.lower()

def get_ready_for_business_trips(value):
    if 'командировка' in value.lower():
        return 'не готов' not in value.lower()
    return False

df['Город'] = df['Город, переезд, командировки'].apply(get_city)
df['Готовность к переезду'] = df['Город, переезд, командировки'].apply(get_ready_to_move)
df['Готовность к командировкам'] = df['Город, переезд, командировки'].apply(get_ready_for_business_trips)
df.drop(columns=['Город, переезд, командировки'], inplace=True)

# Задача 5: Обработка столбца "ЗП"
def parse_salary(salary):
    if pd.isna(salary):
        return pd.Series([None, None])
    try:
        amount, currency = salary.split(' ')
        return pd.Series([float(amount.replace('\u202f', '').replace(',', '')), currency])
    except:
        return pd.Series([None, None])

df[['ЗП (сумма)', 'Валюта']] = df['ЗП'].apply(parse_salary)

currency_mapping = {
    'руб.': ('RUB', 1),
    'грн.': ('UAH', 10),
    'USD': ('USD', 1),
    'EUR': ('EUR', 1),
    'бел.руб.': ('BYN', 1),
    'KGS': ('KGS', 10),
    'сум': ('UZS', 10000),
    'AZN': ('AZN', 1),
    'KZT': ('KZT', 100)
}

df['ISO Валюта'] = df['Валюта'].map(lambda x: currency_mapping[x][0] if x in currency_mapping else None)
df['Пропорция'] = df['Валюта'].map(lambda x: currency_mapping[x][1] if x in currency_mapping else None)

df_exchange['date'] = pd.to_datetime(df_exchange['date'], format='%d/%m/%y').dt.date
df['Обновление резюме'] = pd.to_datetime(df['Обновление резюме'], format='%d.%m.%Y %H:%M').dt.date

df = pd.merge(
    df,
    df_exchange,
    how='left',
    left_on=['Обновление резюме', 'ISO Валюта'],
    right_on=['date', 'currency']
)

df['close'] = df['close'].fillna(1)
df['ЗП (руб)'] = (df['ЗП (сумма)'] * df['close'] / df['Пропорция']).round(2)
df.drop(columns=['ЗП', 'ЗП (сумма)', 'Валюта', 'ISO Валюта', 'Пропорция', 'date', 'currency', 'close'], inplace=True)

# Итоговая проверка
print(df.info())
