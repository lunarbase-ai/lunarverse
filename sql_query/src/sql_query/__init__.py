import csv
import io
from lunarcore.connectors.sql import SQLConnector
from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType


class SQLQuery(
    LunarComponent,
    component_name="SQL Query",
    component_description="""Enables users to run SQL queries on relational databases, facilitating data retrieval, manipulation, and analysis through structured commands.
    Output (str): the query result.""",
    input_types={"query": DataType.TEXT},
    output_type=DataType.CSV,
    component_group=ComponentGroup.DATABASES,
    driver_name="",
    username="$LUNARENV::SQL_USERNAME",
    password="$LUNARENV::SQL_PASSWORD",
    host=None,
    port=None,
    database=None,
    ssl_mode="require",
):
    def __init__(self, **kwargs):
        super().__init__(configuration=kwargs)
        
        self.sql_connector = SQLConnector(
            driver_name=self.configuration.get("driver_name") or "",
            username=self.configuration.get("username") or "",
            password=self.configuration.get("password") or "",
            host=self.configuration.get("host") or "",
            port=self.configuration.get("port") or "",
            database=self.configuration.get("database") or "",
            ssl_mode=self.configuration.get("ssl_mode") or "",
        )

    def run(self, query: str):
        result = self.sql_connector.query(query)
        output = io.StringIO()
        if len(result) > 0:
            headers = list(result[0].keys())
            writer = csv.DictWriter(output, fieldnames=headers)
            writer.writeheader()
            writer.writerows(result)

        return "\n".join(output.getvalue().splitlines())
