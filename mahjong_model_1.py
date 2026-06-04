import pandas as pd
import plotly.express as px
from scipy import stats
import math

df = pd.read_csv(r'C:\Users\Flora Zhu\Downloads\cs109proj\mahjong_hands_train.csv')
df_test = pd.read_csv(r'C:\Users\Flora Zhu\Downloads\cs109proj\mahjong_hands_test.csv')

# generate graph
counts = df.value_counts('score').sort_index()
pmf = pd.DataFrame(counts)['count'] / 100000
#px.line(pmf, title = 'Starting Hand Efficiency Distribution', labels = ['score', 'count']).show()

# sklearn
X_train = df[['flowernum', 'pairs', 'pongs', 'kongs', 'halfchi', 'suites missing']]
y_train = df['score']
X_test = df_test[['flowernum', 'pairs', 'pongs', 'kongs', 'halfchi', 'suites missing']]
y_test = df_test['score']

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression

pipeline = make_pipeline(StandardScaler(), LinearRegression()) # i scaled the data first
pipeline.fit(X_train, y_train)
y_test_ = pipeline.predict(X_test)

from sklearn.metrics import root_mean_squared_error
print(root_mean_squared_error(y_test, y_test_))