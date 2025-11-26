from fastapi import FastAPI, APIRouter # FastAPI는 웹 어플리케이션 프레임워크, APRRouter는 API를 관리하기 위한 라우터 객체
from typing import Dict, List, Any

router = APIRouter(prefix='/to_do', tags=['to_do']) 
todo_list : List[Dict[str,Any]] = []   # key:str, value:any 형태의 딕셔너리를 저장하는 리스트

@router.post('/add') # POST 요청을 처리하는 엔드포인트 정의, 실제 경로는 /to_do/add 
async def add_todo(item: Dict[str, Any]) -> Dict[str,Any]:
    
    # 입력 Dict가 비어 있을 때 경고 반환
    if not item:
        return{
            'status': 'error',
            'message': '빈 값은 추가할 수 없습니다.'
        }
    
    todo_list.append(item)
    return {
        'status': 'ok',
        'added': item,
        'count': len(todo_list),
    }
        
@router.get('/list') # GET 요청을 처리하는 엔드포인트 정의, 실제 경로는 /to_do/list
async def retrieve_todo() -> Dict[str, Any]:
    return {
        'count': len(todo_list),
        'todos': todo_list,
    }
    
todo_app = FastAPI()
todo_app.include_router(router)
    
    
if __name__ == "__main__":
    #todo_app = FastAPI()
    #todo_app.include_router(router)
    import uvicorn
    uvicorn.run(todo_app, host='127.0.0.1', port=8000, reload=True)