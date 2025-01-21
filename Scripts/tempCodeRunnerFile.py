categorical_columns = ['SourceAirport', 'DestinationAirport']

# def encode_categorical_data(data, categorical_columns):
#     """
#     Encode categorical data using LabelEncoder.
    
#     Parameters:
#         data (pd.DataFrame): The dataset.
#         categorical_columns (list): List of categorical column names to encode.
    
#     Returns:
#         pd.DataFrame: The dataset with encoded categorical columns.
#     """
#     label_encoder = LabelEncoder()
#     for col in categorical_columns:
#         data[col] = label_encoder.fit_transform(data[col])
#     print("Categorical columns encoded successfully.")
#     return data
