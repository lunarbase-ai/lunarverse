from typing import Any

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType

import pandas as pd
import duckdb

class CsvQuery(
    LunarComponent,
    component_name="CsvQuery",
    component_group=ComponentGroup.DATA_EXTRACTION,
    component_description="Query CSV files using SQL",
    output_type=DataType.TEXT, 
    description="Query a CSV file using SQL",
    input_types={"query": DataType.TEXT, "csv_files": DataType.JSON},
):
    def __init__(self, **kwargs: Any):
        super().__init__(configuration=kwargs)

    def run(self, query: str, csv_files: dict) -> Any:
        for table_name, file_path in csv_files.items():
            try:
                df = pd.read_csv(file_path)
            except Exception as e:
                raise Exception(f"Error reading '{file_path}' for table '{table_name}': {e}")
            globals()[table_name] = df


        try:
            result_df = duckdb.sql(query).fetchdf()
        except Exception as e:
            raise Exception(f"Error executing query: {e}")
        
        for table_name in csv_files.keys():
            globals().pop(table_name, None)
        
        csv_string = result_df.to_csv(index=False, sep=",")
        return csv_string