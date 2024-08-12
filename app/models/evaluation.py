# models/evaluation.py

from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    audio_file_path = Column(String)
    transcription = Column(String)
    accent_score = Column(Float)
    vocabulary_score = Column(Float)
    grammar_score = Column(Float)
    conjugation_score = Column(Float)
    culture_score = Column(Float)
    expression_score = Column(Float)
