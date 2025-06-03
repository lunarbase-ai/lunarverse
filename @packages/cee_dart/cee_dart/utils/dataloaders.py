import pandera as pa
import pandas as pd
from pandera import Column, Check
import re


# %% LRP input data validation
class LRPData:
    def __init__(self, file_path: str, delimiter: str = ","):
        """
        Initialize the InputData instance.

        Args:
            file_path (str): Path to the input file (Excel, CSV, or tab-separated).
            delimiter (str, optional): Delimiter for the file (None for Excel).
        """
        self.file_path = file_path
        self.delimiter = delimiter
        self.data = None

    @staticmethod
    def is_valid_column_name(column_name: str) -> bool:
        """
        Check if the column name follows the expected format 'xxx - xxx'.

        Args:
            column_name (str): The column name to validate.

        Returns:
            bool: True if the column name is valid, False otherwise.
        """
        return isinstance(column_name, str) and len(column_name.split(" - ")) == 2

    def validate_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate the column names format in the DataFrame. If validation fails, try transposing the DataFrame
        and re-validating. If successful, return the transposed DataFrame.

        Args:
            df (pd.DataFrame): DataFrame to validate.

        Returns:
            pd.DataFrame: The original or transposed DataFrame with valid column names.

        Raises:
            ValueError: If column names are invalid even after transposing.
        """
        try:
            for col in df.columns:
                if not self.is_valid_column_name(col):
                    raise ValueError(
                        f"Invalid column name: {col}. Expected format 'xxx - xxx', where 'xxx' represents one input parameter and 'yyy' represents the second input parameter."
                    )
            return df
        except ValueError as e:
            # Attempt to transpose and validate again
            transposed_df = df.transpose()
            for col in transposed_df.columns:
                if not self.is_valid_column_name(col):
                    raise ValueError(
                        f"Invalid column name: {col}. Expected format 'xxx - xxx', where 'xxx' represents one input parameter and 'yyy' represents the second input parameter, even after transposing."
                    )
            return transposed_df

    @staticmethod
    def read_data(file_path: str, delimiter: str = ",") -> pd.DataFrame:
        """
        Read data from a file into a DataFrame.

        Args:
            file_path (str): Path to the input file (Excel, CSV, or tab-separated).
            delimiter (str, optional): Delimiter for the file (None for Excel).

        Returns:
            pd.DataFrame: DataFrame containing the data from the file.

        Raises:
            ValueError: If the file type is unsupported.
        """
        if file_path.endswith(".csv") or (delimiter and file_path.endswith(".txt")):
            return pd.read_csv(file_path, delimiter=delimiter, index_col=0)
        elif file_path.endswith(".xlsx"):
            return pd.read_excel(file_path, index_col=0)
        else:
            raise ValueError(
                "Unsupported file type. Use Excel (.xlsx), CSV, or tab-separated files."
            )

    def validate_cell_values(self, df: pd.DataFrame) -> None:
        """
        Validate the values in the DataFrame cells. Ensure all values are numeric and there are no missing values.

        Args:
            df (pd.DataFrame): DataFrame to validate.

        Raises:
            ValueError: If any cell contains non-numeric values or missing values.
        """
        if df.isnull().values.any():
            raise ValueError("The DataFrame contains missing values.")

        if not df.map(lambda x: isinstance(x, (int, float))).all().all():
            raise ValueError("All cells in the DataFrame must be numeric.")

    def read_and_validate(self) -> pd.DataFrame:
        """
        Validate the input file for proper column names and row indices.

        Returns:
            pd.DataFrame: Validated DataFrame.

        Raises:
            ValueError: If column names or row indices are invalid.
        """
        # Read the file into a DataFrame
        self.data = self.read_data(self.file_path, self.delimiter)

        # Validate column names format (and use transposed DataFrame if necessary)
        self.data = self.validate_column_names(self.data)

        # Validate cell values
        self.validate_cell_values(self.data)

        return self.data



# %% LRP metadata validation
from pandas import DataFrame


class MetaData:
    def __init__(self, file_path: str, delimiter: str = None):
        """
        Initialize the MetaData object by loading and validating the metadata table.

        Args:
            file_path (str): Path to the input file (Excel, CSV, or tab-separated).
            delimiter (str, optional): Delimiter for the file (None for Excel).
        """
        self.file_path = file_path
        self.delimiter = delimiter
        self.data = self.load_data()

    def load_data(self) -> DataFrame:
        """
        Load the metadata table from the file.

        Returns:
            pd.DataFrame: Loaded DataFrame.

        Raises:
            ValueError: If the file type is unsupported.
        """
        if self.file_path.endswith(".csv") or (
            self.delimiter and self.file_path.endswith(".txt")
        ):
            df = pd.read_csv(self.file_path, delimiter=self.delimiter, index_col=0)
        elif self.file_path.endswith(".xlsx"):
            df = pd.read_excel(self.file_path, index_col=0)
        else:
            raise ValueError(
                "Unsupported file type. Use Excel (.xlsx), CSV, or tab-separated files."
            )

        return df

    def validate_data_indices(self, data_df: pd.DataFrame) -> None:
        """
        Validate that the metadata table index matches the data table index.

        Args:
            data_df (pd.DataFrame): Data table DataFrame.

        Raises:
            ValueError: If the indices do not match.
        """
        if not self.data.index.equals(data_df.index):
            raise ValueError(
                "The index of the metadata table does not match the index of the data table."
            )
        
    
    def match_index_with_lrp_df(self, lrp_df: pd.DataFrame) -> pd.DataFrame:
        """
        Matches the indices of the lrp_df DataFrame with the metadata_df DataFrame and returns the filtered metadata_df.

        Args:
            lrp_df (pd.DataFrame): DataFrame whose indices will be used for filtering.
            metadata_df (pd.DataFrame): DataFrame to be filtered based on the indices of lrp_df.

        Returns:
            pd.DataFrame: Filtered metadata_df containing only the rows with indices present in lrp_df.
        """
        indices = lrp_df.index
        self.data = self.data.loc[indices]
        return self
    
    def summarize(self) -> DataFrame:
        """
        Produce a summary and description of the metadata table.

        Returns:
            pd.DataFrame: DataFrame containing summary statistics for the metadata table.
        """
        summary_data = []

        for col in self.data.columns:
            col_data = {
                "Column Name": col,
                "Data Type": self.data[col].dtype,
                "Missing Values": self.data[col].isnull().sum(),
                "Unique Values": self.data[col].nunique(),
            }

            if self.data[col].dtype == "object":
                unique_values = self.data[col].nunique()
                if unique_values <= 10:
                    col_data["Categories"] = list(self.data[col].unique())
                else:
                    col_data["Categories"] = "Too many to display"
                col_data["Parameter Type"] = "Categorical"
            elif self.data[col].dtype in ["int64", "int32"]:
                unique_values = self.data[col].nunique()
                if unique_values == 2:
                    col_data["Parameter Type"] = "Binary"
                else:
                    col_data["Parameter Type"] = "Integer"
            elif self.data[col].dtype in ["float64", "float32"]:
                col_data["Parameter Type"] = "Numeric"
            else:
                col_data["Parameter Type"] = "Other"

            summary_data.append(col_data)

        summary_df = pd.DataFrame(summary_data)
        return summary_df


