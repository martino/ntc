from user import *
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    overall = Column(Float)
    quality = Column(Float)
    fact = Column(Integer)
    fairness = Column(Integer)
    sourcing = Column(Integer)

    def __init__(self, ovr, qlty, fact, fair, source):
        self.overall = ovr
        self.quality = qlty
        self.fact    = fact
        self.fairness= fair
        self.sourcing=source


