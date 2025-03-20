from app.database import get_db_cursor


def get_tag_count(file_name, tag_name):
    """Получение количества тегов в файле."""
    with get_db_cursor() as cursor:
        query = """
            SELECT COUNT(*)
            FROM Tags
            JOIN Files ON Tags.file_id = Files.id
            WHERE Tags.name = ?
              AND Files.name = ?
        """
        cursor.execute(query, (tag_name, file_name))
        result = cursor.fetchone()
        if result and result[0] > 0:
            return result[0]
        else:
            raise ValueError("Tag not found")


def get_tag_attributes(file_name, tag_name):
    """Получение списка атрибутов тега."""
    with get_db_cursor() as cursor:
        query = """
            SELECT DISTINCT Tags.id, Attributes.name
            FROM Tags
            LEFT JOIN Attributes ON Attributes.tag_id = Tags.id
            JOIN Files ON Tags.file_id = Files.id
            WHERE Tags.name = ? AND Files.name = ?
        """
        cursor.execute(query, (tag_name, file_name))
        result = cursor.fetchall()
        if not (result and result[0]['id']):
             raise ValueError("Tag not found")
        return [row["name"] for row in result if row["name"] is not None]
    