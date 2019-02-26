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
new_index = ["M1"]

measles_1.columns = measles_1.columns.set_levels(np.array(new_index), level=0)

measles_2 = pd.read_csv("./data/MCV2.csv", header=[0, 1], index_col=0)

measles_combined = measles_1.join(measles_2)
