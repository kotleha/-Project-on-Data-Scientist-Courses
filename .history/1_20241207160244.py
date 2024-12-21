import pandas as pd

# Загрузим данные
resume_file_path = '/home/sexxlexx/Desktop/SKILL/dst-3.0_16_1_hh_database.csv'
exchange_file_path = '/home/sexxlexx/Desktop/SKILL/ExchangeRates.csv'

# Чтение данных
df_resume = pd.read_csv(resume_file_path, sep=";")
df_exchange = pd.read_csv(exchange_file_path)

# Убираем лишние пробелы и преобразуем столбцы с датами
df_resume['Обновление резюме'] = pd.to_datetime(df_resume['Обновление резюме'].str.strip(), errors='coerce').dt.date
df_exchange['date'] = pd.to_datetime(df_exchange['date'], format='%d/%m/%y').dt.date

# Сопоставление валюты
currency_mapping = {
    'грн': 'UAH',
    'USD': 'USD',
    'EUR': 'EUR',
    'белруб': 'BYN',
    'KGS': 'KGS',
    'сум': 'UZS',
    'AZN': 'AZN',
    'KZT': 'KZT'
}

# Функция для извлечения суммы и валюты из столбца "ЗП"
def extract_salary_and_currency(salary_str):
    salary_str = salary_str.lower()
    for currency, iso_code in currency_mapping.items():
        if currency in salary_str:
            amount = int(''.join(filter(str.isdigit, salary_str)))
            return amount, iso_code
    return None, None

# Применяем функцию к столбцу "ЗП"
df_resume[['ЗП_сумма', 'Валюта']] = df_resume['ЗП'].apply(lambda x: pd.Series(extract_salary_and_currency(x)))

# Присоединяем таблицу с курсами валют
df_merged = pd.merge(df_resume, df_exchange[['date', 'currency', 'close', 'proportion']], 
                     left_on=['Обновление резюме', 'Валюта'], 
                     right_on=['date', 'currency'], 
                     how='left')

# Рассчитываем ЗП в рублях
df_merged['ЗП (руб)'] = df_merged['ЗП_сумма'] * df_merged['close'] / df_merged['proportion']

# Удаляем лишние столбцы
df_merged = df_merged.drop(columns=['
