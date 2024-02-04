import numpy as np
import pandas as pd
import glob

# Romania
romanian_dataset = []

romanian_files = glob('datasets/romania/*.csv')

for file in romanian_files:
    df = pd.read_csv(file, sep=';')
    romanian_dataset.append(df)