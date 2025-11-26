from fastapi import FastAPI, APIRouter, HTTPException # FastAPI는 웹 어플리케이션 프레임워크, APRRouter는 API를 관리하기 위한 라우터 객체
from typing import Dict, List, Any
from pydantic import BaseModel
from typing import Optional

class TodoItem(BaseModel):
    title: str                  # 반드시 있어야 하는 필드
    description: Optional[str] = None  # 없어도 되는 필드

router = APIRouter(prefix='/to_do', tags=['to_do']) 
todo_list : List[Dict[str,Any]] = []   # key:str, value:any 형태의 딕셔너리를 저장하는 리스트


# =========================
# 1) 할 일 추가 (POST)
# =========================
@router.post('/add')  # 실제 경로: /to_do/add
async def add_todo(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    새로운 할 일을 추가하는 엔드포인트.
    - HTTP 메서드: POST
    - URL: /to_do/add
    - Body: 임의의 JSON (Dict[str, Any])
    """

    # 입력 Dict가 비어 있을 때 경고 반환
    if not item:
        return {
            'status': 'error',
            'message': '빈 값은 추가할 수 없습니다.'
        }

    todo_list.append(item)

    return {
        'status': 'ok',
        'added': item,
        'count': len(todo_list),
    }


# =========================
# 2) 전체 목록 조회 (GET)
# =========================
@router.get('/list') # GET 요청을 처리하는 엔드포인트 정의, 실제 경로는 /to_do/list
async def retrieve_todo() -> Dict[str, Any]:
    return {
        'count': len(todo_list),
        'todos': todo_list,
    }


# =========================
# 3) 개별 조회 (GET) - get_single_todo
# =========================
@router.get('/{todo_id}')
async def get_single_todo(todo_id: int) -> Dict[str, Any]:
    """
    특정 ID의 to_do list 하나만 조회하는 엔드포인트.
    - HTTP 메서드: GET
    - URL: /to_do/{todo_id}
      예: /to_do/0, /to_do/1 ...
    - todo_id: 경로 매개변수 (리스트 인덱스를 아이디처럼 사용)
    """
    # todo_id가 리스트 범위를 벗어난 경우 404 에러 반환
    if todo_id < 0 or todo_id >= len(todo_list):
        raise HTTPException(status_code=404, detail='해당 ID의 할 일이 존재하지 않습니다.')

    return {
        'status': 'ok',
        'id': todo_id,
        'todo': todo_list[todo_id],
    }


# =========================
# 4) 수정 (PUT) - update_todo
# =========================
@router.put('/{todo_id}')
async def update_todo(todo_id: int, item: TodoItem) -> Dict[str, Any]:
    """
    특정 ID의 할 일을 수정하는 엔드포인트.
    - HTTP 메서드: PUT
    - URL: /to_do/{todo_id}
    - Body: TodoItem 모델 형태(JSON)
    """
    if todo_id < 0 or todo_id >= len(todo_list):
        raise HTTPException(status_code=404, detail='수정하려는 ID의 할 일이 존재하지 않습니다.')

    # Pydantic 모델(TodoItem)을 dict로 변환해서 기존 리스트에 덮어쓰기
    updated_item = item.model_dump()
    todo_list[todo_id] = updated_item

    return {
        'status': 'ok',
        'id': todo_id,
        'updated': updated_item,
    }


# =========================
# 5) 삭제 (DELETE) - delete_single_todo
# =========================
@router.delete('/{todo_id}')
async def delete_single_todo(todo_id: int) -> Dict[str, Any]:
    """
    특정 ID의 할 일을 삭제하는 엔드포인트.
    - HTTP 메서드: DELETE
    - URL: /to_do/{todo_id}
    """
    if todo_id < 0 or todo_id >= len(todo_list):
        raise HTTPException(status_code=404, detail='삭제하려는 ID의 할 일이 존재하지 않습니다.')

    # pop()으로 해당 인덱스의 항목을 제거하면서 반환받음
    deleted_item = todo_list.pop(todo_id)

    return {
        'status': 'ok',
        'id': todo_id,
        'deleted': deleted_item,
        'count': len(todo_list),
    }

todo_app = FastAPI()
todo_app.include_router(router)
    
    
if __name__ == "__main__":
    #todo_app = FastAPI()
    #todo_app.include_router(router)
    import uvicorn
    uvicorn.run(todo_app, host='127.0.0.1', port=8000, reload=True)

# curl 실행 예시
# 1) 추가
# curl.exe --% -X POST "http://127.0.0.1:8000/to_do/add" 
# -H "Content-Type: application/json" 
# -d "{\"title\": \"공부하기22\", \"description\": \"FastAPI 실습 두 번째 내용 보내기\"}"