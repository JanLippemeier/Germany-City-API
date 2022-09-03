from pydantic import BaseModel

class api_key_body(BaseModel):
    key: str