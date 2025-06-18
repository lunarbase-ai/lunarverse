import pytest
from postgres_query import PostgresQuery

@pytest.mark.asyncio
async def test_postgres_query_select():
    component = PostgresQuery()
    result = await component.run(
        query="SELECT 1 as test",
        params=None
    )
    assert result["success"] is True
    assert "columns" in result
    assert "rows" in result
    assert result["columns"] == ["test"]
    assert result["rows"] == [(1,)]

@pytest.mark.asyncio
async def test_postgres_query_with_params():
    component = PostgresQuery()
    result = await component.run(
        query="SELECT %s as param1, %s as param2",
        params=("value1", "value2")
    )
    assert result["success"] is True
    assert result["columns"] == ["param1", "param2"]
    assert result["rows"] == [("value1", "value2")]

@pytest.mark.asyncio
async def test_postgres_query_error():
    component = PostgresQuery()
    result = await component.run(
        query="INVALID SQL QUERY",
        params=None
    )
    assert result["success"] is False
    assert "error" in result 