from fastmcp import FastMCP

mcp = FastMCP("Test Server")


@mcp.tool()
def test_tool() -> str:
    """A simple test tool"""
    return "It works!"


if __name__ == '__main__':
    mcp.run()
