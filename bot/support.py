import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

list_type_graphic = [
    'Гистограмма',
    'Коробчатая диаграмма',
    'Столбчатая диаграмма',
    'Линейный график',
    'Диаграмма рассеяния (точечная диаграмма)',
]


async def manager_groupby(df, *args):
    col1, col2, tg = args

    try:
        result = None
        if tg == 'Сумма':
            result = df.groupby(col1)[col2].sum().reset_index()
        elif tg == 'Среднее':
            result = df.groupby(col1)[col2].mean().reset_index()
        elif tg == 'Количество':
            result = df.groupby(col1)[col2].count().reset_index()

        return result
    except KeyError as error:
        return None


def manager_graphic(type_graphic: str):
    pass


def create_graphic_histogram(df, x, title):
    sns.histplot(data=df, x=x, bins=20, kde=True)
    plt.title(title)
    plt.show()


def create_graphic_box(df, x, y, title):
    sns.boxplot(data=df, x=x, y=y)
    plt.title(title)
    plt.show()


def create_graphic_bar(df, x, y, title):
    sns.barplot(data=df, x=x, y=y, ci=None)
    plt.title(title)
    plt.show()


def create_graphic_line(df, x, y, title):
    sns.lineplot(data=df, x=x, y=y)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def create_graphic_scatter(df, x, y, title):
    sns.scatterplot(data=df, x=x, y=y)
    plt.title(title)
    plt.show()
