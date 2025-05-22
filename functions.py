

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