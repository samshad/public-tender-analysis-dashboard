import pandas as pd

from data_cleaning.cluster_entity_mapping import map_cluster_with_entity
from data_cleaning.data_preprocess import get_preprocessed_data, calculate_duration
from utils.constants import DATA_FILEPATH


def load_data(filepath: str) -> pd.DataFrame:
    """
    Loads a CSV file into a pandas DataFrame.
    Args:
        filepath (str): The file path of the CSV file to load.
    Returns:
        pd.DataFrame: A pandas DataFrame containing the data from the CSV file.
    """
    return pd.read_csv(filepath)


def get_data(filepath: str = DATA_FILEPATH):
    """
    Loads and preprocesses data, including calculating the duration and mapping clusters to entities.
    This function processes the dataset by loading the data, preprocessing it, calculating the
    duration of tenders, and mapping each entity to its respective cluster. It also determines the
    minimum and maximum years from the 'TENDER_START_DATE' column.
    Args:
        filepath (str): The file path of the CSV file to load. Defaults to DATA_FILEPATH.
    Returns:
        pd.DataFrame: A processed DataFrame with additional columns such as 'ENTITY_CLUSTER_NAME' and 'DURATION'.
        int: The minimum year from the 'TENDER_START_DATE' column.
        int: The maximum year from the 'TENDER_START_DATE' column.
    """

    # Load the initial dataset
    initial_dataset = load_data(filepath)

    # Preprocess the data (cleaning, filling missing values, etc.)
    df = get_preprocessed_data(initial_dataset)

    # Calculate the duration for each tender
    df = calculate_duration(df)

    # Map entities to clusters
    df = map_cluster_with_entity(df)

    # Get the minimum and maximum years based on the 'TENDER_START_DATE'
    min_year = df['TENDER_START_DATE'].dt.year.min()
    max_year = df['TENDER_START_DATE'].dt.year.max()

    return df, min_year, max_year
