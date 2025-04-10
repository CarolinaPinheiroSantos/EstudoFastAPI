from typing import Optional
from pydantic import BaseModel

class Pato(BaseModel):
    id: Optional[int] = None
    nome: str 
    especie: str
    idade: int
    cor: str
    foto: str 
    