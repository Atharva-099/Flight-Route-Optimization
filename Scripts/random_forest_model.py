import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import joblib  


def load_data(file_path):
    """
    Load the dataset for training the Random Forest model.
    The dataset should contain features and the target column.
    
    Parameters:
        file_path (str): Path to the dataset file.
    
    Returns:
        pd.DataFrame: Loaded dataset.
    """
    data = pd.read_csv(file_path)
    print("Data loaded successfully.")
    return data

def encode_categorical_data(data, categorical_columns, label_encoders=None):
    """
    Encode categorical columns using Label Encoding.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        categorical_columns (list): List of categorical column names to encode.
        label_encoders (dict, optional): Existing label encoders to use for encoding (for prediction).
    
    Returns:
        pd.DataFrame: Data with encoded categorical columns.
        dict: Dictionary of label encoders used for encoding.
    """
    if label_encoders is None:
        label_encoders = {}

    for col in categorical_columns:
        if col not in label_encoders:
            label_encoders[col] = LabelEncoder()
            data[col] = label_encoders[col].fit_transform(data[col])
        else:
            data[col] = label_encoders[col].transform(data[col])

    print("Categorical data encoded successfully.")
    return data, label_encoders

def split_data(data, target_column, test_size=0.2, random_state=42):
    """
    Split the dataset into training and testing sets.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        target_column (str): The name of the target column.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed.
    
    Returns:
        X_train, X_test, y_train, y_test
    """
    X = data.drop(columns=[target_column])
    y = data[target_column]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def train_random_forest(X_train, y_train, n_estimators=100, random_state=42):
    """
    Train the Random Forest Regressor.
    
    Parameters:
        X_train (pd.DataFrame): Training features.
        y_train (pd.Series): Training target.
        n_estimators (int): Number of trees in the forest.
        random_state (int): Random seed.
    
    Returns:
        RandomForestRegressor: Trained model.
    """
    model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
    model.fit(X_train, y_train)
    print("Random Forest model trained successfully.")
    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model on the test set.
    
    Parameters:
        model: Trained model.
        X_test (pd.DataFrame): Testing features.
        y_test (pd.Series): Testing target.
    
    Returns:
        None
    """
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"Mean Squared Error: {mse}")
    print(f"R^2 Score: {r2}")

def save_model(model, file_path):
    """
    Save the trained model to a file.
    
    Parameters:
        model: Trained model.
        file_path (str): Path to save the model.
    """
    joblib.dump(model, file_path)
    print(f"Model saved to {file_path}.")

def save_encoder(label_encoders, file_path):
    """
    Save the label encoders to a file.
    
    Parameters:
        label_encoders (dict): Dictionary of label encoders.
        file_path (str): Path to save the encoders.
    """
    joblib.dump(label_encoders, file_path)
    print(f"Encoder saved to {file_path}.")

def load_model(file_path):
    """
    Load a saved model from a file.
    
    Parameters:
        file_path (str): Path to the saved model file.
    
    Returns:
        The loaded model.
    """
    model = joblib.load(file_path)
    print(f"Model loaded from {file_path}.")
    return model

def load_encoder(file_path):
    """
    Load a saved encoder from a file.
    
    Parameters:
        file_path (str): Path to the saved encoder file.
    
    Returns:
        The loaded encoder.
    """
    encoder = joblib.load(file_path)
    print(f"Encoder loaded from {file_path}.")
    return encoder

def predict_travel_time(model, label_encoders, source, destination):
    """
    Predict the travel time between two airports using the trained Random Forest model.
    
    Parameters:
        model: Trained Random Forest model.
        label_encoders (dict): Label encoders for categorical data.
        source (str): Source airport code.
        destination (str): Destination airport code.
    
    Returns:
        float: Predicted travel time in hours.
    """
    input_data = pd.DataFrame({'SourceAirport': [source], 'DestinationAirport': [destination]})
    input_data, _ = encode_categorical_data(input_data, categorical_columns=['SourceAirport', 'DestinationAirport'], label_encoders=label_encoders)
    
    travel_time = model.predict(input_data.drop(columns=['SourceAirport', 'DestinationAirport']))
    return travel_time[0]

if __name__ == "__main__":
    data_path = "D:/Flight Route Optimization/Data/preprocessed_data.csv"
    model_path = "D:/Flight Route Optimization/Scripts/random_forest_model.pkl"
    encoder_path = "D:/Flight Route Optimization/Scripts/label_encoder.pkl"
    data = load_data(data_path)

    categorical_columns = ['SourceAirport', 'DestinationAirport']

    data, label_encoders = encode_categorical_data(data, categorical_columns)

    X_train, X_test, y_train, y_test = split_data(data, target_column="TravelTime")

    rf_model = train_random_forest(X_train, y_train)

    evaluate_model(rf_model, X_test, y_test)

    save_model(rf_model, model_path)

    save_encoder(label_encoders, encoder_path)
