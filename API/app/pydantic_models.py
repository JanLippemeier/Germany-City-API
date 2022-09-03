from pydantic import BaseModel

class api_key_body(BaseModel):
    key: str

class state_info(BaseModel):
    name: str
    city_count: int
    population: int
    female_population: int
    area: int

class city_info(BaseModel):
    id: int
    name: str
    postal_code: int
    state_name: str
    population: int
    female_population: int
    area: float
    latitude: float
    longitude: float