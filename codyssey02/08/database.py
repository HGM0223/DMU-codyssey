# ORM Object-Relational Mapping
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy.orm import Session

DATABASE_URL = 'sqlite:///C:/Users/user/Documents/DMU-codyssey/codyssey02/08/testCodyssey.db'

# SQLAlchemy 연결을 위한 URL 설정
engine = create_engine(
    DATABASE_URL,        # SQLite 데이터베이스 경로
    echo=True,           # SQL 로깅 보고 싶지 않으면 False
    pool_pre_ping=True   # 연결 유효성 검사 활성화
)

# 세션 로컬 클래스 생성 (DB 세션 관리용)
SessionLocal = sessionmaker(
    autocommit=False,    # 자동 커밋 비활성화
    autoflush=False,     # 자동 플러시 비활성화
    bind=engine          # DB 바인드
)

# 베이스 클래스 생성
Base = declarative_base() 

# Dependency 함수: DB 세션을 요청 시마다 생성하고 종료
'''
def get_db() -> Session :
  db = SessionLocal()
  try:
      yield db
  finally:
      db.close()
'''

@contextmanager
def get_db() -> Generator[Session, None, None]:
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

  '''
   Docstring for get_db_context
   contextlib의 contextmanager 데코레이터를 사용하여 DB세션을 컨텍스트 매니저로 제공
   
   :return: Description
   :rtype: Generator[Session, None, None]
   호출시 Session객체를 생성하고 반환은 Generator로 처리
   '''
  
def get_db_dep() -> Generator[Session, None, None]:
    '''
    FastAPI Depends에서 사용할 의존성 함수.
    내부적으로 위에서 만든 get_db() 컨텍스트 매니저를 사용한다.
    '''
    with get_db() as db:
        yield db