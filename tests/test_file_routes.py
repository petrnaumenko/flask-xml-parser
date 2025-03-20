import pytest
from io import BytesIO
import os
from werkzeug.datastructures import FileStorage


def print_table_contents(cursor, table_name, print_logs=False):
    """Функция для вывода содержимого таблицы на экран, если передан параметр print_logs."""
    if print_logs:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        print(f"\nСодержимое таблицы {table_name}:")
        for row in rows:
            print(dict(row))  # Преобразуем строки в словари для лучшего вывода


def test_file_upload(client, db_cursor, request):
    """Тест для проверки содержимого базы данных с возможностью вывода логов."""

    # Получаем параметр --log из командной строки
    log_param = request.config.getoption("--log")

    # Получаем текущий рабочий каталог
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Формируем путь к файлу
    file_path = os.path.join(current_directory, 'test.xml')

    # Открываем файл
    with open(file_path, 'rb') as file:
        # Создаем объект FileStorage
        test_file = FileStorage(file, filename='test.xml')

        response = client.post(
            '/api/file/read',
            data={'file': test_file}
        )

    assert response.status_code == 200
    assert response.json == {'success': True}

    # Если передан параметр --log, печатаем на экран содержимое таблиц
    if log_param:
        print_table_contents(db_cursor, "Files", print_logs=True)
        print_table_contents(db_cursor, "Tags", print_logs=True)
        print_table_contents(db_cursor, "Attributes", print_logs=True)

    # Проверяем данные в базе данных
    db_cursor.execute("SELECT * FROM Files")
    files = db_cursor.fetchall()
    assert len(files) == 1
    assert files[0]['name'] == 'test.xml'

    db_cursor.execute("SELECT * FROM Tags")
    tags = db_cursor.fetchall()
    assert len(tags) == 11 
    assert tags[0]['name'] == 'root'
    assert tags[1]['name'] == 'tag1'
    assert tags[2]['name'] == 'child1'
    assert tags[3]['name'] == 'child2'
    assert tags[4]['name'] == 'tag2'
    assert tags[5]['name'] == 'child3'
    assert tags[6]['name'] == 'tag3'
    assert tags[7]['name'] == 'child4'

    db_cursor.execute("SELECT * FROM Attributes WHERE tag_id = ?", (tags[1]['id'],))  # tag1
    attributes = db_cursor.fetchall()
    assert len(attributes) == 2  # Для tag1 два атрибута
    assert attributes[0]['name'] == 'name'
    assert attributes[0]['value'] == 'attr1'
    assert attributes[1]['name'] == 'value'
    assert attributes[1]['value'] == 'value1'

    db_cursor.execute("SELECT * FROM Attributes WHERE tag_id = ?", (tags[4]['id'],))  # tag2
    attributes = db_cursor.fetchall()
    assert len(attributes) == 2  # Для tag2 два атрибута
    assert attributes[0]['name'] == 'name'
    assert attributes[0]['value'] == 'attr2'
    assert attributes[1]['name'] == 'value'
    assert attributes[1]['value'] == 'value2'

    db_cursor.execute("SELECT * FROM Attributes WHERE tag_id = ?", (tags[7]['id'],))  # child4 (tag3)
    attributes = db_cursor.fetchall()
    assert len(attributes) == 1  # Для child4 один атрибут
    assert attributes[0]['name'] == 'type'
    assert attributes[0]['value'] == 'type4'


def test_get_tag_count(client, request):
    """Тест для получения количества вхождений тега в файл."""
    response = client.get('/api/tags/get-count', query_string={'file_name': 'test.xml', 'tag_name': 'tag1'})
    assert response.status_code == 200
    data = response.json
    assert 'count' in data
    assert data['count'] == 2  # Тег 'tag1' встречается 1 раз в файле

    response = client.get('/api/tags/get-count', query_string={'file_name': 'test.xml', 'tag_name': 'child1'})
    assert response.status_code == 200
    data = response.json
    assert 'count' in data
    assert data['count'] == 3  # Тег 'child1' встречается 1 раз в файле

    response = client.get('/api/tags/get-count', query_string={'file_name': 'test.xml', 'tag_name': 'child2'})
    assert response.status_code == 200
    data = response.json
    assert 'count' in data
    assert data['count'] == 1  # Тег 'child2' встречается 1 раз в файле

    response = client.get('/api/tags/get-count', query_string={'file_name': 'test.xml', 'tag_name': 'nonexistent_tag'})
    assert response.status_code == 404
    assert response.json == {'error': 'Tag not found'}


def test_get_tag_count_missing_parameters(client):
    """Тест для проверки ошибки при отсутствии обязательных параметров file_name или tag_name."""
    response = client.get('/api/tags/get-count', query_string={'tag_name': 'tag1'})
    assert response.status_code == 400
    assert response.json == {'error': 'File name and tag name are required'}
    
    response = client.get('/api/tags/get-count', query_string={'file_name': 'test.xml'})
    assert response.status_code == 400
    assert response.json == {'error': 'File name and tag name are required'}


def test_get_tag_attributes(client):
    """Тест для получения атрибутов указанного тега в файле."""
    response = client.get('/api/tags/attributes/get', query_string={'file_name': 'test.xml', 'tag_name': 'tag1'})
    assert response.status_code == 200
    data = response.json
    assert 'attributes' in data
    assert isinstance(data['attributes'], list)
    assert len(data['attributes']) > 0
    assert 'name' in data['attributes']
    assert 'value' in data['attributes']

    response = client.get('/api/tags/attributes/get', query_string={'file_name': 'test.xml', 'tag_name': 'child1'})
    assert response.status_code == 200
    data = response.json
    assert 'attributes' in data
    assert len(data['attributes']) == 3
    assert 'type1' in data['attributes']
    assert 'type2' in data['attributes']

    response = client.get('/api/tags/attributes/get', query_string={'file_name': 'test.xml', 'tag_name': 'nonexistent_tag'})
    assert response.status_code == 404
    assert response.json == {'error': 'Tag not found'}

    response = client.get('/api/tags/attributes/get', query_string={'file_name': 'test.xml', 'tag_name': 'root'})
    print(response.json)
    assert response.status_code == 200
    assert response.json == {'attributes': []}
 

def test_get_tag_attributes_missing_parameters(client):
    """Тест для проверки ошибки при отсутствии обязательных параметров file_name или tag_name."""
    response = client.get('/api/tags/attributes/get', query_string={'tag_name': 'tag1'})
    assert response.status_code == 400
    assert response.json == {'error': 'File name and tag name are required'}
    
    response = client.get('/api/tags/attributes/get', query_string={'file_name': 'test.xml'})
    assert response.status_code == 400
    assert response.json == {'error': 'File name and tag name are required'}