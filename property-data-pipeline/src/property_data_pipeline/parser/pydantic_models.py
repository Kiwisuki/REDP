from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class MainInfo(BaseModel):
    house_number: Optional[str] = Field(None, alias='Namo numeris:')
    apartment_number: str = Field(None, alias='Buto numeris:')
    area: Optional[str] = Field(None, alias='Plotas:')
    room_count: Optional[str] = Field(None, alias='Kambarių sk.:')
    floor: Optional[str] = Field(None, alias='Aukštas:')
    total_floors: Optional[str] = Field(None, alias='Aukštų sk.:')
    year: Optional[str] = Field(None, alias='Metai:')
    building_type: Optional[str] = Field(None, alias='Pastato tipas:')
    heating: Optional[str] = Field(None, alias='Šildymas:')
    condition: Optional[str] = Field(None, alias='Įrengimas:')
    energy_class: Optional[str] = Field(
        None, alias='Pastato energijos suvartojimo klasė:'
    )
    features: Optional[str] = Field(None, alias='Ypatybės:')
    additional_rooms: Optional[str] = Field(None, alias='Papildomos patalpos:')
    additional_equipment: Optional[str] = Field(None, alias='Papildoma įranga:')
    security: Optional[str] = Field(None, alias='Apsauga:')


class Distances(BaseModel):
    nearest_kindergarten: Optional[str] = Field(None, alias='Artimiausias darželis')
    nearest_school: Optional[str] = Field(None, alias='Artimiausia mokymo įstaiga')
    nearest_store: Optional[str] = Field(None, alias='Artimiausia parduotuvė')


class Parsed(BaseModel):
    price: str
    main_info: MainInfo
    description: str
    distances: Distances
    images: List[str]
    coordinates: List[float]
    is_map_accurate: bool
