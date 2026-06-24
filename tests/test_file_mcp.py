from mcp.file_mcp import FileMCP

mcp = FileMCP()

mcp.save_report(
    "sample_report.txt",
    "AgentGravity MCP Test"
)

content = mcp.read_report(
    "sample_report.txt"
)

print(content)