from user import *
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

class UserRating(Base):
    __tablename__ = 'user_ratings'

    id          = Column(Integer, primary_key=True)
    
    memberlevel = Column(Float)
    activity    = Column(Float)
    experience  = Column(Float)
    ratings     = Column(Float)
    transparency= Column(Float)
    validation  = Column(Float)
    reviewsion  = Column(Integer)
    answers     = Column(Integer)
    comments    = Column(Integer)
    ratingsrec  = Column(Integer)
    numbersrater= Column(Integer)
    ratingsgiven= Column(Integer)
    
    date        = Column(DateTime)

    user_id     = Column(Integer, ForeignKey('users.id'))
    user        = relationship(User, backref=backref('user_ratings', order_by=id))
    

