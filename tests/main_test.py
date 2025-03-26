
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash

import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import create_app, db
from app.models import Account, Comment, Utilities, Guides
from flask import session
from flask_sqlalchemy import SQLAlchemy

lroutes = [
    "/account",
    "/community",
    "/guides",
    "/guides",
    "/help",
    "/",
    "/login",
    "/logout",
    "/singup",
    "/site_structure",
    "/utilites"
]

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test_secret"
    })
    from app import routes, models
    with app.app_context():
        db.create_all()
        new_account = Account(nickname = "admin", email = "admin@gmail.com", hash_passwd=generate_password_hash("nimda"))
        db.session.add(new_account)
        db.session.commit()
        yield app
        db.drop_all()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def client(app):
    return app.test_client()

def test_all_page(client):
    """Перевіряє сторінки"""
    with client.session_transaction() as sess:
        sess["authorize"] = True
        sess["nickname"] = "admin"
    for page in lroutes:
        response = client.get(page)
        assert response.status_code == 200 or 302, page
        print(page)

