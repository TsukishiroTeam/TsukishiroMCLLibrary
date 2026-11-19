from niquests import AsyncSession
from typing import Optional
from pydantic import BaseModel
import json

session = AsyncSession()

@retry
async def fetch_retry():
    pass

async def get_string():
    pass

async def get_bytearray():
    pass

async def upload_string(url: str, method: str = "POST"):
    pass


async def upload_json(url: str, method: str = "POST", data: Optional[dict[str,str] | BaseModel] = None):
    data_string = data.model_dump_json() if isinstance(data, BaseModel) else json.dumps(data)

    pass