from mcp.file_mcp import FileMCP
from mcp.snowflake_mcp import SnowflakeMCP


def test_file_mcp():

    print("\n" + "=" * 60)
    print("Testing File MCP")
    print("=" * 60)

    file_mcp = FileMCP()

    df = file_mcp.read_csv("data/kpi_data.csv")

    summary = file_mcp.dataframe_summary(df)

    print("\nDataset Summary")

    print(summary)

    print("\nPreview")

    print(file_mcp.preview(df))


def test_snowflake_mcp():

    print("\n" + "=" * 60)
    print("Testing Snowflake MCP")
    print("=" * 60)

    snowflake = SnowflakeMCP()

    print("\nChecking KPI Table...")

    exists = snowflake.table_exists(
        "AGENTGRAVITY.BUSINESS.KPI_METRICS"
    )

    print("Table Exists :", exists)

    count = snowflake.table_count(
        "AGENTGRAVITY.BUSINESS.KPI_METRICS"
    )

    print("Row Count :", count)

    df = snowflake.execute_query("""

        SELECT *

        FROM AGENTGRAVITY.BUSINESS.KPI_METRICS

        LIMIT 5

    """)

    print("\nPreview")

    print(df)


if __name__ == "__main__":

    test_file_mcp()

    test_snowflake_mcp()