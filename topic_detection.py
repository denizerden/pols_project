
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
import boto3
import awswrangler as wr

client = boto3.client('athena')


df_category = pd.read_csv("./home/ec2-user/7allV03.csv")
stop_words = pd.read_csv("./home/ec2-user/stop_words.txt",header=None)
stop_words = stop_words.iloc[:, 0].tolist()
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='utf-8', ngram_range=(1, 2), stop_words=stop_words)
features = tfidf.fit_transform(df_category.text).toarray()
labels = df_category.category
features.shape

df_category['category'] = df_category['category'].astype('category')
# Assigning numerical values and storing in another column
df_category['category_id'] = df_category['category'].cat.codes


model = LinearSVC()
X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, df_category.index, test_size=0.33, random_state=0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

df = wr.pandas.read_sql_athena(
    sql='SELECT DISTINCT * FROM "db"."news_data" ',
    database="database"
)

print(df.head())

X = df["text"]
y_hats = model.predict(X)
y_test = pd.DataFrame(y_hats, columns="topic")


df_out = pd.merge(df,y_hats,how = 'left',left_index = True, right_index = True)