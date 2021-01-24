import pickle
import sklearn
import pandas as pd

def get_prediction(logger, input_data, use_pre_trained = True):
    
    if use_pre_trained:
        model_name_file = "/Users/xrxb206/Desktop/clf_features_pretraind.pkl"
    else:
        model_name_file = "new_trained_model.pkl"

    model_details = pickle.load(open(model_name_file, "rb"))
    clf = model_details[0]
    features = list(model_details[1])
    features.remove("Ticket number")
    features.remove("target")
    input_data_df = pd.DataFrame(index=[1], columns =  features)
    
    for key in list(input_data.keys()):
        if key in input_data_df.columns:
            input_data_df.loc[1,key] = input_data[key]
        elif key == "Color":
            col_name = "Color_" + input_data[key]
            if col_name in input_data_df.columns:
                input_data_df.loc[1,col_name] = 1
            else:
                print(input_data[key] , "is not acceptable color for the model")
                return -1
        
        elif key == "Body Style":
            col_name = "Body Style_" + input_data[key]
            if col_name in input_data_df.columns:
                input_data_df.loc[1,col_name] = 1
            else:
                print(input_data[key] , "is not acceptable Body Style for the model")
                return -1

    input_data_df = input_data_df.fillna(0)

    predicts = clf.predict_proba(input_data_df)[:,1][0]
    return round(predicts,2)


   
    