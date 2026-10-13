# A plugin exercising the python-to-json-schema type conversions
from llme.tools import tool

@tool
def wx(city: str, max_temp: float = 40.0, verbose: bool = False, tags: list = None):
    """Return the weather and forecast of a given city"""
    return "sunny"
