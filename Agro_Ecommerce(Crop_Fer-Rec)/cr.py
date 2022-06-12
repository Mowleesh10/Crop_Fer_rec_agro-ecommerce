import pandas as pd
import numpy as np
import pickle

df = pd.read_csv('Crop_recommendation.csv')

features = df[['N', 'P','K','temperature', 'humidity', 'ph', 'rainfall']]
target = df['label']
#features = df[['temperature', 'humidity', 'ph', 'rainfall']]
labels = df['label']

from sklearn.model_selection import train_test_split
Xtrain, Xtest, Ytrain, Ytest = train_test_split(features,target,test_size = 0.2,random_state =2)

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,classification_report
from sklearn import metrics

DecisionTree = DecisionTreeClassifier(criterion="entropy",random_state=42,max_depth=10)

DecisionTree.fit(Xtrain,Ytrain)
#predicted_values = DecisionTree.predict(Xtest)

from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

KN_clf = KNeighborsClassifier(n_neighbors = 10)

KN_clf.fit(Xtrain,Ytrain)
#predicted_values = KN_clf.predict(Xtest)
 

from sklearn.ensemble import RandomForestClassifier


rf=RandomForestClassifier()

rf.fit(Xtrain,Ytrain)
#model=rf.predict(Xtest)

from sklearn.svm import SVC
svm_clf = SVC(probability = True, kernel='linear')

svm_clf.fit(Xtrain,Ytrain)
#predicted_values = svm_clf.predict(Xtest)

from sklearn.linear_model import LogisticRegression
lr_clf = LogisticRegression(solver='lbfgs', max_iter=10000)
lr_clf.fit(Xtrain,Ytrain)

from sklearn.naive_bayes import GaussianNB
nb_clf = GaussianNB()
nb_clf.fit(Xtrain,Ytrain)

pickle.dump(DecisionTree,open('cr_dt.pkl','wb'))
pickle.dump(KN_clf,open('cr_kn.pkl','wb'))
pickle.dump(rf,open('cr_rf.pkl','wb'))
pickle.dump(svm_clf,open('cr_svm.pkl','wb'))
pickle.dump(lr_clf,open('cr_lr.pkl','wb'))
pickle.dump(nb_clf,open('cr_nb.pkl','wb'))
 
