from flask import Flask
from app.config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from app.routes import main
    app.register_blueprint(main)
    db.init_app(app)
    return app

app = create_app()
migrate = Migrate(app, db)

from app import routes,models

if __name__ == "__main__":
    app.run(debug=True)
