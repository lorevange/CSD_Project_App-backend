from datetime import datetime

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Review(Base):
    __tablename__ = "Review"
    __table_args__ = (
        UniqueConstraint("author_id", "doctor_id", name="uq_author_doctor_review"),
        CheckConstraint("rating >= 0 AND rating <= 5", name="ck_review_rating_range"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    doctor_id = Column(Integer, ForeignKey("Doctor.id"), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("User.id"), nullable=False, index=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    doctor = relationship("Doctor", back_populates="reviews")
    author = relationship("User", back_populates="reviews_authored")
