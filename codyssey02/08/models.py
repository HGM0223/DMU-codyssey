# ORM Object-Relational Mapping
from sqlalchemy import DateTime, create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from database import Base

# 모델 정의 - Question 테이블
class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(
        DateTime, nullable=False, default=datetime.now  
    )