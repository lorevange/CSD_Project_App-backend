from sqlalchemy import Column, ForeignKey, Integer, String, Time, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Day(Base):
    __tablename__ = "Day"

    id = Column(Integer, primary_key=True, autoincrement=True)
    week_day = Column(Integer, nullable=False)  # e.g., sunday=0...saturday=6
    opening = Column(Time, nullable=False)  # time of day opening
    closing = Column(Time, nullable=False)  # time of day closing
    is_closed = Column(Boolean, nullable=False)
    clinic_id = Column(Integer, ForeignKey("Clinic.id"), nullable=False)

    clinic = relationship("Clinic")
