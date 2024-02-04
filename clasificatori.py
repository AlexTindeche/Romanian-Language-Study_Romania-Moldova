import numpy as np
import sqlite3
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from stop_words import get_stop_words
import shap


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
    text = ''
    if len(row[5]) > 10000:
        text = row[5][:10000]
    else:
        text = row[5]
    if row[4] not in moldavian_texts:
        moldavian_texts[row[4]] = []
        
    moldavian_texts[row[4]].append(text)

conn.close()

all_texts = {"romana": [], "moldova": []}

for key in romanian_texts:
    all_texts["romana"].extend(romanian_texts[key])


    
for key in moldavian_texts:
    all_texts["moldova"].extend(moldavian_texts[key])
    

X = []
y = []
for key in all_texts:
    X.extend(all_texts[key])
    y.extend([key]*len(all_texts[key]))
    
X = np.array(X)
y = np.array(y)

    
sss = StratifiedShuffleSplit(n_splits=3, test_size=0.1, random_state=11)
text_clf = Pipeline(steps=[
        ('tfidf', TfidfVectorizer(max_df=0.5, max_features=100000, min_df=0.2, stop_words=get_stop_words('ro'))),
        ('clf', MultinomialNB()),
    ], verbose=True)
parameters = {
    'tfidf__ngram_range': [(2, 3)],
    'tfidf__use_idf': (True, False),
    'clf__alpha': (0.01, 0.001),
}
gs_clf = GridSearchCV(text_clf, parameters, cv=5, n_jobs=-1, verbose=1)

scores = []
gs_scores = []

for train_index, test_index in sss.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]   
    
    text_clf = text_clf.fit(X_train, y_train)
    scores.append(text_clf.score(X_test, y_test))
    
    gs_clf = gs_clf.fit(X_train, y_train)
    gs_scores.append(gs_clf.score(X_test, y_test))
    
print("Mean score: ", np.mean(scores))
print("Mean grid search score: ", np.mean(gs_scores))
print("Best parameters: ", gs_clf.best_params_)
print("Best score: ", gs_clf.best_score_)
print("Classification report: ", classification_report(y_test, gs_clf.predict(X_test)))
    
shap.initjs()
explainer = shap.Explainer(gs_clf.best_estimator_)
shap_values = explainer(X_train)
shap.summary_plot(shap_values, X_train, feature_names=gs_clf.best_estimator_.named_steps['tfidf'].get_feature_names_out())
shap.summary_plot(shap_values, X_train, feature_names=gs_clf.best_estimator_.named_steps['tfidf'].get_feature_names_out(), plot_type="bar")

missclassified = []
for i in range(len(y_test)):
    if y_test[i] != gs_clf.predict(X_test)[i]:
        missclassified.append((X_test[i], y_test[i], gs_clf.predict(X_test)[i]))
        if len(missclassified) == 2:
            break
        
print(f"Text 1: {missclassified[0][0]}\nReal: {missclassified[0][1]}\nPredicted: {missclassified[0][2]}")
print(f"Text 2: {missclassified[1][0]}\nReal: {missclassified[1][1]}\nPredicted: {missclassified[1][2]}")