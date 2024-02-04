import numpy as np
import sqlite3

romanian_texts = {}
moldavian_texts = {}

conn = sqlite3.connect('news.db')
c = conn.cursor()

c.execute('SELECT * FROM romania')
rows = c.fetchall()
for row in rows:
    if row[4] not in romanian_texts:
        romanian_texts[row[4]] = []
    romanian_texts[row[4]].append(row[5])
    
c.execute('SELECT * FROM moldova')
rows = c.fetchall()
for row in rows:
    if row[4] not in moldavian_texts:
        moldavian_texts[row[4]] = []
    moldavian_texts[row[4]].append(row[5])

conn.close()

# Stratified split for country and category
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit

# For each key in the dictionary, split the values into train and test
# Train classificator on context independent features
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
# ssss = []
all_texts = {}

for key in romanian_texts:
    all_texts[key + "_romana"] = romanian_texts[key]
    
for key in moldavian_texts:
    all_texts[key + "_moldova"] = moldavian_texts[key]

X = []
y = []
for key in all_texts:
    X.extend(all_texts[key])
    y.extend([key]*len(all_texts[key]))
    
X = np.array(X)
y = np.array(y)


    
sss = StratifiedShuffleSplit(n_splits=3, test_size=0.33, random_state=11)
for train_index, test_index in sss.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    
    text_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB()),
    ])
    
    text_clf.fit(X_train, y_train)
    predicted = text_clf.predict(X_test)
    print(classification_report(y_test, predicted))

    parameters = {
        'vect__ngram_range': [(1, 1), (1, 2)],
        'tfidf__use_idf': (True, False),
        'clf__alpha': (1e-2, 1e-3),
    }
    gs_clf = GridSearchCV(text_clf, parameters, cv=5, n_jobs=-1)
    gs_clf = gs_clf.fit(X_train, y_train)
    print(gs_clf.best_score_)
    print(gs_clf.best_params_)
    predicted = gs_clf.predict(X_test)
    print(classification_report(y_test, predicted))
    print(gs_clf.best_estimator_)
    print(gs_clf.best_estimator_.score(X_test, y_test))
    print(gs_clf.best_estimator_.score(X_train, y_train ))