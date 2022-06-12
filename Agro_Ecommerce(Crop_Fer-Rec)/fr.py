import pandas as pd
import numpy as np
import pickle

df=pd.read_csv("Fertilizer_Prediction.csv")

from sklearn.preprocessing import StandardScaler,LabelEncoder
soil_type_label_encoder=LabelEncoder()
df["Soil Type"]=soil_type_label_encoder.fit_transform(df["Soil Type"])
crop_type_label_encoder=LabelEncoder()
df["Crop Type"]=crop_type_label_encoder.fit_transform(df["Crop Type"])

croptype_dict = {}
for i in range(len(df["Crop Type"].unique())):
    croptype_dict[i] = crop_type_label_encoder.inverse_transform([i])[0]

soiltype_dict= {}
for i in range(len(df["Soil Type"].unique())):
    soiltype_dict[i] = soil_type_label_encoder.inverse_transform([i])[0]

features = df[['Temparature','Humidity ','Moisture','Soil Type','Crop Type','Nitrogen','Potassium','Phosphorous']]
target = df['Fertilizer Name']
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(features,target,test_size=0.2,random_state=42)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,confusion_matrix
from sklearn.pipeline import make_pipeline

rf_pipeline = make_pipeline(StandardScaler(), RandomForestClassifier(random_state = 42))
rf_pipeline.fit(X_train, Y_train)

from sklearn.svm import SVC

svm_pipeline = make_pipeline(StandardScaler(), SVC(probability=True))
svm_pipeline.fit(X_train, Y_train)

from sklearn.neighbors import  KNeighborsClassifier

knn_pipeline = make_pipeline(StandardScaler(),KNeighborsClassifier())
knn_pipeline.fit(X_train, Y_train)

pickle.dump(rf_pipeline,open('fr_rf.pkl','wb'))
pickle.dump(svm_pipeline,open('fr_svm.pkl','wb'))
pickle.dump(knn_pipeline,open('fr_knn.pkl','wb'))