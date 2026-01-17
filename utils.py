"""
Utility functions for chess games data processing and analysis.
"""
import pandas as pd
import numpy as np
from datetime import datetime


def load_chess_data(filepath='chess_games.csv', sample_size=None):
    """
    Load chess games data from CSV file.

    Parameters:
    -----------
    filepath : str
        Path to the CSV file
    sample_size : int, optional
        If provided, load only a sample of the data (useful for large datasets)

    Returns:
    --------
    pd.DataFrame
        Chess games dataframe
    """
    if sample_size:
        # Read in chunks and sample
        chunk_size = 100000
        chunks = []
        for chunk in pd.read_csv(filepath, chunksize=chunk_size):
            chunks.append(chunk)
            if len(chunks) * chunk_size >= sample_size:
                break
        df = pd.concat(chunks, ignore_index=True)
        df = df.sample(n=min(sample_size, len(df)), random_state=42)
    else:
        df = pd.read_csv(filepath)

    return df


def preprocess_data(df):
    """
    Preprocess chess games data.

    Parameters:
    -----------
    df : pd.DataFrame
        Raw chess games dataframe

    Returns:
    --------
    pd.DataFrame
        Preprocessed dataframe
    """
    df = df.copy()

    # Combine date and time columns
    if 'UTCDate' in df.columns and 'UTCTime' in df.columns:
        df['DateTime'] = pd.to_datetime(df['UTCDate'] + ' ' + df['UTCTime'],
                                        format='%Y.%m.%d %H:%M:%S', errors='coerce')
        df['Date'] = pd.to_datetime(df['UTCDate'], format='%Y.%m.%d', errors='coerce')
        df['Hour'] = df['DateTime'].dt.hour
        # Use Date column for DayOfWeek as it's more reliable (less parsing errors)
        df['DayOfWeek'] = df['Date'].dt.day_name()

    # Parse time control
    if 'TimeControl' in df.columns:
        df['TimeControl_Base'] = df['TimeControl'].str.split('+').str[0].astype(float, errors='ignore')
        df['TimeControl_Increment'] = df['TimeControl'].str.split('+').str[1].astype(float, errors='ignore')

        # Group time controls into categories
        def categorize_time_control(x):
            if pd.isna(x):
                return 'Unknown'
            try:
                base_time = float(str(x).split('+')[0])
                if base_time < 180:
                    return 'Bullet (<3min)'
                elif base_time < 600:
                    return 'Blitz (3-10min)'
                elif base_time < 3600:
                    return 'Rapid (10-60min)'
                else:
                    return 'Classical (>60min)'
            except:
                return 'Unknown'

        df['TimeControl_Grouped'] = df['TimeControl'].apply(categorize_time_control)

    # Calculate average ELO
    if 'WhiteElo' in df.columns and 'BlackElo' in df.columns:
        df['AvgElo'] = (df['WhiteElo'] + df['BlackElo']) / 2
        df['EloDiff'] = abs(df['WhiteElo'] - df['BlackElo'])

    # Parse result
    if 'Result' in df.columns:
        df['WhiteWins'] = (df['Result'] == '1-0').astype(int)
        df['BlackWins'] = (df['Result'] == '0-1').astype(int)
        df['Draw'] = (df['Result'] == '1/2-1/2').astype(int)

    # Extract move count from AN column if available
    if 'AN' in df.columns:
        df['MoveCount'] = df['AN'].str.count(r'\d+\.') + df['AN'].str.count(r'\d+\.\.\.')

    return df


def get_opening_category(eco_code):
    """
    Categorize ECO opening codes into major categories.

    Parameters:
    -----------
    eco_code : str
        ECO code (e.g., 'A00', 'B20', etc.)

    Returns:
    --------
    str
        Opening category
    """
    if pd.isna(eco_code):
        return 'Unknown'

    eco_code = str(eco_code).upper()
    first_letter = eco_code[0]

    categories = {
        'A': 'Flank Openings',
        'B': 'Semi-Open Games',
        'C': 'Open Games',
        'D': 'Closed Games',
        'E': 'Indian Defenses'
    }

    return categories.get(first_letter, 'Other')


def calculate_game_duration(moves_text):
    """
    Estimate game duration based on move count.
    This is a rough estimate assuming average time per move.

    Parameters:
    -----------
    moves_text : str
        Moves in algebraic notation

    Returns:
    --------
    int
        Estimated duration in minutes
    """
    if pd.isna(moves_text):
        return None

    move_count = str(moves_text).count('.')
    # Rough estimate: 2 minutes per move on average
    return move_count * 2
