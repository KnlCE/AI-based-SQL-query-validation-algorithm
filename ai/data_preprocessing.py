import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('sql_errors_dataset.csv')

train, test = train_test_split(df, test_size=0.2, stratify=df['is_valid'], random_state=42)

train.to_csv('data/train.csv', index=False)
test.to_csv('data/test.csv', index=False)
