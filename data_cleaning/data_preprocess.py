import re
import string
import pandas as pd
import nltk
from utils.constants import ENTITY_FIXED_FILEPATH, VENDOR_FIXED_FILEPATH
from utils.unknown_vendor import vendors_to_exclude

# Download required NLTK resources
# nltk.download('punkt', quiet=True)
# nltk.download('stopwords', quiet=True)


def load_mapping(filepath: str) -> dict:
    """
    Load a key-value mapping from a file where each line is in the format 'key: value'.
    """
    with open(filepath, "r") as file:
        return {
            key.strip('"'): value.strip('"').rstrip(",")
            for line in file
            if ":" in line.strip()
            for key, value in [line.strip().split(":", 1)]
        }


def clean_string(input_string: str) -> str:
    """
    Clean input string by removing quotes and commas.
    """
    return input_string.replace('"', "").replace(",", "")


def process_mapping(mapping: dict, old_col: str, new_col: str) -> dict:
    """
    Create a cleaned mapping dictionary for replacing values.
    Args:
        mapping (dict): The original mapping dictionary.
        old_col (str): The original column name.
        new_col (str): The new column name.
    Returns:
        dict: A cleaned dictionary for replacing values.
    """
    return {clean_string(k): clean_string(v) for k, v in mapping.items()}


def calculate_duration(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the duration between 'TENDER_START_DATE' and 'TENDER_CLOSE_DATE' in days.
    """
    df["DURATION"] = (df["TENDER_CLOSE_DATE"] - df["TENDER_START_DATE"]).dt.days
    return df


def clean_and_transform_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform transformations and clean specific columns.
    """
    # Convert 'Y/N' columns to binary (1 for 'Y', 0 for 'N')
    binary_columns = ["GOODS", "SERVICE", "CONSTRUCTION"]
    df[binary_columns] = df[binary_columns].applymap(lambda x: 1 if x == "Y" else 0)

    # Drop rows with missing vendor information
    df.dropna(subset=["VENDOR"], inplace=True)
    return df


def preprocess_dates_and_amounts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert date columns to datetime and numeric columns to numeric, handling errors.
    Drop rows with missing or invalid values in critical columns.
    Additionally, remove rows where AWARDED_AMOUNT is less than 1000.
    """
    # Convert date columns to datetime
    date_columns = ["TENDER_START_DATE", "TENDER_CLOSE_DATE", "AWARDED_DATE"]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # Convert AWARDED_AMOUNT to numeric
    df["AWARDED_AMOUNT"] = pd.to_numeric(df["AWARDED_AMOUNT"], errors="coerce")
    # Drop rows with missing or invalid AWARDED_AMOUNT
    df = df.dropna(subset=["AWARDED_AMOUNT"])
    # Remove rows where AWARDED_AMOUNT is less than 1000
    df = df[df["AWARDED_AMOUNT"] >= 1000]

    return df


def clean_text(text: str) -> str:
    """
    Clean and preprocess the input text by performing various text transformations.
    Args:
        text (str): The text to clean.
    Returns:
        str: The cleaned text.
    """
    text = str(text)  # Ensure the input is a string
    text = text.lower()  # Convert all characters to lower case
    text = re.sub(r"@\S+", "", text)  # Remove Twitter handles
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(
        r"[^a-zA-Z+']", " ", text
    )  # Keep only alphabetic characters and apostrophes
    text = re.sub(r"\s+[a-zA-Z]\s+", " ", text + " ")  # Keep words with length > 1 only
    text = "".join(
        [i for i in text if i not in string.punctuation]
    )  # Remove punctuation
    words = nltk.tokenize.word_tokenize(text)  # Tokenize the text
    stopwords = nltk.corpus.stopwords.words("english")  # Load stopwords
    # Remove stopwords and keep words with length > 2
    text = " ".join([i for i in words if i not in stopwords and len(i) > 2])
    text = re.sub(
        "\s+", " ", text
    ).strip()  # Remove repeated, leading, and trailing spaces
    return text


def clean_entity_and_vendor(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strip leading and trailing whitespaces from 'ENTITY' and 'VENDOR' columns.
    """
    df["ENTITY"] = df["ENTITY"].str.strip()
    df["VENDOR"] = df["VENDOR"].str.strip()

    return df


def drop_nova_scotia_vendor(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop rows where the VENDOR column equals 'Nova Scotia Ltd.' (case-sensitive).
    """
    df = df[df["VENDOR"] != "Nova Scotia Ltd."]
    return df


def clean_unknown_vendor(df: pd.DataFrame) -> pd.DataFrame:
    df = df[~df["VENDOR"].isin(vendors_to_exclude)]
    return df


def get_preprocessed_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the input DataFrame:
    - Replace 'VENDOR' and 'ENTITY' values using mappings.
    - Rename columns and add fixed values.
    Args:
        df (pd.DataFrame): The raw DataFrame containing tender data.
    Returns:
        pd.DataFrame: A cleaned and transformed DataFrame.
    """

    # Load and process mappings for entity and vendor
    entity_mapping = process_mapping(
        load_mapping(ENTITY_FIXED_FILEPATH), "OLD_ENTITY", "NEW_ENTITY"
    )
    vendor_mapping = process_mapping(
        load_mapping(VENDOR_FIXED_FILEPATH), "OLD_VENDOR", "NEW_VENDOR"
    )

    # Rename and update columns
    processed_df = df.rename(
        columns={"VENDOR": "TYPO_MIXED_VENDOR", "ENTITY": "TYPO_MIXED_ENTITY"}
    ).copy()

    # Replace vendor and entity names based on mappings
    processed_df["VENDOR"] = processed_df["TYPO_MIXED_VENDOR"].replace(vendor_mapping)
    processed_df["ENTITY"] = processed_df["TYPO_MIXED_ENTITY"].replace(entity_mapping)

    # Clean and fill missing tender descriptions
    processed_df["TENDER_DESCRIPTION"] = (
        processed_df["TENDER_DESCRIPTION"].fillna("").str.lower()
    )
    # Preserve original tender descriptions for reference
    processed_df["UNCLEANED_TENDER_DESCRIPTION"] = processed_df["TENDER_DESCRIPTION"]
    # Clean tender descriptions
    processed_df["TENDER_DESCRIPTION"] = (
        processed_df["UNCLEANED_TENDER_DESCRIPTION"].fillna("").apply(clean_text)
    )
    # Clean and remove irrelevant vendor and entity records
    processed_df = clean_entity_and_vendor(processed_df)
    processed_df = drop_nova_scotia_vendor(processed_df)
    processed_df = clean_unknown_vendor(processed_df)
    # Apply further preprocessing on dates and amounts
    processed_df = preprocess_dates_and_amounts(processed_df)
    # Apply column transformations and return the cleaned DataFrame
    return clean_and_transform_columns(processed_df)
