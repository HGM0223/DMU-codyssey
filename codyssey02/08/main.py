# ORM Object-Relational Mapping
from sqlalchemy import engine_from_config, pool
from fastapi import FastAPI
from domain.question import question_router

'''
alembic 사용법 
alembic revision --autogenerate -m "create question table" (마이그레이션 파일 생성)
alembic upgrade head (최신 버전으로 DB 스키마 업그레이드)
'''

app = FastAPI() # 메인 FastAPI 애플리케이션 생성 (서버)

app.include_router(question_router.router) # question 도메인 라우터 포함

'''
domain.question.question_router.py중 일부 
router = APIRouter(
    prefix='/api/question',
    tags=['question'],
)
FastAPI 애플리케이션에 요청이 들어오면 /aoi/question 경로로 라우팅 되어 question_router의 엔트포인트가 처리
'''

if __name__ == '__main__':
    import uvicorn
    
    # 메인 애플리케이션 실행
    uvicorn.run(
        app,
        host='127.0.0.1',
        port=8000,
        reload=True,
    )
