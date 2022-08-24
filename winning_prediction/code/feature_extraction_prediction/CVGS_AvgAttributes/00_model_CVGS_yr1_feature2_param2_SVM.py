##############################################
## Author: I-No Liao                        ##
## Date of update: 2018/05/25               ##
## Description: Data Mining Final Project   ##
## - Model Tuning                           ##
##############################################

import numpy as np
import pandas as pd
import time
import csv
import warnings
warnings.filterwarnings('ignore')
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV



#-----------------------#
#     Main Function     #
#-----------------------#

# @param: None
# @return: None
def main():
    startTime = time.time()
    
    # Feature Settings
    dfFile = 'nba_preprocessed.csv'
    dateStart = '2017-08-01'
    dateEnd = '2018-04-13'
    period = 5
    featureSel = 2
    
    # Model Settings
    trialName = '00_model_CVGS_yr1_feature2_param2'
    modelName = '_SVM'
    model = SVC()
    tuned_parameters = {
        'C': [0.01, 0.1, 1, 10, 100],
        'kernel': ['rbf', 'linear'], 
        'probability': [True]
    }
    
    # Feature Extraction
    X, Y = featureExtraction(dfFile, dateStart, dateEnd, period, featureSel)

    # Number of random trials
    NUM_TRIALS = 1
    (max_score, best_estimator) = CrossValidationGridSearchNested(X, Y, NUM_TRIALS, 10, model, tuned_parameters, 'roc_auc')
    
    # Write to .csv
    with open('./00_model_param/' + trialName + modelName + '.csv','w') as myFile:
        for key, value in zip(best_estimator.get_params().keys(), best_estimator.get_params().values()):
            myFile.write(key + ',' + str(value) + '\n')
        myFile.write('max_score' + ',' + str(max_score) + '\n')
        myFile.write('Execution time =' + ',' + str(time.time() - startTime) + '\n')



#-----------------------#
#     Sub-Functions     #
#-----------------------#

# @param X: pandas.DataFrame
# @param featureSel: int
# @return X: pandas.DataFrame
def featureEng(X, featureSel=None):
    # Feature Engineering
    if not featureSel or featureSel == 0:
        return X
    if featureSel == 1:
        X['PTS_DIFF'] = X['PTS_A'] - X['PTS_B']
    elif featureSel == 2:
        attriToDrop = ['PTS_A', 'PTS_B']
        X = X.drop(columns=attriToDrop)
    elif featureSel == 3:
        X['PTS_DIFF'] = X['PTS_A'] - X['PTS_B']
        attriToDrop = ['PTS_A', 'PTS_B']
        X = X.drop(columns=attriToDrop)
    elif featureSel == 4:
        attriToDrop = [
            'FGM_A', 'FGA_A', '3PM_A', '3PA_A', 'FTM_A', 'FTA_A', 'OREB_A', 'DREB_A', 'PF_A', 
            'FGM_B', 'FGA_B', '3PM_B', '3PA_B', 'FTM_B', 'FTA_B', 'OREB_B', 'DREB_B', 'PF_B'
        ]
        X['PTS_DIFF'] = X['PTS_A'] - X['PTS_B']
        X['STL+BLK_A'] = X['STL_A'] + X['BLK_A']
        X['STL+BLK_B'] = X['STL_B'] + X['BLK_B']
        attriToDrop += ['PTS_A', 'PTS_B', 'STL_A', 'STL_B', 'BLK_A', 'BLK_B']
        X = X.drop(columns=attriToDrop)
    return X

# @param dfFile: pandas.DataFrame ('nba_preprocessed.csv')
# @param dateStart, dateEnd: str in the format of 'YYYY-MM-DD'
# @param period: int
# @param featureSel: int (0, 1, 2, and 3 corresponds to feature0, 1, 2, and 3, respectively)
# @return X, Y: pandas.DataFrame
# featureExtraction() outputs X, Y for model training.
# Game date can be assigned
# Attribute to be dropped can be assigned
def featureExtraction(dfFile, dateStart='1000-01-01', dateEnd='2999-12-31', period=5, featureSel=None):
    df = pd.read_csv(dfFile)
    
    # Date selection
    df = df.loc[(df.Date_A >= dateStart) & (df.Date_A <= dateEnd), :].reset_index(drop=True)
    
    # Get label Y
    Y = df[['W/L_A']]
    Y = Y.rename(columns={'W/L_A': 'Label'})
    
    # Get averaged attributes X
    for idx, row in df.iterrows():
        df_sel = df.loc[df.Date_A <= row['Date_A'], :].reset_index(drop=True)
        
        # Process of Team_A
        gamePlayed_A = df_sel.loc[df_sel.Team_A == row['Team_A'], :]
        if len(gamePlayed_A) == 1:
            X_A = gamePlayed_A.loc[(gamePlayed_A.Team_A == row['Team_A']), :].sort_values(by=['Date_A'], ascending=False).iloc[0:1, 0:24].reset_index(drop=True)
        elif len(gamePlayed_A) < period:
            X_A = gamePlayed_A.loc[(gamePlayed_A.Team_A == row['Team_A']), :].sort_values(by=['Date_A'], ascending=False).iloc[1:len(gamePlayed_A), 0:24].reset_index(drop=True)
        else:
            X_A = gamePlayed_A.loc[(gamePlayed_A.Team_A == row['Team_A']), :].sort_values(by=['Date_A'], ascending=False).iloc[1:period+1, 0:24].reset_index(drop=True)
        
        # Process of Team_B
        gamePlayed_B = df_sel.loc[df_sel.Team_A == row['Team_B'], :]
        if len(gamePlayed_B) == 1:
            X_B = gamePlayed_B.loc[(gamePlayed_B.Team_A == row['Team_B']), :].sort_values(by=['Date_A'], ascending=False).iloc[0:1, 0:24].reset_index(drop=True)
        elif len(gamePlayed_B) < period:
            X_B = gamePlayed_B.loc[(gamePlayed_B.Team_A == row['Team_B']), :].sort_values(by=['Date_A'], ascending=False).iloc[1:len(gamePlayed_B), 0:24].reset_index(drop=True)
        else:
            X_B = gamePlayed_B.loc[(gamePlayed_B.Team_A == row['Team_B']), :].sort_values(by=['Date_A'], ascending=False).iloc[1:period+1, 0:24].reset_index(drop=True)
        
        # Drop unnecessary attributes
        colToDrop = ['Home/Away_A'] + ['Team_A', 'Date_A', 'W/L_A', 'Score_A', 'Opponent_A']
        X_A = X_A.drop(columns=colToDrop)
        X_B = X_B.drop(columns=colToDrop)
        
        # Rename X_B's columns
        X_B = X_B.rename(columns=lambda x: x[0:-2] + '_B')
        
        # Get X_single = [Home/Away_A + X_A + X_B]
        X_single = pd.DataFrame(data=pd.concat([X_A.mean(), X_B.mean()])).transpose()
        X_single = pd.concat([pd.DataFrame(data={'Home/Away_A': [row['Home/Away_A']]}), X_single], axis=1)
        
        # Concatenation dataFrames by row
        if idx == 0:
            X = X_single
        else:
            X = pd.concat([X, X_single], ignore_index=True)
        
    # Feature Engineering
    X = featureEng(X, featureSel)
        
    return X, Y

def CrossValidationGridSearchNested(X_data, Y_data, num_trials, fold_num, est_classifcation, tuned_param, scoring):
    max_score = -1
    best_estimator = est_classifcation
    is_tuned_param_empty = (tuned_param == []) | (tuned_param == None)
    
    for i in range(num_trials):
        inner_cv = StratifiedKFold(n_splits=fold_num, random_state=i, shuffle=True)
        outer_cv = StratifiedKFold(n_splits=fold_num, random_state=i+1, shuffle=True)
        
        if(is_tuned_param_empty):
            param_score = cross_val_score(est_classifcation, X=X_data, y=Y_data, cv=outer_cv, scoring=scoring).mean()
        else:
            # Non_nested parameter search and scoring
            clf = GridSearchCV(estimator=est_classifcation, param_grid=tuned_param, cv=inner_cv, scoring=scoring)
            clf.fit(X_data, Y_data)
        
            # CV with parameter optimization
            param_score = cross_val_score(clf.best_estimator_, X=X_data, y=Y_data, cv=outer_cv, scoring=scoring).mean()
            
        if(param_score > max_score):
            max_score = param_score
            if(is_tuned_param_empty):
                best_estimator = est_classifcation
            else:
                best_estimator = clf.best_estimator_
            
        progress = (i+1)/num_trials*100
        print(f'> progress = {progress}%')
    
    return (max_score, best_estimator)



#-----------------------#
#       Execution       #
#-----------------------#

if __name__ == '__main__':
    main()
