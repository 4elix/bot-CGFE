import pandas as pd

df1 = pd.read_excel('Sales_Data.xlsx')

# group1 = df.groupby('Region')['Quantity'].sum().reset_index()
# print(group1)




def manager_groupby(df, *args):
    try:
        col1, col2, tg = args

        result = None
        if tg == 'Сумма':
            result = df.groupby(col1)[col2].sum().reset_index()
        elif tg == 'Среднее':
            result = df.groupby(col1)[col2].mean().reset_index()
        elif tg == 'Количество':
            result = df.groupby(col1)[col2].count().reset_index()

        return result
    except Exception as error:
        print(error)
        return 404

# print(manager_groupby(df1, 'Region', 'Quantity', 'Количество'))

# import seaborn as sns
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
#
# # Установка стиля
# sns.set(style="whitegrid")
#
# # Создание данных
# np.random.seed(42)
# df = pd.DataFrame({
#     'category': np.random.choice(['A', 'B', 'C'], size=100),
#     'value': np.random.normal(loc=10, scale=5, size=100),
#     'value2': np.random.normal(loc=15, scale=3, size=100),
#     'time': pd.date_range(start='2023-01-01', periods=100)
# })
#
#
# # sns.histplot() гистограмма
# # Размер выборки	Рекомендации по bins
# # < 50	            5–10
# # 50–100	        10–20
# # 100–1000	        20–40
# # > 1000	        40+ или автоматический


# plt.figure(figsize=(6, 4))
# sns.histplot(data=df, x='value', bins=20, kde=True)
# plt.title('Histplot: Распределение переменной value')
# plt.show()
#
# # sns.boxplot() коробчатая диаграмма
# plt.figure(figsize=(6, 4))
# sns.boxplot(data=df, x='category', y='value')
# plt.title('Boxplot: Распределение value по категориям')
# plt.show()
#
# # sns.barplot()  столбчатая диаграмма
# plt.figure(figsize=(6, 4))
# sns.barplot(data=df, x='category', y='value', ci=None)
# plt.title('Barplot: Среднее значение value по категориям')
# plt.show()
#
# # sns.lineplot()  линейный график
# plt.figure(figsize=(8, 4))
# sns.lineplot(data=df, x='time', y='value')
# plt.title('Lineplot: Значения value во времени')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()
#
# # sns.scatterplot()  диаграмма рассеяния
# plt.figure(figsize=(6, 4))
# sns.scatterplot(data=df, x='value', y='value2', hue='category')
# plt.title('Scatterplot: Связь между value и value2')
# plt.show()
#

a = None

if a is not None:
    print('as')
else:
    print('zxc')