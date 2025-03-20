import xml.sax
from app.database import get_db_cursor


class FileHandler(xml.sax.ContentHandler):
    """SAX-обработчик для парсинга XML-файлов."""
    def __init__(self, filename):
        super().__init__()
        self.current_tag = ""
        self.current_attrs = {}
        self.file_id = None
        self.tag_id = None
        self.filename = filename
        self.create_file_record()

    def create_file_record(self):
        """Сохраняем запись о файле в базу данных."""
        with get_db_cursor() as cursor:
            cursor.execute("INSERT INTO Files (name) VALUES (?)", (self.filename,))
            self.file_id = cursor.lastrowid
            print(f"Запись о файле добавлена с ID: {self.file_id}")

    def startElement(self, tag, attrs):
        self.current_tag = tag
        self.current_attrs = dict(attrs)
        self.save_tag_and_attrs()

    def save_tag_and_attrs(self):
        """Сохраняем теги и атрибуты для каждого элемента."""
        with get_db_cursor() as cursor:
            cursor.execute(
                "INSERT INTO Tags (name, file_id) VALUES (?, ?)",
                (self.current_tag, self.file_id)
            )
            self.tag_id = cursor.lastrowid
            print(f"Запись о теге добавлена с ID: {self.tag_id} для тега: {self.current_tag}")
            for name, value in self.current_attrs.items():
                cursor.execute(
                    "INSERT INTO Attributes (name, value, tag_id) VALUES (?, ?, ?)",
                    (name, value, self.tag_id)
                )
                print(f"Запись о атрибуте добавлена: {name} = {value} для тега ID {self.tag_id}")


def read_xml_file(file_stream, filename):
    """Чтение XML-файла из потока и сохранение данных в базу данных."""
    try:
        parser = xml.sax.make_parser()
        handler = FileHandler(filename)
        parser.setContentHandler(handler)
        parser.parse(file_stream)
        return True
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return False