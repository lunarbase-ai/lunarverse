import io
import csv
import sqlite3
from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType


class SqliteQuery(
    LunarComponent,
    component_name="Sqlite Query",
    component_description="""Connects to a SQLite database and returns the result of a query in CSV format.""",
    input_types={"db_path": DataType.TEXT, "query": DataType.TEXT},
    output_type=DataType.CSV,
    component_group=ComponentGroup.DATABASES,
):
    def __init__(self, **kwargs):
        super().__init__(configuration=kwargs)

    def run(self, db_path: str, query: str):
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute(query)

            rows = cursor.fetchall()
            headers = (
                [desc[0] for desc in cursor.description] if cursor.description else []
            )

            output = io.StringIO()
            writer = csv.writer(output)

            if headers:
                writer.writerow(headers)
            writer.writerows(rows)

            connection.close()

            return output.getvalue().strip()
        except Exception as e:
            return str(e)
