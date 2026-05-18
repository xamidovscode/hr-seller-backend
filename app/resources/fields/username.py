from typing import Annotated

from pydantic import StringConstraints

UsernameField = Annotated[
    str,
    StringConstraints(
        min_length=4,
        max_length=32,
        pattern=r"^[a-zA-Z0-9_]+$"
    )
]