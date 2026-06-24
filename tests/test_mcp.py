from mcp.snowflake_mcp import SnowflakeMCP

mcp = SnowflakeMCP()

print("\n===== KPI DATA =====")
print(mcp.get_kpi_data())

print("\n===== INCIDENTS =====")
print(mcp.get_incidents())