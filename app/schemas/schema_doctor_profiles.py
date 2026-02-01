from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.schema_doctor_services import DoctorServiceOut
from app.schemas.schema_reviews import ReviewSummary


class TranslatedText(BaseModel):
    it: Optional[str] = None
    en: Optional[str] = None


class DoctorProfileAppointmentsFilter(BaseModel):
    status: Optional[str] = None
    start_from: Optional[datetime] = Field(default=None, alias="startFrom")
    start_to: Optional[datetime] = Field(default=None, alias="startTo")

    model_config = ConfigDict(populate_by_name=True)


class DoctorProfileReviewsFilter(BaseModel):
    limit: int = 50
    sort: str = "created_at_desc"


class DoctorProfileReviewSummaryFilter(BaseModel):
    language: Optional[str] = None


class DoctorProfileRequest(BaseModel):
    doctor_id: int = Field(alias="doctorId")
    include: List[str] = Field(default_factory=list)
    appointments: Optional[DoctorProfileAppointmentsFilter] = None
    reviews: Optional[DoctorProfileReviewsFilter] = None
    review_summary: Optional[DoctorProfileReviewSummaryFilter] = Field(default=None, alias="reviewSummary")

    model_config = ConfigDict(populate_by_name=True)


class DoctorProfileOut(BaseModel):
    id: int
    name: str
    first_name: str
    last_name: str
    specialization: TranslatedText
    bio: TranslatedText
    information: Optional[str] = None
    services: List[DoctorServiceOut] = Field(default_factory=list)
    price: Optional[Decimal] = None
    address: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    photo: Optional[bytes] = None
    photo_url: Optional[str] = None
    average_rating: float = 0.0
    reviews_count: int = 0


class AppointmentProfileOut(BaseModel):
    id: int
    doctor_id: int
    user_id: int
    start_datetime: datetime
    end_datetime: datetime
    examination_type: str
    notes: Optional[str] = None
    status: str

    model_config = ConfigDict(from_attributes=True)


class ReviewAuthorPublicOut(BaseModel):
    first_name: str
    last_name: str
    photo: Optional[bytes] = None

    model_config = ConfigDict(from_attributes=True)


class ReviewPublicOut(BaseModel):
    id: int
    rating: int
    comment: str
    created_at: datetime
    author: ReviewAuthorPublicOut

    model_config = ConfigDict(from_attributes=True)


class DoctorProfileResponse(BaseModel):
    doctor: DoctorProfileOut
    appointments: Optional[List[AppointmentProfileOut]] = None
    reviews: Optional[List[ReviewPublicOut]] = None
    review_summary: Optional[ReviewSummary] = Field(default=None, alias="reviewSummary")

    model_config = ConfigDict(populate_by_name=True)
