

def transform_categorical_to_numerical(df, column, mapping):
    """Transform categorical values in a specified column to numerical values based on a provided mapping.
    Parameters:
    df (DataFrame): The DataFrame to modify.
    column (str): The specific column to operate on.
    mapping (dict): A dictionary where keys are the categorical values and values are the corresponding numerical values.
    Returns:
    DataFrame: The modified DataFrame with categorical values replaced by numerical values.
    """
    if column in df.columns:
        df[column] = df[column].map(mapping)

    return df

def load_dataset(file_name):
    """Load the dataset from the specified file.
    Parameters:
    file_name (str): The name of the file to load.
    Returns:
    DataFrame: The loaded dataset.
    """
    print("Loading data... \n")
    if os.path.exists(file_name):
        try:
            df = pd.read_excel(file_name)
            print("Data loaded successfully.")
            return df
        except Exception as e:
            print(f"Error loading file: {e}")
            return None
    else:
        print("File not found")
        return None