import pandas as pd


# Load data
def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame
    
    Parameters:
    ----------
    file_path : str
        Path to the CSV file
    
    Returns:
    -------
    df : pd.DataFrame
        DataFrame containing the data from the CSV file
    """
    return pd.read_csv(file_path, header=0)


# Display basic information about the data
def display_basic_info(df: pd.DataFrame) -> dict:
    """
    Display basic information about the data
    
    Parameters:
    ----------
    df : pd.DataFrame
        DataFrame containing the data
        
    Returns:
    -------
    info : dict
        Dictionary containing basic information about the data
    """
    info = {
        "head": df.head(),
        "description": df.describe(include='all'),
        "missing_values": df.isnull().sum(),
        "unique_counts": {
            "nutrients": df.iloc[:, 0].nunique(),
            "foods": df.iloc[:, 1].nunique()
        }
    }
    return info
