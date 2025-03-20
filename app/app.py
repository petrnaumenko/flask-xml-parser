from flask import Flask
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
app.config['DATABASE'] = os.path.join(BASE_DIR, 'instance', 'database.db')
print(app.config['DATABASE'])

from app.routes.file_routes import file_bp
from app.routes.tag_routes import tag_bp


app.register_blueprint(file_bp)
app.register_blueprint(tag_bp)


if __name__ == "__main__":
    app.run(debug=True)