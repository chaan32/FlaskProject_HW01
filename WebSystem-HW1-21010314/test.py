# Flask 서버를 실행해둔 상태로 이 `test.py`를 실행하세요.

import requests
import json

BASE_URL = 'http://127.0.0.1:5000'  # Flask 서버 주소

def print_response(response):
    """응답의 상태 코드와 내용을 출력하는 함수"""
    print(f'Status Code: {response.status_code}')
    try:
        print('Response JSON:', json.dumps(response.json(), indent=2))
    except json.JSONDecodeError:
        print('Response Text:', response.text)
    print('-' * 50)

def test_add_todo():
    """POST /todo - 새 할 일 추가 테스트"""
    print('Testing: POST /todo')
    title = input("Enter the title of the new todo: ")
    description = input("Enter the description of the new todo: ")
    payload = {
        'title': title,
        'description': description
    }
    response = requests.post(f'{BASE_URL}/todo', json=payload)
    print_response(response)

def test_get_todo():
    """GET /todo/<id> - 특정 할 일 가져오기"""
    todo_id = input("Enter the ID of the todo: ")
    print(f'Testing: GET /todo/{todo_id}')
    response = requests.get(f'{BASE_URL}/todo/{todo_id}')
    print_response(response)

def test_update_todo():
    """PUT /todo/<id> - 할 일 업데이트 테스트"""
    todo_id = input("Enter the ID of the todo: ")
    print(f'Testing: PUT /todo/{todo_id}')
    title = input("Enter the new title of the todo: ")
    description = input("Enter the new description of the todo: ")
    completed = input("Is the todo completed? (yes/no): ").lower() == 'yes'
    payload = {
        'title': title,
        'description': description,
        'completed': completed
    }
    response = requests.put(f'{BASE_URL}/todo/{todo_id}', json=payload)
    print_response(response)

def test_delete_todo():
    """DELETE /todo/<id> - 할 일 삭제 테스트"""
    todo_id = input("Enter the ID of the todo: ")
    print(f'Testing: DELETE /todo/{todo_id}')
    response = requests.delete(f'{BASE_URL}/todo/{todo_id}')
    print_response(response)

def test_get_all_todos():
    """GET /todos - 모든 할 일 가져오기 테스트"""
    print('Testing: GET /todos')
    response = requests.get(f'{BASE_URL}/todos')
    print_response(response)

def test_get_completed_todos():
    """GET /todos/completed - 완료된 할 일 가져오기 테스트"""
    print('Testing: GET /todos/completed')
    response = requests.get(f'{BASE_URL}/todos/completed')
    print_response(response)

def test_get_sorted_todos():
    """GET /todos/sorted - 정렬된 할 일 가져오기 테스트"""
    print('Testing: GET /todos/sorted')
    response = requests.get(f'{BASE_URL}/todos/sorted')
    print_response(response)

def test_get_paginated_todos():
    """GET /todos/paginated?page=1&per_page=10 - 페이지별 할 일 가져오기 테스트"""
    page = input("Enter the page number: ")
    per_page = input("Enter the number of items per page: ")
    print(f'Testing: GET /todos/paginated?page={page}&per_page={per_page}')
    response = requests.get(f'{BASE_URL}/todos/paginated?page={page}&per_page={per_page}')
    print_response(response)

def test_search_todos():
    """GET /todos/search?keyword=<keyword> - 할 일 검색 테스트"""
    keyword = input("Enter the search keyword: ")
    print(f'Testing: GET /todos/search?keyword={keyword}')
    response = requests.get(f'{BASE_URL}/todos/search', params={'keyword': keyword})
    print_response(response)

def main():
    while True:
        print("\nSelect an action to perform:")
        print("1. Add a new todo (POST /todo)")
        print("2. Get a todo by ID (GET /todo/<id>)")
        print("3. Update a todo by ID (PUT /todo/<id>)")
        print("4. Delete a todo by ID (DELETE /todo/<id>)")
        print("5. Get all todos (GET /todos)")
        print("6. Get completed todos (GET /todos/completed)")
        print("7. Get sorted todos (GET /todos/sorted)")
        print("8. Get paginated todos (GET /todos/paginated)")
        print("9. Search todos by keyword (GET /todos/search)")
        print("10. Exit")

        choice = input("Enter the number of the action you want to perform: ")

        if choice == '1':
            test_add_todo()
        elif choice == '2':
            test_get_todo()
        elif choice == '3':
            test_update_todo()
        elif choice == '4':
            test_delete_todo()
        elif choice == '5':
            test_get_all_todos()
        elif choice == '6':
            test_get_completed_todos()
        elif choice == '7':
            test_get_sorted_todos()
        elif choice == '8':
            test_get_paginated_todos()
        elif choice == '9':
            test_search_todos()
        elif choice == '10':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
