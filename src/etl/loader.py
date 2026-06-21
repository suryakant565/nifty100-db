import pandas as pd


def load_excel(path):
    df = pd.read_excel(path, header=1)
    return df