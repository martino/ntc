from user import *
from sqlalchemy import ForeignKey, Float
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

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, backref=backref('reviews', order_by=id))
    
    def __init__(self, ovr, qlty, fact=-1, fair=-1, source=-1):
        self.overall = ovr
        self.quality = qlty
        self.fact    = fact
        self.fairness= fair
        self.sourcing=source


