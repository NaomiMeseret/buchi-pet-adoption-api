from typing import Any, Literal

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    status: Literal["error"] = "error"
    message: str
    error_code: str
    details: list[dict[str, Any]] | None = None
