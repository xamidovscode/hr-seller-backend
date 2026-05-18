from typing import Annotated

from pydantic import BaseModel, Field


PercentageField = Annotated[
    float,
    Field(ge=0, le=100)
]