
import numpy as np
import pandas as pd
import pickle
import os
import random
import torch
#no warnings
import warnings
warnings.filterwarnings('ignore')



def create_sequences(data, target, sessions, sequence_length):
    sequences = []
    targets = []

    # Split data by session and then create sequences
    unique_sessions = np.unique(sessions)
    for session in unique_sessions:
        session_indices = np.where(sessions == session)[0]
        session_data = data[session_indices]
        session_target = target[session_indices]
        
        if len(session_data) >= sequence_length:
            for i in range(len(session_data) - sequence_length + 1):
                sequences.append(session_data[i : i + sequence_length])
                targets.append(session_target[i + sequence_length - 1])

    #hot one encode the target
    targets = pd.get_dummies(targets).values
    
    return np.array(sequences), np.array(targets)


def createDataSplits(df, fold_no, with_val = 0, label_column = 'UserAkwardness', fold_column = 'fold_id', results_directory= '../logs/', seed_value = 42, sequence_length = 1):

    """
    Split the data into train, validation, and test sets for each fold.
    df - dataframe containing the data
    fold_no - number of fold to get the data for
    with_val - whether to include validation set or not
    label_column - column name for the target class
    fold_column - column name for the fold number
    results_directory - directory to store the results
    seed_value - seed value for reproducibility
    sequence_length - length of the sequence for RNNs or transformers
    
    """

    try:

        # # Set seed
        random.seed(seed_value)
        np.random.seed(seed_value)
    

        # get features and target class
        features = df.iloc[:,7:]
        target_class = df[label_column].values
        target_class = target_class.astype('int')
        sessions = df['session'].values


        #get number of classes
        num_classes = len(np.unique(target_class))
        #if fold number is none
        if fold_no is None:
            train_fold = df[fold_column].unique()
            print('folds:', train_fold)
            train_indices = df[df[fold_column].isin(train_fold)].index
            X_train = features.loc[train_indices]
            y_train = target_class[train_indices]
            session_train = sessions[train_indices]
            X_train = X_train.reset_index(drop=True)
            X_train_sequences, y_train_sequences = create_sequences(X_train.values, y_train, session_train, sequence_length)
            X_val = None
            y_val = None
            X_val_sequences = None
            y_val_sequences = None
            X_test = None
            y_test = None
            X_test_sequences = None
            y_test_sequences = None


        else:
            num_folds = df[fold_column].unique()
            fold_sessions = df[df[fold_column] == fold_no]['session'].unique()

            if with_val == 1:
                val_fold = fold_no
                #test fold should be the next fold, but if fold is max(num_folds), then test fold is 1
                if fold_no == np.max(num_folds):
                    test_fold = 1
                else:
                    test_fold = fold_no + 1
                train_fold = [f for f in num_folds if f not in [val_fold, test_fold]]


            else:
                test_fold = fold_no
                train_fold = [f for f in num_folds if f != test_fold]
                val_fold = None
            print('folds:', train_fold, val_fold, test_fold)


            # Split the data into train, validation, and test sets
            train_indices = df[df[fold_column].isin(train_fold)].index
            if with_val == 1:
                val_indices = df[df[fold_column] == val_fold].index
            test_indices = df[df[fold_column] == test_fold].index

            X_train = features.loc[train_indices]
            y_train = target_class[train_indices]
            session_train = sessions[train_indices]
            if with_val == 1:
                X_val = features.loc[val_indices]
                y_val = target_class[val_indices]
                session_val = sessions[val_indices]

            X_test = features.loc[test_indices]
            y_test = target_class[test_indices]
            session_test = sessions[test_indices]

            #print size of all sets
            print(X_train.shape, y_train.shape)
            if with_val == 1:
                print(X_val.shape, y_val.shape)
            print(X_test.shape, y_test.shape)

            #reset indexes
            X_train = X_train.reset_index(drop=True)
            if with_val == 1:
                X_val = X_val.reset_index(drop=True)
            X_test = X_test.reset_index(drop=True)

            # Create sequences for LSTM
            X_train_sequences, y_train_sequences = create_sequences(X_train.values, y_train, session_train, sequence_length)
            if with_val == 1:
                X_val_sequences, y_val_sequences = create_sequences(X_val.values, y_val, session_val, sequence_length)
            else:
                X_val_sequences = None
                y_val_sequences = None
                X_val = None
                y_val = None
                
            X_test_sequences, y_test_sequences = create_sequences(X_test.values, y_test, session_test, sequence_length)

        return num_classes, X_train, X_val, X_test, y_train, y_val, y_test, X_train_sequences, y_train_sequences, X_val_sequences, y_val_sequences, X_test_sequences, y_test_sequences
    
    except Exception as e:
        print(f"An error occurred: {e}")



        

def createDataSplits_test(df, num_classes, label_column = 'UserAkwardness', results_directory= '../logs/', seed_value = 42, sequence_length = 1):

    """
    Split the data into train, validation, and test sets for each fold.
    df - dataframe containing the data
    fold_no - number of fold to get the data for
    with_val - whether to include validation set or not
    label_column - column name for the target class
    fold_column - column name for the fold number
    results_directory - directory to store the results
    seed_value - seed value for reproducibility
    sequence_length - length of the sequence for RNNs or transformers
    
    """

    try:

        # # Set seed
        random.seed(seed_value)
        np.random.seed(seed_value)
    

        # get features and target class
        features = df.iloc[:,6:]
        target_class = df[label_column].values
        target_class = target_class.astype('int')
        sessions = df['session'].values

        X_test = features
        y_test = target_class


        print(X_test.shape, y_test.shape)

        X_test = X_test.reset_index(drop=True)

        # Create sequences for LSTM
        
        X_test_sequences, y_test_sequences = create_sequences(X_test.values, y_test, sessions, sequence_length)


        return sessions, X_test, y_test, X_test_sequences, y_test_sequences
    
    except Exception as e:
        print(f"An error occurred: {e}")



        