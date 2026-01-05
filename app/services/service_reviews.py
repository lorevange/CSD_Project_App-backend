from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models
from app.config import settings
from app.queries.query_doctors import get_doctor_by_id
from app.queries.query_reviews import get_review_by_id, get_reviews_for_doctor
from google import genai
from google.api_core.exceptions import GoogleAPIError, ResourceExhausted, NotFound
from openai import APIStatusError, OpenAI


def create_review(doctor_id: int, payload, current_user: models.User, db: Session) -> models.Review:
    doctor = get_doctor_by_id(doctor_id, db)

    if current_user.profile == "doctor" and current_user.doctor and current_user.doctor.id == doctor.id:
        raise HTTPException(status_code=400, detail="Doctors cannot review themselves")

    existing = (
        db.query(models.Review)
        .filter(
            models.Review.doctor_id == doctor.id,
            models.Review.author_id == current_user.id,
        )
        .first()
    )
    if existing:
        if existing.deleted_at is not None:
            existing.rating = payload.rating
            existing.comment = payload.comment
            existing.deleted_at = None
            existing.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(existing)
            return existing
        raise HTTPException(status_code=400, detail="You have already reviewed this doctor")

    review = models.Review(
        doctor_id=doctor.id,
        author_id=current_user.id,
        rating=payload.rating,
        comment=payload.comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def list_reviews_for_doctor(doctor_id: int, db: Session, skip: int = 0, limit: int = 50) -> list[models.Review]:
    get_doctor_by_id(doctor_id, db)
    return get_reviews_for_doctor(doctor_id, db, skip=skip, limit=limit)


def update_review(review_id: int, payload, current_user: models.User, db: Session) -> models.Review:
    review = get_review_by_id(review_id, db)
    if review.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own reviews")

    if payload.rating is not None:
        review.rating = payload.rating
    if payload.comment is not None:
        review.comment = payload.comment
    review.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(review)
    return review


def delete_review(review_id: int, current_user: models.User, db: Session) -> None:
    review = get_review_by_id(review_id, db)
    if review.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own reviews")
    review.deleted_at = datetime.utcnow()
    review.updated_at = datetime.utcnow()
    db.commit()


def summarize_reviews_for_doctor(doctor_id: int, db: Session, language: str | None = None) -> dict:
    doctor = get_doctor_by_id(doctor_id, db)
    reviews = get_reviews_for_doctor(doctor.id, db, skip=0, limit=200)
    if not reviews:
        return {"summary": "No reviews available for this doctor yet.", "word_count": 8}

    comments = [review.comment.strip() for review in reviews if review.comment]
    preferred_language = (language or "English").strip() or "English"
    summary = ""
    if settings.gemini_api_key:
        summary = _summarize_with_gemini(comments, doctor.id, preferred_language)
    elif settings.openai_api_key:
        summary = _summarize_with_openai(comments, doctor.id, preferred_language)
    else:
        raise HTTPException(status_code=500, detail="No LLM API key configured (Gemini or OpenAI).")

    words = summary.split()
    if len(words) > 100:
        summary = " ".join(words[:100])
    return {"summary": summary, "word_count": len(summary.split())}


def _summarize_with_gemini(comments: list[str], doctor_id: int, language: str) -> str:
    client = genai.Client(api_key=settings.gemini_api_key)
    prompt_reviews = "\n".join(f"- {comment}" for comment in comments)
    prompt = (
        "You summarize patient reviews for doctors. Be concise, neutral, and avoid PII.\n"
        "Reviews:\n"
        f"{prompt_reviews}\n\n"
        "Summarize the above reviews in no more than 100 words. Mention common positives and negatives. "
        "Do not use markdown. Keep it factual. Respond in {language}."
    )
    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt.format(language=language),
        )
    except ResourceExhausted as exc:  # pragma: no cover - external call
        raise HTTPException(
            status_code=503, detail="LLM temporarily unavailable (quota or rate limit). Try again later."
        )
    except NotFound as exc:  # pragma: no cover - external call
        raise HTTPException(
            status_code=502,
            detail="Requested Gemini model not found. Update gemini_model or check your API version.",
        )
    except GoogleAPIError as exc:  # pragma: no cover - external call
        raise HTTPException(status_code=502, detail=f"Failed to generate summary: {exc}")
    except Exception as exc:  # pragma: no cover - external call
        raise HTTPException(status_code=502, detail=f"Failed to generate summary: {exc}")
    text = (response.text or "").strip() if response else ""
    return text


def _summarize_with_openai(comments: list[str], doctor_id: int, language: str) -> str:
    prompt_reviews = "\n".join(f"- {comment}" for comment in comments)
    client = OpenAI(api_key=settings.openai_api_key)
    messages = [
        {
            "role": "system",
            "content": (
                "You summarize patient reviews for doctors. Be concise, neutral, avoid PII, and respond in {language}."
            ).format(language=language),
        },
        {
            "role": "user",
            "content": (
                "Reviews:\n"
                "{reviews}\n\n"
                "Summarize the above reviews in no more than 100 words. "
                "Mention common positives and negatives. Keep it factual. Respond in {language}."
            ).format(doctor_id=doctor_id, reviews=prompt_reviews, language=language),
        },
    ]

    try:
        completion = client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            max_tokens=220,
            temperature=0.3,
        )
    except APIStatusError as exc:  # pragma: no cover - external call
        if exc.status_code == 429:
            raise HTTPException(
                status_code=503, detail="LLM temporarily unavailable (quota or rate limit). Try again later."
            )
        raise HTTPException(status_code=502, detail=f"Failed to generate summary: {exc}")
    except Exception as exc:  # pragma: no cover - external call
        raise HTTPException(status_code=502, detail=f"Failed to generate summary: {exc}")

    return completion.choices[0].message.content.strip() if completion.choices else ""
