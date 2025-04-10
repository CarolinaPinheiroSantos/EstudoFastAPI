from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Cinema(BaseModel):
    id: Optional[int] = None
    filme: str 
    classificacao: int
    genero: str
    sobre: str
    capa: str
    data_horario: str