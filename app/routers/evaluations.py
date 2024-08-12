# routers/evaluations.py
from http.client import HTTPException
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app import models, database
from app.services import audio_processing, text_evaluation, accent_evaluation
from app.services.text_evaluation import evaluate_speech

router = APIRouter()

@router.post("/evaluations/")
async def create_evaluation(user_id: int = Form(...), audio_file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    evaluation_result = await evaluate_speech(audio_file)

    # Create evaluation in database
    new_evaluation = models.Evaluation(
        user_id=user_id,
        audio_file_path=evaluation_result["audio_file_path"],
        transcription=evaluation_result["transcription"],
        accent_score=evaluation_result["accent_score"],
        vocabulary_score=evaluation_result["vocabulary"]["score"],
        grammar_score=evaluation_result["grammar"]["score"],
        conjugation_score=evaluation_result["conjugation"]["score"],
        culture_score=evaluation_result["culture"]["score"],
        expression_score=evaluation_result["expression"]["score"]
    )
    db.add(new_evaluation)
    db.commit()
    db.refresh(new_evaluation)

    return evaluation_result

@router.get("/evaluations/{evaluation_id}")
async def read_evaluation(evaluation_id: int, db: Session = Depends(database.get_db)):
    evaluation = db.query(models.Evaluation).filter(models.Evaluation.id == evaluation_id).first()
    if evaluation is None:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return evaluation