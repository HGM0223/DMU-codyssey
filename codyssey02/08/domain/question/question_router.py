from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Question
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from database import get_db_dep

# FastAPI 라우터 객체 생성
router = APIRouter(
    prefix='/api/question',
    tags=['question'],
)

# Pydantic 모델 정의 (질문에 대한 응답 DTO)
class QuestionSchema(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime

    # v2 방식 
    model_config = ConfigDict(from_attributes=True)
    '''

    문제 7 - 보너스 과제에 대한 설명

     from_attributes=True 설정은 pydantic이 ORM 모델(여기서는 SQLAlchemy 모델)에서 데이터를 가져올 수 있도록 함
     from_attributes=False 설정이 기본값으로, 딕셔너리 형태의 데이터에서만 값을 가져올 수 있어서 ORM과 호환되지 않음
     
     1) GET요청시 FastAPI는 question_list 엔드포인트에서 QuestionListSchema를 반환 (get_db_dep함수로 db파라미터로 DB세션이 전달됨)
     2) 'questions 변수'에 DB에서 조회한 Question객체 리스트가 할당됨 (DB에서 조회된 ORM모델 객체들)
     3) QuestionListSchema의 questions 필드는 List[QuestionSchema] 타입인데 dict형태가 아닌 Question ORM모델 객체들이('questions 변수'에 담긴) 들어감 -> Pydantic은 dict형태를 기대하여 오류 발생
     4) 이때 QuestionSchema 모델의 model_config에서 from_attributes=True로 설정되어 있어서 Pydantic이 ORM모델 객체에서 속성값을 추출할 수 있게 됨 
        (questions에서 각각의 레코드의 id, subject, content, create_date를 QuestionSchema에 연결해줌) -> 오류 해결

     요청 -> DB에서 SQLAlchemy ORM모델 조회 -> Pydantic변환 -> JSON 응답
    
    '''

    # v1 일 때 Config 클래스를 만들어서 ORM모델과 호환되도록 설정
    #class Config:
    #    orm_mode = True # ORM 모델과 호환되도록 설정(Question을 Pydantic모델로 변환)

# 질문 목록 응답 DTO
class QuestionListSchema(BaseModel):
    count: int
    questions: List[QuestionSchema]


@router.get('/list', response_model=QuestionListSchema)
async def question_list(db: Session = Depends(get_db_dep)) -> QuestionListSchema:
    """
    질문 목록을 반환하는 엔드포인트.
    - HTTP 메서드: GET
    - URL: /api/question/list
    """
    
    # DB에서 목록 조회
    '''
     questions는 List[SQLAlchemy ORM Question 객체] 형태
    '''
    questions = db.query(Question).order_by(
        Question.create_date.desc(),
    ).all()
    

    return QuestionListSchema(
        count= len(questions),
        questions= questions,
    )
