import pandas as pd
import numpy as np

spam_data = pd.read_csv('C:/courses/Coursera/Current/Python Text Mining/Week3/spam.csv')

spam_data['target'] = np.where(spam_data['target']=='spam',1,0)
print(spam_data.head(10))

from sklearn.model_selection import train_test_split


X_train, X_test, y_train, y_test = train_test_split(spam_data['text'], 
                                                    spam_data['target'], 
                                                    random_state=0)
													

def answer_one():    
    
    return 100*spam_data[spam_data['target'] == 1].shape[0] / float(spam_data.shape[0]) #Your answer here

print(answer_one())

from sklearn.feature_extraction.text import CountVectorizer

def answer_two():

    # Fit the CountVectorizer to the training data
    vect = CountVectorizer().fit(X_train)
    tokens = vect.get_feature_names()
    return max([(len(token), token) for token in tokens])[1] #Your answer here
	
print(answer_two())

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import roc_auc_score

def answer_three():
    
     # Fit the CountVectorizer to the training data
    vect = CountVectorizer().fit(X_train)
    X_train_vectorized = vect.transform(X_train)
    model = MultinomialNB(alpha=0.1)
    model.fit(X_train_vectorized, y_train)
    predictions = model.predict(vect.transform(X_test))
    return roc_auc_score(y_test, predictions) #Your answer here
	
print(answer_three())

from sklearn.feature_extraction.text import TfidfVectorizer

def answer_four():
    
    vect = TfidfVectorizer().fit(X_train)
    X_train_vectorized = vect.transform(X_train)
    feature_names = np.array(vect.get_feature_names())
    tfidfs = X_train_vectorized.max(0).toarray()[0]
    sorted_tfidf_index = tfidfs.argsort()
    s1 = pd.Series(tfidfs[sorted_tfidf_index[:20]], index=feature_names[sorted_tfidf_index[:20]])
    s2 = pd.Series(tfidfs[sorted_tfidf_index[:-21:-1]], index=feature_names[sorted_tfidf_index[:-21:-1]])
    return (s1, s2) #Your answer here
	
print(answer_four())

def answer_five():
    
    vect = TfidfVectorizer(min_df=3).fit(X_train)
    X_train_vectorized = vect.transform(X_train)
    model = MultinomialNB(alpha=0.1)
    model.fit(X_train_vectorized, y_train)
    predictions = model.predict(vect.transform(X_test))
    return roc_auc_score(y_test, predictions) #Your answer here
	
print(answer_five())

def answer_six():
    
    return (spam_data[spam_data['target'] == 0].text.str.len().mean(), spam_data[spam_data['target'] == 1].text.str.len().mean()) #Your answer here
	
print(answer_six())

def add_feature(X, feature_to_add):
    """
    Returns sparse feature matrix with added feature.
    feature_to_add can also be a list of features.
    """
    from scipy.sparse import csr_matrix, hstack
    return hstack([X, csr_matrix(feature_to_add).T], 'csr')
	
from sklearn.svm import SVC

def answer_seven():
    
    vect = TfidfVectorizer(min_df=3).fit(X_train)
    X_train_vectorized = add_feature(vect.transform(X_train), X_train.str.len())
    model = SVC(C=10000)
    model.fit(X_train_vectorized, y_train)
    predictions = model.predict(add_feature(vect.transform(X_test), X_test.str.len()))
    return roc_auc_score(y_test, predictions) #Your answer here
	
print(answer_seven())

def answer_eight():
    
    return (spam_data[spam_data['target'] == 0]['text'].str.count(r'\d').mean(), spam_data[spam_data['target'] == 1]['text'].str.count(r'\d').mean()) #Your answer here
	
print(answer_eight())

from sklearn.linear_model import LogisticRegression

def answer_nine():
    
    vect = CountVectorizer(min_df=5, ngram_range=(1,3)).fit(X_train)
    X_train_vectorized = add_feature(add_feature(vect.transform(X_train), X_train.str.len()), X_train.str.count(r'\d'))
    model = LogisticRegression(C=100)
    model.fit(X_train_vectorized, y_train)
    predictions = model.predict(add_feature(add_feature(vect.transform(X_test), X_test.str.len()), X_test.str.count(r'\d')))
    return roc_auc_score(y_test, predictions) #Your answer here

print(answer_nine())	
	
def answer_ten():    
    
    return (spam_data[spam_data['target'] == 0]['text'].str.count(r'\W').mean(), spam_data[spam_data['target'] == 1]['text'].str.count(r'\W').mean()) #Your answer here
	
print(answer_ten())

def answer_eleven():
    
    vect = CountVectorizer(min_df=5, ngram_range=(2,5), analyzer='char_wb').fit(X_train)
    X_train_vectorized = add_feature(add_feature(add_feature(vect.transform(X_train), X_train.str.len()), X_train.str.count(r'\d')), X_train.str.count(r'\W'))
    model = LogisticRegression(C=100)
    model.fit(X_train_vectorized, y_train)
    predictions = model.predict(add_feature(add_feature(add_feature(vect.transform(X_test), X_test.str.len()), X_test.str.count(r'\d')), X_test.str.count(r'\W')))
    feature_names = np.array(vect.get_feature_names() + ['length_of_doc', 'digit_count', 'non_word_char_count'])
    sorted_coef_index = model.coef_[0].argsort()
    return (roc_auc_score(y_test, predictions), feature_names[sorted_coef_index[:10]].tolist(), feature_names[sorted_coef_index[:-11:-1]].tolist()) #Your answer here

print(answer_eleven())	