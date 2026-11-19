from pydantic import BaseModel, Field

class BaseJsonRPC(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: list = Field(default=[])
    id: int