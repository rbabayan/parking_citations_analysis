import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score, precision_score, auc, precision_recall_curve, roc_curve
from sklearn.pipeline import Pipeline

def build_labels(train_set):
    
    train_org = train_set[~train_set["Make"].isna()]
    train_org = train_org.sample(frac=1, random_state=22)
    
    label_freq = pd.DataFrame({"make":train_org["Make"].value_counts().index, 
                           "freq":train_org["Make"].value_counts().values
                              })
    
    label_freq = label_freq.sort_values("freq", ascending=False)

    top_25 = label_freq[:25]
    common_makes = list(top_25["make"].unique())

    train_org.loc[:,"target"] = train_org["Make"].apply(lambda x: create_label(x, common_makes))
    train_org = train_org.drop(columns = "Make")
    
    return train_org

def preprocess_data(df, categorical_columns = ['Color', 'Body Style']):
    
    df = df.drop(columns=["VIN", "Marked Time", "Meter Id", "Issue Date", 
                          "Violation Description", "Location", 'Route', 
                          'Violation code', 'RP State Plate', "Issue Date"])
    
    train = pd.get_dummies(data=df, columns=categorical_columns)

    train = train.fillna(0)
    train = train.sample(frac=1)
    
    return train

def train_model(train_dataset, use_pre_trained = True):
    
    if use_pre_trained:
        clf = pickle.load(open("/Users/xrxb206/Desktop/Assessment/logistic_20_color_state.pkl","rb"))
    
    else:
        scaler = MinMaxScaler()
        clf = LogisticRegression(class_weight = {0: len(train)/len(train["target"]==0), 
                                                 1: len(train)/len(train["target"]==1)}, max_iter = 10000)

        pipeline = Pipeline([('scalar', scaler), ('skb', SelectKBest(chi2)), ('estimator', clf)]) 

        x = train_dataset.drop(columns=["Ticket number", "target"])
        y = train_dataset[["target"]].values

        param_candidate = [{'skb__k':list(range(1,20))}, 
                           {'estimator__C': [0.00001, 0.0001, 0.001, 0.01, 0.1, 10, 100, 1000]}] 

        clf = GridSearchCV(pipeline, param_grid=param_candidate, cv=2,scoring="roc_auc", verbose=1)
        clf = clf.fit(train_X, train_y.ravel())
        
        print('Best score for data:', clf.best_score_) 
        print('Best params:',clf.best_params_) 
        
    return clf

    def main():
        
        df = pd.read_csv("dataset.csv", 
                  usecols=None,
                  low_memory=False, 
                  dtype=str
                )
        df_dataset = preprocess_data(df)
        train_org = df_dataset[~df_dataset["Make"].isna()]
        train_org = build_labels(train_org) 
        train_org = train_org.sample(frac=1, random_state=22)
        clf = train_model(train_org, use_pre_trained = False)

        #Save clf
        pickle.dump(clf, open("new_trained_model.pkl","wb"))
        print("The model is save in 'new_trained_model.pkl' file")

        