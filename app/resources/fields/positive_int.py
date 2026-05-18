from typing import Annotated

from pydantic import Field


PositiveIntField = Annotated[
    int,
    Field(gt=0)
]