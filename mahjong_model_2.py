import pandas as pd
import plotly.express as px
from scipy import stats
import math

df = pd.read_csv(r'C:\Users\Flora Zhu\Downloads\cs109proj\fullhands_train.csv')
df_test = pd.read_csv(r'C:\Users\Flora Zhu\Downloads\cs109proj\fullhands_test.csv')

index = list(range(100000))
index2 = list(range(25000))
df['index'] = index
df = df.set_index('index').drop(columns = ['Unnamed: 0', 'flower'])
df_test['index'] = index2
df_test = df_test.set_index('index').drop(columns = 'Unnamed: 0')

# sklearn
X_train = df.drop(columns = ['score'])
y_train = df['score']
X_test = df_test.drop(columns = 'score')
y_test = df_test['score']

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression

pipeline = make_pipeline(StandardScaler(), LinearRegression()) # i scaled the data first
pipeline.fit(X_train, y_train)
y_test_ = pipeline.predict(X_test)

from sklearn.metrics import root_mean_squared_error
print(root_mean_squared_error(y_test, y_test_))