import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

measles_1 = pd.read_csv("./data/WHS8_110.csv")
# Column name incorrect
print(measles_1)

measles_1 = pd.read_csv("./data/WHS8_110.csv", header=[0, 1])
# Multilevel column name

measles_1 = pd.read_csv("./data/WHS8_110.csv", header=[0, 1], index_col=0)
# Indexed at country name

print(measles_1.columns)
print(measles_1["Measles-containing-vaccine first-dose (MCV1) immunization coverage among 1-year-olds (%)"])
# Too long name

# Index type is immutable so we can't just change the value within the index
# Index have to be unique

measles_1.columns = measles_1.columns.set_levels(["M1"], level=0)
measles_1.columns = measles_1.columns.set_levels([int(i.strip()) for i in measles_1["M1"].columns], level=1)
measles_1 = measles_1.stack()
print(measles_1)

measles_1.index.names = ["Country", "Year"]

long_measles_1 = measles_1.reset_index()

measles_2 = pd.read_csv("./data/MCV2.csv", header=[0, 1], index_col=0)

measles_combined = measles_1.join(measles_2)

def replace(x):
    if type(x) is str:
        if " " in x:
            return x.split(" ")[0]
        else:
            return x
    else:
        return x

measles_1.applym(lambda x: x if type(x) is not str else (x.split()[0] if " " in x else x))