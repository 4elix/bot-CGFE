import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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
