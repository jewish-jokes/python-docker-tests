import pytest

from classes.DB.db import Database


@pytest.fixture()
def database_instance():
    db = Database()
    db.connect()
    yield db
    db.close()
