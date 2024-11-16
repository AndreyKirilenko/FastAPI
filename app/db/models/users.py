from db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password= Column(String, nullable=False)
    is_superuser = Column(Boolean(), default=False)
    is_user = Column(Boolean(), default=True)
    # is_active = relationship