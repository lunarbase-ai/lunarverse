from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentModel
from lunarcore.core.typings.datatypes import DataType
from typing import Any, Optional
import pandas as pd
import duckdb

class CsvQuery(
    BaseComponent,
    component_name="CsvQuery",
    component_group=ComponentGroup.DATA_EXTRACTION,
    component_description="Query CSV files using SQL",
    output_type=DataType.JSON, 
    description="Query a CSV file using SQL",
    input_types={"query": DataType.TEXT, "csv_files": DataType.JSON},
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)

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

