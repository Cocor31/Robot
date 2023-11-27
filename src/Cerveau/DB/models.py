from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, Text


class Base(DeclarativeBase):
    pass

class Phrase(Base):
    __tablename__ = "phrases"
    id = Column(Integer, primary_key=True)
    demande = Column(Text, unique=True)
    reponse = Column(Text, nullable=False)

    def __repr__(self):
        return f"<Phrase demande={self.demande} reponse={self.reponse}>"