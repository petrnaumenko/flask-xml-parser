# Flask XML Parser

Это приложение на Flask для обработки XML файлов. Оно предоставляет несколько API-эндпоинтов для работы с тегами и атрибутами в XML файлах.

## Как скопировать репозиторий

Чтобы склонировать репозиторий, выполните следующую команду:

```bash
git clone https://github.com/petrnaumenko/flask-xml-parser.git
cd flask-xml-parser
```

## Установка зависимостей

1. Убедитесь, что у вас установлен Python 3.10 и выше.
2. Установите виртуальное окружение (если не установлено):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Для Linux/Mac
    venv\Scripts\activate     # Для Windows
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

## Запуск тестов

Для запуска тестов используйте `pytest`:

```bash
pytest tests/
```

## Запуск приложения с Docker Compose

Приложение можно запустить с использованием Docker Compose. Для этого выполните следующие шаги:

1. Соберите контейнеры и запустите приложение:

    ```bash
    docker-compose up --build
    ```

2. После успешного запуска контейнеров приложение будет доступно на порту `5000`.

## Проверка приложения с использованием curl

Теперь вы можете проверять работу API с помощью `curl`. Зайдите в папку flask-xml-parser и используйте следующие команды для тестирования:

### Загрузка файла

Для того чтобы загрузить XML файл с использованием POST запроса:

```bash
curl -X POST http://localhost:5000/api/file/read -F "file=@./tests/test.xml"
```

### Получение количества вхождений тега

Для получения количества вхождений тега в XML файле:

```bash
curl -X GET "http://localhost:5000/api/tags/get-count?file_name=test.xml&tag_name=tag1"
```

### Получение атрибутов тега

Для получения атрибутов указанного тега в XML файле:

```bash
curl -X GET "http://localhost:5000/api/tags/attributes/get?file_name=test.xml&tag_name=tag1"
```

## Заметки

- Если при запуске `curl` возникает ошибка типа "Connection refused", убедитесь, что Docker контейнеры успешно запустились, и приложение Flask работает на порту `5000`.
- Параметры для `file_name` и `tag_name` должны быть указаны корректно, иначе вы получите ошибку с сообщением "Tag not found" или "File name and tag name are required".
  