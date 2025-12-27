from fastmcp import FastMCP

import random
import json


mcp = FastMCP("Simple calculator server")


@mcp.tool
def add(a: int, b: int) -> int:
    '''
    Add Two Numbers

    :param a: Description
    :type a: int
    :param b: Description
    :type b: int
    :return: Description
    :rtype: int
    '''
    return a+b
# Tool: Generate random number


@mcp.tool
def random_number(min: int, max: int) -> int:
    '''
    Generate random number

    :param min: Description
    :type min: int
    :param max: Description
    :type max: int
    :return: Description
    :rtype: int
    '''
    return random.randint(min, max)

# Resource: Server information


@mcp.resource('info://server')
def server_info() -> str:
    '''
    Server information

    :return: Description
    :rtype: str
    '''
    return json.dumps({
        "name": "Simple calculator server",
        "version": "0.0.1",
        "description": "Simple calculator server",
        "tools": ["add", "random_number"],
        "author": "Sakib Malik"
    }, indent=4)


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
