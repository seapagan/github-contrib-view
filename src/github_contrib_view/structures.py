"""Define any structures required by the program."""

from typing import TypedDict


# Define a TypedDict for options
class ContribOptions(TypedDict):
    """TypedDict for contribution display options."""

    ascii: bool
    summary: bool
    username: str
    token: str
