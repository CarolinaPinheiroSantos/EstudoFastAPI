from sqlalchemy import Column, Integer, String
from database import Base

class Cinema(Base):
    __tablename__ = 'cinema'
    
    id = Column(Integer, primary_key=True, index=True)
    filme = Column(String(50))
    classificacao = Column(Integer)
    genero = Column(String(50))
    sobre = Column(String(150))
    capa = Column(String(100))
    data_horario = Column(String(20))
