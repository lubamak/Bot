
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline



data = pd.read_csv('negative.csv', encoding='utf-8', error_bad_lines=False)
data["label"] = -1
columns = ['text', 'label']
data_n = pd.DataFrame(data, columns=columns)

data = pd.read_csv('positive.csv', encoding='utf-8', error_bad_lines=False)
data["label"] = 1
data_p = pd.DataFrame(data, columns=columns)

df = data_n.append(data_p)

df = df.apply(lambda x: x.astype(str).str.lower())
df['label'] = pd.to_numeric(df['label'])

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df['text'].values, df['label'].values, test_size=0.33, random_state=42)

pipeline = Pipeline([("vectorizer", CountVectorizer()),("algo", LogisticRegression(penalty='l1', C=17))])
pipeline.fit(X_train, y_train)


from sklearn.externals import joblib
filename = 'classifier.joblib.pkl'
_ = joblib.dump(pipeline, filename, compress=9)
pipeline = joblib.load('classifier.joblib.pkl')




