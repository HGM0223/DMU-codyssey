import requests

BASE_URL = "http://127.0.0.1:8000/to_do"


def add_todo():
    title = input("제목을 입력하세요: ")
    description = input("설명을 입력하세요(없으면 엔터): ")

    data = {
        "title": title,
        "description": description if description.strip() != "" else None,
    }

    # 서버의 /to_do/add 로 POST 요청
    resp = requests.post(f"{BASE_URL}/add", json=data)
    print(f"[응답 코드] {resp.status_code}")
    print("[응답 바디]")
    print(resp.json())


def list_todos():
    resp = requests.get(f"{BASE_URL}/list")
    print(f"[응답 코드] {resp.status_code}")
    data = resp.json()
    print(f"총 개수: {data['count']}")
    for idx, todo in enumerate(data["todos"]):
        print(f"- ID: {idx}, 제목: {todo.get('title')}, 설명: {todo.get('description')}")


def get_todo():
    todo_id = int(input("조회할 할 일 ID를 입력하세요: "))
    resp = requests.get(f"{BASE_URL}/{todo_id}")
    print(f"[응답 코드] {resp.status_code}")
    print("[응답 바디]")
    try:
        print(resp.json())
    except Exception:
        print(resp.text)


def update_todo():
    todo_id = int(input("수정할 할 일 ID를 입력하세요: "))
    title = input("새 제목을 입력하세요: ")
    description = input("새 설명을 입력하세요(없으면 엔터): ")

    data = {
        "title": title,
        "description": description if description.strip() != "" else None,
    }

    resp = requests.put(f"{BASE_URL}/{todo_id}", json=data)
    print(f"[응답 코드] {resp.status_code}")
    try:
        print(resp.json())
    except Exception:
        print(resp.text)


def delete_todo():
    todo_id = int(input("삭제할 할 일 ID를 입력하세요: "))
    resp = requests.delete(f"{BASE_URL}/{todo_id}")
    print(f"[응답 코드] {resp.status_code}")
    try:
        print(resp.json())
    except Exception:
        print(resp.text)


def main():
    while True:
        print("\n===== TODO 클라이언트 =====")
        print("1. 할 일 추가 (POST /to_do/add)")
        print("2. 전체 목록 조회 (GET /to_do/list)")
        print("3. 개별 조회 (GET /to_do/{id})")
        print("4. 수정 (PUT /to_do/{id})")
        print("5. 삭제 (DELETE /to_do/{id})")
        print("0. 종료")
        choice = input("메뉴 선택: ").strip()

        if choice == "1":
            add_todo()
        elif choice == "2":
            list_todos()
        elif choice == "3":
            get_todo()
        elif choice == "4":
            update_todo()
        elif choice == "5":
            delete_todo()
        elif choice == "0":
            print("종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")


if __name__ == "__main__":
    main()
