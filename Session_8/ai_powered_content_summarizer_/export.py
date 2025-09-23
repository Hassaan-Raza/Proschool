```python
# Import necessary libraries
import csv
import json
import pandas as pd
from datetime import datetime
from io import StringIO
from typing import Dict, List, Tuple

# Define a function to export data to CSV format
def export_to_csv(data: List[Dict], filename: str) -> None:
    """
    Export data to CSV format.

    Args:
        data (List[Dict]): Data to be exported.
        filename (str): Name of the output file.

    Returns:
        None
    """
    try:
        # Create a pandas DataFrame from the data
        df = pd.DataFrame(data)

        # Write the DataFrame to a CSV file
        df.to_csv(filename, index=False)

        print(f"Data exported to {filename} successfully.")

    except Exception as e:
        print(f"Error exporting data to CSV: {str(e)}")

# Define a function to export data to JSON format
def export_to_json(data: List[Dict], filename: str) -> None:
    """
    Export data to JSON format.

    Args:
        data (List[Dict]): Data to be exported.
        filename (str): Name of the output file.

    Returns:
        None
    """
    try:
        # Convert the data to a JSON string
        json_data = json.dumps(data, indent=4)

        # Write the JSON string to a file
        with open(filename, 'w') as f:
            f.write(json_data)

        print(f"Data exported to {filename} successfully.")

    except Exception as e:
        print(f"Error exporting data to JSON: {str(e)}")

# Define a function to export data to Excel format
def export_to_excel(data: List[Dict], filename: str) -> None:
    """
    Export data to Excel format.

    Args:
        data (List[Dict]): Data to be exported.
        filename (str): Name of the output file.

    Returns:
        None
    """
    try:
        # Create a pandas DataFrame from the data
        df = pd.DataFrame(data)

        # Write the DataFrame to an Excel file
        df.to_excel(filename, index=False)

        print(f"Data exported to {filename} successfully.")

    except Exception as e:
        print(f"Error exporting data to Excel: {str(e)}")

# Define a function to export data to a custom format
def export_to_custom(data: List[Dict], filename: str, format: str) -> None:
    """
    Export data to a custom format.

    Args:
        data (List[Dict]): Data to be exported.
        filename (str): Name of the output file.
        format (str): Format of the output file.

    Returns:
        None
    """
    try:
        # Create a pandas DataFrame from the data
        df = pd.DataFrame(data)

        # Write the DataFrame to a file based on the format
        if format == 'csv':
            df.to_csv(filename, index=False)
        elif format == 'json':
            df.to_json(filename, orient='records')
        elif format == 'excel':
            df.to_excel(filename, index=False)
        else:
            print("Unsupported format.")

        print(f"Data exported to {filename} successfully.")

    except Exception as e:
        print(f"Error exporting data to custom format: {str(e)}")

# Define a function to export data to multiple formats
def export_to_multiple_formats(data: List[Dict], filenames: List[str], formats: List[str]) -> None:
    """
    Export data to multiple formats.

    Args:
        data (List[Dict]): Data to be exported.
        filenames (List[str]): Names of the output files.
        formats (List[str]): Formats of the output files.

    Returns:
        None
    """
    try:
        # Export data to each format
        for filename, format in zip(filenames, formats):
            if format == 'csv':
                export_to_csv(data, filename)
            elif format == 'json':
                export_to_json(data, filename)
            elif format == 'excel':
                export_to_excel(data, filename)
            else:
                print("Unsupported format.")

        print("Data exported to multiple formats successfully.")

    except Exception as e:
        print(f"Error exporting data to multiple formats: {str(e)}")

# Example usage
if __name__ == "__main__":
    data = [
        {'name': 'John', 'age': 30},
        {'name': 'Jane', 'age': 25},
        {'name': 'Bob', 'age': 40}
    ]

    filenames = ['data.csv', 'data.json', 'data.xlsx']
    formats = ['csv', 'json', 'excel']

    export_to_multiple_formats(data, filenames, formats)
```